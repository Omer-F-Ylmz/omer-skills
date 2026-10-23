"""Profil config'ini 5 sn arayla 55 sn izler: mtime + code-mode/hostinger/rea durumu (deger yazdirmaz)."""
import glob, json, os, time
p = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\*\claude_desktop_config.json"))[0]
onceki = None
for i in range(12):
    try:
        s = json.load(open(p, encoding="utf-8")).get("mcpServers", {})
        d = (time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p))), len(s), "cm" in s or "code-mode" in s, "hostinger" in s,
             os.path.basename(str((s.get("rea") or {}).get("args", ["-"])[0])))
    except Exception as e:
        d = ("okunamadi", str(e)[:60])
    if d != onceki:
        print(time.strftime("%H:%M:%S"), "->", d, flush=True)
        onceki = d
    time.sleep(5)
