"""Roaming config'teki code-mode ve hostinger girislerinin YAPISI (anahtar adlari, komut/arg dosya adlari; deger yok)."""
import json, os
s = json.load(open(os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json"), encoding="utf-8"))
print("ust anahtarlar:", list(s))
for k in ("code-mode", "hostinger", "rea"):
    v = s.get("mcpServers", {}).get(k) or {}
    print(k, "alanlar:", list(v), "| command:", os.path.basename(str(v.get("command", ""))),
          "| args:", [os.path.basename(str(a)) if ("/" in str(a) or "\\" in str(a)) else str(a)[:40] for a in v.get("args", [])],
          "| env adlari:", list((v.get("env") or {}).keys()))
