"""Ruflo MCP'yi Desktop (MSIX) yapılandırmasına ekler; önce yedek. python desktop_kaydet.py [--geri]"""
import json
import os
import shutil
import sys

YOL = "C:/Users/pc/AppData/Local/Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/claude_desktop_config.json"
YEDEK = YOL + ".ruflo2.bak"
if "--geri" in sys.argv:
    shutil.copyfile(YEDEK, YOL)
    sys.exit(print("geri alındı"))
cfg = json.load(open(YOL, encoding="utf-8"))
user = json.load(open("C:/Users/pc/.claude.json", encoding="utf-8"))["mcpServers"]["ruflo"]
if not os.path.exists(YEDEK):  # ilk (ruflo'suz) yedek korunur
    shutil.copyfile(YOL, YEDEK)
cfg.setdefault("mcpServers", {})["ruflo"] = {"command": shutil.which(user["command"]) or user["command"], "args": user["args"], "env": user["env"]}
json.dump(cfg, open(YOL, "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)
print("eklendi:", sorted(cfg["mcpServers"]))
