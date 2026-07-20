const https = require('https');
const fs = require('fs');
const os = require('os');
const path = require('path');

const COOKIE_FILE = process.env.JUEJIN_COOKIE_FILE || path.join(os.homedir(), '.hermes', 'projects', 'claude-code-skills-zh', '.juejin_cookie');
const COOKIE = process.env.JUEJIN_COOKIE || (fs.existsSync(COOKIE_FILE) ? fs.readFileSync(COOKIE_FILE, 'utf-8').trim() : '');
const TEMP_DIR = path.join(__dirname, '..', '.tmp');
fs.mkdirSync(TEMP_DIR, { recursive: true });
const ERROR_SCREENSHOT = path.join(TEMP_DIR, 'juejin_error.png');
const RESULT_SCREENSHOT = path.join(TEMP_DIR, 'juejin_result.png');
const RESULT_JSON = path.join(TEMP_DIR, 'juejin_result.json');

const rawArgs = process.argv.slice(2);
const shouldPublish = rawArgs.includes('--publish');
const args = rawArgs.filter(arg => arg !== '--publish');
const TITLE = args[0];
const CONTENT_FILE = args[1];
const CATEGORY = args[2] || '开发工具';

if (!TITLE || !CONTENT_FILE) {
  console.error('用法: node post_to_juejin.js "标题" "内容文件路径" [分类] [--publish]');
  process.exit(1);
}

if (!fs.existsSync(CONTENT_FILE)) {
  console.error(`❌ 内容文件不存在: ${CONTENT_FILE}`);
  process.exit(1);
}

if (!shouldPublish) {
  const preview = fs.readFileSync(CONTENT_FILE, 'utf-8');
  console.log('✅ 预检完成，未创建草稿、未发布文章。');
  console.log(`标题: ${TITLE}`);
  console.log(`分类: ${CATEGORY}`);
  console.log(`正文字符数: ${preview.length}`);
  console.log('确认内容后追加 --publish 才会访问掘金并产生外部状态。');
  process.exit(0);
}

if (!COOKIE) {
  console.error('❌ 缺少掘金 Cookie：请设置 JUEJIN_COOKIE 或写入 .juejin_cookie（不要提交 Cookie 到仓库）');
  process.exit(1);
}

const { chromium } = require('playwright');

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
  const content = fs.readFileSync(CONTENT_FILE, 'utf-8');

  // Step 1: 创建草稿
  console.log('📝 Step 1: 创建草稿...');
  const draftResp = await apiPost('/content_api/v1/article_draft/create', {
    title: TITLE,
    mark_content: content,
    brief_content: content.replace(/[#*`>]/g, '').replace(/\n/g, ' ').trim().slice(0, 100).padEnd(50, '。'),
    edit_type: 10,
    category_id: '6809640410229036040',
    tag_ids: ['6809640375880253447'],
    cover_image: '',
    link_url: '',
  });

  if (draftResp.err_no !== 0) {
    console.log('❌ 草稿创建失败:', draftResp.err_msg);
    process.exit(1);
  }

  const draftId = draftResp.data.id;
  console.log(`✅ 草稿创建成功: ${draftId}`);

  // Step 2: 用浏览器发布
  console.log('\n🚀 Step 2: 用浏览器发布...');
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 800 },
  });

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

  // 打开草稿编辑页
  await page.goto(`https://juejin.cn/editor/drafts/${draftId}`, { waitUntil: 'networkidle', timeout: 30000 });
  await page.waitForTimeout(3000);

  // 点击右上角的"发布"按钮打开发布面板
  const publishTopBtn = await page.$('button:has-text("发布")');
  if (publishTopBtn) {
    await publishTopBtn.click();
    await page.waitForTimeout(2000);
    console.log('✅ 已打开发布面板');
  } else {
    console.log('❌ 未找到发布按钮');
    await page.screenshot({ path: ERROR_SCREENSHOT });
    await browser.close();
    process.exit(1);
  }

  // 选择分类（点击分类按钮）
  console.log(`📌 选择分类: ${CATEGORY}`);
  const categoryBtn = await page.$(`text=${CATEGORY}`);
  if (categoryBtn) {
    await categoryBtn.click();
    await page.waitForTimeout(1000);
    console.log('✅ 分类已选择');
  } else {
    console.log(`❌ 未找到指定分类: ${CATEGORY}`);
    await page.screenshot({ path: ERROR_SCREENSHOT });
    await browser.close();
    process.exit(1);
  }

  // 确保摘要至少50字
  const briefInput = await page.$('textarea[placeholder*="摘要"], input[placeholder*="摘要"]');
  if (briefInput) {
    const briefText = content.replace(/[#*`>]/g, '').replace(/\n/g, ' ').trim().slice(0, 100);
    const brief50 = briefText.length >= 50 ? briefText : briefText + '。这是一篇实用的技术分享文章，建议收藏。'.slice(0, 100);
    await briefInput.fill(brief50);
    console.log(`✅ 已更新摘要 (${brief50.length}字)`);
  }

  await page.waitForTimeout(1000);

  // 等待面板加载
  await page.waitForTimeout(2000);

  // 点击"确定并发布"按钮 - 用多种方式尝试
  try {
    // 方式1: 用 locator 精确匹配
    const confirmBtn = page.locator('button:has-text("确定并发布")');
    if (await confirmBtn.count() > 0) {
      await confirmBtn.last().click();
      console.log('✅ 已点击确定并发布按钮 (locator)');
    }
  } catch(e) {
    console.log('locator 方式失败:', e.message);
  }

  await page.waitForTimeout(3000);

  // 检查是否需要再点击（可能弹了确认框）
  const confirmDialog = await page.$('button:has-text("确认发布"), button:has-text("继续发布")');
  if (confirmDialog) {
    await confirmDialog.click();
    console.log('✅ 已点击确认对话框');
    await page.waitForTimeout(3000);
  }

  // 截图
  await page.screenshot({ path: RESULT_SCREENSHOT, fullPage: false });

  // 检查最终状态
  const finalUrl = page.url();
  console.log(`📍 最终 URL: ${finalUrl}`);

  if (finalUrl.includes('/post/')) {
    const articleId = finalUrl.match(/post\/(\d+)/)?.[1];
    console.log(`🎉 发布成功! 文章链接: https://juejin.cn/post/${articleId}`);
    // 写入结果供外部使用
    fs.writeFileSync(RESULT_JSON, JSON.stringify({ success: true, article_id: articleId, url: `https://juejin.cn/post/${articleId}` }));
  } else {
    // 检查是否有成功提示
    const successTip = await page.$('text=发布成功');
    if (successTip) {
      console.log('🎉 发布成功（检测到成功提示）');
      fs.writeFileSync(RESULT_JSON, JSON.stringify({ success: true }));
    } else {
      console.log(`⚠️ 无法确认发布状态，请查看截图 ${RESULT_SCREENSHOT}`);
      fs.writeFileSync(RESULT_JSON, JSON.stringify({ success: false, note: '需人工确认' }));
    }
  }

  await browser.close();
}

main().catch(e => { console.error('❌ Error:', e.message); process.exit(1); });
