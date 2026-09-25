#!/usr/bin/env node
/**
 * Collect OpenRouter dashboard data by connecting to an existing Chrome
 * via remote debugging (http://localhost:9222). Uses the puppeteer module
 * from the chrome-devtools skill scripts node_modules.
 */
import puppeteer from '/home/nando/.config/opencode/skills/chrome-devtools/scripts/node_modules/puppeteer/lib/esm/puppeteer/puppeteer.js';

const TARGET_URL = process.argv[2] || 'https://openrouter.ai/activity';

async function main() {
  const browser = await puppeteer.connect({
    browserURL: 'http://localhost:9222',
    defaultViewport: null
  });
  const pages = await browser.pages();
  let page = pages.find(p => p.url().includes('openrouter.ai')) || pages[0];
  await page.bringToFront();

  // Navigate to the target URL in the connected tab
  await page.goto(TARGET_URL, { waitUntil: 'networkidle2', timeout: 60000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 2500));

  const data = await page.evaluate(() => {
    const txt = (el) => (el ? el.innerText.replace(/\s+/g, ' ').trim() : '');
    const rows = [];
    document.querySelectorAll('tr').forEach(tr => {
      const cells = Array.from(tr.querySelectorAll('td,th')).map(c => txt(c));
      rows.push(cells);
    });
    return {
      url: location.href,
      title: document.title,
      bodyText: document.body.innerText.slice(0, 6000),
      tableRows: rows.slice(0, 60)
    };
  });

  console.log(JSON.stringify(data, null, 2));
  await browser.disconnect();
}

main().catch(e => { console.error(JSON.stringify({ success: false, error: e.message }, null, 2)); process.exit(1); });
