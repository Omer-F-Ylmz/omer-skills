"""FABLE-1 ölçüm tablosu: kol başına ortalama kalite/çıktı jetonu/$/tur + KABUL kararı (fable-1.md 4. adım).
  python tools/olcum/fable1_tablo.py                  # d3: 2026-10-12* · proto
  python tools/olcum/fable1_tablo.py 2026-10-12d kisa # d4: model başına KABUL = kalite ≥ taban VE çıktı ≤ taban VE $ ≤ taban
  python tools/olcum/fable1_tablo.py 2026-10-12d kisa jev  # kalite = jev sütunu (önce jev_yargic --tsv-yaz; regex 10'da doyuyor)
Geçerli satır: çıktı jetonu > 0 ve timeout yok (ağ kopması/timeout satırları dışarı). Görev başına ortalama, sonra görevler üstü ortalama
(tekrar sayısı farklı kollar adil kalsın)."""
import csv
import sys
from pathlib import Path
from statistics import mean

OLCUM = Path(__file__).resolve().parents[2] / "docs" / "kutuphane" / "olcum"
GOREVLER = ["G02", "G12", "J01", "G13"]
KOLLAR = ["fable", "s-taban", "s-proto", "h-taban", "h-proto"]
TARIH = "2026-10-12*"
KALITE = "kalite"


def satirlar(kol):
    for yol in sorted(OLCUM.glob(f"{TARIH}-fable1-{kol}.tsv")):
        with open(yol, encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                if r["gorev"] in GOREVLER and int(r["output"] or 0) > 0 and "timeout" not in (r.get("hata") or "") and r.get(KALITE):
                    yield r


def ozet(kol):
    gorev = {}
    for r in satirlar(kol):
        gorev.setdefault(r["gorev"], []).append(r)
    if not gorev:
        return None
    alan = lambda k: mean(mean(float(r[k]) for r in rs) for rs in gorev.values())
    return {"n": sum(map(len, gorev.values())), "gorev": sorted(gorev), "kalite": alan(KALITE),
            "output": alan("output"), "usd": alan("usd"), "tur": alan("tur"),
            "gorev_kalite": {g: mean(float(r[KALITE]) for r in rs) for g, rs in gorev.items()},
            "g": {g: {k: mean(float(r[k]) for r in rs) for k in ("output", "usd")} for g, rs in gorev.items()}}


def karar(o):
    """Ortak görevlerde proto ≥ taban (her model), ortalama artış > 0 ya da eşit kalitede çıktı jetonu düşüşü, $ artışı ≤ %10."""
    sonuc, artislar = [], []
    for m in ("s", "h"):
        t, p = o.get(f"{m}-taban"), o.get(f"{m}-proto")
        if not t or not p:
            return f"EKSİK ({m}: taban/proto verisi yok)"
        ortak = sorted(set(t["gorev_kalite"]) & set(p["gorev_kalite"]))
        kt = mean(t["gorev_kalite"][g] for g in ortak)
        kp = mean(p["gorev_kalite"][g] for g in ortak)
        artislar.append(kp - kt)
        top = lambda x, k: sum(x["g"][g][k] for g in ortak)  # $/jeton yalnız ortak görevlerde
        usd = (top(p, "usd") - top(t, "usd")) / top(t, "usd") * 100
        jet = (top(p, "output") - top(t, "output")) / top(t, "output") * 100
        o[f"{m}-jet"] = jet
        sonuc.append(f"{m}: kalite {kt:.2f}->{kp:.2f} ({ortak}) · çıktı {jet:+.0f}% · $ {usd:+.0f}%")
        if kp < kt or usd > 10:
            return "RET — " + " | ".join(sonuc)
    # Ömer d3: "kalite düşmez, token düşer" → kalite eşitse çıktı jetonu iki modelde de düşmeli
    ok = mean(artislar) > 0 or all(o[f"{m}-jet"] < 0 for m in ("s", "h"))
    return ("KABUL — " if ok else "RET — ") + " | ".join(sonuc)


def karar_d4(o, ek):
    """Ömer 10 Eki: kalite ASLA düşmez, token her adımda AZALIR → model başına ayrı karar, ortak görevlerde."""
    sonuc = []
    for m in ("s", "h"):
        t, p = o.get(f"{m}-taban"), o.get(f"{m}-{ek}")
        if not t or not p:
            sonuc.append(f"{m}: EKSİK"); continue
        ortak = sorted(set(t["gorev_kalite"]) & set(p["gorev_kalite"]))
        kt, kp = (mean(x["gorev_kalite"][g] for g in ortak) for x in (t, p))
        fark = {k: (sum(p["g"][g][k] for g in ortak) / sum(t["g"][g][k] for g in ortak) - 1) * 100 for k in ("output", "usd")}
        ok = kp >= kt and fark["output"] <= 0 and fark["usd"] <= 0
        sonuc.append(f"{m}: {'KABUL' if ok else 'RET'} kalite {kt:.2f}->{kp:.2f} · çıktı {fark['output']:+.0f}% · $ {fark['usd']:+.0f}% ({ortak})")
    return " | ".join(sonuc)


if __name__ == "__main__":
    ek = None
    if len(sys.argv) > 2:
        TARIH, ek = sys.argv[1], sys.argv[2]
        KALITE = sys.argv[3] if len(sys.argv) > 3 else KALITE
        KOLLAR = ["s-taban", f"s-{ek}", "h-taban", f"h-{ek}"]
    o = {k: ozet(k) for k in KOLLAR}
    for k, v in o.items():
        print(k, "veri yok" if not v else
              f"n={v['n']} kalite={v['kalite']:.2f} out={v['output']:.0f} usd={v['usd']:.3f} tur={v['tur']:.1f} {v['gorev_kalite']}")
    print(karar_d4(o, ek) if ek else karar(o))
