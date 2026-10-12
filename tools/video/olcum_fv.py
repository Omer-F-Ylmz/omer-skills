"""FABLE-VIDEO A/B: 12 sabit IG short (paket önbellekte) — taban vs VIDEO_FABLE_PROTOKOL=1 (yalnız Sonnet çağrısına önek; Haiku'ya
uygulanmadığından ikili taramanın Haiku yarısı iki kolda aynıdır → yalnız Sonnet koşulur). olcum_v16.py (kol/video-shorts) kopyası.
Ölçü: duvar + jeton + $ + tamam_eksik; kalite: form kalemlerinin Jev 'dayanir' oranı + taban kalemlerini kapsama (taban r1↔r2 gürültü tabanı).
Kullanım (tools/video'da): .venv python olcum_fv.py kos <taban|fable> <tekrar> → .kos/fv/<kol>-<tekrar>.json · olcum_fv.py rapor
Tavan: koşu başına 12 claude -p (4 koşu = 48), video başına $0.5, Σ $6 (aşılırsa koşu başlamaz) · Jev ≤ 1500 durum (rapor adımı).
d3 (13 Eki): taban = VİDEO-16 low (kol/video-shorts); kollar taban/A/B/C (VIDEO_FABLE_PROTOKOL), ilk 9 video × 1 = 36 -p → .kos/fv3;
kapsam/kapsam_d sabit dış referansa göre: d1 taban-1/2 formları (.kos/fv, high efor) — ref satırı ref-1↔ref-2 gürültü tabanıdır.
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
B = ANA / ".kos" / "fv3"
REF = ANA / ".kos" / "fv"  # d1 taban formları
VIDEOLAR = ("ig-DeW7JHrgsXb", "ig-DeV9nZPtSsC", "ig-DeHMM45NaFt", "ig-DdrNeEUN63i", "ig-DY_SoPGKv2A", "ig-Db_H8ScP5y-",
            "ig-DdlurQHG2Mm", "ig-Dcd3eY1iOMA", "ig-DeON0MOB5oi", "ig-DYx4OuVuJuI", "ig-DcRhD2Nto7M", "ig-DdWmIHTC322")[:9]
KOLLAR = {"taban": None, "fable": "1", "A": "A", "B": "B", "C": "C"}
MODELLER = ["claude-sonnet-5-5"]
JEV_TAVAN = 1500
USD_TAVAN = 6.0


def kos(kol, tekrar):
    harcanan = sum(x["usd"] or 0 for p in B.glob("*-*.json") for x in json.loads(p.read_text(encoding="utf-8")).values())
    assert harcanan < USD_TAVAN, f"$ tavanı: {harcanan:.2f} ≥ {USD_TAVAN}"
    env = {k: v for k, v in os.environ.items() if k != "VIDEO_FABLE_PROTOKOL"}
    if KOLLAR[kol]:
        env["VIDEO_FABLE_PROTOKOL"] = KOLLAR[kol]
    pdir = B / f"{kol}-{tekrar}"
    pdir.mkdir(parents=True, exist_ok=True)
    pk = {v: pt.paket_oku(ONB / v / "paket.md") for v in VIDEOLAR}
    pt.kare_sigdir(pk, ONB)
    assert all(p["short"] for p in pk.values()), "altın kümede short olmayan video"
    d = {"butce": .5, "tavan": {"usd": 5.0}, "videolar": {v: {"tarama": {}} for v in VIDEOLAR}}
    temizle = lambda s: cli._temizle(s, env)
    sonuc = {}
    for v in VIDEOLAR:
        t0 = time.time()
        y = pt._tara_ikili([v], pk, {}, temizle, d, pdir, env, hafif.cagir, MODELLER)
        u = y.get("usage") or {}
        sonuc[v] = {"duvar": round(time.time() - t0, 1), "usd": y.get("usd"), "cagri": y.get("cagri"), "hata": y.get("hata"),
                    "cikti": u.get("output_tokens", 0), "girdi": u.get("input_tokens", 0), "onb_okuma": u.get("cache_read_input_tokens", 0),
                    "onb_yazma": u.get("cache_creation_input_tokens", 0), "kunye": d["videolar"][v]["tarama"].get("kunye"),
                    "eksik": int(bool(y.get("hata") or pt.dogrula(y.get("form"), pk, [v]).get(v))),  # 1. turda form reddi → tamam_eksik/2. tur adayı
                    "form": (y.get("form") or {}).get("videolar", [None])[0]}
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


def rapor():
    kos_ = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(B.glob("*-*.json"))}
    kos_.update({f"ref-{i}": json.loads((REF / f"taban-{i}.json").read_text(encoding="utf-8")) for i in (1, 2)})
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
            tl = [t for t in kos_ if t.startswith("ref-") and t != ad]
            taban = [kos_[t][v]["form"] or {} for t in tl]
            kd = [kapsam_d(s[v]["form"] or {}, kos_[t][v]["form"] or {}, dogru.get((t, v), set())) for t in tl]
            kd = [x for x in kd if x is not None]
            j = jev.get((ad, v), [])
            ozet.setdefault(kol, []).append({"kos": ad, "v": v, **{k: s[v][k] for k in ("duvar", "usd", "cikti", "onb_okuma", "eksik", "hata")},
                                             "kalem": len(ig.kalemler(s[v]["form"] or {})), "dayanir": round(sum(j) / len(j), 3) if j else None,
                                             "kapsam": round(sum(kapsam(s[v]["form"] or {}, t) for t in taban) / len(taban), 3) if taban else None,
                                             "kapsam_d": round(sum(kd) / len(kd), 3) if kd else None})
    ort = lambda xs: round(sum(xs) / len(xs), 3) if xs else None
    tablo = {kol: {k: ort([x[k] for x in xs if x[k] is not None]) for k in ("duvar", "usd", "cikti", "onb_okuma", "eksik", "kalem", "dayanir", "kapsam", "kapsam_d")}
             for kol, xs in ozet.items()}
    (B / "rapor.json").write_text(json.dumps({"tablo": tablo, "satir": ozet, "jev_durum": len(durum)}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(tablo, ensure_ascii=False, indent=1), "\njev durum:", len(durum))


if __name__ == "__main__":
    {"kos": lambda: kos(sys.argv[2], sys.argv[3]), "rapor": rapor}[sys.argv[1]]()
