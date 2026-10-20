"""rea + ruflo'yu Desktop'ın GERÇEK config'ine ekler (Claude-Data). python desktop_gercek.py [--kuru|--geri]"""
import json
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")
HEDEF = "C:/Users/pc/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/claude_desktop_config.json"
KAYNAK = "C:/Users/pc/AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/claude_desktop_config.json"
YEDEK = HEDEF + ".rea-ruflo.bak"
if "--geri" in sys.argv:
    shutil.copyfile(YEDEK, HEDEF)
    sys.exit(print("geri alındı"))
hedef = json.load(open(HEDEF, encoding="utf-8"))
kaynak = json.load(open(KAYNAK, encoding="utf-8"))["mcpServers"]
sunucu = hedef.setdefault("mcpServers", {})
once = len(sunucu)
for ad in ("rea", "ruflo"):
    sunucu[ad] = dict(kaynak[ad])
sunucu["ruflo"]["command"] = "C:\\Projeler\\omer-skills\\tools\\mcp-launch\\ruflo.cmd"
if "--kuru" in sys.argv:
    sys.exit(print("kuru:", once, "->", len(sunucu), json.dumps({k: sunucu[k]["command"] for k in ("rea", "ruflo")}, ensure_ascii=False)))
import os
if not os.path.exists(YEDEK):
    shutil.copyfile(HEDEF, YEDEK)
json.dump(hedef, open(HEDEF, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
json.load(open(HEDEF, encoding="utf-8"))
print("eklendi:", once, "->", len(sunucu), "yedek", YEDEK)
