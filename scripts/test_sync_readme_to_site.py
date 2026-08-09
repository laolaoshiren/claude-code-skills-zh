#!/usr/bin/env python3
"""Regression tests for sync_readme_to_site.py."""

from __future__ import annotations

import contextlib
import datetime
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import sync_readme_to_site


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync_readme_to_site.py"


def _public_sync_fixture() -> tuple[str, str, str, str]:
    """返回数量已一致、但公开日期较旧的最小同步输入。"""
    readme = """> 🚀 最实用的合集 | 精选 3+ | 按场景分类 | 持续更新

[![Skills](https://img.shields.io/badge/skills-3%2B-green.svg)](#original-skills)
[![Updated](https://img.shields.io/badge/updated-2026--01--02-brightgreen.svg)](#maintenance-update)
"""
    skills_js = "const skillsData = {};"
    html = f"""<meta name="description" content="最实用的 Claude Code Skills / Agents / Plugins 中文精选集，收录 3+ 高质量技能、Agent 和插件，2 个原创技能，适合 Claude Code、Codex、Gemini CLI、Cursor 用户复制即装。">
<meta property="og:description" content="收录 3+ Claude Code Skills / Agents / Plugins，按场景分类，中文说明，复制即装，持续更新。">
<meta name="twitter:description" content="3+ 高质量 Claude Code 技能、Agent、插件中文精选，复制即装。">
<span class="badge green">✅ 3+ 精选技能</span>
<span class="badge purple">🎁 2 个原创技能</span>
<span class="badge orange">⭐ 9 Stars</span>
<span class="badge orange">🔄 更新于 2026-01-02</span>
<h3>3+</h3><p>精选技能</p>
<h3>2</h3><p>原创技能</p>
<h3>9</h3><p>GitHub Stars</p>
<h3>2026-01-02</h3><p>最近更新</p>
<script>{skills_js}</script>"""
    sitemap = """<urlset>
  <url>
    <loc>https://claude-skills.bt199.com/</loc>
    <lastmod>2026-01-02</lastmod>
  </url>
</urlset>
"""
    return readme, html, sitemap, skills_js


def _expect_runtime_error(callback, expected_text: str | None = None) -> None:
    try:
        callback()
    except RuntimeError as exc:
        if expected_text is not None:
            assert expected_text in str(exc)
    else:
        raise AssertionError("operation should fail closed")


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
    _expect_runtime_error(
        lambda: sync_readme_to_site.extract_existing_repo_stars(html + html),
        "重复",
    )


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
    sitemap = """<urlset><url>
<loc>https://claude-skills.bt199.com/</loc>
<lastmod>2026-05-09</lastmod>
</url></urlset>"""

    updated = sync_readme_to_site.update_sitemap_lastmod(sitemap)
    today = sync_readme_to_site.current_project_date().isoformat()

    assert f"<lastmod>{today}</lastmod>" in updated
    assert "2026-05-09" not in updated


def test_replace_skills_data_fails_closed() -> None:
    _expect_runtime_error(
        lambda: sync_readme_to_site.replace_skills_data(
            "<script></script>", "const skillsData = {};"
        ),
        "实际找到 0 个",
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.replace_skills_data(
            "const skillsData = {}; const skillsData = {};",
            "const skillsData = {};",
        ),
        "实际找到 2 个",
    )


def test_crlf_site_data_is_a_byte_preserving_noop() -> None:
    readme, html, sitemap, skills_js = _public_sync_fixture()
    readme = readme.replace("\n", "\r\n")
    html = html.replace("\n", "\r\n")
    sitemap = sitemap.replace("\n", "\r\n")

    outputs = sync_readme_to_site.build_sync_outputs(
        readme,
        html,
        sitemap,
        skills_js=skills_js,
        total_skills=3,
        repo_stars=9,
        total_original=2,
        project_date=datetime.date(2026, 7, 16),
    )

    new_readme, new_html, new_sitemap, material_changed = outputs
    assert material_changed is False
    assert new_readme == readme
    assert new_html == html
    assert new_sitemap == sitemap


def test_date_only_difference_is_a_byte_preserving_noop() -> None:
    readme, html, sitemap, skills_js = _public_sync_fixture()

    outputs = sync_readme_to_site.build_sync_outputs(
        readme,
        html,
        sitemap,
        skills_js=skills_js,
        total_skills=3,
        repo_stars=9,
        total_original=2,
        project_date=datetime.date(2026, 7, 15),
    )

    new_readme, new_html, new_sitemap, material_changed = outputs
    assert material_changed is False
    assert new_readme == readme
    assert new_html == html
    assert new_sitemap == sitemap
    assert "2026--01--02" in new_readme
    assert new_html.count("2026-01-02") == 2


def test_material_change_updates_all_public_dates_together() -> None:
    readme, html, sitemap, skills_js = _public_sync_fixture()
    public_date = datetime.date(2026, 7, 15)

    new_readme, new_html, new_sitemap, material_changed = (
        sync_readme_to_site.build_sync_outputs(
            readme,
            html,
            sitemap,
            skills_js=skills_js,
            total_skills=4,
            repo_stars=10,
            total_original=2,
            project_date=public_date,
        )
    )

    assert material_changed is True
    assert "精选 4+" in new_readme
    assert "skills-4%2B" in new_readme
    assert "updated-2026--07--15" in new_readme
    assert new_html.count("2026-07-15") == 2
    assert "✅ 4+ 精选技能" in new_html
    assert "⭐ 10 Stars" in new_html
    assert "<lastmod>2026-07-15</lastmod>" in new_sitemap
    assert "2026-01-02" not in new_sitemap


def test_public_anchors_are_strictly_unique() -> None:
    readme, html, sitemap, _skills_js = _public_sync_fixture()

    _expect_runtime_error(
        lambda: sync_readme_to_site.update_html_meta(
            html.replace('<meta name="twitter:description"', '<meta name="missing"'),
            3,
            2,
        ),
        "实际找到 0 处",
    )
    stats_anchor = "<h3>3+</h3><p>精选技能</p>"
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_html_stats(
            html + stats_anchor,
            3,
            9,
            2,
        ),
        "实际找到 2 处",
    )
    hero_anchor = '<span class="badge green">✅ 3+ 精选技能</span>'
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_html_badges(
            html + hero_anchor,
            3,
            2,
            9,
        ),
        "实际找到 2 处",
    )
    skills_badge = "https://img.shields.io/badge/skills-3%2B-green.svg"
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_readme_badges(
            readme + skills_badge,
            3,
            9,
        ),
        "实际找到 2 处",
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_sitemap_lastmod(
            sitemap.replace("https://claude-skills.bt199.com/", "https://example.com/")
        ),
        "实际找到 0 个",
    )
    duplicate_homepage = sitemap.replace("</urlset>", sitemap.split("<urlset>", 1)[1])
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_sitemap_lastmod(duplicate_homepage),
        "实际找到 2 个",
    )


def test_inconsistent_public_dates_fail_closed() -> None:
    readme, html, sitemap, skills_js = _public_sync_fixture()
    drifted_html = html.replace("🔄 更新于 2026-01-02", "🔄 更新于 2026-01-03")

    _expect_runtime_error(
        lambda: sync_readme_to_site.build_sync_outputs(
            readme,
            drifted_html,
            sitemap,
            skills_js=skills_js,
            total_skills=3,
            repo_stars=9,
            total_original=2,
            project_date=datetime.date(2026, 7, 15),
        ),
        "公开日期不一致",
    )


def test_sitemap_lastmod_is_anchored_to_homepage() -> None:
    sitemap = """<urlset>
<url><loc>https://claude-skills.bt199.com/docs</loc><lastmod>2026-01-01</lastmod></url>
<url><loc>https://claude-skills.bt199.com/</loc><lastmod>2026-02-02</lastmod></url>
</urlset>"""

    updated = sync_readme_to_site.update_sitemap_lastmod(
        sitemap,
        project_date=datetime.date(2026, 7, 15),
    )

    assert "<loc>https://claude-skills.bt199.com/docs</loc><lastmod>2026-01-01" in updated
    assert "<loc>https://claude-skills.bt199.com/</loc><lastmod>2026-07-15" in updated


def test_file_bundle_rolls_back_when_second_replace_fails() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        paths = [root / "README.md", root / "index.html", root / "sitemap.xml"]
        originals = [b"readme-old", b"html-old", b"sitemap-old"]
        for path, content in zip(paths, originals):
            path.write_bytes(content)

        real_replace = os.replace
        replace_calls = 0

        def fail_second_replace(source, destination):
            nonlocal replace_calls
            replace_calls += 1
            if replace_calls == 2:
                raise OSError("injected second replace failure")
            return real_replace(source, destination)

        with patch.object(
            sync_readme_to_site.os,
            "replace",
            side_effect=fail_second_replace,
        ):
            try:
                sync_readme_to_site.write_file_bundle(
                    {
                        paths[0]: "readme-new",
                        paths[1]: "html-new",
                        paths[2]: "sitemap-new",
                    }
                )
            except OSError as exc:
                assert "second replace" in str(exc)
            else:
                raise AssertionError("second replace failure should escape after rollback")

        assert [path.read_bytes() for path in paths] == originals
        assert list(root.glob(".*.tmp")) == []


def test_file_bundle_skips_unchanged_files() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        root = Path(temporary_directory)
        unchanged = root / "README.md"
        changed = root / "index.html"
        unchanged.write_text("same", encoding="utf-8")
        changed.write_text("old", encoding="utf-8")
        os.chmod(changed, 0o640)
        original_mode = stat.S_IMODE(changed.stat().st_mode)

        real_replace = os.replace
        with patch.object(
            sync_readme_to_site.os,
            "replace",
            wraps=real_replace,
        ) as replace:
            changed_paths = sync_readme_to_site.write_file_bundle(
                {unchanged: "same", changed: "new"}
            )

        assert changed_paths == [changed]
        assert replace.call_count == 1
        assert unchanged.read_text(encoding="utf-8") == "same"
        assert changed.read_text(encoding="utf-8") == "new"
        assert stat.S_IMODE(changed.stat().st_mode) == original_mode


def test_main_captures_project_date_once() -> None:
    fixed_date = datetime.date(2026, 7, 15)
    output = io.StringIO()
    with patch.object(sync_readme_to_site, "current_project_date", return_value=fixed_date) as now:
        with patch.object(sync_readme_to_site.sys, "argv", [str(SCRIPT_PATH), "--dry-run"]):
            with contextlib.redirect_stdout(output):
                sync_readme_to_site.main()

    assert now.call_count == 1
    assert "dry-run 完成" in output.getvalue()


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


def test_checked_in_readme_is_a_user_facing_landing_page() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert '<a id="maintenance-update"></a>' not in readme
    assert not re.search(
        r"^#{2,6}\s+\d{4}-\d{2}-\d{2}\s+维护更新\s*$",
        readme,
        flags=re.MULTILINE,
    )
    assert re.search(
        r"\[!\[Updated\]\(https://img\.shields\.io/badge/updated-"
        r"\d{4}--\d{2}--\d{2}-brightgreen\.svg\)\]"
        r"\(https://github\.com/laolaoshiren/claude-code-skills-zh/commits/main\)",
        readme,
    )


def test_checked_in_landing_pages_avoid_unsynced_ecosystem_stats() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    html = (REPO_ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "## 📊 技能生态数据" not in readme
    assert not re.search(
        r"^- \[[^]]+\]\([^)]+\) — \d+(?:\.\d+)?K? ⭐\s*$",
        readme,
        flags=re.MULTILINE,
    )
    assert "<!-- Ecosystem -->" not in html
    assert "AI Coding Skills 正在爆发式增长" not in html


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
    test_crlf_site_data_is_a_byte_preserving_noop()
    test_date_only_difference_is_a_byte_preserving_noop()
    test_material_change_updates_all_public_dates_together()
    test_public_anchors_are_strictly_unique()
    test_inconsistent_public_dates_fail_closed()
    test_sitemap_lastmod_is_anchored_to_homepage()
    test_file_bundle_rolls_back_when_second_replace_fails()
    test_file_bundle_skips_unchanged_files()
    test_main_captures_project_date_once()
    test_generated_js_escapes_html_breakouts_and_line_separators()
    test_generated_js_rejects_non_http_or_hostless_urls()
    test_refresh_readme_stars_formats_and_unifies_duplicate_repositories()
    test_fetch_github_stars_uses_graphql_and_preserves_partial_failures()
    test_checked_in_site_renders_skill_data_with_safe_dom_apis()
    test_checked_in_site_data_matches_readme()
    test_checked_in_readme_is_a_user_facing_landing_page()
    test_checked_in_landing_pages_avoid_unsynced_ecosystem_stats()
    test_original_skill_sets_and_promo_counts_are_consistent()
    print("PASS: sync_readme_to_site.py regression tests")
