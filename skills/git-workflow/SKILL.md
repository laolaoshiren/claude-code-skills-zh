---
name: git-workflow
description: Git 工作流自动化 - 智能分支管理、提交信息生成、PR 创建
---

# Git 工作流助手

## 触发条件
当用户要求提交代码、创建分支、发起 PR、整理 commit、rebase 时激活此技能。

## 工作流程

### 第 1 步：分析当前状态
```bash
git status
git log --oneline -10
git diff --staged
```
识别暂存区的变更内容、涉及的文件和改动类型。

### 第 2 步：确定提交类型
根据变更内容自动判断 type：
- `feat` — 新功能
- `fix` — Bug 修复
- `docs` — 仅文档变更
- `style` — 格式调整（不影响逻辑）
- `refactor` — 重构（非新功能、非修复）
- `test` — 测试相关
- `perf` — 性能优化
- `chore` — 构建/工具链变更

### 第 3 步：生成提交信息
格式遵循 Conventional Commits：`<type>(<scope>): <description>`

### 第 4 步：分支管理与 PR
根据变更类型创建分支并生成 PR 描述。

### 第 5 步：历史整理
交互式 rebase 整理提交历史，合并琐碎提交。

## 输出格式

### Commit Message 模板

```
<type>(<scope>): <简短描述>

<body: 详细说明变更原因和内容>

<footer: 关联 Issue、Breaking Changes>
```

**示例**：
```
feat(auth): 添加 OAuth2 第三方登录支持

集成 Google 和 GitHub OAuth2 登录，用户可绑定已有账号。
新增 /api/auth/oauth/callback 端点处理回调。

Closes #123
```

### PR 描述模板

```markdown
## 变更摘要
简要描述本次 PR 做了什么。

## 变更类型
- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 文档 (docs)
- [ ] 其他 (chore)

## 改动文件
| 文件 | 变更说明 |
|------|---------|
| src/auth/oauth.ts | 新增 OAuth2 认证逻辑 |
| src/routes/auth.ts | 新增回调路由 |

## 测试情况
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动验证完成

## 关联 Issue
Closes #123

## 截图/录屏（如适用）
```

### 分支命名规范
| 类型 | 格式 | 示例 |
|------|------|------|
| 新功能 | `feat/<功能名>` | `feat/oauth-login` |
| Bug 修复 | `fix/<问题描述>` | `fix/login-timeout` |
| 紧急修复 | `hotfix/<紧急描述>` | `hotfix/security-patch` |
| 文档 | `docs/<内容>` | `docs/api-guide` |
| 重构 | `refactor/<范围>` | `refactor/auth-module` |

## 注意事项
- 提交信息使用中文或英文均可，但同一个仓库应保持一致
- 每个提交应保持原子性，只做一件事
- PR 描述应足够详细，让 reviewer 无需查看代码即可理解变更
- rebase 前确保本地改动已提交或暂存，避免丢失工作
- 不要对已推送到远程的公共分支执行 rebase
