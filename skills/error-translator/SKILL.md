---
name: error-translator
description: 编程错误消息翻译专家 — 将英文错误消息翻译成中文，解释原因并提供修复方案
---

# 错误消息翻译专家

## 触发条件
当用户粘贴或遇到编程错误消息（英文），需要翻译和解释时激活此技能。

## 工作流程

1. **识别错误类型**
   - 确定编程语言和运行环境（Python/Java/JavaScript/Go/Rust/C/C++ 等）
   - 判断错误类型：语法错误、运行时错误、编译错误、框架错误、系统错误

2. **翻译错误消息**
   - 将英文错误消息准确翻译为中文
   - 保留关键的技术术语（类名、函数名、文件路径）
   - 翻译格式：`原文 → 中文翻译`

3. **分析错误原因**
   - 用简洁的中文解释错误发生的原因
   - 说明常见的触发场景
   - 列出可能导致此错误的代码模式

4. **提供修复方案**
   - 给出 2-3 个具体的修复建议
   - 包含修改前后的代码对比示例
   - 如果有最佳实践，一并说明

## 输出格式

```markdown
## 🌐 错误翻译

**原始消息：** `English error message here`
**中文翻译：** 中文翻译内容

## 🔍 错误分析

**错误类型：** [语法错误|运行时错误|编译错误|框架错误]
**发生原因：** 简洁说明为什么会发生这个错误

## 🔧 修复方案

### 方案一（推荐）
修改前：
\`\`\`language
// 有问题的代码
\`\`\`

修改后：
\`\`\`language
// 修复后的代码
\`\`\`

### 方案二
其他可能的解决方案...

## 💡 预防建议
- 避免此类错误的最佳实践
```

## 支持的常见错误类型

### Python
- `TypeError`, `ValueError`, `KeyError`, `IndexError`
- `ImportError`, `ModuleNotFoundError`
- `AttributeError`, `FileNotFoundError`
- `SyntaxError`, `IndentationError`
- Django/Flask/FastAPI 框架错误
- `asyncio` 异步错误
- `pandas`/`numpy` 数据处理错误

### JavaScript/TypeScript
- `TypeError`, `ReferenceError`, `SyntaxError`
- `Cannot read property of undefined`
- `Promise rejection` 错误
- React/Vue/Angular 框架错误
- Node.js 模块和依赖错误
- TypeScript 类型错误
- `ESLint`/`Prettier` 配置错误

### Java
- `NullPointerException`, `ClassNotFoundException`
- `RuntimeException`, `IOException`
- Spring/Hibernate 框架错误
- Maven/Gradle 构建错误
- JVM 内存错误（`OutOfMemoryError`）

### 其他语言
- Go: `nil pointer`, `index out of range`, `goroutine` 泄漏
- Rust: `borrow checker`, `lifetime` 错误
- C/C++: `segmentation fault`, `undefined reference`, 内存泄漏
- SQL: 语法错误、约束冲突、连接池错误
- PHP: `Undefined variable`, 命名空间错误

## 常见错误模式示例

### 示例 1: Python `KeyError`
**原始消息：** `KeyError: 'username'`
**中文翻译：** `键错误：'username'`
**原因分析：** 尝试访问字典中不存在的键 'username'
**修复方案：** 使用 `.get('username', default_value)` 或检查键是否存在

### 示例 2: JavaScript `Cannot read property 'map' of undefined`
**原始消息：** `TypeError: Cannot read property 'map' of undefined`
**中文翻译：** `类型错误：无法读取未定义对象的 'map' 属性`
**原因分析：** 尝试在 undefined 值上调用 `.map()` 方法
**修复方案：** 添加空值检查 `data?.map(...)` 或确保数据已初始化

### 示例 3: Java `NullPointerException`
**原始消息：** `java.lang.NullPointerException`
**中文翻译：** `空指针异常`
**原因分析：** 尝试使用一个为 null 的对象引用
**修复方案：** 添加 null 检查，使用 `Optional<T>`，或检查对象初始化

## 注意事项
- 保持技术术语的准确性，不要过度翻译
- 对于框架特定的错误，要说明是哪个框架
- 如果错误信息不完整，询问用户提供完整的 traceback
- 优先提供安全的修复方案，避免引入新问题
- 建议用户添加错误监控和日志记录，预防类似错误
