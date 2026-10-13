"""ENVANTER-4 m4: iş → ilgili birleşim tarifi + katalog kayıtlarının derin alanları (kompakt).

Kullanım: python tools/kilavuz_ara.py "<iş>" [--n 12]
Sıralama katalog_ara.ara() (dokunulmadan içe alınır); derin alan tekil.tsv temsilcisi üstünden kopyalara da geçer.
"""
import csv
import json
import sys
from pathlib import Path

import katalog_ara

KOK = Path(__file__).resolve().parents[1]
KAT = KOK / "docs" / "katalog"


def tarif_bul(q, kok=KAT / "tarifler"):
    """En çok ortak kelimeli tarif (ad + ilk satır); ortak kelime yoksa None."""
    qk = set(katalog_ara.kelimeler(q))
    en = max(((len(qk & set(katalog_ara.kelimeler(p.stem.replace("-", " ") + " " + p.read_text(encoding="utf8").split("\n", 1)[0]))), p)
              for p in sorted(kok.glob("*.md"))), default=(0, None), key=lambda x: x[0])
    return en[1] if en[0] else None


def derin_tablo():
    tem = {r["ad"]: r["temsilci"] for r in csv.DictReader(open(KAT / "tekil.tsv", encoding="utf8"), delimiter="\t")}
    yol = KAT / "derin.jsonl"
    d = {j["ad"]: j for j in map(json.loads, open(yol, encoding="utf8"))} if yol.exists() else {}
    return lambda ad: d.get(tem.get(ad, ad))


def main():
    a = sys.argv[1:]
    n = int(a[a.index("--n") + 1]) if "--n" in a else 12
    q = " ".join(x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] != "--n"))
    t = tarif_bul(q)
    if t:
        print(f"# tarif: {t.relative_to(KOK).as_posix()}\n{t.read_text(encoding='utf8').strip()}\n")
    derin = derin_tablo()
    sonuc = katalog_ara.ara(q)
    print(f"# kayıt {len(sonuc)} (ilk {min(n, len(sonuc))}, derin dolu olanlar önce)")
    for o in sorted(sonuc, key=lambda o: derin(o["ad"]) is None)[:n]:
        j = derin(o["ad"])
        print(f"- {o['ad']} [{o['tur']}] · {o['cagri'][:60]}")
        if j:
            print(f"  nasıl: {j['nasil']} · ne zaman: {j['neden']} · en iyi: {j['en_iyi']} · birlikte: {j['birlikte']} · tuzak: {j['tuzak']} · maliyet: {j['maliyet']}")
        else:
            print(f"  {(o['is'] or o['metin'])[:140]} (derin yok)")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
