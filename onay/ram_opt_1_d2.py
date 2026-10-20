"""RAM-OPT-1 d2: rea'yı cmd→npx→node zincirinden doğrudan node + global paket yoluna çevirir (iki config'te de).
Zincir Desktop başına ~430 MB'tı (cmd 8 + npx 144 + cmd 8 + rea.mjs 256); doğrudan çağrı yalnız rea.mjs'i bırakır.
python onay/ram_opt_1_d2.py [--kuru|--geri]   (uygulamak için Desktop'ı yeniden başlat)"""
import json
import shutil
import sys

KOK = "C:/Users/pc/AppData/Local/"
CONFIGLER = [KOK + "Claude-Data/claude_pzs8sxrjxfjjc/claude_desktop_config.json",
             KOK + "Packages/Claude_pzs8sxrjxfjjc/LocalCache/Roaming/Claude/claude_desktop_config.json"]
NODE = KOK + "Microsoft/WinGet/Packages/OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe/node-v24.19.0-win-x64/"
REA = {"command": NODE + "node.exe", "args": [NODE + "node_modules/rea-agents/scripts/rea.mjs", "mcp"]}

for yol in CONFIGLER:
    yedek = yol + ".ram-opt-1-d2.bak"
    if "--geri" in sys.argv:
        shutil.copyfile(yedek, yol)
        continue
    cfg = json.load(open(yol, encoding="utf-8"))
    cfg["mcpServers"]["rea"] = {**cfg["mcpServers"]["rea"], **REA}
    if "--kuru" in sys.argv:
        print(yol[-40:], json.dumps(cfg["mcpServers"]["rea"]))
        continue
    shutil.copyfile(yol, yedek)
    json.dump(cfg, open(yol, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("yazıldı; yedek", yedek)
