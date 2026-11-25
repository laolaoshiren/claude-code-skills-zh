---
name: db-migrator
description: 数据库迁移助手，先识别项目 ORM/迁移框架并对比 Schema 变更，再生成可审查的迁移脚本、回滚方案与大表锁表风险评估。用于用户要求生成 migration、变更数据表结构、编写升级/回滚 SQL 或审查数据库迁移风险时；默认只生成和审查迁移脚本，不自动执行数据库变更，执行前必须确认环境、连接目标与备份。
---

# 数据库迁移助手

## 触发边界

- **适用**：对比模型/Schema 变更、生成各主流框架迁移脚本与回滚方案、评估大表 DDL 锁表与向后兼容性风险。
- **不适用**：慢查询索引剖析与运行时基准测试 → `perf-profiler`；源码 SQL 注入安全审计 → `security-audit`。

## 核心原则

1. **默认只生成与审查，不自动执行变更。** 未经用户明确确认目标环境、数据库连接、数据备份与维护窗口，严禁直接执行 `migrate`、`db push` 或手工 DDL。
2. **先读框架与已有迁移历史。** 沿用项目既有版本号格式、命名规范、目录结构与锁定的工具版本，不猜测数据库方言（MySQL / PostgreSQL / SQLite 等）。
3. **可逆性与数据安全优先。** 涉及删列、删表、收窄字段类型或不可逆数据清洗时，必须标注不可自动回滚风险及分阶段扩展-收缩（Expand & Contract）方案。

## 工作流程

### 第 1 步：识别迁移框架与数据库方言

读取项目配置与迁移目录，确认实际使用的工具链：

- **Python**：`alembic.ini` / `alembic/`（Alembic）；`manage.py` + `migrations/`（Django）
- **Node.js / TypeScript**：`prisma/schema.prisma`（Prisma）；`drizzle.config.*`（Drizzle）；`ormconfig.*` / `data-source.*`（TypeORM）
- **Java / JVM**：`pom.xml` / `build.gradle` 含 `flyway`（Flyway）或 `liquibase`（Liquibase）
- **Go**：`migrations/` 配合 `goose` 或 `golang-migrate`
- **Ruby**：`Gemfile` + `db/migrate/`（Rails ActiveRecord）

### 第 2 步：分析 Schema 变更与代码引用

- 对比最新模型定义与已有迁移历史，识别新增/修改/删除的表、列、默认值、非空约束、索引与外键。
- 若涉及**重命名或删除列/表**，先检索业务源码确认是否仍存在旧字段引用，避免上线窗口期间旧版本实例报错。

### 第 3 步：生成迁移与回滚脚本

- 按框架规范生成迁移文件（显式使用 UTF-8 编码写入，避免 Windows CP936 导致中文注释乱码）。
- 框架支持 `downgrade` / `down.sql` 时一并生成逆向逻辑；不支持或涉及破坏性删数据时，明确写出快照恢复或前向修复方案。

### 第 4 步：锁表与兼容性风险评估

逐项检查并在交付报告中标明：

- **大表 DDL 锁表风险**：如 MySQL `ALGORITHM=INPLACE/INSTANT`、`pt-online-schema-change` / `gh-ost`、PostgreSQL `CREATE INDEX CONCURRENTLY`（注意 `CONCURRENTLY` 不能在事务块内执行）。
- **新增非空列**：确认是否提供安全默认值，或拆分为「先可空 → 分批回填 → 再加 NOT NULL 约束」。
- **数据迁移分离**：大批量数据回填脚本与 DDL Schema 变更分开执行，避免长事务阻塞业务。

## 主流框架安全模板

### Alembic (Python)

```python
"""add email column to users

Revision ID: abc123
"""
from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column("users", sa.Column("email", sa.String(255), nullable=True))
    op.create_index("ix_users_email", "users", ["email"], unique=True)


def downgrade():
    op.drop_index("ix_users_email", table_name="users")
    op.drop_column("users", "email")
```

### Prisma (Node.js)

```bash
# 默认仅生成迁移 SQL 供审查，不直接改动数据库
npx prisma migrate dev --name add-email-to-users --create-only
```

人工审查生成的 SQL、确认数据库连接目标与备份后，再由用户授权执行：

```bash
# 开发环境应用迁移
npx prisma migrate dev

# 生产或测试环境应用已审核并提交的迁移
npx prisma migrate deploy
```

### Flyway / Liquibase (Java) 与 Go (goose / golang-migrate)

```sql
-- V2__add_email_to_users.sql（或 goose: +goose Up）
ALTER TABLE users ADD COLUMN email VARCHAR(255);
CREATE UNIQUE INDEX ix_users_email ON users(email);

-- 回滚脚本须单独审查（如 U2__rollback_add_email.sql 或 +goose Down）
```

### Django (Python)

```python
# users/migrations/0002_add_email.py
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.EmailField(unique=True, null=True),
        ),
    ]
```

> 提示：`unique=True` 已由 Django 自动创建唯一约束及索引，不要再重复添加普通索引。默认仅生成迁移文件或使用 `python manage.py sqlmigrate` 预览 SQL，确认后再执行 `migrate`。

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
# 1. 默认仅生成迁移文件供审查，不直接执行数据库变更
rails generate migration AddEmailToUsers

# 2. 审查生成的迁移代码、确认目标环境（RAILS_ENV）与数据库备份后，再经用户确认执行：
# rails db:migrate
# rails db:rollback STEP=1
```

## 回滚策略速查

| 变更场景 | 推荐回滚策略 |
|----------|--------------|
| 新增列 / 新增表 | 直接 drop 新增列或表（确认无新数据依赖） |
| 删除列 / 删除表 | 无法仅靠 DDL 还原数据，必须先备份并优先采用多阶段废弃 |
| 修改列类型 / 缩窄长度 | 存在截断或精度丢失风险，需先评估存量数据并保留备份 |
| 大表加索引 / 改结构 | 使用在线 DDL 或非阻塞索引语法，提前确认维护窗口 |

## 安全边界与注意事项

- 默认只生成和审查迁移脚本；执行前必须核实环境、连接串指向、备份状态与维护窗口。
- 严禁在迁移脚本或报告中硬编码真实数据库密码或连接凭据。
- 先在隔离的本地或 staging 环境验证升级与回滚路径，再应用到生产环境。
- 迁移版本由框架元数据表追踪，不要假设同一版本迁移可以脱离版本表任意重复执行。
