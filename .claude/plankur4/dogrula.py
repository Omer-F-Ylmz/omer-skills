"""Jeton çapraz doğrulama: json usage ↔ transkript; paket 0'da üç kolun araç çağrıları."""
import json, re
from pathlib import Path

D = Path(__file__).parent
PROJ = Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(D / "cwd"))
K = ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens", "output_tokens")
for r in map(json.loads, (D / "sonuc.jsonl").read_text(encoding="utf8").splitlines()):
    u = r.get("usage") or {}
    js = sum(u.get(k, 0) for k in K)
    f = PROJ / f"{r['sid']}.jsonl"
    araclar, mid = [], set()
    if f.exists():
        for s in map(json.loads, filter(str.strip, f.read_text(encoding="utf8").splitlines())):
            m = s.get("message") or {}
            if s.get("type") == "assistant":
                mid.add(m.get("id"))
                for c in m.get("content") or []:
                    if isinstance(c, dict) and c.get("type") == "tool_use":
                        araclar.append(f"{c['name']}:{json.dumps(c.get('input'), ensure_ascii=False)[:110]}")
    print(f"{r['kol']}{r['paket']} tur {r['tur']} json {js} transkript {r['jeton']} fark {(r['jeton'] or 0) - js:+} "
          f"cache_okuma {r['cache_okuma']} cikti {u.get('output_tokens')} mesaj {len(mid)} arac {len(araclar)} metin {len(r['metin'])}kr")
    if r["paket"] in (0, 1):
        print("  " + "\n  ".join(araclar))
