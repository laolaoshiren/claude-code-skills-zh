#!/usr/bin/env python3
"""
sync_readme_to_site.py — 自动从 README.md 提取技能数据并同步到 docs/index.html

功能：
1. 解析 README.md 中所有分类表格
2. 生成 JavaScript skillsData 对象
3. 统计实际技能数量
4. 可选：获取 GitHub star 数（通过 API）
5. 更新 docs/index.html 中的数据和统计数字
6. 更新 sitemap 最近修改日期

用法：
    python scripts/sync_readme_to_site.py [--fetch-stars] [--dry-run]
"""

import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit


def _configure_stdio() -> None:
    """Avoid UnicodeEncodeError when Windows terminals use GBK/CP936."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(errors="replace")


_configure_stdio()

# ── 配置 ──────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parent.parent
README_PATH = REPO_ROOT / "README.md"
HTML_PATH = REPO_ROOT / "docs" / "index.html"
SITEMAP_PATH = REPO_ROOT / "docs" / "sitemap.xml"
GITHUB_REPO = "laolaoshiren/claude-code-skills-zh"
GITHUB_GRAPHQL_BATCH_SIZE = 50
CATEGORY_ORDER = [
    "star",
    "platform",
    "dev",
    "creative",
    "agent",
    "finance",
    "chinese",
]
PROJECT_TIMEZONE = datetime.timezone(datetime.timedelta(hours=8), name="Asia/Shanghai")


# ── 工具函数 ───────────────────────────────────────────────────────────────────

def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def current_project_date(now: datetime.datetime | None = None) -> datetime.date:
    """返回项目公开日期，固定使用中国标准时间，避免 CI 的 UTC 日期回退。"""
    current = now or datetime.datetime.now(datetime.timezone.utc)
    if current.tzinfo is None:
        raise ValueError("now 必须包含时区信息")
    return current.astimezone(PROJECT_TIMEZONE).date()


def escape_js_string(s: str) -> str:
    """转义字符串用于嵌入 HTML 内联 JS 单引号字符串。"""
    return (
        s.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace("\r\n", " ")
        .replace("\r", " ")
        .replace("\n", " ")
        .replace("<", "\\u003C")
        .replace(">", "\\u003E")
        .replace("&", "\\u0026")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def validate_http_url(url: str) -> str:
    """校验将写入公开页面的 URL：仅允许 http/https 且必须有 host。"""
    candidate = url.strip()
    try:
        parsed = urlsplit(candidate)
        hostname = parsed.hostname
    except ValueError as exc:
        raise ValueError(f"无法解析 URL: {url!r}") from exc

    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc or not hostname:
        raise ValueError(f"URL 必须使用 http/https 且包含 host: {url!r}")
    if any(char.isspace() or ord(char) < 0x20 for char in candidate):
        raise ValueError(f"URL 不得包含空白或控制字符: {url!r}")
    return candidate


def extract_github_url(url: str) -> str:
    """从各种格式的 URL 中提取干净的 GitHub URL"""
    url = url.strip()
    if "gh-proxy.com" in url:
        m = re.search(r"github\.com/([^)]+)", url)
        if m:
            return f"https://github.com/{m.group(1)}"
    return url


def extract_github_repo(url: str) -> str | None:
    """从 GitHub 仓库 URL 提取 owner/name；非 GitHub 或非仓库 URL 返回 None。"""
    try:
        parsed = urlsplit(validate_http_url(extract_github_url(url)))
    except ValueError:
        return None

    if (parsed.hostname or "").lower() not in {"github.com", "www.github.com"}:
        return None

    path_parts = [part for part in parsed.path.split("/") if part]
    if len(path_parts) < 2:
        return None

    owner = path_parts[0]
    name = path_parts[1]
    if name.endswith(".git"):
        name = name[:-4]
    if not owner or not name:
        return None
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", owner) or not re.fullmatch(
        r"[A-Za-z0-9_.-]+", name
    ):
        return None
    return f"{owner}/{name}"


def normalize_repo_slug(repo: str) -> str:
    """GitHub owner/name 大小写不敏感，内部统一用小写 key。"""
    owner, separator, name = repo.strip().partition("/")
    if (
        not separator
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", owner)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+", name)
    ):
        raise ValueError(f"非法 GitHub 仓库名: {repo!r}")
    return f"{owner}/{name}".lower()


def format_stars(stars: str) -> str:
    """统一星标格式"""
    if not stars:
        return ""
    stars = stars.strip().rstrip("+")
    if "K" in stars or "k" in stars:
        return stars + "+"
    try:
        num = float(stars.replace(",", ""))
        if num >= 1000:
            return f"{num/1000:.1f}K+".replace(".0K+", "K+")
        return stars
    except ValueError:
        return stars


def format_star_count(stars: int, *, popular: bool) -> str:
    """把数值 Star 格式化为 README 约定：热门列用 K+，其他分类用 K。"""
    if stars < 0:
        raise ValueError("Star 数不能为负数")
    if stars < 1000:
        return str(stars)

    value = f"{stars / 1000:.1f}".rstrip("0").rstrip(".")
    suffix = "K+" if popular else "K"
    return f"{value}{suffix}"


def classify_header(line: str) -> str | None:
    """
    根据 ### 标题行判断分类，返回 JS key 或 None
    """
    line = line.strip()
    # 必须是 ### 开头
    if not line.startswith("### "):
        return None

    # 热门技能：保留旧标题兼容，避免文案调整破坏同步
    if "🏆" in line and ("万星" in line or "热门与高潜" in line):
        return "star"
    # 平台运营
    if "平台运营" in line or "自媒体" in line:
        return "platform"
    # 开发效率：必须有 💻（避免与 🔥 热门原创混淆）
    if "💻" in line and "开发效率" in line:
        return "dev"
    # 内容创作
    if "🎨" in line and "内容创作" in line:
        return "creative"
    # 学术科研
    if "🔬" in line and "学术科研" in line:
        return "academic"
    # AI Agent
    if "🤖" in line and "Agent" in line:
        return "agent"
    # 金融/商业
    if "💰" in line and ("金融" in line or "商业" in line):
        return "finance"
    # 中文专属
    if "🌏" in line and "中文专属" in line:
        return "chinese"

    return None


def parse_stars_from_desc(desc: str) -> tuple[str, str]:
    """
    从描述末尾提取星标数，返回 (清理后的描述, 星标字符串)
    """
    patterns = [
        r"[（(]\s*([\d,.]+K?)\+?\s*⭐\s*[）)]\s*$",  # （7.0K⭐）
        r"\s*⭐\s*([\d,.]+K?)\+?\s*$",  # ⭐ 7.0K
    ]
    for pat in patterns:
        m = re.search(pat, desc)
        if m:
            stars = m.group(1).strip()
            clean_desc = desc[:m.start()].strip().rstrip("｜|")
            return clean_desc, stars
    return desc.strip(), ""


# ── 解析 README ────────────────────────────────────────────────────────────────

def parse_readme(readme_content: str) -> dict[str, list[dict]]:
    """
    解析 README.md 中所有分类表格，返回 {js_key: [skill_obj, ...]}
    学术科研 ('academic') 会映射到 'dev'
    """
    lines = readme_content.split("\n")
    sections: dict[str, list[list[str]]] = {}  # js_key → list of table rows
    current_key: str | None = None
    in_table = False

    for line in lines:
        stripped = line.strip()

        # 检查是否是目标分类标题
        header_key = classify_header(stripped)
        if header_key is not None:
            # 学术科研合并到 dev
            mapped_key = "dev" if header_key == "academic" else header_key
            current_key = mapped_key
            in_table = False
            sections.setdefault(current_key, [])
            continue

        # 遇到新的 ### 或 ## 标题，结束当前区域
        if stripped.startswith("## ") or (stripped.startswith("### ") and current_key is not None):
            if classify_header(stripped) is None:
                # 不是我们关心的标题，退出当前区域
                current_key = None
                in_table = False
                continue

        # 收集表格行
        if current_key is not None and stripped.startswith("|"):
            sections.setdefault(current_key, []).append(stripped)

    # 解析每个分类的表格
    result: dict[str, list[dict]] = {}
    for js_key, table_lines in sections.items():
        skills = parse_table(table_lines, js_key)
        if skills:
            result[js_key] = skills

    return result


def parse_table(table_lines: list[str], category: str) -> list[dict]:
    """解析 Markdown 表格行，提取技能数据"""
    skills = []
    for line in table_lines:
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c]
        if not cells:
            continue
        # 跳过表头和分隔行
        if any(kw in cells[0] for kw in ["技能", "说明", "---", "为什么"]):
            continue
        # 跳过没有链接的行
        if "[" not in cells[0]:
            continue
        skill = parse_skill_row(cells, category)
        if skill:
            skills.append(skill)
    return skills


def parse_skill_row(cells: list[str], category: str) -> dict | None:
    """解析一行表格数据，返回技能对象"""
    if len(cells) < 2:
        return None

    # 第一列：技能名和链接
    name_cell = cells[0]
    link_match = re.search(r"\[([^\]]+)\]\(([^)]+)\)", name_cell)
    if not link_match:
        return None

    name = link_match.group(1).strip()
    url = link_match.group(2).strip()
    url = extract_github_url(url)
    try:
        url = validate_http_url(url)
    except ValueError as exc:
        raise ValueError(f"技能 {name!r} 的 URL 非法: {url!r}") from exc

    # 第二列：描述
    desc_cell = cells[1].strip() if len(cells) > 1 else ""

    # 星标数
    stars = ""

    if category == "star" and len(cells) >= 3:
        # 明星技能：第三列是独立的星标数
        stars_raw = cells[2].strip() if len(cells) > 2 else ""
        stars = format_stars(stars_raw)
        # 清理描述中可能的内嵌星标
        desc_cell = re.sub(r"\s*[（(][\d,.]+K?\s*⭐\s*[）)]\s*$", "", desc_cell)
    else:
        # 其他分类：从描述末尾提取星标
        desc_cell, stars_raw = parse_stars_from_desc(desc_cell)
        stars = format_stars(stars_raw)

    desc = desc_cell.strip()
    if not name or not url:
        return None

    return {
        "name": name,
        "stars": stars,
        "desc": desc,
        "url": url,
    }


# ── GitHub Star 批量刷新 ──────────────────────────────────────────────────

def collect_github_repositories(
    skills_data: dict[str, list[dict]],
    extra_repositories: list[str] | None = None,
) -> list[str]:
    """收集精选分类中的 GitHub 仓库，并按 owner/name 大小写不敏感去重。"""
    repositories: dict[str, str] = {}

    for category in CATEGORY_ORDER:
        for item in skills_data.get(category, []):
            repo = extract_github_repo(item["url"])
            if repo is not None:
                repositories.setdefault(normalize_repo_slug(repo), repo)

    for repo in extra_repositories or []:
        repositories.setdefault(normalize_repo_slug(repo), repo)

    return list(repositories.values())


def _build_github_stars_query(repositories: list[str]) -> str:
    """为一批 owner/name 生成别名固定、可解析的 GraphQL 查询。"""
    lines = ["query RepositoryStars {"]
    for index, repo in enumerate(repositories):
        owner, name = repo.split("/", 1)
        lines.append(
            f"  r{index}: repository(owner: {json.dumps(owner)}, "
            f"name: {json.dumps(name)}) {{ stargazerCount }}"
        )
    lines.append("}")
    return "\n".join(lines)


def _repository_list_preview(repositories: list[str], limit: int = 8) -> str:
    preview = ", ".join(repositories[:limit])
    if len(repositories) > limit:
        preview += f" 等 {len(repositories)} 个仓库"
    return preview


def fetch_github_stars(
    repositories: list[str],
    batch_size: int = GITHUB_GRAPHQL_BATCH_SIZE,
) -> dict[str, int]:
    """
    通过 gh GraphQL 批量获取 Star。

    返回值的 key 是小写 owner/name。某批或某仓库失败时不伪造数值，
    只返回成功项，调用方因此会保留 README 旧值。
    """
    if batch_size <= 0:
        raise ValueError("batch_size 必须大于 0")

    unique_repositories: dict[str, str] = {}
    for repo in repositories:
        try:
            normalized = normalize_repo_slug(repo)
        except ValueError as exc:
            print(f"  ⚠️  {exc}，已跳过并保留 README 旧值", file=sys.stderr)
            continue
        unique_repositories.setdefault(normalized, repo)

    canonical_repositories = list(unique_repositories.values())
    fetched: dict[str, int] = {}

    for start in range(0, len(canonical_repositories), batch_size):
        batch = canonical_repositories[start:start + batch_size]
        query = _build_github_stars_query(batch)
        try:
            result = subprocess.run(
                ["gh", "api", "graphql", "-f", f"query={query}"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
            )
        except Exception as exc:
            print(
                "  ⚠️  gh GraphQL 批量查询异常，"
                f"保留 README 旧值：{_repository_list_preview(batch)}；{exc}",
                file=sys.stderr,
            )
            continue

        if result.returncode != 0:
            error = (result.stderr or result.stdout).strip().replace("\n", " ")[:300]
            print(
                "  ⚠️  gh GraphQL 批量查询失败，"
                "将继续解析 partial data，未返回的仓库保留 README 旧值："
                f"{_repository_list_preview(batch)}"
                f"{f'；{error}' if error else ''}",
                file=sys.stderr,
            )

        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            print(
                "  ⚠️  gh GraphQL 返回了非法 JSON，"
                f"保留 README 旧值：{_repository_list_preview(batch)}；{exc}",
                file=sys.stderr,
            )
            continue
        if not isinstance(payload, dict):
            print(
                "  ⚠️  gh GraphQL 返回的 JSON 不是对象，"
                f"保留 README 旧值：{_repository_list_preview(batch)}",
                file=sys.stderr,
            )
            continue

        errors = payload.get("errors")
        if errors:
            messages = "; ".join(
                str(error.get("message", error)) if isinstance(error, dict) else str(error)
                for error in errors
            )
            print(f"  ⚠️  gh GraphQL 返回部分错误：{messages[:500]}", file=sys.stderr)

        data = payload.get("data")
        if not isinstance(data, dict):
            print(
                "  ⚠️  gh GraphQL 缺少 data，"
                f"保留 README 旧值：{_repository_list_preview(batch)}",
                file=sys.stderr,
            )
            continue

        missing: list[str] = []
        for index, repo in enumerate(batch):
            node = data.get(f"r{index}")
            stars = node.get("stargazerCount") if isinstance(node, dict) else None
            if isinstance(stars, int) and not isinstance(stars, bool) and stars >= 0:
                fetched[normalize_repo_slug(repo)] = stars
            else:
                missing.append(repo)

        if missing:
            print(
                "  ⚠️  GraphQL 未返回有效 Star，"
                f"保留 README 旧值：{_repository_list_preview(missing)}",
                file=sys.stderr,
            )

    return fetched


def _replace_cell_value(cell: str, value: str) -> str:
    """替换 Markdown 单元格内容，保留原有左右空白。"""
    leading_length = len(cell) - len(cell.lstrip())
    trailing_length = len(cell) - len(cell.rstrip())
    leading = cell[:leading_length]
    trailing = cell[len(cell) - trailing_length:] if trailing_length else ""
    return f"{leading}{value}{trailing}"


def refresh_readme_stars(readme: str, star_counts: dict[str, int]) -> str:
    """仅更新 README 精选分类表格中成功获取的 GitHub Star。"""
    normalized_counts = {
        normalize_repo_slug(repo): stars
        for repo, stars in star_counts.items()
        if isinstance(stars, int) and not isinstance(stars, bool) and stars >= 0
    }
    if not normalized_counts:
        return readme

    current_category: str | None = None
    updated_lines: list[str] = []

    for line in readme.splitlines(keepends=True):
        body = line.rstrip("\r\n")
        line_ending = line[len(body):]
        stripped = body.strip()

        header_category = classify_header(stripped)
        if header_category is not None:
            current_category = "dev" if header_category == "academic" else header_category
        elif stripped.startswith("## ") or stripped.startswith("### "):
            current_category = None

        if current_category is not None and stripped.startswith("|"):
            cells = body.split("|")
            if len(cells) >= 4:
                link_match = re.search(r"\[[^\]]+\]\(([^)]+)\)", cells[1])
                repo = extract_github_repo(link_match.group(1)) if link_match else None
                stars = normalized_counts.get(normalize_repo_slug(repo)) if repo else None

                if stars is not None:
                    if current_category == "star" and len(cells) >= 5:
                        cells[3] = _replace_cell_value(
                            cells[3], format_star_count(stars, popular=True)
                        )
                    else:
                        description, _old_stars = parse_stars_from_desc(cells[2].strip())
                        formatted = format_star_count(stars, popular=False)
                        cells[2] = _replace_cell_value(
                            cells[2], f"{description}（{formatted}⭐）"
                        )
                    body = "|".join(cells)

        updated_lines.append(body + line_ending)

    return "".join(updated_lines)


# ── 生成 JavaScript ───────────────────────────────────────────────────────────

def generate_skills_js(skills_data: dict[str, list[dict]]) -> str:
    """生成 skillsData JavaScript 对象代码"""
    lines = ["const skillsData = {"]

    for key in CATEGORY_ORDER:
        items = skills_data.get(key, [])
        lines.append(f"  {key}: [")

        for item in items:
            name = escape_js_string(item["name"])
            stars = escape_js_string(item.get("stars", ""))
            desc = escape_js_string(item["desc"])
            url = escape_js_string(validate_http_url(item["url"]))

            parts = [f"name:'{name}'"]
            if stars:
                parts.append(f"stars:'{stars}'")
            parts.append(f"desc:'{desc}'")
            parts.append(f"url:'{url}'")

            # star 分类加 tag
            if key == "star":
                parts.append("tag:'star'")

            obj = "{" + ",".join(parts) + "},"
            lines.append(f"    {obj}")

        lines.append("  ],")

    lines.append("};")
    return "\n".join(lines)


# ── 更新 HTML ─────────────────────────────────────────────────────────────────

def count_total_skills(skills_data: dict[str, list[dict]]) -> int:
    """统计所有分类的技能总数（去重）"""
    seen_urls = set()
    for skills in skills_data.values():
        for s in skills:
            seen_urls.add(s["url"])
    return len(seen_urls)


def extract_existing_repo_stars(html: str) -> int | None:
    """从现有官网统计栏读取仓库 Star，供网络失败时安全回退。"""
    match = re.search(r'(<h3>)(\d+)(</h3>\s*<p>GitHub Stars</p>)', html)
    return int(match.group(2)) if match else None


def resolve_own_repo_stars(
    fetched_stars: dict[str, int], existing_repo_stars: int | None
) -> int:
    """优先使用同批 GraphQL 数据，失败时回退到官网现有值。"""
    fetched = fetched_stars.get(normalize_repo_slug(GITHUB_REPO))
    if isinstance(fetched, int) and not isinstance(fetched, bool) and fetched >= 0:
        return fetched
    if existing_repo_stars is None:
        raise RuntimeError(
            "批量查询未返回本仓库 Star，官网中也没有可回退的现有值"
        )

    print(
        f"   ⚠️  本仓库 Star 获取失败，安全回退为官网现有值: {existing_repo_stars}",
        file=sys.stderr,
    )
    return existing_repo_stars


def update_html_stats(html: str, total_skills: int, repo_stars: int, total_original: int = 20) -> str:
    """更新 HTML 中的统计数字"""
    today = current_project_date().isoformat()

    html = re.sub(
        r'(<h3>)\d+\+(</h3>\s*<p>精选技能</p>)',
        rf'\g<1>{total_skills}+\2',
        html
    )
    html = re.sub(
        r'(<h3>)\d+(</h3>\s*<p>原创技能</p>)',
        rf'\g<1>{total_original}\2',
        html
    )
    html = re.sub(
        r'(<h3>)\d+(</h3>\s*<p>GitHub Stars</p>)',
        rf'\g<1>{repo_stars}\2',
        html
    )
    html = re.sub(
        r'(<h3>)\d{4}-\d{2}-\d{2}(</h3>\s*<p>最近更新</p>)',
        rf'\g<1>{today}\2',
        html
    )
    return html


def update_sitemap_lastmod(sitemap: str) -> str:
    """更新 sitemap 中站点首页的最近修改日期。"""
    today = current_project_date().isoformat()
    return re.sub(
        r'(<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)',
        rf'\g<1>{today}\2',
        sitemap,
        count=1,
    )




def update_html_badges(html: str, total_skills: int, total_original: int, repo_stars: int) -> str:
    """更新 HTML 中 hero 区域的 badge 数字"""
    today = current_project_date().isoformat()
    # 先清理控制字符
    html = html.replace('', '')
    # 用字符串替换更新 badge
    import re
    patterns = [
        (r'✅ \d+\+[^<]*', f'✅ {total_skills}+ 精选技能'),
        (r'🎁 \d+[^<]*个原创技能', f'🎁 {total_original} 个原创技能'),
        (r'⭐ \d+ Stars', f'⭐ {repo_stars} Stars'),
        (r'🔄 更新于 \d{4}-\d{2}-\d{2}', f'🔄 更新于 {today}'),
    ]
    for pattern, replacement in patterns:
        m = re.search(pattern, html)
        if m:
            html = html.replace(m.group(), replacement)
    return html


def update_html_meta(html: str, total_skills: int, total_original: int) -> str:
    """更新 HTML head 中面向搜索和社交分享的描述文案"""
    replacements = {
        r'<meta name="description" content="[^"]*">':
            f'<meta name="description" content="最实用的 Claude Code Skills / Agents / Plugins 中文精选集，收录 {total_skills}+ 高质量技能、Agent 和插件，{total_original} 个原创技能，适合 Claude Code、Codex、Gemini CLI、Cursor 用户复制即装。">',
        r'<meta property="og:description" content="[^"]*">':
            f'<meta property="og:description" content="收录 {total_skills}+ Claude Code Skills / Agents / Plugins，按场景分类，中文说明，复制即装，持续更新。">',
        r'<meta name="twitter:description" content="[^"]*">':
            f'<meta name="twitter:description" content="{total_skills}+ 高质量 Claude Code 技能、Agent、插件中文精选，复制即装。">',
    }

    for pattern, replacement in replacements.items():
        html = re.sub(pattern, replacement, html, count=1)
    return html


def replace_skills_data(html: str, skills_js: str) -> str:
    """替换 HTML 中的 skillsData 对象"""
    pattern = r"const skillsData = \{.*?\};"
    # 使用函数替换，避免 JS 中的 \uXXXX 被 re 当作替换模板转义。
    new_html, count = re.subn(pattern, lambda _match: skills_js, html, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"skillsData 替换失败：期望 1 个数据块，实际找到 {count} 个")
    return new_html


def update_readme_badges(readme: str, total_skills: int, repo_stars: int) -> str:
    """更新 README.md 中的 badge 数字"""
    today = current_project_date().isoformat()

    readme = re.sub(
        r'skills-\d+%2B',
        f'skills-{total_skills}%2B',
        readme
    )
    readme = re.sub(
        r'精选 \d+\+',
        f'精选 {total_skills}+',
        readme
    )
    readme = re.sub(
        r'updated-\d{4}--\d{2}--\d{2}',
        f'updated-{today.replace("-", "--")}',
        readme
    )
    return readme


# ── 主逻辑 ─────────────────────────────────────────────────────────────────────

def main():
    fetch_stars = "--fetch-stars" in sys.argv
    dry_run = "--dry-run" in sys.argv

    print("🔄 sync_readme_to_site.py — 同步 README.md → docs/index.html")
    print()

    # 1. 读取文件
    print("📖 读取 README.md ...")
    readme_content = read_file(README_PATH)

    print("📖 读取 docs/index.html ...")
    html_content = read_file(HTML_PATH)

    print("📖 读取 docs/sitemap.xml ...")
    sitemap_content = read_file(SITEMAP_PATH)

    # 2. 解析 README 中的分类表格
    print("🔍 解析 README 分类表格 ...")
    skills_data = parse_readme(readme_content)

    # 3. 获取 GitHub star 数
    existing_repo_stars = extract_existing_repo_stars(html_content)
    if fetch_stars:
        repositories = collect_github_repositories(
            skills_data, extra_repositories=[GITHUB_REPO]
        )
        print(f"⭐ 通过 gh GraphQL 批量刷新 {len(repositories)} 个 GitHub 仓库 ...")
        fetched_stars = fetch_github_stars(repositories)
        readme_content = refresh_readme_stars(readme_content, fetched_stars)
        # 回写 Star 后重新解析，保证官网数据与 README 完全一致。
        skills_data = parse_readme(readme_content)
        print(f"   成功刷新 {len(fetched_stars)} / {len(repositories)} 个仓库")

        repo_stars = resolve_own_repo_stars(fetched_stars, existing_repo_stars)
        if normalize_repo_slug(GITHUB_REPO) in fetched_stars:
            print(f"   本仓库 Star 数: {repo_stars}")
    else:
        if existing_repo_stars is None:
            raise RuntimeError("官网中没有可读取的 GitHub Star，请使用 --fetch-stars 获取")
        repo_stars = existing_repo_stars
        print(f"⭐ 使用现有 Star 数: {repo_stars}（使用 --fetch-stars 获取最新值）")

    total_skills = count_total_skills(skills_data)
    print(f"   找到 {total_skills} 个技能：")
    for key in CATEGORY_ORDER:
        items = skills_data.get(key, [])
        print(f"     {key}: {len(items)} 个")

    # 4. 计算原创技能数量
    skills_root = REPO_ROOT / "skills"
    original_count = sum(
        1 for skill_dir in skills_root.iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").is_file()
    )

    # 5. 生成 JavaScript
    print("📝 生成 skillsData JavaScript ...")
    skills_js = generate_skills_js(skills_data)

    # 6. 更新 HTML
    print("🔧 更新 docs/index.html ...")
    new_html = replace_skills_data(html_content, skills_js)
    new_html = update_html_stats(new_html, total_skills, repo_stars, original_count)
    new_html = update_html_badges(new_html, total_skills, original_count, repo_stars)
    new_html = update_html_meta(new_html, total_skills, original_count)
    new_sitemap = update_sitemap_lastmod(sitemap_content)

    if dry_run:
        print("\n--- 预览 skillsData ---")
        print(skills_js[:2000])
        if len(skills_js) > 2000:
            print(f"  ... (共 {len(skills_js)} 字符)")
        print("\n✅ dry-run 完成，未写入文件")
        return

    # 7. 写入文件
    write_file(HTML_PATH, new_html)
    print(f"   ✅ 已写入 {HTML_PATH.relative_to(REPO_ROOT)}")

    write_file(SITEMAP_PATH, new_sitemap)
    print(f"   ✅ 已写入 {SITEMAP_PATH.relative_to(REPO_ROOT)}")

    # 8. 更新 README badges
    print("🔧 更新 README.md badges ...")
    new_readme = update_readme_badges(readme_content, total_skills, repo_stars)
    write_file(README_PATH, new_readme)
    print(f"   ✅ 已写入 {README_PATH.relative_to(REPO_ROOT)}")

    print()
    print("🎉 同步完成！")
    print(f"   精选技能: {total_skills}+")
    print(f"   GitHub Stars: {repo_stars}")
    print(f"   最近更新: {current_project_date().isoformat()}")


if __name__ == "__main__":
    main()
