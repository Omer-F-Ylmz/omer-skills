"""KAYNAK-SITE-2 adim 3: oncelikli turlerde Playwright ile teknik cikarim (kutuphane/ag/baglantilar) + havuz ile kart. Claude yok. Yeniden baslatilabilir."""
import asyncio, json, os, re, sys, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import ucretsiz_havuz as h
from playwright.async_api import async_playwright
KOK = Path(__file__).resolve().parents[1]
SIN = KOK / ".kos/kopru/ara/site-sinif"
KART = KOK / "docs/site-inceleme/kart"
ONCELIK = {"component/animasyon kutuphanesi", "ilham galerisi", "3D/model", "ikon/font/gorsel", "sablon", "egitim/nasil yapilir"}
JS = r"""()=>{const g=(re)=>[...document.querySelectorAll('a[href]')].map(a=>a.href).filter(u=>re.test(u));
const w=window;const lib={three:!!w.THREE||!!document.querySelector('canvas'),gsap:!!w.gsap,lenis:!!w.Lenis,react:!!document.querySelector('[data-reactroot],#__next,#root'),next:!!w.__NEXT_DATA__,vue:!!w.__VUE__||!!document.querySelector('#app[data-v-app]'),framer:!!document.querySelector('[data-framer-name]'),webflow:!!w.Webflow,tailwind:/\b(flex|grid|px-\d|text-\w+-\d00)\b/.test(document.body.className+document.body.innerHTML.slice(0,20000))};
return {lib,github:[...new Set(g(/github\.com\/[^\/]+\/[^\/]+/))].slice(0,5),dl:[...new Set(g(/download|\.zip$|\.fig$|\.ttf|\.woff|\.glb/i))].slice(0,5),fiyat:[...new Set(g(/pricing|price|plans/i))].slice(0,2),lisans:[...new Set(g(/licen[sc]e|terms/i))].slice(0,2),scripts:[...document.scripts].map(s=>s.src).filter(Boolean).map(u=>u.split('/').slice(2,4).join('/')).slice(0,12),text:document.body.innerText.replace(/\s+/g,' ').slice(0,1500)}}"""
IST = """Teknik site karti yaz (Turkce, <=90 kelime, markdown madde listesi: Ne sunuyor · Ucretsiz kisim · Indirilebilir varlik/kaynak kod · Teknoloji · Bizde kullanim (hangi skill/is icin)). SADECE verilen kanittan.
Site: %s | tur: %s | ozet: %s
Kanit: %s"""


def kart(sin, ev):
    ist = IST % (sin["url"], sin["tur"], sin.get("sunar", ""), json.dumps(ev, ensure_ascii=False)[:2500])
    for _ in range(5):
        try:
            m, k, _ = h.cagir("ozet", ist, max_tokens=500, etiket="site-kart")
        except PermissionError:
            continue
        if m:
            return m.strip(), k
    return None, ""


async def bir(br, sem, ex, f):
    sin = json.loads(f.read_text(encoding="utf-8"))
    out = KART / (f.stem + ".md")
    if out.exists():
        return
    ev = {}
    async with sem:
        if "hata" not in sin:
            try:
                ctx = await br.new_context(viewport={"width": 1280, "height": 800})
                p = await ctx.new_page()
                await p.goto(sin["url"], wait_until="domcontentloaded", timeout=25000)
                await p.wait_for_timeout(2000)
                ev = await p.evaluate(JS)
                await ctx.close()
            except Exception as e:
                ev = {"hata": str(e)[:80]}
        else:
            ev = {"not": "icerik alinamadi (olu/engelli); yalniz ad-baglam siniflamasi"}
    m, k = await asyncio.get_running_loop().run_in_executor(ex, kart, sin, ev)
    if not m:
        m, k = "- **Ozet**: %s\n- **Kanit**: %s\n- (havuz yanit vermedi; sablon kart)" % (sin.get("sunar", "-"), json.dumps({x: ev.get(x) for x in ("lib", "github", "dl", "fiyat")}, ensure_ascii=False)[:400]), "sablon"
    out.write_text("---\nsite: %s\ntur: %s\nkaynak: %s\nkart-modeli: %s\n---\n# %s\n\n%s\n\nTur: [[Siteler/%s]]\n" % (
        sin["url"], sin["tur"], "icerik+teknik" if "hata" not in sin and "hata" not in ev else "ad-baglam", k, sin["ad"], m, sin["tur"].replace("/", "-")), encoding="utf-8")


async def main():
    fs = [f for f in sorted(SIN.glob("*.json")) if json.loads(f.read_text(encoding="utf-8")).get("tur") in ONCELIK]
    print("oncelikli", len(fs), flush=True)
    sem, ex = asyncio.Semaphore(4), cf.ThreadPoolExecutor(4)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(channel="chrome", headless=True)
        await asyncio.gather(*(bir(br, sem, ex, f) for f in fs))
        await br.close()

asyncio.run(main())
