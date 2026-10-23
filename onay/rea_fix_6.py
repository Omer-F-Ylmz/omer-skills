"""REA-FIX-6: Desktop'un okudugu TUM config dosyalarinda rea -> rea-mcp-compact.mjs ve code-mode girisi esitlenir.
Kok (24 Eki): REA-FIX-5 ve CODE-MODE-1 yalniz %APPDATA%\\Claude config'ine yazdi; Desktop ise
%LOCALAPPDATA%\\Claude-Data\\<profil>\\claude_desktop_config.json okuyor -> rea full sema (popup), code-mode yok.
Deger/env yazdirmaz. python -I onay/rea_fix_6.py [--kuru|--geri]  -> sonra Desktop'u tamamen kapat-ac."""
import glob, json, os, shutil, sys

NODE = "C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
COMPACT = "C:/Projeler/omer-skills/tools/rea-mcp-compact.mjs"
KAYNAK = os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json")
ADAY = [KAYNAK]
ADAY += glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\*\claude_desktop_config.json"))
ADAY += glob.glob(os.path.expandvars(r"%APPDATA%\Claude-Data\*\claude_desktop_config.json"))
kuru, geri = "--kuru" in sys.argv, "--geri" in sys.argv

cm = None
if os.path.exists(KAYNAK):
    cm = json.load(open(KAYNAK, encoding="utf-8")).get("mcpServers", {}).get("code-mode")

for p in ADAY:
    if not os.path.exists(p):
        continue
    yedek = p + ".rea-fix-6.bak"
    if geri:
        if os.path.exists(yedek):
            shutil.copyfile(yedek, p); print("geri:", p)
        continue
    cfg = json.load(open(p, encoding="utf-8"))
    s = cfg.setdefault("mcpServers", {})
    eski = s.get("rea") or {}
    rea_ok = eski.get("args") == [COMPACT]
    cm_ok = "code-mode" in s
    print(f"{p}\n  rea: {'DOGRU' if rea_ok else 'YANLIS'}  code-mode: {'VAR' if cm_ok else 'YOK'}")
    if (rea_ok and (cm_ok or cm is None)) or kuru:
        continue
    shutil.copyfile(p, yedek)
    if not rea_ok:
        s["rea"] = {"command": NODE, "args": [COMPACT]}
    if not cm_ok and cm is not None:
        s["code-mode"] = cm
    json.dump(cfg, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("  -> yazildi (rea compact" + (", code-mode eklendi" if not cm_ok and cm else "") + "); yedek", os.path.basename(yedek))
