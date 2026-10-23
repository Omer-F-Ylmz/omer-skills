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


YENIDEN_TAVAN = 5  # ölen işi en çok bu kadar yeniden başlatır
BITTI = re.compile(r"^(BITIS|\d{4}-\d\d-\d\d \d\d:\d\d:\d\d DURUM (bitti|vazgecti))", re.M)  # iş ya da toplu_gozetmen.py yazar


def _canli(pid, basladi=None):
    """Pid canlı ve (basladi varsa) süreç ondan sonra doğmadıysa True (ölen pid'i başkası almış olabilir)."""
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    kod, ft = ctypes.c_ulong(), [ctypes.c_ulonglong() for _ in range(4)]  # FILETIME: yaratım, çıkış, çekirdek, kullanıcı
    ok = k.GetExitCodeProcess(h, ctypes.byref(kod)) and k.GetProcessTimes(h, *map(ctypes.byref, ft))
    k.CloseHandle(h)
    if not ok or kod.value != 259:
        return False
    return not basladi or ft[0].value / 1e7 - 11644473600 <= time.mktime(time.strptime(basladi, "%Y-%m-%d %H:%M:%S")) + 5


def _bitti(d):
    """Günlükte (istek başladığından beri) BITIS ya da gözetmenin bitti/vazgecti satırı var mı."""
    try:
        with open(KOK / d["gunluk"], "rb") as g:
            g.seek(d.get("ofset", 0))
            return bool(BITTI.search(g.read().decode("utf-8", "replace")))
    except OSError:
        return False


def isle(klasor=ISTEK, arka=ARKA, log=print):
    for f in sorted(Path(klasor).glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue  # yarım yazılmış olabilir; sonraki döngüde yeniden denenir
        if not isinstance(d, dict) or "hata" in d:
            continue
        if "pid" in d:  # başlamış: ölmüş ve BITIS yazmamışsa (oturum job'ı kapanınca gözetmen de ölür) pid'siz yeniden başlat
            if _canli(d["pid"], d.get("basladi")) or _bitti(d) or d.get("yeniden", 0) >= YENIDEN_TAVAN:
                continue
            d["yeniden"] = d.get("yeniden", 0) + 1
            log("ARKA-YENIDEN", f.stem, "pid", d.pop("pid"), "öldü, BITIS yok", d["yeniden"])
        komut, gunluk = d.get("komut"), d.get("gunluk")
        if not (isinstance(komut, list) and komut and isinstance(gunluk, str) and gunluk):
            d["hata"] = "komut (liste) ve gunluk (metin) şart"
        else:
            yol = KOK / gunluk
            d["ofset"] = yol.stat().st_size if yol.exists() else 0
            argv = [sys.executable, str(arka)] + (["--cwd", d["cwd"]] if d.get("cwd") else []) + [gunluk, *map(str, komut)]
            r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60, creationflags=0x08000000)
            m = re.search(r"arka pid (\d+)", r.stdout)
            if m:
                d["pid"], d["basladi"] = int(m.group(1)), time.strftime("%Y-%m-%d %H:%M:%S")
            else:
                d["hata"] = (r.stdout + r.stderr).strip()[-300:] or f"rc {r.returncode}"
        f.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        log("ARKA-İSTEK", f.stem, d.get("pid") or d.get("hata"))
