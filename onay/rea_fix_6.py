"""REA-FIX-6 (c): Desktop'un okudugu profil config'ine (Claude-Data) rea compact + code-mode + hostinger.
Kok 1: onceki duzeltmeler yalniz %APPDATA%\\Claude config'ine yaziliyordu.
Kok 2: Desktop ACIKKEN config'i bellekteki kopyasiyla geri yaziyor -> yalniz Desktop kapaliyken uygulanir (desktop_kapat_duzelt.ps1).
Kok 3 (24 Eki 00:41 kaniti): Desktop aciliste komutu tam yol olmayan sunuculari (node / npx) siliyor -> komut tam yola cevrilir.
Deger/env yazdirmaz. python -I onay/rea_fix_6.py [--kuru|--geri]"""
import glob, json, os, shutil, sys

NODE = "C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
COMPACT = "C:/Projeler/omer-skills/tools/rea-mcp-compact.mjs"
KAYNAK = os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json")
PROFIL = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\*\claude_desktop_config.json"))
kuru, geri = "--kuru" in sys.argv, "--geri" in sys.argv


def tam_yol(v):
    v = json.loads(json.dumps(v))
    k = os.path.basename(str(v.get("command", ""))).lower()
    if k in ("node", "node.exe") and not os.path.isabs(str(v.get("command", ""))):
        v["command"] = NODE
    elif k in ("npx", "npx.cmd") and not os.path.isabs(str(v.get("command", ""))):
        v["command"] = "cmd"
        v["args"] = ["/c", "npx"] + list(v.get("args", []))
    return v


def gecerli(v):
    c = str(v.get("command", ""))
    if c.lower() == "cmd":
        return True
    if not os.path.isabs(c) or not os.path.exists(c):
        return False
    for a in v.get("args", []):
        a = str(a)
        if a.lower().endswith((".js", ".mjs", ".cjs")) and not os.path.exists(a):
            return False
    return True


r = json.load(open(KAYNAK, encoding="utf-8")).get("mcpServers", {}) if os.path.exists(KAYNAK) else {}
ekle = {k: tam_yol(r[k]) for k in ("code-mode", "hostinger") if k in r}

for p in PROFIL:
    yedek = p + ".rea-fix-6.bak"
    if geri:
        if os.path.exists(yedek):
            shutil.copyfile(yedek, p); print("geri:", p)
        continue
    cfg = json.load(open(p, encoding="utf-8"))
    s = cfg.setdefault("mcpServers", {})
    deg = []
    if (s.get("rea") or {}).get("args") != [COMPACT]:
        s["rea"] = {"command": NODE, "args": [COMPACT]}; deg.append("rea")
    for k, v in ekle.items():
        if not gecerli(v):
            print(f"  UYARI {k}: komut/dosya bulunamadi, eklenmedi"); continue
        if s.get(k) != v:
            s[k] = v; deg.append(k)
    for k, v in s.items():
        if not gecerli(v):
            print(f"  UYARI mevcut {k}: komut tam yol degil/bulunamadi ({os.path.basename(str(v.get('command','')))})")
    print(p, "\n  degisecek:", deg or "-", "| tum gecerli:", all(gecerli(v) for v in s.values()))
    if not deg or kuru:
        continue
    shutil.copyfile(p, yedek)
    json.dump(cfg, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("  -> yazildi; yedek", os.path.basename(yedek))
