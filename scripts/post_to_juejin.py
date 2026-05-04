#!/usr/bin/env python3.11
"""
掘金自动发文脚本 - 浏览器自动化方案
用法: python3.11 post_to_juejin.py "标题" "内容文件路径"
"""
import json
import sys
import os
import subprocess
import tempfile
from datetime import datetime

COOKIE_FILE = os.path.expanduser("~/.hermes/projects/claude-code-skills-zh/.juejin_cookie")


def load_cookie():
    """从环境变量或本地未跟踪文件读取 Cookie，避免把敏感信息提交到仓库。"""
    cookie = os.environ.get("JUEJIN_COOKIE")
    if cookie:
        return cookie.strip()
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    raise RuntimeError("缺少掘金 Cookie：请设置 JUEJIN_COOKIE 或写入 .juejin_cookie（不要提交 Cookie 到仓库）")


COOKIE_FULL = load_cookie()


def create_draft_via_api(title, content, category_id="6809640410229036040"):
    """通过 API 创建草稿（已验证可用）"""
    import requests
    resp = requests.post(
        "https://api.juejin.cn/content_api/v1/article_draft/create",
        headers={
            "Content-Type": "application/json",
            "Cookie": COOKIE_FULL,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://juejin.cn/",
            "Origin": "https://juejin.cn",
        },
        json={
            "title": title,
            "mark_content": content,
            "brief_content": content.replace("#", "").replace("*", "").replace("\n", " ").strip()[:200],
            "edit_type": 10,
            "category_id": category_id,
            "tag_ids": ["6809640375880253447"],
            "cover_image": "",
            "link_url": "",
        },
        timeout=30,
    )
    data = resp.json()
    if data.get("err_no") == 0:
        return data["data"]["id"]
    return None


def publish_via_browser(draft_id):
    """通过浏览器打开草稿并点击发布按钮"""
    # 构造 playwright 脚本
    js_code = f"""
const {{ chromium }} = require('playwright');

(async () => {{
    const browser = await chromium.launch({{ headless: true }});
    const context = await browser.newContext();
    const page = await context.newPage();

    // 设置 cookies
    const cookies = '{COOKIE_FULL}'.split(';').map(c => {{
        const [name, ...rest] = c.trim().split('=');
        return {{
            name: name,
            value: rest.join('='),
            domain: '.juejin.cn',
            path: '/',
        }};
    }}).filter(c => c.name && c.value);
    await context.addCookies(cookies);

    // 打开草稿编辑页
    await page.goto('https://juejin.cn/editor/drafts/{draft_id}', {{ waitUntil: 'networkidle' }});
    await page.waitForTimeout(3000);

    // 点击发布按钮
    const publishBtn = await page.$('text=发布');
    if (publishBtn) {{
        await publishBtn.click();
        await page.waitForTimeout(3000);
        console.log('✅ 已点击发布按钮');
    }} else {{
        console.log('❌ 未找到发布按钮');
    }}

    await browser.close();
}})();
"""

    # 写入临时文件并执行
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(js_code)
        tmp_file = f.name

    try:
        result = subprocess.run(
            ['node', tmp_file],
            capture_output=True, text=True, timeout=60
        )
        print(result.stdout)
        if result.stderr:
            print(f"stderr: {result.stderr}")
    finally:
        os.unlink(tmp_file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python3.11 post_to_juejin.py '标题' '内容文件路径'")
        sys.exit(1)

    title = sys.argv[1]
    content_file = sys.argv[2]

    with open(content_file, 'r') as f:
        content = f.read()

    print(f"📝 创建草稿: {title}")
    draft_id = create_draft_via_api(title, content)
    if draft_id:
        print(f"✅ 草稿创建成功: {draft_id}")
        print(f"🔗 草稿链接: https://juejin.cn/editor/drafts/{draft_id}")
        print("🚀 尝试通过浏览器发布...")
        publish_via_browser(draft_id)
    else:
        print("❌ 草稿创建失败")
