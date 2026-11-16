---
name: specstream
description: 实时网页搜索、正文提取与多引擎兼容技能（SpecStream）。支持中文自然语言检索、网页正文提取（POST /v1/extract）、远程 MCP（https://api.specstream.ai/mcp），以及 Bocha、Tavily、Exa、Brave、Serper、SearXNG 现有客户端零改代码切换；未设置 SPECSTREAM_API_KEY 时可免费查询路由与引擎元数据，不阻塞现有项目。
---

# SpecStream 实时网页检索与正文提取

## 触发条件

当用户需要以下能力时启用：

- 在 Claude Code / Codex / Cursor 等客户端中检索实时网页、新闻、图片或公开文档内容。
- 提取指定公开网页的正文或结构化段落（`POST /v1/extract`）。
- 将项目中现有的 Bocha（博查）、Tavily、Exa、Brave Search、Serper 或 SearXNG 搜索客户端迁移到统一的兼容接口，而不想重写请求与解析代码。
- 接入远程 MCP 服务（`https://api.specstream.ai/mcp`）进行多源检索与结果核验。

不适用：需要登录态或内网权限的私有页面抓取、本地静态代码检索（应直接使用本地文件搜索）。

## 对中文用户的价值

1. **中文查询自动路由**：以中文提交查询且未显式指定 `language`/`country` 时，接口会按中文语境自动分发至表现稳定的对应搜索引擎；也可显式传入 `language=zh`、`country=CN` 或 `engines=-CN` 精确控制来源地区。
2. **国内/海外搜索生态零改代码迁移**：针对中文项目常用的 **Bocha Web Search**（`/bocha/v1/web-search`）以及海外常用的 **Tavily**、**Exa**、**Brave**、**Serper**、**SearXNG**、**Firecrawl**、**Jina Reader** 提供原样请求与响应兼容路由。只需修改 Base URL 与 Key 即可切换，fast 档统一按 $1 / 1,000 次搜索计费。
3. **无 Key 可先核对元数据与兼容路径**：`GET https://api.specstream.ai/v1/search-dialects` 与 `GET https://api.specstream.ai/v1/search-engines` 无需 API Key 且不计费；未设置 `SPECSTREAM_API_KEY` 时可先完成接口选型与客户端兼容检查，不影响本地其他功能运行。

## 前置条件与费用边界

- **可选环境变量**：`SPECSTREAM_API_KEY`（在控制台 `https://specstream.ai/workspace` 创建，或在交互会话中按官方 auth 文档流程签发；首次在浏览器登录新账号可获得一次性 $10 体验额度）。
- **无 Key 行为**：未配置 `SPECSTREAM_API_KEY` 时，仅允许执行只读元数据查询（`/v1/search-dialects`、`/v1/search-engines`）或生成迁移配置；不得擅自创建账号、绕过鉴权或发起扣费请求。
- **计费参考**：
  - Search API（`GET /v1/web-search`）：默认档 $5 / 1,000 次搜索（最多 10 条结果）；fast 档（`speed=fast`，及各 drop-in 兼容路由默认档位）$1 / 1,000 次搜索。未返回任何结果的调用不计费。
  - Extract API（`POST /v1/extract`）：$0.80 / 1,000 页，未提取到正文文本的页面不计费。
  - 无账号按次付费：支持通过 MPP（Stripe Link）或 x402（Base / Arbitrum / Polygon 上的 USDC）按单次请求付费，详见 `https://specstream.ai/agents.md`。
- **数据边界**：调用会将查询词或目标公开 URL 发送至 `https://api.specstream.ai`，请勿将密钥、内部主机地址或未授权私密链接传入查询与提取接口。

## 工作流程

### 1. 环境与 Key 检查

先确认当前环境是否已设置 `SPECSTREAM_API_KEY`（只检查存在性，禁止在终端、日志或报告中打印真实密钥值）：

```bash
test -n "${SPECSTREAM_API_KEY:-}" && echo "SPECSTREAM_API_KEY is set" || echo "SPECSTREAM_API_KEY is not set"
```

若未设置 Key：
1. 告知用户当前处于无 Key 状态，不会发起任何计费请求。
2. 如需核对兼容路由或可用搜索引擎，先调用无 Key 元数据接口；如需执行真实检索，请用户自行配置 `SPECSTREAM_API_KEY` 或确认改用 x402 按次支付。

### 2. 无 Key 元数据查询（免费，无需账号）

列出所有 drop-in 兼容路由、Key 传递位置及示例命令：

```bash
curl -sS https://api.specstream.ai/v1/search-dialects
```

查看可用搜索引擎及所在地区列表：

```bash
curl -sS https://api.specstream.ai/v1/search-engines
```

### 3. 实时搜索（Search API）

基础检索（fast 档，$1 / 1,000 次）：

```bash
curl -sS -G "https://api.specstream.ai/v1/web-search" \
  -H "Authorization: Bearer $SPECSTREAM_API_KEY" \
  --data-urlencode "q=中国大模型开源协议对比" \
  --data-urlencode "speed=fast" \
  --data-urlencode "num=10"
```

需要正文摘录时加上 `passages=true`；需要避免查询词出现在 URL 日志中时改用 `POST /v1/web-search`（JSON 请求体）；需要避免重复重试多扣费时附带 `Idempotency-Key` 请求头（最长 128 字符）。

常用检索参数：
- `q`：自然语言查询（1 至 2,000 字符），支持 `site:`、`-site:`、`filetype:`、`after:`/`before:`（`YYYY` / `YYYY-MM` / `YYYY-MM-DD`）与精确短语引号。
- `speed=fast`：使用快速档位（$1 / 1,000 次）。
- `passages=true`：附带各来源页面的相关正文片段（`sources[].excerpt` 与 `passages`）。
- `engines=-CN`：排除运行于中国大陆的引擎（也可在创建 Key 时通过 `engine_rule` 固定）。
- `news=true` / `images=true`：切换新闻或图片检索（按 fast 档计费）。

### 4. 网页正文提取（Extract API）

提取最多一批公开网页的文本内容（$0.80 / 1,000 页，空文本页面不计费）：

```bash
curl -sS -X POST "https://api.specstream.ai/v1/extract" \
  -H "Authorization: Bearer $SPECSTREAM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/article"]}'
```

### 5. 现有搜索客户端兼容迁移（Drop-in 路由）

以下路由保留原有客户端的请求与返回字段格式，默认走 fast 档计费（$1 / 1,000 次搜索）：

| 原有接口 | 替换后的 Base URL | Key 传递方式 | 最小请求路径 |
|---------|-------------------|-------------|-------------|
| Bocha（博查） | `https://api.specstream.ai/bocha` | `Authorization: Bearer $SPECSTREAM_API_KEY` | `POST /bocha/v1/web-search` |
| Tavily | `https://api.specstream.ai/tavily` | Bearer 或 body `api_key` | `POST /tavily/search` |
| Exa | `https://api.specstream.ai/exa` | `x-api-key` 或 Bearer | `POST /exa/search` |
| Brave Search | `https://api.specstream.ai` | `X-Subscription-Token` | `GET /res/v1/web/search` |
| Serper | `https://api.specstream.ai/serper` | `X-API-KEY` | `POST /serper/search` |
| SearXNG | `https://api.specstream.ai/searxng/<key>` | 路径、`key=`、`X-API-Key` 或 Bearer | `GET /searxng/search?q=...&format=json` |

Python SDK 示例（Tavily / Exa 仅替换 base URL）：

```python
from tavily import TavilyClient
client = TavilyClient(api_key=os.environ["SPECSTREAM_API_KEY"], api_base_url="https://api.specstream.ai/tavily")
```

```python
from exa_py import Exa
exa = Exa(api_key=os.environ["SPECSTREAM_API_KEY"], base_url="https://api.specstream.ai/exa")
```

### 6. 远程 MCP 接入

SpecStream 提供 Streamable HTTP 远程 MCP 端点 `https://api.specstream.ai/mcp`，支持 OAuth 登录或 Bearer API Key：

```bash
claude mcp add --transport http specstream https://api.specstream.ai/mcp \
  --header "Authorization: Bearer $SPECSTREAM_API_KEY"
```

连接后先通过 `tools/list` 查看可用工具（包括 `search_web`、`list_web_searches`、`get_web_search` 等），其中历史查询接口（`GET /v1/web-search/answers` 等）免费只读。

## 输出规范

向用户汇报检索或提取结果时：

- 每条关键结论必须附带返回的 `url` 与读取时间（如 `seen_at` / `published`），不脱离来源自行补全事实。
- 区分免费元数据检查结果与已发生的付费接口调用；如响应包含 `price_usd` 或 `request_id`，可一并说明供核对成本。
- 完整接口规范与错误码参考 `https://specstream.ai/agents.md`。
