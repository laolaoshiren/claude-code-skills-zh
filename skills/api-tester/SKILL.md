---
name: api-tester
description: API 自动化测试 - OpenAPI 解析、测试用例生成、集成测试
---

# API 测试生成器

## 触发条件
当用户要求测试 API、生成测试用例、接口测试、集成测试时激活此技能。

## 工作流程

### 第 1 步：发现 API
按优先级查找 API 定义：
1. OpenAPI/Swagger 文件（`openapi.yaml`、`swagger.json`）
2. 路由定义文件（Express routes、Flask blueprints、Spring controllers）
3. API 目录结构（`/api/`、`/routes/`、`/controllers/`）

**OpenAPI 解析方法**：
```bash
# 使用 swagger-cli 验证
npx @apidevtools/swagger-cli validate openapi.yaml

# 使用 redocly 提取端点信息
npx @redocly/cli lint openapi.yaml

# 从 OpenAPI 提取所有路径
grep -E '^\s+/' openapi.yaml | awk '{print $2}'
```

### 第 2 步：生成测试用例
为每个 endpoint 生成三类测试：
- **正常场景**（happy path）— 合法输入，期望成功响应
- **边界值测试** — 空值、超长字符串、特殊字符、极值
- **错误场景** — 400/401/403/404/422/500

### 第 3 步：生成测试代码
根据项目技术栈选择测试框架并生成代码。

### 第 4 步：测试数据生成

**策略**：
| 策略 | 适用场景 | 工具/方法 |
|------|---------|----------|
| 固定数据 | 简单接口、确定性测试 | JSON fixture 文件 |
| Faker 随机生成 | 大量测试数据、压力测试 | `@faker-js/faker`、`Faker`(Python) |
| 工厂模式 | 复杂对象关系 | factory_boy、fishery |
| 从 Schema 生成 | 基于 OpenAPI 自动生成 | `json-schema-faker` |

## 测试模板

### pytest (Python)
```python
import pytest

# 正常场景
def test_get_users_success(client):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 边界值测试
def test_create_user_empty_name(client):
    response = client.post("/api/users", json={"name": ""})
    assert response.status_code == 422

# 认证测试
def test_get_users_unauthorized(client):
    response = client.get("/api/users", headers={})
    assert response.status_code == 401

# 参数化批量测试
@pytest.mark.parametrize("name,expected_status", [
    ("Alice", 200),
    ("", 422),
    ("a" * 500, 422),
    (None, 422),
])
def test_create_user_validation(client, name, expected_status):
    response = client.post("/api/users", json={"name": name})
    assert response.status_code == expected_status
```

### Jest (JavaScript/TypeScript)
```typescript
import request from 'supertest';
import app from '../src/app';

describe('GET /api/users', () => {
  it('应返回用户列表', async () => {
    const res = await request(app).get('/api/users');
    expect(res.status).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  it('未认证应返回 401', async () => {
    const res = await request(app).get('/api/users');
    expect(res.status).toBe(401);
  });
});

describe('POST /api/users', () => {
  it('空名称应返回 422', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: '' });
    expect(res.status).toBe(422);
  });

  it('有效数据应返回 201', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'Alice', email: 'alice@test.com' });
    expect(res.status).toBe(201);
    expect(res.body).toHaveProperty('id');
  });
});
```

### curl 测试脚本
```bash
#!/bin/bash
BASE_URL="http://localhost:3000/api"

# 正常请求
echo "=== GET /users ==="
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -H "Authorization: Bearer *** \
  "$BASE_URL/users"

# POST 创建资源
echo "=== POST /users ==="
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer *** \
  -d '{"name":"Alice","email":"alice@test.com"}' \
  "$BASE_URL/users"

# 错误场景 - 空 body
echo "=== POST /users (empty) ==="
curl -s -w "\nHTTP Status: %{http_code}\n" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  "$BASE_URL/users"
```

## 注意事项
- 测试用例应独立运行，不依赖执行顺序
- 使用 `beforeEach` 或 fixture 管理测试数据的初始化和清理
- 敏感信息（API Key、Token）使用环境变量，不要硬编码
- 集成测试建议使用独立的测试数据库
- 关注响应时间，添加超时断言
