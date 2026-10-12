// AI-slop denetimi: sayfayı headless açar, ölçer (MEASURE), bayrakları sayar. Çıkış 1 = SLOP.
// Kullanım: node scripts/slop.mjs <url> [--json dosya]
// Eşikler 17 ödüllü/özgün sitenin ölçümünden (omer-skills docs/tasarim/olcum): 16'sı temiz, stripe 3 bayrak (AI'nın taklit ettiği kaynak).
import fs from 'node:fs';

// Sayfa içi ölçüm (page.evaluate). Yalnız sayılar/bayraklar döner.
export const MEASURE = () => {
  const vw = innerWidth, vh = innerHeight;
  const cv = document.createElement('canvas'); cv.__ttc = 'self'; cv.width = cv.height = 1;
  const cx = cv.getContext('2d', { willReadFrequently: true }); const cache = new Map();
  const rgba = c => { // her renk biçimini (oklch, color(), hex) rgba'ya indirger
    if (!c || c === 'transparent') return null; if (cache.has(c)) return cache.get(c);
    cx.clearRect(0, 0, 1, 1); cx.fillStyle = '#000'; cx.fillStyle = c; cx.fillRect(0, 0, 1, 1);
    const d = cx.getImageData(0, 0, 1, 1).data; const v = d[3] < 13 ? null : { r: d[0], g: d[1], b: d[2], a: d[3] / 255 };
    cache.set(c, v); return v;
  };
  const hex = v => '#' + [v.r, v.g, v.b].map(x => x.toString(16).padStart(2, '0')).join('');
  const hsl = v => { const r = v.r / 255, g = v.g / 255, b = v.b / 255, mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2;
    if (mx === mn) return { h: 0, s: 0, l }; const d = mx - mn, s = l > .5 ? d / (2 - mx - mn) : d / (mx + mn);
    const h = mx === r ? (g - b) / d + (g < b ? 6 : 0) : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; return { h: h * 60, s, l }; };
  const lum = v => { const f = x => { x /= 255; return x <= .03928 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4; }; return .2126 * f(v.r) + .7152 * f(v.g) + .0722 * f(v.b); };
  const contrast = (a, b) => { const x = lum(a), y = lum(b); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  const chroma = v => { const h = hsl(v); return h.s > .3 && h.l > .15 && h.l < .9 ? h : null; };

  const SKIP = new Set(['SCRIPT', 'STYLE', 'LINK', 'META', 'NOSCRIPT', 'TEMPLATE', 'HEAD', 'TITLE', 'BR']);
  const all = [...document.body.querySelectorAll('*')].filter(e => !SKIP.has(e.tagName) && !(e.closest('svg') && e.tagName !== 'svg'));
  const vis = [];
  for (const e of all) { if (vis.length >= 4000) break; const r = e.getBoundingClientRect(); if (r.width < 1 || r.height < 1) continue;
    const s = getComputedStyle(e); if (s.visibility !== 'visible' || +s.opacity < .05) continue; vis.push([e, s, r]); }
  const directText = e => { let t = ''; for (const n of e.childNodes) if (n.nodeType === 3) t += n.textContent; return t.trim(); };

  // --- tipografi
  const texts = vis.map(([e, s, r]) => ({ e, s, r, t: directText(e) })).filter(x => x.t.length);
  const fam = s => s.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase();
  const famChars = {}, sizeChars = {}; let maxPx = 0, totalChars = 0;
  for (const x of texts) { const f = fam(x.s), px = parseFloat(x.s.fontSize), n = x.t.length; totalChars += n;
    if (!/icon|awesome|material symbols/.test(f)) famChars[f] = (famChars[f] || 0) + n;
    if (px >= 10 && px <= 24) sizeChars[px] = (sizeChars[px] || 0) + n; if (px > maxPx) maxPx = px; }
  const fams = Object.entries(famChars).filter(([, n]) => n >= Math.max(3, totalChars * .005)).sort((a, b) => b[1] - a[1]).map(([f]) => f);
  const bodyPx = +(Object.entries(sizeChars).sort((a, b) => b[1] - a[1])[0] || [16])[0];
  const bodyEl = texts.filter(x => parseFloat(x.s.fontSize) === bodyPx).sort((a, b) => b.t.length - a.t.length)[0];
  let h1 = vis.find(([e]) => e.tagName === 'H1'); let h1Real = !!h1;
  if (!h1) { const top = texts.filter(x => x.r.top < vh && x.r.bottom > 0).sort((a, b) => parseFloat(b.s.fontSize) - parseFloat(a.s.fontSize))[0]; if (top) h1 = [top.e, top.s, top.r]; }
  const h1s = h1 ? h1[1] : null, h1Px = h1s ? parseFloat(h1s.fontSize) : 0;
  const lhRatio = s => s.lineHeight === 'normal' ? 1.2 : parseFloat(s.lineHeight) / parseFloat(s.fontSize);
  const lsEm = s => s.letterSpacing === 'normal' ? 0 : parseFloat(s.letterSpacing) / parseFloat(s.fontSize);
  const loaded = [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '').toLowerCase()))];

  // --- renk (ilk 400 görünür eleman)
  const palette = new Map(); // hex -> {v, area}
  const add = (v, w) => { if (!v) return; const k = hex(v); const p = palette.get(k) || { v, w: 0 }; p.w += w; palette.set(k, p); };
  for (const [e, s, r] of vis.slice(0, 400)) { const bg = rgba(s.backgroundColor); if (bg && bg.a > .05) add(bg, 1); if (directText(e)) add(rgba(s.color), 1); }
  const chromatic = [...palette.values()].map(p => chroma(p.v)).filter(Boolean);
  const accentBuckets = new Set(chromatic.map(h => Math.round(h.h / 30) % 12));
  // baskın zemin: ilk ekrandaki en geniş opak arka plan
  let domBg = null, domA = 0; const areaBg = new Map();
  for (const [e, s, r] of vis) { const bg = rgba(s.backgroundColor); if (!bg || bg.a < .5) continue;
    const a = Math.max(0, Math.min(r.right, vw) - Math.max(r.left, 0)) * Math.max(0, Math.min(r.bottom, vh) - Math.max(r.top, 0)); if (!a) continue;
    const k = hex(bg); areaBg.set(k, (areaBg.get(k) || 0) + a); if (areaBg.get(k) > domA) { domA = areaBg.get(k); domBg = bg; } }
  const pageBg = rgba(getComputedStyle(document.body).backgroundColor) || rgba(getComputedStyle(document.documentElement).backgroundColor);
  const bg = (domA > vw * vh * .3 ? domBg : null) || pageBg || { r: 255, g: 255, b: 255, a: 1 };
  const fg = rgba((bodyEl ? bodyEl.s : getComputedStyle(document.body)).color) || { r: 0, g: 0, b: 0, a: 1 };

  // --- ızgara
  const conts = vis.filter(([e]) => e.childElementCount > 0);
  const disp = d => conts.filter(([, s]) => s.display.includes(d)).length;
  let maxW = 0; for (const [e, s, r] of vis) { if (r.width >= vw - 8 || r.width < vw * .4 || r.left < 8) continue; if (Math.abs(r.left - (vw - r.right)) <= 2 && r.width > maxW) maxW = r.width; }
  const lefts = texts.map(x => x.r.left).filter(x => x >= 0 && x < vw / 2).sort((a, b) => a - b);
  const gutter = lefts.length ? lefts[Math.floor(lefts.length * .05)] : 0;

  // --- hareket
  let trans = 0, anim = 0; for (const e of all.slice(0, 6000)) { const s = getComputedStyle(e);
    if (s.transitionDuration.split(',').some(d => parseFloat(d) > 0)) trans++; if (s.animationName && s.animationName !== 'none') anim++; }
  const se = document.scrollingElement || document.documentElement;
  let tallest = 0; for (const [e, s, r] of vis) if (r.height > tallest && r.width > vw * .5) tallest = r.height;
  const cursorCss = [document.documentElement, document.body, ...vis.slice(0, 400).map(x => x[0])].some(e => { const c = getComputedStyle(e).cursor; return c === 'none' || c.startsWith('url('); });
  const follower = [...document.body.querySelectorAll('*')].some(e => { const s = getComputedStyle(e); if (s.position !== 'fixed' || s.pointerEvents !== 'none') return false;
    const r = e.getBoundingClientRect(); return r.width > 4 && r.width <= 100 && r.height > 4 && r.height <= 100 && (/cursor/i.test(e.className?.baseVal ?? e.className) || parseFloat(s.borderRadius) >= r.width * .4); });
  let rmCss = false, fvCss = false, focusCss = false; const sheetTxt = [];
  const scan = sh => { try { for (const r of sh.cssRules) { const t = r.cssText; if (t.includes('prefers-reduced-motion')) rmCss = true; if (t.includes(':focus-visible')) fvCss = true; if (t.includes(':focus')) focusCss = true; } } catch {} };
  for (const sh of document.styleSheets) scan(sh); for (const sh of document.adoptedStyleSheets || []) scan(sh);

  // --- AI-slop imzaları
  const COLRE = /(rgba?\([^)]*\)|#[0-9a-f]{3,8}\b|oklch\([^)]*\)|oklab\([^)]*\)|hsla?\([^)]*\)|color\([^)]*\))/gi;
  let grads = 0, pbGrads = 0, gradText = 0, glass = 0, glassCard = 0;
  for (const [e, s, r] of vis) {
    if (s.backgroundImage.includes('gradient(')) { grads++; const hs = (s.backgroundImage.match(COLRE) || []).map(rgba).filter(Boolean).map(chroma).filter(Boolean);
      if (hs.some(h => h.h >= 255 && h.h <= 300) && hs.some(h => h.h >= 190 && h.h < 255)) pbGrads++;
      if ((s.webkitBackgroundClip || s.backgroundClip) === 'text') gradText++; }
    if (/blur/.test(s.backdropFilter || s.webkitBackdropFilter || '')) { glass++; if (!['fixed', 'sticky'].includes(s.position) && r.width < vw * .6) glassCard++; }
  }
  const h1c = h1 ? h1[2] : null;
  const heroCentered = !!(h1 && h1c.top < vh && (h1s.textAlign === 'center' || Math.abs((h1c.left + h1c.right) / 2 - vw / 2) < vw * .03) && h1c.width < vw * .9);
  let cards3 = 0; // aynı satırda >=3 eşit genişlikte kart (vw'nin %18-40'ı)
  for (const [e] of conts) { const kids = [...e.children].map(k => [k, k.getBoundingClientRect(), getComputedStyle(k)]).filter(([, r]) => r.width >= vw * .18 && r.width <= vw * .4 && r.height > 120);
    if (kids.length < 3) continue; const cardish = kids.filter(([, r, s]) => parseFloat(s.borderRadius) > 0 || (rgba(s.backgroundColor)?.a || 0) > .05 || s.boxShadow !== 'none' || parseFloat(s.borderTopWidth) > 0);
    const row = cardish.filter(([, r]) => Math.abs(r.top - cardish[0]?.[1].top) < 4 && Math.abs(r.width - cardish[0][1].width) < 4); if (row.length >= 3) cards3++; }

  // --- yığın
  const q = s => !!document.querySelector(s);
  const scripts = [...document.scripts].map(s => s.src).join(' ');
  const gen = document.querySelector('meta[name=generator]')?.content || '';
  const reactRoot = [document.body, ...document.body.children].some(e => Object.keys(e).some(k => k.startsWith('__react')));
  const fw = [
    (window.__NEXT_DATA__ || window.next || /\/_next\//.test(scripts)) && 'next', (window.__NUXT__ || window.$nuxt || q('#__nuxt') || /\/_nuxt\//.test(scripts)) && 'nuxt',
    (q('astro-island') || /\/_astro\//.test(scripts) || [...vis.slice(0, 300)].some(([e]) => [...e.attributes].some(a => a.name.startsWith('data-astro-cid')))) && 'astro',
    (window.__sveltekit_dev || /_app\/immutable/.test(scripts) || q('[class*="svelte-"]')) && 'svelte', (q('html[data-wf-page]') || window.Webflow) && 'webflow',
    (/framer/i.test(gen) || q('[data-framer-name]')) && 'framer', q('#___gatsby') && 'gatsby', window.__remixContext && 'remix',
    (window.__vue_app__ || q('[data-v-app]') || [...vis.slice(0, 200)].some(([e]) => e.__vue__ || e.__vueParentComponent)) && 'vue', reactRoot && 'react', /wordpress/i.test(gen) && 'wordpress',
  ].filter(Boolean);
  const glob = { gsap: !!window.gsap, scrolltrigger: !!(window.ScrollTrigger || window.gsap?.core?.globals?.()?.ScrollTrigger), lenis: !!(window.Lenis || window.lenis) || document.documentElement.className.includes('lenis'),
    locomotive: q('[data-scroll-container]') || document.documentElement.classList.contains('has-scroll-smooth'), three: !!(window.THREE || window.__THREE__), pixi: !!window.PIXI };
  const canv = [...document.querySelectorAll('canvas')].filter(c => c !== cv);

  // --- hover adayları (ilk 1.5 ekran)
  const cand = vis.filter(([e, s, r]) => e.matches('a,button,[role=button]') && r.top >= 0 && r.top < vh * 1.5 && r.width > 10 && r.left >= 0 && r.right <= vw);
  const pick = []; const step = Math.max(1, Math.floor(cand.length / 10)); for (let i = 0; i < cand.length && pick.length < 10; i += step) pick.push(cand[i][0]);
  pick.forEach((e, i) => e.setAttribute('data-tt-h', i));

  // --- metin imzaları: kalıp pazarlama sözcükleri, emoji ikon
  const low = document.body.innerText.toLowerCase();
  const SLOPW = ['seamless', 'unlock', 'elevate', 'empower', 'revolutioniz', 'next-gen', 'cutting-edge', 'supercharge', 'game-chang', 'effortless', 'unleash', 'all-in-one',
    'sorunsuz', 'yeni nesil', 'devrim', 'zahmetsiz', 'güçlendir', 'hepsi bir arada'];
  const slopWords = SLOPW.filter(w => low.includes(w)).length;
  const emojiIcons = vis.filter(([e]) => e.matches('h1,h2,h3,h4,button,a,li,[class*=icon]') && /\p{Extended_Pictographic}/u.test(directText(e))).length;

  const r2 = x => Math.round(x * 100) / 100;
  return {
    fw, glob, gen, canvas: canv.length, ctx: window.__tt?.ctx || {}, rmJs: (window.__tt?.mm || []).some(m => m.includes('reduced-motion')),
    fontsUsed: fams, fontsLoaded: loaded, bodyPx, bodyLh: bodyEl ? r2(lhRatio(bodyEl.s)) : null, h1Real, h1Px, h1Lh: h1s ? r2(lhRatio(h1s)) : null, h1LsEm: h1s ? r2(lsEm(h1s) * 100) / 100 : null,
    h1Weight: h1s?.fontWeight, h1Fam: h1s ? fam(h1s) : null, maxPx, ratio: r2(h1Px / bodyPx), maxRatio: r2(maxPx / bodyPx),
    bg: hex(bg), fg: hex(fg), contrast: r2(contrast(fg, bg)), uniqColors: palette.size, chromatic: chromatic.length, accents: accentBuckets.size,
    maxW: Math.round(maxW), gutter: Math.round(gutter), gridPct: r2(disp('grid') / Math.max(1, conts.length) * 100), flexPct: r2(disp('flex') / Math.max(1, conts.length) * 100),
    scrollRatio: r2(Math.max(se.scrollHeight, tallest) / vh), trans, anim, elems: all.length, cursorCustom: cursorCss || follower, rmCss, fvCss, focusCss,
    grads, pbGrads, gradText, glass, glassCard, heroCentered, cards3, slopWords, emojiIcons, hoverN: pick.length, lcp: Math.round(window.__tt?.lcp || 0),
  };
};

const GENERIC = /^(inter|roboto|arial|helvetica|helvetica neue|system-ui|-apple-system|blinkmacsystemfont|segoe ui|sans-serif|open sans|poppins|montserrat|lato)$/;
const fam = f => f.toLowerCase().replace(/^__|_[0-9a-f]{6}$/g, '').replace(/_/g, ' ').trim();

export const puan = d => {
  const bayrak = [
    d.gradText > 0 && `gradyan metin ×${d.gradText}`,
    d.pbGrads > 0 && `mor-mavi gradyan ×${d.pbGrads}`,
    d.glassCard >= 2 && `cam (backdrop-blur) kart ×${d.glassCard}`,
    d.heroCentered && d.cards3 > 0 && d.ratio < 3 && `ortalı hero + eş 3'lü kart satırı, h1/gövde ${d.ratio} (<3)`,
    d.fontsUsed?.length > 0 && d.fontsUsed.every(f => GENERIC.test(fam(f))) && `yalnız varsayılan font (${d.fontsUsed.join(', ')})`,
    d.accents >= 4 && `vurgu ton kümesi ${d.accents} (≥4)`,
    d.slopWords >= 2 && `kalıp pazarlama sözcüğü ×${d.slopWords}`,
    d.emojiIcons >= 2 && `emoji ikon ×${d.emojiIcons}`,
  ].filter(Boolean);
  return { bayrak, slop: bayrak.length >= 2 };
};

if (process.argv[1]?.endsWith('slop.mjs')) {
  const url = process.argv[2];
  if (!url) { console.error('kullanım: node slop.mjs <url> [--json dosya]'); process.exit(2); }
  const { default: puppeteer } = await import('puppeteer');
  const bekle = ms => new Promise(r => setTimeout(r, ms));
  const browser = await puppeteer.launch({ args: ['--ignore-certificate-errors'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  await bekle(1500);
  for (let i = 0; i < 20; i++) { await page.mouse.wheel({ deltaY: 720 }); await bekle(100); }
  await page.evaluate(() => scrollTo(0, 0));
  await bekle(800);
  const d = await page.evaluate(MEASURE);
  await browser.close();
  const p = puan(d);
  (await import('./yakinsama.mjs')).gecmisYaz(d); // yakınsama hafızası: sonraki projede `yakinsama.mjs --gecmis`
  const j = process.argv.indexOf('--json');
  if (j > 0) fs.writeFileSync(process.argv[j + 1], JSON.stringify({ d, ...p }, null, 1));
  console.log(p.slop ? 'SLOP' : 'TEMİZ', `${p.bayrak.length} bayrak`);
  for (const b of p.bayrak) console.log(' -', b);
  process.exit(p.slop ? 1 : 0);
}
