"""BLENDER-ARAC-2 K1: GPU kilidi — GPU'yu kullanan iki iş aynı anda koşmaz.

    python tools/gpu_kilit.py durum | al <is> --pid N | birak <is>

%TEMP%\\gpu-kilit.json {pid, is, baslangic}; sahibi ölü PID ise kilit kendiliğinden düşer.
Aynı iş yeniden girebilir (gorsel_uret ac → ComfyUI PID'ine devir). Çıkış: 0 tamam · 2 kilit başka işte.
"""
import argparse
import ctypes
import json
import os
import sys
import tempfile
import time
from pathlib import Path

YOL = Path(tempfile.gettempdir()) / "gpu-kilit.json"


def canli(pid):
    # os.kill(pid, 0) Windows'ta süreci sonlandırır; yalnız sorgu hakkıyla açılır
    k = ctypes.windll.kernel32
    h = k.OpenProcess(0x1000, False, int(pid))  # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        return False
    kod = ctypes.c_ulong()
    k.GetExitCodeProcess(h, ctypes.byref(kod))
    k.CloseHandle(h)
    return kod.value == 259  # STILL_ACTIVE


def durum():
    try:
        k = json.loads(YOL.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not canli(k.get("pid", 0)):
        YOL.unlink(missing_ok=True)
        return None
    return k


def al(is_, pid):
    """None: alındı · str: 'GPU şu işte: <is> (PID n)'."""
    k = durum()
    if k and k["is"] != is_:
        return f"GPU şu işte: {k['is']} (PID {k['pid']})"
    veri = json.dumps({"pid": int(pid), "is": is_, "baslangic": time.time()})
    if k:
        YOL.write_text(veri, encoding="utf-8")
        return None
    try:
        fd = os.open(YOL, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:  # arada başka iş aldı
        return al(is_, pid)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(veri)
    return None


def birak(is_):
    k = durum()
    if k and k["is"] == is_:
        YOL.unlink(missing_ok=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="GPU kilidi (al/birak/durum)")
    alt = ap.add_subparsers(dest="komut", required=True)
    alt.add_parser("durum")
    p = alt.add_parser("al")
    p.add_argument("is_", metavar="is")
    p.add_argument("--pid", type=int, required=True)
    alt.add_parser("birak").add_argument("is_", metavar="is")
    a = ap.parse_args(argv)
    if a.komut == "durum":
        k = durum()
        print(json.dumps(k, ensure_ascii=False) if k else "boş")
        return 0
    if a.komut == "birak":
        birak(a.is_)
        print("bırakıldı")
        return 0
    m = al(a.is_, a.pid)
    print(m or f"alındı: {a.is_} (PID {a.pid})")
    return 2 if m else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
