"""kapı puanı: hakem-g1-<tohum>-<n>.jsonl → hakem başına D oranı + Y listesi (python -X utf8 hakem_puan.py t11 t12)"""
import json, sys
from pathlib import Path

for t in sys.argv[1:]:
    for p in sorted(Path(__file__).parent.glob(f"hakem-g1-{t}-*.jsonl")):
        s = [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
        y = [(r["ad"], a) for r in s for a in ("ne_yapar", "komut", "sinirlar", "mekanizma") if r[a] != "D"]
        n = len(s) * 4
        print(f"{p.name}: kart {len(s)} · alan {n} · Y {len(y)} · %{100 * (n - len(y)) / n:.1f}", y)
