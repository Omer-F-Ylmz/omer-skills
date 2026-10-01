"""BLENDER-ARAC-1 K1: headless Blender betik sözleşmesi — sonraki Blender araçları bunun üstünde.

    python tools/blender_cli.py <betik.py> [json] [--blend Desktop\\<Proje>\\blender\\x.blend] [--zaman-asimi 300]

Komut: <mutlak Blender exe> -b [dosya.blend] --python <betik> -- <json>. Betik sonucu tek satır
"SONUC:" + JSON basar. Çıkış: 0 geçti · 1 kapı kaldı ("gecti": false) · 2 kullanım/yol hatası ·
3 Blender/betik çöktü, zaman aşımı (süreç ağacı PID ile kapatılır) ya da SONUC yok.
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import blender_oturum as bo


def proje_ici(yol):
    """Desktop\\<Proje>\\ altında mı (büyük/küçük harf duyarsız, '..' çözülür)."""
    kok = os.path.normcase(os.path.abspath(bo.MASAUSTU)) + os.sep
    y = os.path.normcase(os.path.abspath(yol))
    return y.startswith(kok) and os.sep in y[len(kok):]


def calistir(betik, args=None, blend=None, zaman_asimi=300):
    """(kod, sonuc | None, pid | None) döner."""
    betik = Path(betik)
    if not Path(bo.BLENDER).is_file():
        print(f"Blender exe yok: {bo.BLENDER}", file=sys.stderr)
        return 2, None, None
    if not betik.is_file():
        print(f"betik yok: {betik}", file=sys.stderr)
        return 2, None, None
    if blend and not (bo.yol_gecerli(Path(blend)) and Path(blend).is_file()):
        print(f"yol kuralı: .blend yalnız Desktop\\<Proje>\\blender\\ altında ve var olmalı: {blend}", file=sys.stderr)
        return 2, None, None
    cmd = [bo.BLENDER, "-b", "--factory-startup", *([str(blend)] if blend else []),
           "--python-exit-code", "3", "--python", str(betik), "--", json.dumps(args or {})]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         encoding="utf-8", errors="replace")
    try:
        cikti, _ = p.communicate(timeout=zaman_asimi)
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True)
        p.communicate()
        print(f"zaman aşımı ({zaman_asimi} sn): süreç ağacı PID {p.pid} ile kapatıldı", file=sys.stderr)
        return 3, None, p.pid
    satirlar = [s for s in cikti.splitlines() if s.startswith("SONUC:")]
    try:
        sonuc = json.loads(satirlar[-1][len("SONUC:"):]) if p.returncode == 0 and satirlar else None
    except ValueError:
        sonuc = None
    if sonuc is None:
        print(f"Blender/betik çöktü ya da SONUC yok (exit {p.returncode}):\n{cikti[-2000:]}", file=sys.stderr)
        return 3, None, p.pid
    return (1 if sonuc.get("gecti") is False else 0), sonuc, p.pid


def main(argv=None):
    ap = argparse.ArgumentParser(description="headless Blender betik sözleşmesi")
    ap.add_argument("betik")
    ap.add_argument("json", nargs="?", default="{}")
    ap.add_argument("--blend")
    ap.add_argument("--zaman-asimi", type=int, default=300)
    a = ap.parse_args(argv)
    try:
        args = json.loads(a.json)
    except ValueError:
        print("json argüman çözülemedi", file=sys.stderr)
        return 2
    kod, sonuc, _ = calistir(a.betik, args, a.blend and Path(a.blend), a.zaman_asimi)
    if sonuc is not None:
        print(json.dumps(sonuc, ensure_ascii=False))
    return kod


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
