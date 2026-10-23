"""Butun aday Desktop config dosyalari: mtime, sunucu sayisi, rea hedefi, code-mode/hostinger var mi (deger yazdirmaz)."""
import glob, json, os, time
ADAY = [os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json"),
        os.path.expandvars(r"%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json")]
ADAY += glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\*\claude_desktop_config.json"))
ADAY += glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\Claude-Data\*\claude_desktop_config.json"))
for p in ADAY:
    if not os.path.exists(p):
        print("YOK", p); continue
    s = json.load(open(p, encoding="utf-8")).get("mcpServers", {})
    rea = " ".join(map(str, (s.get("rea") or {}).get("args", [])))
    print(time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p))), len(s), "rea=" + os.path.basename(rea.split()[0]) if rea else "rea=-",
          "cm=" + ("VAR" if "code-mode" in s else "yok"), "host=" + ("VAR" if "hostinger" in s else "yok"), p)
