---
name: eslint-fix
description: ESLint 自动修复专家 — 识别 ESLint 报错，批量修复，支持常见规则和自定义配置
---

# ESLint 自动修复专家

## 触发条件
当用户遇到 ESLint 错误或需要批量修复代码规范问题时激活此技能。

## 工作流程

1. **检测项目配置**
   - 查找 `.eslintrc.*` 或 `eslint.config.*` 文件
   - 识别使用的 ESLint 版本（v8/v9）和插件
   - 检查是否有 `prettier`、`@typescript-eslint` 等扩展

2. **运行 ESLint 检查**
   - 执行 `npx eslint . --format json` 获取所有错误
   - 按文件和规则分组统计
   - 区分 warning 和 error

3. **分类处理**
   - **可自动修复**（fixable）：直接运行 `eslint --fix`
   - **需手动修复**：逐条分析，提供修改建议
   - **需配置调整**：建议禁用或调整规则

4. **批量修复**
   - 对可自动修复的文件批量执行修复
   - 对需要手动修改的文件，逐一展示 diff
   - 修复后再次运行 ESLint 验证

## 输出格式

```markdown
## 📊 ESLint 检查报告

**项目：** [项目名]
**ESLint 版本：** v8/v9
**总错误数：** X 个 error，Y 个 warning

### 📁 按文件统计
| 文件 | Error | Warning |
|------|-------|---------|
| src/index.ts | 3 | 1 |
| src/utils.ts | 0 | 2 |

## 🔧 修复结果

### ✅ 自动修复（X 个）
已修复文件：
- `src/index.ts` — 修复了 3 个问题

### ⚠️ 需手动修复（Y 个）
#### `src/utils.ts:15`
**规则：** `@typescript-eslint/no-explicit-any`
**当前代码：**
\`\`\`typescript
function process(data: any) { ... }
\`\`\`
**建议修复：**
\`\`\`typescript
function process(data: unknown) { ... }
\`\`\`

## 💡 配置建议
- 建议在 `.eslintrc.js` 中添加以下规则以避免类似问题
```

## 常见可自动修复的规则
- `semi` — 分号
- `quotes` — 引号风格
- `indent` — 缩进
- `no-trailing-spaces` — 行尾空格
- `comma-dangle` — 尾逗号
- `arrow-parements` — 箭头函数括号
- `prefer-const` — const vs let

## 注意事项
- 修复前先确认用户的 ESLint 配置偏好
- 对可能影响逻辑的修改要先询问用户
- 修复后确保代码仍然可编译运行
- 如果有 Prettier 配置，先运行 Prettier 再运行 ESLint
