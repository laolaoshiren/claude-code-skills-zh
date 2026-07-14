#!/usr/bin/env python3
"""Regression tests for sync_readme_to_site.py."""

from __future__ import annotations

import contextlib
import datetime
import io
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

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


def test_project_date_uses_asia_shanghai_boundary() -> None:
    before_midnight = datetime.datetime(
        2026, 7, 14, 15, 59, tzinfo=datetime.timezone.utc
    )
    at_midnight = datetime.datetime(
        2026, 7, 14, 16, 0, tzinfo=datetime.timezone.utc
    )

    assert sync_readme_to_site.current_project_date(before_midnight) == datetime.date(
        2026, 7, 14
    )
    assert sync_readme_to_site.current_project_date(at_midnight) == datetime.date(
        2026, 7, 15
    )

    try:
        sync_readme_to_site.current_project_date(datetime.datetime(2026, 7, 15))
    except ValueError as exc:
        assert "时区" in str(exc)
    else:
        raise AssertionError("naive datetime should be rejected")


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
    today = sync_readme_to_site.current_project_date().isoformat()

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
    today = sync_readme_to_site.current_project_date().isoformat()

    assert "<h3>349+</h3><p>精选技能</p>" in updated
    assert "<h3>19</h3><p>原创技能</p>" in updated
    assert "<h3>513</h3><p>GitHub Stars</p>" in updated
    assert f"<h3>{today}</h3><p>最近更新</p>" in updated
    assert "<h3>20</h3><p>原创技能</p>" not in updated


def test_existing_star_count_is_used_only_when_present() -> None:
    html = "<h3>529</h3><p>GitHub Stars</p>"

    assert sync_readme_to_site.extract_existing_repo_stars(html) == 529
    assert sync_readme_to_site.extract_existing_repo_stars("<main></main>") is None


def test_own_repo_star_uses_batch_value_or_safe_fallback() -> None:
    repo_key = sync_readme_to_site.normalize_repo_slug(sync_readme_to_site.GITHUB_REPO)
    assert sync_readme_to_site.resolve_own_repo_stars({repo_key: 618}, 611) == 618

    warnings = io.StringIO()
    with contextlib.redirect_stderr(warnings):
        assert sync_readme_to_site.resolve_own_repo_stars({}, 611) == 611
    assert "安全回退" in warnings.getvalue()

    try:
        sync_readme_to_site.resolve_own_repo_stars({}, None)
    except RuntimeError as exc:
        assert "没有可回退" in str(exc)
    else:
        raise AssertionError("missing fetched and existing repo stars should fail closed")


def test_update_sitemap_lastmod_refreshes_date() -> None:
    sitemap = "<url><lastmod>2026-05-09</lastmod></url>"

    updated = sync_readme_to_site.update_sitemap_lastmod(sitemap)
    today = sync_readme_to_site.current_project_date().isoformat()

    assert f"<lastmod>{today}</lastmod>" in updated
    assert "2026-05-09" not in updated


def test_replace_skills_data_fails_closed() -> None:
    try:
        sync_readme_to_site.replace_skills_data("<script></script>", "const skillsData = {};")
    except RuntimeError as exc:
        assert "实际找到 0 个" in str(exc)
    else:
        raise AssertionError("missing skillsData block should fail closed")


def test_generated_js_escapes_html_breakouts_and_line_separators() -> None:
    skills_data = {
        "dev": [
            {
                "name": "safe </script>",
                "stars": "1",
                "desc": "A&B > C\u2028D\u2029E",
                "url": "https://example.com/repo?x=1&y=2",
            }
        ]
    }

    generated = sync_readme_to_site.generate_skills_js(skills_data)

    assert "</script>" not in generated
    assert "A&B" not in generated
    assert "\u2028" not in generated
    assert "\u2029" not in generated
    assert "\\u003Csafe" not in generated  # 不应改变文本顺序
    assert "safe \\u003C/script\\u003E" in generated
    assert "A\\u0026B \\u003E C\\u2028D\\u2029E" in generated
    assert "x=1\\u0026y=2" in generated

    replaced = sync_readme_to_site.replace_skills_data(
        "<script>const skillsData = {};</script>", generated
    )
    assert generated in replaced


def test_generated_js_rejects_non_http_or_hostless_urls() -> None:
    for invalid_url in [
        "javascript:alert(1)",
        "/relative/path",
        "https:///missing-host",
        "https://example.com/has space",
    ]:
        try:
            sync_readme_to_site.generate_skills_js(
                {
                    "dev": [
                        {
                            "name": "unsafe",
                            "stars": "",
                            "desc": "unsafe",
                            "url": invalid_url,
                        }
                    ]
                }
            )
        except ValueError as exc:
            assert "URL" in str(exc)
        else:
            raise AssertionError(f"invalid URL should fail closed: {invalid_url}")


def test_refresh_readme_stars_formats_and_unifies_duplicate_repositories() -> None:
    readme = """### 🏆 热门与高潜技能

| 技能 | 说明 | ⭐ |
|------|------|-----|
| [Repo](https://github.com/Owner/Repo) | 热门描述 | 9.9K+ |

### 💻 开发效率

| 技能 | 说明 |
|------|------|
| [Repo 重复](https://github.com/owner/repo) | 普通描述（7⭐）|
| [Small](https://github.com/small/repo) | 小仓库（1.2K⭐）|
| [Missing](https://github.com/missing/repo) | 失败时保留（88⭐）|
"""

    updated = sync_readme_to_site.refresh_readme_stars(
        readme,
        {"owner/repo": 1234, "small/repo": 999},
    )

    assert "| [Repo](https://github.com/Owner/Repo) | 热门描述 | 1.2K+ |" in updated
    assert "普通描述（1.2K⭐）" in updated
    assert "小仓库（999⭐）" in updated
    assert "失败时保留（88⭐）" in updated

    parsed = sync_readme_to_site.parse_readme(updated)
    repositories = sync_readme_to_site.collect_github_repositories(
        parsed,
        extra_repositories=[sync_readme_to_site.GITHUB_REPO],
    )
    normalized = [sync_readme_to_site.normalize_repo_slug(repo) for repo in repositories]
    assert normalized.count("owner/repo") == 1
    assert sync_readme_to_site.normalize_repo_slug(sync_readme_to_site.GITHUB_REPO) in normalized


def test_fetch_github_stars_uses_graphql_and_preserves_partial_failures() -> None:
    completed = subprocess.CompletedProcess(
        args=[],
        # gh 在某个别名查询失败时会以 1 退出，但 stdout 仍含 partial data。
        returncode=1,
        stdout=json.dumps(
            {
                "data": {
                    "r0": {"stargazerCount": 1234},
                    "r1": None,
                },
                "errors": [{"message": "Could not resolve repository"}],
            }
        ),
        stderr="GraphQL: Could not resolve repository",
    )
    warnings = io.StringIO()

    with patch.object(sync_readme_to_site.subprocess, "run", return_value=completed) as run:
        with contextlib.redirect_stderr(warnings):
            stars = sync_readme_to_site.fetch_github_stars(
                ["Owner/Repo", "owner/repo", "Missing/Repo"]
            )

    assert stars == {"owner/repo": 1234}
    run.assert_called_once()
    command = run.call_args.args[0]
    assert command[:3] == ["gh", "api", "graphql"]
    assert any(argument.startswith("query=query RepositoryStars") for argument in command)
    assert "repos/" not in " ".join(command)
    assert "Missing/Repo" in warnings.getvalue()
    assert "保留 README 旧值" in warnings.getvalue()


def test_checked_in_site_renders_skill_data_with_safe_dom_apis() -> None:
    html = (REPO_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    render_block = html.split("function renderSkills(tab) {", 1)[1]
    render_block = render_block.split("// Tab switching", 1)[0]

    assert "container.innerHTML" not in render_block
    assert "link.textContent = s.name" in render_block
    assert "desc.textContent = s.desc" in render_block
    assert "link.rel = 'noopener noreferrer'" in render_block
    assert "container.replaceChildren(fragment)" in render_block


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
    test_project_date_uses_asia_shanghai_boundary()
    test_update_html_meta_refreshes_public_counts()
    test_hot_skills_header_is_stable_after_copy_change()
    test_update_html_badges_refreshes_update_date()
    test_update_html_stats_refreshes_original_count()
    test_existing_star_count_is_used_only_when_present()
    test_own_repo_star_uses_batch_value_or_safe_fallback()
    test_update_sitemap_lastmod_refreshes_date()
    test_replace_skills_data_fails_closed()
    test_generated_js_escapes_html_breakouts_and_line_separators()
    test_generated_js_rejects_non_http_or_hostless_urls()
    test_refresh_readme_stars_formats_and_unifies_duplicate_repositories()
    test_fetch_github_stars_uses_graphql_and_preserves_partial_failures()
    test_checked_in_site_renders_skill_data_with_safe_dom_apis()
    test_checked_in_site_data_matches_readme()
    test_original_skill_sets_and_promo_counts_are_consistent()
    print("PASS: sync_readme_to_site.py regression tests")
