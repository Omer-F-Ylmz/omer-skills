"""IHTIYAC-AC-1 (3): Claude Desktop MCP'leri çekirdek + 'iş başında aç' (silme yok; çıkarılan tanım config içinde _parkta_mcpServers'ta kalır).
  python tools/desktop_mcp.py durum              açık / parktaki sunucu adları
  python tools/desktop_mcp.py park               çekirdek dışını park et (önce yedek)
  python tools/desktop_mcp.py ac <ad> [ad..]     parktakini geri aç (Desktop'u yeniden başlat)
  python tools/desktop_mcp.py geri               en son yedeği aynen geri yükler
Env DEĞERİ hiçbir komutta basılmaz. Etki için Desktop'u bir kez yeniden başlat."""
import json
import os
import shutil
import sys
import time
from pathlib import Path

CFG = Path(os.environ["LOCALAPPDATA"]) / "Packages" / "Claude_pzs8sxrjxfjjc" / "LocalCache" / "Roaming" / "Claude" / "claude_desktop_config.json"
YEDEK = Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "yedek" / "desktop-mcp"
# rea/xerj/code-mode/ruflo: çekirdek; hostinger/apify-actors: havuz köprüsü (ucuz, tek kopya)
CEKIRDEK = {"rea", "xerj", "code-mode", "ruflo", "hostinger", "apify-actors"}


def oku():
    return json.loads(CFG.read_text(encoding="utf-8"))


def yaz(d):
    CFG.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def yedekle():
    YEDEK.mkdir(parents=True, exist_ok=True)
    y = YEDEK / f"claude_desktop_config-{time.strftime('%Y%m%d-%H%M%S')}.json"
    shutil.copy2(CFG, y)
    return y


if __name__ == "__main__":
    a = sys.argv[1:] or ["durum"]
    d = oku()
    acik, park = d.setdefault("mcpServers", {}), d.setdefault("_parkta_mcpServers", {})
    if a[0] == "park":
        print("yedek:", yedekle())
        for ad in [x for x in acik if x not in CEKIRDEK]:
            park[ad] = acik.pop(ad)
        yaz(d)
    elif a[0] == "ac":
        print("yedek:", yedekle())
        for ad in a[1:]:
            if ad in park:
                acik[ad] = park.pop(ad)
            else:
                print("parkta yok:", ad)
        yaz(d)
    elif a[0] == "geri":
        y = sorted(YEDEK.glob("claude_desktop_config-*.json"))
        if y:
            shutil.copy2(y[0], CFG)  # en eski yedek = park öncesi asıl hâl
            print("geri yüklendi:", y[0].name)
        sys.exit(0)
    print("açık:", " ".join(sorted(acik)))
    print("parkta:", " ".join(sorted(park)))
