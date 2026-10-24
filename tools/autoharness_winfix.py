"""autoharness hooks.json'u cmd + Git Bash ikisinde de çalışan biçime getirir (python3 -c ile CLAUDE_PLUGIN_ROOT okunur). Plugin güncellemesinden sonra tekrar koşulur."""
import glob, json, os, shutil, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
KOMUT = "python3 -c \"import os,sys,runpy;sys.path.insert(0,os.environ['CLAUDE_PLUGIN_ROOT']+'/src');runpy.run_module('autoharness.hook.dispatch',run_name='__main__')\""
for p in glob.glob(os.path.expanduser(r"~\.claude\plugins\cache\autoharness\autoharness\*\hooks\hooks.json")):
    j = json.load(open(p, encoding="utf-8"))
    degisti = False
    for olay in j.get("hooks", {}).values():
        for grup in olay:
            for h in grup.get("hooks", []):
                if h.get("type") == "command" and "autoharness.hook.dispatch" in h.get("command", "") and h["command"] != KOMUT:
                    h["command"] = KOMUT
                    degisti = True
    if degisti:
        shutil.copy2(p, p + ".bak-oncesi-winfix")
        json.dump(j, open(p, "w", encoding="utf-8"), indent=2)
    print(p, "duzeltildi" if degisti else "zaten dogru")
