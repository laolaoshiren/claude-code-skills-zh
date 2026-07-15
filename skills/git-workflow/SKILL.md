---
name: git-workflow
description: 安全处理 Git 状态检查、提交信息、commit、分支、push、PR 和 rebase。用于用户要求检查改动、生成或创建提交、管理分支、推送、发起 PR 或整理历史时；严格区分每个动作的授权，并保护工作树中已有和无关的修改。
---

# Git 工作流助手

## 核心原则

- 只执行用户明确要求的 Git 动作。生成提交信息不等于暂存或提交；提交不等于推送；创建 PR 不等于合并 PR、关闭 Issue 或发布 Release。
- 把工作树中已有、未跟踪和无关的修改视为用户资产，不覆盖、不回退、不混入本轮提交。
- 优先使用非交互命令。涉及历史重写、冲突选择或远程覆盖时降低自动化程度。

## 工作流程

### 1. 读取仓库规则与状态

先阅读适用的 `AGENTS.md`、`CONTRIBUTING.md`、README、提交规范和 CI 说明，再检查：

```bash
git status --short --branch
git diff
git diff --cached
git log --oneline -10
git remote -v
git branch -vv
```

同时识别未跟踪文件、当前分支、upstream、远程差异和已有失败。不得只看 staged diff。

### 2. 明确动作与文件范围

把用户请求拆成独立授权：

| 动作 | 默认权限 |
|------|----------|
| 分析状态、生成 commit message 或 PR 文案 | 只读 |
| 暂存、commit | 仅用户要求后执行，只选本轮相关文件 |
| 创建或切换分支 | 仅用户明确要求时执行；实现流程需要但未获授权时，先说明原因并取得同意 |
| fetch、push、创建 PR | 分别确认在请求范围内，不互相推导 |
| merge、关闭 Issue、发布 Release | 必须有明确授权 |
| rebase、修改已发布历史、强制更新远程 | 高风险，必须明确授权并满足额外条件 |

存在无关改动时不得使用 `git add .` 或 `git add -A`。逐个暂存目标文件，并用 `git diff --cached` 复核。

### 3. 规划原子提交

- 根据真实 diff 判断 `feat`、`fix`、`docs`、`refactor`、`test`、`perf` 或 `chore`。
- 沿用仓库近期提交的语言、scope 和格式。
- 一个提交只表达一项可独立理解和验证的改动。
- `Closes #123` 仅在对应 Issue 确实应由该提交自动关闭时使用。

提交信息遵循：

```text
<type>(<scope>): <简短描述>

<必要时说明原因、关键实现和兼容性>

<关联 Issue 或 Breaking Change>
```

### 4. 验证后执行

提交前先检查验证脚本是否会下载依赖、访问外部服务或产生其他状态，再运行与改动相关的测试、lint、构建或文档检查，并记录实际命令和退出状态。可能产生外部副作用时先取得授权。基线已有失败时单独说明，不能把未运行的项目标为通过。

执行 commit 后检查：

```bash
git status --short --branch
git show --stat --oneline HEAD
```

推送前先 `git fetch`，确认 upstream 没有未整合的新提交；禁止 force push。

### 5. 创建 PR

PR 文案应帮助 reviewer 结合 diff 和验证结果快速审查，至少包含：

```markdown
## 变更摘要

## 关键改动

## 验证结果

## 风险与回滚

## 关联 Issue
```

只勾选真实完成的检查。截图、迁移说明和回滚步骤仅在适用时加入。

## Rebase 与历史整理边界

- rebase 前要求工作树和暂存区都干净；未经授权不得自动 stash。
- 先 fetch 并确认目标基线，必要时在用户允许下创建本地备份引用。
- 不对公共分支或其他人依赖的已发布提交执行 rebase。
- 禁止 `git push --force`。确需更新用户明确授权重写的私有分支时，只能在重新确认远程状态后使用 `--force-with-lease`。
- 遇到冲突时停止并报告冲突文件与可选方案，不猜测内容归属或擅自解决。

## 输出

用中文简要报告：

- 执行了哪些 Git 动作、影响哪些文件和分支。
- 实际运行的验证及结果。
- commit SHA、push 状态和 PR URL（若已执行）。
- 未执行、失败或仍需用户决定的事项。
