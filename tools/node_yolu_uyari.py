"""Global SessionStart (startup) erken uyarisi: ~/.claude.json'daki bir MCP komutu var olmayan node.exe'ye
isaret ediyorsa tek satir yazar; sorun yoksa sessiz. Ag ve arac cagrisi yok.
"""
import json
import os
import sys

UYARI = r"MCP node yolu kırık (Node güncellenmiş): python C:\Projeler\omer-skills\tools\mcp_guncelle.py node-yolu"


def uyari(cfg):
    sunucular = json.load(open(cfg, encoding="utf-8")).get("mcpServers", {})
    kirik = any(t.get("command", "").lower().endswith("node.exe") and not os.path.exists(t["command"])
                for t in sunucular.values())
    return UYARI if kirik else ""


if __name__ == "__main__":
    s = uyari(os.path.expanduser("~/.claude.json"))
    if s:
        sys.stdout.reconfigure(encoding="utf-8")
        print(s)
