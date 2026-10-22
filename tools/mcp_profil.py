"""MCP-AÇ-1: köprü ajanlarına görev türüne göre MCP profili (ajan_sira.py --mcp-config).
Tür tespiti zorunlu_arac.GORSEL ile aynı sözlük; tanımlar ~/.claude.json + ecc eklentisi .mcp.json'dan alınır (env değerleri yalnız yeni dosyaya kopyalanır, basılmaz).
  python mcp_profil.py "<görev metni>"    seçilen MCP adları (sınama)"""
import json
import re
import sys
from pathlib import Path

TEMEL = ["ruflo"]
TUR = [  # (desen, MCP'ler); türler birleşir
    (r"(?i)site-3d|\b(site|landing|three(\.js)?|webgl|3d|frontend)\b", ["rea", "playwright", "chrome-devtools", "context7", "21st"]),
    (r"(?i)\b(render\w*|blender)\b", ["blender"]),
    (r"(?i)\bvideo\w*", ["premiere-pro"]),
]
KAYNAK = [Path.home() / ".claude.json", *sorted((Path.home() / ".claude/plugins/cache/ecc/ecc").glob("*/.mcp.json"))]


def tanimlar():
    t = {}
    for f in KAYNAK:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        for ad, v in d.get("mcpServers", d).items():
            if isinstance(v, dict):
                t.setdefault(ad, v)
    return t


def sec(metin):
    ad = list(TEMEL)
    for desen, mcp in TUR:
        if re.search(desen, metin):
            ad += [m for m in mcp if m not in ad]
    return ad


def yaz(metin, hedef):
    """Profil dosyasını hedef'e yazar; tanımı olmayan MCP atlanır. Döner: seçilen adlar."""
    t = tanimlar()
    ad = [m for m in sec(metin) if m in t]
    Path(hedef).write_text(json.dumps({"mcpServers": {m: t[m] for m in ad}}), encoding="utf-8")
    return ad


if __name__ == "__main__":
    print(" ".join(m for m in sec(" ".join(sys.argv[1:])) if m in tanimlar()))
