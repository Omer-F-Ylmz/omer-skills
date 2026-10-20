"""ÖĞREN-2 d3: url/exe-only MCP kayıtlarının kaynak dosyasına yerel README/şema ekler (üstüne yazar; ilk kayıt metni korunur).
  python -X utf8 .claude/ogren2/mcp_kaynak.py"""
import glob
from pathlib import Path

K = Path(__file__).parent / "kaynak"
H = Path.home() / ".claude" / "plugins"
KAYNAK = {
    "godot": ["C:/AI/mcp/godot/node_modules/@coding-solo/godot-mcp/README.md"],
    "blender": ["C:/blender_mcp/mcp/README.md"],
    "claude-design": ["tools/cc-kopru/tasarim.mjs", "tools/cc-kopru/tasarim-semalar.json"],
    "21st": sorted(glob.glob(str(H / "cache/21st-dev/21st/*/README.md")) + glob.glob(str(H / "marketplaces/21st-dev/skills/21st-ui/SKILL.md"))),
}
for ad, dosyalar in KAYNAK.items():
    p = K / f"{ad}.txt"
    t = p.read_text(encoding="utf-8")
    if "=== yerel kaynak:" in t:
        continue
    for d in dosyalar:
        m = Path(d)
        t += f"\n=== yerel kaynak: {d} ===\n" + m.read_text(encoding="utf-8", errors="replace")
    p.write_text(t, encoding="utf-8")
    print(ad, len(dosyalar), len(t.splitlines()))
