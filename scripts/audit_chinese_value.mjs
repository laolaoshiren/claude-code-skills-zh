#!/usr/bin/env node
/**
 * audit_chinese_value.mjs — 只读审计：检查条目是否说明了「对中文用户的价值」
 *
 * 本项目是「Claude Code Skills 中文精选集」，中文是核心。本脚本按分类统计
 * 描述中包含中文价值信号的条目比例，并列出未说明中文价值的条目，供逐轮改进。
 *
 * 判定为「已说明中文价值」的信号（命中任意一项）：
 *   中文、简体、繁体、汉化、中文优先、国内、公众号、小红书、飞书、企业微信、
 *   微信、知乎、掘金、抖音、B 站、钉钉、QQ、台湾、中国大陆、国产、中台
 *
 * 注意：这是**建议性**审计，不作为 CI 门禁——历史条目数量大，需要逐步收敛。
 *
 * 用法：
 *   node scripts/audit_chinese_value.mjs            # 汇总 + 分类占比
 *   node scripts/audit_chinese_value.mjs --list     # 额外列出未覆盖条目
 *   node scripts/audit_chinese_value.mjs --category dev
 */

import { readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const README_PATH = join(REPO_ROOT, "README.md");

const ZH_SIGNALS = [
  /中文/,
  /简体/,
  /繁体/,
  /汉化/,
  /国内/,
  /公众号/,
  /小红书/,
  /飞书/,
  /企业微信/,
  /微信/,
  /知乎/,
  /掘金/,
  /抖音/,
  /B\s?站/,
  /Bilibili/i,
  /钉钉/,
  /\bQQ\b/i,
  /台湾/,
  /国产/,
];

const CATEGORY_LABELS = {
  star: "🏆 热门与高潜",
  platform: "📣 平台运营 / 自媒体",
  dev: "💻 开发效率（含学术科研）",
  creative: "🎨 内容创作",
  agent: "🤖 AI Agent",
  finance: "💰 金融 / 商业",
  chinese: "🌏 中文专属",
};

function classifyHeader(line) {
  const t = line.trim();
  if (!t.startsWith("### ")) return null;
  if (t.includes("🏆") && (t.includes("万星") || t.includes("热门与高潜"))) return "star";
  if (t.includes("平台运营") || t.includes("自媒体")) return "platform";
  if (t.includes("💻") && t.includes("开发效率")) return "dev";
  if (t.includes("🎨") && t.includes("内容创作")) return "creative";
  if (t.includes("🔬") && t.includes("学术科研")) return "academic";
  if (t.includes("🤖") && t.includes("Agent")) return "agent";
  if (t.includes("💰") && (t.includes("金融") || t.includes("商业"))) return "finance";
  if (t.includes("🌏") && t.includes("中文专属")) return "chinese";
  return null;
}

function parseEntries(readme) {
  const rows = [];
  let cur = null;
  readme.split("\n").forEach((raw, i) => {
    const line = raw.trim();
    const key = classifyHeader(line);
    if (key !== null) {
      cur = key === "academic" ? "dev" : key;
      return;
    }
    if (line.startsWith("## ") || (line.startsWith("### ") && cur !== null)) {
      cur = null;
      return;
    }
    if (cur === null || !line.startsWith("|")) return;
    const cells = line.split("|").slice(1, -1).map((c) => c.trim());
    if (cells.length === 0) return;
    if (["技能", "说明", "---", "为什么"].some((k) => (cells[0] ?? "").includes(k))) return;
    const m = (cells[0] ?? "").match(/\[([^\]]+)\]\(([^)]+)\)/);
    if (!m) return;
    rows.push({ category: cur, name: m[1].trim(), desc: cells[1] ?? "", line: i + 1 });
  });
  return rows;
}

function main() {
  const argv = process.argv.slice(2);
  const list = argv.includes("--list");
  const catIdx = argv.indexOf("--category");
  const onlyCat = catIdx >= 0 ? argv[catIdx + 1] : null;

  const rows = parseEntries(readFileSync(README_PATH, "utf8"));
  const hasZh = (r) => ZH_SIGNALS.some((re) => re.test(r.desc));

  const byCat = {};
  for (const r of rows) {
    byCat[r.category] ??= { total: 0, zh: 0 };
    byCat[r.category].total += 1;
    if (hasZh(r)) byCat[r.category].zh += 1;
  }

  const totalZh = rows.filter(hasZh).length;
  console.log(`总计 ${rows.length} 条，说明中文价值 ${totalZh} 条（${((totalZh / rows.length) * 100).toFixed(1)}%）\n`);
  console.log("分类占比：");
  for (const [cat, label] of Object.entries(CATEGORY_LABELS)) {
    const v = byCat[cat];
    if (!v) continue;
    const pct = ((v.zh / v.total) * 100).toFixed(0);
    const bar = "█".repeat(Math.round((v.zh / v.total) * 20)).padEnd(20, "·");
    console.log(`  ${label.padEnd(22)} ${bar} ${String(v.zh).padStart(3)}/${String(v.total).padStart(3)} (${pct}%)`);
  }

  if (list) {
    console.log("\n=== 未说明中文价值的条目 ===");
    const targets = rows.filter((r) => !hasZh(r) && (!onlyCat || r.category === onlyCat));
    for (const r of targets) {
      console.log(`  L${r.line} [${r.category}] ${r.name}`);
      console.log(`      ${r.desc.slice(0, 70)}`);
    }
    console.log(`\n合计 ${targets.length} 条待补充。`);
  }

  console.log("\n提示：这是建议性审计，不计入 CI。改描述时请回答「对中文用户有什么用」，不要只写「功能强大」。");
}

main();
