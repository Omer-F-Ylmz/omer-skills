"""Leave-one-out WER, hakemli: X kaynağı, diğer iki kaynağın ayrıştığı yerlerde ücretsiz LLM hakemin seçtiği referansa karşı ölçülür.

Hakem metin-bağlamıyla seçer, ses duymaz; adaylar yalnız diğer iki kaynaktan gelir (X'in kendi yazımı referansı etkilemez).
Kullanım: python tools/wer_hakem.py   (hakem kararları .kos/kopru/wer-altin/hakem-<a>-<b>.json'da önbelleklenir; sonuç loo-hakem.json)
"""
import difflib
import itertools
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wer_altin as wa  # noqa: E402
import wer_loo as wl  # noqa: E402
import ucretsiz_havuz as uh  # noqa: E402

PARTI = 40
ISTEM = ("Türkçe konuşma dökümünde iki ASR sisteminin ayrıştığı yerler var (konu: yapay zeka/yazılım araçları, Claude, skill, agent). "
         "Her madde için bağlama göre konuşmacının GERÇEKTE söylediği doğru yazımı seç: A, B ya da ikisi de eşit/bilinmiyorsa ?. "
         "Eksik harfli/kesik kelime, yanlış ad (ör. 'cloud' yerine Claude) yanlıştır. Yalnız JSON ver: {\"1\":\"A\",\"2\":\"B\",...}\n\n")


def ayrisimlar(a, b):
    return [(i1, i2, j1, j2) for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if op != "equal"]


def hakemle(maddeler):
    """maddeler: [(baglam, A, B)] → ['A'|'B'|'?'] ; havuz başarısızsa '?'."""
    sonuc = []
    for i in range(0, len(maddeler), PARTI):
        parca = maddeler[i:i + PARTI]
        istem = ISTEM + "\n".join(f"{n}. ...{ctx}... | A: {a or '(yok)'} | B: {b or '(yok)'}" for n, (ctx, a, b) in enumerate(parca, 1))
        metin, kaynak, _ = uh.cagir("hakem", istem, max_tokens=1500, etiket="wer-hakem")
        m = re.search(r"\{.*\}", metin or "", re.S)
        try:
            kar = json.loads(m.group()) if m else {}
        except ValueError:
            kar = {}
        sonuc += [kar.get(str(n), "?") if kar.get(str(n), "?") in ("A", "B") else "?" for n in range(1, len(parca) + 1)]
        print("hakem", i + len(parca), "/", len(maddeler), kaynak, flush=True)
    return sonuc


def cift_ref(kodlar, metin, p, q):
    """(p,q) için klip başına referans öğeleri: kelime ya da None (hakem '?' dediği joker blok). Önbellekli."""
    yol = wa.ALTIN / f"hakem-{p}-{q}.json"
    onb = json.loads(yol.read_text(encoding="utf-8")) if yol.exists() else {}
    yeni = []
    for kod in kodlar:
        a, b = metin[kod][p], metin[kod][q]
        for k, (i1, i2, j1, j2) in enumerate(ayrisimlar(a, b)):
            if f"{kod}:{k}" not in onb:
                yeni.append((f"{kod}:{k}", (" ".join(a[max(0, i1 - 7):i1]) + " ... " + " ".join(a[i2:i2 + 4]), " ".join(a[i1:i2]), " ".join(b[j1:j2]))))
    if yeni:
        # A/B yer yanlılığını kırmak için tek indekslerde sıra çevrilir
        cev = [(n % 2 == 1) for n in range(len(yeni))]
        mad = [(c, y, x) if f else (c, x, y) for (_, (c, x, y)), f in zip(yeni, cev)]
        for (anahtar, _), f, s in zip(yeni, cev, hakemle(mad)):
            onb[anahtar] = {"A": "q" if f else "p", "B": "p" if f else "q", "?": "?"}[s]
        yol.write_text(json.dumps(onb), encoding="utf-8")
    ref = {}
    for kod in kodlar:
        a, b, og, onceki = metin[kod][p], metin[kod][q], [], 0
        for k, (i1, i2, j1, j2) in enumerate(ayrisimlar(a, b)):
            og += a[onceki:i1]
            ka = onb[f"{kod}:{k}"]
            og += a[i1:i2] if ka == "p" else b[j1:j2] if ka == "q" else [None]
            onceki = i2
        ref[kod] = og + a[onceki:]
    return ref


def main():
    kodlar = sorted(p.name.split(".")[0] for p in wa.ALTIN.glob("*.altin.txt"))
    yerel = json.loads((wa.ALTIN / "seg-large-v3.json").read_text(encoding="utf-8"))["segler"]
    metin = {kod: {**{k: wa.norm((wa.ALTIN / f"{kod}.{k}.txt").read_text(encoding="utf-8")).split() for k in ("groq", "gemini", "mistral")},
                   "yerel": wa.norm(" ".join(sg[2] for sg in yerel[kod])).split()} for kod in kodlar}
    refler = {}
    for p, q in itertools.combinations(wl.HAVUZ, 2):
        refler[(p, q)] = cift_ref(kodlar, metin, p, q)
    sonuc = {}
    for x in wl.KAYNAKLAR:
        cift = tuple(d for d in wl.HAVUZ if d != x) if x in wl.HAVUZ else ("groq", "gemini")
        h = n = 0
        for kod in kodlar:
            og = refler[cift][kod]
            h += wl.hata(og, metin[kod][x])
            n += sum(o is not None for o in og)
        sonuc[x] = {"wer": round(h / n, 4), "hata": h, "ref_kelime": n, "referans": "+".join(cift)}
    (wa.ALTIN / "loo-hakem.json").write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(sonuc, ensure_ascii=False))


if __name__ == "__main__":
    sys.exit(main())
