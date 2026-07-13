#!/usr/bin/env python3
"""Regression tests for sync_readme_to_site.py."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import datetime
from pathlib import Path

import sync_readme_to_site


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync_readme_to_site.py"


def test_dry_run_works_with_gbk_stdout() -> None:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "gbk"

    result = subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--dry-run"],
        cwd=REPO_ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="gbk",
        errors="replace",
        timeout=30,
    )

    assert result.returncode == 0, (
        "sync_readme_to_site.py --dry-run should not crash when stdout uses GBK.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
    assert "UnicodeEncodeError" not in result.stderr


def test_update_html_meta_refreshes_public_counts() -> None:
    html = """<meta name="description" content="收录 329+ 高质量技能、Agent 和插件，20 个原创技能。">
<meta property="og:description" content="收录 200+ Claude Code Skills / Agents / Plugins，按场景分类，中文说明，复制即装，持续更新。">
<meta name="twitter:description" content="200+ 高质量 Claude Code 技能、Agent、插件中文精选，复制即装。">"""

    updated = sync_readme_to_site.update_html_meta(html, total_skills=345, total_original=19)

    assert "收录 345+ 高质量技能、Agent 和插件，19 个原创技能" in updated
    assert "收录 345+ Claude Code Skills / Agents / Plugins" in updated
    assert "345+ 高质量 Claude Code 技能、Agent、插件中文精选" in updated
    assert "329+" not in updated
    assert "200+" not in updated
    assert "20 个原创技能" not in updated


def test_hot_skills_header_is_stable_after_copy_change() -> None:
    assert sync_readme_to_site.classify_header("### 🏆 热门与高潜技能") == "star"
    assert sync_readme_to_site.classify_header("### 🏆 明星技能（万星以上）") == "star"


def test_update_html_badges_refreshes_update_date() -> None:
    html = """<span class="badge green">✅ 339+ 精选技能</span>
<span class="badge purple">🎁 19 个原创技能</span>
<span class="badge orange">⭐ 425 Stars</span>
<span class="badge orange">🔄 更新于 2026-06-23</span>"""

    updated = sync_readme_to_site.update_html_badges(
        html,
        total_skills=349,
        total_original=19,
        repo_stars=513,
    )
    today = datetime.date.today().isoformat()

    assert "✅ 349+ 精选技能" in updated
    assert "⭐ 513 Stars" in updated
    assert f"🔄 更新于 {today}" in updated
    assert "2026-06-23" not in updated


def test_update_html_stats_refreshes_original_count() -> None:
    html = """<h3>339+</h3><p>精选技能</p>
<h3>20</h3><p>原创技能</p>
<h3>425</h3><p>GitHub Stars</p>
<h3>2026-06-23</h3><p>最近更新</p>"""

    updated = sync_readme_to_site.update_html_stats(
        html,
        total_skills=349,
        total_original=19,
        repo_stars=513,
    )
    today = datetime.date.today().isoformat()

    assert "<h3>349+</h3><p>精选技能</p>" in updated
    assert "<h3>19</h3><p>原创技能</p>" in updated
    assert "<h3>513</h3><p>GitHub Stars</p>" in updated
    assert f"<h3>{today}</h3><p>最近更新</p>" in updated
    assert "<h3>20</h3><p>原创技能</p>" not in updated


def test_existing_star_count_is_used_only_when_present() -> None:
    html = "<h3>529</h3><p>GitHub Stars</p>"

    assert sync_readme_to_site.extract_existing_repo_stars(html) == 529
    assert sync_readme_to_site.extract_existing_repo_stars("<main></main>") is None


def test_update_sitemap_lastmod_refreshes_date() -> None:
    sitemap = "<url><lastmod>2026-05-09</lastmod></url>"

    updated = sync_readme_to_site.update_sitemap_lastmod(sitemap)
    today = datetime.date.today().isoformat()

    assert f"<lastmod>{today}</lastmod>" in updated
    assert "2026-05-09" not in updated


def test_replace_skills_data_fails_closed() -> None:
    try:
        sync_readme_to_site.replace_skills_data("<script></script>", "const skillsData = {};")
    except RuntimeError as exc:
        assert "实际找到 0 个" in str(exc)
    else:
        raise AssertionError("missing skillsData block should fail closed")


def test_checked_in_site_data_matches_readme() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    html = (REPO_ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    expected = sync_readme_to_site.generate_skills_js(
        sync_readme_to_site.parse_readme(readme)
    )
    match = re.search(r"const skillsData = \{.*?\};", html, flags=re.DOTALL)

    assert match is not None
    assert match.group(0) == expected


def test_original_skill_sets_and_promo_counts_are_consistent() -> None:
    skills_root = REPO_ROOT / "skills"
    skill_names = {
        path.name for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    original_readme = readme.split('<a id="original-skills"></a>', 1)[1]
    original_readme = original_readme.split("\n---\n", 1)[0]
    readme_names = set(re.findall(r"\(skills/([a-z0-9-]+)/\)", original_readme))

    html = (REPO_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    original_html = html.split('<section class="original-skills" id="original">', 1)[1]
    original_html = original_html.split("<!-- Curated Skills -->", 1)[0]
    html_names = set(re.findall(r"<h3>([a-z0-9-]+)</h3>", original_html))

    promo = (REPO_ROOT / "PROMO.md").read_text(encoding="utf-8")
    total_curated = sync_readme_to_site.count_total_skills(
        sync_readme_to_site.parse_readme(readme)
    )

    assert readme_names == skill_names
    assert html_names == skill_names
    assert f"{total_curated}+ 精选" in promo
    assert f"{len(skill_names)} 个原创" in promo


if __name__ == "__main__":
    test_dry_run_works_with_gbk_stdout()
    test_update_html_meta_refreshes_public_counts()
    test_hot_skills_header_is_stable_after_copy_change()
    test_update_html_badges_refreshes_update_date()
    test_update_html_stats_refreshes_original_count()
    test_existing_star_count_is_used_only_when_present()
    test_update_sitemap_lastmod_refreshes_date()
    test_replace_skills_data_fails_closed()
    test_checked_in_site_data_matches_readme()
    test_original_skill_sets_and_promo_counts_are_consistent()
    print("PASS: sync_readme_to_site.py regression tests")
