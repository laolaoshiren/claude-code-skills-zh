---
name: i18n-helper
description: 国际化/本地化助手 — 扫描代码中的硬编码文本、生成 i18n 配置、批量翻译
---

# 🌍 i18n-helper — 国际化/本地化助手

## 触发条件
当用户要求以下操作时激活此技能：
- 扫描代码中的硬编码中文/英文文本
- 为项目添加国际化支持（i18n）
- 批量提取和翻译语言文件
- 检查翻译完整性（缺失 key 检测）

## 工作流程

### 1. 项目分析
- 检测项目类型（React/Vue/Angular/Node.js/Python/Java 等）
- 识别已使用的 i18n 框架（react-intl, vue-i18n, i18next, gettext 等）
- 扫描源代码目录结构

### 2. 硬编码文本扫描
- 在 `.js/.jsx/.ts/.tsx/.vue/.py/.java/.go` 等文件中搜索硬编码字符串
- 排除：变量名、URL、正则表达式、import 路径、日志调试信息
- 标记：用户可见的 UI 文本、错误提示、通知消息

### 3. 语言文件生成
根据项目框架生成对应格式：
- **JSON** (i18next/react-intl): `{ "key": "value" }`
- **YAML** (vue-i18n): `key: value`
- **PO/POT** (gettext): 标准格式
- **Properties** (Java): `key=value`

### 4. 代码替换
- 将硬编码文本替换为 i18n 函数调用
- 保持原有格式和变量插值
- 示例：
  ```javascript
  // 替换前
  alert('保存成功');
  // 替换后
  alert(t('alert.saveSuccess'));
  ```

### 5. 完整性检查
- 对比主语言文件与翻译文件的 key 差异
- 输出缺失翻译的 key 列表
- 统计翻译完成度百分比

## 输出格式
```markdown
## 📊 i18n 扫描报告

### 硬编码文本
| 文件 | 行号 | 内容 | 建议 key |
|------|------|------|----------|
| src/App.tsx | 42 | '欢迎使用' | page.welcome |

### 语言文件
已生成 `locales/zh-CN.json` 和 `locales/en-US.json`

### 翻译完整性
- zh-CN: 45/45 (100%) ✅
- en-US: 42/45 (93.3%) ⚠️ 缺少 3 个 key
```

## 支持的 i18n 框架
- react-intl / FormatJS
- vue-i18n
- i18next / react-i18next / next-i18next
- Angular @ngx-translate
- Python gettext / Flask-Babel
- Java ResourceBundle / Spring MessageSource
- Go go-i18n

## 注意事项
- 不要翻译技术术语（API、SDK、HTTP 等）
- 保留变量占位符 `{name}` `{{count}}` `%s` 等格式
- 复数形式和性别变体需要特殊处理
- 日期、数字、货币格式需使用 locale 感知的格式化函数
