"""MOTOR-M5 son ölçüm: güncel motor (ikinci göz açık) beş altın set videosunu İKİ taze koşuyla tarar (izole KOS, ayrı partiler);
eşleme (olcum_m3b.esle) + görsel yargıç (olcum_m4.gorsel_yargi). Ölçütler ve altın set değişmez.

Kullanım (tools/video'da): uv run python olcum_m5.py <adim>...  (tara · esle · gorsel · rapor)
Paket: .kos/m4b/cache-m3b (M3b paketi; motor M3b + K1). Koşu başına tavan: Sonnet ≤10 çağrı / $1,03 (M3b-1 8 / $0,86 ×1,2;
form_red bir kez yeniden bu toplam içinde) · luna ≤$0,1 · Jev ≤150 durum (motor + eşleme) · yargıç ≤8 çağrı (motor + ölçüm).
"""
import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE3 = REPO / ".kos" / "m4b" / "cache-m3b"
os.environ["VIDEO_CACHE"] = str(CACHE3)  # olcum_m3b.CACHE ve cli.KOK içe aktarımda okur

import olcum_m3b as o3  # noqa: E402
import olcum_m4 as m4  # noqa: E402
from video import cli, hafif  # noqa: E402
from video import ikinci_goz as ig  # noqa: E402
from video import parti as pt  # noqa: E402

B = REPO / ".kos" / "m5"
KOSULAR = ("r1", "r2")
SONNET = [(3, .18), (4, .55), (3, .30)]  # Σ 10 / $1,03
IG_PARTI = {"or_usd": .033, "jev": 50, "yargic": 3}  # 3 parti → luna ≤$0,1 · Jev ≤150 · motor yargıcı ≤5 (video başına ≤1)
JEV, YARGIC = 300, 8  # ölçüm tavanları (koşu başına), motorunkilerden ayrı
M3B1 = {"yuksek": .90, "genel": .81, "day": .04, "usd": .8596, "cagri": 8}
M4C3 = {"yuksek": .92, "genel": .82, "day": .03, "usd": .932}
GURULTU = {"yuksek": 1.3, "genel": 5.0, "day": 1.5}


def _j(p, bos=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else bos


def _jy(p, d):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _kur(r):
    o3.KOS, o3.KOLLAR, o3.AD, o3.CACHE = B / r, {"sonnet": (None, SONNET)}, f"m5{r}", CACHE3
    o3.ATLA_RAPOR.add(ig.EK)
    m4.CACHE = CACHE3


def _motor(r):
    """Koşunun defterleri: Sonnet (çağrı, $, jeton) + ikinci göz toplamları + videolar."""
    s, g, vid = [0, 0.0, 0], dict.fromkeys(("luna", "or_usd", "jev", "yargic", "yargic_usd"), 0), {}
    for x in (_j(B / r / "tara.json") or {}).values():
        pdir = REPO / ".kos" / x["pid"]
        s = [a + b for a, b in zip(s, pt._defter(pdir))]
        g = {k: g[k] + v for k, v in pt._ig_defter(pdir).items()}
        vid |= {v: y["tarama"] for v, y in _j(pdir / "durum.json")["videolar"].items()}
    return s, g, vid


def tara():
    print(f"OPENROUTER_API_KEY var: {bool(os.environ.get('OPENROUTER_API_KEY'))}", flush=True)
    pt.IG_TAVAN = IG_PARTI
    C, U = sum(c for c, _ in SONNET), sum(u for _, u in SONNET)
    for r in KOSULAR:
        _kur(r)
        d = o3.tara()
        for anah, x in d.items():  # form_red (86HM0RUWhCk dahil) bir kez yeniden, koşu Σ 10 / $1,03 içinde
            n, u = sum(y["cagri"] for y in d.values()), sum(y["usd"] for y in d.values())
            if "form_red" not in x["videolar"].values() or n + 1 > C:
                continue
            env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(o3.KOS / "sonnet" / "rapor"), "PYTHONIOENCODING": "utf-8"}
            cli.main(["parti", "devam", x["pid"], "--form-red-yeniden", "--cagri-ek", "1", "--usd-ek", f"{max(0.0, U - u - .005):.4f}"], env=env)
            pdir = REPO / ".kos" / x["pid"]
            x["cagri"], x["usd"], x["jeton"] = pt._defter(pdir)
            x["videolar"] = {v: s["tarama"]["durum"] for v, s in _j(pdir / "durum.json")["videolar"].items()}
            o3._yaz("tara", d)
        s, g, vid = _motor(r)
        print(f"tara {r}: sonnet {s[0]} çağrı ${s[1]:.3f} · ikinci göz {g} · {({v: t['durum'] for v, t in vid.items()})}", flush=True)


def onar():
    """Devam K3: yalnız 86HM0RUWhCk, iki koşuda da. K1 kök neden Sonnet taramasında (r1: parti içi onarım çağrısı
    parti.py:351'de kalan parti $'ına kırpıldı → error_max_budget_usd → hata; r2: iki deneme form_red), ikinci gözde değil;
    bu yüzden motora dokunulmaz, ölçümün onarımı `hata`yı da kapsar. Video başına tavan: sonnet ≤3 çağrı / $0,35,
    luna ≤$0,02, motor yargıcı ≤1. Eski esle/gorsel `-eski` adıyla saklanır (yeniden ölçülecek)."""
    V = "86HM0RUWhCk"
    for r in KOSULAR:
        _kur(r)
        d = o3._oku("tara")
        for anah, x in d.items():
            dur = x["videolar"].get(V)
            if dur not in ("hata", "form_red"):
                continue
            pdir = REPO / ".kos" / x["pid"]
            durum = _j(pdir / "durum.json")
            c, u, _ = pt._defter(pdir)
            g = pt._ig_defter(pdir)
            pt.IG_TAVAN = {"or_usd": g["or_usd"] + .02, "jev": IG_PARTI["jev"], "yargic": g["yargic"] + 1}
            env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(o3.KOS / "sonnet" / "rapor"), "PYTHONIOENCODING": "utf-8"}
            print(f"onar {r} {anah} {V}: {dur} · harcanan {c} çağrı ${u:.3f} · ig {g} · tavan +3 / +$0,35", flush=True)
            cli.main(["parti", "devam", x["pid"], *(["--form-red-yeniden"] if dur == "form_red" else []),
                      f"--cagri-ek={c + 3 - durum['tavan']['cagri']}", f"--usd-ek={u + .35 - durum['tavan']['usd']:.4f}"], env=env)
            x["cagri"], x["usd"], x["jeton"] = pt._defter(pdir)
            x["videolar"] = {v: s["tarama"]["durum"] for v, s in _j(pdir / "durum.json")["videolar"].items()}
            o3._yaz("tara", d)
            print(f"onar {r}: {V} → {x['videolar'][V]} · parti {x['cagri']} çağrı ${x['usd']:.3f} · ig {pt._ig_defter(pdir)}", flush=True)
        for ad in ("esle", "gorsel"):
            if (p := B / r / f"{ad}.json").is_file():
                p.replace(B / r / f"{ad}-eski.json")


def esle():
    for r in KOSULAR:
        _kur(r)
        if (B / r / "esle.json").is_file():
            continue
        o3.JEV_TAVAN = JEV  # devam: ölçümün Jev tavanı motorunkinden ayrı (M3b ölçümüyle aynı)
        print(f"esle {r}: Jev tavanı {o3.JEV_TAVAN}", flush=True)
        o3.esle()


def gorsel():
    for r in KOSULAR:
        _kur(r)
        g = _j(B / r / "gorsel.json", {"g": {}, "cagri": 0, "usd": 0.0})
        tavan = YARGIC
        for vid, v in _j(B / r / "esle.json")["veri"].items():
            if vid in g["g"]:
                continue
            kv, paket = v["kollar"]["sonnet"], (CACHE3 / vid / "paket.md").read_text(encoding="utf-8")
            kal = {m["metin"]: m["zaman"] for j, x in (kv.get("k3") or {}).items()
                   if o3.k3_duzelt(m := kv["motor"][int(j)], x, paket) == "kare-doğrulanamadı"}
            if kal and g["cagri"] >= tavan:
                print(f"gorsel {r} {vid}: yargıç tavanı ({tavan}) — ölçülemedi", flush=True)
                continue
            if kal:
                p = pt.paket_oku(CACHE3 / vid / "paket.md")
                kz = [(k, t) for k, t in zip(p["kareler"], p["kare_zaman"]) if Path(k).is_file()]
                sec = {min(kz, key=lambda k: abs((k[1] or 0) - z))[0] for z in kal.values() if z is not None} if kz else set()
                sec = sorted(sec | ({k for k, _ in kz} if None in kal.values() else set()))[:8]
                et, usd = m4.gorsel_yargi(list(kal)[:40], sec, hafif.cagir, butce=.05, env=dict(os.environ))
                g["g"][vid], g["cagri"], g["usd"] = dict(zip(list(kal)[:40], et)), g["cagri"] + 1, g["usd"] + usd
                print(f"gorsel {r} {vid}: {len(kal)} kalem · {len(sec)} kare · ${usd:.3f}", flush=True)
            else:
                g["g"][vid] = {}
            _jy(B / r / "gorsel.json", g)


def _p(x):
    return f"%{100 * x:.1f}"


def rapor():
    oz = {}
    for r in KOSULAR:
        _kur(r)
        g = _j(B / r / "gorsel.json", {"g": {}, "cagri": 0, "usd": 0.0})
        o = m4.olc(_j(B / r / "esle.json")["veri"], lambda v: "sonnet", g["g"], "paket.md")
        s, ig_, vid = _motor(r)
        ek = [t.get("ikinci_goz") or {} for t in vid.values()]
        oz[r] = {"o": o, "y": o3.oran(o["m"]["yuksek"]), "ge": o3.oran(o["m"]["genel"]), "d": o3.oran(o["day"]), "s": s, "ig": ig_, "g": g,
                 "ekl": sum(x.get("eklenen", 0) for x in ek), "dog": sum(x.get("dogrulanamadi", 0) for x in ek),
                 "dur": {v: t["durum"] for v, t in vid.items()},
                 # devam: ölçülemeyen = görsel yargıç tavanı dışı + Jev tavanı dışı (K3'e hiç girmeyen) motor kalemi
                 "ol": o["say"]["ölçülemedi"] + _j(B / r / "esle.json")["jev"]["k3_dusen"]["sonnet"]}
    a, b = oz["r1"], oz["r2"]
    ort = {k: ((a[k] + b[k]) / 2, abs(a[k] - b[k]) / 2) for k in ("y", "ge", "d")}
    gec = {"y": ort["y"][0] >= .9, "ge": ort["ge"][0] >= .75, "d": ort["d"][0] <= .05}
    ad = {"y": "yüksek ≥%90", "ge": "genel ≥%75", "d": "dayanmayan ≤%5"}
    fark = {"y": ort["y"][0] - .9, "ge": ort["ge"][0] - .75, "d": .05 - ort["d"][0]}
    sonuc = "MÜKEMMEL"
    if not all(gec.values()):
        k = max((k for k in gec if not gec[k]), key=lambda k: fark[k])
        sonuc = f"DEĞİL — en yakın kalan ölçüt {ad[k]}: ortalama {_p(ort[k][0])} (fark {100 * fark[k]:+.1f} puan)"
    if any(z["ol"] > .05 * z["o"]["n"] for z in oz.values()):
        sonuc = "GEÇERSİZ — ölçülemeyen kalem >%5 (dayanmayan gerçek ölçülmedi)"
    usd = lambda z: z["s"][1] + z["ig"]["or_usd"] + z["ig"]["yargic_usd"]
    mx = lambda z: z["s"][0] + z["ig"]["yargic"]
    L = ["# M5 — son ölçüm (ikinci göz açık, iki taze koşu)", "",
         "Ölçütler (yüksek ≥%90 · genel ≥%75 · dayanmayan ≤%5) ve altın set değişmedi. Motor: M3b + K1 + ikinci göz (luna; özgü kalem Jev/görsel yargıçla doğrulanırsa).",
         f"Paket: .kos/m4b/cache-m3b (M3b-1 ile aynı girdi). Koşular izole: .kos/m5/r1 · .kos/m5/r2, ayrı partiler. Tavan (koşu başına): Sonnet 10 çağrı / $1,03 · luna $0,1 · Jev 150 durum · yargıç 8.",
         "", f"**SONUÇ: {sonuc}**", "",
         "## Koşular", "| koşu | yüksek | genel | dayanmayan | Sonnet çağrı | Sonnet $ | luna $ (çağrı) | Jev durum (motor) | yargıç motor/ölçüm | eklenen / doğrulanamadı | durumlar |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r, z in oz.items():
        L.append(f"| {r} | {_p(z['y'])} ({z['o']['m']['yuksek'][0]}/{z['o']['m']['yuksek'][1]}) | {_p(z['ge'])} ({z['o']['m']['genel'][0]}/{z['o']['m']['genel'][1]}) | "
                 f"{_p(z['d'])} ({z['o']['day'][0]}/{z['o']['day'][1]}) | {z['s'][0]} | {z['s'][1]:.3f} | {z['ig']['or_usd']:.4f} ({z['ig']['luna']}) | {z['ig']['jev']} | "
                 f"{z['ig']['yargic']}/{z['g']['cagri']} | {z['ekl']} / {z['dog']} | {' · '.join(f'{v[:4]} {d}' for v, d in z['dur'].items())} |")
    L += ["", "Ölçülemeyen motor kalemi (Jev/görsel yargıç tavanı dışı): " + " · ".join(f"{r} {z['ol']}/{z['o']['n']} ({_p(o3.oran((z['ol'], z['o']['n'])))})" for r, z in oz.items()),
          "Devam (K1): 86HM0RUWhCk ilk ölçümde r1 `hata` (Sonnet parti içi onarım çağrısı kalan parti $'ına kırpıldı, parti.py:351 → error_max_budget_usd) · "
          "r2 iki deneme form_red; ikinci gözden değil. `onar` yalnız bu video için hata/form_red'i yeniden taradı (≤3 çağrı / $0,35). "
          f"Ölçüm tavanları motordan ayrı: Jev {JEV} durum · görsel yargıç {YARGIC}/koşu."]
    L += ["", "## Ortalama ± yarı fark (ölçütlere karşı)", "| ölçüt | ortalama | ± | M4b gürültüsü (puan) | sonuç |", "|---|---|---|---|---|"]
    L += [f"| {ad[k]} | {_p(ort[k][0])} | {100 * ort[k][1]:.1f} | {GURULTU[{'y': 'yuksek', 'ge': 'genel', 'd': 'day'}[k]]} | {'GEÇTİ' if gec[k] else 'KALDI'} |" for k in ad]
    L += ["", "## Yan yana", "| | yüksek | genel | dayanmayan | $ (koşu) |", "|---|---|---|---|---|",
          f"| M3b-1 (tek koşu) | {_p(M3B1['yuksek'])} | {_p(M3B1['genel'])} | {_p(M3B1['day'])} | {M3B1['usd']:.3f} |",
          f"| M4c (iii) simülasyon | {_p(M4C3['yuksek'])} | {_p(M4C3['genel'])} | {_p(M4C3['day'])} | {M4C3['usd']:.3f} |",
          f"| M5 ortalama | {_p(ort['y'][0])} | {_p(ort['ge'][0])} | {_p(ort['d'][0])} | {(usd(a) + usd(b)) / 2:.3f} |"]
    kir = sorted(set(a["o"]["m"]["kirilim"]) | set(b["o"]["m"]["kirilim"]), key=lambda k: (k[0], o3.ONEM.index(k[1]) if k[1] in o3.ONEM else 9))
    L += ["", "## Kategori × önem (yakalama)", "| kategori | önem | r1 | r2 | ortalama |", "|---|---|---|---|---|"]
    for k in kir:
        x, y = a["o"]["m"]["kirilim"].get(k, (0, 0)), b["o"]["m"]["kirilim"].get(k, (0, 0))
        L.append(f"| {k[0]} | {k[1]} | {x[0]}/{x[1]} | {y[0]}/{y[1]} | {_p((o3.oran(x) + o3.oran(y)) / 2)} |")
    ek_v = ((a["ig"]["or_usd"] + a["ig"]["yargic_usd"]) + (b["ig"]["or_usd"] + b["ig"]["yargic_usd"])) / 2 / len(o3.VIDEOLAR)
    L += ["", "## Maliyet ve Max kotası",
          f"- Koşu $ (Sonnet + luna + motor yargıcı): r1 {usd(a):.3f} · r2 {usd(b):.3f} · ortalama {(usd(a) + usd(b)) / 2:.3f} (M3b-1 {M3B1['usd']:.3f})",
          f"- İkinci göz video başına ek $ (luna + yargıç, ortalama): {ek_v:.4f}",
          f"- Max kotası payı (Sonnet tarama + motor görsel yargıç çağrısı): r1 {mx(a)} · r2 {mx(b)} · ortalama {(mx(a) + mx(b)) / 2:.1f} "
          f"(m3b-1 {M3B1['cagri']} → %{100 * ((mx(a) + mx(b)) / 2 / M3B1['cagri'] - 1):+.0f}); ölçüm yargıcı ayrıca r1 {a['g']['cagri']} · r2 {b['g']['cagri']}",
          "", "## Kural 21",
          f"- ikinci göz: $ {M3B1['usd']:.3f} → {(usd(a) + usd(b)) / 2:.3f} (%{100 * ((usd(a) + usd(b)) / 2 / M3B1['usd'] - 1):+.0f}) · "
          f"yüksek {100 * (ort['y'][0] - M3B1['yuksek']):+.1f} · genel {100 * (ort['ge'][0] - M3B1['genel']):+.1f} · dayanmayan {100 * (ort['d'][0] - M3B1['day']):+.1f} puan "
          f"(M3b-1'e göre; gürültü yüksek ±{GURULTU['yuksek']} · genel ±{GURULTU['genel']} · dayanmayan ±{GURULTU['day']})"]
    (REPO / "docs" / "olcumler" / "m5-son-olcum.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"yazıldı: docs/olcumler/m5-son-olcum.md · {sonuc}", flush=True)
    for r, z in oz.items():
        print(f"{r}: yüksek {_p(z['y'])} · genel {_p(z['ge'])} · dayanmayan {_p(z['d'])} · sonnet {z['s'][0]} ${z['s'][1]:.3f} · ig {z['ig']} · eklenen {z['ekl']} / doğrulanamadı {z['dog']}", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    for a in sys.argv[1:]:
        {"tara": tara, "onar": onar, "esle": esle, "gorsel": gorsel, "rapor": rapor}[a]()
