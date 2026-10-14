"""SİTE-OKULU-1: bir sitenin ekran + kod mekanizmasını yerel analiz klasörüne çeker (yayınlanmaz, .kos/ gitignore).
Kullanım: python tools/site-okulu/cek.py <slug> <url> [...slug url]  → .kos/site-okulu/<slug>/{d-0..7.jpg, m-0..7.jpg, kayit.webm, js/, olcum.json}
Teknik çıkarmak içindir; varlık/metin yeniden kullanılmaz (Ömer 29 Eyl)."""
import asyncio, json, re, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

KOK = Path(__file__).resolve().parents[2] / ".kos" / "site-okulu"
KOD_UZANTI = re.compile(r"\.(m?js|glsl|vs|fs|vert|frag|wgsl)(\?|$)", re.I)


async def kaydir(page, adim, vh, mobil):
    """Lenis/sanal scroll wheel ister; mobilde wheel yoksa scrollBy'a düşer."""
    once = await page.evaluate("scrollY")
    for _ in range(max(1, int(adim // 150))):
        await page.mouse.wheel(0, 150)
        await page.wait_for_timeout(45)
    if mobil and await page.evaluate("scrollY") == once:
        await page.evaluate(f"scrollBy(0,{int(adim)})")


async def tur(pw, slug, url, d, mobil):
    vp = {"width": 390, "height": 844} if mobil else {"width": 1440, "height": 900}
    tarayici = await pw.chromium.launch(channel="chrome", headless=True, args=["--enable-unsafe-swiftshader", "--autoplay-policy=no-user-gesture-required"])
    ctx = await tarayici.new_context(viewport=vp, device_scale_factor=1, is_mobile=mobil, has_touch=mobil,
                                     record_video_dir=None if mobil else str(d / "_v"), record_video_size=None if mobil else {"width": 960, "height": 600})
    page = await ctx.new_page()
    kodlar = []

    async def yanit(r):
        if mobil or not KOD_UZANTI.search(r.url.split("#")[0]) and "javascript" not in (r.headers.get("content-type") or ""):
            return
        try:
            b = await r.body()
        except Exception:
            return
        ad = re.sub(r"[^\w.-]", "_", r.url.split("?")[0].rsplit("/", 1)[-1])[:80] or "kok.js"
        (d / "js").mkdir(exist_ok=True)
        (d / "js" / f"{len(kodlar):03d}-{ad}").write_bytes(b)
        kodlar.append([r.url[:200], len(b)])
    page.on("response", lambda r: asyncio.ensure_future(yanit(r)))
    t = time.monotonic()
    try:
        await page.goto(url, wait_until="load", timeout=45000)
    except Exception as e:
        print(slug, "goto", type(e).__name__)
    yuk = round((time.monotonic() - t) * 1000)
    await page.wait_for_timeout(5000)  # yükleyici + giriş animasyonu kayda girsin
    await page.mouse.move(vp["width"] / 2, vp["height"] / 2)
    docH = await page.evaluate("document.documentElement.scrollHeight")
    adim = (docH - vp["height"]) / 7 if docH > vp["height"] * 1.5 else 1200
    on = "m" if mobil else "d"
    for i in range(8):
        if i:
            await kaydir(page, adim, vp["height"], mobil)
            await page.wait_for_timeout(1600)
        await page.screenshot(path=str(d / f"{on}-{i}.jpg"), type="jpeg", quality=55)
    kaynak = await page.evaluate("""performance.getEntriesByType('resource').map(e=>[e.name.split('?')[0].slice(-90), e.transferSize||e.encodedBodySize||0, e.initiatorType])""")
    sayfa = await page.evaluate("""({docH: document.documentElement.scrollHeight, canv: [...document.querySelectorAll('canvas')].map(c=>c.width+'x'+c.height+' '+getComputedStyle(c).position),
        video: document.querySelectorAll('video').length, lenis: !!document.querySelector('.lenis,[data-lenis-prevent]') || 'lenis' in window,
        gsap: window.gsap?.version || null, three: window.__THREE__ || null, ctxGpu: !!navigator.gpu, fonts: [...new Set([...document.fonts].map(f=>f.family))].slice(0,8)})""")
    await ctx.close()
    await tarayici.close()
    if not mobil:
        v = next((d / "_v").glob("*.webm"), None)
        if v:
            v.replace(d / "kayit.webm")
    return {"yukMs": yuk, "sayfa": sayfa, "kaynak": kaynak, "kod": kodlar}


async def main(ciftler):
    async with async_playwright() as pw:
        for slug, url in ciftler:
            d = KOK / slug
            d.mkdir(parents=True, exist_ok=True)
            try:
                masa = await tur(pw, slug, url, d, False)
                mob = await tur(pw, slug, url, d, True)
                ozet = {"slug": slug, "url": url, "masa": masa, "mobil": {k: mob[k] for k in ("yukMs", "sayfa")}, "mobilBayt": sum(x[1] for x in mob["kaynak"])}
                (d / "olcum.json").write_text(json.dumps(ozet, ensure_ascii=False), encoding="utf-8")
                print(slug, "tamam", len(masa["kod"]), "kod dosyası", round(sum(x[1] for x in masa["kaynak"]) / 1e6, 1), "MB", flush=True)
            except Exception as e:
                print(slug, "DÜŞTÜ", type(e).__name__, str(e)[:200], flush=True)
    print("BITTI", flush=True)


if __name__ == "__main__":
    a = sys.argv[1:]
    asyncio.run(main(list(zip(a[::2], a[1::2]))))
