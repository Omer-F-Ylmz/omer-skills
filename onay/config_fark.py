"""Iki Desktop config'ini yalniz sunucu ADI + komut dosya adi duzeyinde karsilastirir (env/deger yazdirmaz).
python -I onay/config_fark.py [--esitle]  --esitle: Roaming'de olup profilde olmayan sunuculari profile kopyalar (yedekli)."""
import glob, json, os, shutil, sys

R = os.path.expandvars(r"%APPDATA%\Claude\claude_desktop_config.json")
P = glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Claude-Data\*\claude_desktop_config.json"))

def oz(v):
    a = v.get("args") or []
    son = next((x for x in reversed(a) if isinstance(x, str) and ("/" in x or "\\" in x)), a[-1] if a else "")
    return os.path.basename(str(v.get("command", ""))) + " " + os.path.basename(str(son))

r = json.load(open(R, encoding="utf-8")).get("mcpServers", {})
for p in P:
    cfg = json.load(open(p, encoding="utf-8"))
    s = cfg.setdefault("mcpServers", {})
    yalniz_r = sorted(set(r) - set(s))
    yalniz_p = sorted(set(s) - set(r))
    farkli = sorted(k for k in set(r) & set(s) if oz(r[k]) != oz(s[k]))
    print(p)
    print("  roaming", len(r), "profil", len(s))
    print("  yalniz roaming:", yalniz_r or "-")
    print("  yalniz profil:", yalniz_p or "-")
    for k in farkli:
        print(f"  farkli {k}: roaming[{oz(r[k])}] profil[{oz(s[k])}]")
    if "--esitle" in sys.argv and yalniz_r:
        shutil.copyfile(p, p + ".config-fark.bak")
        for k in yalniz_r:
            s[k] = r[k]
        json.dump(cfg, open(p, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
        print("  -> profile eklendi:", yalniz_r)
