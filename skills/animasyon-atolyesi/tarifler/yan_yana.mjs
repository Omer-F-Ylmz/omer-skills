// Hazır-önce yan yana deneme: node yan_yana.mjs <ad> <bizim-yol> <hazir-yol> [kare=60] [cikti=.] [kok=http://127.0.0.1:8765]
// İki sayfa da sözleşmeye uyar: window.__hazir = true (durağan/kendi döngüsü) ya da window.__T = { hazir, adim(dt, n), olc?(ms) } (sabit adım).
// Çıktı: <cikti>/hazir-<ad>.png (sol bizim, sağ hazır, etiketli) + <cikti>/olcum.json[<ad>].
// Ölçü: p2–p98 parlaklık, artık = |L − medyan3×3(L)| > 12 piksel sayısı, kare süresi ort / p95 (?oto'suz, 3 sn; ekran tazelemesinde doyar).
// Bağımlılık: playwright-core + sharp (projede kurulu olmalı), Chrome kanalı; Git Bash'te MSYS_NO_PATHCONV=1 (yoksa /yol → C:/Program Files/Git/yol).
import { chromium } from 'playwright-core';
import sharp from 'sharp';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const [ad, bizim, hazir, n = 60, cikti = '.', kok = 'http://127.0.0.1:8765'] = process.argv.slice(2);
if (!hazir) { console.error('kullanım: node yan_yana.mjs <ad> <bizim-yol> <hazir-yol> [kare] [cikti] [kok]'); process.exit(2); }
const W = 1280, H = 800, ek = (u, q) => u + (u.includes('?') ? '&' : '?') + q;
const b = await chromium.launch({ channel: 'chrome', headless: true, args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist'] });
const hatalar = [];

async function cek(yol) {
  const p = await b.newPage({ viewport: { width: W, height: H } });
  p.on('pageerror', e => hatalar.push(`${yol}: ${e.message}`));
  await p.goto(kok + ek(yol, 'oto=1'));
  await p.waitForFunction(() => window.__T?.hazir || window.__hazir, null, { timeout: 30000 });
  if (await p.evaluate(() => !!window.__T)) await p.evaluate(n => window.__T.adim(1 / 60, n), +n); else await p.waitForTimeout(1500);
  const png = await p.screenshot();
  await p.close();
  const p2 = await b.newPage({ viewport: { width: W, height: H } });
  await p2.goto(kok + yol);
  await p2.waitForFunction(() => window.__T?.hazir || window.__hazir, null, { timeout: 30000 });
  await p2.waitForTimeout(800);
  const fps = await p2.evaluate(() => window.__T?.olc ? window.__T.olc(3000) : new Promise(res => { const o = []; const f = now => { o.push(now); if (now - o[0] < 3000) requestAnimationFrame(f); else { const d = o.slice(1).map((x, i) => x - o[i]).sort((a, b) => a - b); res({ fps: +(1000 / (d.reduce((a, b) => a + b, 0) / d.length)).toFixed(1), p95: +d[Math.floor(d.length * 0.95)].toFixed(2), n: d.length }); } }; requestAnimationFrame(f); }));
  await p2.close();
  return { png, fps, ...(await olc(png)) };
}

async function olc(png) {
  const gri = s => s.greyscale().toColourspace('b-w').raw().toBuffer();
  const L = await gri(sharp(png).removeAlpha()), M = await gri(sharp(png).removeAlpha().median(3));
  const h = new Array(256).fill(0); let artik = 0;
  for (let i = 0; i < L.length; i++) { h[L[i]]++; if (Math.abs(L[i] - M[i]) > 12) artik++; }
  const yuzde = q => { let s = 0; for (let v = 0; v < 256; v++) if ((s += h[v]) >= q * L.length) return v; };
  return { p2: yuzde(0.02), p98: yuzde(0.98), artik };
}

const A = await cek(bizim), B = await cek(hazir);
await b.close();
const etiket = (s, x) => ({ input: Buffer.from(`<svg width="${W}" height="40"><text x="16" y="28" font-family="sans-serif" font-size="20" fill="#3a2a1e">${s}</text></svg>`), left: x, top: 0 });
await sharp({ create: { width: 2 * W, height: H, channels: 3, background: '#000' } })
  .composite([{ input: A.png, left: 0, top: 0 }, { input: B.png, left: W, top: 0 },
    etiket(`BİZİM · p2–p98 ${A.p2}–${A.p98} · artık ${A.artik} · p95 ${A.fps.p95} ms`, 0),
    etiket(`HAZIR (${ad}) · p2–p98 ${B.p2}–${B.p98} · artık ${B.artik} · p95 ${B.fps.p95} ms`, W)])
  .png().toFile(join(cikti, `hazir-${ad}.png`));
const J = join(cikti, 'olcum.json'), kayit = existsSync(J) ? JSON.parse(readFileSync(J, 'utf8')) : {};
const oz = o => ({ p2: o.p2, p98: o.p98, artik: o.artik, fps: o.fps });
kayit[ad] = { bizim: { yol: bizim, ...oz(A) }, hazir: { yol: hazir, ...oz(B) }, kare: +n, hatalar };
writeFileSync(J, JSON.stringify(kayit, null, 1));
console.log(JSON.stringify(kayit[ad]));
