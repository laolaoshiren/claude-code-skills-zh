---
name: eslint-fix
description: 安全诊断并修复 ESLint error、warning 和配置兼容问题。用于用户要求运行 lint、解释 ESLint 报错、限定范围自动修复或迁移 ESLint 配置时；优先使用项目锁定的包管理器与版本，先预检再修改，不自动下载最新版或批量改写无关源码。
---

# ESLint 修复助手

## 工作流程

### 1. 识别项目工具链

读取：

- `package.json` 中的 scripts、`devDependencies` 和 `packageManager`。
- npm、pnpm、Yarn 或 Bun 的 lockfile。
- `eslint.config.*`、`.eslintrc.*`、`.eslintignore`、Prettier 和 TypeScript 配置。
- 适用的仓库规则、Git 状态和用户指定的文件范围。

优先运行仓库已有的 lint script。只有确认 ESLint 已被当前项目锁定并安装时，才使用对应包管理器的本地执行方式。若缺失依赖，先报告；安装包、更新 lockfile 或迁移配置需要单独授权。

### 2. 建立只读基线

先对用户指定或本轮相关范围运行不修改文件的检查，记录：

- 实际命令、ESLint 版本和退出状态。
- error / warning 数量、涉及文件和规则。
- 基线中已有的问题与本轮引入的问题。

不要默认扫描整个大型仓库，也不要用未锁定依赖、可能联网下载新版本的 `npx` 调用。

### 3. 预览可修复范围

- 使用项目现有命令支持的 `--fix-dry-run`、JSON 输出或等价能力判断预计改动。
- 检查当前 Git diff，确认目标文件没有与用户修改重叠。
- 区分可自动修复、需要理解代码语义、需要配置决策三类问题。
- 展示预计修改范围；可能产生大面积格式 diff 或改变逻辑时先取得确认。

### 4. 限定范围修复

- 只对已确认的文件执行 `--fix`，不自动扩大到整个仓库。
- 对 `no-explicit-any`、未处理 Promise、React Hooks 依赖等语义规则，结合类型、调用方和运行路径修改，不能机械替换。
- 不为消除报错而默认禁用规则、加入全局 ignore、修改 formatter 顺序或降低严重级别。
- Prettier 与 ESLint 的执行顺序以项目现有 scripts 和集成配置为准。

常见可自动修复规则包括 `semi`、`quotes`、`indent`、`no-trailing-spaces`、`comma-dangle`、`arrow-parens` 和 `prefer-const`；dry-run 和 diff 只能预览改动，最终仍需按风险运行类型检查、测试或构建。

### 5. 复验

实际修改后：

1. 重新运行目标范围 lint。
2. 按改动风险运行类型检查、相关测试或构建。
3. 查看 Git diff，确认没有 lockfile、生成物或无关格式变化。
4. 记录未解决规则、原因和建议下一步。

## 安全边界

- 未经明确授权，不安装或升级依赖，不修改 lockfile、ESLint 配置、Prettier 配置或项目脚本。
- 不覆盖工作树中已有修改；目标文件存在重叠时先报告。
- 不声称“已修复”或“可编译”，除非对应命令真实运行并成功。
- Windows 与 Linux 都优先使用项目已有 scripts 和路径，不硬编码 shell 专属命令。

## 输出

```markdown
## ESLint 检查结果

- 范围：
- ESLint / 包管理器版本：
- 基线：X error，Y warning
- 实际命令与退出状态：

## 修改

| 文件 | 规则 | 处理方式 |
|------|------|----------|

## 复验

- lint：
- 类型检查 / 测试 / 构建：
- 未解决问题与原因：
```
