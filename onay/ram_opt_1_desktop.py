"""RAM-OPT-1: Desktop config'te paylaşım havuzundaki 8 sunucuyu stdio köprüsüne (tools/ram/mcp_koprusu.py) çevirir.
Desktop her sunucuyu iki kez başlatıyor; köprü ~22 MB, gerçek sunucu havuzda tek kopya. Env havuzdakiyle eşit doğrulandı.
python onay/ram_opt_1_desktop.py [--kuru|--geri]   (uygulamak için Desktop'ı yeniden başlat)"""
import json
import shutil
import sys

CONFIG = "C:/Users/pc/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/claude_desktop_config.json"
YEDEK = CONFIG + ".ram-opt-1.bak"
PYTHON = "C:\\Users\\pc\\AppData\\Local\\Programs\\Python\\Python312\\python.exe"
KOPRU = "C:\\Projeler\\omer-skills\\tools\\ram\\mcp_koprusu.py"
ADLAR = ["brave-search", "code-review", "headroom", "mcp-fetch", "mcp-memory", "mcp-sequential-thinking", "mcp-time", "stitch"]

if "--geri" in sys.argv:
    shutil.copyfile(YEDEK, CONFIG)
    sys.exit(print("geri alındı"))
cfg = json.load(open(CONFIG, encoding="utf-8"))
for ad in ADLAR:
    cfg["mcpServers"][ad] = {"command": PYTHON, "args": ["-I", "-S", KOPRU, ad]}
if "--kuru" in sys.argv:
    sys.exit(print(json.dumps({a: cfg["mcpServers"][a] for a in ADLAR}, indent=1)))
shutil.copyfile(CONFIG, YEDEK)
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("yazıldı; yedek", YEDEK)
