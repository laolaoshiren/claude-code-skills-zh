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
COOKIE_FULL = 's_v_web_id=verify_mnyghpv1_2nb3ituQ_Qu90_4aKY_86Ix_VKyTjxNrYjIU;_tea_utm_cache_2608=undefined;__tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227628554038237218339%2522%252C%2522user_unique_id%2522%253A%25227628554038237218339%2522%252C%2522timestamp%2522%253A1776161154712%257D;passport_csrf_token=dc2c4740f403fd1bf4fede7d5d447888;passport_csrf_token_default=dc2c4740f403fd1bf4fede7d5d447888;odin_tt=4d5fd13504789f72028b22e1934879897c39b23ddca230f2ce510f1b8966a35f59698e6d4c34655068ae7fd040f4caaf3b7dd9da812c55202e43af250c96dd9a;n_mh=YWU8yCoGLpZjom3SqQ1Ylh7b87QnMl2ZnsghqSBcj44;passport_auth_status=8618318468ea7a9de4390b92eb104670%2C;passport_auth_status_ss=8618318468ea7a9de4390b92eb104670%2C;sid_guard=bc0ee3eed82ba004bec74f38e9be1717%7C1776161184%7C31536000%7CWed%2C+14-Apr-2027+10%3A06%3A24+GMT;uid_tt=26bb4609cb393e9932c7866da91058db;uid_tt_ss=26bb4609cb393e9932c7866da91058db;sid_tt=bc0ee3eed82ba004bec74f38e9be1717;sessionid=bc0ee3eed82ba004bec74f38e9be1717;sessionid_ss=bc0ee3eed82ba004bec74f38e9be1717;session_tlb_tag=sttt%7C10%7CvA7j7tgroAS-x0846b4XF__________J9YGaDxtrJdQfckj62q5Zs1qboODOjsTl-Stfiwtfmn4%3D;is_staff_user=false;has_biz_token=false;sid_ucp_v1=1.0.0-KGIzZDVkMzc4ZDU5MjFhYzgxN2I5YThiOTU3MWE5MGJjZGJlYWRiM2MKFgjK9sCI3q1GEKCj-M4GGLAUOAJA7AcaAmxmIiBiYzBlZTNlZWQ4MmJhMDA0YmVjNzRmMzhlOWJlMTcxNw;ssid_ucp_v1=1.0.0-KGIzZDVkMzc4ZDU5MjFhYzgxN2I5YThiOTU3MWE5MGJjZGJlYWRiM2MKFgjK9sCI3q1GEKCj-M4GGLAUOAJA7AcaAmxmIiBiYzBlZTNlZWQ4MmJhMDA0YmVjNzRmMzhlOWJlMTcxNw;_tea_utm_cache_576092=undefined'


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
