#!/usr/bin/env node
/**
 * sync_readme_to_site.mjs — README → docs/index.html / docs/sitemap.xml 同步（Node 版）
 *
 * 与 scripts/sync_readme_to_site.py 等价：本机没有 Python 时用它完成同一套同步，
 * 并复刻脚本的“严格唯一锚点”策略——任何锚点缺失或重复都直接失败，绝不半写。
 *
 * 同步内容：
 *   1. docs/index.html 的 skillsData 数据块
 *   2. 官网统计栏（精选技能 / 原创技能 / GitHub Stars / 最近更新）
 *   3. 官网 Hero badge 数字与更新日期
 *   4. 官网 meta / og / twitter description 中的数量
 *   5. docs/sitemap.xml 首页 lastmod
 *   6. README badge（skills 数量、updated 日期）与首屏精选数量
 *
 * star 刷新不在本脚本范围内：它需要联网调用 GitHub GraphQL，由 CI 中的
 * scripts/sync_readme_to_site.py --fetch-stars 完成。本脚本保留 README 中的
 * 现有 star 数值，不做任何猜测。
 *
 * 用法：
 *   node scripts/sync_readme_to_site.mjs [--dry-run] [--project-date YYYY-MM-DD]
 */

import { readFileSync, writeFileSync, statSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const README_PATH = join(REPO_ROOT, "README.md");
const HTML_PATH = join(REPO_ROOT, "docs", "index.html");
const SITEMAP_PATH = join(REPO_ROOT, "docs", "sitemap.xml");
const SKILLS_ROOT = join(REPO_ROOT, "skills");
const SITE_HOME_URL = "https://claude-skills.bt199.com/";
const TIMEZONE_OFFSET_HOURS = 8; // Asia/Shanghai

const CATEGORY_ORDER = ["star", "platform", "dev", "creative", "agent", "finance", "chinese"];

const argv = process.argv.slice(2);
const DRY_RUN = argv.includes("--dry-run");
const dateFlagIndex = argv.indexOf("--project-date");
const PROJECT_DATE =
  dateFlagIndex >= 0 && argv[dateFlagIndex + 1]
    ? argv[dateFlagIndex + 1]
    : currentProjectDate();

function currentProjectDate() {
  const now = new Date();
  const shifted = new Date(now.getTime() + TIMEZONE_OFFSET_HOURS * 3600 * 1000);
  return shifted.toISOString().slice(0, 10);
}

function fail(message) {
  throw new Error(message);
}

/** 严格替换唯一锚点；缺失或重复都拒绝继续写入（对应 Python 的 _replace_exact）。 */
function replaceExact(content, pattern, replacement, label) {
  const matches = [...content.matchAll(new RegExp(pattern, "gm"))];
  if (matches.length !== 1) {
    fail(`${label} 替换失败：期望 1 处，实际找到 ${matches.length} 处`);
  }
  const match = matches[0];
  const value = typeof replacement === "function" ? replacement(match) : replacement;
  return content.slice(0, match.index) + value + content.slice(match.index + match[0].length);
}

// ── 解析 README（与 sync_readme_to_site.py 的解析规则一致）─────────────────────

function classifyHeader(line) {
  const text = line.trim();
  if (!text.startsWith("### ")) return null;
  if (text.includes("🏆") && (text.includes("万星") || text.includes("热门与高潜"))) return "star";
  if (text.includes("平台运营") || text.includes("自媒体")) return "platform";
  if (text.includes("💻") && text.includes("开发效率")) return "dev";
  if (text.includes("🎨") && text.includes("内容创作")) return "creative";
  if (text.includes("🔬") && text.includes("学术科研")) return "academic";
  if (text.includes("🤖") && text.includes("Agent")) return "agent";
  if (text.includes("💰") && (text.includes("金融") || text.includes("商业"))) return "finance";
  if (text.includes("🌏") && text.includes("中文专属")) return "chinese";
  return null;
}

function extractGithubUrl(url) {
  const text = url.trim();
  if (text.includes("gh-proxy.com")) {
    const match = text.match(/github\.com\/([^)]+)/);
    if (match) return `https://github.com/${match[1]}`;
  }
  return text;
}

/** 与 Python 的 format_stars 一致：去尾 +，K 结尾补 +，>=1000 转 K+。 */
function formatStars(raw) {
  if (!raw) return "";
  let stars = String(raw).trim().replace(/\+$/, "");
  if (/[Kk]/.test(stars)) return `${stars}+`;
  const num = Number(stars.replace(/,/g, ""));
  if (Number.isFinite(num)) {
    if (num >= 1000) {
      const value = (num / 1000).toFixed(1).replace(/\.0$/, "");
      return `${value}K+`;
    }
    return stars;
  }
  return stars;
}

function parseStarsFromDesc(desc) {
  const patterns = [
    /[（(]\s*([\d,.]+K?)\+?\s*⭐\s*[）)]\s*$/,
    /\s*⭐\s*([\d,.]+K?)\+?\s*$/,
  ];
  for (const pattern of patterns) {
    const match = desc.match(pattern);
    if (match) {
      const clean = desc.slice(0, match.index).trim().replace(/[｜|]+$/, "");
      return [clean, match[1].trim()];
    }
  }
  return [desc.trim(), ""];
}

function parseReadme(readme) {
  const sections = new Map();
  let currentKey = null;

  for (const rawLine of readme.split("\n")) {
    const line = rawLine.trim();
    const headerKey = classifyHeader(line);
    if (headerKey !== null) {
      currentKey = headerKey === "academic" ? "dev" : headerKey;
      if (!sections.has(currentKey)) sections.set(currentKey, []);
      continue;
    }
    if (line.startsWith("## ") || (line.startsWith("### ") && currentKey !== null)) {
      currentKey = null;
      continue;
    }
    if (currentKey !== null && line.startsWith("|")) {
      sections.get(currentKey).push(line);
    }
  }

  const skillsData = {};
  for (const [key, tableLines] of sections) {
    const items = [];
    for (const line of tableLines) {
      const cells = line
        .split("|")
        .map((cell) => cell.trim())
        .filter((cell) => cell !== "");
      if (cells.length === 0) continue;
      if (["技能", "说明", "---", "为什么"].some((kw) => cells[0].includes(kw))) continue;
      if (!cells[0].includes("[")) continue;

      const link = cells[0].match(/\[([^\]]+)\]\(([^)]+)\)/);
      if (!link) continue;
      const name = link[1].trim();
      const url = extractGithubUrl(link[2].trim());
      if (!/^https?:\/\//.test(url)) fail(`技能 ${name} 的 URL 非法：${url}`);

      let desc = cells[1] ?? "";
      let stars = "";
      if (key === "star" && cells.length >= 3) {
        stars = formatStars(cells[2]);
        desc = desc.replace(/\s*[（(][\d,.]+K?\s*⭐\s*[）)]\s*$/, "");
      } else {
        const [clean, rawStars] = parseStarsFromDesc(desc);
        desc = clean;
        stars = formatStars(rawStars);
      }
      items.push({ name, stars, desc: desc.trim(), url });
    }
    if (items.length > 0) skillsData[key] = items;
  }
  return skillsData;
}

// ── 生成 skillsData JavaScript ────────────────────────────────────────────────

function escapeJsString(value) {
  return String(value)
    .replace(/\\/g, "\\\\")
    .replace(/'/g, "\\'")
    .replace(/\r\n?/g, " ")
    .replace(/\n/g, " ")
    .replace(/</g, "\\u003C")
    .replace(/>/g, "\\u003E")
    .replace(/&/g, "\\u0026")
    .replace(/\u2028/g, "\\u2028")
    .replace(/\u2029/g, "\\u2029");
}

function generateSkillsJs(skillsData) {
  const lines = ["const skillsData = {"];
  for (const key of CATEGORY_ORDER) {
    const items = skillsData[key] ?? [];
    lines.push(`  ${key}: [`);
    for (const item of items) {
      const parts = [`name:'${escapeJsString(item.name)}'`];
      if (item.stars) parts.push(`stars:'${escapeJsString(item.stars)}'`);
      parts.push(`desc:'${escapeJsString(item.desc)}'`);
      parts.push(`url:'${escapeJsString(item.url)}'`);
      if (key === "star") parts.push("tag:'star'");
      lines.push(`    {${parts.join(",")}},`);
    }
    lines.push("  ],");
  }
  lines.push("};");
  return lines.join("\n");
}

function countTotalSkills(skillsData) {
  const urls = new Set();
  for (const items of Object.values(skillsData)) {
    for (const item of items) urls.add(item.url);
  }
  return urls.size;
}

function countOriginalSkills() {
  return readdirSync(SKILLS_ROOT)
    .filter((name) => statSync(join(SKILLS_ROOT, name)).isDirectory())
    .filter((name) => {
      try {
        return statSync(join(SKILLS_ROOT, name, "SKILL.md")).isFile();
      } catch {
        return false;
      }
    }).length;
}

// ── 生成三份输出 ──────────────────────────────────────────────────────────────

function replaceSkillsData(html, skillsJs) {
  const match = html.match(/const skillsData = \{[\s\S]*?\};/);
  if (!match) fail("skillsData 替换失败：未找到数据块");
  const before = html.slice(0, match.index);
  if (before.includes("const skillsData")) fail("skillsData 替换失败：数据块不唯一");
  const newline = match[0].includes("\r\n") ? "\r\n" : "\n";
  const normalized = skillsJs.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  return html.slice(0, match.index) + normalized.replace(/\n/g, newline) + html.slice(match.index + match[0].length);
}

function updateHtml(html, { totalSkills, totalOriginal, repoStars, updateDate }) {
  html = replaceExact(
    html,
    "(<h3>)\\d+\\+(</h3>\\s*<p>精选技能</p>)",
    (m) => `${m[1]}${totalSkills}+${m[2]}`,
    "HTML 精选技能统计",
  );
  html = replaceExact(
    html,
    "(<h3>)\\d+(</h3>\\s*<p>原创技能</p>)",
    (m) => `${m[1]}${totalOriginal}${m[2]}`,
    "HTML 原创技能统计",
  );
  html = replaceExact(
    html,
    "(<h3>)\\d+(</h3>\\s*<p>GitHub Stars</p>)",
    (m) => `${m[1]}${repoStars}${m[2]}`,
    "HTML GitHub Stars 统计",
  );
  html = replaceExact(
    html,
    "(<span class=\"badge green\">)✅ \\d+\\+ 精选技能(</span>)",
    (m) => `${m[1]}✅ ${totalSkills}+ 精选技能${m[2]}`,
    "HTML Hero 精选技能 badge",
  );
  html = replaceExact(
    html,
    "(<span class=\"badge purple\">)🎁 \\d+ 个原创技能(</span>)",
    (m) => `${m[1]}🎁 ${totalOriginal} 个原创技能${m[2]}`,
    "HTML Hero 原创技能 badge",
  );
  html = replaceExact(
    html,
    "(<span class=\"badge orange\">)⭐ \\d+ Stars(</span>)",
    (m) => `${m[1]}⭐ ${repoStars} Stars${m[2]}`,
    "HTML Hero GitHub Stars badge",
  );

  const description =
    `最实用的 Claude Code Skills / Agents / Plugins 中文精选集，收录 ${totalSkills}+ 高质量技能、Agent 和插件，` +
    `${totalOriginal} 个原创技能，适合 Claude Code、Codex、Gemini CLI、Cursor 用户复制即装。`;
  html = replaceExact(
    html,
    "<meta name=\"description\" content=\"[^\"]*\">",
    `<meta name="description" content="${description}">`,
    "HTML meta description",
  );
  html = replaceExact(
    html,
    "<meta property=\"og:description\" content=\"[^\"]*\">",
    `<meta property="og:description" content="收录 ${totalSkills}+ Claude Code Skills / Agents / Plugins，按场景分类，中文说明，复制即装，持续更新。">`,
    "HTML og:description",
  );
  html = replaceExact(
    html,
    "<meta name=\"twitter:description\" content=\"[^\"]*\">",
    `<meta name="twitter:description" content="${totalSkills}+ 高质量 Claude Code 技能、Agent、插件中文精选，复制即装。">`,
    "HTML twitter:description",
  );

  if (updateDate) {
    html = replaceExact(
      html,
      "(<h3>)\\d{4}-\\d{2}-\\d{2}(</h3>\\s*<p>最近更新</p>)",
      (m) => `${m[1]}${PROJECT_DATE}${m[2]}`,
      "HTML 最近更新统计",
    );
    html = replaceExact(
      html,
      "(<span class=\"badge orange\">)🔄 更新于 \\d{4}-\\d{2}-\\d{2}(</span>)",
      (m) => `${m[1]}🔄 更新于 ${PROJECT_DATE}${m[2]}`,
      "HTML Hero 更新日期 badge",
    );
  } else {
    // 即使不更新日期，也要求锚点唯一，避免漏改静态区域。
    replaceExact(html, "(<h3>)\\d{4}-\\d{2}-\\d{2}(</h3>\\s*<p>最近更新</p>)", (m) => m[0], "HTML 最近更新统计");
    replaceExact(
      html,
      "(<span class=\"badge orange\">)🔄 更新于 \\d{4}-\\d{2}-\\d{2}(</span>)",
      (m) => m[0],
      "HTML Hero 更新日期 badge",
    );
  }
  return html;
}

function updateReadme(readme, { totalSkills, updateDate }) {
  readme = replaceExact(
    readme,
    "(https://img\\.shields\\.io/badge/skills-)\\d+(%2B-green\\.svg)",
    (m) => `${m[1]}${totalSkills}${m[2]}`,
    "README Skills badge",
  );
  readme = replaceExact(
    readme,
    "^(> 🚀 .*?\\| 精选 )(\\d+)(\\+ \\|.*)$",
    (m) => `${m[1]}${totalSkills}${m[3]}`,
    "README 首屏精选数量",
  );
  if (updateDate) {
    readme = replaceExact(
      readme,
      "(https://img\\.shields\\.io/badge/updated-)\\d{4}--\\d{2}--\\d{2}(-brightgreen\\.svg)",
      (m) => `${m[1]}${PROJECT_DATE.replace(/-/g, "--")}${m[2]}`,
      "README Updated badge",
    );
  } else {
    replaceExact(
      readme,
      "(https://img\\.shields\\.io/badge/updated-)\\d{4}--\\d{2}--\\d{2}(-brightgreen\\.svg)",
      (m) => m[0],
      "README Updated badge",
    );
  }
  return readme;
}

function updateSitemap(sitemap, updateDate) {
  const blocks = [...sitemap.matchAll(/<url(?:\s[^>]*)?>[\s\S]*?<\/url>/g)].map((m) => m[0]);
  const homeBlocks = blocks.filter((block) => block.includes(`<loc>${SITE_HOME_URL}</loc>`));
  if (homeBlocks.length !== 1) {
    fail(`sitemap 首页 URL 锚点校验失败：期望 1 个 ${SITE_HOME_URL}，实际找到 ${homeBlocks.length} 个`);
  }
  const block = homeBlocks[0];
  const updated = replaceExact(
    block,
    "(<lastmod>)(?:\\d{4}-\\d{2}-\\d{2})(</lastmod>)",
    (m) => (updateDate ? `${m[1]}${PROJECT_DATE}${m[2]}` : m[0]),
    "sitemap 首页 lastmod",
  );
  return sitemap.replace(block, updated);
}

function extractExistingRepoStars(html) {
  const matches = [...html.matchAll(/<h3>(\d+)<\/h3>\s*<p>GitHub Stars<\/p>/g)];
  if (matches.length > 1) {
    fail(`官网 GitHub Stars 统计锚点重复：期望至多 1 处，实际找到 ${matches.length} 处`);
  }
  return matches.length === 1 ? Number(matches[0][1]) : null;
}

function validatePublicDates(readme, html, sitemap) {
  const pick = (content, pattern, label) => {
    const matches = [...content.matchAll(new RegExp(pattern, "g"))].map((m) => m[1].replace(/--/g, "-"));
    if (matches.length !== 1) {
      fail(`${label} 日期校验失败：期望 1 处，实际找到 ${matches.length} 处`);
    }
    return matches[0];
  };
  const dates = {
    "README Updated badge": pick(readme, "badge/updated-(\\d{4}--\\d{2}--\\d{2})-brightgreen\\.svg", "README Updated badge"),
    "HTML 最近更新统计": pick(html, "<h3>(\\d{4}-\\d{2}-\\d{2})</h3>\\s*<p>最近更新</p>", "HTML 最近更新统计"),
    "HTML Hero 更新 badge": pick(html, "🔄 更新于 (\\d{4}-\\d{2}-\\d{2})</span>", "HTML Hero 更新 badge"),
    "sitemap 首页 lastmod": pick(sitemap, "<lastmod>(\\d{4}-\\d{2}-\\d{2})</lastmod>", "sitemap 首页 lastmod"),
  };
  const unique = new Set(Object.values(dates));
  if (unique.size !== 1) {
    fail(`公开日期不一致，拒绝同步：${Object.entries(dates).map(([k, v]) => `${k}=${v}`).join("，")}`);
  }
  return [...unique][0];
}

// ── 主流程 ────────────────────────────────────────────────────────────────────

function main() {
  console.log("🔄 sync_readme_to_site.mjs — 同步 README.md → docs/index.html");
  console.log();

  const originalReadme = readFileSync(README_PATH, "utf8");
  const originalHtml = readFileSync(HTML_PATH, "utf8");
  const originalSitemap = readFileSync(SITEMAP_PATH, "utf8");

  const skillsData = parseReadme(originalReadme);
  const totalSkills = countTotalSkills(skillsData);
  const totalOriginal = countOriginalSkills();
  const repoStars = extractExistingRepoStars(originalHtml);
  if (repoStars === null) fail("官网中没有可读取的 GitHub Stars");

  console.log(`   找到 ${totalSkills} 个精选技能，${totalOriginal} 个原创技能，本仓库 Star ${repoStars}`);
  for (const key of CATEGORY_ORDER) {
    console.log(`     ${key}: ${(skillsData[key] ?? []).length} 个`);
  }

  const skillsJs = generateSkillsJs(skillsData);

  // 先确认现有公开日期四处自洽，再生成不带日期变动的结果，最后统一推进日期。
  validatePublicDates(originalReadme, originalHtml, originalSitemap);

  const htmlWithoutDate = updateHtml(replaceSkillsData(originalHtml, skillsJs), {
    totalSkills,
    totalOriginal,
    repoStars,
    updateDate: false,
  });
  const readmeWithoutDate = updateReadme(originalReadme, { totalSkills, updateDate: false });
  updateSitemap(originalSitemap, false);

  const materialChanged = htmlWithoutDate !== originalHtml || readmeWithoutDate !== originalReadme;
  if (!materialChanged) {
    console.log("\n✅ 无实质变化，所有文件保持原字节");
    return;
  }

  const newHtml = updateHtml(htmlWithoutDate, { totalSkills, totalOriginal, repoStars, updateDate: true });
  const newReadme = updateReadme(readmeWithoutDate, { totalSkills, updateDate: true });
  const newSitemap = updateSitemap(originalSitemap, true);
  validatePublicDates(newReadme, newHtml, newSitemap);

  const outputs = [
    [README_PATH, originalReadme, newReadme],
    [HTML_PATH, originalHtml, newHtml],
    [SITEMAP_PATH, originalSitemap, newSitemap],
  ];

  if (DRY_RUN) {
    console.log("\n--- dry-run：将发生的变化 ---");
    for (const [path, before, after] of outputs) {
      console.log(`   ${after === before ? "无变化" : "将更新"}  ${path.replace(REPO_ROOT + "\\", "").replace(REPO_ROOT + "/", "")}`);
    }
    console.log(`\n✅ dry-run 完成，未写入文件（公开日期 ${PROJECT_DATE}）`);
    return;
  }

  for (const [path, before, after] of outputs) {
    if (after !== before) writeFileSync(path, after, "utf8");
  }
  console.log("\n🎉 同步完成！");
  console.log(`   精选技能: ${totalSkills}+`);
  console.log(`   原创技能: ${totalOriginal}`);
  console.log(`   最近更新: ${PROJECT_DATE}`);
}

main();
