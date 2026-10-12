// TASARIM-2 (3) kör yargı ekran görüntüsü: headless puppeteer (frontend-craft'ın kendi bağımlılığı, pencere yok), 1440 genişlik, ilk 2700px.
// Kullanım: node kor.mjs <index.html> <cikti.png> [<index.html> <cikti.png> ...]
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';

const fc = new URL('../../plugins/frontend-craft/skills/frontend-craft/scripts/slop.mjs', import.meta.url);
const { default: puppeteer } = await import(pathToFileURL(createRequire(fc).resolve('puppeteer')).href);
const arg = process.argv.slice(2);
const tarayici = await puppeteer.launch({ headless: true });
for (let i = 0; i < arg.length; i += 2) {
  const sayfa = await tarayici.newPage();
  await sayfa.setViewport({ width: 1440, height: 900 });
  await sayfa.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await sayfa.goto(pathToFileURL(arg[i]).href, { waitUntil: 'load', timeout: 30000 });
  // IntersectionObserver ile gelen içerik görünür olsun diye sayfayı baştan sona kaydır
  const h = await sayfa.evaluate(() => document.documentElement.scrollHeight);
  for (let y = 0; y < h; y += 600) await sayfa.evaluate((y) => window.scrollTo(0, y), y);
  await sayfa.evaluate(() => window.scrollTo(0, 0));
  await new Promise((r) => setTimeout(r, 800));
  await sayfa.screenshot({ path: arg[i + 1], clip: { x: 0, y: 0, width: 1440, height: Math.min(h, 2700) } });
  await sayfa.close();
}
await tarayici.close();
