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
import os
import re
import stat
import subprocess
import sys
import tempfile
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
SITE_HOME_URL = "https://claude-skills.bt199.com/"
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
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def _replace_exact(
    content: str,
    pattern: str,
    replacement,
    label: str,
    *,
    flags: int = 0,
) -> str:
    """严格替换唯一锚点；缺失或重复都拒绝继续写入。"""
    updated, count = re.subn(pattern, replacement, content, flags=flags)
    if count != 1:
        raise RuntimeError(f"{label} 替换失败：期望 1 处，实际找到 {count} 处")
    return updated


def _write_temp_bytes(path: Path, content: bytes, suffix: str, mode: int) -> Path:
    """在目标同目录落临时文件，保证 os.replace 不跨文件系统。"""
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=suffix,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary_path, mode)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise
    return temporary_path


def write_file_bundle(outputs: dict[Path, str]) -> list[Path]:
    """
    以可回滚 bundle 写入文件。

    未变化的文件不会创建临时文件或调用 ``os.replace``。所有新文件和备份
    都位于目标同目录；替换中途失败时，已替换目标会按逆序恢复。
    """
    changed: list[tuple[Path, bytes, bytes, int]] = []
    for raw_path, content in outputs.items():
        path = Path(raw_path)
        original = path.read_bytes()
        proposed = content.encode("utf-8")
        if proposed != original:
            mode = stat.S_IMODE(path.stat().st_mode)
            changed.append((path, original, proposed, mode))

    if not changed:
        return []

    staged: dict[Path, Path] = {}
    backups: dict[Path, Path] = {}
    replaced: list[Path] = []
    try:
        for path, original, proposed, mode in changed:
            staged[path] = _write_temp_bytes(path, proposed, ".new.tmp", mode)
            backups[path] = _write_temp_bytes(path, original, ".backup.tmp", mode)

        for path, _original, _proposed, _mode in changed:
            os.replace(staged[path], path)
            replaced.append(path)
    except Exception as exc:
        rollback_errors: list[str] = []
        for path in reversed(replaced):
            try:
                os.replace(backups[path], path)
            except Exception as rollback_exc:  # pragma: no cover - 极端磁盘故障
                rollback_errors.append(f"{path}: {rollback_exc}")
        if rollback_errors:
            raise RuntimeError(
                "同步写入失败，且部分文件回滚失败：" + "; ".join(rollback_errors)
            ) from exc
        raise
    finally:
        for temporary_path in [*staged.values(), *backups.values()]:
            temporary_path.unlink(missing_ok=True)

    return [path for path, _original, _proposed, _mode in changed]


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
    matches = list(re.finditer(r'<h3>(\d+)</h3>\s*<p>GitHub Stars</p>', html))
    if len(matches) > 1:
        raise RuntimeError(
            f"官网 GitHub Stars 统计锚点重复：期望至多 1 处，实际找到 {len(matches)} 处"
        )
    return int(matches[0].group(1)) if matches else None


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


def _resolve_public_date(project_date: datetime.date | None) -> datetime.date:
    return project_date if project_date is not None else current_project_date()


def update_html_stats(
    html: str,
    total_skills: int,
    repo_stars: int,
    total_original: int = 20,
    *,
    project_date: datetime.date | None = None,
    update_date: bool = True,
) -> str:
    """更新 HTML 中的统计数字"""
    html = _replace_exact(
        html,
        r'(<h3>)\d+\+(</h3>\s*<p>精选技能</p>)',
        lambda match: f"{match.group(1)}{total_skills}+{match.group(2)}",
        "HTML 精选技能统计",
    )
    html = _replace_exact(
        html,
        r'(<h3>)\d+(</h3>\s*<p>原创技能</p>)',
        lambda match: f"{match.group(1)}{total_original}{match.group(2)}",
        "HTML 原创技能统计",
    )
    html = _replace_exact(
        html,
        r'(<h3>)\d+(</h3>\s*<p>GitHub Stars</p>)',
        lambda match: f"{match.group(1)}{repo_stars}{match.group(2)}",
        "HTML GitHub Stars 统计",
    )
    today = _resolve_public_date(project_date).isoformat() if update_date else None
    html = _replace_exact(
        html,
        r'(<h3>)\d{4}-\d{2}-\d{2}(</h3>\s*<p>最近更新</p>)',
        (
            (lambda match: f"{match.group(1)}{today}{match.group(2)}")
            if update_date
            else (lambda match: match.group(0))
        ),
        "HTML 最近更新统计",
    )
    return html


def _find_sitemap_homepage_block(sitemap: str) -> re.Match[str]:
    """返回 sitemap 唯一首页 URL 块。"""
    url_matches = list(re.finditer(r"<url(?:\s[^>]*)?>.*?</url>", sitemap, re.DOTALL))
    homepage_blocks: list[re.Match[str]] = []
    homepage_pattern = re.compile(
        rf"<loc>\s*{re.escape(SITE_HOME_URL)}\s*</loc>"
    )
    for match in url_matches:
        if homepage_pattern.search(match.group(0)):
            homepage_blocks.append(match)

    if len(homepage_blocks) != 1:
        raise RuntimeError(
            "sitemap 首页 URL 锚点校验失败："
            f"期望 1 个 {SITE_HOME_URL}，实际找到 {len(homepage_blocks)} 个"
        )

    block_match = homepage_blocks[0]
    block = block_match.group(0)
    if len(homepage_pattern.findall(block)) != 1:
        raise RuntimeError("sitemap 首页 URL 块中的 loc 必须恰好出现 1 次")
    return block_match


def update_sitemap_lastmod(
    sitemap: str,
    *,
    project_date: datetime.date | None = None,
    update_date: bool = True,
) -> str:
    """只更新 sitemap 中首页 URL 的 lastmod，并严格校验唯一锚点。"""
    block_match = _find_sitemap_homepage_block(sitemap)
    block = block_match.group(0)

    today = _resolve_public_date(project_date).isoformat() if update_date else None
    updated_block = _replace_exact(
        block,
        r'(<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)',
        (
            (lambda match: f"{match.group(1)}{today}{match.group(2)}")
            if update_date
            else (lambda match: match.group(0))
        ),
        "sitemap 首页 lastmod",
    )
    return sitemap[:block_match.start()] + updated_block + sitemap[block_match.end():]


def _extract_unique_date(content: str, pattern: str, label: str) -> str:
    matches = re.findall(pattern, content)
    if len(matches) != 1:
        raise RuntimeError(f"{label} 日期校验失败：期望 1 处，实际找到 {len(matches)} 处")
    raw_date = matches[0]
    normalized = raw_date.replace("--", "-")
    try:
        datetime.date.fromisoformat(normalized)
    except ValueError as exc:
        raise RuntimeError(f"{label} 日期非法：{raw_date}") from exc
    return normalized


def validate_public_dates(readme: str, html: str, sitemap: str) -> str:
    """确认 README、HTML 两处与 sitemap 首页公开日期完全一致。"""
    homepage_block = _find_sitemap_homepage_block(sitemap).group(0)
    public_dates = {
        "README Updated badge": _extract_unique_date(
            readme,
            r'https://img\.shields\.io/badge/updated-(\d{4}--\d{2}--\d{2})-brightgreen\.svg',
            "README Updated badge",
        ),
        "HTML 最近更新统计": _extract_unique_date(
            html,
            r'<h3>(\d{4}-\d{2}-\d{2})</h3>\s*<p>最近更新</p>',
            "HTML 最近更新统计",
        ),
        "HTML Hero 更新 badge": _extract_unique_date(
            html,
            r'<span class="badge orange">🔄 更新于 (\d{4}-\d{2}-\d{2})</span>',
            "HTML Hero 更新 badge",
        ),
        "sitemap 首页 lastmod": _extract_unique_date(
            homepage_block,
            r'<lastmod>(\d{4}-\d{2}-\d{2})</lastmod>',
            "sitemap 首页 lastmod",
        ),
    }
    if len(set(public_dates.values())) != 1:
        detail = "，".join(f"{label}={value}" for label, value in public_dates.items())
        raise RuntimeError(f"公开日期不一致，拒绝自动同步：{detail}")
    return next(iter(public_dates.values()))




def update_html_badges(
    html: str,
    total_skills: int,
    total_original: int,
    repo_stars: int,
    *,
    project_date: datetime.date | None = None,
    update_date: bool = True,
) -> str:
    """更新 HTML 中 hero 区域的 badge 数字"""
    # 先清理控制字符
    html = html.replace('', '')
    today = _resolve_public_date(project_date).isoformat() if update_date else None
    replacements = [
        (
            r'(<span class="badge green">)✅ \d+\+ 精选技能(</span>)',
            lambda match: f"{match.group(1)}✅ {total_skills}+ 精选技能{match.group(2)}",
            "HTML Hero 精选技能 badge",
        ),
        (
            r'(<span class="badge purple">)🎁 \d+ 个原创技能(</span>)',
            lambda match: f"{match.group(1)}🎁 {total_original} 个原创技能{match.group(2)}",
            "HTML Hero 原创技能 badge",
        ),
        (
            r'(<span class="badge orange">)⭐ \d+ Stars(</span>)',
            lambda match: f"{match.group(1)}⭐ {repo_stars} Stars{match.group(2)}",
            "HTML Hero GitHub Stars badge",
        ),
        (
            r'(<span class="badge orange">)🔄 更新于 \d{4}-\d{2}-\d{2}(</span>)',
            (
                (lambda match: f"{match.group(1)}🔄 更新于 {today}{match.group(2)}")
                if update_date
                else (lambda match: match.group(0))
            ),
            "HTML Hero 更新日期 badge",
        ),
    ]
    for pattern, replacement, label in replacements:
        html = _replace_exact(html, pattern, replacement, label)
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
        html = _replace_exact(
            html,
            pattern,
            lambda _match, value=replacement: value,
            f"HTML meta {pattern}",
        )
    return html


def _detect_newline_style(content: str, label: str) -> str | None:
    """识别唯一换行风格；混用 CRLF、LF 或 CR 时拒绝自动替换。"""
    without_crlf = content.replace("\r\n", "")
    styles = []
    if "\r\n" in content:
        styles.append("\r\n")
    if "\n" in without_crlf:
        styles.append("\n")
    if "\r" in without_crlf:
        styles.append("\r")
    if len(styles) > 1:
        raise RuntimeError(f"{label} 混用了多种换行符，拒绝自动同步")
    return styles[0] if styles else None


def replace_skills_data(html: str, skills_js: str) -> str:
    """替换 HTML 中的 skillsData 对象，并保留目标数据块的换行风格。"""
    pattern = r"const skillsData = \{.*?\};"

    def render_replacement(match: re.Match[str]) -> str:
        newline = (
            _detect_newline_style(match.group(0), "skillsData 数据块")
            or _detect_newline_style(html, "HTML")
            or "\n"
        )
        normalized = skills_js.replace("\r\n", "\n").replace("\r", "\n")
        return normalized.replace("\n", newline)

    # 使用函数替换，避免 JS 中的 \uXXXX 被 re 当作替换模板转义。
    new_html, count = re.subn(pattern, render_replacement, html, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"skillsData 替换失败：期望 1 个数据块，实际找到 {count} 个")
    return new_html


def update_readme_badges(
    readme: str,
    total_skills: int,
    repo_stars: int,
    *,
    project_date: datetime.date | None = None,
    update_date: bool = True,
) -> str:
    """更新 README badge 与首屏精选数量，并严格校验唯一锚点。"""
    del repo_stars  # README 使用 GitHub 动态 Star badge，不写死仓库 Star。
    readme = _replace_exact(
        readme,
        r'(https://img\.shields\.io/badge/skills-)\d+(%2B-green\.svg)',
        lambda match: f"{match.group(1)}{total_skills}{match.group(2)}",
        "README Skills badge",
    )
    readme = _replace_exact(
        readme,
        r'(?m)^(> 🚀 .*?\| 精选 )\d+(\+ \|.*)$',
        lambda match: f"{match.group(1)}{total_skills}{match.group(2)}",
        "README 首屏精选数量",
    )
    today = _resolve_public_date(project_date).isoformat() if update_date else None
    readme = _replace_exact(
        readme,
        r'(https://img\.shields\.io/badge/updated-)\d{4}--\d{2}--\d{2}(-brightgreen\.svg)',
        (
            (
                lambda match: (
                    f"{match.group(1)}{today.replace('-', '--')}{match.group(2)}"
                )
            )
            if update_date
            else (lambda match: match.group(0))
        ),
        "README Updated badge",
    )
    return readme


def build_sync_outputs(
    readme_content: str,
    html_content: str,
    sitemap_content: str,
    *,
    proposed_readme_content: str | None = None,
    skills_js: str,
    total_skills: int,
    repo_stars: int,
    total_original: int,
    project_date: datetime.date,
) -> tuple[str, str, str, bool]:
    """先生成并校验非日期结果，仅在有实质变化时统一推进公开日期。"""
    readme_source = (
        proposed_readme_content
        if proposed_readme_content is not None
        else readme_content
    )
    html_without_date = replace_skills_data(html_content, skills_js)
    html_without_date = update_html_stats(
        html_without_date,
        total_skills,
        repo_stars,
        total_original,
        update_date=False,
    )
    html_without_date = update_html_badges(
        html_without_date,
        total_skills,
        total_original,
        repo_stars,
        update_date=False,
    )
    html_without_date = update_html_meta(
        html_without_date, total_skills, total_original
    )
    readme_without_date = update_readme_badges(
        readme_source,
        total_skills,
        repo_stars,
        update_date=False,
    )
    # 即使最终 no-op，也要先验证首页锚点和 lastmod 唯一性。
    update_sitemap_lastmod(sitemap_content, update_date=False)
    validate_public_dates(readme_without_date, html_without_date, sitemap_content)

    material_changed = (
        html_without_date != html_content or readme_without_date != readme_content
    )
    if not material_changed:
        return readme_content, html_content, sitemap_content, False

    new_html = update_html_stats(
        html_without_date,
        total_skills,
        repo_stars,
        total_original,
        project_date=project_date,
    )
    new_html = update_html_badges(
        new_html,
        total_skills,
        total_original,
        repo_stars,
        project_date=project_date,
    )
    new_readme = update_readme_badges(
        readme_without_date,
        total_skills,
        repo_stars,
        project_date=project_date,
    )
    new_sitemap = update_sitemap_lastmod(
        sitemap_content,
        project_date=project_date,
    )
    validate_public_dates(new_readme, new_html, new_sitemap)
    return new_readme, new_html, new_sitemap, True


# ── 主逻辑 ─────────────────────────────────────────────────────────────────────

def main():
    fetch_stars = "--fetch-stars" in sys.argv
    dry_run = "--dry-run" in sys.argv
    project_date = current_project_date()

    print("🔄 sync_readme_to_site.py — 同步 README.md → docs/index.html")
    print()

    # 1. 读取文件
    print("📖 读取 README.md ...")
    original_readme_content = read_file(README_PATH)
    readme_content = original_readme_content

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

    # 6. 先在内存生成并严格校验三文件结果。
    print("🔧 在内存生成并校验 README、官网与 sitemap ...")
    new_readme, new_html, new_sitemap, material_changed = build_sync_outputs(
        original_readme_content,
        html_content,
        sitemap_content,
        proposed_readme_content=readme_content,
        skills_js=skills_js,
        total_skills=total_skills,
        repo_stars=repo_stars,
        total_original=original_count,
        project_date=project_date,
    )

    if dry_run:
        print("\n--- 预览 skillsData ---")
        print(skills_js[:2000])
        if len(skills_js) > 2000:
            print(f"  ... (共 {len(skills_js)} 字符)")
        state = "存在实质变化" if material_changed else "无实质变化"
        print(f"\n✅ dry-run 完成（{state}），未写入文件")
        return

    # 7. 同目录临时文件 + os.replace 组成可回滚 bundle；未变化文件自动跳过。
    changed_paths = write_file_bundle(
        {
            README_PATH: new_readme,
            HTML_PATH: new_html,
            SITEMAP_PATH: new_sitemap,
        }
    )
    if changed_paths:
        for changed_path in changed_paths:
            print(f"   ✅ 已写入 {changed_path.relative_to(REPO_ROOT)}")
    else:
        print("   ✅ 无实质变化，所有文件保持原字节")

    print()
    print("🎉 同步完成！")
    print(f"   精选技能: {total_skills}+")
    print(f"   GitHub Stars: {repo_stars}")
    public_date = project_date.isoformat() if material_changed else "保持不变"
    print(f"   最近更新: {public_date}")


if __name__ == "__main__":
    main()
