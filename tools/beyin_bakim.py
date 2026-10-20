"""BEYIN-1 arşivci (elle koşu, model yok): kasayı denetler, 90-log'a rapor yazar; not silmez.

Tespit: çift not (aynı gövde, farklı kaynak) · kırık [[bağlantı]] · bayat (kaynak değişti/silindi).
Yan iş: ROUTER-1 yonlendir-kayit.jsonl sayım özeti → 50-dersler/yonlendir-ozet.md.
Kullanım: python tools/beyin_bakim.py [--kasa YOL]
"""
import argparse
import collections
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from beyin_al import KASA, KOK, yaz  # noqa: E402


def govde(metin):
    p = metin.split("\n---\n", 1)
    return p[1] if len(p) == 2 else ""


def denetle(kasa):
    notlar = {p.stem: p for p in kasa.rglob("*.md") if ".obsidian" not in p.parts}
    durum = json.loads((kasa / ".beyin/durum.json").read_text(encoding="utf-8"))
    cift, kirik, bayat = collections.defaultdict(list), [], []
    for ad, p in notlar.items():
        m = p.read_text(encoding="utf-8")
        if "gecersiz: true" in m[:200]:
            continue
        g = govde(m).rsplit("\n\n", 1)[0].strip()  # bağlantı satırı hariç
        if len(g) > 80:
            cift[hashlib.sha256(g.encode()).hexdigest()].append(ad)
        kirik += [(ad, h) for h in re.findall(r"\[\[([^\]|#]+)", m) if h not in notlar]
    for kaynak, d in durum.items():
        k = Path(kaynak)
        if kaynak == "video projeler":
            continue
        if not k.exists():
            bayat.append((kaynak, "silindi"))
        elif hashlib.sha256(k.read_bytes()).hexdigest()[:16] != d["sha"]:
            bayat.append((kaynak, "değişti"))
    return [v for v in cift.values() if len(v) > 1], kirik, bayat


def yonlendir_ozet(kasa):
    yol = KOK / ".kos/kopru/yonlendir-kayit.jsonl"
    if not yol.exists():
        return
    say = collections.Counter()
    for s in yol.read_text(encoding="utf-8").splitlines():
        if s.strip():
            r = json.loads(s)
            say[(r.get("tur"), r.get("kademe"), r.get("sonuc"))] += 1
    satir = ["---", f"kaynak: {yol}", "satir: 1", f"tarih: {datetime.date.today()}", "tur: ders",
             "guven: sayim", "etiket: [router-1, ders]", "---", "# ROUTER-1 yönlendirme sayımı",
             "", "| tür | kademe | sonuç | adet |", "|---|---|---|---|"]
    satir += [f"| {t} | {k} | {s} | {n} |" for (t, k, s), n in sorted(say.items(), key=str)]
    yaz(kasa / "50-dersler/yonlendir-ozet.md", "\n".join(satir + ["", "[[index]]"]) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--kasa", default=str(KASA))
    kasa = Path(ap.parse_args(argv).kasa)
    cift, kirik, bayat = denetle(kasa)
    yonlendir_ozet(kasa)
    rapor = [f"## {datetime.datetime.now():%H:%M} beyin_bakim",
             f"- çift: {len(cift)} küme" + "".join(f"\n  - {', '.join(v[:4])}" for v in cift[:20]),
             f"- kırık bağlantı: {len(kirik)}" + "".join(f"\n  - {a} → {h}" for a, h in kirik[:20]),
             f"- bayat: {len(bayat)} (yeniden al: python tools/beyin_al.py)"
             + "".join(f"\n  - {k} ({n})" for k, n in bayat[:20])]
    with open(kasa / "90-log" / f"{datetime.date.today()}.md", "a", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(rapor) + "\n")
    print(f"beyin_bakim: çift {len(cift)} · kırık {len(kirik)} · bayat {len(bayat)}")


if __name__ == "__main__":
    main()
