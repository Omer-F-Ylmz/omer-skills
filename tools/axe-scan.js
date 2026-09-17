// node tools/axe-scan.js <url> → 390/768/1440 axe ihlalleri; exit 1 = ihlal var.
// Bağımlılıklar frontend-craft'ın node_modules'ından (puppeteer Chromium + @axe-core/puppeteer).
const path = require('node:path');
const { createRequire } = require('node:module');

const fc = createRequire(path.join(__dirname, '../plugins/frontend-craft/skills/frontend-craft/package.json'));
const puppeteer = fc('puppeteer');
const { AxePuppeteer } = fc('@axe-core/puppeteer');

const url = process.argv[2];
if (!url) {
  console.error('kullanım: node tools/axe-scan.js <url>');
  process.exit(2);
}

(async () => {
  const browser = await puppeteer.launch({ args: ['--ignore-certificate-errors'] });
  let total = 0;
  try {
    for (const w of [390, 768, 1440]) {
      const page = await browser.newPage();
      await page.setViewport({ width: w, height: 900 });
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 });
      const { violations } = await new AxePuppeteer(page).analyze();
      console.log(`== ${w}: ${violations.length}`);
      for (const v of violations) {
        console.log(`${v.id} · ${v.impact} · ${v.nodes.length} · ${v.nodes[0].target.join(' ')}`);
      }
      total += violations.length;
      await page.close();
    }
  } finally {
    await browser.close();
  }
  process.exit(total > 0 ? 1 : 0);
})();
