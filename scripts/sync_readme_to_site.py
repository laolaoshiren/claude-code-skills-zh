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

import re
import sys
import datetime
from pathlib import Path


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


# ── 工具函数 ───────────────────────────────────────────────────────────────────

def read_file(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def escape_js_string(s: str) -> str:
    """转义字符串用于嵌入 JS 单引号字符串"""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")


def extract_github_url(url: str) -> str:
    """从各种格式的 URL 中提取干净的 GitHub URL"""
    url = url.strip()
    if "gh-proxy.com" in url:
        m = re.search(r"github\.com/([^)]+)", url)
        if m:
            return f"https://github.com/{m.group(1)}"
    return url


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
        r"[（(]\s*([\d,.]+K?)\s*⭐\s*[）)]\s*$",   # （7.0K⭐）
        r"\s*⭐\s*([\d,.]+K?)\s*$",                  # ⭐ 7.0K
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


# ── 生成 JavaScript ───────────────────────────────────────────────────────────

def generate_skills_js(skills_data: dict[str, list[dict]]) -> str:
    """生成 skillsData JavaScript 对象代码"""
    lines = ["const skillsData = {"]

    category_order = ["star", "platform", "dev", "creative", "agent", "finance", "chinese"]

    for idx, key in enumerate(category_order):
        items = skills_data.get(key, [])
        lines.append(f"  {key}: [")

        for item in items:
            name = escape_js_string(item["name"])
            stars = escape_js_string(item.get("stars", ""))
            desc = escape_js_string(item["desc"])
            url = escape_js_string(item["url"])

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


def get_repo_stars(repo: str) -> int | None:
    """通过 gh CLI 获取仓库 star 数（已认证，不受限流）"""
    try:
        import subprocess
        result = subprocess.run(
            ["gh", "api", f"repos/{repo}", "--jq", ".stargazers_count"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            return int(result.stdout.strip())
        print(f"  ⚠️  gh CLI 获取 star 失败: {result.stderr[:100]}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ⚠️  获取 star 数失败: {e}", file=sys.stderr)
        return None


def update_html_stats(html: str, total_skills: int, repo_stars: int, total_original: int = 20) -> str:
    """更新 HTML 中的统计数字"""
    today = datetime.date.today().isoformat()

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
    today = datetime.date.today().isoformat()
    return re.sub(
        r'(<lastmod>)\d{4}-\d{2}-\d{2}(</lastmod>)',
        rf'\g<1>{today}\2',
        sitemap,
        count=1,
    )




def update_html_badges(html: str, total_skills: int, total_original: int, repo_stars: int) -> str:
    """更新 HTML 中 hero 区域的 badge 数字"""
    today = datetime.date.today().isoformat()
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
    new_html, count = re.subn(pattern, skills_js, html, flags=re.DOTALL)
    if count != 1:
        raise RuntimeError(f"skillsData 替换失败：期望 1 个数据块，实际找到 {count} 个")
    return new_html


def update_readme_badges(readme: str, total_skills: int, repo_stars: int) -> str:
    """更新 README.md 中的 badge 数字"""
    today = datetime.date.today().isoformat()

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

    total_skills = count_total_skills(skills_data)
    print(f"   找到 {total_skills} 个技能：")
    for key in ["star", "platform", "dev", "creative", "agent", "finance", "chinese"]:
        items = skills_data.get(key, [])
        print(f"     {key}: {len(items)} 个")

    # 3. 获取 GitHub star 数
    existing_repo_stars = extract_existing_repo_stars(html_content)
    if fetch_stars:
        print(f"⭐ 获取 {GITHUB_REPO} 的 star 数 ...")
        fetched_repo_stars = get_repo_stars(GITHUB_REPO)
        if fetched_repo_stars is None:
            if existing_repo_stars is None:
                raise RuntimeError("无法获取 GitHub Star，官网中也没有可回退的现有值")
            repo_stars = existing_repo_stars
            print(f"   ⚠️  获取失败，保留现有 Star 数: {repo_stars}")
        else:
            repo_stars = fetched_repo_stars
            print(f"   Star 数: {repo_stars}")
    else:
        if existing_repo_stars is None:
            raise RuntimeError("官网中没有可读取的 GitHub Star，请使用 --fetch-stars 获取")
        repo_stars = existing_repo_stars
        print(f"⭐ 使用现有 Star 数: {repo_stars}（使用 --fetch-stars 获取最新值）")

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
    print(f"   最近更新: {datetime.date.today().isoformat()}")


if __name__ == "__main__":
    main()
