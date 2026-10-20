"""tersine probu: headless Playwright ile sayfa kanıtı (kütüphane, CSS animasyon, WebGL/canvas çağrıları, scroll örnekleri) + ekran görüntüleri.
  python tools/ters/probe.py <url> <çıktı_dizini> [--bekle=ms]   → <dizin>/kanit.json, kare-<n>.png
Pencere açmaz (headless). Dışarıdan çağrılabilir: probe(url, dizin) -> dict."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

KANCA = """(() => {
  const s = window.__ters = {raf: 0, ctx: {}, gl: {draw: 0}, c2d: {arc: 0, fill: 0, rect: 0}};
  const raf = window.requestAnimationFrame; window.requestAnimationFrame = f => { s.raf++; return raf.call(window, f); };
  const gc = HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext = function (t, ...a) { s.ctx[t] = (s.ctx[t] || 0) + 1; return gc.call(this, t, ...a); };
  for (const C of [window.WebGLRenderingContext, window.WebGL2RenderingContext]) if (C)
    for (const m of ['drawArrays', 'drawElements', 'drawArraysInstanced', 'drawElementsInstanced']) {
      const o = C.prototype[m]; C.prototype[m] = function (...a) { s.gl.draw++; return o.apply(this, a); }; }
  const P = CanvasRenderingContext2D.prototype;
  for (const [m, k] of [['arc', 'arc'], ['fill', 'fill'], ['fillRect', 'rect']]) {
    const o = P[m]; P[m] = function (...a) { s.c2d[k]++; return o.apply(this, a); }; }
})()"""

TOPLA = """() => {
  const g = window, r = {};
  r.kutuphane = {gsap: g.gsap && g.gsap.version, three: g.THREE && g.THREE.REVISION, lenis: !!g.Lenis, scrolltrigger: !!g.ScrollTrigger};
  r.animasyonlar = document.getAnimations().slice(0, 12).map(a => ({
    tur: a.constructor.name, ad: a.animationName || a.transitionProperty || null,
    zaman_cizelgesi: a.timeline && a.timeline.constructor.name, sure_ms: a.effect && a.effect.getComputedTiming().duration,
    easing: a.effect && a.effect.getTiming().easing, hedef: a.effect && a.effect.target && (a.effect.target.tagName + (a.effect.target.className ? '.' + String(a.effect.target.className).split(' ')[0] : ''))}));
  const kural = [];
  for (const sh of document.styleSheets) { let rs; try { rs = sh.cssRules; } catch (e) { continue; }
    for (const k of rs) { const t = k.cssText; if (/animation|transition|view-timeline|scroll-timeline|@keyframes|sticky|perspective/.test(t)) kural.push(t.slice(0, 160)); } }
  r.css_kurallar = kural.slice(0, 14);
  r.canvas = document.querySelectorAll('canvas').length;
  r.ters = window.__ters;
  r.scroll_yuksekligi = document.documentElement.scrollHeight;
  return r;
}"""

ORNEK = """() => [...document.querySelectorAll('body *')].filter(e => e.getAnimations().length || e.matches('canvas, [style*=transform], [class]'))
  .slice(0, 8).map(e => { const c = getComputedStyle(e); return [e.tagName + (e.className ? '.' + String(e.className).split(' ')[0] : ''), c.transform, c.opacity]; })"""


def probe(url, dizin, bekle=1500, genislik=1280, yukseklik=720):
    dizin = Path(dizin); dizin.mkdir(parents=True, exist_ok=True)
    ag = []
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
        s = b.new_page(viewport={"width": genislik, "height": yukseklik})
        s.add_init_script(KANCA)
        s.on("response", lambda r: ag.append((r.request.resource_type, r.url.split("?")[0][-90:], r.status)))
        s.on("pageerror", lambda e: ag.append(("hata", str(e)[:100], 0)))
        s.goto(url, wait_until="load"); s.wait_for_timeout(bekle)
        kanit = s.evaluate(TOPLA)
        maks = max(0, kanit["scroll_yuksekligi"] - yukseklik)
        kanit["scroll"] = []
        for i, oran in enumerate((0, 0.25, 0.5, 0.75, 1)):
            s.evaluate(f"window.scrollTo(0, {int(maks * oran)})"); s.wait_for_timeout(400)
            kanit["scroll"].append({"oran": oran, "ornek": s.evaluate(ORNEK)})
            if oran in (0, 0.5, 1): s.screenshot(path=str(dizin / f"kare-{int(oran * 100)}.png"))
        s.close(); b.close()
    kanit["ag"] = [a for a in ag if a[0] in ("script", "stylesheet", "hata", "fetch", "xhr")][:20]
    (dizin / "kanit.json").write_text(json.dumps(kanit, ensure_ascii=False, indent=1), encoding="utf-8")
    return kanit


if __name__ == "__main__":
    k = probe(sys.argv[1], sys.argv[2], int(next((a.split("=")[1] for a in sys.argv if a.startswith("--bekle=")), 1500)))
    print(json.dumps({"kutuphane": k["kutuphane"], "anim": len(k["animasyonlar"]), "canvas": k["canvas"], "ters": k["ters"]}, ensure_ascii=False))
