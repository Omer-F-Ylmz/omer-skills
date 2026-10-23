"""USTA-OKULU-0: alan başına kaynak envanteri (var/eksik) -> docs/okul/envanter.md. Salt okuma, Claude yok.
  python tools/okul/envanter.py"""
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
alanlar = json.loads((Path(__file__).with_name("alanlar.json")).read_text(encoding="utf-8"))
skills = sorted({p.name for d in (KOK / "skills", Path.home() / ".claude/skills") if d.is_dir() for p in d.iterdir() if p.is_dir()})
mcp_adlari = set()
for f in (KOK / ".mcp.json", Path.home() / ".claude.json"):
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
        mcp_adlari |= set((d.get("mcpServers") or {}).keys())
    except Exception:
        pass
cikti = ["# Okul envanteri (otomatik; tools/okul/envanter.py)", "", f"skill dizini: {len(skills)} · MCP: {len(mcp_adlari)}", ""]
for k, a in alanlar.items():
    es = [s for s in skills if any(t in s.lower() for t in a["anahtar"])]
    mcp = [m for m in a["mcp"] if any(m in x for x in mcp_adlari)]
    eksik = [m for m in a["mcp"] if m not in mcp]
    kart = (KOK / "docs/okul" / f"{k}.md").exists()
    cikti.append(f"## {k} — {a['ad']}")
    cikti.append(f"- skill {len(es)}: " + ", ".join(es[:12]) + (" …" if len(es) > 12 else ""))
    cikti.append(f"- MCP var: {mcp or '-'} · eksik: {eksik or '-'}")
    cikti.append(f"- ek kaynak: {a['ek']} · proje: {a['proje']} · ders kitabı: {'var' if kart else 'YOK'}")
    cikti.append("")
(KOK / "docs/okul").mkdir(parents=True, exist_ok=True)
(KOK / "docs/okul/envanter.md").write_text("\n".join(cikti), encoding="utf-8")
print("\n".join(c for c in cikti if c.startswith("## ") or c.startswith("- skill")))
