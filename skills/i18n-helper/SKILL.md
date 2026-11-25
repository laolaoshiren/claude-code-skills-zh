---
name: i18n-helper
description: 代码库国际化（i18n）与本地化助手，扫描业务源码中的硬编码 UI 文本、核查多语言文件缺失 key、生成语言包与配置。用于用户要求给前端或后端代码接入 i18n、提取硬编码文案或检查翻译完整性时；默认先出扫描清单并核对脏工作树，经用户确认范围后再改写源码，汉化英文 SKILL.md 请使用 skill-translator。
---

# 🌍 i18n-helper — 国际化 / 本地化助手

## 触发边界

- **适用**：扫描业务代码中的硬编码 UI 文案、接入或补全 `i18next` / `react-intl` / `vue-i18n` / `gettext` 等多语言框架、核对多语言 JSON/YAML/PO 缺失 key。
- **不适用**：把第三方英文 `SKILL.md` / `AGENTS.md` / `CLAUDE.md` 本地化为中文 → 请使用 `skill-translator`。

## 核心原则

1. **先盘点确认，再批量改源码。** 默认先输出硬编码扫描清单、建议 key 命名规范与受影响文件列表；**未经用户明确确认范围，不得直接批量改写业务源码或新建语言包目录**。
2. **保护工作树与框架运行约束。** 修改前先检查 `git status`，不覆盖用户已有未提交改动；替换文本时严格遵守目标框架作用域规则（尤其是 React Hooks 规则）。
3. **跨平台 UTF-8 写入。** 生成或更新中文语言包（`.json` / `.yaml` / `.po` / `.properties`）时必须显式使用 UTF-8（无 BOM）编码，防止 Windows 环境下默认 CP936/GBK 写坏非 ASCII 字符。

## 工作流程

### 1. 项目与现有 i18n 设施识别

- 读取 `package.json`、`pyproject.toml`、`go.mod`、`pom.xml` 等清单文件，确认技术栈与已安装的 i18n 库（`react-i18next`、`react-intl`、`vue-i18n`、`next-intl`、`gettext`、`Spring MessageSource`、`go-i18n` 等）。
- 未安装 i18n 依赖时先报告并给出方案，**未经授权不擅自执行 `npm install` / `pip install` 或改写 lockfile**。
- 读取已有语言文件目录与 key 命名风格（扁平点分或嵌套对象），保持一致。

### 2. 硬编码文本只读扫描

- 扫描用户指定目录中的 `.js/.jsx/.ts/.tsx/.vue/.py/.java/.go` 等源文件。
- **排除**：日志调试信息、SQL、正则、URL、import 路径、代码注释、内部枚举值与测试断言（除非用户指定）。
- **提取**：面向终端用户的 UI 文本、表单校验提示、按钮标签、弹窗与错误消息，汇总为清单交用户复核。

### 3. 语言文件生成与缺失 key 对账

根据项目既有格式生成或补齐语言包（始终显式 UTF-8 读写）：

- **JSON** (`i18next` / `react-intl` / `next-intl`)：`{ "key": "value" }`
- **YAML** (`vue-i18n`)：`key: value`
- **PO/POT** (`gettext`)：保留 `msgid` / `msgstr` 与复数规则
- **Properties** (Java)：明确项目要求的 UTF-8 或 `\uXXXX` 转义规范

同时对比基准语言与目标语言文件，列出缺失 key、多余孤儿 key 与插值占位符不一致项（如 `{name}`、`{{count}}`、`%s`）。

### 4. 确认后限范围代码替换

仅在用户确认替换范围后执行，并严格检查上下文作用域：

- **React 特别校验（严防 Hooks 崩溃）**：
  - 函数组件或自定义 Hook 内部：使用 `const { t } = useTranslation()`；
  - **非组件普通工具函数、常量定义、类方法或模块顶层**：严禁调用 `useTranslation()` 等 Hook，必须改为通过参数传入 `t` 或调用项目初始化后的 `i18n.t(...)` 实例，或改为保存 message key 在渲染层翻译。
- **Vue / 后端框架**：区分 `<template>` 内 `$t()`、`<script setup>` 内 `useI18n()` 与纯 TS 模块调用方式。
- 保留全部变量插值、HTML 富文本组件（如 `<Trans>`）与复数/性别格式。

### 5. 复验与差异核查

完成替换后：

1. 运行项目现有的类型检查（如 `tsc --noEmit`）、lint、构建或相关测试，验证没有引入作用域错误、缺失 import 或 JSON 语法错误。
2. 核对 `git diff`，确认未改动范围外文件且语言文件均为合法 UTF-8。
3. 未实际运行构建或测试时，如实标注「已修改、未执行构建验证」。

## 输出格式

```markdown
## 📊 i18n 扫描与处理报告

### 硬编码文本清单（待确认 / 已替换）
| 文件:行号 | 原文 | 建议 key | 上下文类型（组件 / 纯函数 / 模板） |
|-----------|------|----------|------------------------------------|
| `src/App.tsx:42` | 欢迎使用 | `page.welcome` | React 组件（可用 `useTranslation`） |

### 语言文件完整性
- `locales/zh-CN.json`：45/45 (100%)
- `locales/en-US.json`：42/45 (93.3%)，缺失 3 个 key：`...`

### 验证与限制
- 实际运行命令与结果：
- 需人工复核的动态拼接文本或复数变体：
```

## 注意事项

- 不要翻译专有技术术语（API、SDK、HTTP、OAuth 等）和品牌名。
- 日期、数字、货币格式优先使用 `Intl.DateTimeFormat` / `Intl.NumberFormat` 等 locale 感知 API。
- 严禁把硬编码文本与动态字符串直接用 `+` 拼接翻译，应改为命名插值占位符（如 `t('welcome', { name })`）。
