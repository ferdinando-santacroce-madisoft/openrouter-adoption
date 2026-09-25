#!/usr/bin/env node
/**
 * Collect OpenRouter dashboard data by connecting to an existing browser
 * via CDP (http://localhost:9222) using Playwright.
 * Usage: node collect-pw.js "<url>"
 */
const { chromium } = require('/home/nando/.npm-global/lib/node_modules/@playwright/cli/node_modules/playwright');

const TARGET = process.argv[2] || 'https://openrouter.ai/activity';

(async () => {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const ctx = browser.contexts()[0];
  const pages = ctx.pages();
  let page = pages.find(p => p.url().includes('openrouter.ai')) || pages[0];
  await page.bringToFront();

  if (!page.url().startsWith('http')) {
    await page.goto(TARGET, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  } else if (!page.url().includes(TARGET.replace(/^https?:\/\/[^/]*/, ''))) {
    await page.goto(TARGET, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
  }
  await page.waitForTimeout(2500);

  const data = await page.evaluate(() => {
    const txt = (el) => (el ? el.innerText.replace(/\s+/g, ' ').trim() : '');
    const rows = [];
    document.querySelectorAll('tr').forEach(tr => {
      rows.push(Array.from(tr.querySelectorAll('td,th')).map(c => txt(c)));
    });
    return {
      url: location.href,
      title: document.title,
      bodyText: document.body.innerText.slice(0, 8000),
      tableRows: rows.slice(0, 80),
      links: Array.from(document.querySelectorAll('a')).slice(0,80).map(a => ({t: txt(a), h: a.href}))
    };
  });

  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})().catch(e => { console.error(JSON.stringify({ success: false, error: e.message }, null, 2)); process.exit(1); });
