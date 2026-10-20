"""ÖĞREN-6 d4: mek-sonuc.jsonl ({"ad","m":[rol],"kanit_satir":N}) → v1-yazar-*.jsonl mekanizma + kanıt (kaynak satırından BİREBİR).
  python -X utf8 .claude/ogren6/mek_uygula.py    (sonra v1.py birlestir)"""
import json, re
from pathlib import Path

B = Path(__file__).parent
ROL = {"birim test", "e2e/tarayıcı", "kalite ölçümü", "LLM değerlendirme", "statik analiz", "sır/bağımlılık taraması", "sızma/DAST",
       "uyumluluk", "derleme/teşhis", "backend/API", "veri/şema", "sorgu/analiz", "rehber", "G4-dışı"}
s = {}
for l in (B / "mek-sonuc.jsonl").read_text(encoding="utf-8").splitlines():
    if l.strip():
        o = json.loads(l)
        assert set(o["m"]) <= ROL and 1 <= len(o["m"]) <= 2, o
        s[o["ad"]] = o
n = 0
for p in sorted(B.glob("v1-yazar-*.jsonl")):
    out = []
    for l in p.read_text(encoding="utf-8").splitlines():
        o = json.loads(l)
        if o["ad"] in s:
            m = (B / "kaynak" / (re.sub(r"[^\w.-]", "_", o["ad"]) + ".txt")).read_text(encoding="utf-8", errors="replace").splitlines()
            k = m[s[o["ad"]]["kanit_satir"] - 1].strip()
            assert len(k) >= 15, (o["ad"], k)
            o["mekanizma"], o["kanit"] = s[o["ad"]]["m"], k[:700]
            n += 1
        out.append(json.dumps(o, ensure_ascii=False))
    p.write_bytes(("\n".join(out) + "\n").encode("utf-8"))
print(f"{n}/{len(s)} kalem güncellendi")
