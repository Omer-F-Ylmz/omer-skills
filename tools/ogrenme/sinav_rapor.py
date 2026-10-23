"""ÖĞRENME-2e rapor ($0): sınav sonucu + 4 kaynak son 1 saat satır sayısı + 4271a4/K2m önce/sonra tekrar-hata oranı."""
import collections
import json
import re
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent.parent
KOP = KOK / ".kos/kopru"


def olaylar():
    dec, out = json.JSONDecoder(), []
    for s in (KOP / "beyin-olay.jsonl").read_text(encoding="utf-8", errors="replace").splitlines():
        i = 0
        while i < len(s):  # bozuk (yapışık) satırlar: art arda çözülür
            try:
                o, i = dec.raw_decode(s, i)
                if isinstance(o, dict) and isinstance(o.get("t"), (int, float)):  # başka şemalı (t: metin) satırlar atlanır
                    out.append(o)
            except ValueError:
                break
    return out


def main():
    ol = olaylar()
    son = time.time() - 3600
    say = collections.Counter(o.get("kaynak", "?") for o in ol if o.get("t", 0) >= son)
    print("kaynak (son 1 sa, satır):", dict(say))
    sj = json.loads((KOP / "sinav.json").read_text(encoding="utf-8"))
    print("sınav:", json.dumps(sj["ozet"], ensure_ascii=False), "· dosya yaşı dk", round((time.time() - sj["t"]) / 60))
    satirlar = (KOK / ".kos/ogrenme/dersler.jsonl").read_text(encoding="utf-8").splitlines()
    ders = next(r for r in map(json.loads, (s for s in satirlar if s.strip())) if r["id"] == "4271a4")
    t0 = time.mktime(time.strptime(ders["tarih"], "%Y-%m-%d"))
    print("4271a4 tarih", ders["tarih"], "· kullanım", ders["kullanim"], "· yardım", ders["yardim"])
    desen = re.compile(r"run_in_background|arka plan|DETACHED|start /b", re.I)
    ilgili = [o for o in ol if desen.search(o.get("ozet", ""))]
    for ad, sec in (("önce", lambda o: o["t"] < t0), ("sonra", lambda o: o["t"] >= t0)):
        grup = [o for o in ilgili if sec(o)]
        toplam = [o for o in ol if sec(o)]
        h = sum(1 for o in grup if o.get("hata"))
        print(f"{ad}: arka plan olay {len(grup)} · hata {h} · oran {round(h / len(grup), 3) if grup else None} · tüm olay {len(toplam)}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
