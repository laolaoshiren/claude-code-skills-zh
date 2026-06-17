---
name: changelog-gen
description: Changelog 生成器 - 从 Git 历史自动生成 CHANGELOG
---

# Changelog 自动生成

## 触发条件
当用户要求生成 changelog、更新日志、版本记录、release notes 时激活此技能。

## 工作流程

### 第 1 步：获取 Git 历史
```bash
# 获取上一个 tag 到 HEAD 的所有提交
git log --oneline --since="$(git describe --tags --abbrev=0)" HEAD

# 或指定范围
git log --oneline v1.0.0..HEAD
```

### 第 2 步：分类提交
按 Conventional Commits 分类：

| 分类 | Type 标识 | 图标 |
|------|----------|------|
| 新功能 | `feat` | ✨ |
| Bug 修复 | `fix` | 🐛 |
| 文档 | `docs` | 📝 |
| 重构 | `refactor` | ♻️ |
| 性能优化 | `perf` | ⚡ |
| 测试 | `test` | 🧪 |
| 构建/工具 | `chore` | 🔧 |
| Breaking Changes | 含 `BREAKING CHANGE:` 或 `!` | ⚠️ |
| 安全修复 | `fix(security)` 或含 CVE | 🔒 |
| 依赖更新 | `deps` 或 `chore(deps)` | 📦 |

### 第 3 步：版本号确定策略

遵循 Semantic Versioning 规则：

| 变更类型 | 版本变化 | 示例 |
|---------|---------|------|
| Breaking Changes | 主版本 +1 | 1.2.0 → 2.0.0 |
| 新功能 (feat) | 次版本 +1 | 1.2.0 → 1.3.0 |
| Bug 修复 (fix) | 修订版本 +1 | 1.2.0 → 1.2.1 |
| 安全修复 (fix(security)) | 修订版本 +1（紧急发布） | 1.2.0 → 1.2.1 |

**判断依据**：
- 提交信息含 `BREAKING CHANGE:` 或 type 后加 `!`（如 `feat!:`）→ 主版本
- 存在 `feat` 提交 → 次版本
- 仅 `fix`/`docs`/`chore` 等 → 修订版本

### 第 4 步：生成 CHANGELOG

## 输出格式

```markdown
# Changelog

## [1.3.0] - 2026-06-17

### ⚠️ Breaking Changes
- 移除废弃的 `/api/v1/users` 端点，统一使用 `/api/v2/users` (#130)

### ✨ 新功能
- 新增用户认证模块 (#123)
- 支持 OAuth2 登录 (#124)
- 新增批量导出功能 (#128)

### 🔒 安全修复
- 升级 lodash 修复原型污染漏洞 CVE-2025-XXXX (#129)

### 🐛 Bug 修复
- 修复分页查询偏移量错误 (#125)
- 修复并发写入导致的数据竞争 (#127)

### ⚡ 性能优化
- 优化大列表渲染性能，减少 50% 内存占用 (#126)

### 📝 文档
- 更新 API 文档 (#131)

### 📦 依赖更新
- 升级 axios 1.6.0 → 1.7.0 (#132)
```

## 注意事项
- Breaking Changes 必须放在最前面，加粗突出显示
- 每条记录关联 Issue/PR 编号，便于追溯
- 安全修复需注明 CVE 编号（如有）
- 版本号应与 git tag 保持一致
- 如果是预发布版本，使用 `-beta.1`、`-rc.1` 后缀
- 可维护一个 `CHANGELOG.md` 文件，每次 release 追加到顶部
