"""RAM-OPT-1 d3 (TASLAK): Desktop'ta kalan durumlu sunucuları mcp_koprusu köprüsüne alır → Desktop'ın ikinci başlatması
yalnız hafif köprü olur, gerçek sunucu havuzda tek kopya. Havuz o adı henüz sunmuyorsa girdiye DOKUNMAZ (araç bozulmaz).
python onay/ram_opt_1_d3.py [--kuru|--geri]   (uygulamak için Desktop'ı yeniden başlat)
Önkoşul: havuz (tools/mcp_paylasim.py) bu adları Desktop config'inden sunmalı; bugün PAYLASIM yalnız 21 durumsuz adı sunar."""
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import mcp_paylasim as mp  # noqa: E402

CONFIG = "C:/Users/pc/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/claude_desktop_config.json"
ADLAR = ["mcp-filesystem", "mcp-git", "obsidian", "claude-design", "binlog", "claude-mem", "puppeteer", "playwright", "blender"]
KOPRU = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tools", "ram", "mcp_koprusu.py"))
PY = "C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
yedek = CONFIG + ".ram-opt-1-d3.bak"

if "--geri" in sys.argv:
    shutil.copyfile(yedek, CONFIG)
    sys.exit(print("geri alındı"))
cfg = json.load(open(CONFIG, encoding="utf-8"))
for ad in ADLAR:
    try:
        araclar = mp.araclar_http(mp.url(ad))
    except Exception as e:
        print(f"{ad}: havuzda yok ({type(e).__name__}) — dokunulmadı")
        continue
    print(f"{ad}: havuz {len(araclar)} araç → köprü")
    if "--kuru" not in sys.argv:
        cfg["mcpServers"][ad] = {"command": PY, "args": ["-I", "-S", KOPRU, ad]}
if "--kuru" not in sys.argv:
    shutil.copyfile(CONFIG, yedek)
    json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print("yazıldı; yedek", yedek)
