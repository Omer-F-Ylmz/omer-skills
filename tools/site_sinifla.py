"""KAYNAK-SITE-2 adim 2: acik siteleri Playwright (Chrome, headless, <=4 sekme) ile ac; metin+baslik+ilk ekran -> ucretsiz havuz siniflar. Claude yok.
Kullanim: python site_sinifla.py [baslangic] [adet]   Yeniden baslatilabilir (cikti dosyasi varsa atlar)."""
import asyncio, csv, json, os, sys, re, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import ucretsiz_havuz as h
from playwright.async_api import async_playwright

KOK = Path(__file__).resolve().parents[1]
CIK = KOK / ".kos/kopru/ara/site-sinif"
TURLER = "arac/uretici|ilham galerisi|component/animasyon kutuphanesi|egitim/nasil yapilir|3D/model|ikon/font/gorsel|sablon|portfolyo/ajans|blog/haber|urun/SaaS|dizin/liste|diger"
IST = """Web sitesi sayfa metninden siniflandir. SADECE tek satir JSON ver: {"tur":"<%s>","sunar":"<ne sunuyor, <=15 kelime>","ucretsiz":"evet|kismen|hayir|belirsiz","indirilebilir":"<indirilebilir varlik: kod/model/font/ikon/sablon/yok>"}
Site: %s | Baslik: %s
Metin:
%s"""


def isle_havuz(ad, url, baslik, metin):
    import time
    for _t in range(4):
        try:
            return _havuz(ad, url, baslik, metin)
        except PermissionError:
            time.sleep(0.5 + _t)
    return None


def _havuz(ad, url, baslik, metin):
    m, kay, _ = h.cagir("ozet", IST % (TURLER, url, baslik, metin[:1800]), max_tokens=300, etiket="site-sinifla",
                        dogrula=lambda t: None if re.search(r'\{.*"tur".*\}', t, re.S) else "json yok")
    if not m:
        return None
    try:
        return json.loads(re.search(r"\{.*\}", m, re.S).group(0))
    except Exception:
        return None


async def bir(br, sem, ex, ad, url):
    cik = CIK / (re.sub(r"[^\w.-]", "_", ad) + ".json")
    if cik.exists():
        return
    async with sem:
        sonuc = {"ad": ad, "url": url}
        try:
            ctx = await br.new_context(viewport={"width": 1280, "height": 800})
            p = await ctx.new_page()
            await p.goto(url, wait_until="domcontentloaded", timeout=25000)
            await p.wait_for_timeout(1500)
            sonuc["baslik"] = (await p.title())[:150]
            sonuc["metin"] = re.sub(r"\s+", " ", await p.evaluate("document.body?document.body.innerText:''"))[:2500]
            await p.screenshot(path=str(CIK / "ss" / (cik.stem + ".jpg")), type="jpeg", quality=40)
            await ctx.close()
        except Exception as e:
            sonuc["hata"] = str(e)[:120]
    if "hata" not in sonuc and len(sonuc["metin"]) > 40:
        r = await asyncio.get_running_loop().run_in_executor(ex, isle_havuz, ad, url, sonuc["baslik"], sonuc["metin"])
        if r:
            sonuc.update(r)
        else:
            sonuc["hata"] = "havuz yanit yok"
    elif "hata" not in sonuc:
        sonuc["hata"] = "metin bos"
    sonuc.pop("metin", None)
    if sonuc.get("hata") == "havuz yanit yok":
        return  # kaydetme: yeniden denenir
    cik.write_text(json.dumps(sonuc, ensure_ascii=False), encoding="utf-8")


async def main():
    bas, adet = (int(sys.argv[1]) if len(sys.argv) > 1 else 0), (int(sys.argv[2]) if len(sys.argv) > 2 else 10**6)
    satir = [r for r in csv.DictReader(open(KOK / "docs/site-inceleme/site-tam.tsv", encoding="utf-8"), delimiter="\t") if r["erisim"].startswith(("aç", "gir"))][bas:bas + adet]
    sem = asyncio.Semaphore(4)
    ex = cf.ThreadPoolExecutor(4)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(channel="chrome", headless=True)
        await asyncio.gather(*(bir(br, sem, ex, r["ad"], r["url"]) for r in satir))
        await br.close()


asyncio.run(main())
