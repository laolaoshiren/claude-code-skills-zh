const { chromium } = require('playwright');
const https = require('https');
const fs = require('fs');

const COOKIE_FILE = process.env.JUEJIN_COOKIE_FILE || `${process.env.HOME}/.hermes/projects/claude-code-skills-zh/.juejin_cookie`;
const COOKIE = process.env.JUEJIN_COOKIE || (fs.existsSync(COOKIE_FILE) ? fs.readFileSync(COOKIE_FILE, 'utf-8').trim() : '');

if (!COOKIE) {
  console.error('❌ 缺少掘金 Cookie：请设置 JUEJIN_COOKIE 或写入 .juejin_cookie（不要提交 Cookie 到仓库）');
  process.exit(1);
}

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
