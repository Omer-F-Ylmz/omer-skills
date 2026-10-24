"""ROVER/çoğunluk referansı: groq (pivot) + gemini + yerel large-v3 kelime hizalı oylama.

Kullanım: python tools/rover_ref.py   (çıktı: .kos/kopru/wer-altin/rover/<id>.txt + rover/ozet.json)
İki kaynağın uzlaştığı bölge kazanır; üçü de ayrışırsa 'belirsiz' (WER'den ayrı sayılır, Gemini metni konur).
"""
import difflib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wer_altin as wa  # noqa: E402

ROVER = wa.ALTIN / "rover"


def kaynaklar(kod, yerel):
    t = {k: wa.norm((wa.ALTIN / f"{kod}.{k}.txt").read_text(encoding="utf-8")).split() for k in ("groq", "gemini")}
    t["yerel"] = wa.norm(" ".join(sg[2] for sg in yerel[kod])).split()
    return t


def bloklar(piv, x):
    return difflib.SequenceMatcher(None, piv, x, autojunk=False).get_opcodes()


def sinir(ops, p, son):
    """Pivot sınırı p → x indeksi; eşit blokta kesin, ekleme/değişme kenarında başlangıç en küçük, bitiş en büyük."""
    aday = []
    for op, i1, i2, j1, j2 in ops:
        if op == "equal" and i1 <= p <= i2:
            aday.append(j1 + p - i1)
        elif op != "equal" and p == i1:
            aday.append(j1)
        elif op != "equal" and p == i2:
            aday.append(j2)
    return max(aday) if son else min(aday)


def kume(piv, ops_list):
    ara = sorted((i1, i2) for ops in ops_list for op, i1, i2, _, _ in ops if op != "equal")
    out = []
    for a, b in ara:
        if out and a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return out


def rover(kod, t):
    piv = t["groq"]
    ops = {k: bloklar(piv, t[k]) for k in ("gemini", "yerel")}
    cikti, belirsiz, i = [], [], 0
    for a, b in kume(piv, list(ops.values())):
        cikti += piv[i:a]
        aday = {"groq": piv[a:b]} | {k: t[k][sinir(ops[k], a, False):sinir(ops[k], b, True)] for k in ops}
        # boşluk farkı (bitişik/ayrı yazım) aynı sayılır
        say = {}
        for k, c in aday.items():
            say.setdefault("".join(c), []).append(k)
        kazan = [k for k in say.values() if len(k) >= 2]
        if kazan:
            cikti += aday[kazan[0][0]]
        else:
            belirsiz.append({"id": kod, "span": [a, b], "baglam": " ".join(piv[max(0, a - 5):b + 5]),
                             **{k: " ".join(c) for k, c in aday.items()}})
            cikti += aday["gemini"]
        i = b
    return cikti + piv[i:], belirsiz


def main():
    ROVER.mkdir(parents=True, exist_ok=True)
    yerel = json.loads((wa.ALTIN / "seg-large-v3.json").read_text(encoding="utf-8"))["segler"]
    ozet, tum = {}, []
    for kod in sorted(p.name.split(".")[0] for p in wa.ALTIN.glob("*.altin.txt")):
        t = kaynaklar(kod, yerel)
        metin, bel = rover(kod, t)
        (ROVER / f"{kod}.txt").write_text(" ".join(metin), encoding="utf-8")
        ozet[kod] = {"kelime": len(metin), "belirsiz_blok": len(bel), "belirsiz_kelime": sum(max(len(b[k].split()) for k in ("groq", "gemini", "yerel")) for b in bel)}
        tum += bel
    k = sum(o["kelime"] for o in ozet.values())
    bk = sum(o["belirsiz_kelime"] for o in ozet.values())
    (ROVER / "ozet.json").write_text(json.dumps({"kelime": k, "belirsiz_kelime": bk, "oran": bk / k, "klip": ozet}, ensure_ascii=False, indent=1), encoding="utf-8")
    (ROVER / "belirsiz.json").write_text(json.dumps(tum, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"kelime {k} belirsiz_kelime {bk} oran {bk / k:.2%} blok {len(tum)}")


if __name__ == "__main__":
    main()
