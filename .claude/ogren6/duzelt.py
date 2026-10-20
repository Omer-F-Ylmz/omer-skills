"""ÖĞREN-6 d3: hakem t61a bulgusu (sınırlar/komut 'belirsiz' ama kaynakta var) → yazar satırlarını kaynak satırından BİREBİR doldurur.
  python -X utf8 .claude/ogren6/duzelt.py    (v1-yazar-*.jsonl yerinde; sonra v1.py birlestir)"""
import json, re
from pathlib import Path

B = Path(__file__).parent
SINIR = re.compile(r"\b(NEVER|MUST NOT|MUST|ALWAYS|DO NOT|Do not)\b|\bASLA\b|[Yy]asak|[Aa]sla ")
n = {"s": 0, "k": 0, "kb": 0}
for p in sorted(B.glob("v1-yazar-*.jsonl")):
    out = []
    for l in p.read_text(encoding="utf-8").splitlines():
        o = json.loads(l)
        ad = o["ad"]
        m = (B / "kaynak" / (re.sub(r"[^\w.-]", "_", ad) + ".txt")).read_text(encoding="utf-8", errors="replace").splitlines()
        if o["sinirlar"]["deger"].startswith("belirsiz"):
            s = next((x.strip() for x in m if SINIR.search(x) and len(x.strip()) >= 25), None)
            if s:
                o["sinirlar"] = {"deger": "Kaynaktaki kural: " + s[:150], "alinti": s[:700]}
                n["s"] += 1
        k = o["komut"]
        ana = ad.lower().replace("-", "")
        if k["deger"].startswith("belirsiz"):
            fence, bulunan = False, None
            for x in m:
                if x.lstrip().startswith("```"):
                    fence = not fence
                elif fence and len(x.strip()) >= 15 and ana in x.lower().replace("-", "").replace("_", "").replace(" ", ""):
                    bulunan = x.strip()
                    break
            if bulunan:
                o["komut"] = {"deger": bulunan[:150], "alinti": bulunan[:700]}
                n["k"] += 1
        elif k["deger"] and ana not in k["deger"].lower().replace("-", "").replace("_", "").replace(" ", ""):
            o["komut"] = {"deger": "belirsiz — kaynakta bu aracın kendi komutu yok", "alinti": ""}
            n["kb"] += 1
        out.append(json.dumps(o, ensure_ascii=False))
    p.write_bytes(("\n".join(out) + "\n").encode("utf-8"))
print(n)
