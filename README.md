# 🛠️ Claude Code Skills 中文精选集

> 🚀 最实用的 Claude Code Skills / Agents / Plugins 合集 | 精选 120+ | 按场景分类 | 复制即装 | 持续更新

[![Stars](https://img.shields.io/github/stars/laolaoshiren/claude-code-skills-zh?style=social)](https://github.com/laolaoshiren/claude-code-skills-zh)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-120%2B-green.svg)](#-原创技能)
[![Updated](https://img.shields.io/badge/updated-2026--04--26-brightgreen.svg)](#)
[![Website](https://img.shields.io/badge/website-claude--skills.bt199.com-6c5ce7.svg)](https://claude-skills.bt199.com)

**中文开发者最好的 Claude Code Skills 资源站。** 不只是列表，更包含可直接安装的原创技能包。

适合这几类人直接拿去用：
- 👨‍💻 想给 Claude Code **快速补齐专业能力** 的开发者
- 📦 想找 **中文可读、复制即装** skills 的个人开发者 / 团队
- 🎯 想用现成技能解决 **代码审查、README、API 测试、性能分析、重构建议** 等高频场景的人

**✨ 如果你是第一次接触这个仓库，建议先看这 5 个最值得马上装的原创技能：**
- 🔍 [zh-code-reviewer](skills/zh-code-reviewer/) — 中文代码审查，直接输出中文审查报告
- 📝 [zh-readme](skills/zh-readme/) — 先分析项目，再写更像人写的中文 README
- 🧪 [api-tester](skills/api-tester/) — 自动解析 OpenAPI，快速生成接口测试思路
- ♻️ [refactor-advisor](skills/refactor-advisor/) — 找坏味道，给出可执行重构建议
- ⚡ [perf-profiler](skills/perf-profiler/) — 定位性能瓶颈，优先级明确

🔗 **官网**：[claude-skills.bt199.com](https://claude-skills.bt199.com)

---

## 🚀 为什么这个仓库值得现在就收藏

- **不是只做导航**：既有高质量第三方精选，也有能直接安装的原创技能
- **中文友好**：很多说明直接面向中文开发者，不用自己二次理解
- **高频场景覆盖全**：代码审查、文档、测试、安全、性能、重构、CI/CD 都覆盖
- **持续维护**：定期补新技能、更新 README、官网和分类结构

---

## 🔥 热门原创技能（优先看这几个）

| 技能 | 为什么值得先看 |
|------|----------------|
| [zh-code-reviewer](skills/zh-code-reviewer/) | 当前最受关注的原创技能之一，适合几乎所有代码仓库 |
| [refactor-advisor](skills/refactor-advisor/) | 很适合老项目和屎山项目，容易形成强感知价值 |
| [zh-readme](skills/zh-readme/) | 对开源项目、作品集、内部工具都很实用 |
| [api-tester](skills/api-tester/) | 后端、全栈、集成场景都高频需要 |
| [perf-profiler](skills/perf-profiler/) | 适合排查慢接口、慢任务、慢页面 |

---

## 📖 什么是 Claude Code Skills？

Claude Code Skills 是可复用的指令模块，让 Claude Code 拥有特定领域的专业能力。只需一个 `SKILL.md` 文件，就能让 Claude 变成代码审查专家、安全审计师、文档写手…

### ⚡ 30 秒上手建议

如果你不想挑，第一次可以先装这 5 个：
- `zh-code-reviewer`
- `zh-readme`
- `api-tester`
- `refactor-advisor`
- `perf-profiler`

**安装方式：** 将 skill 目录复制到 `~/.claude/skills/` 即可。

```bash
# GitHub 原生地址
git clone https://github.com/laolaoshiren/claude-code-skills-zh.git
cp -r claude-code-skills-zh/skills/* ~/.claude/skills/

# 国内镜像（GitHub 访问困难时使用）
git clone https://gh-proxy.com/https://github.com/laolaoshiren/claude-code-skills-zh.git
cp -r claude-code-skills-zh/skills/* ~/.claude/skills/

# 或者直接下载 ZIP（无需 git）
# GitHub 原生：https://github.com/laolaoshiren/claude-code-skills-zh/archive/main.zip
# 国内镜像：https://gh-proxy.com/https://github.com/laolaoshiren/claude-code-skills-zh/archive/main.zip
```

---

## ⭐ 精选第三方技能

### 🏆 明星技能（万星以上）

| 技能 | 说明 | ⭐ |
|------|------|-----|
| [everything-claude-code](https://github.com/affaan-m/everything-claude-code) | 🧠 Claude Code 全栈技能系统：Skills + 记忆 + 安全 + 研究驱动开发 | 163K+ |
| [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) | 📚 1,400+ 可安装技能库，覆盖 Claude Code / Cursor / Codex / Gemini CLI | 34K+ |
| [caveman](https://github.com/JuliusBrussee/caveman) | 🪨 用最少的 token 说最短的话，节省 65% token | 42K+ |
| [career-ops](https://github.com/santifer/career-ops) | 💼 AI 求职系统：14 种技能模式 + Go 仪表盘 + PDF 生成 | 38K+ |
| [graphify](https://github.com/safishamsi/graphify) | 🕸️ 将代码/文档/论文转为可查询知识图谱 | 32K+ |
| [marketingskills](https://github.com/coreyhaines31/marketingskills) | 📈 营销技能包：CRO、文案、SEO、数据分析、增长工程 | 23K+ |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 📋 Manus 风格的持久化 Markdown 规划工作流 | 19K+ |
| [humanizer](https://github.com/blader/humanizer) | ✍️ 消除 AI 写作痕迹，让文本更自然 | 15K+ |
| [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | 🎮 49 个 AI 代理 + 72 个工作流，完整游戏开发工作室 | 15K+ |
| [open-saas](https://github.com/wasp-lang/open-saas) | 🔥 100% 免费 SaaS 模板，React + Node + Prisma，AI-ready | 14K+ |
| [ai-guide](https://github.com/liyupi/ai-guide) | 🇨🇳 程序员鱼皮 AI 资源大全：Claude Code / Cursor / DeepSeek 全攻略 | 12K+ |
| [claude-skills](https://github.com/alirezarezvani/claude-skills) | 📦 232+ 技能包，支持 Claude Code / Codex / Gemini CLI / Cursor | 12K+ |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | 📓 Google NotebookLM 非官方 Python API + Agent 技能 | 11K+ |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | ✍️ Humanizer 中文版，消除中文 AI 写作痕迹 | 6K+ |
| [superpowers](https://github.com/obra/superpowers) | 🦸 agentic 技能框架 + 软件开发方法论，163K 认证 | 163K+ |
| [anthropic-skills](https://github.com/anthropics/skills) | 🏛️ Anthropic 官方 Agent Skills 公开仓库 | 122K+ |
| [gstack](https://github.com/garrytan/gstack) | 🧑‍💼 Garry Tan 的 Claude Code 全套配置：23 个工具覆盖 CEO/设计/工程/QA | 79K+ |
| [get-shit-done](https://github.com/gsd-build/get-shit-done) | ⚡ 轻量级元提示 + 上下文工程 + 规格驱动开发系统 | 56K+ |
| [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | 🇨🇳 superpowers 完整汉化 + 6 个中国原创 skills，支持 16 款 AI 工具 | 1.2K+ |
| [claude-mem](https://github.com/thedotmack/claude-mem) | 🧠 自动捕获会话上下文，AI 压缩后注入未来会话，告别遗忘 | 65K+ |
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | 📊 实时显示上下文用量、活跃工具、运行中 Agent 和 TODO 进度 | 20K+ |
| [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 🏛️ Anthropic 官方高质量 Claude Code 插件目录 | 18K+ |
| [agent-skills](https://github.com/addyosmani/agent-skills) | ⚙️ Google 总监出品：生产级工程技能集，覆盖前端/后端/DevOps | 20K+ |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | 📅 近 30 天事件追踪：跨 Reddit / X / YouTube / HN / Polymarket 检索 | 23K+ |

### 📣 平台运营 / 自媒体 / 办公流量

| 技能 | 说明 |
|------|------|
| [XiaohongshuSkills](https://github.com/white0dew/XiaohongshuSkills) | 小红书自动化运营 Skill：自动发布、评论、检索，支持 OpenClaw / Codex / Claude Code（2.6K⭐）|
| [ai-trend-publish](https://github.com/liyown/ai-trend-publish) | 公众号自动化运营系统：多源抓取 + AI 写作 + 智能排序 + 定时发布（2.9K⭐）|
| [wx-favorites-report](https://github.com/zhuyansen/wx-favorites-report) | 微信收藏可视化 Skill：从加密 DB 到交互式 HTML 报告的端到端管线（537⭐）|
| [feishu-openclaw](https://github.com/AlexAnys/feishu-openclaw) | 飞书 / Lark 连接 OpenClaw：免公网、免域名、稳定接入机器人（321⭐）|
| [easy-wx/wecom-bot-svr](https://github.com/easy-wx/wecom-bot-svr) | 企业微信机器人回调服务框架：pip 安装、开箱即用、快速部署（174⭐）|
| [Long-louis/AIFeedTracker](https://github.com/Long-louis/AIFeedTracker) | AI 内容追踪 + 视频总结 + 飞书机器人集成（161⭐）|
| [rawchen/feishu-bot](https://github.com/rawchen/feishu-bot) | 飞书群聊 / 私聊机器人，Spring Boot 实现（158⭐）|
| [loonghao/wecom-bot-mcp-server](https://github.com/loonghao/wecom-bot-mcp-server) | 企业微信机器人 MCP Server，支持上下文感知自动消息处理（85⭐）|
| [openclaw-china](https://github.com/BytePioneer-AI/openclaw-china) | OpenClaw 中国 IM 渠道插件：飞书 / 钉钉 / QQ / 企业微信 / 微信公众号 一站式接入（3.8K⭐）|
| [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) | Notion 官方 MCP Server：OAuth 接入 + Markdown 页面编辑 + AI Agent 低 token 工具集（4.2K⭐）|
| [cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server) | Obsidian 知识库 MCP Server：读写笔记、全文检索、Frontmatter/Tag 管理（463⭐）|
| [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) | Obsidian 官方生态技能包：Markdown / Bases / JSON Canvas / CLI / Defuddle，兼容 Claude Code / Codex / OpenCode（26K⭐）|
| [YishenTu/claudian](https://github.com/YishenTu/claudian) | Obsidian 内嵌 Claude Code / Codex 协作插件：让知识库直接成为 Agent 工作目录，支持 Skills、MCP、计划模式（9.0K⭐）|
| [freestylefly/openclaw-wechat](https://github.com/freestylefly/openclaw-wechat) | OpenClaw 个人微信通道插件：真实微信账号接入、扫码登录、群聊/私聊收发与多账号支持（1.6K⭐）|
| [autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills) | 小红书自动化 Skills：真实浏览器 + 真实账号环境，覆盖发布、评论、检索、批量运营与 CLI 调用（1.1K⭐）|
| [IanShaw027/wemp-operator](https://github.com/IanShaw027/wemp-operator) | 微信公众号自动化运营 OpenClaw Skill：内容采集、数据分析、互动管理，内置 70 个 API、20+ 数据源，支持直接安装（81⭐）|
| [geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill) | 公众号 Markdown 排版与草稿箱上传 Skill：支持 Claude Code / Codex / OpenClaw 安装，适合内容运营批量发布（1.5K⭐）|
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | Google Workspace 全能 CLI：统一操作 Gmail / Drive / Docs / Sheets / Calendar，并内置 40+ agent skills，适合办公自动化与 AI 助手集成（25K⭐）|
| [ythx-101/x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher) | X / 微信文章抓取 Skill：三后端智能回退，支持推文、列表、长文与微信内容检索，适合热点跟踪和自媒体选题（796⭐）|
| [qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm) | 多源内容处理 Claude Skill：支持微信文章 / 网页 / YouTube / PDF / 播客 / Office 文档，并可一键生成播客、PPT、脑图、Quiz，适合内容运营与知识整理（1.4K⭐）|
| [tuya-openclaw-skills](https://github.com/tuya/tuya-openclaw-skills) | 涂鸦官方 OpenClaw 智能家居技能库：接入 3000+ 设备品类，支持设备控制、天气、通知、摄像头抓拍与事件订阅，安装门槛清晰（562⭐）|
| [gemini_cli_skill](https://github.com/forayconsulting/gemini_cli_skill) | Gemini CLI 增强 Skill：让 Claude Code 协同调用 Gemini CLI 做代码生成、代码审查、测试生成、文档编写、网页研究与架构分析，安装与前置条件清晰（177⭐）|

### 💻 开发效率

| 技能 | 说明 |
|------|------|
| [spec-driven-develop](https://github.com/zhu1090093659/spec_driven_develop) | 📋 规格驱动开发：7 阶段预开发流水线，架构优先，纯 Markdown（699⭐）|
| [robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) | 🤖 机器人开发技能集：ROS1/ROS2、设计模式、感知系统、Docker（180⭐）|
| [skill-optimizer](https://github.com/hqhq1025/skill-optimizer) | 🔧 Skill 诊断优化工具：基于真实会话数据的静态分析（54⭐）|
| [github-tech-scanner](https://github.com/claude-access/github-tech-scanner) | 扫描 GitHub 仓库的语言和框架 |
| [review-checkpoint](https://github.com/Atharva-Kanherkar/review-checkpoint) | 结构化自审查工作流：先契约后代码 |
| [archflow](https://github.com/rafaelolsr/archflow) | 将代码库转为动画 HTML 架构图（15⭐）|
| [autoresearch](https://github.com/uditgoenka/autoresearch) | 自主迭代研究：修改→验证→保留/丢弃→循环（3.9K⭐）|
| [SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) | iOS/macOS SwiftUI 开发专用技能（3.7K⭐）|
| [plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) | 423 插件 + 2,849 技能 + 177 代理，超大合集（1.9K⭐）|
| [slavingia-skills](https://github.com/slavingia/skills) | 基于《极简创业者》理念的实用技能集（8.1K⭐）|
| [trailofbits-skills](https://github.com/trailofbits/skills) | Trail of Bits 安全研究与审计技能（4.7K⭐）|
| [skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) | 技能工厂：一键生成、测试、发布 Claude Code 技能（711⭐）|
| [jeffallan-skills](https://github.com/Jeffallan/claude-skills) | 66 个全栈开发者专用技能，成为你的专家配对程序员（8.4K⭐）|
| [daymade-skills](https://github.com/daymade/claude-code-skills) | 专业技能市场，生产就绪的高质量技能集（897⭐）|
| [pinme](https://github.com/glitternetwork/pinme) | 前端一键部署，Claude Code 技能驱动（3.2K⭐）|
| [playwright-skill](https://github.com/lackeyjb/playwright-skill) | Playwright 浏览器自动化，Claude 自主编写+执行测试（2.5K⭐）|
| [android-reverse](https://github.com/SimoneAvogadro/android-reverse-engineering-skill) | Android 应用逆向工程辅助（4.4K⭐）|
| [skill-codex](https://github.com/skills-directory/skill-codex) | 将提示词委派给 Codex 执行（1.2K⭐）|
| [claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | 股票投资者工具：技术分析、选股器、交易策略（969⭐）|
| [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) | .NET 开发者专用技能集：子代理 + 标准化开发流程（869⭐）|
| [app-onboarding-questionnaire](https://github.com/adamlyttleapps/claude-skill-app-onboarding-questionnaire) | 高转化 App 引导页问卷设计：基于顶级订阅 App 的转化模式（934⭐）|
| [bmad-skills](https://github.com/aj-geddes/claude-code-bmad-skills) | BMAD Method：自动检测 + Memory 集成 + 完整开发流程（390⭐）|
| [rails-upgrade](https://github.com/ombulabs/claude-code_rails-upgrade-skill) | Rails 一键升级技能，自动化版本迁移（247⭐）|
| [apple-skills](https://github.com/rshankras/claude-code-apple-skills) | iOS/macOS/iPadOS 开发专用技能集（207⭐）|
| [scrapling](https://github.com/Cedriccmh/claude-code-skill-scrapling) | 智能网页爬虫，自动 Fetcher 选择 + 反爬绕过（224⭐）|
| [context-mode](https://github.com/mksglu/context-mode) | 上下文窗口优化：工具输出沙箱化，减少 98%，支持 12 平台（8.6K⭐）|
| [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) | Claude Code 基础设施展示：技能自动激活 + Hooks + Agents（9.5K⭐）|
| [chops](https://github.com/Shpigford/chops) | macOS 技能管理器：浏览/编辑/管理 Claude Code / Cursor / Codex 技能（1.2K⭐）|
| [sast-skills](https://github.com/utkusen/sast-skills) | 将 AI 编程助手变成 SAST 安全扫描器（612⭐）|
| [cc-skills-golang](https://github.com/samber/cc-skills-golang) | Golang 开发专用 agentic skills 集合（1.3K⭐）|
| [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) | 将代码库转为交互式 HTML 课程（4K⭐）|
| [Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) | 通过 Hooks + Ledgers 实现持久化上下文管理（3.7K⭐）|
| [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | Claude Code Hooks 完全指南：掌握事件驱动自动化（3.5K⭐）|
| [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | 生成生产级 SVG+PNG 技术架构图，支持 8 种图表类型（4.1K⭐）|
| [claude-octopus](https://github.com/nyldn/claude-octopus) | 每个编码任务最多用 8 个 AI 模型并行审查（2.8K⭐）|
| [nothing-design-skill](https://github.com/dominikmartn/nothing-design-skill) | Nothing 设计语言 UI 生成：极简单色、排版、工业风（2K⭐）|
| [huashu-design](https://github.com/alchaincyf/huashu-design) | 🇨🇳 HTML 原生设计 Skill：高保真原型 + 设计系统 + 动效，Claude Code 专属（3K⭐）|
| [darwin-skill](https://github.com/alchaincyf/darwin-skill) | 🧬 技能进化系统：评估→改进→测试→保留或回滚，让 Skill 无限自优化（1.5K⭐）|
| [claude-forge](https://github.com/sangrokjung/claude-forge) | 11 个 AI Agent + 36 命令 + 15 技能，类 oh-my-zsh 插件框架（659⭐）|
| [agentic-stack](https://github.com/codejunkie99/agentic-stack) | 🧠 One brain, many harnesses：可移植 .agent/ 文件夹，跨 Claude/Cursor/Codex 共享（1.2K⭐）|
| [cartographer](https://github.com/kingbootoshi/cartographer) | 用并行子 Agent 映射和文档化任意规模代码库（545⭐）|
| [agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skill-creator) | 将任意工作流转化为可复用的 AI Agent 技能，支持 14+ 工具（743⭐）|
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 从文本生成专业 draw.io 图表的 Agent Skill（365⭐）|
| [ok-skills](https://github.com/mxyhi/ok-skills) | 精选 AI Agent 技能 + AGENTS.md Playbook 合集（281⭐）|
| [awesome-claude-code-config](https://github.com/Mizoreww/awesome-claude-code-config) | 生产级 Claude Code 配置：自改进循环 + 多语言规则 + MCP 集成（222⭐）|
| [agnix](https://github.com/agent-sh/agnix) | AI 编程助手的 Linter + LSP：校验 CLAUDE.md / AGENTS.md / SKILL.md / Hooks（195⭐）|
| [writing-style-skill](https://github.com/jzOcb/writing-style-skill) | 写作风格技能模板，AI 写作→你编辑→自动学习→规则迭代（199⭐）|
| [cursor-rules-java](https://github.com/jabrena/cursor-rules-java) | Java 企业开发技能与 Agents 合集：覆盖规划、架构、Maven、测试、性能、文档与流水线（360⭐）|
| [Dimillian/Skills](https://github.com/Dimillian/Skills) | 高质量 Codex Skills 集合：GitHub 工作流、Diff Review Swarm、Bug Hunt Swarm、React 性能与 SwiftUI/iOS/macOS 专项开发（3.3K⭐）|
| [openai/skills](https://github.com/openai/skills) | OpenAI 官方 Codex Skills Catalog：内置 system / curated / experimental 技能目录，支持 `$skill-installer` 按名称或 GitHub 目录安装（17K⭐）|
| [awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills) | Codex 实用技能精选清单：覆盖开发、协作、沟通、数据分析等多类可安装 skills，并提供 GitHub 路径安装器（1.1K⭐）|
| [huggingface/skills](https://github.com/huggingface/skills) | Hugging Face 官方 Skills 仓库：覆盖模型选择、数据集处理、训练、评测、论文发布与 JS 推理，兼容 Claude Code / Codex / Gemini CLI / Cursor，安装方式清晰（10K⭐）|

### 🎨 内容创作

| 技能 | 说明 |
|------|------|
| [mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) | Excalidraw MCP 服务器：AI 驱动的图表绘制 + 实时画布同步（1.8K⭐）|
| [gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills) | AI/GEO 优化：16 项基础检查 + 6 维智能分析（900⭐）|
| [openmontage](https://github.com/calesthio/OpenMontage) | 🎬 世界首个开源 agentic 视频制作系统：12 流水线 + 52 工具 + 500+ 技能（2.9K⭐）|
| [axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills) | Obsidian 可视化 Skills 套装：让 Claude Code 一次生成 Canvas / Excalidraw / Mermaid，中文文档完善、安装清晰，适合知识整理与内容表达（2.6K⭐）|

### 🤖 AI Agent

| 技能 | 说明 |
|------|------|
| [wshobson/agents](https://github.com/wshobson/agents) | 🧠 智能自动化 & 多 Agent 编排，Claude Code 核心工作流（34K⭐）|
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | 🏢 Teams-first 多 Agent 编排，团队协作场景（31K⭐）|
| [refly](https://github.com/refly-ai/refly) | 🔧 首个开源 Agent Skills 构建器，vibe workflow 定义技能（7.2K⭐）|
| [raptor](https://github.com/gadievron/raptor) | ⚔️ 攻防安全 Agent：SAST/DAST 扫描 + OWASP + CVE 检测（2.3K⭐）|
| [godogen](https://github.com/htdt/godogen) | 🎮 从游戏描述构建完整 Godot 4 项目（2.9K⭐）|
| [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 📚 100+ 子代理合集，覆盖各类开发场景（18K⭐）|
| [videocut-skills](https://github.com/Ceeon/videocut-skills) | 🎬 视频剪辑 Agent，Claude Code 驱动（1.4K⭐）|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | ⚔️ 自主 ML 研究：跨模型审查 + 想法发现 + 实验自动化（7.1K⭐）|
| [browser-use](https://github.com/browser-use/browser-use) | 🌐 AI 浏览器自动化基础设施：提供开源库 + Cloud stealth 浏览器 + 文档化 LLM 接入方式，适合为 Claude Code / Cursor / 自定义 agent 增强网页操作能力（90K⭐）|

### 💰 金融/商业

| 技能 | 说明 |
|------|------|
| [dbskill](https://github.com/dontbesilent2025/dbskill) | 🏢 商业诊断技能包：市场分析、竞品调研、商业模式画布（3.3K⭐） |
| [financial-report-minesweeper](https://github.com/terancejiang/financial-report-minesweeper) | A 股财报排雷工具，28 条唐朝方法论检查（77⭐） |
| [tech-digest](https://github.com/camilleroux/tech-digest) | HN/Lobste.rs 每日科技摘要，评分过滤（25⭐） |

---

### 🌏 中文专属

| 技能 | 说明 |
|------|------|
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 消除中文 AI 写作痕迹（6.4K⭐）|
| [financial-report-minesweeper](https://github.com/terancejiang/financial-report-minesweeper) | A 股财报排雷（唐朝方法论）（77⭐）|
| [web-access](https://github.com/eze-is/web-access) | 给 Claude Code 装上完整联网能力：三层通道调度 + 浏览器 CDP（5.5K⭐）|
| [awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills) | 🇨🇳 精选 AI Agent Skills 列表，适配 Cursor / Claude Code / GitHub Copilot（463⭐）|
| [wx-favorites-report](https://github.com/zhuyansen/wx-favorites-report) | 微信收藏可视化 Skill：从加密 DB 到交互式 HTML 报告的端到端管线（537⭐）|
| [awesome-openclaw-skills-zh](https://github.com/clawdbot-ai/awesome-openclaw-skills-zh) | OpenClaw 中文官方技能库：按办公自动化、系统工具、开发运维等场景整理官方技能，适合中文用户快速发现与调用（4.0K⭐）|

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
| [zh-readme](skills/zh-readme/) | 文档 | 先分析项目，再生成面向中文开发者的高质量 README |
| [perf-profiler](skills/perf-profiler/) | 性能 | 性能分析：瓶颈识别 + 优化建议 |
| [db-migrator](skills/db-migrator/) | 数据库 | 数据库迁移助手：Schema diff + 迁移脚本 |
| [i18n-helper](skills/i18n-helper/) | 开发效率 | 国际化/本地化：扫描硬编码文本 + i18n 配置生成 |
| [log-analyzer](skills/log-analyzer/) | 调试 | 日志分析：异常模式检测 + 根因定位 + 分析报告 |
| [error-translator](skills/error-translator/) | 调试 | 编程错误翻译：英文报错 → 中文解释 + 修复方案 |
| [eslint-fix](skills/eslint-fix/) | 开发效率 | ESLint 自动修复：批量检测 + 自动修复 + 配置建议 |
| [dep-auditor](skills/dep-auditor/) | 安全 | 依赖安全审计：CVE 漏洞检测 + 过期检查 + 许可证风险 |
| [test-generator](skills/test-generator/) | 测试 | 自动生成单元测试：识别函数逻辑 + 边界条件覆盖 + 多语言支持 |
| [github-actions-gen](skills/github-actions-gen/) | CI/CD | GitHub Actions 流水线生成器：根据技术栈自动创建 workflows |
| [env-manager](skills/env-manager/) | 开发效率 | 环境变量管理：扫描 .env 文件 + 校验 + 安全检查 + 生成模板 |
| [ds-mapper](skills/ds-mapper/) | 理解代码库 | 项目结构地图：生成带注释的可视化目录树，快速理解任意仓库 |

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
| Claude Code | 2000+ | 📈 爆发增长中 |
| OpenClaw | 5400+ | 📈 最大生态 |
| Hermes Agent | 500+ | 📈 稳定增长 |
| Cursor Rules | 3000+ | 📈 增长中 |
| Gemini CLI | 500+ | 📈 新兴生态 |

---

## 🔗 相关资源

- [Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)
- [OpenClaw Skills Registry](https://registry.openclaw.ai)
- [awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) — 59K ⭐
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 55K ⭐
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — 39K ⭐
- [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) — 18K ⭐
- [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — 17K ⭐
- [awesome-claude-skills-vn](https://github.com/travisvn/awesome-claude-skills) — 11K ⭐
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 46K ⭐
- [everything-claude-code](https://github.com/affaan-m/everything-claude-code) — 163K ⭐
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) — 34K ⭐
- [awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) — 1.3K ⭐
- [playwright-skill](https://github.com/lackeyjb/playwright-skill) — 2.5K ⭐
- [awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) — 1.1K ⭐
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) — 697 ⭐
- [cc-marketplace](https://github.com/ananddtyagi/cc-marketplace) — 677 ⭐
- [claude-mem](https://github.com/thedotmack/claude-mem) — 65K ⭐
- [claude-hud](https://github.com/jarrodwatts/claude-hud) — 20K ⭐

---

## 📈 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=laolaoshiren/claude-code-skills-zh&type=Date)](https://star-history.com/#laolaoshiren/claude-code-skills-zh&Date)

---

## 🤝 贡献

欢迎提交 PR！请将你的 skill 放入 `skills/` 目录并更新上方列表。

📢 [征集优质 Skills！提交即上榜 →](https://github.com/laolaoshiren/claude-code-skills-zh/issues/1)

---

## ⭐ 如果这个项目帮到了你

请给个 Star ⭐ 这是对我最大的鼓励！

---

## 📝 License

MIT
