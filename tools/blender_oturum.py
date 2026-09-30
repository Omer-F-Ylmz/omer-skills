"""Blender oturumu: ac <.blend> [--yeni] · kapat · durum (BLENDER-OTURUM).

Çıkış: 0 tamam · 1 açılamadı/kapanamadı (süreç yalnız PID ile kapatılır) · 2 kural ihlali, hiçbir şey başlatılmadı.
Kurallar: dosya yalnız <Masaüstü>\\<Proje>\\blender\\ altında; sunucu yalnız 127.0.0.1:9876; eklenti tercihi değiştirilmez.
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MASAUSTU = Path.home() / "Desktop"
DURUM = Path(tempfile.gettempdir()) / "blender-oturum.json"
SONUC = Path(tempfile.gettempdir()) / "blender-oturum-sonuc.json"
BETIK = Path(tempfile.gettempdir()) / "blender-oturum-baslat.py"
BLENDER = r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
HOST, PORT = "127.0.0.1", 9876
ACILIS_SN, KAPANIS_SN = 30, 15

# Blender içinde koşar: argv "--" sonrası <sonuc.json> <yeni_yol|"">.
BASLAT = '''import bpy, json, sys
sonuc, yeni = sys.argv[sys.argv.index("--") + 1:][:2]

def adim():
    kayit = {}
    try:
        if yeni:
            for o in list(bpy.data.objects):
                bpy.data.objects.remove(o)
            bpy.ops.wm.save_as_mainfile(filepath=yeni)
        prefs = bpy.context.preferences.addons["bl_ext.user_default.mcp"].preferences
        kayit = {"host": prefs.host, "port": prefs.port}
        if prefs.host == "127.0.0.1" and prefs.port == 9876:
            kayit["baslat"] = sorted(bpy.ops.blmcp.server_start())
    except Exception as ex:
        kayit["hata"] = str(ex)
    with open(sonuc, "w", encoding="utf-8") as f:
        json.dump(kayit, f)

bpy.app.timers.register(adim, first_interval=1.0)
'''


def yol_gecerli(yol):
    try:
        parca = yol.resolve().relative_to(MASAUSTU.resolve()).parts
    except ValueError:
        return False
    return len(parca) >= 3 and parca[1].lower() == "blender" and yol.suffix.lower() == ".blend"


def dinleyenler():
    cikti = subprocess.run(["netstat", "-ano", "-p", "TCP"], capture_output=True, text=True, errors="replace").stdout
    cikti += subprocess.run(["netstat", "-ano", "-p", "TCPv6"], capture_output=True, text=True, errors="replace").stdout
    return [(p[1], int(p[4])) for p in (s.split() for s in cikti.splitlines())
            if len(p) == 5 and p[0] == "TCP" and p[1].endswith(f":{PORT}") and p[2].endswith(":0")]


def pid_canli(pid):
    cikti = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True, errors="replace").stdout
    return "blender.exe" in cikti.lower() and str(pid) in cikti


def oldur(pid):
    # Yalnız PID ile; ad ile öldürme bu araçta yok.
    if pid_canli(pid):
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, text=True, errors="replace")


def ac(yol, yeni):
    yol = Path(yol)
    if not yol_gecerli(yol):
        print(f"DUR: {yol} <Proje>\\blender\\ altında bir .blend değil")
        return 2
    if yeni and yol.exists():
        print(f"DUR: {yol} zaten var; --yeni üzerine yazmaz")
        return 2
    if not yeni and not yol.is_file():
        print(f"DUR: {yol} yok (oluşturmak için --yeni)")
        return 2
    if dinleyenler():
        print(f"DUR: {PORT} zaten dinleniyor; başka oturum Blender'ı sürüyor olabilir")
        return 2
    SONUC.unlink(missing_ok=True)
    BETIK.write_text(BASLAT, encoding="utf-8")
    if yeni:
        yol.parent.mkdir(parents=True, exist_ok=True)
    komut = [BLENDER] + ([] if yeni else [str(yol)]) + ["--python", str(BETIK), "--", str(SONUC), str(yol) if yeni else ""]
    baslangic = time.time()
    pid = subprocess.Popen(komut, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP).pid
    for _ in range(ACILIS_SN):
        time.sleep(1)
        d = dinleyenler()
        if any(adres.rsplit(":", 1)[0] != HOST for adres, _ in d):
            oldur(pid)
            print(f"DUR: {HOST} dışı dinleme {d}; süreç PID {pid} kapatıldı")
            return 1
        s = json.loads(SONUC.read_text(encoding="utf-8")) if SONUC.exists() else {}
        if s and (s.get("host") != HOST or s.get("port") != PORT):
            oldur(pid)
            print(f"DUR: eklenti tercihi {s.get('host')}:{s.get('port')} ({HOST}:{PORT} değil); tercih değiştirilmedi, süreç kapatıldı")
            return 2
        if "hata" in s:
            oldur(pid)
            print(f"DUR: açılış betiği hatası: {s['hata']}; süreç kapatıldı")
            return 1
        if d and all(p == pid for _, p in d):
            DURUM.write_text(json.dumps({"pid": pid, "dosya": str(yol), "baslangic": baslangic}), encoding="utf-8")
            print(f"açık: {yol} · PID {pid} · {HOST}:{PORT} · {time.time() - baslangic:.0f} sn")
            return 0
    oldur(pid)
    print(f"DUR: {ACILIS_SN} sn içinde {HOST}:{PORT} dinlenmedi; süreç kapatıldı")
    return 1


def kapat():
    if not DURUM.exists():
        print("zaten kapalı")
        return 0
    d = json.loads(DURUM.read_text(encoding="utf-8"))
    pid = d["pid"]
    for _ in range(KAPANIS_SN):
        if not pid_canli(pid) and not dinleyenler():
            DURUM.unlink()
            print(f"kapandı: PID {pid} yok, {PORT} kapalı")
            return 0
        time.sleep(1)
    dosya = Path(d["dosya"])
    if not dosya.exists() or dosya.stat().st_mtime < d["baslangic"]:
        print(f"DUR: {dosya} bu oturumda kaydedilmemiş; zorla kapatma yapılmadı")
        return 1
    oldur(pid)
    DURUM.unlink()
    print(f"zorla kapatıldı: PID {pid}")
    return 0


def durum():
    d = json.loads(DURUM.read_text(encoding="utf-8")) if DURUM.exists() else {}
    pid = d.get("pid")
    sure = int(time.time() - d["baslangic"]) if d else 0
    print(f"port {PORT}: {dinleyenler() or 'kapalı'} · PID {pid} {'canlı' if pid and pid_canli(pid) else 'yok'}"
          f" · dosya {d.get('dosya', '-')} · süre {sure} sn")
    return 0


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(prog="blender_oturum")
    alt = ap.add_subparsers(dest="komut", required=True)
    a = alt.add_parser("ac")
    a.add_argument("yol")
    a.add_argument("--yeni", action="store_true")
    alt.add_parser("kapat")
    alt.add_parser("durum")
    g = ap.parse_args(argv)
    if g.komut == "ac":
        return ac(g.yol, g.yeni)
    return kapat() if g.komut == "kapat" else durum()


if __name__ == "__main__":
    sys.exit(main())
