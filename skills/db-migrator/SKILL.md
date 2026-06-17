---
name: db-migrator
description: 数据库迁移助手 - Schema 对比、迁移脚本生成
---

# 数据库迁移助手

## 触发条件
当用户要求数据库迁移、生成 migration、schema 变更、数据库升级时激活此技能。

## 工作流程

### 第 1 步：识别框架
扫描项目文件，判断使用的 ORM/迁移框架：
- `alembic.ini` / `alembic/` → Alembic
- `prisma/schema.prisma` → Prisma
- `pom.xml` 含 flyway → Flyway
- `manage.py` + `settings.py` → Django
- `Gemfile` + `db/migrate/` → Rails

### 第 2 步：分析 Schema 变更
- 对比 models 定义与现有迁移历史
- 识别新增/修改/删除的表和字段
- 检测索引、约束、外键变更

### 第 3 步：生成迁移脚本
根据框架生成对应的迁移文件，并同时生成回滚脚本。

### 第 4 步：风险评估
- 大表 DDL 变更（锁表风险）
- 数据迁移需求
- 向后兼容性

## 迁移模板

### Alembic (Python)
```python
"""add email column to users

Revision ID: abc123
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255), nullable=True))
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

def downgrade():
    op.drop_index('ix_users_email')
    op.drop_column('users', 'email')
```

### Flyway (Java)
```sql
-- V2__add_email_to_users.sql
ALTER TABLE users ADD COLUMN email VARCHAR(255);
CREATE UNIQUE INDEX ix_users_email ON users(email);

-- 回滚脚本 (单独文件 U2__rollback_add_email.sql)
-- 逆向操作
```

### Prisma (Node.js)
```prisma
// schema.prisma 变更
model User {
  id    Int     @id @default(autoincrement())
  name  String
  email String? @unique  // 新增字段
}
```
```bash
# 生成迁移
npx prisma migrate dev --name add-email-to-users
npx prisma migrate dev --name add-email-to-users --create-only  # 仅生成不执行
```

### Django (Python)
```python
# users/migrations/0002_add_email.py
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('users', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, null=True),
        ),
        migrations.RunSQL(
            sql='CREATE INDEX ix_users_email ON users(email);',
            reverse_sql='reverse_sql_here',
        ),
    ]
```

### Rails (Ruby)
```ruby
# db/migrate/20260617_add_email_to_users.rb
class AddEmailToUsers < ActiveRecord::Migration[7.0]
  def change
    add_column :users, :email, :string
    add_index :users, :email, unique: true
  end
end
```
```bash
rails db:migrate         # 执行迁移
rails db:rollback        # 回滚上一次
rails db:rollback STEP=3 # 回滚最近 3 次
```

## 回滚策略

| 场景 | 策略 |
|------|------|
| 新增列 | 直接移除该列 |
| 删除列 | 无法自动回滚，需提前备份数据 |
| 修改列类型 | 反向修改为原类型，注意数据丢失风险 |
| 新增表 | 移除该表 |
| 数据迁移 | 编写反向迁移脚本，保留原始数据快照 |
| 大表变更 | 使用在线 DDL 工具避免锁表 |

## 注意事项
- 总是生成 downgrade 回滚脚本
- 大表变更需考虑在线 DDL，避免长时间锁表
- 数据迁移与 schema 变更分开处理
- 迁移脚本必须幂等，可重复执行不出错
- 在 staging 环境验证后再应用到生产环境
- 涉及删除列/表的变更，确保应用代码已先移除相关引用
