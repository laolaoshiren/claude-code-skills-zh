---
name: test-generator
description: 自动生成单元测试：识别函数逻辑、覆盖边界条件、生成可运行测试代码
---

# 测试生成器

## 触发条件
当用户要求"生成测试"、"写单元测试"、"为 XX 函数写测试"、"增加测试覆盖率"时激活此技能。

## 工作流程

### 1. 分析目标代码
- 读取目标文件，识别函数/类的输入输出
- 分析参数类型、返回值、副作用
- 识别依赖关系（数据库、API、文件系统等）

### 2. 确定测试策略
- **纯函数**：参数化测试，覆盖正常/边界/异常输入
- **类方法**：测试初始化、正常调用、状态变化
- **异步函数**：测试成功路径、超时、网络错误
- **含副作用的函数**：使用 mock/stub 隔离依赖

### 3. 生成测试用例
每个函数至少覆盖：
- ✅ 正常输入（happy path）
- ⚠️ 边界条件（空值、零值、极大值、空字符串/数组）
- ❌ 异常输入（类型错误、格式错误）
- 🔗 依赖失败（网络超时、数据库异常）

### 4. 输出格式
根据项目语言和测试框架生成对应代码：

#### Python (pytest)
```python
import pytest
from mymodule import my_function

class TestMyFunction:
    def test_normal_input(self):
        assert my_function("hello") == "HELLO"
    
    def test_empty_string(self):
        assert my_function("") == ""
    
    def test_none_input(self):
        with pytest.raises(TypeError):
            my_function(None)
    
    def test_special_characters(self):
        assert my_function("你好!@#") == "你好!@#"
```

#### JavaScript (Jest)
```javascript
const { myFunction } = require('./mymodule');

describe('myFunction', () => {
  test('正常输入', () => {
    expect(myFunction('hello')).toBe('HELLO');
  });
  
  test('空字符串', () => {
    expect(myFunction('')).toBe('');
  });
  
  test('null 输入', () => {
    expect(() => myFunction(null)).toThrow(TypeError);
  });
});
```

#### Go (testing)
```go
package mypackage

import "testing"

func TestMyFunction(t *testing.T) {
    tests := []struct {
        name  string
        input string
        want  string
    }{
        {"正常输入", "hello", "HELLO"},
        {"空字符串", "", ""},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            if got := MyFunction(tt.input); got != tt.want {
                t.Errorf("MyFunction(%q) = %q, want %q", tt.input, got, tt.want)
            }
        })
    }
}
```

## 测试命名规范
- 中文项目：`test_函数名_场景描述` 或 `函数名_正常输入/边界条件/异常输入`
- 英文项目：遵循项目现有命名风格

## 最佳实践
1. **先读再写**：理解代码逻辑后再生成测试，不要盲目覆盖
2. **独立性**：每个测试独立运行，不依赖执行顺序
3. **可读性**：测试名即文档，一看就知道测什么
4. **适度 mock**：外部依赖必须 mock，内部逻辑尽量不 mock
5. **渐进式**：先覆盖核心路径，再补充边界条件
