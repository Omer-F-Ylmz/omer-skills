"""KÜTÜPHANE-4: profil TSV'lerini karşılaştırır. Tek turlu görevlerde bağlam = sabit önek (temiz ölçü); kalite/isabet/USD tüm görevler.
  python tools/olcum/karsilastir.py 2026-10-10 tam nameonly75 tam75 [...]   → tablo + docs/kutuphane/olcum/<tarih>-karsilastirma.md"""
import sys
from pathlib import Path

D = Path(__file__).resolve().parents[2] / "docs" / "kutuphane" / "olcum"


def oku(tarih, ad):
    y = D / f"{tarih}-{ad}.tsv"
    if not y.exists():
        return {}
    L = y.read_text(encoding="utf-8").splitlines()
    b = L[0].split("\t")
    return {r[0]: dict(zip(b, r)) for r in (l.split("\t") for l in L[1:]) if len(r) >= len(b) - 2}


def ozet(rows, ortak):
    tek = [r for g, r in rows.items() if g in ortak and r["tur"] == "1"]
    f = lambda k, rs: sum(float(r[k]) for r in rs)
    return {"gorev": len([g for g in rows if g in ortak]),
            "tek_tur_baglam_ort": round(f("baglam", tek) / len(tek)) if tek else 0,
            "usd": round(f("usd", [rows[g] for g in ortak]), 3),
            "kalite": int(f("kalite", [rows[g] for g in ortak])),
            "isabet": int(f("arac_isabet", [rows[g] for g in ortak])),
            "out": int(f("output", [rows[g] for g in ortak]))}


def main(a):
    tarih, adlar = a[0], a[1:]
    veri = {ad: oku(tarih, ad) for ad in adlar}
    ortak = set.intersection(*(set(v) for v in veri.values() if v))
    sat = [f"# Karşılaştırma {tarih} — ortak görev {len(ortak)}: {', '.join(sorted(ortak))}", "",
           "| profil | görev | tek-tur bağlam ort. | USD | kalite (toplam) | araç isabeti | çıktı jeton |", "|---|---|---|---|---|---|---|"]
    taban = None
    for ad in adlar:
        if not veri[ad]:
            continue
        o = ozet(veri[ad], ortak)
        taban = taban or o
        fark = lambda k: f" ({(o[k] - taban[k]) / taban[k] * 100:+.0f}%)" if taban[k] and ad != adlar[0] else ""
        sat.append(f"| {ad} | {o['gorev']} | {o['tek_tur_baglam_ort']}{fark('tek_tur_baglam_ort')} | {o['usd']}{fark('usd')} | {o['kalite']} | {o['isabet']} | {o['out']} |")
    sat += ["", "Görev bazında kalite/isabet:", "", "| görev | " + " | ".join(adlar) + " |", "|---|" + "---|" * len(adlar)]
    for g in sorted(ortak):
        sat.append(f"| {g} | " + " | ".join(f"{veri[a][g]['kalite']}/{veri[a][g]['arac_isabet']}" for a in adlar if veri[a]) + " |")
    metin = "\n".join(sat) + "\n"
    (D / f"{tarih}-karsilastirma.md").write_text(metin, encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(metin)


if __name__ == "__main__":
    main(sys.argv[1:])
