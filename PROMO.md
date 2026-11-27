# 📢 推广文案（复制粘贴即用）

> 精选数量与原创数量由 `scripts/sync_readme_to_site.py` 自动同步，请勿手动修改数字。
> 内容改动可随时编辑，但发布前建议先跑一次同步脚本，确保口径与 README 一致。

## 1️⃣ V2EX 发帖

**标题：** [分享] Claude Code Skills 中文精选集 — 453+ 精选技能 + 22 个原创可安装技能

**正文：**
做了个 Claude Code Skills 的中文资源站，不只是 awesome 列表，还包含可直接安装的原创中文技能：
- 英文 Skill 汉化与安全/Windows 预检器（`skill-translator`）
- 八阶段中文 AI 视频流水线（`ai-video-producer`）
- 中文代码审查专家（`zh-code-reviewer`，基于 git diff 分级报告）
- 中文 README / 技术文档生成器（`zh-readme` / `zh-docgen`）
- 安全审计与依赖体检（`security-audit` / `dep-auditor`）
- API 测试生成器与重构顾问（`api-tester` / `refactor-advisor`）
- Skill 收录核验器（`skill-curator`）
...

还整理了 453+ 第三方精选资源，按场景分类，并提供项目入口、Windows/macOS/Linux 安装指引和跨工具路径速查，已同步到可搜索官网。

链接：https://github.com/laolaoshiren/claude-code-skills-zh
官网：https://claude-skills.bt199.com

欢迎 star + 提交你发现的好技能 🙏

---

## 2️⃣ 掘金发文

**标题：** Claude Code Skills 入门指南：22 个面向中文开发者的实用 AI 技能

**正文：**
最近 Claude Code Skills 生态爆发式增长，但中文资料很少，直接装英文高星 Skill 又经常遇到触发不稳、输出全英文或 Windows 终端命令报错的问题。我整理了一份中文精选集，还写了 22 个实用的原创技能：

🔥 最值得先装的几个：
1. `skill-translator` — 把任意英文 `SKILL.md` / `AGENTS.md` 无损转为中文触发版，顺带做安全与 Windows 兼容性预检
2. `ai-video-producer` — 八阶段 AI 视频流水线，内置中文口播语速、字幕断句与防抽卡成本门禁
3. `zh-code-reviewer` — 基于 `git diff` 输出「阻塞缺陷 / 重要改进 / 可选建议」中文只读审查报告
4. `security-audit` / `api-tester` — 安全隐患排查与按真实契约生成并验证 API 测试
5. `refactor-advisor` / `perf-profiler` — 识别代码坏味道、用可复现基线定位性能瓶颈

GitHub 地址：https://github.com/laolaoshiren/claude-code-skills-zh
在线搜索官网：https://claude-skills.bt199.com

一键安装（Claude Code 2.1+，推荐）：
/plugin marketplace add laolaoshiren/claude-code-skills-zh
/plugin install zh-skills@claude-code-skills-zh

按需单装某个技能：
npx skills add laolaoshiren/claude-code-skills-zh --skill skill-translator

或者手动复制（macOS / Linux）：
git clone https://github.com/laolaoshiren/claude-code-skills-zh.git && mkdir -p ~/.claude/skills && cp -r claude-code-skills-zh/skills/* ~/.claude/skills/

Windows PowerShell 5.1+：
git clone https://github.com/laolaoshiren/claude-code-skills-zh.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force ".\claude-code-skills-zh\skills\*" "$HOME\.claude\skills\"

---

## 3️⃣ Twitter/X 推文

🛠️ 做了个 Claude Code Skills 中文精选集！

✅ 453+ 精选资源列表
✅ 22 个原创可安装技能
✅ 按场景分类，中文说明，官网支持实时搜索

英文 Skill 汉化体检（skill-translator）| AI 视频流水线（ai-video-producer）| 中文代码审查 | API 测试 | 性能分析...

🔗 github.com/laolaoshiren/claude-code-skills-zh
🌐 claude-skills.bt199.com

#ClaudeCode #AI #编程 #开源

---

## 4️⃣ 知乎回答（相关问题下）

推荐一个面向中文开发者的开源项目：Claude Code Skills 中文精选集

github.com/laolaoshiren/claude-code-skills-zh

不只列出了 453+ 优质资源，还带了 22 个原创技能可以直接装：
- `skill-translator`：把海外高星英文 Skill 无损转为中文触发 + 安全/Windows 体检版
- `ai-video-producer`：面向中文口播与抖音/B 站/小红书的八阶段 AI 视频流水线
- `zh-code-reviewer`、`api-tester`、`zh-readme`、`perf-profiler` 等日常高频研发技能

除了插件一键安装，也给了 Windows PowerShell 命令和 Codex / Cursor / Gemini CLI 路径速查表，上手门槛低。

---

## 5️⃣ 微信群/技术群

分享个资源，做了个 Claude Code Skills 的中文精选集 📋

不只列了 453+ 好用的资源，还带了 22 个原创技能可以直接装：
英文 Skill 汉化体检（skill-translator）、AI 视频流水线（ai-video-producer）、中文代码审查、API 测试、Git 自动化...

一键安装 👇
/plugin marketplace add laolaoshiren/claude-code-skills-zh
/plugin install zh-skills@claude-code-skills-zh

地址：github.com/laolaoshiren/claude-code-skills-zh
官网搜技能：claude-skills.bt199.com

觉得顺手帮忙点个 star 🙏

---

## 6️⃣ 实测前后对比型干货帖（掘金 / V2EX / 知乎长文模板）

**标题：** 把十万星英文 Claude Code Skill 搬进中文项目：我踩过的 3 个坑与无损本地化实测

**正文骨架（发帖前填入当次真实仓库测试截图）：**

1. **痛点切入（实话实说，不喊口号）**：
   直接装海外高星英文 `SKILL.md` 时，中文开发者常遇到 3 个问题：
   - 用中文提问时，纯英文 `description` 触发不稳定，或者触发后全程输出英文报告；
   - 让 AI 直接“翻译成中文”，容易把 YAML frontmatter 键名、CLI 参数和代码路径翻坏；
   - 很多英文 Skill 默认跑在 macOS/Linux 上，里面藏着 `find`、`sed -i` 或未审核的外部脚本，Windows 终端一跑就报错。

2. **实测对比 1：用 `skill-translator` 处理一个真实高星英文 Skill**：
   - **处理前**：纯英文触发词、隐含 macOS 专属 Shell 命令、中文项目里需要反复补一句“请用中文回答”。
   - **处理后**：
     - 先出一份「安全与 Windows 兼容性预检表」，一眼看清有没有读 `.env`、裸 `npx` 或 Bash 专属命令；
     - 保留原 `name`、YAML 键名、命令行参数与代码块 100% 不动，仅将 `description` 重构为中英双语触发词，正文去掉翻译腔并保留原作者署名与 LICENSE；
     - 1:1 核对标题、代码块与门禁条件，经确认后再落盘，不盲目覆写原文件。

3. **实测对比 2：用 `zh-code-reviewer` 跑一次真实的 `git diff` 审查**：
   - **处理前**：口头让 AI“帮我 review 一下代码”，常给一堆泛泛的风格意见，还动不动打个不知标准的 `8/10`。
   - **处理后**：只读分析当前 `git diff`，按「阻塞缺陷 / 重要改进 / 可选建议」输出带 `文件:行号`、触发路径与最小修复代码的中文报告，并补查测试覆盖缺口。

4. **怎么直接用（不绑定全量安装）**：
   - 装全部原创技能（Claude Code 2.1+）：`/plugin marketplace add laolaoshiren/claude-code-skills-zh` + `/plugin install zh-skills@claude-code-skills-zh`
   - 只装单个体验：`npx skills add laolaoshiren/claude-code-skills-zh --skill skill-translator`
   - 完整分类目录（含公众号/小红书/飞书/企微等国内平台与学术科研）：https://github.com/laolaoshiren/claude-code-skills-zh
   - 官网按关键词跨分类检索：https://claude-skills.bt199.com
