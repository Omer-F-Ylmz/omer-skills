"""BEYIN-ARAC-KART-1: arac-ara MCP'sini CC (~/.claude.json) ve Claude Desktop yapılandırmasına ekleyen onay betiği.
  python tools/arac_ara_kur.py            kuru koşu: ne eklenecek, hangi dosyaya (yazmaz)
  python tools/arac_ara_kur.py --uygula   iki dosyaya `arac-ara` girdisini ekler (yedek: <dosya>.arac-ara.bak); zaten aynıysa dokunmaz
Yalnız `mcpServers.arac-ara` yazılır; başka anahtara/ortam değerine dokunulmaz, hiçbir değer basılmaz."""
import json
import os
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
GIRDI = {"command": sys.executable, "args": ["-I", str(KOK / "tools/arac_ara_mcp.py")]}
# Desktop'ın gerçek dosyası %LOCALAPPDATA%\Claude-Data\<paket>\ altında (Packages\...\Roaming yönlendirmesi aynı dosyaya çıkar)
DESKTOP = sorted(Path(os.environ.get("LOCALAPPDATA") or Path.home() / "AppData/Local").glob("Claude-Data/**/claude_desktop_config.json"))[:1]
HEDEFLER = [Path.home() / ".claude.json", *DESKTOP]


def isle(yol, uygula):
    if not yol.exists():
        return f"{yol}: yok (atlandı)"
    j = json.loads(yol.read_text(encoding="utf8"))
    if j.get("mcpServers", {}).get("arac-ara") == GIRDI:
        return f"{yol}: zaten kurulu"
    if uygula:
        shutil.copy2(yol, yol.with_name(yol.name + ".arac-ara.bak"))
        j.setdefault("mcpServers", {})["arac-ara"] = GIRDI
        yol.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf8")
        return f"{yol}: eklendi"
    return f"{yol}: eklenecek (mcpServers.arac-ara → {GIRDI['command']} -I tools/arac_ara_mcp.py)"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    for h in HEDEFLER:
        print(isle(h, "--uygula" in sys.argv))
