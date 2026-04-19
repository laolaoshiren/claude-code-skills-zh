---
name: github-actions-gen
description: GitHub Actions CI/CD 流水线生成器：根据项目技术栈自动创建 workflows
---

# GitHub Actions CI/CD 生成器

## 触发条件
当用户要求创建 CI/CD 流水线、GitHub Actions workflow、自动化部署配置时激活。

## 工作流程

### 1. 项目分析
- 检测项目语言和框架（package.json / requirements.txt / go.mod / Cargo.toml 等）
- 识别现有 CI 配置（.github/workflows/）
- 分析项目结构：单体仓库 or 单项目、monorepo 工具（nx / turborepo / lerna）
- 检测测试框架（jest / pytest / go test / cargo test）

### 2. 流水线设计
根据项目类型生成对应 workflow：

**通用流水线模板：**
- `ci.yml` — 代码检查 + 测试（push/PR 触发）
- `release.yml` — 版本发布（tag 触发）
- `deploy.yml` — 部署流水线（按需）

**前端项目额外：**
- Node.js 版本矩阵测试
- Lighthouse 性能检测
- 静态资源 CDN 缓存失效

**后端项目额外：**
- Docker 镜像构建 + 推送
- 数据库 migration 检查
- API 契约测试

### 3. 生成配置
- 使用 GitHub Actions 最佳实践
- 合理利用 cache（actions/cache）加速构建
- 矩阵策略覆盖多版本
- Secrets 引用安全规范（不硬编码）
- 中文注释说明每个 step 的作用

### 4. 输出文件
在 `.github/workflows/` 目录生成：
- `ci.yml` — 主 CI 流水线
- `release.yml` — 发布流水线（如需要）
- `README-CICD.md` — 流水线使用说明

## 输出格式

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18, 20, 22]  # 按项目调整
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
      - run: npm run lint
```

## 质量检查清单
- [ ] workflow 文件语法正确（可用 `actionlint` 验证）
- [ ] 使用固定版本 tag（避免 `@main`）
- [ ] Secrets 通过 `${{ secrets.XXX }}` 引用
- [ ] 设置适当的权限（`permissions`）
- [ ] 超时时间合理（`timeout-minutes`）
- [ ] 失败通知机制（Slack / 邮件 / 微信 webhook）

## 常见陷阱
- **Node.js 项目**：确保 lockfile（package-lock.json / pnpm-lock.yaml）存在，否则 `npm ci` 会失败
- **Python 项目**：注意 requirements.txt 和 pyproject.toml 的优先级
- **Docker 构建**：使用 multi-stage build 减小镜像体积
- **缓存策略**：key 要包含 lockfile hash，否则缓存可能过期
- **矩阵测试**：不要过度配置，3-5 个版本足够

## 示例

用户输入：「帮我给这个 Next.js 项目创建 CI/CD 流水线」

输出：
1. 分析 package.json 检测 Next.js 版本、测试框架、部署目标
2. 生成 ci.yml（lint + test + build）
3. 生成 deploy.yml（Vercel / Docker 部署）
4. 生成使用说明 README-CICD.md
