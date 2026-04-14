---
name: git-workflow
description: Git 工作流自动化 - 智能分支管理、提交信息生成、PR 创建
---

# Git 工作流助手

## 触发条件
当用户要求提交代码、创建分支、发起 PR、整理 commit、rebase 时激活此技能。

## 工作流程

### 智能提交信息
1. 分析 `git diff` 内容
2. 自动生成符合 Conventional Commits 规范的提交信息
3. 格式：`<type>(<scope>): <description>`
4. type 选择：feat/fix/docs/style/refactor/test/chore/perf

### 分支管理
- `feat/功能名` — 新功能
- `fix/问题描述` — Bug 修复
- `hotfix/紧急修复` — 紧急修复

### PR 描述生成
自动生成包含以下内容的 PR 描述：
- 变更摘要
- 改动文件列表
- 测试情况
- 关联 Issue

## 命令参考
```bash
# 查看当前状态
git status
git log --oneline -10
git diff --staged

# 分支操作
git checkout -b feat/xxx
git rebase -i HEAD~n
```
