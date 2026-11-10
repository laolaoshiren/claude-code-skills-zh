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
- 运行 `python scripts/sync_readme_to_site.py --fetch-stars` 同步 README 徽章、官网数据、`docs/sitemap.xml` 日期、以及 `PROMO.md` 中的精选与原创数量。
- 跑本地校验，确保 GitHub Actions 不报错。
- 仓库已配置 `Auto Maintenance` GitHub Actions，每周自动同步 README / 官网统计并向 `PROMO.md` 对齐数量，同时执行 lint、链接和脚本回归检查。

每月维护：

- 重新审视分类是否需要拆分或合并。
- 清理 404、低质量、重复、明显跑题的资源。
- 优化 README 首屏、热门原创技能、官网 SEO 描述。
- 从高频用户需求中挑 1-2 个场景新增原创 skill。

## 收录原则

### 中文是核心（不可让渡）

本项目是「Claude Code Skills 中文精选集」，「中文」不是翻译层，而是选品与写作的核心标准。每个条目都必须能回答一个问题：**这个项目对中文用户的价值是什么？**

具体判断维度（命中任意一项即可，但必须在描述里写出来）：

- **中文文档**：仓库提供中文 README、中文 SKILL.md 或中文使用说明。
- **中文场景**：覆盖国内平台与生态，如公众号、小红书、飞书、企业微信、钉钉、B 站、抖音、QQ、国内云服务。
- **中文语境优化**：针对中文写作、中文排版、中文分词、去 AI 味、中文内容审核等做过专门处理。
- **中文开发者高频痛点**：即使项目本身是英文，也要说明它解决的是中文开发者的什么问题（例如"项目结构地图，不依赖英文描述即可读懂大型仓库"）。

**不要**把「中文用户也能用」当成中文价值——几乎所有项目都成立，等于没说。

### 描述包装：英文项目也要写给中文用户看

很多高质量项目是纯英文的，收录它们没问题，但**描述不能照搬英文简介**。每条描述都要完成一次「翻译成中文用户的语境」：

- **两段式写法**：先说它是什么能力，再说「对中文用户意味着什么」——省掉什么成本、替代什么流程、适合哪类人。
- **英文项目要诚实标注**：可以写「英文文档，适合愿意读原文的进阶用户」，但不能虚构中文支持；只有确实提供中文 README / 中文官网才加 🇨🇳 标记。
- **落到具体场景**：与其写「提升开发效率」，不如写「接手大型遗留项目时，先让它把代码库梳理成图谱再动手」。
- **不要堆形容词**：「强大」「优雅」「革命性」一律不用，读者要的是判断依据。

正反例：

```text
❌ Agentic 技能框架与软件开发方法论
✅ 想理解「Agent 该怎么协作」而不只是收集技能的人，适合从它的方法论文档读起

❌ 免费 SaaS 模板，React + Node + Prisma，AI-ready
✅ 想做副业或小产品验证时，省掉搭脚手架的一周
```

### 分类与展示的优先级

- 「🌏 中文专属」是本项目的差异化阵地：优先收录中文优先、中文原生、国内平台相关的项目，不要把英文项目塞进来凑数。
- 「🏆 热门与高潜」是门面：优先放**有中文文档、或对中文开发者有明确价值**的高星项目。纯英文且无中文价值说明的项目，即使 star 很高也不要放在这个分类。
- 任何分类的条目描述，都要用中文说明「解决什么场景、支持什么工具、为什么值得中文用户看」。

### 优先收录

- 直接包含 `SKILL.md`、Claude Code plugin、Agent、slash command、workflow、MCP 或安装说明的项目。
- 明确支持 Claude Code、Codex、Gemini CLI、Cursor、OpenClaw、OpenCode、Copilot CLI 等 AI 编程工具的项目。
- 中文用户容易理解、安装路径清晰、README 完整的项目。
- 能解决高频场景的项目：代码审查、测试、安全、文档、重构、性能、DevOps、内容创作、办公自动化、知识管理。
- 活跃维护、链接稳定、有真实使用价值的项目。

### 谨慎收录

- 只是普通 prompt 集合，但没有技能化、安装化或 Agent 工作流说明的项目。
- star 很高但和 skills / agents / plugins 关系弱的泛 AI 项目。
- 只有概念介绍、没有可复用文件或命令的项目。
- README 不清晰、安装方式不明、强依赖私有服务且不可验证的项目。

### 不要收录

- 404、私有仓库、空仓库、明显模板仓库。
- 与 AI coding skills 无关的普通应用、营销页面、下载站。
- 描述夸张但看不到实际 skill、agent、plugin、workflow 的项目。
- 涉及恶意攻击、盗号、绕过付费、违法采集或明显侵权的项目。

### 纯引流 / 广告 / 低质项目识别

以下信号**同时命中两条以上**才判定为引流或低质，避免误伤正常项目：

- **无任何可复用资产**：文件树里既没有 `SKILL.md`、`skills/`、`.claude-plugin/`、
  `plugin.json`、`agents/`、`commands/`，也没有 `src/`、`packages/` 等可运行实现，
  且 README 里找不到任何安装命令。
- **重度导流**：README 的主要篇幅用于导流到同一个非 GitHub 商业站点，
  且仓库本身不提供可独立使用的资产。
- **空壳仓库**：根目录文件极少（≤4 项）且无资产、无文档。
- **无 README**：根目录不存在任何 `readme` 变体（含 `readme.md`、`README_zh.md`）。
- **星数异常**：创建不足 90 天却获得数千 star，且缺少对应资产支撑。

判定时必须**组合信号 + 人工复核**，单一信号不足以删除。以下情况不算引流：
自建官网 / 文档站的正常项目（链接自家文档是正常行为）、awesome 类精选目录、
厂商官方仓库（如 `microsoft/*`、`prisma/*`）、MCP Server 与 CLI 工具。

## 条目淘汰标准

每次迭代应顺带体检并清理以下条目，避免历史遗留长期堆积：

- **仓库 404 / 已删除 / 转为私有**：直接删除。
- **已归档（archived）**：删除。
- **fork 而非原创资产**：删除，除非原作者明确以 fork 作为唯一维护渠道。
- **0 星且 60 天以上无推送**：删除（新仓库尚无沉淀）。
- **长期无维护且低星**：超过 300 天未推送且 star ≤ 50，删除。
- **无许可证且长期无维护**：超过 300 天未推送且无 `LICENSE`，删除。
- **分类错位**：低星项目不应出现在「热门与高潜」，应移动到对应场景分类。

**不要**仅以「停止更新」作为删除理由：高星成熟项目（如 10K+ star 的稳定工具）
即使一年未推送，其资产仍然可用，应保留。

体检脚本（均为只读工具，会按批调用 GitHub GraphQL，带本地缓存并在中断后续传）：

```bash
# 元数据与失效条目：必须显式指定范围，避免误触发数百次请求
node scripts/audit_readme_entries.mjs --limit 50        # 只查前 50 个未缓存仓库
node scripts/audit_readme_entries.mjs --out audit.json  # 全量体检并写出结果

# 引流 / 低质信号：同样必须显式指定范围
node scripts/audit_promotional_entries.mjs --limit 30
node scripts/audit_promotional_entries.mjs --all        # 全量抓取
```

不带范围参数时脚本会拒绝运行（退出码 2）并提示用法，`--help` 可查看完整说明。
缓存文件 `.audit-cache.json`、`.audit-promo.json` 已加入 `.gitignore`。

中文价值审计（建议每轮迭代跑一次，量化「初心」是否被稀释）：

```bash
node scripts/audit_chinese_value.mjs              # 各分类中文价值覆盖率
node scripts/audit_chinese_value.mjs --list       # 列出未说明中文价值的条目
node scripts/audit_chinese_value.mjs --category dev
```

该脚本为建议性审计，不计入 CI。目标不是一次清零，而是**新收录不再拉低比例、老条目逐轮补齐**。
若某个分类的覆盖率长期低于 20%，说明选品已经偏离「中文精选」定位，应在下一轮优先调整。

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

该命令会通过已认证的 `gh` CLI 批量读取全部精选 GitHub 仓库及本仓库的实时 Star，并统一同仓库跨分类条目的显示值。单个仓库查询失败时保留 README 中已有数字并输出警告，不得用估算值补齐。

README badge、官网统计和 sitemap 的公开日期统一按 Asia/Shanghai（UTC+8）计算，不能直接使用 GitHub Runner 的 UTC 日期。

README 是面向用户的项目首页，只保留项目价值、安装入口、精选目录和必要的更新时间，不堆叠按日期展开的完整维护日志。详细变更写入 Git commit、PR / Issue 回复和交付记录；README 的 `Updated` badge 链接到 `main` 分支提交历史，供需要的用户查看。

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
- 在 Git commit、PR / Issue 回复和交付记录中写清楚“新增了什么、修了什么、为什么值得看”，不要把完整维护日志堆进 README。

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
python scripts/test_juejin_safety.py
node --test scripts/test_secure_temp.js
npx --yes markdownlint-cli2 "**/*.md"
git diff --check
```

**关于 Python 运行环境**：Windows 上 `PATH` 里的 `python.exe` 可能只是
Microsoft Store 的 0 字节占位程序，执行会失败或提示去商店安装。这不代表本机
没有可用的 Python——DSH 等工具链会自带独立运行时，例如：

```text
%USERPROFILE%\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe
```

找不到解释器时，先确认实际路径再判断，**不要因为 `python` 命令不可用就跳过
Python 测试**。Windows 控制台默认使用 GBK/CP936，脚本必须能在该编码下正常
输出中文与 emoji（参见 `tests` 中的 GBK 回归用例）；仅在 Linux CI 通过不足以
证明这一点，必要时应设置 `PYTHONIOENCODING=gbk` 复测。

如果改了 README 中的 GitHub 链接，抽样或批量检查仓库是否可访问。外部非 GitHub 链接至少检查新增链接。

## 自动维护任务

`.github/workflows/auto-maintenance.yml` 每周运行一次（周一 UTC 02:00），也可在 GitHub Actions 页面手动触发。

自动任务负责：

- 运行 `scripts/test_sync_readme_to_site.py`，避免同步脚本在 Windows/GBK 等环境再次回归。
- 运行 `scripts/sync_readme_to_site.py --fetch-stars`，同步 README badge、官网统计、精选条目 Star 和站点数据。
- 同步脚本只接受 `http` / `https` 资源地址；生成数据需要转义脚本边界字符，官网卡片使用 DOM API 和 `textContent` 渲染，不得重新改回拼接 `innerHTML`。
- 运行 markdownlint 和 `git diff --check`。
- 如果 README、`docs/index.html` 或 `docs/sitemap.xml` 有自动同步差异，直接提交 `docs: auto maintenance sync`。

README 外部链接由独立的 `Link Check` workflow 检查：只在 PR 改动 README、每周定时或手动触发时运行，且并发与重试保持低值。一次检查会访问 README 中约 500 个外部链接，因此不在每次 push 时运行。链接波动或第三方图片接口故障不应阻断已经完成的统计同步提交。

自动任务不负责：

- 自动把搜索到的项目写进 README。
- 自动接受低质量 PR。
- 自动修改原创 skills 的行为。

新增精选资源仍然需要遵守本手册的收录原则，由维护者基于相关性、安装清晰度和中文用户价值判断。

## 自动化频率约定

项目账户曾因被判定滥用 GitHub 功能而封禁，因此仓库自动化刻意保持低频。以下为硬性约定，不要收紧频率：

- `auto-maintenance.yml` 保持每周一次，不要改回每 3 天或更高频率。
- `link-check.yml` 不在 `push` 时运行；并发保持低值（`--max-concurrency 4`），重试不超过 1 次。
- `markdown-lint.yml` 只在 Markdown 或 lint 配置变化时触发。
- 不要用 `gh workflow run` 手动触发定时 workflow；确需补跑时先说明理由。
- 不要轮询 CI 状态（`gh run watch` 或循环 `gh run list`），需要确认结果时只做单次查询。
- 核验第三方仓库时优先用一次 GraphQL 批量取数，避免逐仓库、逐文件的大量 API 调用。
- 单轮维护尽量合并为一次推送，减少 workflow 触发次数，也减少对外部站点的请求。
