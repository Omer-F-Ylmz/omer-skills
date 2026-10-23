"""Ekran-altyazı referanslı WER: gömülü altyazı olaylarını (ekran_yazi.py) insan referansı sayıp her ASR kaynağını ölçer.

Olay kabulü kaynaktan bağımsız: olay, altın metinde (3 ASR'nin oyu) en iyi pencereyle ≥0.5 (<4 kelimede ≥0.6) örtüşüyorsa altyazıdır (arayüz yazısı değil).
Kabul edilen her olay için her kaynakta en az hatalı pencere seçilir; WER = toplam hata / toplam olay kelimesi. Katlama: aksan/noktalama yok sayılır.
Yapışık OCR jetonu (claudecode) hyp penceresindeki 2-3 ardışık kelimeye açılır.
Kullanım: python tools/ekran_wer.py [--min-olay 6]   (çıktı: .kos/kopru/rapor/ekran-wer.json)
"""
import argparse
import difflib
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
import ekran_duzelt as ed  # noqa: E402
import wer_altin as wa  # noqa: E402
from ekran_yazi import kat  # noqa: E402

EKRAN = KOK / ".kos/kopru/ekran-tmp"


def kelimeler(m):
    return [w for w in (kat(x) for x in m.split()) if w]


def mesafe(r, h):
    d = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        yeni = [i]
        for j, hw in enumerate(h, 1):
            yeni.append(min(d[j] + 1, yeni[j - 1] + 1, d[j - 1] + (rw != hw)))
        d = yeni
    return d[-1]


def ac(ref, pencere):
    """Yapışık ref jetonunu penceredeki 2-3 ardışık kelimenin birleşimiyse açar."""
    cikti = []
    for w in ref:
        if w not in pencere:
            for n in (2, 3):
                if any("".join(pencere[i:i + n]) == w for i in range(len(pencere) - n + 1)):
                    cikti += next(pencere[i:i + n] for i in range(len(pencere) - n + 1) if "".join(pencere[i:i + n]) == w)
                    break
            else:
                cikti.append(w)
        else:
            cikti.append(w)
    return cikti


def en_iyi(ref, hyp):
    """(hata, ref_uzunluk) en iyi hyp penceresi için; pencere uzunluğu ref ± 2."""
    n = len(ref)
    en = None
    for L in range(max(1, n - 2), n + 3):
        for i in range(0, max(1, len(hyp) - L + 1)):
            pen = hyp[i:i + L]
            r = ac(ref, pen)
            e = mesafe(r, pen)
            if en is None or e < en[0]:
                en = (e, len(r))
    return en or (n, n)


def ortusme(ref, hyp):
    n = len(ref)
    en = 0.0
    for L in range(max(1, n - 1), n + 2):
        for i in range(0, max(1, len(hyp) - L + 1)):
            en = max(en, difflib.SequenceMatcher(None, ref, hyp[i:i + L], autojunk=False).ratio())
    return en


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-olay", type=int, default=6)
    a = ap.parse_args()
    toplam, klip = {}, {}
    for p in sorted(EKRAN.glob("*.json")):
        kod = p.stem
        altin_yol = wa.ALTIN / f"{kod}.altin.txt"
        if not altin_yol.exists():
            continue
        veri = json.loads(p.read_text(encoding="utf-8"))
        altin = kelimeler(altin_yol.read_text(encoding="utf-8"))
        yerel_m = " ".join(sg[2] for sg in json.loads((wa.ALTIN / "seg-large-v3.json").read_text(encoding="utf-8"))["segler"][kod])
        ekran_m = "\n".join(s for _, s in veri["olaylar"])
        duz, ops = ed.duzelt(yerel_m, ekran_m)
        kaynak = {"altin": altin, "yerel": kelimeler(yerel_m), "yerel+ekran": kelimeler(duz),
                  **{k: kelimeler((wa.ALTIN / f"{kod}.{k}.txt").read_text(encoding="utf-8")) for k in ("groq", "gemini")}}
        olay = [kelimeler(s) for _, s in veri["olaylar"]]
        olay = [o for o in olay if len(o) >= 2 and ortusme(o, altin) >= (0.6 if len(o) < 4 else 0.5)]
        if len(olay) < a.min_olay:
            print(f"{kod}: altyazı yok/az ({len(olay)} olay)", flush=True)
            continue
        satir = {"olay": len(olay), "kelime": sum(map(len, olay)), "duzeltme": len(ops)}
        for ad, h in kaynak.items():
            e = n = 0
            for o in olay:
                he, hn = en_iyi(o, h)
                e, n = e + he, n + hn
            satir[ad] = round(e / n, 4)
            t = toplam.setdefault(ad, [0, 0])
            t[0] += e
            t[1] += n
        klip[kod] = satir
        print(kod, json.dumps(satir, ensure_ascii=False), flush=True)
    ozet = {"klip": len(klip), "wer": {ad: round(e / n, 4) for ad, (e, n) in toplam.items()}, "klipler": klip}
    (KOK / ".kos/kopru/rapor/ekran-wer.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: ozet[k] for k in ("klip", "wer")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
