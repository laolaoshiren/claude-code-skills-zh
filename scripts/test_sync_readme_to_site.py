#!/usr/bin/env python3
"""Regression tests for sync_readme_to_site.py."""

from __future__ import annotations

import contextlib
import datetime
import inspect
import io
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

import sync_readme_to_site


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "sync_readme_to_site.py"


def _public_sync_fixture() -> tuple[str, str, str, str, str, str]:
    """返回数量已一致、但公开日期较旧的最小同步输入。"""
    readme = """> 🚀 最实用的合集 | 精选 3+ | 按场景分类 | 持续更新

[![Skills](https://img.shields.io/badge/skills-3%2B-green.svg)](#original-skills)
[![Updated](https://img.shields.io/badge/updated-2026--01--02-brightgreen.svg)](#maintenance-update)

**合集名称** 是面向中文开发者的精选仓库：**3+** 个精选技能按场景分类，另含 **2 个**可直接安装的原创中文技能。

**English:** it is a curated list of 3+ Claude Code Skills, Agents and Plugins for Chinese-speaking developers, plus 2 original install-ready skills.

## 📊 同类仓库对比

| 仓库 | Stars | 规模 | 语言 | 定位 |
|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 180K | 官方技能集 | 英文 | Anthropic 官方出品 |
| **claude-code-skills-zh（本仓库）** | 见[顶部徽章](https://github.com/laolaoshiren/claude-code-skills-zh) | 3+ 精选 + 2 原创 | **中文** | 中文精选与原创技能 |

## ❓ 常见问题（FAQ）

A：本仓库按场景收录了 3+ 个 Skills / Agents / Plugins，并提供官网筛选。
"""
    skills_js = "const skillsData = {};"
    html = f"""<meta name="description" content="最实用的 Claude Code Skills / Agents / Plugins 中文精选集，收录 3+ 高质量技能、Agent 和插件，2 个原创技能，适合 Claude Code、Codex、Gemini CLI、Cursor 用户复制即装。">
<meta property="og:description" content="收录 3+ Claude Code Skills / Agents / Plugins，按场景分类，中文说明，复制即装，持续更新。">
<meta name="twitter:description" content="3+ 高质量 Claude Code 技能、Agent、插件中文精选，复制即装。">
<script type="application/ld+json">{{"text": "按场景收录 3+ 个 Claude Code Skills / Agents / Plugins，并附带 2 个可直接安装的原创中文技能。"}}</script>
<a class="nav-star">⭐ GitHub <span class="nav-star-count">9</span></a>
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
    promo = """**标题：** [分享] Claude Code Skills 中文精选集 — 3+ 精选技能 + 2 个原创可安装技能
还整理了 3+ 第三方精选资源，按场景分类。
**标题：** Claude Code Skills 入门指南：2 个面向中文开发者的实用 AI 技能
我整理了一份中文精选集，还写了 2 个实用的原创技能：
✅ 3+ 精选资源列表
✅ 2 个原创可安装技能
不只列出了 3+ 优质资源，还带了 2 个原创技能可以直接装：
不只列了 3+ 好用的资源，还带了 2 个原创技能可以直接装：
"""
    llms = """> 面向中文开发者的精选仓库，收录 3+ 个精选技能，另含 2 个可直接安装的原创中文技能。
"""
    return readme, html, sitemap, promo, llms, skills_js


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
    readme, html, sitemap, promo, llms, skills_js = _public_sync_fixture()
    readme = readme.replace("\n", "\r\n")
    html = html.replace("\n", "\r\n")
    sitemap = sitemap.replace("\n", "\r\n")
    promo = promo.replace("\n", "\r\n")
    llms = llms.replace("\n", "\r\n")

    outputs = sync_readme_to_site.build_sync_outputs(
        readme,
        html,
        sitemap,
        promo,
        llms,
        skills_js=skills_js,
        total_skills=3,
        repo_stars=9,
        total_original=2,
        project_date=datetime.date(2026, 7, 16),
    )

    new_readme, new_html, new_sitemap, new_promo, new_llms, material_changed = outputs
    assert material_changed is False
    assert new_readme == readme
    assert new_html == html
    assert new_sitemap == sitemap
    assert new_promo == promo
    assert new_llms == llms


def test_date_only_difference_is_a_byte_preserving_noop() -> None:
    readme, html, sitemap, promo, llms, skills_js = _public_sync_fixture()

    outputs = sync_readme_to_site.build_sync_outputs(
        readme,
        html,
        sitemap,
        promo,
        llms,
        skills_js=skills_js,
        total_skills=3,
        repo_stars=9,
        total_original=2,
        project_date=datetime.date(2026, 7, 15),
    )

    new_readme, new_html, new_sitemap, new_promo, new_llms, material_changed = outputs
    assert material_changed is False
    assert new_readme == readme
    assert new_html == html
    assert new_sitemap == sitemap
    assert new_promo == promo
    assert new_llms == llms
    assert "2026--01--02" in new_readme
    assert new_html.count("2026-01-02") == 2


def test_material_change_updates_all_public_dates_together() -> None:
    readme, html, sitemap, promo, llms, skills_js = _public_sync_fixture()
    public_date = datetime.date(2026, 7, 15)

    new_readme, new_html, new_sitemap, new_promo, new_llms, material_changed = (
        sync_readme_to_site.build_sync_outputs(
            readme,
            html,
            sitemap,
            promo,
            llms,
            skills_js=skills_js,
            total_skills=4,
            repo_stars=10,
            total_original=3,
            project_date=public_date,
        )
    )

    assert material_changed is True
    assert "精选 4+" in new_readme
    assert "skills-4%2B" in new_readme
    assert "4+ 精选 + 3 原创" in new_readme
    assert "收录了 4+ 个 Skills / Agents / Plugins" in new_readme
    assert "updated-2026--07--15" in new_readme
    assert new_html.count("2026-07-15") == 2
    assert "✅ 4+ 精选技能" in new_html
    assert "⭐ 10 Stars" in new_html
    assert '<span class="nav-star-count">10</span>' in new_html
    assert "按场景收录 4+ 个 Claude Code Skills / Agents / Plugins" in new_html
    assert "并附带 3 个可直接安装的原创中文技能" in new_html
    assert "<lastmod>2026-07-15</lastmod>" in new_sitemap
    assert "2026-01-02" not in new_sitemap
    assert "入门指南：3 个面向中文开发者的实用 AI 技能" in new_promo
    assert "还写了 3 个实用的原创技能" in new_promo
    assert "收录 4+ 个精选技能" in new_llms
    assert "另含 3 个可直接安装的原创中文技能" in new_llms


def test_public_anchors_are_strictly_unique() -> None:
    readme, html, sitemap, _promo, _llms, _skills_js = _public_sync_fixture()

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
    readme, html, sitemap, promo, llms, skills_js = _public_sync_fixture()
    drifted_html = html.replace("🔄 更新于 2026-01-02", "🔄 更新于 2026-01-03")

    _expect_runtime_error(
        lambda: sync_readme_to_site.build_sync_outputs(
            readme,
            drifted_html,
            sitemap,
            promo,
            llms,
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

    assert "innerHTML" not in html
    assert "container.innerHTML" not in render_block
    assert "document.createElement('article')" in render_block
    assert "link.className = 'skill-title-link'" in render_block
    assert "link.textContent = s.name" in render_block
    assert "desc.textContent = s.desc" in render_block
    assert "link.rel = 'noopener noreferrer'" in render_block
    assert "isSafeDetailUrl(s.detailUrl)" in render_block
    assert "detailLink.className = 'skill-detail-btn'" in render_block
    assert "ghLink.className = 'skill-gh-link'" in render_block
    assert "ghLink.rel = 'noopener noreferrer'" in render_block
    assert "container.replaceChildren(fragment)" in render_block
    assert (
        '<a class="original-detail-link" href="/skills/skill-translator/">📖 详解页</a>'
        in html
    )

    class _NestedAnchorChecker(HTMLParser):
        def __init__(self) -> None:
            super().__init__()
            self.anchor_depth = 0
            self.nested_found = False

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
            if tag.lower() == "a":
                self.anchor_depth += 1
                if self.anchor_depth > 1:
                    self.nested_found = True

        def handle_endtag(self, tag: str) -> None:
            if tag.lower() == "a" and self.anchor_depth > 0:
                self.anchor_depth -= 1

    checker = _NestedAnchorChecker()
    checker.feed(html)
    checker.close()
    assert checker.nested_found is False


def test_checked_in_site_data_matches_readme() -> None:
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    html = (REPO_ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    detail_pages = sync_readme_to_site.discover_detail_pages(REPO_ROOT / "docs")
    detail_url_map = sync_readme_to_site.build_detail_url_map(detail_pages)

    expected = sync_readme_to_site.generate_skills_js(
        sync_readme_to_site.parse_readme(readme),
        detail_url_map=detail_url_map,
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


def test_readme_fact_summary_counts_are_synced() -> None:
    """「一句话事实」、同类仓库对比表和 FAQ 的精选数量必须跟随同步，避免长期漂移。"""
    readme, _html, _sitemap, _promo, _llms, _js = _public_sync_fixture()

    updated = sync_readme_to_site.update_readme_badges(readme, 7, 9)

    assert "**7+** 个精选技能" in updated
    assert "of 7+ Claude Code Skills, Agents and Plugins" in updated
    assert "7+ 精选 + 2 原创" in updated
    assert "收录了 7+ 个 Skills / Agents / Plugins" in updated
    assert "**3+**" not in updated
    assert "of 3+ Claude" not in updated
    assert "3+ 精选" not in updated
    assert "收录了 3+ 个 Skills" not in updated


def test_readme_fact_summary_original_count_is_synced() -> None:
    """事实摘要与同类仓库对比表里的原创技能数量必须跟随同步，避免新增技能后忘记改。"""
    readme, _html, _sitemap, _promo, _llms, _js = _public_sync_fixture()

    updated = sync_readme_to_site.update_readme_original_count(readme, 5)

    assert "另含 **5 个**可直接安装的原创中文技能" in updated
    assert "plus 5 original install-ready skills" in updated
    assert "3+ 精选 + 5 原创" in updated
    assert "另含 **2 个**" not in updated
    assert "plus 2 original" not in updated
    assert "+ 2 原创" not in updated


def test_update_promo_counts_refreshes_all_occurrences() -> None:
    """PROMO.md 的每处精选/原创数量（含第 2 节掘金发文）都应被同步，且互不干扰。"""
    promo = """**标题：** [分享] Claude Code Skills 中文精选集 — 438+ 精选技能 + 20 个原创可安装技能

还整理了 438+ 第三方精选资源，按场景分类。

**标题：** Claude Code Skills 入门指南：20 个面向中文开发者的实用 AI 技能
我整理了一份中文精选集，还写了 20 个实用的原创技能：

✅ 438+ 精选资源列表
✅ 20 个原创可安装技能

不只列出了 438+ 优质资源，还带了 20 个原创技能可以直接装：

不只列了 438+ 好用的资源，还带了 20 个原创技能可以直接装：
"""
    updated = sync_readme_to_site.update_promo_counts(promo, 445, 22)

    # 标题 1 处 + 正文 4 处 = 5 处精选数量
    assert updated.count("445+") == 5
    assert "438+" not in updated
    # V2EX 标题 + 掘金标题 + 掘金正文 + 推文 + 知乎 + 微信群 = 6 处原创数量
    assert "入门指南：22 个面向中文开发者的实用 AI 技能" in updated
    assert "还写了 22 个实用的原创技能" in updated
    assert updated.count("22 个原创") == 4
    assert "20 个" not in updated
    # 除数字外不应改动其他文字
    assert "第三方精选资源" in updated
    assert "好用的资源" in updated


def test_update_promo_counts_fails_closed_on_missing_anchor() -> None:
    """锚点缺失时必须抛错，不能静默留下过期数字。"""
    broken = "**标题：** [分享] Claude Code Skills 中文精选集 — 438+ 精选技能\n"
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_promo_counts(broken, 445, 22),
    )


def test_update_promo_counts_fails_closed_on_duplicate_anchor() -> None:
    """同一锚点出现两次时必须抛错，避免改错位置。"""
    duplicated = (
        "✅ 438+ 精选资源列表\n"
        "✅ 438+ 精选资源列表\n"
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_promo_counts(duplicated, 445, 22),
    )


def test_academic_category_is_independent_and_synced() -> None:
    """学术科研分类必须独立输出，不再静默并入 dev，且支持 Star 刷新。"""
    assert sync_readme_to_site.CATEGORY_ORDER == [
        "star",
        "platform",
        "dev",
        "creative",
        "academic",
        "agent",
        "finance",
        "chinese",
    ]
    readme = """### 💻 开发效率

| 技能 | 说明 |
|------|------|
| [dev-tool](https://github.com/org/dev-tool) | 开发工具（10⭐）|

### 🔬 学术科研

| 技能 | 说明 |
|------|------|
| [paper-tool](https://github.com/org/paper-tool) | 论文检索（20⭐）|
"""
    parsed = sync_readme_to_site.parse_readme(readme)
    assert [item["name"] for item in parsed["dev"]] == ["dev-tool"]
    assert [item["name"] for item in parsed["academic"]] == ["paper-tool"]

    js = sync_readme_to_site.generate_skills_js(parsed)
    assert "  academic: [\n    {name:'paper-tool',stars:'20',desc:'论文检索',url:'https://github.com/org/paper-tool'},\n  ]," in js
    assert "paper-tool" not in js.split("  dev: [", 1)[1].split("  ],", 1)[0]

    refreshed = sync_readme_to_site.refresh_readme_stars(readme, {"org/paper-tool": 2500})
    assert "论文检索（2.5K⭐）" in refreshed


def test_zh_doc_flag_preserved_only_when_marked_after_link() -> None:
    """项目名列在 [name](url) 后含 🇨🇳 时输出 zhDoc:true，且 name 保持纯名称。"""
    readme = """### 🏆 热门与高潜技能

| 技能 | 说明 | ⭐ |
|------|------|-----|
| [ClawX](https://github.com/ValueCell-ai/ClawX) 🇨🇳 | 可视化桌面体验 | 7.6K+ |
| [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) | 🇨🇳 完整汉化技能 | 8.5K+ |

### 🤖 AI Agent

| 技能 | 说明 |
|------|------|
| [deja-vu](https://github.com/vshulcz/deja-vu) 🇨🇳 | 本地会话记忆（1.5K⭐）|
"""
    parsed = sync_readme_to_site.parse_readme(readme)
    clawx = parsed["star"][0]
    superpowers_zh = parsed["star"][1]
    dejavu = parsed["agent"][0]

    assert clawx["name"] == "ClawX"
    assert clawx.get("zhDoc") is True
    assert superpowers_zh["name"] == "superpowers-zh"
    assert "zhDoc" not in superpowers_zh
    assert dejavu["name"] == "deja-vu"
    assert dejavu.get("zhDoc") is True

    js = sync_readme_to_site.generate_skills_js(parsed)
    assert "{name:'ClawX',stars:'7.6K+',desc:'可视化桌面体验',url:'https://github.com/ValueCell-ai/ClawX',zhDoc:true,tag:'star'}," in js
    assert "{name:'superpowers-zh',stars:'8.5K+',desc:'🇨🇳 完整汉化技能',url:'https://github.com/jnMetaCode/superpowers-zh',tag:'star'}," in js
    assert "{name:'deja-vu',stars:'1.5K+',desc:'本地会话记忆',url:'https://github.com/vshulcz/deja-vu',zhDoc:true}," in js


def test_strip_inline_markdown_cleans_bold_and_backticks_while_keeping_escaping() -> None:
    """写入 skillsData 的 desc 应剥离成对 **...** 与 `...`，并保留脚本边界转义。"""
    assert (
        sync_readme_to_site.strip_inline_markdown(
            "含 **中文官网** 与 **`SKILL.md`**，支持 `npx skills add a/b`，保留 skills/**/*.md 与 2 ** 3"
        )
        == "含 中文官网 与 SKILL.md，支持 npx skills add a/b，保留 skills/**/*.md 与 2 ** 3"
    )
    js = sync_readme_to_site.generate_skills_js(
        {
            "dev": [
                {
                    "name": "md-test",
                    "stars": "12",
                    "desc": "提供 **中文文档**，命令 `echo </script>&1`",
                    "url": "https://github.com/org/md-test",
                }
            ]
        }
    )
    assert "**" not in js
    assert "`" not in js
    assert "</script>" not in js
    assert "提供 中文文档，命令 echo \\u003C/script\\u003E\\u00261" in js


def test_refresh_readme_stars_syncs_comparison_table_external_repos() -> None:
    """同类仓库对比表中的外部仓库随 --fetch-stars 同步，但永不覆写本仓动态徽章。"""
    readme = """## 📊 同类仓库对比

| 仓库 | Stars | 规模 | 语言 | 定位 |
|---|---|---|---|---|
| [anthropics/skills](https://github.com/anthropics/skills) | 182.7K | 官方技能集 | 英文 | Anthropic 官方出品 |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 77.6K | 1000+ | 英文 | 英文精选列表 |
| [missing/repo](https://github.com/missing/repo) | 12.3K | 100 | 英文 | 未拉取到时保留旧值 |
| **claude-code-skills-zh（本仓库）** | 见[顶部徽章](https://github.com/laolaoshiren/claude-code-skills-zh) | 445+ 精选 + 22 原创 | **中文** | 中文精选 |

### 🏆 热门与高潜技能

| 技能 | 说明 | ⭐ |
|------|------|-----|
| [anthropic-skills](https://github.com/anthropics/skills) | 官方仓库 | 182.7K+ |
"""
    updated = sync_readme_to_site.refresh_readme_stars(
        readme,
        {
            "anthropics/skills": 191234,
            "ComposioHQ/awesome-claude-skills": 79140,
            sync_readme_to_site.GITHUB_REPO: 999,
        },
    )

    assert "| [anthropics/skills](https://github.com/anthropics/skills) | 191.2K |" in updated
    assert "| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 79.1K |" in updated
    assert "| [missing/repo](https://github.com/missing/repo) | 12.3K |" in updated
    assert "见[顶部徽章](https://github.com/laolaoshiren/claude-code-skills-zh)" in updated
    assert "| [anthropic-skills](https://github.com/anthropics/skills) | 官方仓库 | 191.2K+ |" in updated


def test_update_llms_counts_syncs_curated_and_original_and_fails_closed() -> None:
    """docs/llms.txt 的原创数量与精选数量应同步更新，缺失或重复锚点均须 fail-closed。"""
    llms_with_both = (
        "> 收录 445+ 个 Claude Code Skills / Agents / Plugins，另含 20 个可直接安装的原创中文技能。\n"
    )
    updated = sync_readme_to_site.update_llms_counts(llms_with_both, 453, 22)
    assert "收录 453+ 个 Claude Code Skills / Agents / Plugins" in updated
    assert "另含 22 个可直接安装的原创中文技能" in updated

    llms_curated_short = (
        "> 面向中文开发者的精选仓库，收录 445+ 个精选技能，另含 20 个可直接安装的原创中文技能。\n"
    )
    updated_short = sync_readme_to_site.update_llms_counts(llms_curated_short, 453, 22)
    assert "收录 453+ 个精选技能" in updated_short
    assert "另含 22 个可直接安装的原创中文技能" in updated_short

    _expect_runtime_error(
        lambda: sync_readme_to_site.update_llms_counts(
            "> 面向中文开发者的精选仓库，另含 20 个可直接安装的原创中文技能。\n", 453, 22
        ),
        "实际找到 0 处",
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_llms_counts("无任何数量锚点", 453, 22),
        "实际找到 0 处",
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_llms_counts(
            "收录 445+ 个精选技能，又收录 445+ 个精选技能，另含 20 个可直接安装的原创中文技能。",
            453,
            22,
        ),
        "实际找到 2 处",
    )


def test_promo_or_llms_only_change_triggers_material_changed() -> None:
    """仅 PROMO.md 或仅 docs/llms.txt 发生数量修正时，必须计入 material_changed 并推进日期。"""
    readme, html, sitemap, promo, llms, skills_js = _public_sync_fixture()
    public_date = datetime.date(2026, 7, 15)

    drifted_promo = promo.replace("入门指南：2 个面向中文开发者的实用 AI 技能", "入门指南：1 个面向中文开发者的实用 AI 技能")
    new_readme, new_html, new_sitemap, new_promo, new_llms, changed = (
        sync_readme_to_site.build_sync_outputs(
            readme,
            html,
            sitemap,
            drifted_promo,
            llms,
            skills_js=skills_js,
            total_skills=3,
            repo_stars=9,
            total_original=2,
            project_date=public_date,
        )
    )
    assert changed is True
    assert new_promo == promo
    assert new_llms == llms
    assert "updated-2026--07--15" in new_readme
    assert new_html.count("2026-07-15") == 2
    assert "<lastmod>2026-07-15</lastmod>" in new_sitemap

    drifted_llms = llms.replace("另含 2 个可直接安装的原创中文技能", "另含 1 个可直接安装的原创中文技能")
    _r2, _h2, _s2, _p2, new_llms_2, changed_2 = (
        sync_readme_to_site.build_sync_outputs(
            readme,
            html,
            sitemap,
            promo,
            drifted_llms,
            skills_js=skills_js,
            total_skills=3,
            repo_stars=9,
            total_original=2,
            project_date=public_date,
        )
    )
    assert changed_2 is True
    assert new_llms_2 == llms


def test_html_optional_nav_stars_and_jsonld_faq_anchors() -> None:
    """导航栏星数与 JSON-LD FAQ 数量在存在时自动同步、缺失时兼容、重复时 fail-closed。"""
    _readme, html, _sitemap, _promo, _llms, _js = _public_sync_fixture()

    updated_badges = sync_readme_to_site.update_html_badges(html, 10, 5, 927)
    assert '<span class="nav-star-count">927</span>' in updated_badges

    updated_meta = sync_readme_to_site.update_html_meta(html, 10, 5)
    assert "按场景收录 10+ 个 Claude Code Skills / Agents / Plugins" in updated_meta
    assert "并附带 5 个可直接安装的原创中文技能" in updated_meta

    html_without_optional = html.replace('<span class="nav-star-count">9</span>', "")
    html_without_optional = re.sub(r'<script type="application/ld\+json">.*?</script>', "", html_without_optional)
    sync_readme_to_site.update_html_badges(html_without_optional, 10, 5, 927)
    sync_readme_to_site.update_html_meta(html_without_optional, 10, 5)

    _expect_runtime_error(
        lambda: sync_readme_to_site.update_html_badges(
            html + '<span class="nav-star-count">9</span>',
            10,
            5,
            927,
        ),
        "期望至多 1 处",
    )


def test_sync_script_hygiene_no_raw_control_chars_or_stale_original_default() -> None:
    """源码不得残留裸控制字符，且 update_html_stats 不得写死过期原创数量默认值。"""
    source = SCRIPT_PATH.read_bytes()
    assert b"\x02" not in source
    assert b"\x08" not in source

    param = inspect.signature(sync_readme_to_site.update_html_stats).parameters["total_original"]
    assert param.default is inspect.Parameter.empty

    _readme, html, _sitemap, _promo, _llms, _js = _public_sync_fixture()
    dirty_html = "\x02" + html + "\x08"
    cleaned = sync_readme_to_site.update_html_badges(dirty_html, 3, 2, 9)
    assert "\x02" not in cleaned
    assert "\x08" not in cleaned


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
    llms = (REPO_ROOT / "docs" / "llms.txt").read_text(encoding="utf-8")
    total_curated = sync_readme_to_site.count_total_skills(
        sync_readme_to_site.parse_readme(readme)
    )

    assert readme_names == skill_names
    assert html_names == skill_names
    assert f"{total_curated}+ 精选" in promo
    assert f"{len(skill_names)} 个原创" in promo
    assert f"{len(skill_names)} 个面向中文开发者的实用 AI 技能" in promo
    assert f"{len(skill_names)} 个实用的原创技能" in promo
    assert f"{len(skill_names)} 个可直接安装的原创中文技能" in llms


def test_discover_detail_pages_extracts_metadata_and_sorts_deterministically() -> None:
    """discover_detail_pages 应扫描 skills/p/c 三个目录、规范化元数据并按路径确定性排序。"""
    with tempfile.TemporaryDirectory() as temporary_directory:
        docs_dir = Path(temporary_directory)
        (docs_dir / "skills" / "skill-translator").mkdir(parents=True)
        (docs_dir / "p" / "baoyu-skills").mkdir(parents=True)
        (docs_dir / "p" / "archify").mkdir(parents=True)
        (docs_dir / "c" / "dev-workflow").mkdir(parents=True)
        (docs_dir / "p" / "ignored-dir").mkdir(parents=True)
        (docs_dir / "p" / "ignored-dir" / "notes.html").write_text("<title>ignore</title>", encoding="utf-8")

        (docs_dir / "skills" / "skill-translator" / "index.html").write_text(
            """<!DOCTYPE html>
<html lang="zh-CN"><head>
<title>skill-translator 中文详解 | Claude Code Skills</title>
<link rel="canonical" href="https://claude-skills.bt199.com/skills/skill-translator/">
<meta name="original-skill" content="skill-translator">
</head><body><h1>正文</h1></body></html>""",
            encoding="utf-8",
        )
        (docs_dir / "p" / "baoyu-skills" / "index.html").write_text(
            """<!DOCTYPE html>
<html lang="zh-CN"><head>
<title>baoyu-skills 中文详解与安装指南</title>
<meta content="https://github.com/JimLiu/baoyu-skills/" name="skill-repo">
<link href="https://claude-skills.bt199.com/p/baoyu-skills/" rel="canonical">
</head><body></body></html>""",
            encoding="utf-8",
        )
        (docs_dir / "p" / "archify" / "index.html").write_text(
            """<!DOCTYPE html>
<html lang="zh-CN"><head>
<title>archify 交互架构图中文指南</title>
<meta name="skill-repo" content="https://github.com/tt-a1i/archify">
<link rel="canonical" href="https://claude-skills.bt199.com/p/archify/">
</head><body></body></html>""",
            encoding="utf-8",
        )
        (docs_dir / "c" / "dev-workflow" / "index.html").write_text(
            """<!DOCTYPE html>
<html lang="zh-CN"><head>
<title>开发效率专题 | Claude Code Skills</title>
</head><body></body></html>""",
            encoding="utf-8",
        )

        pages = sync_readme_to_site.discover_detail_pages(docs_dir)
        assert [p["path"] for p in pages] == [
            "/c/dev-workflow/",
            "/p/archify/",
            "/p/baoyu-skills/",
            "/skills/skill-translator/",
        ]
        by_path = {p["path"]: p for p in pages}
        assert by_path["/p/baoyu-skills/"]["skill_repo"] == "https://github.com/jimliu/baoyu-skills"
        assert by_path["/p/baoyu-skills/"]["title"] == "baoyu-skills 中文详解与安装指南"
        assert by_path["/p/archify/"]["skill_repo"] == "https://github.com/tt-a1i/archify"
        assert by_path["/skills/skill-translator/"]["original_skill"] == "skill-translator"
        assert by_path["/skills/skill-translator/"]["skill_repo"] is None
        assert by_path["/c/dev-workflow/"]["url"] == "https://claude-skills.bt199.com/c/dev-workflow/"

        url_map = sync_readme_to_site.build_detail_url_map(pages)
        assert url_map == {
            "https://github.com/jimliu/baoyu-skills": "/p/baoyu-skills/",
            "https://github.com/tt-a1i/archify": "/p/archify/",
        }

        # 外站 canonical 必须 fail-closed
        (docs_dir / "p" / "bad-canonical").mkdir(parents=True)
        (docs_dir / "p" / "bad-canonical" / "index.html").write_text(
            '<head><link rel="canonical" href="https://evil.example/p/x/"></head>',
            encoding="utf-8",
        )
        try:
            sync_readme_to_site.discover_detail_pages(docs_dir)
        except ValueError as exc:
            assert "canonical" in str(exc)
        else:
            raise AssertionError("cross-origin canonical should fail closed")
        (docs_dir / "p" / "bad-canonical" / "index.html").unlink()

        # 重复 skill-repo 必须 fail-closed
        (docs_dir / "p" / "dup-archify").mkdir(parents=True)
        (docs_dir / "p" / "dup-archify" / "index.html").write_text(
            '<head><meta name="skill-repo" content="https://github.com/TT-A1I/ARCHIFY"></head>',
            encoding="utf-8",
        )
        _expect_runtime_error(
            lambda: sync_readme_to_site.discover_detail_pages(docs_dir),
            "重复",
        )


def test_generate_skills_js_injects_detail_url_and_validates_safe_paths() -> None:
    """generate_skills_js 应按规范化 GitHub URL 注入 detailUrl，并拒绝任何非安全站内路径。"""
    skills_data = {
        "star": [
            {
                "name": "JimLiu/baoyu-skills",
                "stars": "27.9K+",
                "desc": "宝玉技能集",
                "url": "https://github.com/JimLiu/baoyu-skills",
                "zhDoc": True,
            },
            {
                "name": "subpath-item",
                "stars": "1K+",
                "desc": "子路径不应误匹配根仓详情页",
                "url": "https://github.com/JimLiu/baoyu-skills/tree/main/skills/foo",
            },
        ],
        "dev": [
            {
                "name": "tt-a1i/archify",
                "stars": "99.7K+",
                "desc": "交互架构图",
                "url": "https://github.com/TT-A1I/Archify/",
            },
        ],
    }
    js = sync_readme_to_site.generate_skills_js(
        skills_data,
        detail_url_map={
            "https://github.com/jimliu/baoyu-skills": "/p/baoyu-skills/",
            "https://github.com/tt-a1i/archify": "/p/archify/",
        },
    )
    assert "name:'JimLiu/baoyu-skills',stars:'27.9K+',desc:'宝玉技能集',url:'https://github.com/JimLiu/baoyu-skills',zhDoc:true,detailUrl:'/p/baoyu-skills/',tag:'star'" in js
    assert "name:'subpath-item',stars:'1K+',desc:'子路径不应误匹配根仓详情页',url:'https://github.com/JimLiu/baoyu-skills/tree/main/skills/foo',tag:'star'" in js
    assert "name:'tt-a1i/archify',stars:'99.7K+',desc:'交互架构图',url:'https://github.com/TT-A1I/Archify/',detailUrl:'/p/archify/'" in js

    for unsafe_path in [
        "//evil.com/p/x/",
        "https://evil.com/p/x/",
        "javascript:alert(1)",
        "p/baoyu-skills/",
        "/p/../etc/passwd",
        "/p/baoyu?x=1",
        "/p/baoyu#frag",
        "/p/baoyu' onclick='alert(1)",
        "/",
        "",
    ]:
        try:
            sync_readme_to_site.generate_skills_js(
                {"dev": [{"name": "x", "stars": "1", "desc": "d", "url": "https://github.com/a/b"}]},
                detail_url_map={"https://github.com/a/b": unsafe_path},
            )
        except ValueError as exc:
            assert "详情页路径" in str(exc)
        else:
            raise AssertionError(f"unsafe detail path should fail closed: {unsafe_path!r}")


def test_sync_sitemap_xml_generates_multipage_and_is_idempotent() -> None:
    """多页 sitemap.xml 应生成首页(1.0/weekly)+详情页(0.8/monthly)，且无实质变化时完全幂等。"""
    initial_sitemap = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://claude-skills.bt199.com/</loc>
    <lastmod>2026-01-02</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    pages_v1 = [
        {"path": "/skills/skill-translator/", "title": "skill-translator"},
        {"path": "/p/baoyu-skills/", "title": "baoyu-skills"},
    ]
    day1 = datetime.date(2026, 7, 15)
    generated_v1 = sync_readme_to_site.sync_sitemap_xml(
        initial_sitemap, pages_v1, project_date=day1, update_date=True
    )

    assert "<loc>https://claude-skills.bt199.com/</loc>" in generated_v1
    assert "<changefreq>weekly</changefreq>" in generated_v1
    assert "<priority>1.0</priority>" in generated_v1
    assert "<loc>https://claude-skills.bt199.com/p/baoyu-skills/</loc>" in generated_v1
    assert "<loc>https://claude-skills.bt199.com/skills/skill-translator/</loc>" in generated_v1
    assert generated_v1.count("<changefreq>monthly</changefreq>") == 2
    assert generated_v1.count("<priority>0.8</priority>") == 2
    assert generated_v1.count("<lastmod>2026-07-15</lastmod>") == 3
    assert generated_v1.index("/p/baoyu-skills/") < generated_v1.index("/skills/skill-translator/")

    # 第二天无变化：update_date=False 必须字节完全一致（不改动任何 lastmod）
    day2 = datetime.date(2026, 7, 16)
    noop_check = sync_readme_to_site.sync_sitemap_xml(
        generated_v1, pages_v1, project_date=day2, update_date=False
    )
    assert noop_check == generated_v1

    # 第二天新增 1 个详情页：已有详情页保留旧 lastmod，新页面和首页写入 day2
    pages_v2 = pages_v1 + [{"path": "/p/archify/", "title": "archify"}]
    generated_v2 = sync_readme_to_site.sync_sitemap_xml(
        generated_v1, pages_v2, project_date=day2, update_date=True
    )
    assert (
        "<loc>https://claude-skills.bt199.com/</loc>\n    <lastmod>2026-07-16</lastmod>"
        in generated_v2
    )
    assert (
        "<loc>https://claude-skills.bt199.com/p/archify/</loc>\n    <lastmod>2026-07-16</lastmod>"
        in generated_v2
    )
    assert (
        "<loc>https://claude-skills.bt199.com/p/baoyu-skills/</loc>\n    <lastmod>2026-07-15</lastmod>"
        in generated_v2
    )

    # CRLF 保留
    crlf_v1 = generated_v1.replace("\n", "\r\n")
    assert (
        sync_readme_to_site.sync_sitemap_xml(
            crlf_v1, pages_v1, project_date=day2, update_date=False
        )
        == crlf_v1
    )


def test_update_llms_detail_pages_syncs_index_and_fails_closed() -> None:
    """docs/llms.txt 详情页索引区块应自动同步、幂等，且标记缺失/重复/倒序均 fail-closed。"""
    base_llms = (
        "> 面向中文开发者的精选仓库，收录 3+ 个精选技能，另含 2 个可直接安装的原创中文技能。\n\n"
        "## 独立中文详解页\n\n"
        "<!-- detail-pages-start -->\n"
        "- old\n"
        "<!-- detail-pages-end -->\n"
    )
    pages = [
        {"path": "/skills/skill-translator/", "title": "skill-translator [原创] 指南"},
        {"path": "/p/baoyu-skills/", "title": "baoyu-skills 中文详解"},
    ]
    updated = sync_readme_to_site.update_llms_detail_pages(base_llms, pages)
    assert "- [baoyu-skills 中文详解](https://claude-skills.bt199.com/p/baoyu-skills/)" in updated
    assert (
        "- [skill-translator \\[原创\\] 指南](https://claude-skills.bt199.com/skills/skill-translator/)"
        in updated
    )
    assert updated.index("/p/baoyu-skills/") < updated.index("/skills/skill-translator/")

    empty_updated = sync_readme_to_site.update_llms_detail_pages(base_llms, [])
    assert "暂无已发布的独立中文详解页" in empty_updated

    # CRLF 保留
    crlf_llms = updated.replace("\n", "\r\n")
    assert sync_readme_to_site.update_llms_detail_pages(crlf_llms, pages) == crlf_llms

    # 标记异常必须 fail-closed
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_llms_detail_pages("no markers", pages),
        "标记校验失败",
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_llms_detail_pages(
            "<!-- detail-pages-end -->\n<!-- detail-pages-start -->\n", pages
        ),
        "顺序错误",
    )
    _expect_runtime_error(
        lambda: sync_readme_to_site.update_llms_detail_pages(
            base_llms + "<!-- detail-pages-start -->\n", pages
        ),
        "标记校验失败",
    )

    # 端到端 build_sync_outputs 多页联动 + 幂等检查
    readme, html, _sitemap, promo, _llms, skills_js = _public_sync_fixture()
    sitemap_v0 = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://claude-skills.bt199.com/</loc>
    <lastmod>2026-01-02</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
"""
    r1, h1, s1, p1, l1, changed1 = sync_readme_to_site.build_sync_outputs(
        readme,
        html,
        sitemap_v0,
        promo,
        base_llms,
        skills_js=skills_js,
        total_skills=3,
        repo_stars=9,
        total_original=2,
        project_date=datetime.date(2026, 7, 15),
        detail_pages=pages,
    )
    assert changed1 is True
    assert "<loc>https://claude-skills.bt199.com/p/baoyu-skills/</loc>" in s1
    assert "https://claude-skills.bt199.com/p/baoyu-skills/" in l1

    # 次日无新增/改动时完全幂等，不改日期
    r2, h2, s2, p2, l2, changed2 = sync_readme_to_site.build_sync_outputs(
        r1,
        h1,
        s1,
        p1,
        l1,
        skills_js=skills_js,
        total_skills=3,
        repo_stars=9,
        total_original=2,
        project_date=datetime.date(2026, 7, 16),
        detail_pages=pages,
    )
    assert changed2 is False
    assert (r2, h2, s2, p2, l2) == (r1, h1, s1, p1, l1)


def test_checked_in_llms_has_valid_detail_pages_markers() -> None:
    """仓库内 docs/llms.txt 必须包含唯一且顺序正确的详情页起止标记。"""
    llms = (REPO_ROOT / "docs" / "llms.txt").read_text(encoding="utf-8")
    assert llms.count(sync_readme_to_site.LLMS_DETAIL_PAGES_START) == 1
    assert llms.count(sync_readme_to_site.LLMS_DETAIL_PAGES_END) == 1
    assert llms.index(sync_readme_to_site.LLMS_DETAIL_PAGES_START) < llms.index(
        sync_readme_to_site.LLMS_DETAIL_PAGES_END
    )


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
    test_readme_fact_summary_counts_are_synced()
    test_readme_fact_summary_original_count_is_synced()
    test_update_promo_counts_refreshes_all_occurrences()
    test_update_promo_counts_fails_closed_on_missing_anchor()
    test_update_promo_counts_fails_closed_on_duplicate_anchor()
    test_academic_category_is_independent_and_synced()
    test_zh_doc_flag_preserved_only_when_marked_after_link()
    test_strip_inline_markdown_cleans_bold_and_backticks_while_keeping_escaping()
    test_refresh_readme_stars_syncs_comparison_table_external_repos()
    test_update_llms_counts_syncs_curated_and_original_and_fails_closed()
    test_promo_or_llms_only_change_triggers_material_changed()
    test_html_optional_nav_stars_and_jsonld_faq_anchors()
    test_sync_script_hygiene_no_raw_control_chars_or_stale_original_default()
    test_original_skill_sets_and_promo_counts_are_consistent()
    test_discover_detail_pages_extracts_metadata_and_sorts_deterministically()
    test_generate_skills_js_injects_detail_url_and_validates_safe_paths()
    test_sync_sitemap_xml_generates_multipage_and_is_idempotent()
    test_update_llms_detail_pages_syncs_index_and_fails_closed()
    test_checked_in_llms_has_valid_detail_pages_markers()
    print("PASS: sync_readme_to_site.py regression tests")
