"""Leave-one-out WER: her kaynak (groq/gemini/mistral), kendisi dışındaki ikisinin uzlaştığı kelimelere karşı ölçülür.

Diğer ikisinin ayrıştığı bloklar joker sayılır (X orada ne yazarsa yazsın ceza yok, referans kelime sayılmaz) → yanlılık yok.
Kullanım: python tools/wer_loo.py   (çıktı: .kos/kopru/wer-altin/loo.json)
"""
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wer_altin as wa  # noqa: E402

KAYNAKLAR = ("groq", "gemini", "mistral", "yerel")
HAVUZ = ("groq", "gemini", "yerel")  # referans kurabilen kaynaklar; Voxtral Türkçeyi desteklemiyor (API 400), yalnız ölçülür


def uzlasi(a, b):
    """İki dökümün hizalı karşılaştırması → referans öğeleri: kelime (uzlaşılan) ya da None (joker blok)."""
    ogeler = []
    for op, i1, i2, _, _ in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if op == "equal":
            ogeler += a[i1:i2]
        else:
            ogeler.append(None)
    return ogeler


def hata(ogeler, x):
    """Jokerli düzeltme mesafesi: joker, x'ten herhangi bir parçayı bedavaya yutar."""
    d = list(range(len(x) + 1))
    for o in ogeler:
        yeni = [d[0] + (o is not None)]
        for j, xw in enumerate(x, 1):
            if o is None:
                yeni.append(min(d[j], yeni[j - 1]))
            else:
                yeni.append(min(d[j] + 1, yeni[j - 1] + 1, d[j - 1] + (o != xw)))
        d = yeni
    return d[-1]


def olc(kodlar, metin):
    """metin[kod][kaynak] → kelime listesi; döner: {kaynak: (hata, ref_kelime)}"""
    sonuc = {k: [0, 0] for k in KAYNAKLAR}
    for kod in kodlar:
        for k in KAYNAKLAR:
            a, b = [metin[kod][d] for d in (HAVUZ if k not in HAVUZ else [d for d in HAVUZ if d != k])[:2]]
            og = uzlasi(a, b)
            sonuc[k][0] += hata(og, metin[kod][k])
            sonuc[k][1] += sum(o is not None for o in og)
    return sonuc


def main():
    kodlar = sorted(p.name.split(".")[0] for p in wa.ALTIN.glob("*.altin.txt"))
    yerel = json.loads((wa.ALTIN / "seg-large-v3.json").read_text(encoding="utf-8"))["segler"]  # faster-whisper large-v3 (yerel)
    metin = {kod: {**{k: wa.norm((wa.ALTIN / f"{kod}.{k}.txt").read_text(encoding="utf-8")).split() for k in KAYNAKLAR[:3]},
                   "yerel": wa.norm(" ".join(sg[2] for sg in yerel[kod])).split()} for kod in kodlar}
    s = olc(kodlar, metin)
    ozet = {k: {"loo_wer": round(h / n, 4), "hata": h, "ref_kelime": n} for k, (h, n) in s.items()}
    ozet["klip"] = len(kodlar)
    (wa.ALTIN / "loo.json").write_text(json.dumps(ozet, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(ozet, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
