# 🛠️ Claude Code Skills 中文精选集

> 🚀 最实用的 Claude Code Skills / Agents / Plugins 合集 | 精选 80+ | 按场景分类 | 复制即装 | 持续更新

[![Stars](https://img.shields.io/github/stars/laolaoshiren/claude-code-skills-zh?style=social)](https://github.com/laolaoshiren/claude-code-skills-zh)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-80+-green.svg)](#-原创技能)
[![Updated](https://img.shields.io/badge/updated-2026--04--14-orange.svg)](#)

**中文开发者最好的 Claude Code Skills 资源站。** 不只是列表，更包含可直接安装的原创技能包。

---

## 📖 什么是 Claude Code Skills？

Claude Code Skills 是可复用的指令模块，让 Claude Code 拥有特定领域的专业能力。只需一个 `SKILL.md` 文件，就能让 Claude 变成代码审查专家、安全审计师、文档写手…

**安装方式：** 将 skill 目录复制到 `~/.claude/skills/` 即可。

```bash
# 一键安装本仓库所有原创技能
git clone https://github.com/laolaoshiren/claude-code-skills-zh.git
cp -r claude-code-skills-zh/skills/* ~/.claude/skills/
```

---

## ⭐ 精选第三方技能

### 🏆 明星技能（万星以上）

| 技能 | 说明 | ⭐ |
|------|------|-----|
| [caveman](https://github.com/JuliusBrussee/caveman) | 🪨 用最少的 token 说最短的话，节省 65% token | 27K+ |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 📋 Manus 风格的持久化 Markdown 规划工作流 | 18K+ |
| [humanizer](https://github.com/blader/humanizer) | ✍️ 消除 AI 写作痕迹，让文本更自然 | 13K+ |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | ✍️ Humanizer 中文版，消除中文 AI 写作痕迹 | 6K+ |

### 💻 开发效率

| 技能 | 说明 |
|------|------|
| [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) | 将代码库转为交互式 HTML 课程 |
| [github-tech-scanner](https://github.com/claude-access/github-tech-scanner) | 扫描 GitHub 仓库的语言和框架 |
| [review-checkpoint](https://github.com/Atharva-Kanherkar/review-checkpoint) | 结构化自审查工作流：先契约后代码 |
| [ship](https://github.com/maxtechera/ship) | 端到端 GTM 流水线 + 凭证预检 |
| [diagent-cli](https://github.com/daniellee-ux/diagent-cli) | Diagent 图表 URL 编解码 CLI + Skill |

### 🎨 内容创作

| 技能 | 说明 |
|------|------|
| [make-mermaid](https://github.com/gy1041/make-mermaid) | 从代码/描述生成 Mermaid 图表，输出 PNG/SVG |
| [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | 生产级 SVG+PNG 技术图表，支持 8 种图表类型 |
| [nothing-design-skill](https://github.com/dominikmartn/nothing-design-skill) | Nothing 设计语言：单色、排版、工业风 |
| [gongnangi-chart-skill](https://github.com/kimsh-1/gongnangi-chart-skill) | 麦肯锡/贝恩风格咨询图表生成器 |

### 🤖 AI Agent

| 技能 | 说明 |
|------|------|
| [ai-second-brain-skills](https://github.com/NulightJens/ai-second-brain-skills) | Karpathy 风格的 LLM Wiki — AI 第二大脑 |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 持久化 Markdown 规划，Manus 工作流模式 |
| [godogen](https://github.com/htdt/godogen) | 从游戏描述构建完整 Godot 4 项目 |

### 💰 金融/商业

| 技能 | 说明 |
|------|------|
| [financial-report-minesweeper](https://github.com/terancejiang/financial-report-minesweeper) | A 股财报排雷工具，28 条唐朝方法论检查 |
| [tax-filer](https://github.com/chaturchatur/tax-filer) | 美国联邦/州所得税申报指导 |
| [tech-digest](https://github.com/camilleroux/tech-digest) | HN/Lobste.rs 每日科技摘要，评分过滤 |

### 🌏 中文专属

| 技能 | 说明 |
|------|------|
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 消除中文 AI 写作痕迹 |
| [financial-report-minesweeper](https://github.com/terancejiang/financial-report-minesweeper) | A 股财报排雷（唐朝方法论） |
| [nanobananas-api-guide](https://github.com/ailingqu/nanobananas-api-guide) | NanoBananas.AI 图片/视频生成 API 指南 |
| [myquant-dev](https://github.com/aliwangzai/myquant-dev) | 掘金量化开发助手 |
| [TESSNG_secondary_dev_Skills](https://github.com/passengerxuhongli/TESSNG_secondary_dev_Skills) | TESS NG 仿真二次开发技能 |

---

## 🎁 原创技能（本仓库独有）

以下技能由本仓库原创开发，可直接安装使用：

### 📦 快速安装

```bash
# 安装单个技能
cp -r skills/<skill-name> ~/.claude/skills/

# 安装全部原创技能
cp -r skills/* ~/.claude/skills/
```

### 🔍 技能列表

| 技能 | 分类 | 说明 |
|------|------|------|
| [zh-code-reviewer](skills/zh-code-reviewer/) | 代码质量 | 中文代码审查专家，生成中文审查报告 |
| [zh-docgen](skills/zh-docgen/) | 文档 | 从代码库自动生成中文技术文档 |
| [git-workflow](skills/git-workflow/) | 开发效率 | Git 工作流自动化：分支、提交、PR |
| [security-audit](skills/security-audit/) | 安全 | 代码安全审计：漏洞扫描 + 修复建议 |
| [api-tester](skills/api-tester/) | 测试 | API 自动化测试：OpenAPI 解析 + 用例生成 |
| [changelog-gen](skills/changelog-gen/) | 文档 | 从 Git 历史自动生成 CHANGELOG |
| [refactor-advisor](skills/refactor-advisor/) | 代码质量 | 代码重构建议：识别坏味道 + 重构方案 |
| [zh-readme](skills/zh-readme/) | 文档 | 一键生成高质量中文 README |
| [perf-profiler](skills/perf-profiler/) | 性能 | 性能分析：瓶颈识别 + 优化建议 |
| [db-migrator](skills/db-migrator/) | 数据库 | 数据库迁移助手：Schema diff + 迁移脚本 |

---

## 🚀 如何创建自己的 Skill

每个 Skill 就是一个目录，里面放一个 `SKILL.md` 文件：

```markdown
---
name: my-skill
description: 技能的一句话描述
---

# 技能名称

## 触发条件
当用户要求 XXX 时激活此技能

## 工作流程
1. 第一步...
2. 第二步...

## 输出格式
- 格式说明...
```

### Skill 最佳实践

1. **触发条件要明确** — 避免与其他 skill 冲突
2. **步骤要具体** — 让 Claude 知道该做什么
3. **包含示例** — 给出输入/输出样例
4. **保持精简** — 一个 skill 做一件事
5. **中英混合** — 技术术语保留英文，说明用中文

---

## 📊 技能生态数据

| 平台 | 技能数量 | 趋势 |
|------|---------|------|
| Claude Code | 1000+ | 📈 爆发增长中 |
| OpenClaw | 5400+ | 📈 最大生态 |
| Hermes Agent | 500+ | 📈 稳定增长 |
| Cursor Rules | 3000+ | 📈 增长中 |

---

## 🔗 相关资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [OpenClaw Skills Registry](https://registry.openclaw.ai)
- [awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) — 59K ⭐
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 53K ⭐
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 45K ⭐

---

## 🤝 贡献

欢迎提交 PR！请将你的 skill 放入 `skills/` 目录并更新上方列表。

---

## ⭐ 如果这个项目帮到了你

请给个 Star ⭐ 这是对我最大的鼓励！

---

## 📝 License

MIT
