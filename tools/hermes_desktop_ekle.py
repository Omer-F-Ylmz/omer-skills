"""Claude Desktop yapılandırmasına hermes MCP girdisini ekler (yedek alır, diğer girdilere dokunmaz)."""
import json
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
CFG = Path(sys.argv[1])
yedek = CFG.with_suffix(".json.hermes-oncesi")
if not yedek.exists():
    shutil.copy2(CFG, yedek)

ham = CFG.read_bytes()
crlf = b"\r\n" in ham
cfg = json.loads(ham.decode("utf-8-sig"))
cfg.setdefault("mcpServers", {})["hermes"] = {
    "command": str(KOK / "araclar/hermes/Scripts/hermes.exe"),
    "args": ["mcp-serve"],
    "env": {"HERMES_HOME": str(KOK / "araclar/hermes-home"), "PYTHONUTF8": "1"},
}
metin = json.dumps(cfg, indent=2, ensure_ascii=False)
CFG.write_bytes((metin.replace("\n", "\r\n") if crlf else metin).encode("utf-8"))
print("mcpServers:", ",".join(cfg["mcpServers"]))
