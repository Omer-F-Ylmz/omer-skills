"""Ölçü (b): ekranda geçen araç/komut adlarının dökümde doğru geçme oranı, düzeltme önce/sonra (derin JSON'ları üzerinde).

Ad "konuşuldu" sayılır: dökümde ad'a ≥0.75 benzeyen, yaygın kelime olmayan jeton var. "Doğru": katlanmış kelime ad ile eşit ya da ad + Türkçe ek (claudein).
Kullanım: python tools/ekran_adlari_olc.py [--n 0] [--ornek 25]   (n=0 hepsi; çıktı: .kos/kopru/rapor/ekran-adlari.json)
"""
import argparse
import difflib
import json
import random
import re
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
import ekran_duzelt as ed  # noqa: E402
from ekran_yazi import kat  # noqa: E402

DERIN = KOK / "docs/video-tarama/derin"


def sayim(metin, adlar):
    """{ad: durum} durum: dogru | yanlis (konuşuldu, farklı yazıldı); konuşulmayanlar yok."""
    yg = ed.yaygin()
    ham = re.findall(r"\w+", metin)
    tek = {kat(t) for t in ham} - {""}
    toks = tek | {kat(a + b) for a, b in zip(ham, ham[1:])}  # bitişik çift yalnız "doğru" için (agent reach = agentreach); yakın-yanlış testinde sahte eşleşme üretir
    out = {}
    for k in adlar:
        if any(t == k or (t.startswith(k) and len(t) - len(k) <= 4) for t in toks):
            out[k] = "dogru"
        elif any(difflib.SequenceMatcher(None, k, t).ratio() >= 0.75 for t in tek if abs(len(t) - len(k)) <= 3 and t not in yg):
            out[k] = "yanlis"
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--ornek", type=int, default=25)
    a = ap.parse_args()
    dosyalar = sorted(DERIN.glob("*.json"))
    if a.n:
        dosyalar = dosyalar[: a.n]
    onc = {"dogru": 0, "yanlis": 0}
    son = {"dogru": 0, "yanlis": 0}
    ornek, videolu = [], 0
    for p in dosyalar:
        j = json.loads(p.read_text(encoding="utf-8"))
        seg = j.get("transkript") or []
        if not seg:
            continue
        metin = " ".join(s["t"] for s in seg)
        ekran = "\n".join(e["t"] for e in j.get("ekran", []))
        cand = ed.adaylar(ekran)
        if not cand:
            continue
        yeni, ops = ed.duzelt(metin, ekran)
        s0, s1 = sayim(metin, cand), sayim(yeni, cand)
        if not s0:
            continue
        videolu += 1
        for k, v in s0.items():
            onc[v] += 1
        for k, v in s1.items():
            son[v] += 1
        ornek += [(p.stem, e, y) for e, y in ops]
    toplam = lambda d: d["dogru"] + d["yanlis"]
    ozet = {"video": len(dosyalar), "adli_video": videolu, "konusulan_ad": toplam(onc),
            "yakalama_once": round(onc["dogru"] / max(toplam(onc), 1), 4), "yakalama_sonra": round(son["dogru"] / max(toplam(son), 1), 4),
            "degisim": len(ornek)}
    random.seed(1)
    ozet["ornek"] = [f"{v}: {e} > {y}" for v, e, y in random.sample(ornek, min(a.ornek, len(ornek)))]
    out = KOK / ".kos/kopru/rapor/ekran-adlari.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in ozet.items() if k != "ornek"}, ensure_ascii=False))
    for o in ozet["ornek"]:
        print(o)


if __name__ == "__main__":
    main()
