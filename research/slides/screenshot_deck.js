const { chromium } = require('/home/nando/.npm-global/lib/node_modules/@playwright/cli/node_modules/playwright');
const PRES = 'https://docs.google.com/presentation/d/1Ws2piUxYrFDbYogsCUjbOKHUnMcxjzYaPIAkqYIFxeQ';
(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const ctx = browser.contexts()[0];
  const page = await ctx.newPage();
  await page.setViewportSize({ width: 1600, height: 900 });
  await page.goto(PRES + '/present?rm=minimal', { waitUntil: 'networkidle', timeout: 90000 }).catch(e=>console.log('nav warn', e.message));
  await page.waitForTimeout(6000);
  const total = await page.evaluate(() => { return document.title; }).catch(()=> '');
  for (let i = 1; i <= 12; i++) {
    await page.waitForTimeout(1400);
    await page.screenshot({ path: `/home/nando/Source/work/Madisoft/openrouter-adoption/research/slides/slide_${String(i).padStart(2,'0')}.png` });
    if (i < 12) { await page.keyboard.press('ArrowRight'); await page.waitForTimeout(600); }
  }
  await page.close();
  await browser.close();
  console.log('done', total);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
