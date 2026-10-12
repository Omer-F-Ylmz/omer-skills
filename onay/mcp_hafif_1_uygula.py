"""MCP-HAFIF-1 onay betiği (Desktop koşar): arka plan claude -p oturumlarının açtığı her Serena örneği kendi tepsi simgesini/
pencere arayüzünü açmasın. ~/.serena/serena_config.yml: web_dashboard_interface boş (Windows'ta `app` = örnek başına tepsi +
pencere) → `browser`; web_dashboard_open_on_launch false kalır. Sunucu, araçlar ve panel aynı (http://localhost:24282/dashboard/).
python onay/mcp_hafif_1_uygula.py --kuru   # plan: değişecek satırlar
python onay/mcp_hafif_1_uygula.py uygula   # yedek alır (serena_config.yml.bak-mcphafif1-<zaman>) → yazar
python onay/mcp_hafif_1_uygula.py --geri   # son mcphafif1 yedeğini geri koyar"""
import re
import shutil
import sys
import time
from pathlib import Path

EV = Path.home()
HEDEF = {b"web_dashboard_interface": b"browser", b"web_dashboard_open_on_launch": b"false"}


def yol(ev=EV):
    return ev / ".serena" / "serena_config.yml"


def degisim(veri):
    """→ (yeni bayt, [(anahtar, eski, yeni)]). Satır sonu (LF/CRLF) ve yorumlar korunur."""
    fark = []
    for k, v in HEDEF.items():
        m = re.search(rb"^" + k + rb":[ \t]*([^\r\n#]*)", veri, re.M)
        if not m:
            sys.exit(f"anahtar yok: {k.decode()} — Serena sürümü değişmiş olabilir, elle bak")
        if m.group(1).strip() != v:
            fark.append((k.decode(), m.group(1).strip().decode(), v.decode()))
            veri = veri[:m.start()] + k + b": " + v + veri[m.end():]
    return veri, fark


def kuru(ev=EV):
    _, fark = degisim(yol(ev).read_bytes())
    for k, e, y in fark:
        print(f"{k}: {e or '(boş)'} → {y}")
    print("değişiklik yok" if not fark else f"{len(fark)} satır; sonraki Serena başlangıcından itibaren (çalışanlar etkilenmez)")
    return fark


def uygula(ev=EV):
    p = yol(ev)
    yeni, fark = degisim(p.read_bytes())
    if not fark:
        print("değişiklik yok")
        return None
    yedek = p.with_name(f"{p.name}.bak-mcphafif1-{time.strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(p, yedek)
    p.write_bytes(yeni)
    print(f"uygulandı ({len(fark)} satır), yedek {yedek.name}")
    return yedek


def geri(ev=EV):
    p = yol(ev)
    yedekler = sorted(p.parent.glob(f"{p.name}.bak-mcphafif1-*"))
    if not yedekler:
        sys.exit("mcphafif1 yedeği yok")
    shutil.copy2(yedekler[-1], p)
    print(f"geri alındı: {yedekler[-1].name}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"--kuru": kuru, "uygula": uygula, "--geri": geri}[sys.argv[1] if len(sys.argv) > 1 else "--kuru"]()
