#!/usr/bin/env node
/**
 * check_sync_local.mjs — README / 官网 / sitemap 一致性本地校验（Node 版）
 *
 * 本机没有 Python 时，用 Node 复刻 scripts/sync_readme_to_site.py 的解析规则，
 * 只做只读校验，不写入任何文件：
 *
 *   1. 复算精选技能总数（按 URL 去重），用于核对 README 首屏、badge、官网统计；
 *   2. 校验各分类表格列数是否一致（避免 Markdown 表格被破坏）；
 *   3. 校验各分类条目数、原创技能数量；
 *   4. 校验 README badge、官网统计栏、官网 Hero badge、sitemap lastmod 的公开日期一致。
 *
 * 真正的同步仍以 scripts/sync_readme_to_site.py 为准（CI 中运行）。
 *
 * 用法：
 *   node scripts/check_sync_local.mjs
 */

import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const README_PATH = join(REPO_ROOT, "README.md");
const HTML_PATH = join(REPO_ROOT, "docs", "index.html");
const SITEMAP_PATH = join(REPO_ROOT, "docs", "sitemap.xml");
const SKILLS_ROOT = join(REPO_ROOT, "skills");

const CATEGORY_ORDER = ["star", "platform", "dev", "creative", "agent", "finance", "chinese"];
const CATEGORY_LABELS = {
  star: "热门与高潜",
  platform: "平台运营",
  dev: "开发效率（含学术科研）",
  creative: "内容创作",
  agent: "AI Agent",
  finance: "金融/商业",
  chinese: "中文专属",
};

/** 与 sync_readme_to_site.py 的 classify_header 保持一致的分类判定。 */
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

/** 拆分行内表格单元格，保留列数（含首尾空串），用于列数一致性检查。 */
function splitRow(line) {
  return line.split("|").slice(1, -1);
}

function parseReadme(readme) {
  const sections = new Map();
  const problems = [];
  let currentKey = null;
  let currentHeader = null;
  let headerColumns = null;

  for (const [index, rawLine] of readme.split("\n").entries()) {
    const line = rawLine.trim();
    const headerKey = classifyHeader(line);

    if (headerKey !== null) {
      currentKey = headerKey === "academic" ? "dev" : headerKey;
      currentHeader = line;
      headerColumns = null;
      if (!sections.has(currentKey)) {
        sections.set(currentKey, { header: line, rows: [] });
      }
      sections.get(currentKey).header = line;
      continue;
    }

    if (line.startsWith("## ") || (line.startsWith("### ") && currentKey !== null)) {
      currentKey = null;
      currentHeader = null;
      headerColumns = null;
      continue;
    }

    if (currentKey !== null && line.startsWith("|")) {
      const cells = splitRow(line);
      if (headerColumns === null) {
        headerColumns = cells.length;
      } else if (cells.length !== headerColumns) {
        problems.push(
          `${currentHeader} 第 ${index + 1} 行列数为 ${cells.length}，` +
            `与表头 ${headerColumns} 列不一致：${line.slice(0, 80)}`,
        );
      }
      sections.get(currentKey).rows.push({ cells, line, lineNumber: index + 1 });
    }
  }

  const skills = new Map();
  for (const key of CATEGORY_ORDER) {
    skills.set(key, []);
  }

  // 与 sync_readme_to_site.py 的 parse_table 保持一致：
  // 跳过表头 / 分隔行，以及首列不含链接的行（例如原创技能列表的 skills/ 相对链接）。
  const isHeaderRow = (firstCell) =>
    ["技能", "说明", "---", "为什么"].some((keyword) => firstCell.includes(keyword));

  for (const [key, section] of sections) {
    for (const { cells } of section.rows) {
      const first = (cells[0] ?? "").trim();
      if (isHeaderRow(first)) continue;
      if (!first.includes("[")) continue;
      const match = first.match(/\[([^\]]+)\]\(([^)]+)\)/);
      if (!match) {
        problems.push(`${section.header} 出现无法解析的条目：${first.slice(0, 60)}`);
        continue;
      }
      skills.get(key).push({ name: match[1].trim(), url: match[2].trim() });
    }
  }

  return { sections, skills, problems };
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

function uniqueTotal(skills) {
  const urls = new Set();
  for (const key of CATEGORY_ORDER) {
    for (const item of skills.get(key) ?? []) urls.add(item.url);
  }
  return urls.size;
}

function uniqueGithubRepos(skills) {
  const repos = new Set();
  for (const key of CATEGORY_ORDER) {
    for (const item of skills.get(key) ?? []) {
      const match = item.url.match(/^https?:\/\/(?:www\.)?github\.com\/([^/]+)\/([^/?#]+)/i);
      if (match) repos.add(`${match[1]}/${match[2].replace(/\.git$/, "")}`.toLowerCase());
    }
  }
  return repos;
}

function readDate(content, pattern, label, problems) {
  const matches = [...content.matchAll(pattern)];
  if (matches.length !== 1) {
    problems.push(`${label} 日期锚点期望 1 处，实际 ${matches.length} 处`);
    return null;
  }
  return matches[0][1].replaceAll("--", "-");
}

function main() {
  const readme = readFileSync(README_PATH, "utf8");
  const html = readFileSync(HTML_PATH, "utf8");
  const sitemap = readFileSync(SITEMAP_PATH, "utf8");

  const { skills, problems } = parseReadme(readme);
  const total = uniqueTotal(skills);
  const repos = uniqueGithubRepos(skills);
  const original = countOriginalSkills();

  console.log("📊 分类条目数：");
  for (const key of CATEGORY_ORDER) {
    console.log(`   ${key.padEnd(9)} ${String((skills.get(key) ?? []).length).padStart(3)}  （${CATEGORY_LABELS[key]}）`);
  }
  console.log(`   合计（按 URL 去重）: ${total}`);
  console.log(`   GitHub 仓库数（去重）: ${repos.size}`);
  console.log(`   原创技能（skills/*/SKILL.md）: ${original}`);

  console.log("\n🔎 公开数字一致性：");
  const checks = [
    ["README Skills badge", readme, /badge\/skills-(\d+)%2B-green\.svg/],
    ["README 首屏精选", readme, /精选 (\d+)\+ \|/],
    ["HTML Hero 精选 badge", html, /✅ (\d+)\+ 精选技能/],
    ["HTML 统计栏精选", html, /<h3>(\d+)\+<\/h3>\s*<p>精选技能<\/p>/],
  ];
  for (const [label, content, pattern] of checks) {
    const match = content.match(pattern);
    if (!match) {
      problems.push(`${label} 未找到`);
      continue;
    }
    const value = Number(match[1]);
    const ok = value === total;
    console.log(`   ${ok ? "✅" : "❌"} ${label} = ${value}（应为 ${total}）`);
    if (!ok) problems.push(`${label} = ${value}，应为 ${total}`);
  }

  const originalChecks = [
    ["HTML Hero 原创 badge", html, /🎁 (\d+) 个原创技能/],
    ["HTML 统计栏原创", html, /<h3>(\d+)<\/h3>\s*<p>原创技能<\/p>/],
  ];
  for (const [label, content, pattern] of originalChecks) {
    const match = content.match(pattern);
    if (!match) {
      problems.push(`${label} 未找到`);
      continue;
    }
    const value = Number(match[1]);
    const ok = value === original;
    console.log(`   ${ok ? "✅" : "❌"} ${label} = ${value}（应为 ${original}）`);
    if (!ok) problems.push(`${label} = ${value}，应为 ${original}`);
  }

  const dates = {
    "README Updated badge": readDate(
      readme,
      /badge\/updated-(\d{4}--\d{2}--\d{2})-brightgreen\.svg/g,
      "README Updated badge",
      problems,
    ),
    "HTML 统计栏最近更新": readDate(
      html,
      /<h3>(\d{4}-\d{2}-\d{2})<\/h3>\s*<p>最近更新<\/p>/g,
      "HTML 最近更新",
      problems,
    ),
    "HTML Hero 更新 badge": readDate(
      html,
      /🔄 更新于 (\d{4}-\d{2}-\d{2})<\/span>/g,
      "HTML Hero 更新 badge",
      problems,
    ),
    "sitemap lastmod": readDate(
      sitemap,
      /<loc>https:\/\/claude-skills\.bt199\.com\/<\/loc>\s*<lastmod>(\d{4}-\d{2}-\d{2})<\/lastmod>/g,
      "sitemap lastmod",
      problems,
    ),
  };
  const dateValues = new Set(Object.values(dates).filter(Boolean));
  console.log(`   公开日期: ${[...dateValues].join(", ") || "（未读取到）"}`);
  if (dateValues.size !== 1) {
    problems.push(`公开日期不一致：${JSON.stringify(dates)}`);
  }

  console.log("\n🧹 表格结构：");
  if (problems.length === 0) {
    console.log("   ✅ 所有分类表格列数一致，条目均可解析");
  } else {
    for (const problem of problems) console.log(`   ❌ ${problem}`);
  }

  if (problems.length > 0) {
    console.error(`\n❌ 校验未通过：${problems.length} 个问题`);
    process.exit(1);
  }
  console.log("\n✅ 本地等效校验通过（行数、数量、日期均一致）");
}

main();
