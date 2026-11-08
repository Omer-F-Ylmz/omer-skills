() => {
  const q = s => [...document.querySelectorAll(s)];
  const w = window;
  const src = q('script[src]').map(s => s.src);
  const has = re => src.some(s => re.test(s));
  const libs = {};
  const chk = {
    gsap: () => w.gsap && (w.gsap.version || 'var'),
    ScrollTrigger: () => (w.ScrollTrigger || has(/ScrollTrigger/i)) && 'var',
    SplitText: () => (w.SplitText || has(/SplitText/i)) && 'var',
    three: () => (w.THREE && w.THREE.REVISION) || (has(/three(\.module)?(\.min)?\.js/i) && 'src'),
    r3f: () => has(/react-three|@react-three/i) && 'src',
    lenis: () => (w.Lenis || w.lenis || document.documentElement.classList.contains('lenis') || has(/lenis/i)) && 'var',
    locomotive: () => (w.LocomotiveScroll || document.querySelector('[data-scroll-container]')) && 'var',
    barba: () => (w.barba || document.querySelector('[data-barba]')) && 'var',
    swup: () => (w.swup || document.querySelector('#swup')) && 'var',
    next: () => (w.__NEXT_DATA__ && 'pages') || (w.next && 'app') || (q('script[src*="/_next/"]').length && '_next'),
    nuxt: () => (w.__NUXT__ || w.$nuxt || q('script[src*="/_nuxt/"]').length) && 'nuxt',
    astro: () => document.querySelector('astro-island,[data-astro-cid]') && 'astro',
    framer: () => (document.querySelector('[data-framer-name],[data-framer-component-type]') || has(/framerusercontent|framer\.com/i)) && 'framer',
    webflow: () => (document.documentElement.dataset.wfPage || w.Webflow || has(/webflow/i)) && 'webflow',
    wordpress: () => (has(/wp-content|wp-includes/i) || document.querySelector('link[href*="wp-content"]')) && 'wp',
    shopify: () => (w.Shopify || has(/cdn\.shopify/i)) && 'shopify',
    react: () => (w.React || document.querySelector('[data-reactroot]') || (w.__REACT_DEVTOOLS_GLOBAL_HOOK__ && w.__REACT_DEVTOOLS_GLOBAL_HOOK__.renderers && w.__REACT_DEVTOOLS_GLOBAL_HOOK__.renderers.size)) && 'react',
    vue: () => (w.Vue || w.__VUE__ || document.querySelector('[data-v-app]')) && 'vue',
    svelte: () => document.querySelector('[class*="svelte-"]') && 'svelte',
    motion: () => (w.Motion || has(/framer-motion|motion\.dev|\/motion@/i)) && 'var',
    anime: () => w.anime && (w.anime.version || 'var'),
    lottie: () => (w.lottie || w.bodymovin || document.querySelector('lottie-player,dotlottie-player,dotlottie-wc')) && 'var',
    rive: () => (w.rive || has(/rive/i)) && 'var',
    spline: () => (document.querySelector('spline-viewer') || has(/splinetool|spline\.design/i)) && 'spline',
    pixi: () => w.PIXI && (w.PIXI.VERSION || 'var'),
    ogl: () => has(/\bogl\b/i) && 'src',
    swiper: () => (w.Swiper || document.querySelector('.swiper')) && 'var',
    splide: () => (w.Splide || document.querySelector('.splide')) && 'var',
    matter: () => w.Matter && 'var',
    tailwind: () => document.querySelector('[class*="tw-"],[class*=" md:"],[class*=" lg:"]') && 'sınıf',
  };
  for (const [k, f] of Object.entries(chk)) { try { const v = f(); if (v) libs[k] = v; } catch (e) {} }
  const vars = {}, kf = new Set(), media = new Set();
  for (const sh of document.styleSheets) {
    let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    for (const r of rules) {
      if (r.type === 1 && /^(:root|html|body)$/.test(r.selectorText || '')) for (const p of r.style) if (p.startsWith('--')) vars[p] = r.style.getPropertyValue(p).trim();
      if (r.type === 7) kf.add(r.name);
      if (r.type === 4) media.add(r.conditionText || (r.media && r.media.mediaText));
    }
  }
  const say = (o, k) => { o[k] = (o[k] || 0) + 1; };
  const renk = {}, zemin = {}, font = {}, gecis = {}, radius = {}, golge = {};
  for (const el of q('body *').slice(0, 4000)) {
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    say(renk, cs.color);
    if (cs.backgroundColor !== 'rgba(0, 0, 0, 0)') say(zemin, cs.backgroundColor);
    if (cs.backgroundImage && cs.backgroundImage.includes('gradient')) say(zemin, cs.backgroundImage.slice(0, 120));
    say(font, cs.fontFamily.split(',')[0].trim().replace(/["']/g, ''));
    if (cs.transitionDuration !== '0s') say(gecis, cs.transitionProperty.slice(0, 30) + ' ' + cs.transitionDuration + ' ' + cs.transitionTimingFunction);
    if (cs.animationName !== 'none') say(gecis, 'anim ' + cs.animationName + ' ' + cs.animationDuration + ' ' + cs.animationTimingFunction);
    if (cs.borderRadius !== '0px') say(radius, cs.borderRadius);
    if (cs.boxShadow !== 'none') say(golge, cs.boxShadow.slice(0, 80));
  }
  const ust = (o, n = 8) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n);
  const bas = q('h1,h2,h3').slice(0, 6).map(e => { const cs = getComputedStyle(e); return { t: e.tagName, x: e.textContent.trim().replace(/\s+/g, ' ').slice(0, 50), fs: cs.fontSize, fw: cs.fontWeight, ff: cs.fontFamily.split(',')[0], ls: cs.letterSpacing, lh: cs.lineHeight, tt: cs.textTransform }; });
  const b = getComputedStyle(document.body);
  const cv = q('canvas');
  return {
    baslik: document.title, aciklama: (document.querySelector('meta[name=description]') || {}).content,
    generator: (document.querySelector('meta[name=generator]') || {}).content, kutuphane: libs,
    script: [...new Set(src.map(s => { try { const u = new URL(s); return u.hostname + '/' + u.pathname.split('/').pop(); } catch (e) { return s.slice(0, 60); } }))].slice(0, 40),
    canvas: cv.length, webgl: cv.filter(c => { try { return !!(c.getContext('webgl2') || c.getContext('webgl')); } catch (e) { return false; } }).length,
    video: q('video').length, svg: q('svg').length, img: q('img').length, iframe: q('iframe').map(f => (f.src || '').slice(0, 60)).slice(0, 5),
    cssVar: Object.fromEntries(Object.entries(vars).slice(0, 80)), keyframes: [...kf].slice(0, 40), breakpoint: [...media].filter(Boolean).slice(0, 15),
    renk: ust(renk), zemin: ust(zemin), font: ust(font, 6), gecis: ust(gecis, 12), radius: ust(radius, 6), golge: ust(golge, 5),
    fontFace: [...new Set([...document.fonts].map(f => f.family.replace(/["']/g, '') + ' ' + f.weight + ' ' + f.style))].slice(0, 20),
    basliklar: bas, govde: { ff: b.fontFamily, fs: b.fontSize, lh: b.lineHeight, bg: b.backgroundColor, c: b.color },
    yukseklik: document.documentElement.scrollHeight, genislik: innerWidth,
  };
}
