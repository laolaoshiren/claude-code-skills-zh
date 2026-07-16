# 🛠️ Claude Code Skills 中文精选集

> 🚀 最实用的 Claude Code Skills / Agents / Plugins 合集 | 精选 397+ | 按场景分类 | 复制即装 | 持续更新

[![Stars](https://img.shields.io/github/stars/laolaoshiren/claude-code-skills-zh?style=social)](https://github.com/laolaoshiren/claude-code-skills-zh)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-397%2B-green.svg)](#original-skills)
[![Updated](https://img.shields.io/badge/updated-2026--07--17-brightgreen.svg)](#maintenance-update)
[![Website](https://img.shields.io/badge/website-claude--skills.bt199.com-6c5ce7.svg)](https://claude-skills.bt199.com)

**中文开发者最好的 Claude Code Skills 资源站。** 不只是列表，更包含可直接安装的原创技能包。

适合这几类人直接拿去用：
- 👨‍💻 想给 Claude Code **快速补齐专业能力** 的开发者
- 📦 想找 **中文可读、复制即装** skills 的个人开发者 / 团队
- 🎯 想用现成技能解决 **代码审查、README、API 测试、性能分析、重构建议** 等高频场景的人

**✨ 如果你是第一次接触这个仓库，建议先看这 5 个最值得马上装的原创技能：**
- 🔍 [zh-code-reviewer](skills/zh-code-reviewer/) — 中文代码审查，直接输出中文审查报告
- 📝 [zh-readme](skills/zh-readme/) — 先分析项目，再写更像人写的中文 README
- 🧪 [api-tester](skills/api-tester/) — 依据真实契约，在确认环境与授权后生成并验证 API 测试
- ♻️ [refactor-advisor](skills/refactor-advisor/) — 找坏味道，给出可执行重构建议
- ⚡ [perf-profiler](skills/perf-profiler/) — 用可复现基线和 profiler 证据定位性能瓶颈

🔗 **官网**：[claude-skills.bt199.com](https://claude-skills.bt199.com)

---

## 🚀 为什么这个仓库值得现在就收藏

- **不是只做导航**：既有高质量第三方精选，也有能直接安装的原创技能
- **中文友好**：很多说明直接面向中文开发者，不用自己二次理解
- **高频场景覆盖全**：代码审查、文档、测试、安全、性能、重构、CI/CD 都覆盖
- **持续维护**：定期补新技能、更新 README、官网和分类结构

<a id="maintenance-update"></a>

### 2026-07-17 维护更新

- 实际核验并新增 3 个资源：NVIDIA 官方 230 个验证型 Agent Skills、带中文文档的 GitHub README 视觉重构 Skill，以及 PlanetScale 官方 15 个数据库审查与运维 Skills。
- 修复 Windows `core.autocrlf=true` 下的同步幂等问题：替换 `skillsData` 时保留目标 CRLF / LF 风格，并新增真实 CRLF 字节级 no-op 回归测试。
- 重写原创 `api-tester`：按 OpenAPI、路由和现有测试的真实契约生成用例，区分“生成测试”与“执行请求”授权，禁止裸 `npx`、猜测状态码 / SLA 和未确认的生产写请求。
- 加固 GitHub Actions：固定所有第三方 Action 的完整 commit SHA，只读任务显式使用 `contents: read` 和超时；自动维护不再持久化 Git 凭据，仅在最终 push 步骤临时注入 Token。
- 更新长期征集 [Issue #1](https://github.com/laolaoshiren/claude-code-skills-zh/issues/1)：将“提交即上榜”改为“审核后收录”，明确真实资产、安装路径、许可证、重复项和安全合规核验标准。
- 检查 GitHub Issues、PR、review 与评论：当前无开放 PR、无新增未处理推荐或评论；PR #13 已合并且无后续反馈。

---

### 2026-07-15 维护更新

- 实际核验并新增 8 个资源：`academic-research-skills`、`shuorenhua`、`AppGenesisForge`、`kc_ai_skills`、`hermes-edu-skills`、`taiwan-translate-skill`、`feishu-whiteboard-pro` 与 `ccteam`，覆盖学术研究、中文写作、工程协作、教育、本地化、飞书白板和多 Agent 团队。
- 审查并合并社区 [PR #13](https://github.com/laolaoshiren/claude-code-skills-zh/pull/13)：实际检查 `niubiskill` 的中文 `SKILL.md`、安装路径、25 个行为场景与校验脚本；目录描述补充“不承诺收益”和受监管活动权限边界。
- 新增 `dotnet/skills` 与 `tex-manual-translation`：前者提供 .NET 团队维护的 15 组跨 Agent 插件，后者用中文术语表、CJK 编译门禁和检查脚本处理 LaTeX 手册翻译。
- 补齐安全与使用边界：学术输出保留人工核验，CTF / 逆向仅限授权环境，飞书写入需确认账号与租户权限，ccteam 默认无 TLS 的 Web 控制台仅建议用于可信局域网或绑定本机。
- 重写 `git-workflow`、`eslint-fix`、`perf-profiler` 与 `test-generator` 的关键流程：严格区分 Git 动作授权，禁止隐式下载 ESLint，用真实基线和 profiler 证据报告性能，并按真实代码契约生成测试。
- 加固 README → 官网同步链路：只接受 `http` / `https` 外链，安全转义脚本边界字符，并改用 DOM `textContent` 渲染卡片，防止恶意目录条目注入页面脚本。
- 让同步任务真正幂等并失败关闭：公开锚点缺失或重复时拒绝写入，仅在内容实质变化时统一推进日期，并通过同目录临时文件、原子替换和逆序回滚保护 README、官网与 sitemap。
- 修复 Star、入口与日期一致性：`--fetch-stars` 现在批量刷新全部 GitHub 条目并统一跨分类重复项；公开更新时间固定按 Asia/Shanghai 计算，同时将已合并的 SEO/GEO 独立仓迁移到 120 个营销技能的统一仓库。
- 移除会返回 503 的 Star History 图片，README 与官网统一使用 canonical `www.star-history.com` 文本入口，同时恢复该域名的常规链接检查。
- 检查 GitHub Issues、PR 与评论：PR #13 已完成中文 review 并合并，当前无开放 PR；长期征集 [Issue #1](https://github.com/laolaoshiren/claude-code-skills-zh/issues/1) 暂无新增未处理推荐，继续保持开放。

---

### 2026-07-14 维护更新

- 修复连续三次失败的自动维护任务：替换 404 资源、排除不稳定的 Star History 图片接口，并升级 GitHub Actions 运行时版本。
- 核验 PR #11 / #12 的 LinkedIn Skills，未直接合并不符合中文表格规范的改动；改为收录一个仓库级中文条目，并明确 Token、云浏览器和真实账号风险。
- 新增 Microsoft SkillOpt、Microsoft Agent Skills、claudelint、finding-unknowns、codex-hygiene、歸藏材质插画、人文学科写作伙伴、罗盘和繁体中文去 AI 味等高价值资源。
- 清理重定向、重复与归档条目：迁移到 canonical URL，以 GSD Core 替代已归档旧仓库，移除已归档抖音 MCP，并更新热门项目 Star。
- 新增原创 `skill-curator`，用中文核验候选仓库的实际资产、安装方式、分类、重复项和风险，原创技能增至 20 个。
- 加固 README → 官网同步：修复原创数量统计、Star 获取失败回退、`skillsData` 替换失败保护，并自动更新 sitemap 日期。
- 修复 API 测试和数据库迁移示例，收紧环境变量脱敏规则；掘金脚本默认只预检，必须显式 `--publish` 才会产生外部状态。

---

## 🔥 热门原创技能（优先看这几个）

| 技能 | 为什么值得先看 |
|------|----------------|
| [zh-code-reviewer](skills/zh-code-reviewer/) | 当前最受关注的原创技能之一，适合几乎所有代码仓库 |
| [refactor-advisor](skills/refactor-advisor/) | 很适合老项目和屎山项目，容易形成强感知价值 |
| [zh-readme](skills/zh-readme/) | 对开源项目、作品集、内部工具都很实用 |
| [api-tester](skills/api-tester/) | 依据真实契约生成测试，并在确认环境、授权和清理方案后执行 |
| [perf-profiler](skills/perf-profiler/) | 基于可复现基线和 profiler 证据排查慢接口、慢任务、慢页面 |

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

### 🏆 热门与高潜技能

| 技能 | 说明 | ⭐ |
|------|------|-----|
| [everything-claude-code](https://github.com/affaan-m/ECC) | 🧠 Claude Code 全栈技能系统：Skills + 记忆 + 安全 + 研究驱动开发 | 230.4K+ |
| [agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | 📚 1,900+ 可安装技能库，覆盖 Claude Code / Cursor / Codex / Gemini CLI | 43.4K+ |
| [ClawX](https://github.com/ValueCell-ai/ClawX) | 🖥️ OpenClaw 桌面图形界面：把 CLI Agent 编排变成可视化桌面体验，中文官网与快速开始完整 | 7.5K+ |
| [obsidian-skills](https://github.com/kepano/obsidian-skills) | 🧠 Obsidian 官方生态技能包：Markdown / Bases / JSON Canvas / CLI / Defuddle，兼容 Claude Code / Codex / OpenCode | 42.2K+ |
| [caveman](https://github.com/JuliusBrussee/caveman) | 🪨 用最少的 token 说最短的话，节省 65% token | 90.1K+ |
| [career-ops](https://github.com/santifer/career-ops) | 💼 AI 求职系统：14 种技能模式 + Go 仪表盘 + PDF 生成 | 60.3K+ |
| [graphify](https://github.com/Graphify-Labs/graphify) | 🕸️ 将代码、文档和数据结构转为可查询知识图谱 | 88.6K+ |
| [marketingskills](https://github.com/coreyhaines31/marketingskills) | 📈 营销技能包：CRO、文案、SEO、数据分析、增长工程 | 40.1K+ |
| [planning-with-files](https://github.com/OthmanAdi/planning-with-files) | 📋 Manus 风格的持久化 Markdown 规划工作流 | 25.4K+ |
| [humanizer](https://github.com/blader/humanizer) | ✍️ 消除 AI 写作痕迹，让文本更自然 | 29.5K+ |
| [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) | 🎮 49 个 AI 代理 + 72 个工作流，完整游戏开发工作室 | 23.1K+ |
| [open-saas](https://github.com/wasp-lang/open-saas) | 🔥 免费 SaaS 模板，React + Node + Prisma，AI-ready | 14.9K+ |
| [ai-guide](https://github.com/liyupi/ai-guide) | 🇨🇳 程序员鱼皮 AI 资源大全：Claude Code / Cursor / DeepSeek 全攻略 | 17.3K+ |
| [claude-skills](https://github.com/alirezarezvani/claude-skills) | 📦 232+ 技能包，支持 Claude Code / Codex / Gemini CLI / Cursor | 22.7K+ |
| [notebooklm-py](https://github.com/teng-lin/notebooklm-py) | 📓 Google NotebookLM 非官方 Python API + Agent 技能 | 17.8K+ |
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | ✍️ Humanizer 中文版，消除中文 AI 写作痕迹 | 13.3K+ |
| [superpowers](https://github.com/obra/superpowers) | 🦸 Agentic 技能框架与软件开发方法论 | 255.9K+ |
| [anthropic-skills](https://github.com/anthropics/skills) | 🏛️ Anthropic 官方 Agent Skills 公开仓库 | 161.6K+ |
| [gstack](https://github.com/garrytan/gstack) | 🧑‍💼 Garry Tan 的 Claude Code 全套配置：覆盖 CEO、设计、工程与 QA | 122.3K+ |
| [GSD Core](https://github.com/open-gsd/gsd-core) | ⚡ Get Shit Done 的活跃后继项目：规格驱动开发、Skills、Agents、Hooks 与中文 README | 6.7K+ |
| [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | 🇨🇳 superpowers 完整汉化 + 6 个中国原创 Skills，支持多款 AI 工具 | 7K+ |
| [claude-mem](https://github.com/thedotmack/claude-mem) | 🧠 自动捕获会话上下文，AI 压缩后注入未来会话，告别遗忘 | 87.5K+ |
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | 📊 实时显示上下文用量、活跃工具、运行中 Agent 和 TODO 进度 | 26.5K+ |
| [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 🏛️ Anthropic 官方 Claude Code 插件目录 | 32.2K+ |
| [agent-skills](https://github.com/addyosmani/agent-skills) | ⚙️ 生产级工程技能集，覆盖前端、后端与 DevOps | 78.7K+ |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | 📅 近 30 天事件追踪：跨 Reddit / X / YouTube / HN / Polymarket 检索 | 52.4K+ |
| [openclaw](https://github.com/openclaw/openclaw) | 🦞 OpenClaw 官方个人 AI 助手：跨 OS 调度 Skills、插件与本地工具 | 383.1K+ |
| [hermes-agent](https://github.com/NousResearch/hermes-agent) | 🪽 NousResearch 的可成长 Agent：Skills、记忆与工具链一体化 | 215.9K+ |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 🧠 Karpathy 编码观察提炼的 CLAUDE.md 行为技能，减少常见 LLM 编程误区 | 193.2K+ |
| [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) | 🦞 OpenClaw 5,400+ 技能精选目录，适合发现可安装技能 | 51.3K+ |
| [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | 📚 Claude Code Skills、Hooks、Commands、Agents 和 Plugins 生态导航 | 50.2K+ |
| [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | 🧩 1,000+ Agent Skills 精选，兼容 Claude Code / Codex / Gemini CLI / Cursor | 28.2K+ |
| [vercel-agent-skills](https://github.com/vercel-labs/agent-skills) | ▲ Vercel 官方 Agent Skills，适合前端、部署与现代 Web 工程工作流 | 29.1K+ |
| [awesome-copilot](https://github.com/github/awesome-copilot) | 🐙 GitHub Copilot 官方社区 Instructions、Agents、Skills 与配置合集 | 36.7K+ |
| [google/skills](https://github.com/google/skills) | 🏛️ Google 官方 Agent Skills：覆盖 Cloud、Gemini API、BigQuery、GKE、Firebase 与 Ads | 14.9K+ |
| [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | 🔬 148 个科学研究 Skills + 100+ 数据库，覆盖生物、化学、医学与金融数据 | 31K+ |
| [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) | 🛡️ NVIDIA Agent Skill 安全扫描器：检测 prompt injection、数据外泄和工具投毒 | 13.3K+ |
| [microsoft/SkillOpt](https://github.com/microsoft/SkillOpt) | 🧪 Microsoft Skill 文本优化框架：用轨迹、验证门禁和离线训练迭代可部署技能，支持 Claude Code / Codex | 12.9K+ |
| [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 📚 Composio 维护的 Claude Skills 导航，按研究、设计和生产力等场景分类 | 67.9K+ |
| [mattpocock/skills](https://github.com/mattpocock/skills) | 🧑‍💻 Matt Pocock 的工程 Skills：覆盖代码审查、类型安全、测试与重构 | 173.8K+ |
| [open-design](https://github.com/nexu-io/open-design) | 🎨 19 个设计 Skills + 71 套品牌级设计系统，支持多种 Coding Agent CLI | 78.9K+ |
| [OpenViking](https://github.com/volcengine/OpenViking) | 🧠 火山引擎 Agent Context Database：统一管理 memory、resources 与 skills | 26.9K+ |
| [cherry-studio](https://github.com/CherryHQ/cherry-studio) | 🍒 高星 AI 生产力桌面工作台，可作为 Claude Code、OpenClaw 与 MCP 工作流入口 | 48.7K+ |
| [memU](https://github.com/NevaMind-AI/memU) | 🧠 面向常驻主动 Agent 的长期记忆层 | 14K+ |
| [agency-agents](https://github.com/msitarzewski/agency-agents) | 🏢 完整 AI Agency 代理团队，覆盖工程、增长、社区与交付流程 | 132.1K+ |
| [github/spec-kit](https://github.com/github/spec-kit) | 💫 GitHub 官方规格驱动开发工具包，串联需求、计划、任务与实现 | 121.8K+ |
| [bytedance/deer-flow](https://github.com/bytedance/deer-flow) | 🦌 字节开源长周期 SuperAgent 框架：沙箱、记忆、Tools、Skills 与 Subagents | 77.2K+ |
| [paperclip](https://github.com/paperclipai/paperclip) | 📎 面向零人公司的开源 Agent 编排平台 | 73.9K+ |
| [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) | 🧰 面向 Claude Code / Codex / OpenCode 的 Agent Harness 工具箱 | 66K+ |
| [nexu-io/html-anything](https://github.com/nexu-io/html-anything) | AI Agent HTML 编辑器，75 个 Skills × 9 种输出形式 | 7.8K+ |
| [op7418/guizang-social-card-skill](https://github.com/op7418/guizang-social-card-skill) | 小红书轮播图与微信封面生成 Skill | 5.1K+ |
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | Bug 挖掘与红队技能包，包含 71 个技能 | 3K+ |
| [muxuuu/serenity-skill](https://github.com/muxuuu/serenity-skill) | 供应链瓶颈股票研究 Agent Skill | 3.5K+ |
| [DenisSergeevitch/agents-best-practices](https://github.com/DenisSergeevitch/agents-best-practices) | Codex / Claude Code 通用 Agent 最佳实践 | 2.1K+ |
| [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | 逆向工程与渗透测试 Skill 路由包 | 8.3K+ |
| [JimLiu/baoyu-design](https://github.com/JimLiu/baoyu-design) | 本地 UI 设计 Agent Skill | 2.6K+ |
| [Kaelio/ktx](https://github.com/Kaelio/ktx) | 数据分析 Agent 可执行上下文层 | 1.5K+ |

### 📣 平台运营 / 自媒体 / 办公流量

| 技能 | 说明 |
|------|------|
| [XiaohongshuSkills](https://github.com/white0dew/XiaohongshuSkills) | 小红书自动化运营 Skill：自动发布、评论、检索，支持 OpenClaw / Codex / Claude Code（3.2K⭐）|
| [ai-trend-publish](https://github.com/liyown/ai-trend-publish) | 公众号自动化运营系统：多源抓取 + AI 写作 + 智能排序 + 定时发布（3.1K⭐）|
| [wx-favorites-report](https://github.com/zhuyansen/wx-favorites-report) | 微信收藏可视化 Skill：从加密 DB 到交互式 HTML 报告的端到端管线（625⭐）|
| [feishu-openclaw](https://github.com/AlexAnys/feishu-openclaw) | 飞书 / Lark 连接 OpenClaw：免公网、免域名、稳定接入机器人（318⭐）|
| [easy-wx/wecom-bot-svr](https://github.com/easy-wx/wecom-bot-svr) | 企业微信机器人回调服务框架：pip 安装、开箱即用、快速部署（179⭐）|
| [yulong-ge/AIFeedTracker](https://github.com/yulong-ge/AIFeedTracker) | AI 内容追踪 + 视频总结 + 飞书机器人集成（169⭐）|
| [rawchen/feishu-bot](https://github.com/rawchen/feishu-bot) | 飞书群聊 / 私聊机器人，Spring Boot 实现（159⭐）|
| [loonghao/wecom-bot-mcp-server](https://github.com/loonghao/wecom-bot-mcp-server) | 企业微信机器人 MCP Server，支持上下文感知自动消息处理（98⭐）|
| [openclaw-china](https://github.com/BytePioneer-AI/openclaw-china) | OpenClaw 中国 IM 渠道插件：飞书 / 钉钉 / QQ / 企业微信 / 微信公众号 一站式接入（4K⭐）|
| [Claude-to-IM-skill](https://github.com/op7418/Claude-to-IM-skill) | Claude Code / Codex IM 桥接 Skill：把 Telegram / Discord / 飞书 / QQ / 微信接到 AI 编码代理，支持后台守护进程、权限审批、流式预览与会话持久化，安装与更新说明完整（2.8K⭐）|
| [makenotion/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) | Notion 官方 MCP Server：OAuth 接入 + Markdown 页面编辑 + AI Agent 低 token 工具集（4.5K⭐）|
| [cyanheads/obsidian-mcp-server](https://github.com/cyanheads/obsidian-mcp-server) | Obsidian 知识库 MCP Server：读写笔记、全文检索、Frontmatter/Tag 管理（630⭐）|
| [YishenTu/claudian](https://github.com/YishenTu/claudian) | Obsidian 内嵌 Claude Code / Codex 协作插件：让知识库直接成为 Agent 工作目录，支持 Skills、MCP、计划模式（14.1K⭐）|
| [freestylefly/openclaw-wechat](https://github.com/freestylefly/openclaw-wechat) | OpenClaw 个人微信通道插件：真实微信账号接入、扫码登录、群聊/私聊收发与多账号支持（1.7K⭐）|
| [autoclaw-cc/xiaohongshu-skills](https://github.com/autoclaw-cc/xiaohongshu-skills) | 小红书自动化 Skills：真实浏览器 + 真实账号环境，覆盖发布、评论、检索、批量运营与 CLI 调用（1.6K⭐）|
| [IanShaw027/wemp-operator](https://github.com/IanShaw027/wemp-operator) | 微信公众号自动化运营 OpenClaw Skill：内容采集、数据分析、互动管理，内置 70 个 API、20+ 数据源，支持直接安装（102⭐）|
| [geekjourneyx/md2wechat-skill](https://github.com/geekjourneyx/md2wechat-skill) | 公众号 Markdown 排版与草稿箱上传 Skill：支持 Claude Code / Codex / OpenClaw 安装，适合内容运营批量发布（3.3K⭐）|
| [googleworkspace/cli](https://github.com/googleworkspace/cli) | Google Workspace 全能 CLI：统一操作 Gmail / Drive / Docs / Sheets / Calendar，并内置 40+ agent skills，适合办公自动化与 AI 助手集成（29.7K⭐）|
| [ythx-101/x-tweet-fetcher](https://github.com/ythx-101/x-tweet-fetcher) | X / 微信文章抓取 Skill：三后端智能回退，支持推文、列表、长文与微信内容检索，适合热点跟踪和自媒体选题（901⭐）|
| [qiaomu-anything-to-notebooklm](https://github.com/joeseesun/qiaomu-anything-to-notebooklm) | 多源内容处理 Claude Skill：支持微信文章 / 网页 / YouTube / PDF / 播客 / Office 文档，并可一键生成播客、PPT、脑图、Quiz，适合内容运营与知识整理（5.6K⭐）|
| [tuya-openclaw-skills](https://github.com/tuya/tuya-openclaw-skills) | 涂鸦官方 OpenClaw 智能家居技能库：接入 3000+ 设备品类，支持设备控制、天气、通知、摄像头抓拍与事件订阅，安装门槛清晰（564⭐）|
| [gemini_cli_skill](https://github.com/forayconsulting/gemini_cli_skill) | Gemini CLI 增强 Skill：让 Claude Code 协同调用 Gemini CLI 做代码生成、代码审查、测试生成、文档编写、网页研究与架构分析，安装与前置条件清晰（187⭐）|
| [vivy-yi/xiaohongshu-skills](https://github.com/vivy-yi/xiaohongshu-skills) | 小红书完整运营技能库：139 个 SKILL.md 覆盖内容创作、账号运营、互动运营、数据分析、电商转化、平台规则、工具生态、营销推广、增长策略 9 大分类，安装步骤清晰，适合中文运营场景（303⭐）|
| [skillx](https://github.com/nextlevelbuilder/skillx) | AI Agent 技能市场：集 Web Marketplace、CLI、语义搜索、排行榜、评分与 Claude Code 插件市场于一体，适合多技能发现与安装（157⭐）|
| [content-collector-skill](https://github.com/vigorX777/content-collector-skill) | 社交内容收藏助手：自动抓取 X / 微信公众号 / 即刻 / Reddit / 知乎 / B 站等内容，经 AI 整理后写入飞书多维表格，README 完整、安装前置清晰，适合内容运营与知识沉淀（236⭐）|
| [farion1231/cc-switch](https://github.com/farion1231/cc-switch) | 跨平台代理桌面管理器：统一管理 Claude Code / Codex / Gemini CLI / OpenCode / OpenClaw 的账号、模型、配置与切换，中文文档完善、安装包齐全，适合高频多 Agent 用户（117.9K⭐）|
| [cso1z/Feishu-MCP](https://github.com/cso1z/Feishu-MCP) | 飞书文档与任务管理 MCP/CLI 工具：支持文档读写、任务 CRUD、用户查询，并可配合 Feishu-Skill 让 Claude Code / Cursor / Cline 自动化操作飞书，安装与配置说明完整（710⭐）|
| [larksuite/cli](https://github.com/larksuite/cli) | 飞书 / Lark 官方 CLI：覆盖消息、文档、Base、表格、日历、邮箱、任务、会议等 14 个业务域，提供 200+ 命令与 20+ AI Agent Skills，安装路径清晰，适合办公自动化与 Agent 集成（15.6K⭐）|
| [superpowers-marketplace](https://github.com/obra/superpowers-marketplace) | Claude Code 插件市场：聚合 superpowers、写作规范、Claude Code 开发工具与私密日记 MCP 等高质量插件，安装命令简单，适合需要持续扩展插件/技能生态的重度用户（1.2K⭐）|
| [CowAgent](https://github.com/zhayujie/CowAgent) | 微信 / 飞书 / 钉钉 / 企微 / QQ / 公众号 / 网页多渠道 AI 助理与 Agent 框架：内置 Skills 引擎、长期记忆、知识库、任务规划和工具调用，支持从 Skill Hub / GitHub 一键安装技能（46K⭐）|
| [nexu](https://github.com/nexu-io/nexu) | OpenClaw 桌面客户端与多 IM 连接器：一键把本地 AI Agent 接入微信、飞书、Slack、Discord，支持 Claude Code / Codex / 任意 LLM，BYOK、本地优先、移动端随时调度（3.2K⭐）|
| [TrendRadar](https://github.com/sansan0/TrendRadar) | AI 舆情与热点监控系统：聚合多平台热点 / RSS，支持关键词筛选、AI 简报和微信 / 飞书 / 钉钉 / Telegram 推送，并可接入 MCP 做趋势分析（60.6K⭐）|
| [wechatDownload](https://github.com/qiye45/wechatDownload) | 微信公众号文章批量下载工具：支持合集、评论、HTML / Markdown / PDF / DOCX 导出，并提供 MCP / Skill 调用能力，适合内容沉淀与选题分析（8.5K⭐）|
| [wenyan-mcp](https://github.com/caol64/wenyan-mcp) | 文颜 MCP Server：让 AI 自动完成 Markdown 排版并发布到微信公众号，适合公众号运营与内容发布自动化（1.3K⭐）|
| [OpenCoworkAI/open-cowork](https://github.com/OpenCoworkAI/open-cowork) | 开源 AI Agent 桌面应用：一键安装 Claude Code、MCP 工具和 Skills，支持沙箱隔离、多模型与飞书 / Slack 集成（1.9K⭐）|
| [Xiangyu-CAS/xiaohongshu-ops-skill](https://github.com/Xiangyu-CAS/xiaohongshu-ops-skill) | 小红书运营 OpenClaw Skill：基于浏览器自动化，覆盖推荐流分析、账号分析、选题灵感、知识库沉淀、自动发布与评论回复，README 有完整示例和安装说明（2.1K⭐）|
| [MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian) | Obsidian MCP Server：通过 Obsidian REST API 插件让 Claude Code / Cursor 等 Agent 读写知识库、搜索笔记和管理内容，活跃度高、社区采用广（4.1K⭐）|
| [leemysw/feishu-docx](https://github.com/leemysw/feishu-docx) | 飞书 / Lark 文档 Markdown 导出与写入工具：支持 Docs / Sheet / Bitable、OAuth 2.0、CLI/TUI、公众号导入与 Claude Skills，适合团队知识库和内容流转自动化（238⭐）|
| [Wechat-ggGitHub/wechat-claude-code](https://github.com/Wechat-ggGitHub/wechat-claude-code) | 个人微信接入 Claude Code Skill：把手机微信作为 Claude Code 远程入口，支持图片识别、权限审批、Slash Commands、实时工具进度与高风险命令拦截，适合把开发 Agent 接入移动办公流（612⭐）|
| [OrangeViolin/content-pipeline](https://github.com/OrangeViolin/content-pipeline) | 中文创作者内容生产线 Skill：一个提示词完成选题、写作、改写、排版和多平台发布准备，面向公众号 / 小红书 / 知乎等内容运营场景（203⭐）|
| [chenxiachan/xhs-claude-skills](https://github.com/chenxiachan/xhs-claude-skills) | 小红书转 Obsidian Claude Code 插件：图文/视频帖子采集、视频转录、Markdown 笔记沉淀，无需 MCP 或浏览器后端，安装前置清晰（379⭐）|
| [czlonkowski/n8n-skills](https://github.com/czlonkowski/n8n-skills) | n8n 工作流 Claude Code Skill：把节点配置、表达式、凭证检查和最佳实践固化为可复用技能，README 安装步骤清晰，适合低代码自动化与运营流程编排（5.8K⭐）|
| [langbot-app/LangBot](https://github.com/langbot-app/LangBot) | 生产级多平台智能机器人开发平台：支持微信、企微、公众号、飞书、钉钉、QQ、Slack、Discord 等渠道，内置 Agent、知识库编排和插件系统，适合企业 IM 助手与私有化运营（16.9K⭐）|
| [iniwap/AIWriteX](https://github.com/iniwap/AIWriteX) | 微信公众号全自动 AI 运营工具：热点聚合、趋势分析、爆款选题、文章采集、生成、排版发布与多平台分发，覆盖小红书 / 百家号 / 抖音等创作者场景（1.4K⭐）|
| [AgriciDaniel/claude-ads](https://github.com/AgriciDaniel/claude-ads) | Claude Code 广告投放审计 Skill：250+ 检查项覆盖 Google / Meta / YouTube / LinkedIn / TikTok 等平台，支持加权评分、并行 Agent、行业模板与 AI 创意生成，适合投放优化和营销复盘（7.1K⭐）|
| [Affitor/affiliate-skills](https://github.com/Affitor/affiliate-skills) | 联盟营销 Agent Skills：50 个技能覆盖趋势研究、数据化文章、信息图、落地页、部署与社媒情报飞轮，兼容 Claude Code / Gemini / Cursor / Windsurf（548⭐）|
| [minhnv0807/ai-business-skills](https://github.com/minhnv0807/ai-business-skills) | AI Business Skills：60 个生产级营销 Skills + 5 个 Agents + 15 个 Workflows，覆盖越南、本地化个人品牌、TikTok/Meta 广告、Dropshipping 与全球市场运营，MIT 开源且安装文档完整（499⭐）|
| [zubair-trabzada/ai-agency-claude](https://github.com/zubair-trabzada/ai-agency-claude) | AI Agency Command Center for Claude Code：用 5 个并行团队把营销、销售、法务、声誉和 GEO/SEO 审计编排成统一客户报告，提供一行安装、9 个 skills、5 个 agents 和 PDF 交付链路，适合咨询顾问与运营服务商（113⭐）|
| [liangdabiao/tikhub_api_skill](https://github.com/liangdabiao/tikhub_api_skill) | TikHub API Claude Code Skill：封装抖音 / TikTok / 小红书 / Instagram / YouTube / X / Reddit 等多平台数据 API 搜索、发现与调用说明，适合社媒数据分析和选题监控（112⭐）|
| [joewongjc/feishu-claude-code](https://github.com/joewongjc/feishu-claude-code) | 飞书 × Claude Code WebSocket 桥接：让团队在飞书中实时调度 Claude Code CLI，对话链路清晰，适合企业内协作和移动端远程操作（162⭐）|
| [xhs_content_agent](https://github.com/hl897tech/xhs_content_agent) | 小红书内容运营 Agent：用 Playwright 抓取热门笔记、分析爆款规律、生成选题/文案/配图，并支持 API/MCP 一键发布，适合小红书矩阵号与自媒体自动化（253⭐）|
| [xhs-mcp-server](https://github.com/aicu-icu/xhs-mcp-server) | 小红书 MCP Server：覆盖笔记/用户搜索、通知消息监控等高频工具调用，README 有配置与调用示例，适合给 Claude Code / Cursor 接入小红书数据源（176⭐）|
| [douyin-upload-mcp-skill](https://github.com/WJZ-P/douyin-upload-mcp-skill) | 抖音视频/图文上传 MCP 与 Skill：基于浏览器自动化发布内容，适配 OpenClaw 与任意支持 Skill/MCP 的 Agent，适合短视频运营发布链路补齐（71⭐）|
| [zubair-trabzada/ai-marketing-claude](https://github.com/zubair-trabzada/ai-marketing-claude) | Claude Code AI Marketing Suite：15 个营销技能加并行子代理，覆盖网站审计、文案、邮件序列、广告活动、内容日历、竞品情报与客户级 PDF 报告（2.1K⭐）|
| [aaron-marketing-skills](https://github.com/aaron-he-zhu/aaron-marketing-skills) | 120 个营销技能覆盖 SEO/GEO、达人营销、付费广告、邮件、产品发布、社媒和品牌叙事 7 类场景，提供 Claude Code Plugin 与 `npx skills` 统一安装入口；外部连接器和写操作需显式授权（2.4K⭐）|
| [openclaudia-skills](https://github.com/OpenClaudia/openclaudia-skills) | OpenClaudia 营销技能库：34 个开源 Claude Code 营销 skills，覆盖 SEO、内容、邮件、广告、分析和增长，安装方式直接，适合作为运营团队基础技能包（573⭐）|
| [Eronred/aso-skills](https://github.com/Eronred/aso-skills) | App Store Optimization 营销 Agent Skills：关键词研究、元数据优化、竞品分析和 App 增长策略，兼容 Claude Code / Cursor 等 Agent，适合独立开发者和增长团队（1.6K⭐）|
| [zubair-trabzada/ai-ads-claude](https://github.com/zubair-trabzada/ai-ads-claude) | Claude Code 广告策略 Skill：生成 Google / Meta / LinkedIn / TikTok / YouTube / Pinterest 广告文案、漏斗、预算分配与 PDF 策略报告（200⭐）|
| [Bwkyd/wexin-read-mcp](https://github.com/Bwkyd/wexin-read-mcp) | 微信公众号文章阅读 MCP：用浏览器模拟让大模型读取公众号文章内容，适合内容调研、素材整理与选题分析（438⭐）|
| [DemonDamon/AgenticX](https://github.com/DemonDamon/AgenticX) | 生产级多 Agent 平台：Python SDK + CLI + Studio + 桌面端，内置 MCP Hub、层级记忆、Skill 生态、安全沙箱与飞书/微信 IM 网关，适合把办公协作和 Agent 技能运营统一到一套平台（185⭐）|
| [LAVARONG/wechat-automation-api](https://github.com/LAVARONG/wechat-automation-api) | 微信 Windows 自动化发送 Agent Skill / HTTP API：基于 UI 自动化支持文本、图片、批量发送和队列管理，非 Hook/非协议（157⭐）|
| [zhimaAi/ChatClaw](https://github.com/zhimaAi/ChatClaw) | 轻量 OpenClaw-like 个人 AI Agent：内置 Skill Market、知识库、记忆、MCP、定时任务，并连接微信企微、飞书、钉钉、QQ、Slack 等渠道（302⭐）|
| [aitytech/agentkits-marketing](https://github.com/aitytech/agentkits-marketing) | 企业级 AI 营销自动化 AgentKit：18 个 Agents、93 条 Commands、28 个 Skills，覆盖 SaaS 增长、内容、SEO、营销活动、报告与数据分析（566⭐）|
| [kostja94/marketing-skills](https://github.com/kostja94/marketing-skills) | Marketing & SEO Skills for AI Agents：160+ Markdown 技能覆盖 SEO、页面类型、付费广告、渠道和策略，支持 npx skills 安装（738⭐）|
| [BrianRWagner/ai-marketing-claude-code-skills](https://github.com/BrianRWagner/ai-marketing-claude-code-skills) | Claude Code 营销框架技能集：23 个免费 + 10 个 Pro skills，支持 quick/standard/deep 执行模式，覆盖转化、定位、文案、渠道和增长审计（369⭐）|
| [AgriciDaniel/claude-youtube](https://github.com/AgriciDaniel/claude-youtube) | YouTube 创作者 Claude Code Skill：14 个子技能覆盖频道审计、视频 SEO、留存脚本、标题缩略图、Shorts、内容日历、变现和竞品分析，README 文档完整且仍活跃（249⭐）|
| [sergebulaev/linkedin-skills](https://github.com/sergebulaev/linkedin-skills) | LinkedIn 增长 Claude Code Skills：面向创作者、Founder 和营销团队，覆盖自然帖、评论、信息流分析与发布节奏，适合 B2B 自媒体运营（386⭐）|
| [Linked-API/linkedin-skills](https://github.com/Linked-API/linkedin-skills) | LinkedIn 自动化 Agent Skills：支持资料检索、企业/人员搜索、消息、连接与内容互动，兼容 Claude Code / Codex / Cursor；依赖 Node.js 20、Linked API Token 和真实云浏览器，操作真实账号前需确认并遵守平台规则（35⭐）|
| [ijerryhuang/xiaohongshu-auto-operation](https://github.com/ijerryhuang/xiaohongshu-auto-operation) | 小红书账号全自动运营 OpenClaw Skill：选题、内容生成、封面、定时发布和数据报告全流程自动化，安装依赖与 MCP 配置说明清晰（78⭐）|
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | 多平台内容检索 CLI/MCP：无需官方 API 即可读搜 X / Reddit / YouTube / GitHub / B 站 / 小红书，中文 README、安装和 Agent 接入说明完整，适合热点追踪、自媒体选题与竞品情报（57.2K⭐）|
| [xpzouying/xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) | 小红书 MCP Server：支持搜索、笔记/用户数据读取与 Agent 工具调用，README 详尽、仍活跃，适合给 Claude Code / Cursor 接入小红书内容调研能力（14.7K⭐）|
| [BiboyQG/WeChat-MCP](https://github.com/BiboyQG/WeChat-MCP) | WeChat MCP Server：让 OpenClaw / Claude / ChatGPT 等助手读取和回复微信消息，提供 PyPI 安装、配置和文档站，适合个人微信 Agent 助理（219⭐）|
| [iFurySt/RedNote-MCP](https://github.com/iFurySt/RedNote-MCP) | 小红书 / RedNote MCP Server：npm 包安装，提供内容访问、检索与 Agent 工具接入说明，适合把 Claude Code / Cursor 接入小红书内容调研（1.1K⭐）|
| [autoclaw-cc/xiaohongshu-mcp-skills](https://github.com/autoclaw-cc/xiaohongshu-mcp-skills) | 基于 xiaohongshu-mcp 的 Agent Skills 集合：覆盖安装部署、扫码登录、发布图文、搜索笔记与数据抓取，兼容 OpenClaw / Claude Code（234⭐）|
| [agenmod/immortal-skill](https://github.com/agenmod/immortal-skill) | 开源数字分身 / 记忆蒸馏 Agent Skill：支持微信、飞书、iMessage、Telegram 等聊天记录采集，按 OpenClaw Soul Spec 蒸馏人格画像，中文 README 和安装说明完整（906⭐）|
| [aiworkskills/wechat-article-skills](https://github.com/aiworkskills/wechat-article-skills) | 微信公众号 AI 运营 Skills：选题、写稿、审稿、排版、配图、发布全流程，支持 OpenClaw / Claude Code / Cursor / Codex，中文文档完善（389⭐）|
| [KroMiose/nekro-agent](https://github.com/KroMiose/nekro-agent) | 跨平台多人互动 Agent 框架：集 Claude Code 沙盒执行、MCP 管理、长期记忆和可视化控制台于一体，支持 QQ / Discord / Telegram / BilibiliLive / WeChat / Email 等渠道，中文文档与 Docker/PyPI 安装完善（1.1K⭐）|
| [Dcatfly/weixin_claude_code](https://github.com/Dcatfly/weixin_claude_code) | 微信 Channel 插件 for Claude Code：通过微信双向通信、远程审批工具调用，支持文本/图片/语音/视频/文件，安装流程清晰，适合手机端远程调度本地 Claude Code（57⭐）|
| [nexscope-ai/eCommerce-Skills](https://github.com/nexscope-ai/eCommerce-Skills) | 电商运营 Agent Skills：142 个免费技能覆盖 Amazon / Shopify / eBay / Etsy / TikTok Shop / Walmart 的选品、营销自动化、供应链与数据分析，支持 OpenClaw / Claude Code / Cursor / Codex（391⭐）|
| [pawbytes/skill-suites](https://github.com/pawbytes/skill-suites) | 59 个 AI Agent Skill Suites：包含 23 个营销自动化技能、创意代理流程、产品开发与开发者效率模块，支持 npx skills 安装，适合运营流程编排参考（74⭐）|
| [gtmagents/gtm-agents](https://github.com/gtmagents/gtm-agents) | GTM / Revenue Ops Agent Skills：覆盖销售、市场、客户成功和增长运营工作流，面向 Claude Code 的生产级 go-to-market 技能集合，适合 SaaS 团队搭建获客与转化自动化（334⭐）|
| [ArtemXTech/personal-os-skills](https://github.com/ArtemXTech/personal-os-skills) | Obsidian × Claude Code 个人操作系统 Skills：把项目、日记、任务和知识库组织成 AI-first 工作台，适合创作者、研究者和知识工作者长期沉淀上下文（523⭐）|
| [huytieu/COG-second-brain](https://github.com/huytieu/COG-second-brain) | 自演化第二大脑：17 个 AI skills + 6 个 worker agents + People CRM，兼容 Claude Code / Cursor / Kiro / Gemini CLI / Codex，适合个人知识管理与关系运营（603⭐）|
| [bitbonsai/mcpvault](https://github.com/bitbonsai/mcpvault) | 轻量 Obsidian Vault MCP Server：强调安全的本地知识库访问、搜索和笔记操作，适合把个人第二大脑接入 Claude Code / Cursor 等 Agent 工作流（1.5K⭐）|
| [laborany/laborany](https://github.com/laborany/laborany) | 基于 Claude Code 的桌面 AI 工作力平台：支持飞书 / QQ 远程调度、技能创建和定时任务，定位 OpenClaw 桌面实现，适合非开发者低门槛养成 AI 助手（73⭐）|
| [yaoleifly/wechat-writing-style](https://github.com/yaoleifly/wechat-writing-style) | 微信公众号中文写作风格 Claude Code Skill：沉淀账号语气、标题和排版偏好，适合公号作者把个人风格复用到选题、改稿与发布准备（64⭐）|
| [wewrite](https://github.com/imraywang/wewrite) | 公众号文章全流程 AI Skill：热点抓取、选题评分、素材采集、SEO 优化、AI 配图、微信排版与草稿箱推送，兼容 Claude Code / OpenClaw，安装和首次风格引导清晰（2.8K⭐）|
| [Jane-xiaoer/feishu-portfolio-launch](https://github.com/Jane-xiaoer/feishu-portfolio-launch) | 飞书多维表格 → GitHub Pages 作品集网站 Claude Code Skill：把内容表格、静态站点生成和上线流程串起来，适合运营作品集与个人品牌展示（71⭐）|
| [viktorxhzj/feishu-webhook-skill](https://github.com/viktorxhzj/feishu-webhook-skill) | 飞书 / Lark Webhook 通知 Claude Code Skill：让本地 Agent 把任务进度、日报和自动化结果推送到飞书群，安装与调用方式简单（30⭐）|
| [Varnan-Tech/opendirectory](https://github.com/Varnan-Tech/opendirectory) | GTM / 技术营销 / 增长自动化 Agent Skills 目录：51 个预置技能，支持 Claude、Codex、Gemini CLI，通过 npm 一键安装，README 展示完整分类与安装路径（546⭐）|
| [nicepkg/ai-workflow](https://github.com/nicepkg/ai-workflow) | 跨平台 AI Workflow 技能集合：170+ 预置技能覆盖内容创作、营销增长、视频、交易、产品管理与演示，支持 Claude Code / Cursor / Codex / OpenCode 等 14+ AI 工具，一条命令安装（266⭐）|
| [yhslgg-arch/url-reader](https://github.com/yhslgg-arch/url-reader) | 智能网页内容读取 Claude Code Skill：自动识别微信公众号 / 小红书 / 今日头条 / 抖音 / 淘宝等平台，Firecrawl → Jina → Playwright 三层降级，输出 Markdown 并可保存图片，适合内容调研与选题归档（184⭐）|
| [absolute](https://github.com/maddhruv/absolute) | AI Agent Skills 注册表：覆盖框架 API、营销策略等领域，兼容 Claude Code / Gemini CLI / Codex / Cursor 等工具，提供网站与 skills.sh 安装入口（196⭐）|
| [ParthJadhav/ios-marketing-capture](https://github.com/ParthJadhav/ios-marketing-capture) | iOS App 营销截图采集 Skill：为 SwiftUI 应用自动植入 DEBUG 截图系统、填充演示数据并按多语言批量导出素材，适合独立开发者做 App Store 上架与本地化营销（250⭐）|
| [wonda](https://github.com/degausai/wonda) | 终端内容生成 CLI：统一生成图片、视频、音乐、音频、编辑与社交发布流程，npm 安装清晰，适合创作者多模态内容生产（136⭐）|
| [fastclaw-ai/weclaw](https://github.com/fastclaw-ai/weclaw) | 微信 AI Agent Bridge：一行安装把个人微信接入 Claude / Codex / Gemini / Kimi 等 Agent，扫码登录、多账号与 Docker/Go 安装路径清晰，适合移动端调度本地代理（1.6K⭐）|
| [sunnoy/openclaw-plugin-wecom](https://github.com/sunnoy/openclaw-plugin-wecom) | OpenClaw 企业微信增强插件：基于 WebSocket 长连接，支持多账号、动态 Agent 隔离、Webhook 出站、企业微信 MCP 文档/智能表格能力与白名单控制（704⭐）|
| [zhaoxinyi02/ClawPanel](https://github.com/zhaoxinyi02/ClawPanel) | OpenClaw 智能管理面板：Go 单二进制 + React，可统一管理 20+ 通道、实时日志和外部运行时，适合团队化运维 OpenClaw / IM Agent（853⭐）|
| [miantiao-me/bm.md](https://github.com/miantiao-me/bm.md) | Markdown 排版助手：一键适配微信公众号、网页与图片，提供 CLI / REST API / MCP 集成和 14 种排版样式，适合公众号发布前排版自动化（595⭐）|
| [bzd6661/wechat-article-for-ai](https://github.com/bzd6661/wechat-article-for-ai) | 微信公众号文章转 Markdown 工具：面向 AI Agent 的 MCP Server + SKILL.md，支持反检测抓取、批量处理、图片本地化与结构化元数据（85⭐）|
| [wechatsync/Wechatsync](https://github.com/wechatsync/Wechatsync) | 多平台文章同步发布工具：一键把内容分发到公众号生态相关的今日头条、知乎、简书、掘金、CSDN、WordPress 等平台，TypeScript 实现、插件生态成熟，适合内容运营分发链路（6K⭐）|
| [iBigQiang/feedgrab](https://github.com/iBigQiang/feedgrab) | 多平台内容抓取与摘要工具：统一抓取微信、小红书、X/Twitter、YouTube、B 站、Telegram、RSS 等来源，输出规范化内容与摘要，适合自媒体选题监控和知识沉淀（556⭐）|
| [zhylq/yuan-skills](https://github.com/zhylq/yuan-skills) | 公众号写作 Agent Skills：主写作 + 配图 + Markdown 转微信 HTML + 草稿箱发布 4 个技能，支持 `npx skills add` 安装，适合中文创作者把选题、证据池、润色和发布前处理串成闭环（38⭐）|
| [next-open-ai/openclawx](https://github.com/next-open-ai/openclawx) | 国产桌面级 AI Agent 平台：CLI / Web / Desktop 多端，已接入飞书、钉钉、Telegram、微信，支持 Claude Code / OpenCode 代理、MCP、Skills、插件和本地推理 0 Token，中文文档体系完整（55⭐）|
| [YYH211/xiaohongshu](https://github.com/YYH211/xiaohongshu) | 小红书内容自动生成与发布 MCP 应用：从主题输入到文案/图片生成再到自动发布，适合验证小红书运营工作流的端到端自动化（162⭐）|
| [luyike221/xiaohongshu-mcp-python](https://github.com/luyike221/xiaohongshu-mcp-python) | 小红书 MCP Python 服务：支持登录管理、图文/视频发布、内容搜索、帖子详情和评论互动，格式与配置说明完整，适合创作者和营销团队接入 AI 工作流（129⭐）|
| [adennng/wechat-query-skill](https://github.com/adennng/wechat-query-skill) | OpenClaw 微信公众号订阅/查询/推送 Skill：内置本地 wechat-download-api、SQLite 缓存、订阅轮询、文章查询、每日汇总和登录巡检流程，中文 README 有部署链路与场景说明（67⭐）|
| [hekaixin66-sketch/xiaohongshuritter](https://github.com/hekaixin66-sketch/xiaohongshuritter) | 企业级小红书多账号 MCP 系统：支持多租户、并发控制、图文/视频发布、搜索、评论与账号状态管理，提供 Docker / 源码 / OpenClaw 多种部署文档，适合团队运营矩阵号（134⭐）|
| [rediumvex/viral-hooks-skill](https://github.com/rediumvex/viral-hooks-skill) | 短视频爆款开头 Claude Code Skill：内置 100 个 hook 公式与 10 类心理触发器，为 TikTok / Reels / YouTube Shorts / LinkedIn / X 生成 3 个可测试开头，适合内容运营脚本优化（62⭐）|
| [bi-boo/claude-model-fingerprint](https://github.com/bi-boo/claude-model-fingerprint) | 个人 Claude Code Skills 合集：覆盖公众号文章、多视角对话素材、会议方法论提炼、文字稿润色、小宇宙播客下载与模型指纹检测，适合内容团队沉淀日常工作流（73⭐）|
| [CosmoBlk/email-marketing-bible](https://github.com/CosmoBlk/email-marketing-bible) | Email Marketing Bible Claude Code Skill：68,000 词、908 个来源、19 个行业 playbook 和 57 个邮件设计案例，覆盖邮件审计、自动化流程、冷邮件、合规与投放文案，一行 git clone 安装，适合跨境电商 / SaaS 增长团队（243⭐）|
| [geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | GEO-first SEO Claude Code Skill：面向 ChatGPT / Claude / Perplexity / Gemini / Google AI Overviews 做 AI 搜索优化，提供 citability 评分、AI crawler 分析、品牌权威、Schema 标记和 PDF 报告，一行 curl 安装，适合企业官网与内容团队做 GEO/SEO 审计（9K⭐）|
| [Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills) | 多模态内容生成 Agent Skills：用 muapi-cli 让 Claude Code / Cursor / Gemini CLI 生成、编辑并展示图片/视频/音频，内置 100+ 模型与 MCP Server，适合品牌视觉、短视频和创意素材生产（3.8K⭐）|
| [n8n-claw](https://github.com/freddy-schuetz/n8n-claw) | 基于 n8n 的自托管 OpenClaw-like AI Agent：PostgreSQL 记忆、MCP Skills Library、专家代理、Telegram/HTTP 接入和定时任务，安装文档完整，适合无代码团队把运营自动化部署到私有基础设施（540⭐）|
| [social-media-skills](https://github.com/blacktwist/social-media-skills) | 社媒策略与内容 Agent Skills：覆盖平台上下文、内容策略、发布日历、平台策略、创作与分析，适合把 LinkedIn / X / Instagram / TikTok 等账号运营方法论沉淀成可复用技能（334⭐）|
| [skilless.ai](https://github.com/BrikerMan/skilless.ai) | 给 Agent 增强真实数据能力的一键安装工具：提供网页搜索、网页读取、YouTube 字幕/视频处理、RSS 等数据技能，支持 Claude Code / Cursor / OpenCode 和中文文档，适合热点调研与内容素材采集（221⭐）|
| [liangdabiao/lark-workflow-feishu-cli](https://github.com/liangdabiao/lark-workflow-feishu-cli) | 飞书 AI 效率系统：22 大 Claude Code Skill 工作流覆盖个人 CRM、会议待办、知识库、内容创作、晨报、审批催办和团队 CRM，README 详尽、权限和定时自动化说明完整（56⭐）|
| [iamzifei/wechat-article-publisher-skill](https://github.com/iamzifei/wechat-article-publisher-skill) | 微信公众号草稿箱发布 Claude Code Skill：把 Markdown / HTML 文章通过官方 API 直接转成公众号草稿，自动处理格式与图片上传，README 中英双语、安装路径清晰，适合内容团队减少复制排版成本（148⭐）|
| [iamzifei/wechat-article-formatter-skill](https://github.com/iamzifei/wechat-article-formatter-skill) | 微信公众号文章排版 Claude Code Skill：将 Markdown 转为适配公众号的精美 HTML，支持本地图片上传、自定义 CSS、脚注链接转换，并可衔接发布 Skill 形成排版到草稿箱闭环（74⭐）|
| [manwithshit/xhs-images](https://github.com/manwithshit/xhs-images) | 小红书信息图生成 Claude Skill：把文章/笔记一键转成 1-10 张小红书配图，内置 11 种视觉风格与 6 种信息布局，适合知识博主和品牌号做图文素材批量生产（40⭐）|
| [ZeroPointRepo/youtube-skills](https://github.com/ZeroPointRepo/youtube-skills) | YouTube Transcript API Agent Skills：支持字幕提取、视频搜索、频道浏览和播放列表解析，兼容 OpenClaw / Hermes Agent / Claude Code / Cursor / Windsurf，README 安装和 API Key 配置清晰（332⭐）|
| [michalparkola/tapestry-skills](https://github.com/michalparkola/tapestry-skills) | Tapestry AI Agent 生产力 Skills：可下载文章、PDF、YouTube 字幕并转成学习笔记 / 决策材料，适合创始人、运营和知识工作者做资料消化（474⭐）|
| [ivangfalco/ads-skills](https://github.com/ivangfalco/ads-skills) | B2B 广告投放 Claude Code Skills：40+ 策略文件与 39 个 API 脚本覆盖 LinkedIn、Meta、Google Ads，适合增长团队把广告诊断和操作沉淀为 Agent 工作流（211⭐）|
| [wxkingstar/SpecFusion](https://github.com/wxkingstar/SpecFusion) | 中国开放平台 API 文档搜索 MCP/CLI：在 Claude Code / Cursor / Gemini CLI 里直接查询企业微信、飞书、钉钉、小红书、抖音电商、微信支付等 18 个平台文档（43⭐）|
| [MaxKmet/idea-validation-agents](https://github.com/MaxKmet/idea-validation-agents) | 创业想法验证 Agent Skills：从 idea brainstorming 到市场验证、GTM 策略和机会评估，兼容 Claude Code / Codex / Cursor，适合独立开发者和增长团队快速筛选项目（389⭐）|
| [feishu-whiteboard-pro](https://github.com/LcpMarvel/feishu-whiteboard-pro) | 可编辑飞书 / Lark 白板设计 Skill：用布局组件、预渲染 fit-check 和独立设计评审生成有层次的真实白板；依赖已认证的 `lark-cli` 与飞书账号，写入租户前需确认权限和敏感内容（51⭐）|

### 💻 开发效率

| 技能 | 说明 |
|------|------|
| [spec-driven-develop](https://github.com/zhu1090093659/spec_driven_develop) | 📋 规格驱动开发：7 阶段预开发流水线，架构优先，纯 Markdown（928⭐）|
| [robotics-agent-skills](https://github.com/arpitg1304/robotics-agent-skills) | 🤖 机器人开发技能集：ROS1/ROS2、设计模式、感知系统、Docker（316⭐）|
| [skill-optimizer](https://github.com/hqhq1025/skill-optimizer) | 🔧 Skill 诊断优化工具：基于真实会话数据的静态分析（135⭐）|
| [github-tech-scanner](https://github.com/claude-access/github-tech-scanner) | 扫描 GitHub 仓库的语言和框架（3⭐） |
| [review-checkpoint](https://github.com/Atharva-Kanherkar/review-checkpoint) | 结构化自审查工作流：先契约后代码（4⭐） |
| [archflow](https://github.com/rafaelolsr/archflow) | 将代码库转为动画 HTML 架构图（27⭐）|
| [autoresearch](https://github.com/uditgoenka/autoresearch) | 自主迭代研究：修改→验证→保留/丢弃→循环（5.3K⭐）|
| [SwiftUI-Agent-Skill](https://github.com/twostraws/SwiftUI-Agent-Skill) | iOS/macOS SwiftUI 开发专用技能（4.3K⭐）|
| [plugins-plus-skills](https://github.com/jeremylongshore/claude-code-plugins-plus-skills) | Claude Code 插件市场：425 插件 + 2,810 技能 + 200 代理，提供 `ccpi` CLI 与网站检索，适合批量发现、安装和治理团队技能（2.5K⭐）|
| [wednesday-solutions/ai-agent-skills](https://github.com/wednesday-solutions/ai-agent-skills) | Wednesday Agent Skills：为 Claude Code / Cursor / Gemini / Copilot 生成代码库知识图谱、风险评分、blast radius 和统一规则，适合大型项目减少 Agent 反复读文件与误改（160⭐）|
| [slavingia-skills](https://github.com/slavingia/skills) | 基于《极简创业者》理念的实用技能集（9.6K⭐）|
| [trailofbits-skills](https://github.com/trailofbits/skills) | Trail of Bits 安全研究与审计技能（6.1K⭐）|
| [skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory) | 技能工厂：一键生成、测试、发布 Claude Code 技能（830⭐）|
| [jeffallan-skills](https://github.com/Jeffallan/claude-skills) | 66 个全栈开发者专用技能，成为你的专家配对程序员（10.6K⭐）|
| [daymade-skills](https://github.com/daymade/claude-code-skills) | 专业技能市场，生产就绪的高质量技能集（1.3K⭐）|
| [pinme](https://github.com/glitternetwork/pinme) | 前端一键部署，Claude Code 技能驱动（3.7K⭐）|
| [playwright-skill](https://github.com/lackeyjb/playwright-skill) | Playwright 浏览器自动化，Claude 自主编写+执行测试（2.9K⭐）|
| [android-reverse](https://github.com/SimoneAvogadro/android-reverse-engineering-skill) | Android 应用逆向工程辅助（6.4K⭐）|
| [skill-codex](https://github.com/skills-directory/skill-codex) | 将提示词委派给 Codex 执行（1.4K⭐）|
| [claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | 股票投资者工具：技术分析、选股器、交易策略（2.4K⭐）|
| [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) | .NET 开发者专用技能集：子代理 + 标准化开发流程（1.1K⭐）|
| [dotnet/skills](https://github.com/dotnet/skills) | .NET 团队维护的 Agent Skills / Plugins：覆盖 C#、ASP.NET Core、Blazor、数据访问、MSBuild、NuGet、升级、测试、诊断、MAUI 与 .NET AI / MCP，提供 Claude Code / Copilot、Cursor 和 Codex 安装路径（4.6K⭐）|
| [planetscale/skills](https://github.com/planetscale/skills) | PlanetScale 官方数据库审查与运维 Skills：15 个技能覆盖只读盘点、Vitess / Postgres 安全、Query Insights、Schema 建议、CLI / MCP 与自动化；按 A–E 风险分级，生产变更要求明确授权、命名目标和回滚验证（99⭐）|
| [app-onboarding-questionnaire](https://github.com/adamlyttleapps/claude-skill-app-onboarding-questionnaire) | 高转化 App 引导页问卷设计：基于顶级订阅 App 的转化模式（1.1K⭐）|
| [bmad-skills](https://github.com/aj-geddes/claude-code-bmad-skills) | BMAD Method：自动检测 + Memory 集成 + 完整开发流程（461⭐）|
| [rails-upgrade](https://github.com/ombulabs/claude-code_rails-upgrade-skill) | Rails 一键升级技能，自动化版本迁移（366⭐）|
| [apple-skills](https://github.com/rshankras/claude-code-apple-skills) | iOS/macOS/iPadOS 开发专用技能集（520⭐）|
| [scrapling](https://github.com/Cedriccmh/claude-code-skill-scrapling) | 智能网页爬虫，自动 Fetcher 选择 + 反爬绕过（363⭐）|
| [context-mode](https://github.com/mksglu/context-mode) | 上下文窗口优化：工具输出沙箱化，减少 98%，支持 14 平台（19K⭐）|
| [claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) | Claude Code 基础设施展示：技能自动激活 + Hooks + Agents（9.7K⭐）|
| [chops](https://github.com/Shpigford/chops) | macOS 技能管理器：浏览/编辑/管理 Claude Code / Cursor / Codex 技能（1.4K⭐）|
| [sast-skills](https://github.com/utkusen/sast-skills) | 将 AI 编程助手变成 SAST 安全扫描器（1.1K⭐）|
| [cc-skills-golang](https://github.com/samber/cc-skills-golang) | Golang 开发专用 agentic skills 集合（2.6K⭐）|
| [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) | 将代码库转为交互式 HTML 课程（5.2K⭐）|
| [Continuous-Claude-v3](https://github.com/parcadei/Continuous-Claude-v3) | 通过 Hooks + Ledgers 实现持久化上下文管理（3.9K⭐）|
| [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) | Claude Code Hooks 完全指南：掌握事件驱动自动化（3.8K⭐）|
| [fireworks-tech-graph](https://github.com/yizhiyanhua-ai/fireworks-tech-graph) | 生成生产级 SVG+PNG 技术架构图，支持 8 种图表类型（8.8K⭐）|
| [claude-octopus](https://github.com/nyldn/claude-octopus) | 每个编码任务最多用 8 个 AI 模型并行审查（3.8K⭐）|
| [nothing-design-skill](https://github.com/dominikmartn/nothing-design-skill) | Nothing 设计语言 UI 生成：极简单色、排版、工业风（2.6K⭐）|
| [huashu-design](https://github.com/alchaincyf/huashu-design) | 🇨🇳 HTML 原生设计 Skill：高保真原型 + 设计系统 + 动效，Claude Code 专属（21.6K⭐）|
| [darwin-skill](https://github.com/alchaincyf/darwin-skill) | 🧬 技能进化系统：评估→改进→测试→保留或回滚，让 Skill 无限自优化（4.9K⭐）|
| [claude-forge](https://github.com/sangrokjung/claude-forge) | 11 个 AI Agent + 36 命令 + 15 技能，类 oh-my-zsh 插件框架（776⭐）|
| [agentic-stack](https://github.com/codejunkie99/agentic-stack) | 🧠 One brain, many harnesses：可移植 .agent/ 文件夹，跨 Claude/Cursor/Codex 共享（2.2K⭐）|
| [cartographer](https://github.com/kingbootoshi/cartographer) | 用并行子 Agent 映射和文档化任意规模代码库（604⭐）|
| [agent-skill-creator](https://github.com/FrancyJGLisboa/agent-skill-creator) | 将任意工作流转化为可复用的 AI Agent 技能，支持 14+ 工具（1.8K⭐）|
| [drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 从文本生成专业 draw.io 图表的 Agent Skill（5.9K⭐）|
| [ok-skills](https://github.com/mxyhi/ok-skills) | 精选 AI Agent 技能 + AGENTS.md Playbook 合集（453⭐）|
| [awesome-claude-code-config](https://github.com/Mizoreww/awesome-claude-code-config) | 生产级 Claude Code 配置：自改进循环 + 多语言规则 + MCP 集成（247⭐）|
| [agnix](https://github.com/agent-sh/agnix) | AI 编程助手的 Linter + LSP：校验 CLAUDE.md / AGENTS.md / SKILL.md / Hooks / MCP，支持 IDE 插件与自动修复（348⭐）|
| [writing-style-skill](https://github.com/jzOcb/writing-style-skill) | 写作风格技能模板，AI 写作→你编辑→自动学习→规则迭代（232⭐）|
| [plinth](https://github.com/jabrena/plinth) | Java 企业工程 Agent 工具箱：覆盖规划、架构、Maven、测试、性能、文档、Skills 与 MCP Servers（417⭐）|
| [Dimillian/Skills](https://github.com/Dimillian/Skills) | 高质量 Codex Skills 集合：GitHub 工作流、Diff Review Swarm、Bug Hunt Swarm、React 性能与 SwiftUI/iOS/macOS 专项开发（3.8K⭐）|
| [openai/skills](https://github.com/openai/skills) | OpenAI 官方 Codex Skills Catalog：内置 system / curated / experimental 技能目录，支持 `$skill-installer` 按名称或 GitHub 目录安装（23.8K⭐）|
| [awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills) | Codex 实用技能精选清单：覆盖开发、协作、沟通、数据分析等多类可安装 skills，并提供 GitHub 路径安装器（15K⭐）|
| [huggingface/skills](https://github.com/huggingface/skills) | Hugging Face 官方 Skills 仓库：覆盖模型选择、数据集处理、训练、评测、论文发布与 JS 推理，兼容 Claude Code / Codex / Gemini CLI / Cursor，安装方式清晰（10.8K⭐）|
| [NVIDIA/skills](https://github.com/NVIDIA/skills) | NVIDIA 官方验证 Agent Skills 目录：当前 230 个可安装技能覆盖 CUDA、Jetson、NeMo、DeepStream、TAO、RAG、医疗与 Physical AI，提供签名、治理卡和评测，并支持 Claude Code / Codex / Cursor 一行安装；具体技能可能依赖 NVIDIA GPU、云服务或产品环境（2.5K⭐）|
| [skills-manage](https://github.com/iamzhihuix/skills-manage) | 跨平台技能管理桌面应用：统一管理 Claude Code / Cursor / Gemini CLI / Codex / Hermes / OpenClaw 等 20+ 平台技能，支持本地发现、集合安装、GitHub 导入与市场浏览（2.1K⭐）|
| [BuilderIO/skills](https://github.com/BuilderIO/skills) | 🏗️ BuilderIO 官方 Agent Skills 集合，面向编码代理的生产级技能库（3.7K⭐）|
| [produck-skills](https://github.com/tryproduck/produck-skills) | 🛠️ 产品导向 Agent Skills：帮助构建用户喜爱的产品，Apache-2.0 开源（486⭐）|
| [loopy](https://github.com/Forward-Future/loopy) | 🔄 可复用 AI Agent 循环与工作流库：覆盖工程、评测、运营、内容与设计（2.7K⭐）|
| [skills-manager](https://github.com/xingkongliang/skills-manager) | 轻量级跨工具技能管理桌面应用：支持 Claude Code / Cursor / Codex / Copilot 等 15+ 工具的统一安装、同步、场景切换、项目工作区与 Git 备份，中文说明完善、截图清晰，适合重度技能用户集中管理（3.1K⭐）|
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Vercel 出品的开放 Agent Skills CLI：支持 OpenCode / Claude Code / Codex / Cursor 等 40+ Agent，提供安装、搜索、更新、初始化全流程（26.3K⭐）|
| [Dimillian/CodexSkillManager](https://github.com/Dimillian/CodexSkillManager) | macOS 技能管理器：统一浏览本地 Codex / Claude Code 技能，并可从 Clawdhub 搜索、下载、删除与导入，适合多技能重度用户（1.4K⭐）|
| [ui-design-brain](https://github.com/carmahhawwari/ui-design-brain) | Cursor UI 设计技能：基于 component.gallery 沉淀 60+ 组件最佳实践、布局模式、反模式与设计哲学，安装清晰，适合生成更像资深设计师产出的前端界面（843⭐）|
| [DrCatHicks/learning-opportunities](https://github.com/DrCatHicks/learning-opportunities) | Claude Code / Codex 学习型插件市场：在完成架构、重构、Schema 等代码工作后，自动生成 10-15 分钟刻意练习，内置 repo orientation 技能，适合团队把 AI 辅助编码转化为可复盘的能力成长（2.3K⭐）|
| [claude-code-action](https://github.com/anthropics/claude-code-action) | Anthropic 官方 GitHub Action：让 Claude Code 在 PR / Issue 中自动答疑、审查、实现与定时维护，文档完整、支持多认证方式，适合仓库自动化运营（8.4K⭐）|
| [wei18/Upkeep](https://github.com/wei18/Upkeep) | Claude Code 仓库语义漂移审计插件 / Skill：并行检查文档过期、规格与代码不一致、孤立资产和约定偏移，只输出证据报告，可用插件、`npx skills` 或 CI 安装（7⭐）|
| [openskills](https://github.com/numman-ali/openskills) | 通用 Skills 安装器：把 Claude Code 的 SKILL.md 体系带到 Cursor / Windsurf / Aider / Codex 等多 Agent 环境，支持 GitHub、本地路径、私有仓库安装与 AGENTS.md 同步（10.6K⭐）|
| [AionUi](https://github.com/iOfficeAI/AionUi) | 本地开源 24/7 Cowork / OpenClaw 桌面应用：内置 Agent 与 Office/PPT/Excel/Word skills，支持 Claude Code、Codex、Hermes、OpenClaw 等 20+ CLI 自动检测、WebUI 远程访问和定时任务，适合办公自动化与多代理协作（30.2K⭐）|
| [mcp-use](https://github.com/mcp-use/mcp-use) | 全栈 MCP 框架：同时提供 TypeScript / Python SDK、MCP Inspector、云端部署与 MCP App/Server 构建链路，适合把 Claude / ChatGPT / Claude Code 的工具能力产品化（10.3K⭐）|
| [ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 跨平台 UI/UX 设计智能 Skill：沉淀 161 条推理规则、67 种 UI 风格与多平台设计规范，安装说明完整，适合产品界面、落地页和 App 原型生成（106.5K⭐）|
| [aiskillstore/marketplace](https://github.com/aiskillstore/marketplace) | 安全审计型 Agent Skills 市场：面向 Claude / Codex / Claude Code 提供一键安装与质量校验，README 明确列出 Claude Code 和 Codex 安装方式（387⭐）|
| [bencium/bencium-marketplace](https://github.com/bencium/bencium-marketplace) | 设计、架构与生产力 Claude Code 插件市场：13 个技能，可用 `npx skills` 或 Claude Code `/plugin marketplace` 安装，适合 UI/UX 与产品工程团队（339⭐）|
| [Rito-w/skills-manager](https://github.com/Rito-w/skills-manager) | 跨平台 AI Skills Manager：聚合 Claude Plugins / SkillsLLM / SkillsMP 等市场，支持搜索、下载、本地仓库和一键安装到 Claude / Cursor / Windsurf（192⭐）|
| [osovv/grace-marketplace](https://github.com/osovv/grace-marketplace) | GRACE contract-first 工程技能市场：提供 Graph-RAG Anchored Code Engineering skills 与 CLI，支持 Claude Code / Codex / Kilo Code 的语义契约、知识图谱和自主校验流程（224⭐）|
| [borghei/Claude-Skills](https://github.com/borghei/Claude-Skills) | 266 个跨部门 AI skills 与 67 个 cs-* agents，覆盖工程、营销、合规、C-level 与垂直行业，支持 Claude Code / Codex / Gemini CLI / Cursor 等 11 种助手（379⭐）|
| [NeoLabHQ/context-engineering-kit](https://github.com/NeoLabHQ/context-engineering-kit) | 手工打磨的上下文工程 Skills Kit：聚焦提升 Agent 输出质量，兼容 Claude Code / OpenCode / Cursor / Antigravity / Gemini CLI，文档站与快速开始完整（1.2K⭐）|
| [microsoft/power-platform-skills](https://github.com/microsoft/power-platform-skills) | Microsoft Power Platform 官方插件市场：为 Claude Code / GitHub Copilot 提供可复用 skills、agents、commands，适合企业低代码与办公自动化开发（476⭐）|
| [microsoft/skills](https://github.com/microsoft/skills) | Microsoft 官方 Agent Skills 仓库：175 个 Skills 覆盖 Azure SDK、Foundry、MCP、Custom Agents 与 AGENTS.md 模板，支持 `npx skills add` 选择安装（2.8K⭐）|
| [claudelint](https://github.com/pdugan20/claudelint) | Claude Code 项目 Linter：校验 CLAUDE.md、Skills、Settings、Hooks、MCP 和 Plugin 结构，提供 npm CLI、自动修复与 Claude Code 插件；需 Node.js 20+（9⭐）|
| [finding-unknowns-skills](https://github.com/Neeeophytee/finding-unknowns-skills) | 实现前盲点发现 Skills：8 个技能覆盖未知风险扫描、需求访谈、参考检索、实施计划、变更测验和交付说明，兼容 Claude Code / Codex（218⭐）|
| [codex-hygiene](https://github.com/sunflower-of-parchman/codex-hygiene) | Codex Desktop 上下文与工具面审计 Skill：用只读 SQLite 测量定位 MCP、Plugin、缓存和长任务回放开销，仅建议可逆优化；目前面向 macOS/Unix（240⭐）|
| [hashicorp/agent-skills](https://github.com/hashicorp/agent-skills) | HashiCorp 官方 Agent Skills 与 Claude Code 插件：覆盖 Terraform 代码生成、模块生成、Provider 开发和 Packer 工作流，支持 `npx skills add` 与 `/plugin install`（736⭐）|
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Google Stitch 设计 Skills：提供 `stitch-design`、`stitch-build`、`stitch-utilities` 插件，把前端代码、设计系统和 Stitch MCP 串成可安装设计工作流（7.5K⭐）|
| [vuejs-ai/skills](https://github.com/vuejs-ai/skills) | Vue 3 Agent Skills：沉淀 Vue 最佳实践、Router/Composable 等专项技能，可用 `npx skills add` 或 Claude Code marketplace 安装（2.7K⭐）|
| [michtio/craftcms-claude-skills](https://github.com/michtio/craftcms-claude-skills) | Craft CMS 5 专项 Claude Code 插件：11 个 skills、6 个 agents 和 105 个 reference 文件覆盖插件开发、内容建模、Twig、DDEV、Craft Cloud / Servd 部署，支持 `/plugin marketplace add` 与 `npx skills add`（61⭐）|
| [ory/gemini-cli-extension](https://github.com/ory/gemini-cli-extension) | Ory 官方 Gemini CLI 扩展：把认证、授权、本地 Ory stack、slash commands 与 skills 打包到编码代理工作流，适合需要安全登录体系的应用脚手架（0⭐）|
| [run-llama/llamaparse-agent-skills](https://github.com/run-llama/llamaparse-agent-skills) | LlamaParse 官方 Agent Skills：提供 LlamaParse、LiteParse 和 LlamaCloud Index 检索技能，适合 PDF/Office/扫描件解析与 RAG 索引工作流（71⭐）|
| [LerianStudio/ring](https://github.com/LerianStudio/ring) | Claude Code 插件市场：89 个 skills + 38 个专业 agents，覆盖 TDD、系统化调试、并行代码审查和 10-gate 开发流程（202⭐）|
| [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub) | Binance 官方开放 Skills Hub：为 AI Agent 提供加密资产查询、交易、钱包追踪、信号监控和 DeFi 交互能力，支持 OpenClaw / Claude Code，`npx skills add` 安装路径清晰（932⭐）|
| [am-will/codex-skills](https://github.com/am-will/codex-skills) | Codex / Agent Skills 集合：覆盖规划、多 Agent 编排、Context7/OpenAI 文档访问、前端开发和浏览器自动化，README 列出可用技能与安装/复制路径（995⭐）|
| [thinkyou0714/github-flow-kit](https://github.com/thinkyou0714/github-flow-kit) | GitHub 原生维护 Skills：`pr-respond`、`release-notes`、`issue-triage`、`repo-tour`、PR 权限审计和仓库安全审计 6 件套，带 CI 校验、测试和 `gh skill install` 路径，适合开源维护者处理 PR / Issue / Release（0⭐）|
| [vibeforge1111/keep-codex-fast](https://github.com/vibeforge1111/keep-codex-fast) | Codex 本地状态维护 Skill：先报告、再备份归档会话/日志/旧 worktree，帮助重度 Codex 用户保持启动和恢复速度，强调不直接删除上下文（1.5K⭐）|
| [x0c/session-continue](https://github.com/x0c/session-continue) | Claude Code / Codex CLI 终端会话选择与交接工具：适合多项目、多终端之间恢复上下文和继续任务（1⭐）|
| [yotsuda/PowerShell.MCP](https://github.com/yotsuda/PowerShell.MCP) | 通用 PowerShell MCP Server：让 Claude Code 等 MCP 客户端调用 10,000+ PowerShell 模块和任意 CLI，尤其适合 Windows 自动化场景（84⭐）|
| [GeoLab-org/source-to-skill](https://github.com/GeoLab-org/source-to-skill) | Source-to-Skill 转换工具：分析来源材料并提炼为可复用 agent skills，适合把文档、流程和知识资产沉淀成技能（5⭐）|
| [giuseppe-trisciuoglio/developer-kit](https://github.com/giuseppe-trisciuoglio/developer-kit) | 模块化 Claude Code 插件市场：150+ Skills、45+ Agents，覆盖 Java / TypeScript / Python / PHP / AWS 等工程栈，支持 `/plugin marketplace add`、OpenCode、Codex 和 GitHub Copilot CLI，并提供中文 README（305⭐）|
| [trailofbits/skills-curated](https://github.com/trailofbits/skills-curated) | Trail of Bits 维护的社区验证 Claude Code 插件市场：强调安全审计与质量筛选，适合团队优先选择可信 Skills（461⭐）|
| [gupsammy/Claudest](https://github.com/gupsammy/Claudest) | 面向 Claude Code 的高质量插件市场：收录经过实战筛选的 skills / tools，Python 项目、近期仍活跃，适合发现可安装扩展（258⭐）|
| [23blocks-OS/ai-maestro](https://github.com/23blocks-OS/ai-maestro) | 多 Agent 编排 OS：支持 Claude Code / Codex / Aider / OpenClaw / Hermes 等终端代理，内置持久记忆、Agent-to-Agent 消息、多机器协作，并附 Claude Code 插件、5 个 skills 和 32 个 CLI 脚本（726⭐）|
| [withkynam/vibecode-pro-max-kit](https://github.com/withkynam/vibecode-pro-max-kit) | 规格驱动编码框架，AI 记忆系统（1K⭐）|
| [UditAkhourii/adhd](https://github.com/UditAkhourii/adhd) | 思维树 + 剪枝的 Coding Agent Skill（947⭐）|
| [amElnagdy/guard-skills](https://github.com/amElnagdy/guard-skills) | 代码质量门禁，捕获 AI 生成代码失败模式（1K⭐）|
| [DanMcInerney/architect-loop](https://github.com/DanMcInerney/architect-loop) | 双模型协作：Opus 架构师 + Codex 构建者（615⭐）|
| [proffesor-for-testing/agentic-qe](https://github.com/proffesor-for-testing/agentic-qe) | AI 驱动 QA/QE 平台（415⭐）|
| [cwinvestments/memstack](https://github.com/cwinvestments/memstack) | 127 个技能的结构化框架 + Dashboard（408⭐）|
| [coleam00/helpline](https://github.com/coleam00/helpline) | Claude Code 完整 AI 层示范（106⭐）|
| [sruthik27/creating-claude-md](https://github.com/sruthik27/creating-claude-md) | 自动生成高质量 CLAUDE.md（64⭐）|
| [AppGenesisForge](https://github.com/pcliangx/AppGenesisForge) | Claude Code Agent Teams 应用工程脚手架：19 个角色、7 道阶段门与强制 Skills / Hooks / DoD 串联 Web、微信小程序和 macOS / iOS 交付；安装会写入目标 Git 仓，建议先在分支或备份中试用（742⭐）|

### 🎨 内容创作

| 技能 | 说明 |
|------|------|
| [mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) | Excalidraw MCP 服务器：AI 驱动的图表绘制 + 实时画布同步（2.2K⭐）|
| [gtm-engineer-skills](https://github.com/onvoyage-ai/gtm-engineer-skills) | AI/GEO 优化：16 项基础检查 + 6 维智能分析（1.2K⭐）|
| [openmontage](https://github.com/calesthio/OpenMontage) | 🎬 世界首个开源 agentic 视频制作系统：12 流水线 + 52 工具 + 500+ 技能（39.2K⭐）|
| [axton-obsidian-visual-skills](https://github.com/axtonliu/axton-obsidian-visual-skills) | Obsidian 可视化 Skills 套装：让 Claude Code 一次生成 Canvas / Excalidraw / Mermaid，中文文档完善、安装清晰，适合知识整理与内容表达（3.2K⭐）|
| [nexu-io/open-design](https://github.com/nexu-io/open-design) | 本地优先 Claude Design 开源替代：19 个 Skills + 71 套品牌级设计系统，可生成 Web / 桌面 / 移动端原型、Slides、图片与视频，支持 Claude Code / Codex / Cursor / Gemini 等多 Agent（78.9K⭐）|
| [bevibing/tutor-skills](https://github.com/bevibing/tutor-skills) | 学习型 Claude Code Skill：把 PDF、文档和代码库转成 Obsidian 学习库，适合课程化内容沉淀、知识整理和自学复盘（1K⭐）|
| [AgriciDaniel/claude-blog](https://github.com/AgriciDaniel/claude-blog) | 博客内容生产与优化 Claude Code Skill 生态：覆盖选题、写作、SEO/GEO 优化、内容管理和发布，兼顾 Google 排名与 AI 引用，README 安装与工作流说明清晰（1.4K⭐）|
| [beautify-github-readme](https://github.com/oil-oil/beautify-github-readme) | GitHub README 视觉重构 Skill：先核验项目真实内容，再用项目原生 SVG / 可选 GIF 重排信息架构与证据；支持只读审查、仅生成素材或整页优化，明确未经授权不修改、提交或推送，中文文档和安装路径完整（665⭐）|
| [claude-world/notebooklm-skill](https://github.com/claude-world/notebooklm-skill) | NotebookLM × Claude Code 内容工作流：NotebookLM 负责研究，Claude 负责写作，串联 Research → Synthesis → Content Creation → Publishing，并提供 Skill + MCP Server（355⭐）|
| [limecloud/lime](https://github.com/limecloud/lime) | 本地优先 AI Agent 创作工作台：面向中文创作者把 Workspace、Agent、Skills、MCP、Claw 渠道和 Artifact 交付整合到桌面端，覆盖成稿、成图、成片与项目沉淀（1.5K⭐）|
| [AlemTuzlak/skills](https://github.com/AlemTuzlak/skills) | Claude Code 插件式内容生产 Skills：把 PR、git ref、文件或想法转成营销简报、博客、newsletter、社媒文案、Slidev 演示和视频脚本，支持插件市场与 drop-in 安装（33⭐）|
| [alchaincyf/huashu-md-html](https://github.com/alchaincyf/huashu-md-html) | md/html 双向流水线，反 AI slop（847⭐）|
| [clipify](https://github.com/louisedesadeleer/clipify) | 长视频→社交媒体短视频（459⭐）|
| [illo-skill](https://github.com/tmchow/illo-skill) | 🎨 AI 插画生成 Skill：将文章/想法转为原创印刷风格插画，30+ 角色包（279⭐）|
| [effective-html](https://github.com/plannotator/effective-html) | 📐 优雅简洁的 HTML 规划 Skill：架构图、计划与可视化文档生成（1.4K⭐）|
| [liangdabiao/ecom-details-image](https://github.com/liangdabiao/ecom-details-image) | 跨境电商视觉创作 Skill（652⭐）|
| [feicaiclub/video-spec-builder](https://github.com/feicaiclub/video-spec-builder) | 视频创意→分镜脚本生成（797⭐）|
| [Hao0321/claude-skill-social-post](https://github.com/Hao0321/claude-skill-social-post) | 学习文风自动发帖 + 内容日历（552⭐）|
| [realrossmanngroup/no_ai_slop_writing_rules](https://github.com/realrossmanngroup/no_ai_slop_writing_rules) | 反 AI 味写作规则（587⭐）|
| [haidang1810/md2html](https://github.com/haidang1810/md2html) | md→精美 HTML 页面（398⭐）|
| [worldwonderer/video-recap-skills](https://github.com/worldwonderer/video-recap-skills) | 视频→中文解说视频（392⭐）|
| [aref-vc/tufte-claude-skill](https://github.com/aref-vc/tufte-claude-skill) | Tufte 风格数据图表生成（278⭐）|
| [Jaderson-bit/mindmap-markmap-viewer](https://github.com/Jaderson-bit/mindmap-markmap-viewer) | Markdown→交互式思维导图（65⭐）|
| [micheledalsanto/design-from-references](https://github.com/micheledalsanto/design-from-references) | Claude Code 视觉设计参考技能：从优秀站点量测字体、颜色、间距并生成原创可访问的 Figma 设计系统（0⭐）|
| [anything-to-course](https://github.com/lowwwbank/anything-to-course) | 学习科学驱动的 Agent Skill：把文档、笔记、转录、幻灯片或代码库转成自学课程，内置检索练习、间隔复习、交错练习和独立答案文件，支持 Claude Code / Claude.ai / Codex 安装（2⭐）|
| [novel-to-webnovel](https://github.com/aimerfeng/novel-to-webnovel) | 中文小说网文化改写 Claude Code Skill：五阶段流水线把日轻译稿、机翻稿或自写草稿去翻译腔并转成中文网文口感，含 Perl 分章、格式清理和 QA 脚本，明确版权与未成年露骨内容边界（0⭐）|
| [guizang-material-illustration](https://github.com/op7418/guizang-material-illustration) | 歸藏材质插画 Skill：把文章、截图或数据转成带中文标签的机制图、解释图和材质化图表，内置参考调研、提示词模板与图像 QA；仓库暂未声明许可证（697⭐）|

### 🔬 学术科研

| 技能 | 说明 |
|------|------|
| [zLanqing/codex-claude-academic-skills](https://github.com/zLanqing/codex-claude-academic-skills) | 学术科研全流程 Skills（2K⭐）|
| [Haojae/scipilot-figure-skill](https://github.com/Haojae/scipilot-figure-skill) | 出版级科学图表绘制（1.2K⭐）|
| [xiaofenggan01/aigc-reduce](https://github.com/xiaofenggan01/aigc-reduce) | 降低学术论文 AIGC 查重率（456⭐）|
| [u7079256/paperjury](https://github.com/u7079256/paperjury) | 论文投稿前 AI 压力测试（691⭐）|
| [Awesome-Vibe-Research](https://github.com/modelscope/Awesome-Vibe-Research) | 🔬 魔搭社区开源 AI 辅助科研全流程仓库：收集 agents、skills、workflows 与最佳实践（357⭐）|
| [Awesome-Journal-Skills](https://github.com/brycewang-stanford/Awesome-Journal-Skills) | 面向 Claude Code / Codex 的期刊投稿 Skills 包：覆盖 AER、QJE、Nature、Cell、管理世界、经济研究等 200+ 期刊，支持选题、识别策略、表格规范和审稿回复（815⭐）|
| [humanities-writing-companion](https://github.com/tizzy916/humanities-writing-companion) | 人文学科写作伙伴：中英双语 SKILL.md 覆盖研究问题、文献图谱、写作、对抗审阅、修订和 AI 使用披露，强调保留作者声音；采用 CC BY-NC 4.0（54⭐）|
| [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | 人机协作学术研究 Skills 套件：4 个核心 Skill 串联深度研究、论文写作、审稿与修订，带引用核验和完整性门禁，支持 Claude Code 插件安装；采用 CC BY-NC 4.0，最终论证与学术诚信仍由研究者负责（38.1K⭐）|
| [tex-manual-translation](https://github.com/Explorer-cc/tex-manual-translation) | 中文 LaTeX 手册翻译 Agent Skill：通过术语表、CJK 编译门禁和 3 个检查脚本处理环境失衡、中文标点反斜杠与漏译问题，支持 npm 安装到 Claude Code / Codex；安装器需 Node.js 18+，编译验证需 TeX Live 或 MiKTeX（0⭐）|

### 🤖 AI Agent

| 技能 | 说明 |
|------|------|
| [wshobson/agents](https://github.com/wshobson/agents) | 🧠 智能自动化 & 多 Agent 编排，Claude Code 核心工作流（38K⭐）|
| [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) | 🏢 Teams-first 多 Agent 编排，团队协作场景（37.8K⭐）|
| [refly](https://github.com/refly-ai/refly) | 🔧 首个开源 Agent Skills 构建器，vibe workflow 定义技能（7.4K⭐）|
| [raptor](https://github.com/gadievron/raptor) | ⚔️ 攻防安全 Agent：SAST/DAST 扫描 + OWASP + CVE 检测（3.3K⭐）|
| [godogen](https://github.com/htdt/godogen) | 🎮 从游戏描述构建完整 Godot 4 项目（4.8K⭐）|
| [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | 📚 100+ 子代理合集，覆盖各类开发场景（23.4K⭐）|
| [chengfeng-videocut-skills](https://github.com/Agentchengfeng/chengfeng-videocut-skills) | 🎬 Claude Code Skills 驱动的视频剪辑 Agent（2.7K⭐）|
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) | ⚔️ 自主 ML 研究：跨模型审查 + 想法发现 + 实验自动化（13.5K⭐）|
| [browser-use](https://github.com/browser-use/browser-use) | 🌐 AI 浏览器自动化基础设施：提供开源库 + Cloud stealth 浏览器 + 文档化 LLM 接入方式，适合为 Claude Code / Cursor / 自定义 agent 增强网页操作能力（105.1K⭐）|
| [iflytek/skillhub](https://github.com/iflytek/skillhub) | 企业级自托管 Agent Skill Registry：支持技能发布、版本管理、RBAC 权限、审计日志，以及 Docker / Kubernetes 私有化部署，适合团队内部沉淀与分发 Skills（4K⭐）|
| [tech-leads-club/agent-skills](https://github.com/tech-leads-club/agent-skills) | 安全优先的专业 Agent Skills Registry：提供校验过的技能目录、CLI 安装/更新/移除、多 Agent 兼容与 Snyk 扫描，适合团队级技能治理与分发（4.9K⭐）|
| [openclaw/clawhub](https://github.com/openclaw/clawhub) | OpenClaw 官方技能注册中心：支持 Skill/Plugin/SOUL.md 发布、版本管理、向量搜索、CLI 安装与 OpenClaw 包目录，适合发现、分发和治理 agent skills（9.2K⭐）|
| [browserbase/skills](https://github.com/browserbase/skills) | Browserbase 官方浏览器自动化 Skills：覆盖远程浏览器、Browserbase CLI、trace、browser-to-api、UI 测试、竞品研究和公司调研，并支持 Claude Code 插件安装（3.6K⭐）|
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | Snyk Agent Scan：自动发现并扫描 Claude Code / Codex / Gemini CLI 等环境中的 MCP Server、skills 和 agent 组件，识别 prompt injection、敏感数据和恶意载荷风险（2.8K⭐）|
| [anthropics/launch-your-agent](https://github.com/anthropics/launch-your-agent) | 🚀 Anthropic 官方 Claude Managed Agent 发布技能：从想法到上线的完整工作流，含访谈、规划、部署与迭代（807⭐）|
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | 产品经理 Skills Marketplace：65+ PM Skills 与 36 个链式工作流，覆盖用户发现、战略、执行、发布和增长，适合产品/运营团队把方法论固化为可复用 Agent 技能（23.9K⭐）|
| [davepoon/buildwithclaude](https://github.com/davepoon/buildwithclaude) | Claude 生态发现平台：聚合 Skills、Agents、Commands、Hooks、Plugins 与 Marketplace 集合，支持 `/plugin marketplace add` 快速接入，适合发现可安装 Claude Code / OpenClaw 扩展（3.2K⭐）|
| [numman-ali/n-skills](https://github.com/numman-ali/n-skills) | 跨 Agent 技能市场：以 “write once, run everywhere” 方式兼容 Claude Code、Codex、Cursor、OpenCode 和 openskills，适合团队统一沉淀与分发技能（1K⭐）|
| [garrytan/gbrain](https://github.com/garrytan/gbrain) | Garry Tan 的 OpenClaw / Hermes Agent Brain：把个人工作方法、记忆与 Agent 配置沉淀为可复用大脑，适合个人 AI 助手长期演化（26.4K⭐）|
| [screenpipe](https://github.com/screenpipe/screenpipe) | 24/7 本地屏幕与麦克风上下文记录基础设施：让 Agent 基于真实工作流自动触发与复盘，适合个人知识捕获和运营分析（20.2K⭐）|
| [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | Obsidian 第二大脑 Claude Code Skill：31 个命令覆盖 vault-first research、定时 Agent 与长期知识维护，让知识库成为可持续演化的 Agent 工作台（3.3K⭐）|
| [Karanjot786/agent-skills-cli](https://github.com/Karanjot786/agent-skills-cli) | 通用 Agent Skills CLI：从 SkillsMP 同步 40,000+ 技能到 Cursor、Claude Code、GitHub Copilot、OpenAI Codex 与 Antigravity，适合多工具技能市场接入（173⭐）|
| [Leon-Drq/openagentskill](https://github.com/Leon-Drq/openagentskill) | 开放 Agent Skills 市场：提供技能发现、提交、API 文档和基于真实 Agent 使用反馈的排行，适合寻找可复用 MCP / Web 自动化 / 生产力技能（203⭐）|
| [learn-skills.dev](https://github.com/NeverSight/learn-skills.dev) | AI Agent Skills 搜索与安装站：聚合 skills.sh 榜单和手动技能索引，支持搜索、复制与安装 Claude Code / Cursor / OpenClaw 等工具可用技能，并提供中文 README（185⭐）|
| [agent-install](https://github.com/millionco/agent-install) | 跨 Agent 安装库与 CLI：用统一 API 安装 `SKILL.md`、MCP Server 和 AGENTS.md 片段到 Claude Code / Cursor / Codex / OpenCode 等 40+ 工具（51⭐）|
| [Meta_Kim](https://github.com/KimYx0207/Meta_Kim) | 面向 Claude Code / Codex / OpenClaw / Cursor 的 AI 编码治理层：用 agents、skills、contracts、hooks 和验证证据把复杂任务路由、审查和沉淀成可复用执行链（253⭐）|
| [multi-turn-inc/enacta-plugins](https://github.com/multi-turn-inc/enacta-plugins) | Enacta 官方 Claude Code 插件：为 coding agents 提供长期记忆能力，适合需要跨会话沉淀项目知识的工作流（0⭐）|
| [ManuelStaggl/keepmind](https://github.com/ManuelStaggl/keepmind) | 面向 Claude Code / Codex / Cursor 的跨会话记忆工具：Node-only、跨平台，自动压缩观察并注入未来会话（0⭐）|
| [devakchow/parrot](https://github.com/devakchow/parrot) | Claude Code 插件：builder/checker 双代理循环，内置最大轮次、回归中止和防篡改停止规则，适合受控自动实现流程（0⭐）|
| [hamelsmu/claude-review-loop](https://github.com/hamelsmu/claude-review-loop) | Claude Code × Codex 代码审查闭环插件：Claude 实现后触发 Codex 多代理审查，再把合并后的 findings 写回 `reviews/` 供修复（704⭐）|
| [blader/napkin](https://github.com/blader/napkin) | Claude Code / Codex 持久错误记忆 Skill：在仓库内维护 `.claude/napkin.md`，记录纠错、偏好和复盘，帮助后续会话避免重复犯错（570⭐）|
| [berabuddies/Semia](https://github.com/berabuddies/Semia) | AI Agent Skills 安全审计工具（555⭐）|
| [tuchg/Lucarne](https://github.com/tuchg/Lucarne) | 远程通知/审批/恢复 Codex/Claude Code 会话（311⭐）|
| [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) | ADHD 友好输出（367⭐）|
| [Lynnouo/yushio](https://github.com/Lynnouo/yushio) | AI 协作者人设 Skill（217⭐）|
| [swaylq/master-skill](https://github.com/swaylq/master-skill) | 输入行业自动调研→Master OS skill（106⭐）|
| [ccteam](https://github.com/firstintent/ccteam) | 自托管 Claude Code / Codex 多 Agent 团队控制台：通过 Telegram、飞书或 Web 远程派单、收集结果并限制层级、并发和预算；默认监听 `0.0.0.0:7331` 且无 TLS，仅建议用于可信局域网或改为绑定本机（7⭐）|

### 💰 金融/商业

| 技能 | 说明 |
|------|------|
| [dbskill](https://github.com/dontbesilent2025/dbskill) | 🏢 商业诊断技能包：市场分析、竞品调研、商业模式画布（8.3K⭐） |
| [gtm-eng-skills](https://github.com/getaero-io/gtm-eng-skills) | GTM Engineering Claude Code Skills：覆盖 TAM 构建、联系人/LinkedIn 查找、线索富集、投放受众和 outbound 工作流，内置成本门禁与 `npx skills add` 安装路径（43⭐）|
| [financial-report-minesweeper](https://github.com/terancejiang/financial-report-minesweeper) | A 股财报排雷工具，28 条唐朝方法论检查（162⭐） |
| [tech-digest](https://github.com/camilleroux/tech-digest) | HN/Lobste.rs 每日科技摘要，评分过滤（34⭐） |
| [MobiusQuant/OpenMobius-skill](https://github.com/MobiusQuant/OpenMobius-skill) | ICT/SMC 交易知识 Skill（421⭐）|
| [ViryaZheng/recomby-geo](https://github.com/ViryaZheng/recomby-geo) | GEO 生成式引擎优化（504⭐）|
| [duolahypercho/fusion-fable](https://github.com/duolahypercho/fusion-fable) | 双模型融合（453⭐）|
| [ybuild-ai/ai-game-art-pipeline-skill](https://github.com/ybuild-ai/ai-game-art-pipeline-skill) | AI 图片→可玩游戏美术资产（309⭐）|
| [Utopai-Research/pai-pro](https://github.com/Utopai-Research/pai-pro) | 本地 AI 电影制作工作室（319⭐）|
| [gauss314/skills](https://github.com/gauss314/skills) | 📊 金融市场数据消费 Skills：面向 Claude Code 与 AI Agent 的金融数据接入能力（163⭐）|
| [luopan](https://github.com/zhangxiaoqiang1991/luopan) | 中文行业与公司研究路由 Skill：通过信源分级和对抗验证分析产业链权力、利润分布与公司质量，适合投资或求职研究，不替代投资建议（260⭐）|
| [qlik-oss/agentic-skills](https://github.com/qlik-oss/agentic-skills) | Qlik 官方 Agentic Skills Hub：提供 Qlik Cloud AI readiness / MCP 优化 Skill、官方与社区插件分层、`npx skills add` 与 Claude Code plugin 安装路径（3⭐）|
| [niubiskill](https://github.com/nathanskill/niubiskill) | 中文变现决策 Skill：打断无收入验证的瞎忙，找到离真实收钱最近的一步，二选一（引流 / 成交），停掉一件分散精力的事并给出 7 天证据测试，支持 `npx skills add nathanskill/niubiskill` 安装；不承诺收益，涉及受监管活动时需先核验权限（93⭐）|

---

### 🌏 中文专属

| 技能 | 说明 |
|------|------|
| [Humanizer-zh](https://github.com/op7418/Humanizer-zh) | 消除中文 AI 写作痕迹（13.3K⭐）|
| [shuorenhua](https://github.com/MrGeDiao/shuorenhua) | 中文优先的去 AI 味改写 Skill：按发布场景分档，先锁定事实再处理语气，支持 Claude Code / Codex / Cursor / OpenClaw；代码、日志、配置和命令输出不应套用该 Skill（736⭐）|
| [financial-report-minesweeper](https://github.com/terancejiang/financial-report-minesweeper) | A 股财报排雷（唐朝方法论）（162⭐）|
| [web-access](https://github.com/eze-is/web-access) | 给 Claude Code 装上完整联网能力：三层通道调度 + 浏览器 CDP（8.3K⭐）|
| [awesome-agent-skills](https://github.com/JackyST0/awesome-agent-skills) | 🇨🇳 精选 AI Agent Skills 列表，适配 Cursor / Claude Code / GitHub Copilot（592⭐）|
| [wx-favorites-report](https://github.com/zhuyansen/wx-favorites-report) | 微信收藏可视化 Skill：从加密 DB 到交互式 HTML 报告的端到端管线（625⭐）|
| [awesome-openclaw-skills-zh](https://github.com/Rito-w/awesome-openclaw-skills-zh) | OpenClaw Skills 中文翻译与分类目录：整理 5,494 个社区技能、30 个中文分类和安装说明，并明确提示安装前进行安全审查（66⭐）|
| [luban-skill](https://github.com/LearnPrompt/luban-skill) | 🔧 鲁班 Agent Skill 打磨工作坊：把能用的 Skill 打磨成能被装、能传播、能验证、能进化的公共资产（882⭐）|
| [compass-skills](https://github.com/dongshuyan/compass-skills) | 🧭 司南：个性化 AI 任务总控 Skills 系统，面向中文用户的 Agent 任务编排（630⭐）|
| [chubbyguan/chubbyskills](https://github.com/chubbyguan/chubbyskills) | 中文全渠道内容采集（抖音/B站/小红书/公众号）（551⭐）|
| [dzcmemory-web/bazi-ziwei-skill](https://github.com/dzcmemory-web/bazi-ziwei-skill) | 八字+紫微斗数排盘（654⭐）|
| [lan1177/interview-prep](https://github.com/lan1177/interview-prep) | 产品/运营岗位面试准备文档生成器（76⭐）|
| [ziwei-doushu](https://github.com/Linden-TR/ziwei-doushu-skill) | 🔮 紫微斗数命盘排盘与解读：中州派为宗，融合三合/飞星/钦天/河洛四大学派，支持十二宫分析、四化追踪、大限流年、45种格局识别，基于 MCP 的专业命理 Claude Code Skill（2⭐） |
| [offer-helper](https://github.com/dominciyue/resume_skill) | 💼 中文求职助手：摄入简历/GitHub 仓库/文档建可持久化经历库，按 JD 生成 STAR 量化简历（严格防虚构），并做大厂式由浅及深的深挖面试（0⭐） |
| [Bloom](https://github.com/Li-Evan/Bloom) | 🌸 基于 Bloom 2-Sigma 研究的中文苏格拉底式 AI 家教：自适应学习路径、反问引导、中文优先（200⭐）|
| [yzfly/awesome-skills-zh](https://github.com/yzfly/awesome-skills-zh) | 中文 Skills 精选资源：收录 Claude Skills、LLM Skills、AI Skills，适合中文用户发现可迁移技能素材（22⭐）|
| [zhuwujing28-del/codex-skills-cn](https://github.com/zhuwujing28-del/codex-skills-cn) | 面向中文用户的 Codex skills 收藏、适配和维护仓库，适合寻找 Codex 侧技能迁移参考（1⭐）|
| [speak-human-tw](https://github.com/Raymondhou0917/speak-human-tw) | 繁体中文去 AI 味编辑 Skill：检查 38 类 AI 写作痕迹，校正台湾用语与标点，并通过“先列修改清单、确认后再动稿”保护事实和作者语气（543⭐）|
| [miniprogram-skills](https://github.com/Sun-sunshine06/miniprogram-skills) | 微信小程序开发 Codex / Claude Code Skills：6 个可复用技能覆盖 DevTools 诊断、官方脚手架校验、GUI 冒烟、架构重组和 UI 文案精简，中英文文档与验证脚本完整（19⭐）|
| [skillforge](https://github.com/t115601251-hue/skillforge) | 中文优先的跨 Agent 技能闭环管理 CLI：用自然语言查找、安装、修改和创建 Claude Code / Codex / OpenClaw skills，零第三方运行时依赖，带 R/U/T 三维评分、OpenSSF Scorecard / OSV 安全审和 117 个单测（2⭐）|
| [kc_ai_skills](https://github.com/KerberosClaw/kc_ai_skills) | 中文优先的 22 个通用 Agent Skills：覆盖仓库预检、ADR / PRD、故障诊断、报告和内容生成，兼容 Claude Code / Codex；其中 CTF / 逆向仅限授权环境，外部服务技能部署前需审查认证与网络配置（75⭐）|
| [hermes-edu-skills](https://github.com/hezkvectory/hermes-edu-skills) | 面向中国教育场景的 170 个 Agent Skills：覆盖教材同步、备考、拍照答疑、错题复盘、亲子陪学和教师工具，Hermes 可直接安装并可导出到 Claude Code / Codex / Cursor；处理学生资料时需保护隐私，输出仍应由教师或家长核验（43⭐）|
| [taiwan-translate-skill](https://github.com/Moksa1123/taiwan-translate-skill) | 台湾正体中文本地化 Skill：内置 2,300+ WordPress 官方词汇，支持 PO / POT 与双来源术语策略，可通过 npm 安装到 14 类 AI 工具；法律、医疗等专业文本仍需人工校对（7⭐）|

---

<a id="original-skills"></a>

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
| [git-workflow](skills/git-workflow/) | 开发效率 | 先审查改动，再按授权提交、建分支、推送或创建 PR |
| [security-audit](skills/security-audit/) | 安全 | 代码安全审计：漏洞扫描 + 修复建议 |
| [api-tester](skills/api-tester/) | 测试 | 依据真实 OpenAPI / 路由契约，在确认测试环境与授权后生成并验证 API 测试 |
| [changelog-gen](skills/changelog-gen/) | 文档 | 从 Git 历史自动生成 CHANGELOG |
| [refactor-advisor](skills/refactor-advisor/) | 代码质量 | 代码重构建议：识别坏味道 + 重构方案 |
| [zh-readme](skills/zh-readme/) | 文档 | 先分析项目，再生成面向中文开发者的高质量 README |
| [perf-profiler](skills/perf-profiler/) | 性能 | 基于可复现基线和 profiler 证据定位瓶颈并同条件复测 |
| [db-migrator](skills/db-migrator/) | 数据库 | 数据库迁移助手：Schema diff + 迁移脚本 |
| [i18n-helper](skills/i18n-helper/) | 开发效率 | 国际化/本地化：扫描硬编码文本 + i18n 配置生成 |
| [log-analyzer](skills/log-analyzer/) | 调试 | 日志分析：异常模式检测 + 根因定位 + 分析报告 |
| [error-translator](skills/error-translator/) | 调试 | 编程错误翻译：英文报错 → 中文解释 + 修复方案 |
| [eslint-fix](skills/eslint-fix/) | 开发效率 | 使用项目锁定工具预检、限范围修复并复验 ESLint 问题 |
| [dep-auditor](skills/dep-auditor/) | 安全 | 依赖安全审计：CVE 漏洞检测 + 过期检查 + 许可证风险 |
| [test-generator](skills/test-generator/) | 测试 | 依据真实代码契约生成并运行单元测试或集成测试 |
| [github-actions-gen](skills/github-actions-gen/) | CI/CD | GitHub Actions 流水线生成器：根据技术栈自动创建 workflows |
| [env-manager](skills/env-manager/) | 开发效率 | 环境变量管理：扫描 .env 文件 + 校验 + 安全检查 + 生成模板 |
| [ds-mapper](skills/ds-mapper/) | 理解代码库 | 项目结构地图：生成带注释的可视化目录树，快速理解任意仓库 |
| [skill-curator](skills/skill-curator/) | 资源维护 | 核验 GitHub 候选 Skill，输出中文分类、描述、评分与风险证据 |

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

- [Claude Code 官方文档](https://code.claude.com/docs)
- [awesome-chatgpt-prompts-zh](https://github.com/PlexPt/awesome-chatgpt-prompts-zh) — 60.9K ⭐
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) — 67.6K ⭐
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) — 49.9K ⭐
- [awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) — 23.3K ⭐
- [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) — 28K ⭐
- [awesome-claude-skills-vn](https://github.com/travisvn/awesome-claude-skills) — 14.1K ⭐
- [awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) — 51.2K ⭐
- [everything-claude-code](https://github.com/affaan-m/ECC) — 229.2K ⭐
- [agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) — 43.1K ⭐
- [awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) — 2.3K ⭐
- [playwright-skill](https://github.com/lackeyjb/playwright-skill) — 2.9K ⭐
- [awesome-llm-skills](https://github.com/Prat011/awesome-llm-skills) — 1.4K ⭐
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) — 878 ⭐
- [cc-marketplace](https://github.com/ananddtyagi/cc-marketplace) — 684 ⭐
- [Agent Skills Specification](https://github.com/agentskills/agentskills) — 23K ⭐
- [claude-mem](https://github.com/thedotmack/claude-mem) — 87.1K ⭐
- [Vexilo · Claude Code 工具书](https://vexilo.app/?lang=en) — 31 agents / 99 commands / 123 skills / 13 rules 的可视化工具书，按 5 步工作流组织，一键喂给 Claude。([companion repo](https://github.com/lilhawk7077/claude-code-resources))
- [claude-hud](https://github.com/jarrodwatts/claude-hud) — 26.4K ⭐
- [agency-agents](https://github.com/msitarzewski/agency-agents) — 131.1K ⭐
- [github/spec-kit](https://github.com/github/spec-kit) — 120.5K ⭐
- [bytedance/deer-flow](https://github.com/bytedance/deer-flow) — 76.9K ⭐

---

## 📈 Star History

[在 Star History 查看项目增长趋势](https://www.star-history.com/#laolaoshiren/claude-code-skills-zh&Date)

---

## 🤝 贡献

欢迎提交 PR！请将你的 skill 放入 `skills/` 目录并更新上方列表。

📢 [征集优质 Skills！提交即上榜 →](https://github.com/laolaoshiren/claude-code-skills-zh/issues/1)

维护和收录标准见：[项目维护手册](docs/MAINTENANCE.md)。

---

## ⭐ 如果这个项目帮到了你

请给个 Star ⭐ 这是对我最大的鼓励！

---

## 📝 License

MIT
