"""VİDEO-3 d5 teşhis: kaçan PAKETTE adlar ve yp nereden — sözlük (envanter/DF/sızıntı), metin penceresi, Gemini çıktıları. Salt okuma.
Kullanım (tools/video'dan): uv run python ../../.kos/kopru/video/v3_teshis.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from v3 import CIK, ONB  # noqa: E402
from video import kisa, uzun  # noqa: E402

KACAN = {"aZe5ZTYcF1M": ["Framer Motion", "Built-in browser", "TypeScript", "Neue Montreal"], "d_UE-wHLoZY": ["Tripo v3.1"],
         "FaChtkkG9X4": ["Claude Code"], "HYMDaMcuSGQ": ["Hafıza modu", "Araştırma masası modu", "Git", "Buluttaki Claude Code"],
         "YDAK1lvVXho": ["TypeScript", "OpenAI Pro paketi"]}
YP = {"1nGx7WR8YLE": ["KAP"], "HYMDaMcuSGQ": ["KAP", "img", "node"]}

y = json.loads((CIK / "kos.json").read_text(encoding="utf-8"))
t = kisa._tarama(ONB)
for v in sorted(set(KACAN) | set(YP)):
    d = ONB / v
    p = (d / "paket.md").read_text(encoding="utf-8")
    pc = p.casefold()
    mu = json.loads((d / "gemini-metin-uzun.json").read_text(encoding="utf-8"))["adlar"] if (d / "gemini-metin-uzun.json").is_file() else None
    g = [a["ad"] for a in y[v]["g"]["araclar"]]
    pen = uzun.pencereler(p)
    print(f"## {v} paket {len(p)} kr, pencere {len(pen)}, metin-uzun {'yok' if mu is None else len(mu)}, g {len(g)}")
    for ad in KACAN.get(v, []):
        k = " ".join(kisa._sozcuk(ad))
        i = pc.find(ad.casefold())
        env = t["ad"].get(k)
        print(f"  KAÇAN {ad!r}: konum {i}/{len(p)} · envanter {'yok' if not env else env[0]} · df {t['df'].get(k, 0)}/{t['n']}"
              f" · sızıntı {bool(env) and all(v[3:] in x for x in env[1])} · metin-uzun {any(ad.casefold() in a.casefold() for a in mu or [])}"
              f" · g {any(ad.casefold() in a.casefold() for a in g)}")
        print(f"     …{p[max(i - 80, 0):i + 60]!r}" if i >= 0 else "     (tam dizge yok)")
    for ad in YP.get(v, []):
        nd = [a.get("ne_dedi", "")[:80] for a in y[v]["g"]["araclar"] if a["ad"] == ad]
        so = [a["ad"] for a in kisa.sozluk_tara(d, {}) if a["ad"] == ad]
        print(f"  YP {ad!r}: g {nd} · metin-uzun {ad in (mu or [])} · sözlük {so}")
