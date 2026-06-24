const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  await page.goto('http://localhost:8000/index.html');
  await page.waitForTimeout(2000); // Wait for fonts and canvas to render
  await page.screenshot({ path: 'screenshot.png' });
  await browser.close();
})();
