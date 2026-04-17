---
name: dep-auditor
description: 依赖安全审计：扫描依赖文件，检测已知漏洞、过期版本、许可证风险
---

# 依赖安全审计

## 触发条件
当用户要求检查依赖安全、审查 package.json/requirements.txt/go.mod，或询问依赖是否有漏洞时激活。

## 工作流程

### 1. 扫描依赖文件
自动识别项目中的依赖清单：
- `package.json` / `package-lock.json` / `pnpm-lock.yaml`
- `requirements.txt` / `Pipfile.lock` / `poetry.lock`
- `go.mod` / `go.sum`
- `Cargo.toml` / `Cargo.lock`
- `pom.xml` / `build.gradle`
- `Gemfile.lock`

### 2. 安全检查

#### 🔴 高危：已知 CVE 漏洞
- 查询 npm audit / pip-audit / govulncheck 等官方工具
- 检查 OSV 数据库
- 标记 CVSS 评分 ≥ 7.0 的漏洞

#### 🟡 中危：过期依赖
- 检查是否有大版本落后（当前版本 vs 最新稳定版）
- 检查已废弃（deprecated）的包
- 检查超过 2 年未更新的依赖

#### 🟠 低危：许可证风险
- 检查 GPL/AGPL 等传染性许可证
- 检查未知或自定义许可证
- 检查许可证不一致（同项目多许可证冲突）

### 3. 生成审计报告

```markdown
# 📋 依赖安全审计报告

**项目**: {project-name}
**扫描时间**: {date}
**依赖总数**: N

## 🔴 高危漏洞 (X)

| 包名 | 当前版本 | 漏洞 | CVSS | 修复版本 | 说明 |
|------|---------|------|------|---------|------|
| ... | ... | ... | ... | ... | ... |

## 🟡 过期依赖 (X)

| 包名 | 当前版本 | 最新版本 | 落后版本数 | 说明 |
|------|---------|---------|-----------|------|
| ... | ... | ... | ... | ... |

## 🟠 许可证风险 (X)

| 包名 | 许可证 | 风险等级 | 说明 |
|------|--------|---------|------|
| ... | ... | ... | ... |

## ✅ 建议操作

1. 立即修复高危漏洞：`npm audit fix` / `pip-audit --fix`
2. 更新过期依赖：按 major/minor 分批升级
3. 许可证合规：替换或协商使用
```

### 4. 自动修复建议
- 对于每个漏洞，提供具体的升级命令
- 如果有 breaking change，说明迁移步骤
- 生成批量升级脚本

## 命令参考

```bash
# Node.js
npm audit --json
npx npm-check-updates

# Python
pip-audit
pip list --outdated

# Go
govulncheck ./...
go list -m -u all

# Rust
cargo audit
```

## 注意事项
- 先在测试环境验证升级，不要直接在生产环境操作
- 某些漏洞可能有缓解措施（workaround），不必急于升级
- 注意 lock 文件的一致性，升级后务必重新生成 lock 文件
