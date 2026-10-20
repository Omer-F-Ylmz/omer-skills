"""ÖĞREN-2 d3: "belirsiz" kalan sinirlar/komut alanlarını kaynaktaki birebir satırdan doldurur (model yok; ÖĞREN-3 komut.KALIP + ÖĞREN-6 duzelt SINIR).
  python -X utf8 .claude/ogren2/duzelt.py    (g1-yazar-*.jsonl yerinde; sonra g1.py birlestir)"""
import json, re, sys
from pathlib import Path

B = Path(__file__).parent
sys.path.insert(0, str(B.parent / "ogren3"))
from komut import KALIP  # noqa: E402

SINIR = re.compile(r"\b(NEVER|MUST NOT|MUST|ALWAYS|DO NOT|Do not)\b|\bASLA\b|[Yy]asak|[Aa]sla |\bCaution\b|\bWarning\b")


def belirsiz(a):
    return a["deger"].startswith("belirsiz")


def duzelt_satir(o, m):
    """o yazar satırı, m kaynak metni; doldurulan alan adlarını döner"""
    d = []
    satirlar = [x.strip() for x in m.splitlines()]
    if belirsiz(o["sinirlar"]):
        s = next((x for x in satirlar if SINIR.search(x) and len(x) >= 20), None)
        if s:
            o["sinirlar"] = {"deger": "Kaynaktaki kural: " + s[:150], "alinti": s[:200]}
            d.append("sinirlar")
    if belirsiz(o["komut"]):
        for k in KALIP:
            s = re.search(k, m, re.M | re.I)
            if s and len(s.group(0).strip()) >= 15:
                o["komut"] = {"deger": s.group(0).strip()[:150], "alinti": s.group(0).strip()[:200]}
                d.append("komut")
                break
    return d


if __name__ == "__main__":
    n = {"sinirlar": 0, "komut": 0}
    for p in sorted(B.glob("g1-yazar-*.jsonl")):
        out = []
        for l in p.read_text(encoding="utf-8").splitlines():
            o = json.loads(l)
            kaynak = B / "kaynak" / (re.sub(r"[^\w.-]", "_", o["ad"]) + ".txt")
            for a in duzelt_satir(o, kaynak.read_text(encoding="utf-8", errors="replace")):
                n[a] += 1
            out.append(json.dumps(o, ensure_ascii=False))
        p.write_bytes(("\n".join(out) + "\n").encode("utf-8"))
    print(n)
