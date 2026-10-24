import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
D = r"C:\Projeler\omer-skills\.kos\kopru\ajan-sira"
KISA = "--kisa" in sys.argv
for ad in [a for a in sys.argv[1:] if a != "--kisa"]:
    p = os.path.join(D, ad + ".json")
    try:
        d, _ = json.JSONDecoder().raw_decode(open(p, encoding="utf-8", errors="replace").read().lstrip())  # RAM-BEKCI-3c: sonuna yapisan hook hata metni (Extra data) yok sayilir
    except Exception as e:
        print("==", ad, "OKUNAMADI", e, os.path.getsize(p) if os.path.exists(p) else "yok")
        continue
    st = d.get("subagent_stats") or {}
    mu = {k: round(v.get("costUSD", 0), 2) for k, v in (d.get("modelUsage") or {}).items()}
    try:  # ZORUNLU-ARAÇ-1: denetim bayrağı üst satırda
        den = json.load(open(os.path.join(D, ad + ".denetim.json"), encoding="utf-8"))
        bayrak = f"[{den['durum'].upper()}: {', '.join(den['eksik'])[:120]}] " if den["durum"] != "ok" else ""
    except (OSError, ValueError, KeyError):
        bayrak = ""
    print(f"== {bayrak}{ad} · ${d.get('total_cost_usd', 0):.2f} · {mu} · turn {d.get('num_turns')} · spawned {st.get('spawned')} killed.sys {(st.get('killed') or {}).get('system')} · by_type {st.get('by_type')} · {d.get('subtype')}")
    r = (d.get("result") or "").splitlines()
    if KISA:
        r = r[:6] + [x for x in r[6:] if "★" in x][:1]
    print(chr(10).join(r)[:2200])
