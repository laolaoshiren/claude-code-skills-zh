---
name: changelog-gen
description: Changelog 生成器 - 从 Git 历史自动生成 CHANGELOG
---

# Changelog 自动生成

## 触发条件
当用户要求生成 changelog、更新日志、版本记录、release notes 时激活此技能。

## 工作流程

1. **获取 Git 历史** — `git log --oneline --since="last tag"`
2. **分类提交** — 按 Conventional Commits 分类：
   - ✨ Features (feat)
   - 🐛 Bug Fixes (fix)
   - 📝 Documentation (docs)
   - ♻️ Refactoring (refactor)
   - ⚡ Performance (perf)
   - 🧪 Tests (test)
   - 🔧 Chores (chore)
3. **生成 CHANGELOG** — Markdown 格式，按版本号组织

## 输出格式

```markdown
# Changelog

## [1.2.0] - 2026-04-14

### ✨ 新功能
- 新增用户认证模块 (#123)
- 支持 OAuth2 登录 (#124)

### 🐛 Bug 修复
- 修复分页查询偏移量错误 (#125)

### 📝 文档
- 更新 API 文档 (#126)
```
