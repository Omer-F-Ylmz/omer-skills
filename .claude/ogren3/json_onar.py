"""yazar JSONL'inde tek ters eğik çizgili Windows yolu (C:/Users ters eğikle) → geçerli JSON kaçışı; geçerli satırlara dokunmaz
  python -X utf8 .claude/ogren3/json_onar.py <dosya.jsonl>"""
import json, re, sys
from pathlib import Path

p = Path(sys.argv[1])
o = []
for s in p.read_text(encoding="utf-8").splitlines():
    try:
        json.loads(s)
    except json.JSONDecodeError:
        s = re.sub(r'\\(?![\\"/bfnrtu])', r"\\\\", s)
        json.loads(s)  # hâlâ bozuksa dur
    o.append(s)
p.write_text("\n".join(o) + "\n", encoding="utf-8")
print("ok", len(o))
