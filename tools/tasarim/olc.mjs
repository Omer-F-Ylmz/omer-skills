// TASARIM-1 (2) teknik ölçüm: headless playwright, yalnız ölçüm verisi (varlık kaydedilmez, ss yalnız kanıt).
// Kullanım: node olc.mjs [ad ...]   -> out/<ad>.json
import { chromium, devices } from 'playwright';
import fs from 'node:fs';
import { MEASURE } from '../../plugins/frontend-craft/skills/frontend-craft/scripts/slop.mjs';

export const SITES = [
  ['activetheory', 'https://activetheory.net', 'webgl'],
  ['lusion', 'https://lusion.co', 'webgl'],
  ['igloo', 'https://www.igloo.inc', 'webgl'],
  ['bruno-simon', 'https://bruno-simon.com', 'webgl'],
  ['resn', 'https://resn.co.nz', 'webgl'],
  ['immersive-g', 'https://immersive-g.com', 'webgl'],
  ['locomotive', 'https://locomotive.ca', 'editoryal'],
  ['14islands', 'https://14islands.com', 'editoryal'],
  ['darkroom', 'https://darkroom.engineering', 'editoryal'],
  ['basement', 'https://basement.studio', 'editoryal'],
  ['obys', 'https://obys.agency', 'editoryal'],
  ['cuberto', 'https://cuberto.com', 'editoryal'],
  ['linear', 'https://linear.app', 'saas'],
  ['vercel', 'https://vercel.com', 'saas'],
  ['stripe', 'https://stripe.com', 'saas'],
  ['raycast', 'https://www.raycast.com', 'saas'],
  ['rauno', 'https://rauno.me', 'portfolyo'],
  ['emilkowal', 'https://emilkowal.ski', 'portfolyo'],
  ['paco', 'https://paco.me', 'portfolyo'],
  ['brittanychiang', 'https://brittanychiang.com', 'portfolyo'],
];

const JS_SIG = {
  gsap: /GreenSock|\bgsap\b/, scrolltrigger: /ScrollTrigger|scrollTrigger/, lenis: /lenis-smooth|lenis-scrolling|\blenis\b/i,
  locomotive: /locomotive-scroll|has-scroll-smooth|data-scroll-container/, three: /__THREE__|WebGLRenderer/, r3f: /__r3f|react-three-fiber/,
  ogl: /["'\/@]ogl["'\/]|\bOGL\b/, pixi: /PIXI\.|pixi\.js/i, motion: /framer-motion|framerAppearId|data-framer-appear|useMotionValue|MotionValue/,
  barba: /@barba|barba\.js|data-barba/, swup: /\bswup\b/i, spline: /@splinetool|splinetool/, theatre: /@theatre\/core/,
};

const INIT = () => {
  window.__tt = { ctx: {}, mm: [], lcp: 0 };
  const g = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (t, ...a) {
    const c = g.call(this, t, ...a);
    if (c && !this.__ttc) { this.__ttc = t; window.__tt.ctx[t] = (window.__tt.ctx[t] || 0) + 1; }
    return c;
  };
  const m = window.matchMedia;
  window.matchMedia = function (q) { try { window.__tt.mm.push(String(q)); } catch {} return m.call(window, q); };
  try { new PerformanceObserver(l => { for (const e of l.getEntries()) window.__tt.lcp = e.startTime; }).observe({ type: 'largest-contentful-paint', buffered: true }); } catch {}
};


const SNAP = (i) => { const e = document.querySelector(`[data-tt-h="${i}"]`); if (!e) return '';
  const P = ['color', 'backgroundColor', 'transform', 'opacity', 'textDecorationLine', 'borderTopColor', 'boxShadow', 'filter', 'letterSpacing', 'clipPath', 'scale', 'translate'];
  const els = [e, ...[...e.querySelectorAll('*')].slice(0, 8)];
  return els.map(x => [getComputedStyle(x), getComputedStyle(x, '::before'), getComputedStyle(x, '::after')].map(s => P.map(p => s[p]).join('|')).join('/')).join(';'); };

async function runVp(browser, ad, url, m) {
  const base = m ? { ...devices['iPhone 13'], deviceScaleFactor: 1 } : { viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 };
  delete base.defaultBrowserType;
  const ctx = await browser.newContext({ ...base, locale: 'en-US', reducedMotion: 'no-preference', ignoreHTTPSErrors: true });
  await ctx.addInitScript(INIT);
  const page = await ctx.newPage();
  const cdp = await ctx.newCDPSession(page); await cdp.send('Network.enable');
  const types = new Map(); const net = { total: 0, js: 0, css: 0, img: 0, font: 0, media: 0, n: 0 };
  cdp.on('Network.responseReceived', e => types.set(e.requestId, e.type));
  cdp.on('Network.loadingFinished', e => { net.n++; net.total += e.encodedDataLength; const t = types.get(e.requestId);
    if (t === 'Script') net.js += e.encodedDataLength; else if (t === 'Stylesheet') net.css += e.encodedDataLength; else if (t === 'Image') net.img += e.encodedDataLength;
    else if (t === 'Font') net.font += e.encodedDataLength; else if (t === 'Media') net.media += e.encodedDataLength; });
  const sig = {}; let rmNet = false, fvNet = false; const pend = [];
  page.on('response', r => { const t = r.request().resourceType(); if (t !== 'script' && t !== 'stylesheet') return;
    pend.push(r.text().then(x => { if (t === 'stylesheet') { if (x.includes('prefers-reduced-motion')) rmNet = true; if (x.includes(':focus-visible')) fvNet = true; }
      else { for (const [k, re] of Object.entries(JS_SIG)) if (re.test(x)) sig[k] = true; if (/prefers-reduced-motion/.test(x)) sig.rmInJs = true; } }).catch(() => {})); });
  const t0 = Date.now();
  const resp = await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  const loadMs = Date.now() - t0;
  await page.waitForTimeout(4000);
  const lcpEarly = await page.evaluate(() => Math.round(window.__tt?.lcp || 0));
  await page.mouse.move(m ? 200 : 700, m ? 400 : 450);
  for (let i = 0; i < 25; i++) { await page.mouse.wheel(0, Math.round((m ? 844 : 900) * .8)).catch(() => {}); await page.waitForTimeout(150); }
  await page.evaluate(() => window.scrollTo(0, 0)); for (let i = 0; i < 25; i++) await page.mouse.wheel(0, -2000).catch(() => {});
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `ss/${ad}-${m ? 'm' : 'd'}.png`, timeout: 20000 }).catch(e => console.error(ad, 'ss', e.message.split('\n')[0]));
  const r = await page.evaluate(MEASURE);
  let hov = 0;
  if (!m) for (let i = 0; i < r.hoverN; i++) { const sel = `[data-tt-h="${i}"]`;
    try { await page.mouse.move(2, 2); await page.waitForTimeout(150); const a = await page.evaluate(SNAP, i);
      await page.hover(sel, { force: true, timeout: 2000 }); await page.waitForTimeout(450); const b = await page.evaluate(SNAP, i); if (a && a !== b) hov++; } catch {} }
  await Promise.all(pend);
  await ctx.close();
  return { ...r, lcp: r.lcp || lcpEarly, hoverDiff: hov, status: resp?.status(), finalUrl: page.url(), loadMs, net, sig, rmCss: r.rmCss || rmNet, fvCss: r.fvCss || fvNet, rmJsBundle: !!sig.rmInJs };
}

async function site(browser, [ad, url, kat]) {
  const res = { ad, url, kat };
  for (const m of [false, true]) {
    for (let a = 1; a <= 2; a++) {
      try { res[m ? 'm' : 'd'] = await runVp(browser, ad, url, m); break; }
      catch (e) { res[(m ? 'm' : 'd') + 'Err'] = e.message.split('\n')[0]; console.error(ad, m ? 'm' : 'd', a, res[(m ? 'm' : 'd') + 'Err']); }
    }
  }
  fs.writeFileSync(`out/${ad}.json`, JSON.stringify(res, null, 1));
  console.log('ok', ad, !!res.d, !!res.m);
}

if (process.argv[1].endsWith('olc.mjs')) {
  fs.mkdirSync('out', { recursive: true }); fs.mkdirSync('ss', { recursive: true });
  const want = process.argv.slice(2); const list = SITES.filter(s => !want.length || want.includes(s[0]));
  const browser = await chromium.launch({ headless: true, executablePath: process.env.LOCALAPPDATA + '/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-win64/chrome-headless-shell.exe', args: ['--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--ignore-gpu-blocklist'] });
  const q = [...list]; await Promise.all([1, 2, 3].map(async () => { while (q.length) await site(browser, q.shift()); }));
  await browser.close();
}
