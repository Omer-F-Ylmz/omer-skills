"""KAYNAK-SITE-3 adim 2: 228 kartin her maddesini sayfa kanitiyla eslestir. Kart modelinden FARKLI aile hakem (havuz haric_aile) + alinti literal kontrolu:
hakem 'destekli' diyip alintiyi kanit metninde gosteremezse madde '⚠[kanitsiz]' isaretlenir. 'Bizde kullanim' cikarimdir, dogrulama disi.
Cikti: kartlar yerinde guncellenir (frontmatter dogrulama: ...), docs/site-inceleme/kart-dogrulama.tsv. Yeniden baslatilabilir. Claude yok."""
import asyncio, csv, json, os, re, sys, time, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import ucretsiz_havuz as h
from playwright.async_api import async_playwright

KOK = Path(__file__).resolve().parents[1]
KART = KOK / "docs/site-inceleme/kart"
CIKTI = KOK / "docs/site-inceleme/kart-dogrulama.tsv"
EV = KOK / ".kos/kopru/ara/kart-kanit"
JS = r"""()=>{const a=[...document.querySelectorAll('a[href]')].map(x=>x.href);
const lib=['three','gsap','Lenis','React','__NEXT_DATA__','Webflow'].filter(k=>window[k]||(k==='React'&&document.querySelector('#__next,#root')));
return 'LIB:'+lib.join(',')+' LINKS:'+[...new Set(a.filter(u=>/github\.com|download|pricing|licen[sc]e|\.zip|\.fig|\.glb/i.test(u)))].slice(0,15).join(' ')+' META:'+((document.querySelector('meta[name=description]')||{}).content||'')+' TEXT:'+document.body.innerText.replace(/\s+/g,' ').slice(0,6000)}"""
IST = """Asagida bir web sitesinin KANIT metni ve bu siteye dair kart maddeleri var. Her numarali madde icin kanit metninden destek var mi karar ver.
SADECE JSON ver: {"1":{"ok":true,"q":"kanit metninden BIREBIR kopyalanmis kisa alinti (<=12 kelime)"},"2":{"ok":false,"q":""},...}
Alinti kanit metninde harfi harfine gecmiyorsa ok:false say. Ozel adlar/sayilar/lisans/fiyat iddialari yalniz alinti ile desteklenir.
KANIT:
%s

MADDELER:
%s"""


def norm(s):
    return re.sub(r"\W+", " ", s.lower()).strip()


son = [""]
bos = [0]


def hakem(ev, maddeler, aile):
    num = "\n".join("%d. %s" % (i + 1, m) for i, m in enumerate(maddeler))
    for t in range(8):
        m = None
        try:
            m, k, _ = h.cagir("hakem", IST % (ev[:7000], num), max_tokens=900, haric_aile=aile, etiket="kart-dogrula",
                              dogrula=lambda x: None if re.search(r"\{.*\}", x, re.S) else "json yok")
            if m:
                return json.loads(re.search(r"\{.*\}", m, re.S).group(0)), k
        except PermissionError:
            time.sleep(1 + t)
            continue
        except Exception as e:
            son[0] = type(e).__name__ + str(e)[:40]
            time.sleep(5)
            continue
        print("  havuz bos, deneme", t + 1, son[0], flush=True)
        time.sleep(20)
    return None, ""


async def kanit(br, sem, url, ad):
    yol = EV / (ad + ".txt")
    if yol.exists():
        return yol.read_text(encoding="utf-8")
    async with sem:
        for u in (url, "https://web.archive.org/web/2/" + url):
            ctx = await br.new_context(viewport={"width": 1280, "height": 800})
            try:
                p = await ctx.new_page()
                await p.goto(u, wait_until="domcontentloaded", timeout=35000)
                await p.wait_for_timeout(2500)
                t = await p.evaluate(JS)
                if len(t) > 150:
                    yol.write_text(t, encoding="utf-8")
                    return t
            except Exception:
                pass
            finally:
                await ctx.close()
    return ""


async def bir(br, sem, ex, f, sat):
    ad = f.stem
    txt = f.read_text(encoding="utf-8")
    if "dogrulama:" in txt.split("---")[1]:
        return
    fm = txt.split("---")[1]
    url = re.search(r"site: (\S+)", fm).group(1)
    model = re.search(r"kart-modeli: (\S+)", fm)
    aile = (model.group(1).split("/")[0] if model else None)
    ev = await kanit(br, sem, url, ad)
    satirlar = txt.split("\n")
    bk = next((i for i, l in enumerate(satirlar) if "Bizde kullan" in l), len(satirlar))  # bolum alti cikarim: dogrulama disi
    idx = [i for i, l in enumerate(satirlar[:bk]) if re.match(r"\s*- ", l) and len(re.sub(r"[-*\s:]|\*\*", "", l)) > 20 and not re.match(r"^\s*- \*\*[^*]+\*\*:?\s*$", l)]
    sonuc, hk = (None, "")
    if len(ev) > 150 and idx:
        sonuc, hk = await asyncio.get_running_loop().run_in_executor(ex, hakem, ev, [satirlar[i].strip("- ").strip() for i in idx], aile)
        bos[0] = 0 if sonuc is not None else bos[0] + 1
        if bos[0] >= 3:  # havuz kotasi bitti: bos donguyle bekleme, durup yeniden baslatilabilir cik
            print("havuz tukendi (ardisik 3 kart hakemsiz), cikis; yeniden baslat", flush=True)
            os._exit(3)
    kanitli = kanitsiz = 0
    if sonuc is not None:
        en = norm(ev)
        for n, i in enumerate(idx, 1):
            r = sonuc.get(str(n)) or {}
            q = norm(r.get("q", ""))
            if r.get("ok") and len(q) > 6 and q in en:
                kanitli += 1
            else:
                kanitsiz += 1
                satirlar[i] = satirlar[i].rstrip() + " ⚠[kanitsiz]"
        durum = "dogrulandi"
    else:
        durum = "kanit-yok" if len(ev) <= 150 else "hakem-yok-" + re.sub(r"\W", "_", son[0])[:30]
    ust = "dogrulama: %s (kanitli=%d kanitsiz=%d hakem=%s)" % (durum, kanitli, kanitsiz, hk or "-")
    yeni = "\n".join(satirlar).replace("\n---\n", "\n" + ust + "\n---\n", 1)
    f.write_text(yeni, encoding="utf-8")
    sat.append([ad, durum, kanitli, kanitsiz, hk])
    print(len(sat), ad, durum, kanitli, kanitsiz, flush=True)


async def main():
    EV.mkdir(parents=True, exist_ok=True)
    fs = sorted(KART.glob("*.md"))
    sat = []
    sem, ex = asyncio.Semaphore(3), cf.ThreadPoolExecutor(2)
    async with async_playwright() as pw:
        br = await pw.chromium.launch(channel="chrome", headless=True)
        await asyncio.gather(*(bir(br, sem, ex, f, sat) for f in fs))
        await br.close()
    with open(CIKTI, "w", encoding="utf-8", newline="") as o:
        w = csv.writer(o, delimiter="	"); w.writerow(["kart", "durum", "kanitli", "kanitsiz", "hakem"])
        for f in fs:
            m = re.search(r"dogrulama: (\S+) \(kanitli=(\d+) kanitsiz=(\d+) hakem=(\S+)\)", f.read_text(encoding="utf-8"))
            w.writerow([f.stem] + list(m.groups()) if m else [f.stem, "yok", "", "", ""])
    print("bitti", len(sat))


asyncio.run(main())
