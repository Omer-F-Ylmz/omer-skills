"""Kaynakların ROVER referansına (ve eski altına) karşı WER'i; groq + ekran adı düzeltici etkisi.

Kullanım: python tools/rover_olc.py   (rover_ref.py önce koşmuş olmalı; çıktı: .kos/kopru/wer-altin/rover/olcum.json)
Not: ROVER referansı groq+gemini+yerel oyundan çıkar → bu üçü lehine yanlı; 'altın' oyu ise mistral ile kurulmuştu.
"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
import ekran_duzelt  # noqa: E402
import rover_ref as rr  # noqa: E402
import wer_altin as wa  # noqa: E402
from wer_altin_olc import wer  # noqa: E402

DERIN = KOK / "docs/video-tarama/derin"


def main():
    yerel = json.loads((wa.ALTIN / "seg-large-v3.json").read_text(encoding="utf-8"))["segler"]
    toplam = {}
    for kod in sorted(p.name.split(".")[0] for p in wa.ALTIN.glob("*.altin.txt")):
        t = rr.kaynaklar(kod, yerel)
        rov = (rr.ROVER / f"{kod}.txt").read_text(encoding="utf-8").split()
        altin = (wa.ALTIN / f"{kod}.altin.txt").read_text(encoding="utf-8").split()
        d = DERIN / f"{kod}.json"
        ekran = "\n".join(e["t"] for e in json.loads(d.read_text(encoding="utf-8")).get("ekran", [])) if d.exists() else ""
        duz, ops = ekran_duzelt.duzelt(" ".join(t["groq"]), ekran)
        hip = {"groq": t["groq"], "gemini": t["gemini"], "yerel": t["yerel"], "rover": rov, "groq+duzelt": wa.norm(duz).split()}
        for ad, h in hip.items():
            for rn, ref in (("rover", rov), ("altin", altin)):
                s = toplam.setdefault(f"{ad}|{rn}", [0.0, 0])
                s[0] += wer(" ".join(ref), " ".join(h)) * len(ref)
                s[1] += len(ref)
        toplam.setdefault("duzeltme_sayisi", [0, 0])[0] += len(ops)
    sonuc = {k: round(v[0] / v[1], 4) for k, v in toplam.items() if "|" in k}
    sonuc["duzeltme_sayisi"] = toplam["duzeltme_sayisi"][0]
    (rr.ROVER / "olcum.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in sonuc.items():
        print(k, v)


if __name__ == "__main__":
    main()
