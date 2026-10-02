"""TOKEN-2b: once/sonra gözlemlerinden ≤10 kör çift (A/B karışık) → kor-ciftler.md + kor-anahtar.json."""
import hashlib
import json
import sqlite3
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
BU = Path(__file__).parent
c = sqlite3.connect(f"file:{Path.home() / '.claude-mem/claude-mem.db'}?mode=ro", uri=True)
c.row_factory = sqlite3.Row
ALAN = ("type", "title", "subtitle", "narrative", "facts", "files_read")


def gozlemler(e):
    sid = json.loads((KOK / f"olcum/token-2-kapi-{e}.json").read_text(encoding="utf-8"))["session_id"]
    return [dict(r) for r in c.execute(
        "select o.* from observations o join sdk_sessions s on o.memory_session_id = s.memory_session_id "
        "where s.content_session_id = ? order by o.id", (sid,))]


def dosyalar(o):
    return set(json.loads(o.get("files_read") or "[]"))


once, sonra = gozlemler("once"), gozlemler("sonra")
ciftler, kalan = [], list(sonra)
for o in once:  # dosya örtüşmesi en yüksek sonra-gözlemiyle eşle; eşit → sıra
    if not kalan or len(ciftler) == 10:
        break
    s = max(kalan, key=lambda x: (len(dosyalar(o) & dosyalar(x)), -kalan.index(x)))
    kalan.remove(s)
    ciftler.append((o, s))

md, anahtar = ["# Kör çiftler\n"], []
for i, (o, s) in enumerate(ciftler, 1):
    ters = hashlib.sha256(f"{o['id']}-{s['id']}".encode()).digest()[0] % 2
    a, b = (s, o) if ters else (o, s)
    anahtar.append({"cift": i, "A": "sonra" if ters else "once", "once_id": o["id"], "sonra_id": s["id"]})
    md.append(f"\n## Çift {i}\n")
    for etiket, g in (("A", a), ("B", b)):
        md.append(f"\n### {etiket}\n" + "\n".join(f"- {k}: {str(g.get(k) or '')[:1200]}" for k in ALAN) + "\n")
(BU / "kor-ciftler.md").write_text("".join(md), encoding="utf-8")
(BU / "kor-anahtar.json").write_text(json.dumps(anahtar, indent=1), encoding="utf-8")
print(f"once={len(once)} sonra={len(sonra)} cift={len(ciftler)}")
