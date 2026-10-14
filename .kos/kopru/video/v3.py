"""VİDEO-3 ölçüm: olc (V1 adım dökümü, .kos/*/defter.jsonl, claude -p yok) · taban (uzun altın: eski hat formu + jeton) · kos (uzun.izle + metin geçişi, Gemini) · puan.
cd tools/video && PYTHONPATH=. .venv/Scripts/python.exe ../../.kos/kopru/video/v3.py olc|taban|kos|puan
"""
import json
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from video import altin, kisa, uzun

ANA = Path(r"C:\Projeler\omer-skills")
ONB = Path(r"C:\Projeler\.video-cache")
CIK = ANA / ".kos" / "kopru" / "video" / "v3"
ALTIN = ("1nGx7WR8YLE", "aZe5ZTYcF1M", "d_UE-wHLoZY", "FaChtkkG9X4", "HYMDaMcuSGQ", "YDAK1lvVXho")  # docs/video-tarama/altin (Desktop doğrulamalı)


def agir(r):
    return r.get("girdi", 0) + 0.1 * r.get("onb_okuma", 0) + 1.25 * r.get("onb_yazma", 0) + 5 * r.get("cikti", 0)  # kisa_m4.agir ile aynı


def defterler():
    for p in (ANA / ".kos").glob("*/defter.jsonl"):
        for s in p.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(s)
            except ValueError:
                continue
            if r.get("videolar"):
                yield p.parent, r


def olc():
    """Adım başı ağırlıklı jeton (video başına paylaştırılmış) · uzun (YouTube) ve kısa (ig-) ayrı."""
    t = defaultdict(lambda: [0.0, 0.0, set()])
    for _, r in defterler():
        for v in r["videolar"]:
            k = t[("ig" if v.startswith("ig-") else "yt", r.get("adim", "?"))]
            k[0] += agir(r) / len(r["videolar"])
            k[1] += (r.get("sure") or 0) / len(r["videolar"])
            k[2].add(v)
            if r.get("adim") == "tarama":  # tarama içi kategori: çıktı ×5 = rapor yazımı · kare ≈1229 jeton (1280×720) önbellek yazımında · kalan = metin+sabit istem
                n, kare = len(r["videolar"]), 1.25 * 1229 * (r.get("kare") or 0)
                for ad, x in (("rapor_yazimi", 5 * r.get("cikti", 0)), ("kare", kare), ("metin_sabit", agir(r) - 5 * r.get("cikti", 0) - kare)):
                    t[("ig" if v.startswith("ig-") else "yt", f"  └ {ad}")][0] += x / n
                    t[("ig" if v.startswith("ig-") else "yt", f"  └ {ad}")][2].add(v)
    for tur in ("yt", "ig"):
        top = sum(v[0] for (a, ad), v in t.items() if a == tur and "└" not in ad)
        n = len(set().union(*(v[2] for (a, _), v in t.items() if a == tur)))
        print(f"{tur}: {n} video · Σ ağır {top:,.0f} · video başı {top / max(n, 1):,.0f}")
        for (a, adim), v in sorted(t.items(), key=lambda x: -x[1][0]):
            if a == tur:
                print(f"  {adim}\t%{100 * v[0] / top:.1f}\t{v[0] / len(v[2]):,.0f}/video\t{v[1] / len(v[2]):.0f} sn/video\t{len(v[2])} video")


def _son_form(v):
    """Eski hattın en yeni formu (sonnet+haiku birleşik) + o partinin defterinden video başı jeton/süre."""
    fs = sorted((p for p in (ANA / ".kos").glob(f"*/form/{v}.json")), key=lambda p: p.stat().st_mtime)
    if not fs:
        return None
    parti = fs[-1].parents[1]
    rs = [r for d, r in defterler() if d == parti and v in r["videolar"]]
    return (json.loads(fs[-1].read_text(encoding="utf-8")), parti.name, sum(agir(r) / len(r["videolar"]) for r in rs),
            sum((r.get("sure") or 0) / len(r["videolar"]) for r in rs))


def _kom(f):
    return [k.get("komut", "") if isinstance(k, dict) else str(k) for k in f.get("kurulum_komutlar") or f.get("komutlar") or []]


def _puan(md, v):
    p = altin.puan(md, json.loads((ANA / "docs" / "video-tarama" / "altin" / f"{v}.json").read_text(encoding="utf-8")))
    return {k: p[k] for k in ("yakalama", "isabet", "urller", "komutlar")} | {"link": p["link_aciklama"]["yakalama"]}


def taban():
    out = {}
    for v in ALTIN:
        x = _son_form(v)
        if not x:
            print(v, "form yok")
            continue
        f, parti, ag, sn = x
        md = uzun.rapor_md([a["ad"] for a in f.get("adaylar", [])], [b["url"] for b in f.get("aciklama_baglantilari", [])],
                           [u["url"] for u in f.get("urller", [])], _kom(f))
        out[v] = {"parti": parti, "agir": round(ag), "sure": round(sn, 1), **_puan(md, v)}
        print(v, out[v], flush=True)
    CIK.mkdir(parents=True, exist_ok=True)
    (CIK / "taban.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def kos():
    """Yalnız Gemini (Claude 0): uzun.izle ∥ metin geçişi → birleştir → paket linkleri. Önbellek gemini.json'u kisa ile ortak."""
    CIK.mkdir(parents=True, exist_ok=True)
    out = json.loads((CIK / "kos.json").read_text(encoding="utf-8")) if (CIK / "kos.json").is_file() else {}
    for v in ALTIN:
        d, t = ONB / v, time.monotonic()
        try:
            with ThreadPoolExecutor(2) as ex:
                fg, fm = ex.submit(uzun.izle, d), ex.submit(uzun.metin_gec, d)
                (g, gi), mg = fg.result(), fm.result()
        except RuntimeError as e:  # ücretsiz kota 429: video atlanmaz, sonraki koşuda önbellekten devam
            print(v, "HATA", str(e)[:160], flush=True)
            continue
        kisa.birlestir(g, mg)
        out[v] = {"g": g, "iz": gi, "metin": mg.get("_iz"), "sure": round(time.monotonic() - t, 1), "paket_link": kisa.paket_linkleri(d)}
        print(v, gi, out[v]["sure"], len(g["araclar"]), flush=True)
        (CIK / "kos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    (CIK / "kos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("BITTI")


def puan():
    t = json.loads((CIK / "taban.json").read_text(encoding="utf-8"))
    y = json.loads((CIK / "kos.json").read_text(encoding="utf-8"))
    print("video\tkol\taday\tisabet\turl\tkomut\tlink\tağır_tk\tsn")
    for v in ALTIN:
        if v in t:
            print(v, "taban", *(t[v][k] for k in ("yakalama", "isabet", "urller", "komutlar", "link", "agir", "sure")), sep="\t")
        if v in y:
            g, ln = y[v]["g"], y[v]["paket_link"]
            md = uzun.rapor_md([a["ad"] for a in g["araclar"]], ln, list(dict.fromkeys(g["linkler"] + ln)), g["komutlar"])
            p = _puan(md, v)
            print(v, "yeni", *(p[k] for k in ("yakalama", "isabet", "urller", "komutlar", "link")), 0, y[v]["sure"], sep="\t")


def oturum():
    """Claude adımı: kos.json Gemini çıktıları → kisa.blok (katalog durumu) → tek claude -p (kisa.oturum) → v3/oturum.json + puan.
    shortcut: araştırma künyesi (gh) yok — yalnız not kalitesini etkiler, yakalama/isabeti değil; uçtan uca hatta kisa.calistir'daki gibi eklenir."""
    y = json.loads((CIK / "kos.json").read_text(encoding="utf-8"))
    bl = []
    for v in ALTIN:
        g = uzun.son(ONB / v, json.loads(json.dumps(y[v]["g"])))  # d4: sözlük adayı + istem yankısı süzgeci
        if isinstance(g.get("ekran_metni"), str):  # uzun.birlestir metni tek dizgeye katıyor; blok liste bekler
            g["ekran_metni"] = g["ekran_metni"].splitlines()
        g["linkler"] = list(dict.fromkeys(g["linkler"] + y[v]["paket_link"]))
        bl.append(kisa.blok(v, g, kisa.katalog([a["ad"] for a in g["araclar"]], kok=ONB, vid=v), {}))
    r = kisa.oturum(bl, "low")
    u = r.get("usage") or {}
    r["agir"] = round(agir({"girdi": u.get("input_tokens", 0), "onb_okuma": u.get("cache_read_input_tokens", 0),
                            "onb_yazma": u.get("cache_creation_input_tokens", 0), "cikti": u.get("output_tokens", 0)}))
    (CIK / "oturum.json").write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ağır", r["agir"], "video başı", r["agir"] // len(ALTIN), "sn", r.get("sure"), "hata", r.get("hata"))
    for x in (r["form"] or {}).get("videolar", []):
        ln = y[x["id"]]["paket_link"]
        p = _puan(uzun.rapor_md([a["ad"] for a in x["araclar"]], ln, list(dict.fromkeys(x["linkler"] + ln)), y[x["id"]]["g"]["komutlar"]), x["id"])
        print(x["id"], p, flush=True)
    print("BITTI")


def kacak():
    """Kaçan sınıflama + temiz kapı (kisa 19:15/20:30 kuralı): teknik araç sayımına girmez; pakette geçmeyen altın kalemi temiz paydaya girmez
    (listelenir); yp = altında eşi yok VE pakette geçmiyor. Kaynak: v3/oturum.json (yoksa kos.json Gemini adları)."""
    y = json.loads((CIK / "kos.json").read_text(encoding="utf-8"))
    o = CIK / (sys.argv[2:] or ["oturum.json"])[0]
    form = {x["id"]: x for x in json.loads(o.read_text(encoding="utf-8"))["form"]["videolar"]} if o.is_file() else {}
    if "son" in sys.argv[2:]:  # Claude'suz: kos.json Gemini çıktısı + uzun.son (Claude ad eklemiyor, d3)
        form = {v: uzun.son(ONB / v, json.loads(json.dumps(y[v]["g"]))) for v in ALTIN}
    top = [0, 0, 0, 0, 0]
    for v in ALTIN:
        a = json.loads((ANA / "docs" / "video-tarama" / "altin" / f"{v}.json").read_text(encoding="utf-8"))
        adlar = [x["ad"] for x in (form.get(v) or y[v]["g"])["araclar"] if "teknik" not in (x.get("tur") or "").lower() + (x.get("ne_dedi") or "")]  # teknik ayrı alan (kisa 19:15)
        kel = [altin.norm(w) for w in re.findall(r"\w+", (ONB / v / "paket.md").read_text(encoding="utf-8").casefold())]
        duz, pen = "".join(kel), {"".join(kel[i:i + k]) for k in range(1, 6) for i in range(len(kel))}
        pakette = lambda xs: any(altin.gecer(x, duz, pen) for x in xs)  # noqa: E731
        ar = [x for x in a["adaylar"] if x["tur"] in altin.ADAY_TUR and x["tur"] != "teknik" and not x.get("belirsiz")]
        bul = lambda x: any(altin._icerir(r, [x["ad"], *x.get("alias", [])]) for r in adlar)  # noqa: E731
        kn = [x for x in ar if pakette([x["ad"], *x.get("alias", [])])]
        yp = [r for r in adlar if not any(altin._icerir(r, [x["ad"], *x.get("alias", [])]) for x in a["adaylar"]) and not pakette([r])]
        s = (sum(map(bul, ar)), len(ar), sum(map(bul, kn)), len(kn), len(yp))
        top = [t + z for t, z in zip(top, s)]
        print(f"{v}\taraç {s[0]}/{s[1]}\ttemiz {s[2]}/{s[3]}\typ {s[4]} {yp[:6]}")
        for x in ar:
            if not bul(x):
                print(f"  {'PAKETTE' if x in kn else 'kanıtsız'}\t{x['tur']}\t{x['ad']}\t{x.get('kaynak', '')}")
    print(f"TOPLAM araç {top[0]}/{top[1]} = {top[0] / top[1]:.3f} · temiz {top[2]}/{top[3]} = {top[2] / top[3]:.3f} · yp {top[4]}")


KARUSEL = ("ig-DdrEmDHkouJ", "ig-DePQ2O3ElPy", "ig-Dd7WYSniFvP")  # en çok slaytlı, eski hat formu olan carousel'ler (sonuncusu slayt videolu)


def karusel():
    """V3: referans = eski hat formu, yalnız paket.md'de (açıklama/OCR) kanıtlı kalemler · yeni kol = kisa.izle (slayt görselleri) + metin geçişi."""
    import kisa_m4 as m  # aynı dizin; yalnız okunur (VİDEO-KISA-TOKEN-1 dosyası)
    out = json.loads((CIK / "karusel.json").read_text(encoding="utf-8")) if (CIK / "karusel.json").is_file() else {}
    print("video\tref_araç\tref_link\taraç_yak\tlink_yak\typ\ttaban_ağır\ttaban_sn\tyeni_sn")
    for v in KARUSEL:
        d = ONB / v
        f, _, ag, sn = _son_form(v)
        sat = (d / "paket.md").read_text(encoding="utf-8").splitlines()
        rad, rln = m.ogeler(f, v)
        rad = {a for a in rad if m._kanit(a, sat)}  # kanıtsız referans paydaya girmez (aşırı uyumsuz kapı)
        rln = {u for u in rln if u in "\n".join(sat).lower()}
        if v not in out:
            t = time.monotonic()
            with ThreadPoolExecutor(2) as ex:
                fg, fm = ex.submit(kisa.izle, d), ex.submit(kisa.metin_gec, d)
                (g, gi), mg = fg.result(), fm.result()
            kisa.birlestir(g, mg)
            out[v] = {"g": g, "iz": gi, "sure": round(time.monotonic() - t, 1), "paket_link": kisa.paket_linkleri(d)}
            (CIK / "karusel.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        g = out[v]["g"]
        ad = {a["ad"] for a in g["araclar"]}
        ln = {m._url(u) for u in g["linkler"] + out[v]["paket_link"]}
        ya, yl, yp, _ = m.olc(ad, ln, rad, rln, m.tr.normal("\n".join(sat)))
        print(v, len(rad), len(rln), round(ya, 3), yl if yl is None else round(yl, 3), yp, round(ag), round(sn), out[v]["sure"], sep="\t")
    print("BITTI")


if __name__ == "__main__":
    {"olc": olc, "taban": taban, "kos": kos, "puan": puan, "karusel": karusel, "oturum": oturum, "kacak": kacak}[sys.argv[1]]()
