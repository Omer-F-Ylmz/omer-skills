import puppeteer from 'puppeteer';
import fs from 'node:fs';

const [, , file] = process.argv;
if (!file) { console.error('kullanım: node olc-renk.mjs <referans.png>'); process.exit(1); }

// Piksel sayımı Chromium'da: yalnız yatayda VE dikeyde aynı renkli komşusu olan pikseller (düz alan) sayılır,
// kenar yumuşatma karışımları elenir. Renk profili dönüşümü kapalı: dosyadaki hex neyse o.
const browser = await puppeteer.launch();
const page = await browser.newPage();
const { total, colors } = await page.evaluate(async b64 => {
  const bytes = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
  const bmp = await createImageBitmap(new Blob([bytes]), { colorSpaceConversion: 'none', premultiplyAlpha: 'none' });
  const { width: W, height: H } = bmp;
  const ctx = new OffscreenCanvas(W, H).getContext('2d');
  ctx.drawImage(bmp, 0, 0);
  const d = ctx.getImageData(0, 0, W, H).data;
  const same = (a, b) => d[a] === d[b] && d[a + 1] === d[b + 1] && d[a + 2] === d[b + 2];
  const m = new Map();
  let total = 0;
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    const i = (y * W + x) * 4;
    if (d[i + 3] < 255) continue;
    total++;
    const h = (x > 0 && same(i, i - 4)) || (x < W - 1 && same(i, i + 4));
    const v = (y > 0 && same(i, i - 4 * W)) || (y < H - 1 && same(i, i + 4 * W));
    if (h && v) { const k = d[i] << 16 | d[i + 1] << 8 | d[i + 2]; m.set(k, (m.get(k) || 0) + 1); }
  }
  return { total, colors: [...m] };
}, fs.readFileSync(file).toString('base64'));
await browser.close();

// sRGB -> Lab (D65), CIEDE2000
const lin = c => (c /= 255) <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
const lab = k => {
  const [R, G, B] = [k >> 16, (k >> 8) & 255, k & 255].map(lin);
  const f = t => t > 216 / 24389 ? Math.cbrt(t) : (24389 / 27 * t + 16) / 116;
  const fx = f((0.4124564 * R + 0.3575761 * G + 0.1804375 * B) / 0.95047);
  const fy = f(0.2126729 * R + 0.7151522 * G + 0.072175 * B);
  const fz = f((0.0193339 * R + 0.119192 * G + 0.9503041 * B) / 1.08883);
  return [116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)];
};
const rad = Math.PI / 180;
const de2000 = ([L1, a1, b1], [L2, a2, b2]) => {
  const Cm = (Math.hypot(a1, b1) + Math.hypot(a2, b2)) / 2;
  const G = 0.5 * (1 - Math.sqrt(Cm ** 7 / (Cm ** 7 + 25 ** 7)));
  const A1 = (1 + G) * a1, A2 = (1 + G) * a2;
  const C1 = Math.hypot(A1, b1), C2 = Math.hypot(A2, b2);
  const hue = (a, b) => (a || b) ? (Math.atan2(b, a) / rad + 360) % 360 : 0;
  const h1 = hue(A1, b1), h2 = hue(A2, b2);
  let dh = C1 * C2 ? h2 - h1 : 0;
  if (dh > 180) dh -= 360; else if (dh < -180) dh += 360;
  const dH = 2 * Math.sqrt(C1 * C2) * Math.sin(dh * rad / 2);
  const Lm = (L1 + L2) / 2, Cpm = (C1 + C2) / 2;
  const hm = !(C1 * C2) ? h1 + h2 : Math.abs(h1 - h2) <= 180 ? (h1 + h2) / 2 : (h1 + h2 + (h1 + h2 < 360 ? 360 : -360)) / 2;
  const T = 1 - 0.17 * Math.cos((hm - 30) * rad) + 0.24 * Math.cos(2 * hm * rad) + 0.32 * Math.cos((3 * hm + 6) * rad) - 0.2 * Math.cos((4 * hm - 63) * rad);
  const Sl = 1 + 0.015 * (Lm - 50) ** 2 / Math.sqrt(20 + (Lm - 50) ** 2), Sc = 1 + 0.045 * Cpm, Sh = 1 + 0.015 * Cpm * T;
  const Rt = -Math.sin(60 * Math.exp(-(((hm - 275) / 25) ** 2)) * rad) * 2 * Math.sqrt(Cpm ** 7 / (Cpm ** 7 + 25 ** 7));
  return Math.sqrt(((L2 - L1) / Sl) ** 2 + ((C2 - C1) / Sc) ** 2 + (dH / Sh) ** 2 + Rt * ((C2 - C1) / Sc) * (dH / Sh));
};

// Gruplama: renkler sıklığa göre; ΔE2000 <= 5 olan en sık gruba katılır. Grubun hex'i en sık gerçek piksel rengidir, ortalama değil.
const groups = [];
for (const [k, n] of colors.sort((a, b) => b[1] - a[1])) {
  const L = lab(k);
  const g = groups.find(g => de2000(g.L, L) <= 5);
  if (g) g.n += n; else groups.push({ k, L, n });
}
// Payı %0.5 altındaki gruplar yazdırılmaz; en fazla 6, eksik kalırsa tamamlanmaz.
for (const g of groups.filter(g => g.n / total >= 0.005).sort((a, b) => b.n - a.n).slice(0, 6)) {
  console.log(`#${g.k.toString(16).padStart(6, '0')}  ${(g.n / total * 100).toFixed(2)}%`);
}
