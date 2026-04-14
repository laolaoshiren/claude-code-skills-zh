---
name: api-tester
description: API 自动化测试 - OpenAPI 解析、测试用例生成、集成测试
---

# API 测试生成器

## 触发条件
当用户要求测试 API、生成测试用例、接口测试、集成测试时激活此技能。

## 工作流程

1. **发现 API** — 查找 OpenAPI/Swagger 文件、路由定义
2. **生成测试用例** — 为每个 endpoint 生成：
   - 正常场景测试（happy path）
   - 边界值测试（空值、超长、特殊字符）
   - 错误场景测试（400/401/403/404/500）
3. **生成测试代码** — 支持 pytest / jest / curl

## 测试模板

### 正常测试
```python
def test_get_users_success(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### 边界测试
```python
def test_create_user_empty_name(client):
    response = client.post("/api/users", json={"name": ""})
    assert response.status_code == 422
```
