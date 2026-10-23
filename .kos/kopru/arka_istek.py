"""ARKA-KALICI-1: ajanlar uzun işi doğrudan başlatmaz (ajan bitince job'la birlikte ölür); .kos/kopru/arka-istek/<ad>.json yazar.
İstek: {"komut": ["tools/x.py", "arg"], "gunluk": ".kos/kopru/x.log", "cwd": "isteğe bağlı"} (komut = python betiği + argümanlar).
Kalıcı yönetici (ajan_sira.py) her döngüde isle() çağırır: arka.py ile başlatır, "pid" (ya da "hata") yazar.
Dosyada pid/hata varsa ikinci başlatma yok; yeniden başlatmak için isteği pid'siz yeniden yaz."""
import ctypes
import json
import re
import subprocess
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
ISTEK = KOK / ".kos" / "kopru" / "arka-istek"
ARKA = KOK / ".kos" / "kopru" / "arka.py"


def _canli(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if h:
        ctypes.windll.kernel32.CloseHandle(h)
    return bool(h)


def isle(klasor=ISTEK, arka=ARKA, log=print):
    for f in sorted(Path(klasor).glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue  # yarım yazılmış olabilir; sonraki döngüde yeniden denenir
        if not isinstance(d, dict) or "hata" in d:
            continue
        komut, gunluk = d.get("komut"), d.get("gunluk")
        if "pid" in d:
            # gözetmen ölmüşse ve iş BITIS yazmadan bitmişse yeniden başlat (en fazla 3 kez)
            bitti = isinstance(gunluk, str) and gunluk and Path(gunluk).is_file() and any(s.startswith("BITIS") for s in Path(gunluk).read_text(encoding="utf-8", errors="replace").splitlines())
            if _canli(d["pid"]) or bitti or d.get("yeniden", 0) >= 3:
                continue
            d.pop("pid")
            d["yeniden"] = d.get("yeniden", 0) + 1
        if not (isinstance(komut, list) and komut and isinstance(gunluk, str) and gunluk):
            d["hata"] = "komut (liste) ve gunluk (metin) şart"
        else:
            argv = [sys.executable, str(arka)] + (["--cwd", d["cwd"]] if d.get("cwd") else []) + [gunluk, *map(str, komut)]
            r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60, creationflags=0x08000000)
            m = re.search(r"arka pid (\d+)", r.stdout)
            if m:
                d["pid"], d["basladi"] = int(m.group(1)), time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                d["hata"] = (r.stdout + r.stderr).strip()[-300:] or f"rc {r.returncode}"
        f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        log("ARKA-İSTEK", f.stem, d.get("pid") or d.get("hata"))
