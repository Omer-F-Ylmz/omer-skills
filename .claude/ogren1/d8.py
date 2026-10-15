"""ÖĞREN-1 d8: d7 görülmemiş 28 kalem → Claude yükseltmesi (düşen: tüm alanlar · çekişmeli: mekanizma) + iki kör hakem kapısı.
  python -X utf8 .claude/ogren1/d8.py is        → Claude'a gidecek kalemler (ad · ne · kaynak)
  python -X utf8 .claude/ogren1/d8.py birlestir → Claude satırları gecerli_a/gecerli_b'den geçer → d7-son.jsonl + hakem-d7.jsonl (model bilgisi yok)
  python -X utf8 .claude/ogren1/d8.py puan h1.jsonl h2.jsonl → iki hakemin alan kararları: hata sayısı + ayrışan alanlar"""
import json, sys
from pathlib import Path

import ozet_kaynak
from ozet3 import adlari, gecerli_a, gecerli_b
from son import ALAN, oku

O = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren")
D7, CLAUDE, SON, HAKEM = O / "ozet-token-d7.jsonl", O / "ozet-token-d7-claude.jsonl", O / "ozet-token-d7-son.jsonl", O / "hakem-d7.jsonl"
D = dict(s.split("\t")[::3] for s in (Path(__file__).parent / "d7-ornek.tsv").read_text(encoding="utf-8").splitlines())


def is_listesi(v):
    return {ad: ("tum" if ad not in v else "mekanizma") for ad in D if ad not in v or v[ad]["cekismeli"]}


def denetle(ad, ne, c):
    """d7 (4): Claude yükseltmesi de mekanik denetimden geçer — :free kollarla aynı kurallar"""
    m = ozet_kaynak.metin(D[ad])
    neden = gecerli_a(c, m, adlari(ad, D[ad])) if ne == "tum" else None
    return neden or (None if gecerli_b(c, m) else "mekanizma/kanıt geçersiz")


def karar(p):
    """hakem satırı: {"ad", "ne_yapar": "D"|"Y", ... } → {(ad, alan): D/Y}"""
    return {(r["ad"], a): r[a] for r in oku(Path(p)).values() for a in ALAN}


if __name__ == "__main__":
    v = oku(D7)
    isler = is_listesi(v)
    if sys.argv[1:] == ["is"]:
        for ad, ne in isler.items():
            print(ad, ne, D[ad], sep="\t")
    elif sys.argv[1:] == ["birlestir"]:
        c = oku(CLAUDE)
        hatalar = {ad: "satır yok" if ad not in c else denetle(ad, ne, c[ad]) for ad, ne in isler.items()}
        hatalar = {ad: h for ad, h in hatalar.items() if h}
        assert not hatalar, f"Claude satırı RET: {hatalar}"
        son = {}
        for ad in D:
            r = dict(v.get(ad, {}), ad=ad, kaynak=D[ad])
            if ad in isler:
                r.update({k: c[ad][k] for k in (ALAN + ["girdi_cikti", "ne_zaman", "cakistigi_arac", "alinti", "kanit"]
                                                if isler[ad] == "tum" else ["mekanizma", "kanit"]) if k in c[ad]}, claude=isler[ad], cekismeli=False)
            son[ad] = r
        SON.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
        HAKEM.write_text("".join(json.dumps({k: r[k] for k in ["ad", "kaynak"] + ALAN}, ensure_ascii=False) + "\n" for r in son.values()),
                         encoding="utf-8")
        cf = sum(4 if ne == "tum" else 1 for ne in isler.values())
        print(f"son {len(son)} kalem · Claude alan {cf}/{len(son) * 4} = %{100 * cf / len(son) / 4:.1f}")
    elif sys.argv[1:2] == ["puan"]:
        h1, h2 = karar(sys.argv[2]), karar(sys.argv[3])
        assert h1.keys() == h2.keys() and len(h1) == len(D) * 4, f"alan sayısı: {len(h1)} / {len(h2)} (beklenen {len(D) * 4})"
        ayri = sorted(k for k in h1 if h1[k] != h2[k])
        print(f"alan {len(h1)} · hakem1 Y {sum(x == 'Y' for x in h1.values())} · hakem2 Y {sum(x == 'Y' for x in h2.values())} · ayrışan {len(ayri)}")
        for ad, a in ayri:
            print("AYRI", ad, a, h1[ad, a], h2[ad, a], sep="\t")
