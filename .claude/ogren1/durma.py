"""ÖĞREN-1 d4: d1–d3 transkriptlerinde önbellek durması (cw=0, girdi ≥3000; durum_ozet.durma_orani tanımı)
adım adım: önceki adımdan süre (TTL 5m), cr düşüşü, önceki araç çıktısı baytı. Kullanım: python durma.py <jsonl>..."""
import json, sys
from datetime import datetime
from pathlib import Path


def zaman(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def coz(yol):
    adim, gorulen, arac_bayt = [], set(), 0
    for s in Path(yol).open(encoding="utf-8", errors="replace"):
        try:
            o = json.loads(s)
        except ValueError:
            continue
        m = o.get("message") if isinstance(o, dict) else None
        if o.get("type") == "user" and isinstance(m, dict) and isinstance(m.get("content"), list):
            arac_bayt += sum(len(json.dumps(c.get("content"), ensure_ascii=False)) for c in m["content"]
                             if isinstance(c, dict) and c.get("type") == "tool_result")
            continue
        if o.get("type") != "assistant" or not isinstance(m, dict) or not isinstance(m.get("usage"), dict) \
                or m.get("id") in gorulen:
            continue
        gorulen.add(m.get("id"))
        u = m["usage"]
        adim.append(dict(t=zaman(o.get("timestamp")), i=u.get("input_tokens") or 0,
                         cw=u.get("cache_creation_input_tokens") or 0, cr=u.get("cache_read_input_tokens") or 0,
                         model=m.get("model"), arac=arac_bayt))
        arac_bayt = 0
    return adim


for yol in sys.argv[1:]:
    a = coz(yol)
    d = [k for k, x in enumerate(a) if not x["cw"] and x["i"] >= 3000]
    print(f"== {Path(yol).stem[:8]} adım {len(a)} durma {len(d)} (son20: {sum(1 for k in d if k >= len(a) - 20)})")
    for k in d:
        x, p = a[k], a[k - 1] if k else None
        bosluk = (x["t"] - p["t"]).total_seconds() if p and x["t"] and p["t"] else -1
        print(f"  #{k} t+{bosluk:.0f}s i={x['i']} cr={x['cr']} oncekicr={p['cr'] if p else 0} "
              f"arac={x['arac']}B model={x['model']}")
