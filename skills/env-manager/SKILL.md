---
name: env-manager
description: 环境变量管理器：扫描、校验、同步 .env 文件，生成安全配置模板
---

# 环境变量管理器

## 触发条件
当用户要求管理环境变量、.env 文件、配置同步、Secrets 检查时激活。

## 工作流程

### 1. 扫描项目
- 检测所有 `.env*` 文件（.env / .env.local / .env.development / .env.production）
- 扫描代码中引用的环境变量（`process.env.XXX` / `os.environ['XXX']` / `os.getenv('XXX')`）
- 识别已定义但未使用的变量（死配置）
- 识别已使用但未定义的变量（缺失配置）

### 2. 校验分析
- 检查必填变量是否有默认值
- 验证 URL 格式、端口号范围、布尔值格式
- 检测硬编码的敏感信息（API Key / Token / Password）
- 对比 .env.example 与实际 .env 文件的差异

### 3. 生成/修复
- 生成 `.env.example` 模板（仅包含变量名和说明，不含真实值）
- 生成 `.env.schema.json`（结构化校验规则）
- 检测到硬编码密钥时，建议迁移到环境变量
- 生成 `dotenv` 加载配置（针对不同框架）

### 4. 同步
- 在 monorepo 中同步共享环境变量
- 生成 Docker Compose 的 env_file 配置
- 生成 CI/CD 的 Secrets 配置清单

## 输出格式

### .env.example 示例
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
DB_PASSWORD=                 # 必填，生产环境请使用 Secrets

# 第三方服务
REDIS_URL=                   # 必填，格式：redis://host:port
JWT_SECRET=                  # 必填，至少 32 位随机字符串
```

### 校验报告示例
```
📋 环境变量分析报告
==================
✅ 定义且使用: 12 个
⚠️  定义未使用: 2 个（S3_BUCKET, OLD_API_KEY）
❌ 使用未定义: 1 个（SENDGRID_API_KEY）
🔒 硬编码敏感信息: 1 处（src/auth.js:23）

建议：
1. 删除 .env 中的 S3_BUCKET 和 OLD_API_KEY
2. 在 .env 中添加 SENDGRID_API_KEY
3. 将 src/auth.js:23 的硬编码 token 迁移到环境变量
```

## 安全检查清单
- [ ] `.env` 已添加到 `.gitignore`
- [ ] `.env.example` 存在且与代码同步
- [ ] 无硬编码的 API Key / Token / Password
- [ ] 生产环境使用 Secrets 管理（GitHub Secrets / AWS SSM / Vault）
- [ ] JWT_SECRET / ENCRYPTION_KEY 足够随机（32+ 字符）
- [ ] 数据库密码不在日志中输出

## 常见陷阱
- **Next.js**：只有 `NEXT_PUBLIC_` 前缀的变量会暴露给客户端，后端专用变量不要加此前缀
- **Docker**：构建时的 ARG 和运行时的 ENV 是不同的，不要混淆
- **Create React App**：`.env` 中的变量必须以 `REACT_APP_` 开头才会被注入
- **Vite**：使用 `VITE_` 前缀暴露变量给客户端
- **monorepo**：根目录的 `.env` 不会自动被子包读取，需要显式配置

## 框架适配

| 框架 | 客户端前缀 | 配置文件 | 加载方式 |
|------|-----------|---------|---------|
| Next.js | NEXT_PUBLIC_ | .env.local | 自动 |
| Vite | VITE_ | .env | 自动 |
| CRA | REACT_APP_ | .env | 自动 |
| Nuxt | NUXT_PUBLIC_ | .env | 自动 |
| Vue CLI | VUE_APP_ | .env | 自动 |
