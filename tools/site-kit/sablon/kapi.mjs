// Kapı (TELVE R2e'den): dist'i süreç içi sunar; masaüstü · mobil · reduced-motion'da konsol/sayfa hatası, scroll boyunca
// kare süresi p95, ilk/toplam JS gz → kapi.esik.json karşılaştırması, kapi.json döküm. Chrome yoksa açık hata (çıkış 2).
import { createServer } from 'node:http';
import { readFileSync, readdirSync, existsSync, writeFileSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { gzipSync } from 'node:zlib';
import { chromium } from 'playwright-core';

const ESIK = JSON.parse(readFileSync('kapi.esik.json', 'utf8'));
const TIP = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.avif': 'image/avif', '.svg': 'image/svg+xml', '.woff2': 'font/woff2', '.glb': 'model/gltf-binary', '.hdr': 'application/octet-stream' };

const sunucu = createServer((q, s) => {
  let yol = join('dist', normalize(decodeURIComponent(new URL(q.url, 'http://x').pathname)));
  if (yol.endsWith('\\') || yol.endsWith('/')) yol = join(yol, 'index.html');
  if (!existsSync(yol)) return s.writeHead(404).end();
  s.writeHead(200, { 'content-type': TIP[extname(yol)] ?? 'application/octet-stream' }).end(readFileSync(yol));
}).listen(0);
const URL_ = `http://localhost:${sunucu.address().port}/`;

const js = Object.fromEntries(readdirSync('dist/_astro').filter((f) => f.endsWith('.js')).map((f) => [f, gzipSync(readFileSync(`dist/_astro/${f}`)).length]));
// shortcut: ilk yük parça adı desenine göre (sayfa betiği + gsap + ScrollTrigger); parça bölünmesi değişirse deseni güncelle
const ilk = Object.entries(js).filter(([f]) => /^(index|gsap|ScrollTrigger)/.test(f)).reduce((t, [, b]) => t + b, 0);
const toplam = Object.values(js).reduce((t, b) => t + b, 0);

let tarayici;
try {
  tarayici = await chromium.launch({ channel: 'chrome', headless: true });
} catch (e) {
  console.error(`Chrome bulunamadı (playwright-core channel 'chrome'): ${e.message.split('\n')[0]}`);
  sunucu.close();
  process.exit(2);
}

const sonuc = { js_kb_gz: { ilk: +(ilk / 1024).toFixed(1), toplam: +(toplam / 1024).toFixed(1) } };
for (const [ad, width, height, reducedMotion] of [['masaustu', 1440, 900, 'no-preference'], ['mobil', 390, 844, 'no-preference'], ['az_hareket', 1440, 900, 'reduce']]) {
  const ctx = await tarayici.newContext({ viewport: { width, height }, reducedMotion });
  const sayfa = await ctx.newPage();
  const hatalar = [];
  sayfa.on('console', (m) => m.type() === 'error' && hatalar.push(m.text()));
  sayfa.on('pageerror', (e) => hatalar.push(e.message));
  await sayfa.goto(URL_, { waitUntil: 'load' });
  await sayfa.waitForTimeout(1000);
  // 240 karede sayfa boyunca kaydır; her bölüm sahnesi yüklenip çalışır
  const p95 = await sayfa.evaluate(() => new Promise((bitti) => {
    const d = [], n = 240, H = document.documentElement.scrollHeight - innerHeight;
    let i = 0, t = performance.now();
    const kare = (simdi) => {
      d.push(simdi - t); t = simdi; scrollTo(0, (H * i) / n);
      if (++i < n) return requestAnimationFrame(kare);
      d.sort((a, b) => a - b);
      bitti(+d[Math.floor(d.length * 0.95)].toFixed(1));
    };
    requestAnimationFrame(kare);
  }));
  sonuc[ad] = { hata: hatalar.length, hatalar: hatalar.slice(0, 5), kare_p95_ms: p95 };
  await ctx.close();
}
await tarayici.close();
sunucu.close();

const kosullar = [
  ['hata', Math.max(...['masaustu', 'mobil', 'az_hareket'].map((k) => sonuc[k].hata)), ESIK.hata],
  ['kare_p95_ms', Math.max(sonuc.masaustu.kare_p95_ms, sonuc.mobil.kare_p95_ms), ESIK.kare_p95_ms],
  ['ilk_js_kb_gz', sonuc.js_kb_gz.ilk, ESIK.ilk_js_kb_gz],
  ['toplam_js_kb_gz', sonuc.js_kb_gz.toplam, ESIK.toplam_js_kb_gz],
];
writeFileSync('kapi.json', JSON.stringify(sonuc, null, 1));
let gecti = true;
for (const [ad, deger, esik] of kosullar) {
  const ok = deger <= esik;
  gecti &&= ok;
  console.log(`${ok ? 'GEÇTİ' : 'KALDI'}  ${ad} ${deger} (eşik ${esik})`);
}
process.exit(gecti ? 0 : 1);
