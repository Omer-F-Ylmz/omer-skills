"""VİDEO-16 A/B: 3 sabit short (2026-10-12-short, paket önbellekte) — taban vs VIDEO_SHORT_HIZ=<efor>. Video başı _tara_ikili (iki kol eşzamanlı)
duvar süresi + jeton + $; kalite: birleşik form kalemlerinin Jev 'dayanir' oranı (kaynakta dayanağı olan kalem) + taban kalemlerini kapsama
(ikinci_goz.ozgu anahtar kesişimi; taban r1↔r2 gürültü tabanı).
Kullanım (tools/video'da): uv run python olcum_v16.py kos <kol> <tekrar>   (kol: taban | low | medium) → .kos/v16/<kol>-<tekrar>.json
                           uv run python olcum_v16.py rapor               → .kos/v16/rapor.json + özet
Tavan: koşu başına 6 claude -p (3 video × 2 kol), video başına $0.5 · Jev ≤ 400 durum (rapor adımı).
"""
import json
import os
import sys
import time
from pathlib import Path

from video import cli, hafif
from video import ikinci_goz as ig
from video import parti as pt

REPO = Path(__file__).resolve().parents[2]
ANA = Path(r"C:\Projeler\omer-skills")  # parti günlükleri ana çalışma ağacında
ONB = Path(r"C:\Projeler\.video-cache")
B = ANA / ".kos" / "v16"
VIDEOLAR = ("ig-DeW7JHrgsXb", "ig-DeV9nZPtSsC", "ig-DeHMM45NaFt")  # 28 · 38 · 64 sn
MODELLER = ["claude-sonnet-5-5", "claude-haiku-5-5"]
JEV_TAVAN = 400


def kos(kol, tekrar):
    """d5: kol = <efor>[-d0][-s|-h|-ss|-ssb] — ss/ssb: VIDEO_SHORT_KOL (ssb: ikinci sonnet dar şema) · d0: MAX_THINKING_TOKENS=0 (düşünmesiz) · s/h: tek kol sonnet/haiku. Kol başı süre "kollar"a yazılır."""
    efor, *ek = kol.split("-")
    env = {k: v for k, v in os.environ.items() if k not in ("VIDEO_SHORT_HIZ", "VIDEO_SHORT_KOL", "ANTHROPIC_API_KEY")}
    if efor != "taban":
        env["VIDEO_SHORT_HIZ"] = efor
    env["VIDEO_SHORT_KOL"] = next((x for x in ek if x in ("ss", "ssb")), "0")  # d7: short varsayılanı ss → eski kollar "0" ile sabit
    if "d0" in ek:
        env["MAX_THINKING_TOKENS"] = "0"
    modeller = [m for m in MODELLER if not ({"s", "h"} & set(ek)) or m.split("-")[1][0] in ek]
    kayit = []

    def cagir(*a, **k):
        y = hafif.cagir(*a, **k)
        kayit.append({"model": k.get("model"), "sure": y.get("sure"), "cikti": (y.get("usage") or {}).get("output_tokens", 0), "usd": y.get("usd")})
        return y
    pdir = B / f"{kol}-{tekrar}"
    pdir.mkdir(parents=True, exist_ok=True)
    pk = {v: pt.paket_oku(ONB / v / "paket.md") for v in VIDEOLAR}
    pt.kare_sigdir(pk, ONB)
    assert all(p["short"] for p in pk.values()), "altın kümede short olmayan video"
    d = {"butce": .5, "tavan": {"usd": 5.0}, "videolar": {v: {"tarama": {}} for v in VIDEOLAR}}
    temizle = lambda s: cli._temizle(s, env)
    sonuc = {}
    for v in VIDEOLAR:
        t0, kayit[:] = time.time(), []
        y = pt._tara_ikili([v], pk, {}, temizle, d, pdir, env, cagir, modeller)
        u = y.get("usage") or {}
        sonuc[v] = {"duvar": round(time.time() - t0, 1), "usd": y.get("usd"), "cagri": y.get("cagri"), "hata": y.get("hata"),
                    "cikti": u.get("output_tokens", 0), "girdi": u.get("input_tokens", 0), "onb_okuma": u.get("cache_read_input_tokens", 0),
                    "onb_yazma": u.get("cache_creation_input_tokens", 0), "kunye": d["videolar"][v]["tarama"].get("kunye"),
                    "form": (y.get("form") or {}).get("videolar", [None])[0], "kollar": list(kayit)}
        print(v, sonuc[v]["duvar"], "sn", sonuc[v]["usd"], "$", sonuc[v]["hata"], flush=True)
    (B / f"{kol}-{tekrar}.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")


def kapsam(f, taban):
    """taban kalemlerinden f'de anahtar karşılığı olanların oranı."""
    n = len(ig.kalemler(taban))
    return 1.0 if not n else round(1 - len(ig.ozgu(f, taban)) / n, 3)


def kapsam_d(f, taban, dogru):
    """taban'ın Jev'in kaynakta dayanağını bulduğu kalemlerinden f'de anahtar karşılığı olanların oranı (doğru bilgi kaybı)."""
    s = set().union(*(a for _, _, a in ig.kalemler(f)))
    t = [a for i, (_, _, a) in enumerate(ig.kalemler(taban)) if i in dogru]
    return round(sum(bool(a & s) for a in t) / len(t), 3) if t else None


def tek(*kosular):
    """d5 kol katkısı: kayıtlı koşuların sonnet kol formundan sanal tek kol koşusu sonnet-<n>.json (claude -p yok; duvar = sonnet kol süresi)."""
    for n, ad in enumerate(kosular, 1):
        s, out = json.loads((B / f"{ad}.json").read_text(encoding="utf-8")), {}
        for v, x in s.items():
            k = next(k for k in x["kollar"] if "sonnet" in k["model"])
            out[v] = {"duvar": k["sure"], "usd": k["usd"], "cikti": k["cikti"], "onb_okuma": 0, "hata": None, "kunye": f"tek kol: {ad}",
                      "form": json.loads((B / ad / "form" / f"{v}.sonnet.json").read_text(encoding="utf-8"))}
        (B / f"sonnet-{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def cift(*kosular):
    """d5: sonnet×2 (haiku yerine ikinci sonnet low) — kayıtlı koşuların sonnet formları ikişer birlestir → ss-<n>.json (0 -p; duvar = iki kolun büyüğü)."""
    s = {ad: json.loads((B / f"{ad}.json").read_text(encoding="utf-8")) for ad in kosular}
    cifter = [(a, b) for i, a in enumerate(kosular) for b in kosular[i + 1:]]
    for n, (a, b) in enumerate(cifter, 1):
        out = {}
        for v in VIDEOLAR:
            k = [next(k for k in s[x][v]["kollar"] if "sonnet" in k["model"]) for x in (a, b)]
            f = [json.loads((B / x / "form" / f"{v}.sonnet.json").read_text(encoding="utf-8")) for x in (a, b)]
            out[v] = {"duvar": max(x["sure"] for x in k), "usd": sum(x["usd"] for x in k), "cikti": sum(x["cikti"] for x in k), "onb_okuma": 0,
                      "hata": None, "kunye": f"sonnet×2: {a}+{b}", "form": pt.birlestir(*f)}
        (B / f"ss-{n}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def rapor(*secili):
    kos_ = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(B.glob("*-*.json")) if not secili or p.stem in secili}
    pk = {v: pt.paket_oku(ONB / v / "paket.md") for v in VIDEOLAR}
    durum, yer = [], []
    for ad, s in kos_.items():
        for v in VIDEOLAR:
            for i, (b, k, _) in enumerate(ig.kalemler(s[v]["form"] or {})):
                if b != "kareden_okunanlar" and k.get("kaynak") != "kare":
                    durum.append(f"kalem:\n[{b}] {ig._duz(k)[:400]}\n\nkaynak:\n{ig.kesit(k, pk[v]['metin'])}")
                    yer.append((ad, v, i))
    assert len(durum) <= JEV_TAVAN, f"Jev tavanı: {len(durum)} > {JEV_TAVAN}"
    r = pt._jev(os.environ)(durum, ig.Q)
    jev, dogru = {}, {}
    for (ad, v, i), x in zip(yer, r):
        s = ((x or {}).get("dayanir") or {}).get("noul")
        if s is not None:
            jev.setdefault((ad, v), []).append(s >= .5)
            if s >= .5:
                dogru.setdefault((ad, v), set()).add(i)
    ozet = {}
    for ad, s in kos_.items():
        kol = ad.rsplit("-", 1)[0]
        for v in VIDEOLAR:
            tl = [t for t in kos_ if t.startswith("taban-") and t != ad]
            taban = [kos_[t][v]["form"] or {} for t in tl]
            kd = [kapsam_d(s[v]["form"] or {}, kos_[t][v]["form"] or {}, dogru.get((t, v), set())) for t in tl]
            kd = [x for x in kd if x is not None]
            j = jev.get((ad, v), [])
            ozet.setdefault(kol, []).append({"kos": ad, "v": v, **{k: s[v][k] for k in ("duvar", "usd", "cikti", "onb_okuma", "hata")},
                                             "kalem": len(ig.kalemler(s[v]["form"] or {})), "dayanir": round(sum(j) / len(j), 3) if j else None,
                                             "kapsam": round(sum(kapsam(s[v]["form"] or {}, t) for t in taban) / len(taban), 3) if taban else None,
                                             "kapsam_d": round(sum(kd) / len(kd), 3) if kd else None})
    ort = lambda xs: round(sum(xs) / len(xs), 3) if xs else None
    tablo = {kol: {k: ort([x[k] for x in xs if x[k] is not None]) for k in ("duvar", "usd", "cikti", "onb_okuma", "kalem", "dayanir", "kapsam", "kapsam_d")}
             for kol, xs in ozet.items()}
    (B / "rapor.json").write_text(json.dumps({"tablo": tablo, "satir": ozet, "jev_durum": len(durum)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(tablo, ensure_ascii=False, indent=1), "\njev durum:", len(durum))


if __name__ == "__main__":
    {"kos": lambda: kos(sys.argv[2], sys.argv[3]), "rapor": lambda: rapor(*sys.argv[2:]), "tek": lambda: tek(*sys.argv[2:]), "cift": lambda: cift(*sys.argv[2:])}[sys.argv[1]]()
