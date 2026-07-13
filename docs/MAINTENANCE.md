# 项目维护手册

这份文档用于长期维护 `claude-code-skills-zh`，目标是把它做成中文开发者查找 Claude Code Skills / Agents / Plugins 的首选入口。

## 项目定位

本仓库不是普通 awesome list，而是“中文可读 + 可直接安装 + 持续筛选”的技能资源站。

核心价值：

- 帮中文开发者快速发现 Claude Code / Codex / Gemini CLI / Cursor / OpenClaw 可用的技能、插件、Agent 和工作流。
- 维护一批本仓库原创 `skills/`，让用户复制即可安装。
- 用 README 作为内容源，同步生成 GitHub Pages 官网。

## 内容更新节奏

建议每周做一次小维护，每月做一次结构性维护。

每周维护：

- 检查开放 PR 和 Issue，优先处理新增资源推荐、断链、描述错误。
- 搜索近期活跃的 Claude Code / Codex / Agent Skills 项目，补充 5-15 个高相关条目。
- 运行 `python scripts/sync_readme_to_site.py --fetch-stars` 同步 README、官网数据和 star 数。
- 跑本地校验，确保 GitHub Actions 不报错。
- 仓库已配置 `Auto Maintenance` GitHub Actions，每 3 天自动同步 README / 官网统计并执行 lint、链接和脚本回归检查。

每月维护：

- 重新审视分类是否需要拆分或合并。
- 清理 404、低质量、重复、明显跑题的资源。
- 优化 README 首屏、热门原创技能、官网 SEO 描述。
- 从高频用户需求中挑 1-2 个场景新增原创 skill。

## 收录原则

优先收录：

- 直接包含 `SKILL.md`、Claude Code plugin、Agent、slash command、workflow、MCP 或安装说明的项目。
- 明确支持 Claude Code、Codex、Gemini CLI、Cursor、OpenClaw、OpenCode、Copilot CLI 等 AI 编程工具的项目。
- 中文用户容易理解、安装路径清晰、README 完整的项目。
- 能解决高频场景的项目：代码审查、测试、安全、文档、重构、性能、DevOps、内容创作、办公自动化、知识管理。
- 活跃维护、链接稳定、有真实使用价值的项目。

谨慎收录：

- 只是普通 prompt 集合，但没有技能化、安装化或 Agent 工作流说明的项目。
- star 很高但和 skills / agents / plugins 关系弱的泛 AI 项目。
- 只有概念介绍、没有可复用文件或命令的项目。
- README 不清晰、安装方式不明、强依赖私有服务且不可验证的项目。

不要收录：

- 404、私有仓库、空仓库、明显模板仓库。
- 与 AI coding skills 无关的普通应用、营销页面、下载站。
- 描述夸张但看不到实际 skill、agent、plugin、workflow 的项目。
- 涉及恶意攻击、盗号、绕过付费、违法采集或明显侵权的项目。

## 候选验证流程

新增资源不要只看 GitHub Search 摘要或 star 数。合入 README 前至少确认：

- 仓库可访问、未归档、不是空仓库。
- README 说明清楚，能看出它提供的是 `SKILL.md`、Claude Code plugin、Agent workflow、MCP、CLI 或可迁移的 agent 配置。
- 顶层或子目录中能找到 `skills/`、`.claude-plugin/`、`SKILL.md`、`plugin.json`、`commands/`、`AGENTS.md` 等实际资产，或 README 给出了明确安装命令。
- 对 0 star 或刚创建的仓库，只有在作者/组织可信、安装路径清晰、场景价值强时才收录。
- 对安全、浏览器自动化、爬虫、交易、账号登录等高风险场景，描述里要写清前置条件和适用边界，不夸大“自动赚钱”“绕过限制”等能力。

## README 更新规则

README 是单一内容源。新增条目后必须运行同步脚本生成官网：

```bash
python scripts/sync_readme_to_site.py --fetch-stars
```

新增资源时尽量使用这种描述结构：

```markdown
| [项目名](https://github.com/owner/repo) | 一句话说明：解决什么场景，支持哪些工具，为什么值得中文用户看（123⭐）|
```

描述要避免：

- “强大、优雅、领先、革命性”等空泛词。
- 只堆关键词，不说明实际使用场景。
- 明显未经验证的星标数、功能数、官方身份。

## 原创 Skills 迭代方向

已落地：

- `skill-curator`：核验 GitHub 候选仓库的真实资产、安装路径、重复项和风险，输出中文收录建议。

优先补这类原创技能：

- `repo-maintainer`：面向开源项目的日常维护助手，处理断链、README、release notes、PR triage。
- `github-pages-sync`：检查 README 与官网是否一致，避免 SEO 和 badge 过期。
- `awesome-list-auditor`：检查 awesome list 的重复、断链、分类漂移和描述质量。
- `skill-translator`：把英文 `SKILL.md` 翻译成自然中文并保留结构。

新增原创 skill 前，要确保它能在真实仓库中触发，并且 `description` 足够明确。

## 增长策略

更容易带来 star 的维护动作：

- 首屏价值明确：告诉用户“这是什么、适合谁、30 秒怎么安装”。
- 持续增加高质量新项目，而不是单纯堆数量。
- 保持官网与 README 数据一致，避免用户觉得项目停更。
- 把热门原创技能放在 README 前半屏，降低安装门槛。
- 处理社区 PR，让贡献者愿意继续推荐资源。
- 为每次维护写清楚“新增了什么、修了什么、为什么值得看”。

不建议做的增长动作：

- 批量灌入不相关链接，只追求数量。
- 复制其他 awesome list 的全部条目而不筛选。
- 频繁改名、改域名、改分类，破坏用户记忆。
- 在 README 中放过多营销口号，稀释安装和资源发现体验。

## 发布前检查

每次提交前运行：

```bash
python scripts/test_sync_readme_to_site.py
python scripts/sync_readme_to_site.py --dry-run
npx --yes markdownlint-cli2 "**/*.md"
git diff --check
```

如果改了 README 中的 GitHub 链接，抽样或批量检查仓库是否可访问。外部非 GitHub 链接至少检查新增链接。

## 自动维护任务

`.github/workflows/auto-maintenance.yml` 每 3 天运行一次，也支持在 GitHub Actions 页面手动触发。

自动任务负责：

- 运行 `scripts/test_sync_readme_to_site.py`，避免同步脚本在 Windows/GBK 等环境再次回归。
- 运行 `scripts/sync_readme_to_site.py --fetch-stars`，同步 README badge、官网统计和站点数据。
- 运行 markdownlint 和 `git diff --check`。
- 如果 README、`docs/index.html` 或 `docs/sitemap.xml` 有自动同步差异，直接提交 `docs: auto maintenance sync`。

README 外部链接由独立的 `Link Check` workflow 定期检查。链接波动或第三方图片接口故障不应阻断已经完成的统计同步提交。

自动任务不负责：

- 自动把搜索到的项目写进 README。
- 自动接受低质量 PR。
- 自动修改原创 skills 的行为。

新增精选资源仍然需要遵守本手册的收录原则，由维护者基于相关性、安装清晰度和中文用户价值判断。
