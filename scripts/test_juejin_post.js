const { chromium } = require('playwright');
const https = require('https');

const COOKIE = 's_v_web_id=verify_mnyghpv1_2nb3ituQ_Qu90_4aKY_86Ix_VKyTjxNrYjIU;_tea_utm_cache_2608=undefined;__tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227628554038237218339%2522%252C%2522user_unique_id%2522%253A%25227628554038237218339%2522%252C%2522timestamp%2522%253A1776161154712%257D;passport_csrf_token=dc2c4740f403fd1bf4fede7d5d447888;passport_csrf_token_default=dc2c4740f403fd1bf4fede7d5d447888;odin_tt=4d5fd13504789f72028b22e1934879897c39b23ddca230f2ce510f1b8966a35f59698e6d4c34655068ae7fd040f4caaf3b7dd9da812c55202e43af250c96dd9a;n_mh=YWU8yCoGLpZjom3SqQ1Ylh7b87QnMl2ZnsghqSBcj44;passport_auth_status=8618318468ea7a9de4390b92eb104670%2C;passport_auth_status_ss=8618318468ea7a9de4390b92eb104670%2C;sid_guard=bc0ee3eed82ba004bec74f38e9be1717%7C1776161184%7C31536000%7CWed%2C+14-Apr-2027+10%3A06%3A24+GMT;uid_tt=26bb4609cb393e9932c7866da91058db;uid_tt_ss=26bb4609cb393e9932c7866da91058db;sid_tt=bc0ee3eed82ba004bec74f38e9be1717;sessionid=bc0ee3eed82ba004bec74f38e9be1717;sessionid_ss=bc0ee3eed82ba004bec74f38e9be1717;session_tlb_tag=sttt%7C10%7CvA7j7tgroAS-x0846b4XF__________J9YGaDxtrJdQfckj62q5Zs1qboODOjsTl-Stfiwtfmn4%3D;is_staff_user=false;has_biz_token=false;sid_ucp_v1=1.0.0-KGIzZDVkMzc4ZDU5MjFhYzgxN2I5YThiOTU3MWE5MGJjZGJlYWRiM2MKFgjK9sCI3q1GEKCj-M4GGLAUOAJA7AcaAmxmIiBiYzBlZTNlZWQ4MmJhMDA0YmVjNzRmMzhlOWJlMTcxNw;ssid_ucp_v1=1.0.0-KGIzZDVkMzc4ZDU5MjFhYzgxN2I5YThiOTU3MWE5MGJjZGJlYWRiM2MKFgjK9sCI3q1GEKCj-M4GGLAUOAJA7AcaAmxmIiBiYzBlZTNlZWQ4MmJhMDA0YmVjNzRmMzhlOWJlMTcxNw;_tea_utm_cache_576092=undefined';

// 测试文章
const TITLE = '测试文章-请忽略';
const CONTENT = '# 测试\n\n这是一篇测试文章，验证自动发文流程。请忽略此文章。';

async function apiPost(path, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const req = https.request({
      hostname: 'api.juejin.cn',
      path: path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://juejin.cn/',
        'Origin': 'https://juejin.cn',
        'Content-Length': Buffer.byteLength(data),
      },
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch(e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  // Step 1: 创建草稿
  console.log('📝 Step 1: 创建草稿...');
  const draftResp = await apiPost('/content_api/v1/article_draft/create', {
    title: TITLE,
    mark_content: CONTENT,
    brief_content: '测试文章',
    edit_type: 10,
    category_id: '6809640410229036040',
    tag_ids: ['6809640375880253447'],
    cover_image: '',
    link_url: '',
  });

  if (draftResp.err_no !== 0) {
    console.log('❌ 草稿创建失败:', draftResp.err_msg);
    return;
  }

  const draftId = draftResp.data.id;
  console.log(`✅ 草稿创建成功: ${draftId}`);
  console.log(`🔗 编辑链接: https://juejin.cn/editor/drafts/${draftId}`);

  // Step 2: 用浏览器打开草稿并发布
  console.log('\n🚀 Step 2: 用浏览器发布...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  // 设置 cookies
  const cookies = COOKIE.split(';').filter(c => c.trim()).map(c => {
    const idx = c.indexOf('=');
    if (idx === -1) return null;
    return {
      name: c.substring(0, idx).trim(),
      value: c.substring(idx + 1).trim(),
      domain: '.juejin.cn',
      path: '/',
    };
  }).filter(Boolean);
  await context.addCookies(cookies);

  const page = await context.newPage();
  await page.goto(`https://juejin.cn/editor/drafts/${draftId}`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(5000);

  // 截图看看页面状态
  await page.screenshot({ path: '/tmp/juejin_draft.png', fullPage: false });
  console.log('📸 页面截图已保存到 /tmp/juejin_draft.png');

  // 查找并点击发布按钮
  const publishBtn = await page.$('button:has-text("发布")');
  if (publishBtn) {
    await publishBtn.click();
    console.log('✅ 已点击发布按钮');
    await page.waitForTimeout(5000);

    // 再截图
    await page.screenshot({ path: '/tmp/juejin_published.png', fullPage: false });
    console.log('📸 发布后截图已保存到 /tmp/juejin_published.png');

    // 检查 URL 是否跳转到文章页
    const finalUrl = page.url();
    console.log(`📍 最终 URL: ${finalUrl}`);
    if (finalUrl.includes('/post/')) {
      const articleId = finalUrl.match(/post\/(\d+)/)?.[1];
      console.log(`🎉 发布成功! 文章链接: https://juejin.cn/post/${articleId}`);
    }
  } else {
    console.log('❌ 未找到发布按钮');
    // 打印页面上的所有按钮
    const buttons = await page.$$eval('button', btns => btns.map(b => b.textContent?.trim()).filter(Boolean));
    console.log('页面按钮:', buttons);
  }

  await browser.close();
}

main().catch(console.error);
