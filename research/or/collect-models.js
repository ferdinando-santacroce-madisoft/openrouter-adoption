const { chromium } = require('/home/nando/.npm-global/lib/node_modules/@playwright/cli/node_modules/playwright');
const URL = process.argv[2] || 'https://openrouter.ai/activity';
(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  let page = pages.find(p => p.url().includes('openrouter.ai')) || pages[0];
  await page.bringToFront();
  await page.goto(URL, { waitUntil: 'networkidle', timeout: 60000 }).catch(()=>{});
  await page.waitForTimeout(3500);
  const data = await page.evaluate(() => {
    const out = { perModel: [], sections: [] };
    // Find model usage rows: labels with a model name followed by a $ value
    const all = Array.from(document.querySelectorAll('span,div,button'));
    // Heuristic: gather text blocks like "ModelName ... $X.XX"
    const texts = Array.from(document.querySelectorAll('*')).filter(e=>e.children.length===0).map(e=>e.innerText.trim()).filter(Boolean);
    // capture lines that look like model + amount
    out.lines = texts.slice(-120);
    // Try to read table-like structures for model spend
    document.querySelectorAll('table').forEach(t=>{
      const rows=Array.from(t.querySelectorAll('tr')).map(tr=>Array.from(tr.querySelectorAll('td,th')).map(c=>c.innerText.replace(/\s+/g,' ').trim()));
      out.sections.push({label:(t.previousElementSibling&&t.previousElementSibling.innerText.slice(0,60))||'', rows});
    });
    return out;
  });
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})().catch(e=>{console.error(JSON.stringify({success:false,error:e.message},null,2));process.exit(1);});
