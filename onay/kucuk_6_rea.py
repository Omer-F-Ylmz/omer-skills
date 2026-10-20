"""KUCUK-6: Desktop config'te rea sunucusunu tools/mcp-launch/rea-sema.js sarmalayıcısına çevirir
(compare_web_captures şeması 166 KB/derinlik 31 → sadeleştirilmiş). python onay/kucuk_6_rea.py [--kuru|--geri]  (Desktop'ı yeniden başlat)"""
import json
import shutil
import sys

CONFIG = "C:/Users/pc/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/claude_desktop_config.json"
YEDEK = CONFIG + ".kucuk-6.bak"
NODE = "C:/Users/pc/AppData/Local/Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/node.exe"
SARMAL = "C:/Projeler/omer-skills/tools/mcp-launch/rea-sema.js"

if "--geri" in sys.argv:
    shutil.copyfile(YEDEK, CONFIG)
    sys.exit(print("geri alındı"))
cfg = json.load(open(CONFIG, encoding="utf-8"))
cfg["mcpServers"]["rea"] = {"command": NODE, "args": [SARMAL]}
if "--kuru" in sys.argv:
    sys.exit(print(json.dumps(cfg["mcpServers"]["rea"], indent=1)))
shutil.copyfile(CONFIG, YEDEK)
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("yazıldı; yedek", YEDEK)
