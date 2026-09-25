const { chromium } = require('/home/nando/.npm-global/lib/node_modules/@playwright/cli/node_modules/playwright');
const URL = process.argv[2] || 'https://openrouter.ai/activity';
(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  let page = pages.find(p => p.url().includes('openrouter.ai')) || pages[0];
  await page.bringToFront();
  const captured = [];
  page.on('response', async (resp) => {
    const url = resp.url();
    if ((url.includes('/api/') ) && /activity|usage|log|spend|perday|aggregate/i.test(url)) {
      try { const j = await resp.json(); captured.push({url, status: resp.status(), data: j}); } catch(e){}
    }
  });
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 }).catch(()=>{});
  await page.waitForTimeout(4000);
  console.log(JSON.stringify({captured: captured.slice(0,20)}, null, 2));
  await browser.close();
})().catch(e=>{console.error(JSON.stringify({success:false,error:e.message},null,2));process.exit(1);});
