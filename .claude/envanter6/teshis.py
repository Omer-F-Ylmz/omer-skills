"""ENVANTER-6 m1: ENVANTER-2 kapı transkriptlerinden tur teşhisi (araç çağrıları + tur başı jeton)."""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path.home() / ".claude/projects/C--Projeler-omer-skills-wt-envanter2--claude-envanter2-kapi-cwd"
for f in sorted(P.glob("*.jsonl"), key=lambda x: x.stat().st_mtime):
    satir = [json.loads(l) for l in f.read_text(encoding="utf8").splitlines() if l.strip()]
    ilk = next((s for s in satir if s.get("type") == "user"), {})
    icerik = ilk.get("message", {}).get("content", "")
    icerik = icerik if isinstance(icerik, str) else json.dumps(icerik, ensure_ascii=False)
    kol = "B?" if "yetenek-getir" in json.dumps(satir[:3], ensure_ascii=False) else ""
    araclar, uso = [], []
    for s in satir:
        m = s.get("message", {})
        if s.get("type") == "assistant":
            u = m.get("usage", {})
            uso.append((u.get("input_tokens", 0), u.get("cache_creation_input_tokens", 0), u.get("cache_read_input_tokens", 0), u.get("output_tokens", 0)))
            for c in m.get("content", []) or []:
                if isinstance(c, dict) and c.get("type") == "tool_use":
                    araclar.append(f"{c['name']}:{json.dumps(c['input'], ensure_ascii=False)[:110]}")
    print(f"== {f.name[:8]} {kol} işler={icerik[icerik.find('1.') if '1.' in icerik else 0:][:40]!r} msj={len(uso)}")
    print("   kullanım(in,cc,cr,out) ilk/son:", uso[:1], uso[-1:])
    for a in araclar:
        print("   -", a)
