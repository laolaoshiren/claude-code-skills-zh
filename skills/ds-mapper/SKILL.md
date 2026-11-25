---
name: ds-mapper
description: 项目目录结构地图生成器，只读扫描代码库并输出带中文注释的可视化目录树、模块职责表与启动入口建议。用于用户要求「带我看看项目结构」「这个仓库怎么组织的」「画目录树」或快速上手陌生代码库时；仅产出结构导览，不替代项目 README 编写（zh-readme）或详细技术/API 手册生成（zh-docgen）。
---

# 项目目录结构地图（Directory Structure Mapper）

## 触发边界

- **适用**：快速梳理任意代码库的目录层级、模块职责、入口文件与配置文件分布。
- **不适用**：撰写开源仓库展示首页 → `zh-readme`；撰写详细架构设计、API 手册或运维文档 → `zh-docgen`。

## 工作流程

1. **跨平台扫描根目录（只读）**
   - 优先使用当前 Agent 原生文件列举工具，或跨平台 Git 命令获取受版本控制的目录结构（Windows 含中文路径时关闭引号转义）：
     - Git 仓库：`git -c core.quotepath=false ls-files`
     - 无 Git 的 Windows 环境：PowerShell `Get-ChildItem -Depth 3`（**不要在 Windows 下运行 Unix `find . -maxdepth 3`**，Windows 自带 `find.exe` 是文本搜索工具，会直接报错）
     - 无 Git 的 macOS / Linux 环境：`ls -la` 或 `find . -maxdepth 3`
2. **读取关键清单文件**
   - 读取实际存在的元信息文件（如 `package.json`、`pyproject.toml`、`Cargo.toml`、`go.mod`、`pom.xml`、`README.md`），确认真实语言、框架、包管理器与工作区（monorepo）边界，不凭目录名猜测。
3. **梳理核心目录职责**
   - 抽样阅读各核心目录的入口文件与典型模块，用一句自然中文概括目录职责。
4. **生成结构地图**
   - 输出带中文注释的 ASCII 目录树、模块职责对照表与阅读入口建议。

## 输出格式

```markdown
## 📂 项目结构地图

### 🔧 项目信息
- 语言：TypeScript / Python / Go / ...
- 框架：Next.js / FastAPI / Gin / ...
- 包管理：pnpm / uv / go mod / ...

### 🌳 目录树

```text
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
| `src/` | 核心源码 | `index.ts`, `app.ts` |
| `src/components/` | UI 组件 | `Button.tsx`, `Modal.tsx` |

### 💡 入口建议
- 🚀 启动入口：`src/index.ts`
- 📖 入门文档：`README.md`
- ⚙️ 配置文件：`config.yaml`
```

## 注意事项

- 默认只读，不修改仓库中的任何文件。
- 自动跳过 `node_modules`、`.git`、`vendor`、`__pycache__`、`dist`、`build`、`.next`、`target` 等产物与依赖目录。
- 默认最多展示 3 层深度，monorepo 项目按 `packages/` 或 `apps/` 分区列出核心子包，避免输出过长。
- 未实际读取到的目录或文件不得编造用途，必要时标明「待进一步查看」。
