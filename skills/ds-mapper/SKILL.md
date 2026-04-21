---
name: ds-mapper
description: 项目目录结构地图 - 生成带说明的可视化目录树，快速理解任意代码库
---

# 项目目录结构地图（Directory Structure Mapper）

## 触发条件
当用户说「带我看看项目结构」「这个仓库怎么组织的」「目录树」「帮我理解这个代码库」或类似需求时激活此技能。

## 工作流程

1. **扫描根目录** — 使用 Bash `find` 和 `ls` 获取顶层结构
2. **分析关键目录** — 读取关键文件（package.json, Cargo.toml, pyproject.toml, go.mod 等）获取项目元信息
3. **递归扫描** — 深入扫描主要目录，理解各模块职责
4. **生成结构图** — 输出 ASCII 目录树 + 中文注释说明

## 输出格式

```markdown
## 📂 项目结构地图

### 🔧 项目信息
- 语言：TypeScript / Python / Go / ...
- 框架：Next.js / FastAPI / Gin / ...
- 包管理：pnpm / pip / go mod

### 🌳 目录树

```
project-root/
├── src/                    # 📦 核心源码
│   ├── components/         # 🧩 UI 组件
│   ├── services/           # 🔌 业务逻辑层
│   ├── utils/              # 🔧 工具函数
│   └── index.ts            # 🚀 入口文件
├── tests/                  # 🧪 测试文件
├── docs/                   # 📖 文档
├── .github/                # 🔄 CI/CD 配置
├── package.json            # 📋 依赖管理
└── README.md               # 📝 项目说明
```

### 🗺️ 模块说明

| 目录 | 职责 | 关键文件 |
|------|------|----------|
| `src/` | 核心源码 | index.ts, app.ts |
| `src/components/` | UI 组件 | Button.tsx, Modal.tsx |

### 💡 入口建议
- 🚀 启动入口：`src/index.ts`
- 📖 入门文档：`README.md`
- ⚙️ 配置文件：`config.yaml`
```

## 注意事项
- 跳过 node_modules, .git, vendor, __pycache__ 等常见忽略目录
- 对每个关键目录给出一行中文说明
- 如果项目有 monorepo 结构，分别列出各 packages
- 最多展示 3 层深度，避免输出过长
