---
name: github-actions-gen
description: 分析真实项目并生成或修订安全、可验证的 GitHub Actions workflow；当用户要求创建 CI、测试矩阵、构建、Release、部署、缓存、Secrets、OIDC、PR 自动化或排查 workflow 配置时使用
---

# GitHub Actions CI/CD 生成器

## 核心原则

- 先读项目，再生成 workflow。不要凭项目名猜测运行时、包管理器、测试命令或部署目标。
- 默认只生成只读 CI。Release、部署、推送镜像、写回仓库和调用外部 webhook 必须先确认目标、凭据、环境保护与回滚方式。
- 将不可信 PR 代码与 Secrets、写权限、自托管 Runner 隔离。不要为方便而改用 `pull_request_target` 执行 PR 代码。
- 把所有 Action 固定到核验过的完整 40 位 commit SHA，并在旁边保留版本注释。不要使用 `@main`、`@master`、`@latest` 或可移动的 `@vN` tag。
- 为每个 job 设置最小 `permissions` 和 `timeout-minutes`；不依赖仓库默认权限。
- 生成后运行真实语法与项目命令验证，不把“配置看起来正确”当作通过。

## 工作流程

### 1. 盘点项目证据

- 读取 manifest、lockfile、wrapper、运行时文件和现有 workflow，例如 `package.json`、`.nvmrc`、`pyproject.toml`、`go.mod`、`Cargo.toml`、`Dockerfile` 与 `.github/workflows/`。
- 从项目脚本、贡献文档和现有 CI 确认 lint、test、build、package 命令。命令不存在时先指出缺口。
- 识别 monorepo 边界、工作目录、矩阵维度、服务容器、缓存路径与产物。
- 询问必要决策：触发分支、支持的运行时、部署目标、云账号、GitHub Environment、失败处理和发布授权。
- 检查当前工作树，保留用户已有修改；只编辑本次授权的 workflow 和必要配置。

### 2. 建立威胁模型

- `pull_request`：按不可信代码处理，使用只读 Token，不提供 Secrets，不在高权限自托管 Runner 上执行 fork 代码。
- `pull_request_target`：仅处理标签、评论等可信基准分支逻辑；绝不 checkout PR head、运行 PR 脚本或安装 PR 依赖。
- `push` / tag / `workflow_dispatch`：仍需限制分支、输入、Environment 和权限；写操作放入独立 job。
- 避免把 `${{ github.event.* }}` 等不可信表达式直接插进 `run:`。通过 `env:` 传值，并在脚本中按数据处理。
- 不把 Secrets 写入命令行、日志、缓存、Artifact 或 PR 评论；fork PR 缺少 Secrets 是正常安全边界。

### 3. 设计最小流水线

优先拆分职责：

- `ci.yml`：lint、test、build；`pull_request` 与受控 `push` 触发，只读权限。
- `release.yml`：仅在用户明确要求时生成；使用受保护 tag 或手动触发。
- `deploy.yml`：仅在部署目标明确时生成；使用 GitHub Environment、并发控制和最小 OIDC / Secrets 权限。

为耗时 job 设置取消策略和超时。矩阵只覆盖项目真正支持的版本；缓存 key 必须包含 lockfile，不能缓存凭据和构建秘密。

### 4. 核验并固定 Action

- 从 Action 官方仓库 release / tag 解析完整 commit SHA，核对仓库所有者、版本说明和运行时要求。
- 采用 `uses: owner/action@<40位SHA> # vX.Y.Z` 格式。版本注释用于阅读，SHA 才是执行边界。
- 对 `actions/checkout` 默认设置 `persist-credentials: false`。只有后续步骤确实要执行经过授权的 Git 写入时才保留凭据，并限制 job 权限。
- 使用 Dependabot 或人工维护流程更新 SHA；更新时重新阅读 release notes，不盲目替换。
- 本文示例 SHA 核验于 2026-07-22；实际生成时应重新核验官方 release。

### 5. 生成 workflow

下面示例假设项目已有 `.nvmrc`、`package-lock.json`、`lint`、`test` 和 `build` 脚本：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false

      - name: 配置 Node.js
        uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0
        with:
          node-version-file: .nvmrc
          cache: npm
          cache-dependency-path: package-lock.json

      - name: 安装依赖
        run: npm ci

      - name: 代码检查
        run: npm run lint

      - name: 运行测试
        run: npm test

      - name: 构建
        run: npm run build
```

不要机械复制示例。若项目使用 pnpm、Yarn、uv、Poetry、Gradle、Go 或 Rust，应使用其真实锁文件、wrapper 和命令。

### 6. 单独保护发布与部署

- 把发布 / 部署放入独立 job，只给该 job 必需的 `contents: write`、`packages: write` 或 `id-token: write`。
- 优先使用短期 OIDC，避免长期云密钥；限制云端 audience、subject、分支、仓库和 Environment。
- 为 production 使用 required reviewers、受保护 Environment、并发锁和可验证回滚。
- 对 `workflow_dispatch` 输入设置类型、选项和默认值；在执行前再次校验目标环境与版本。
- 发布前验证产物来源，必要时生成 attestations / provenance；不要部署来自未验证 PR 的 Artifact。

### 7. 验证

- 运行 `actionlint`；若工具不可用，明确说明未完成该门禁，不要声称语法通过。
- 运行 YAML 解析检查，并核对所有 `${{ }}`、shell、路径、矩阵和 `needs` 引用。
- 在本地执行 workflow 中引用的 lint、test、build 命令，或说明环境限制。
- 搜索所有 `uses:`，确认第三方 Action 都是完整 SHA；检查 checkout 的 `persist-credentials`。
- 用 fork PR、内部 PR、push、tag、手动部署等场景检查 Secrets 与权限是否符合预期。
- 查看最终 diff，确认没有写入 Token、账号、真实 webhook、`.env` 或无关配置。

## 交付格式

用中文说明：

1. 新增或修改的 workflow 及触发条件；
2. 每个 job 的权限、Secrets / OIDC 和 Environment 边界；
3. Action SHA 的版本来源与核验时间；
4. 已运行的验证、结果和未覆盖项；
5. 发布 / 部署的人工确认点与回滚方式。

除非用户明确要求，不额外创建 `README-CICD.md` 等辅助文档。

## 质量检查清单

- [ ] 命令、运行时和 lockfile 来自真实项目证据
- [ ] 所有 Action 使用完整 40 位 SHA 和版本注释
- [ ] checkout 默认 `persist-credentials: false`
- [ ] workflow / job 权限最小化并设置超时
- [ ] fork PR 不接触 Secrets、写权限或高权限 Runner
- [ ] `pull_request_target` 不执行不可信 PR 内容
- [ ] 不可信上下文未直接拼入 shell
- [ ] Release / 部署经过明确授权和 Environment 保护
- [ ] `actionlint` 与项目命令验证已完成或如实记录缺口
