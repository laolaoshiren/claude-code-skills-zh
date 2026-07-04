#!/usr/bin/env python3
"""Regression tests for sync_readme_to_site.py."""

from __future__ import annotations

import os
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


if __name__ == "__main__":
    test_dry_run_works_with_gbk_stdout()
    test_update_html_meta_refreshes_public_counts()
    test_update_html_badges_refreshes_update_date()
    print("PASS: sync_readme_to_site.py regression tests")
