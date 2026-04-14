---
name: db-migrator
description: 数据库迁移助手 - Schema 对比、迁移脚本生成
---

# 数据库迁移助手

## 触发条件
当用户要求数据库迁移、生成 migration、schema 变更、数据库升级时激活此技能。

## 工作流程

1. **分析 Schema** — 读取 models/ORM 定义或现有数据库结构
2. **对比差异** — 识别新增/修改/删除的表和字段
3. **生成迁移脚本** — 支持多种框架：
   - Alembic (Python)
   - Flyway (Java)
   - Prisma (Node.js)
   - Django migrations
   - Rails migrations

## 迁移模板

### Alembic
```python
def upgrade():
    op.add_column('users', sa.Column('email', sa.String(255)))
    op.create_index('ix_users_email', 'users', ['email'])

def downgrade():
    op.drop_index('ix_users_email')
    op.drop_column('users', 'email')
```

## 注意事项
- 总是生成 downgrade 回滚脚本
- 大表变更需考虑在线 DDL
- 数据迁移与 schema 变更分开
