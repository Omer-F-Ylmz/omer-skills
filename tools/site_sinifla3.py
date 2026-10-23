"""KAYNAK-SITE-3 adim 1: hatali (88) + 'diger' (79) siteleri yeniden ac (bekleme uzun, kaydirma, meta+basliklar, basarisizsa web.archive.org) ve genisletilmis tur listesiyle sinifla.
Kullanim: python site_sinifla3.py   (yeniden baslatilabilir: .v3 = islendi). Claude yok."""
import asyncio, json, os, sys, re, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import ucretsiz_havuz as h
from playwright.async_api import async_playwright

KOK = Path(__file__).resolve().parents[1]
CIK = KOK / ".kos/kopru/ara/site-sinif"
TURLER = ("arac/uretici|ilham galerisi|component/animasyon kutuphanesi|egitim/nasil yapilir|3D/model|ikon/font/gorsel|sablon|portfolyo/ajans|"
          "blog/haber|urun/SaaS|dizin/liste|kurs/akademi|topluluk/forum/sosyal|arastirma/makale/veri|AI model/sohbet|e-ticaret/pazaryeri|"
          "gelistirici platformu/dokuman|medya/video/muzik|oyun|kisisel/kurumsal|diger")
IST = """Web sitesi sayfa metninden siniflandir; 'diger' yalnizca hicbir tur uymuyorsa. SADECE tek satir JSON ver: {"tur":"<%s>","sunar":"<ne sunuyor, <=15 kelime>","ucretsiz":"evet|kismen|hayir|belirsiz","indirilebilir":"<indirilebilir varlik: kod/model/font/ikon/sablon/yok>"}
Site: %s | Baslik: %s
Metin:
%s"""
JS = """() => { const m=(document.querySelector('meta[name=description],meta[property="og:description"]')||{}).content||'';
 const hs=[...document.querySelectorAll('h1,h2,h3')].slice(0,12).map(e=>e.innerText).join(' | ');
 return m+' || '+hs+' || '+(document.body?document.body.innerText:''); }"""


def _havuz(url, baslik, metin):
    import time
    for t in range(40):  # havuz soguma/kota: bekle (gemini/mistral dakikalik soguma)
        m = None
        try:
            m, _, _ = h.cagir("hakem", IST % (TURLER, url, baslik, metin[:1800]), max_tokens=300, etiket="site-sinifla3",
                              dogrula=lambda x: None if re.search(r'\{.*"tur".*\}', x, re.S) else "json yok")
            if m:
                return json.loads(re.search(r"\{.*\}", m, re.S).group(0))
        except PermissionError:
            time.sleep(0.5 + t)
        except Exception:
            return None
        if m is None:
            time.sleep(20)
    return None


async def ac(br, url):
    ctx = await br.new_context(viewport={"width": 1280, "height": 800})
    try:
        p = await ctx.new_page()
        await p.goto(url, wait_until="domcontentloaded", timeout=40000)
        await p.wait_for_timeout(4000)
        await p.mouse.wheel(0, 1200)
        await p.wait_for_timeout(1000)
        b = (await p.title())[:150]
        t = re.sub(r"\s+", " ", await p.evaluate(JS))[:2500]
        return b, t
    finally:
        await ctx.close()


async def bir(br, sem, ex, f):
    d = json.loads(f.read_text(encoding="utf-8"))
    if d.get("v3"):
        return
    url = d["url"]
    b, t, kaynak = d.get("baslik3"), d.get("metin3"), d.get("kaynak3", "canli")
    async with sem:
        for u, k in (() if t else ((url, "canli"), ("https://web.archive.org/web/2/" + url, "arsiv"))):
            try:
                b, t = await ac(br, u)
                kaynak = k
                if len(t) > 80:
                    break
            except Exception as e:
                d["hata"] = str(e)[:100]
    if t and len(t) > 80:
        d["baslik3"], d["metin3"], d["kaynak3"] = b, t, kaynak
        f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        r = await asyncio.get_running_loop().run_in_executor(ex, _havuz, url, b, t)
        if r:
            d.pop("hata", None)
            d.update(r)
            d["baslik"] = b
            d["v3"] = 1
    elif "hata" in d:
        d["v3"] = 1
    f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


async def main():
    hed = []
    for f in sorted(CIK.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if not d.get("v3") and ("hata" in d or d.get("tur") == "diger"):
            hed.append(f)
    print("hedef", len(hed), flush=True)
    sem, ex = asyncio.Semaphore(3), cf.ThreadPoolExecutor(2)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(channel="chrome", headless=True)
        await asyncio.gather(*(bir(br, sem, ex, f) for f in hed))
        await br.close()


asyncio.run(main())
