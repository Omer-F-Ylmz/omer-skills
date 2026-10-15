"""ÖĞREN-1 d6 son çıktı: v3c (:free) + Claude yükseltmeleri → ozet-token-son.jsonl; kör hakem örneklemleri (model bilgisi yok).
  python -X utf8 .claude/ogren1/son.py is      → Claude'a gidecek kalemler (düşen: tüm alanlar · çekişmeli: yalnız mekanizma)
  python -X utf8 .claude/ogren1/son.py birlestir → son.jsonl + hakem-ayni.jsonl / hakem-yeni.jsonl + Claude alan oranı"""
import json, sys
from pathlib import Path

import ozet_kaynak

O = Path(r"C:\Projeler\omer-skills\.kos\kopru\ogren")
V3C, CLAUDE, SON = O / "ozet-token-v3c.jsonl", O / "ozet-token-v3c-claude.jsonl", O / "ozet-token-son.jsonl"
AYNI = ["rtk-desktop", "rtk", "headroom", "qmd", "jev", "mem-search", "graphify", "smart-explore", "strategic-compact",
        "context-mode", "cagri_sayac"]  # d3 hakeminin 10'u (+rtk-desktop, d5)
ALAN = ["ne_yapar", "komut", "sinirlar", "mekanizma"]


def oku(p):
    return {r["ad"]: r for r in map(json.loads, p.read_text(encoding="utf-8").splitlines())} if p.exists() else {}


def is_listesi(v):
    return {ad: ("tum" if ad not in v else "mekanizma") for ad in ozet_kaynak.D if ad not in v or v[ad]["cekismeli"]}


if __name__ == "__main__":
    v = oku(V3C)
    isler = is_listesi(v)
    if sys.argv[1:] == ["is"]:
        for ad, ne in isler.items():
            print(ad, ne, ozet_kaynak.D[ad], sep="\t")
        sys.exit()
    c = oku(CLAUDE)
    eksik = [ad for ad in isler if ad not in c]
    assert not eksik, f"Claude satırı eksik: {eksik}"
    son = {}
    for ad in ozet_kaynak.D:
        r = dict(v.get(ad, {}), ad=ad, kaynak=ozet_kaynak.D[ad])
        if ad in isler:
            r.update({k: c[ad][k] for k in (ALAN + ["girdi_cikti", "ne_zaman", "cakistigi_arac"] if isler[ad] == "tum" else ["mekanizma"])
                      if k in c[ad]}, claude=isler[ad], cekismeli=False)
        son[ad] = r
    SON.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in son.values()), encoding="utf-8")
    for ad_dosya, adlar in (("hakem-ayni.jsonl", AYNI), ("hakem-yeni.jsonl", [a for a in son if a not in AYNI])):
        (O / ad_dosya).write_text("".join(json.dumps({k: son[a][k] for k in ["ad", "kaynak"] + ALAN}, ensure_ascii=False) + "\n"
                                          for a in adlar), encoding="utf-8")
    cf = sum(4 if ne == "tum" else 1 for ne in isler.values())
    print(f"son {len(son)} kalem · Claude alan {cf}/{len(son) * 4} = %{100 * cf / len(son) / 4:.1f} · "
          f"düşen {sum(ne == 'tum' for ne in isler.values())} · çekişmeli {sum(ne == 'mekanizma' for ne in isler.values())}")
