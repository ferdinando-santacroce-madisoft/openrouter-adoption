const { chromium } = require('/home/nando/.npm-global/lib/node_modules/@playwright/cli/node_modules/playwright');
const URL = process.argv[2] || 'https://openrouter.ai/activity';
(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  let page = pages.find(p => p.url().includes('openrouter.ai')) || pages[0];
  await page.bringToFront();
  const urls = [];
  page.on('response', (resp) => { if (resp.url().includes('/api/')) urls.push(resp.url()); });
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 }).catch(()=>{});
  await page.waitForTimeout(4000);
  console.log(urls.join('\n'));
  await browser.close();
})().catch(e=>{console.error(JSON.stringify({success:false,error:e.message},null,2));process.exit(1);});
