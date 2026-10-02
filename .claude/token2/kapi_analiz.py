"""TOKEN-2b kapı analizi: once/sonra pencerelerinde observer istekleri (compress / diğer) + gözlem sayısı."""
import json
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
from token_olc import SIKISTIR, agirlikli, parcala, usd  # noqa: E402

OBS_DIR = Path.home() / ".claude/projects/C--Users-pc--claude-mem-observer-sessions"
DB = Path.home() / ".claude-mem/claude-mem.db"
t = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))  # noqa: E731


def ilk_metin(satirlar):
    for s in satirlar:
        if s.get("type") == "user":
            c = s.get("message", {}).get("content")
            return c if isinstance(c, str) else " ".join(b.get("text", "") for b in c or [] if isinstance(b, dict))
    return ""


def pencere(k):
    t0, t2 = t(k["t0"]), t(k["t2"]) + timedelta(seconds=60)
    out, gor = {}, set()
    for f in OBS_DIR.glob("*.jsonl"):
        if datetime.fromtimestamp(f.stat().st_mtime).astimezone() < t0:
            continue
        sat = [json.loads(x) for x in f.read_text(encoding="utf-8").splitlines() if x.strip()]
        tur = "compress" if ilk_metin(sat).startswith(SIKISTIR) else "diger"
        for s in sat:
            m = s.get("message", {})
            u, ts = m.get("usage"), s.get("timestamp")
            if s.get("type") != "assistant" or not u or not ts or not (t0 <= t(ts) <= t2) or m.get("id") in gor:
                continue
            gor.add(m.get("id"))
            r = out.setdefault(tur, {"istek": 0, "agirlikli": 0, "usd": 0, **dict.fromkeys(parcala({}), 0)})
            r["istek"] += 1
            r["agirlikli"] += agirlikli(u)
            r["usd"] += usd(u, m.get("model")) or 0
            for a, v in parcala(u).items():
                r[a] += v
    return out


def gozlem(sid):
    c = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    return [r[0] for r in c.execute(
        "select o.id from observations o join sdk_sessions s on o.memory_session_id = s.memory_session_id "
        "where s.content_session_id = ? order by o.id", (sid,))]


sonuc = {}
for e in ("once", "sonra"):
    k = json.loads((KOK / f"olcum/token-2-kapi-{e}.json").read_text(encoding="utf-8"))
    sonuc[e] = {"cost": k.get("cost"), "pencere": pencere(k), "gozlem": gozlem(k["session_id"])}
print(json.dumps(sonuc, ensure_ascii=False, indent=1))
