---
name: env-manager
description: 环境变量与 .env 安全管理助手，只读扫描 .env* 文件与源码中的环境变量引用、识别缺失或硬编码密钥，并生成脱敏的 .env.example 与校验模板。用于用户要求整理环境变量、检查缺失配置、核查 .gitignore 泄漏风险或生成配置模板时；绝不回显真实 Secret 原文，修改真实 .env 文件前必须取得确认。
---

# 环境变量管理器

## 触发边界

- **适用**：梳理项目 `.env*` 变量清单、对比源码引用找出缺失配置、检查 `.gitignore` 与客户端前缀泄露（如 `NEXT_PUBLIC_` / `VITE_`）、生成安全的 `.env.example` 与校验 Schema。
- **不适用**：全仓库源码注入/越权漏洞审计 → `security-audit`；第三方依赖 CVE 核查 → `dep-auditor`。

## 核心原则

1. **凭据零回显。** 扫描 `.env*` 文件时只提取变量名、来源文件和是否为空，**严禁在终端输出、报告、`.env.example` 或聊天记录中打印任何真实 API Key / Token / 密码原文**。
2. **默认不改写真实 `.env`。** 生成或更新 `.env.example`、校验 Schema 或修改真实 `.env` 前先展示差异并取得用户确认；严禁自动删除疑似未使用的环境变量。
3. **跨平台 UTF-8 读写。** Windows 环境下通过 Python 或脚本读写含中文注释的 `.env` / `.env.example` 时，必须显式声明 `encoding="utf-8"`，避免 CP936/GBK 编码报错或乱码。

## 工作流程

### 1. 只读扫描项目

- 检测所有 `.env*` 文件（`.env` / `.env.local` / `.env.development` / `.env.production` / `.env.example`），仅提取变量名与赋值状态（已设 / 为空），不输出值内容。
- 检查 `.gitignore` 是否正确忽略了包含真实凭据的 `.env*` 文件，并用 `git ls-files ".env*"` 检查是否已被误提交进版本库。
- 扫描源码中引用的环境变量（`process.env.XXX`、`import.meta.env.XXX`、`os.environ["XXX"]`、`os.getenv("XXX")`、`os.Getenv("XXX")`、`env::var("XXX")` 等）。
- 区分三类结果：
  - **已使用但未在模板/环境中定义**（缺失配置）；
  - **静态扫描未发现引用的变量**（仅标为「待人工确认候选」，可能被 CI、容器、框架隐式读取或动态拼接引用）；
  - **代码中疑似硬编码的敏感凭据**（仅报告 `文件:行号`）。

### 2. 校验与风险分析

- 检查必填变量是否在模板中标明格式与约束（URL、端口号 1–65535、布尔值、枚举值）。
- 核对前端框架公开前缀边界：确保后端私钥/数据库密码未被误加 `NEXT_PUBLIC_`、`VITE_`、`REACT_APP_`、`NUXT_PUBLIC_`、`VUE_APP_` 前缀暴露到浏览器 Bundle。
- 对比 `.env.example` 与真实环境变量名清单的差异。

### 3. 确认后生成与同步模板

经用户确认目标文件后：

- 生成或更新 `.env.example`（仅包含变量名、安全占位符与中文注释，严禁填入真实密钥）。
- 按需生成结构化校验规则（如 Zod / Pydantic Settings / `.env.schema.json`）或 CI Secrets 清单。
- 对 monorepo / Docker Compose 给出显式 `env_file` 挂载与子包加载建议。

## 输出格式

### `.env.example` 规范示例

```bash
# 应用配置
APP_NAME=my-app
APP_ENV=development          # development | staging | production
APP_PORT=3000                # 服务端口 (1-65535)
APP_DEBUG=true               # 调试模式

# 数据库
DB_HOST=localhost
DB_PORT=5432
DB_NAME=mydb
DB_USER=                     # 必填
DB_PASSWORD=                 # 必填，生产环境请通过 Secrets 注入

# 第三方服务
REDIS_URL=                   # 必填，格式：redis://host:port
JWT_SECRET=                  # 必填，至少 32 位高熵随机字符串
```

### 校验报告示例

```text
📋 环境变量分析报告
==================
✅ 已定义且已引用：12 个
⚠️ 静态扫描未见引用（待人工确认）：2 个（S3_BUCKET, OLD_API_KEY）
❌ 代码已引用但模板缺失：1 个（SENDGRID_API_KEY）
🔒 疑似硬编码敏感信息：1 处（src/auth.js:23，已脱敏）

建议：
1. 人工确认 S3_BUCKET 与 OLD_API_KEY 是否由 CI、部署平台或动态代码读取，勿直接删除
2. 在 .env.example 中补充 SENDGRID_API_KEY 及格式说明
3. 将 src/auth.js:23 的硬编码凭据迁移至环境变量，并视泄露范围轮换密钥
```

## 安全检查清单

- [ ] 扫描和报告只展示变量名及脱敏状态，不回显真实 Secret
- [ ] `.env` 及含密钥的本地环境文件已加入 `.gitignore` 且未被 Git 跟踪
- [ ] `.env.example` 存在且与源码引用同步
- [ ] 后端敏感变量未误加前端客户端公开前缀
- [ ] 生产环境使用 Secrets 管理（GitHub Secrets / Vault / 云 KMS）
- [ ] 数据库密码与 Token 不写入应用日志

## 修改边界

- 不要自动删除或改写真实 `.env`；先展示差异并取得用户确认。
- “未发现引用”仅代表静态扫描结果，仍需核对 CI、容器编排、部署平台和动态变量拼接访问。
- 不把任何真实 Secret 复制到 `.env.example`、Schema、日志、Issue 或聊天输出中。

## 框架客户端前缀速查

| 框架 | 客户端暴露前缀 | 常见本地文件 | 说明 |
|------|----------------|--------------|------|
| Next.js | `NEXT_PUBLIC_` | `.env.local` | 后端私密变量严禁加此前缀 |
| Vite | `VITE_` | `.env` / `.env.local` | 会打入前端构建产物 |
| Create React App | `REACT_APP_` | `.env` | 会打入前端构建产物 |
| Nuxt | `NUXT_PUBLIC_` | `.env` | 运行时公开配置 |
| Vue CLI | `VUE_APP_` | `.env` | 会打入前端构建产物 |
| Docker | `ARG` vs `ENV` | `compose.yml` | 勿把敏感密钥写入 `ARG` 留存在镜像层 |
