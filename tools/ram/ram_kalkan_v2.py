r"""RAM kalkani v2 (9 Kas 2026). v1'in iki hatasini kapatir:
  1) v1 olunce askiya aldigi surecler sonsuza dek askida kaliyordu > v2 her acilista once askidakileri KADEMELI acar,
     kapanirken (finally + atexit + SIGBREAK) yine kademeli acar; pid kilidiyle tek kopya kosar.
  2) v1 45 sureci ayni anda devam ettirdi, RAM firladi, Desktop dondu > v2 surec agaclarini birer birer, RAM'e bakarak acar.
Borsa (Omer 8 Kas): normalde tam hiz; RAM %94'te durmaz ama ciddi yavaslar (3 turun 2'si askida); %85 altinda eski hiza doner.
Kurulum agaclari (claude.exe cocuklari dahil): %89'da yari hiz, %93'te dur, %89 altinda kademeli ac.
  pythonw -I tools/ram/ram_kalkan_v2.py --calis      (arka plan; 12 saat)
  python  -I tools/ram/ram_kalkan_v2.py --baslat     (arka planda calis'i baslatir, tek kopya)
  python  -I tools/ram/ram_kalkan_v2.py --ac         (askidaki hedefleri kademeli acar ve cikar)
  python  -I tools/ram/ram_kalkan_v2.py --durum      (RAM, hedefler, askidakiler, kalkan canli mi)"""
import atexit
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import psutil

KOK = Path(__file__).resolve().parents[2]
LOG = KOK / "rapor" / "ram-kalkan-v2.log"
PID = KOK / ".kos" / "ram-kalkan-v2.pid"

DUSUK = ["borsa egit", "-m borsa", "egit_surekli.py"]
ORTA = ["kurulum_d2", "coz_v2", "kurulum_denetim", "yeniden_cikar", "kaynak_bul", "yeniden_hakem", "ornek_denetim"]
KORUNAN = ["ram_kalkan", "is_sirasi.py", "mcp_paylasim", "mcp-proxy", "headroom", "yonetici_gorev"]

YAVAS, DUR = 89.0, 93.0
BORSA_YAVAS, BORSA_NORMAL = 94.0, 85.0
AC_ESIK = 84.0
AC_ARA = 6
SURE = 12 * 3600


def log(m):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(time.strftime("%H:%M:%S ") + m + "\n")


def ram():
    return psutil.virtual_memory().percent


def cmd(p):
    try:
        return " ".join(p.cmdline())
    except psutil.Error:
        return ""


def kokler(desen):
    out = []
    for p in psutil.process_iter():
        c = cmd(p)
        if any(k in c for k in KORUNAN):
            continue
        if any(d in c for d in desen) and (p.name() or "").lower().startswith("python"):
            try:
                ust = p.parent()
                if ust and (ust.name() or "").lower().startswith("python") and any(d in cmd(ust) for d in desen):
                    continue
            except psutil.Error:
                pass
            out.append(p)
    return out


def agac(p):
    try:
        return [p] + p.children(recursive=True)
    except psutil.Error:
        return []


def durdur(kok):
    n = 0
    for q in reversed(agac(kok)):
        try:
            if q.status() != psutil.STATUS_STOPPED:
                q.suspend(); n += 1
        except psutil.Error:
            pass
    return n


def devam(kok):
    n = 0
    for q in agac(kok):
        try:
            if q.status() == psutil.STATUS_STOPPED:
                q.resume(); n += 1
        except psutil.Error:
            pass
    return n


def askida(kok):
    for q in agac(kok):
        try:
            if q.status() == psutil.STATUS_STOPPED:
                return True
        except psutil.Error:
            pass
    return False


def kademeli_ac(sinir=AC_ESIK, bekle_max=600):
    sira = [k for k in kokler(ORTA) if askida(k)] + [k for k in kokler(DUSUK) if askida(k)]
    acilan = 0
    for k in sira:
        t0 = time.time()
        while ram() >= sinir and time.time() - t0 < bekle_max:
            time.sleep(5)
        n = devam(k)
        acilan += n
        log(f"kademeli ac pid {k.pid} ({n} surec) RAM {ram():.1f}")
        time.sleep(AC_ARA)
    return acilan


def tek_kopya():
    if PID.exists():
        try:
            eski = int(PID.read_text())
            if psutil.pid_exists(eski) and "ram_kalkan_v2" in cmd(psutil.Process(eski)) and eski != os.getpid():
                return False
        except (ValueError, psutil.Error):
            pass
    PID.parent.mkdir(parents=True, exist_ok=True)
    PID.write_text(str(os.getpid()))
    return True


def kapanis(*_):
    try:
        kademeli_ac(sinir=90.0, bekle_max=60)
    finally:
        try:
            if PID.exists() and PID.read_text().strip() == str(os.getpid()):
                PID.unlink()
        except OSError:
            pass
    if _:
        sys.exit(0)


def calis():
    if not tek_kopya():
        return
    atexit.register(kapanis)
    for s in (getattr(signal, "SIGBREAK", None), signal.SIGTERM, signal.SIGINT):
        if s:
            try:
                signal.signal(s, kapanis)
            except (ValueError, OSError):
                pass
    log(f"v2 basladi RAM {ram():.1f}; once askidakiler kademeli aciliyor")
    kademeli_ac()
    durum, borsa_yavas, t0, son, tik = "normal", False, time.time(), 0.0, 0
    while time.time() - t0 < SURE:
        r = ram()
        tik += 1
        yeni = "dur" if r >= DUR else ("yavas" if r >= YAVAS else "normal")
        if durum == "dur" and r >= YAVAS:
            yeni = "dur"
        if yeni != durum:
            log(f"RAM {r:.1f} : kurulum {durum} -> {yeni}")
            if durum in ("dur", "yavas") and yeni == "normal":
                kademeli_ac()
            durum = yeni
        if not borsa_yavas and r >= BORSA_YAVAS:
            borsa_yavas = True
            log(f"RAM {r:.1f} : borsa ciddi yavas (>= {BORSA_YAVAS})")
        elif borsa_yavas and r < BORSA_NORMAL:
            borsa_yavas = False
            log(f"RAM {r:.1f} : borsa eski hizinda (< {BORSA_NORMAL})")
        if time.time() - son > 300:
            log(f"nabiz RAM {r:.1f} kurulum {durum} borsa {'yavas' if borsa_yavas else 'normal'}")
            son = time.time()
        orta = kokler(ORTA)
        if durum == "normal":
            for k in orta:
                devam(k)
        elif durum == "yavas":
            for k in orta:
                (devam if tik % 2 else durdur)(k)
        else:
            for k in orta:
                durdur(k)
        for k in kokler(DUSUK):
            if borsa_yavas and tik % 3:
                durdur(k)
            else:
                devam(k)
        time.sleep(10)
    log("12 saat doldu; kapanis")


def baslat():
    if PID.exists():
        try:
            p = int(PID.read_text())
            if psutil.pid_exists(p) and "ram_kalkan_v2" in cmd(psutil.Process(p)):
                return print("zaten calisiyor pid", p)
        except (ValueError, psutil.Error):
            pass
    pyw = Path(sys.executable).with_name("pythonw.exe")
    exe = str(pyw if pyw.exists() else sys.executable)
    subprocess.Popen([exe, "-I", __file__, "--calis"], creationflags=0x00000008 | 0x00000200 | 0x08000000, close_fds=True)
    print("kalkan v2 basladi, RAM", ram())


def goster():
    print(f"RAM %{ram():.1f}")
    canli = False
    if PID.exists():
        try:
            canli = psutil.pid_exists(int(PID.read_text()))
        except ValueError:
            pass
    print("kalkan canli:", canli)
    for ad, desen in (("dusuk", DUSUK), ("orta", ORTA)):
        for k in kokler(desen):
            mb = sum(q.memory_info().rss for q in agac(k) if q.is_running()) // 2**20
            print(f"{ad:5} pid {k.pid:6} askida={askida(k)!s:5} {mb:5} MB | {cmd(k)[-110:]}")


if __name__ == "__main__":
    kip = (sys.argv[1] if len(sys.argv) > 1 else "durum").lstrip("-")
    {"calis": calis, "baslat": baslat, "ac": lambda: print("acilan", kademeli_ac()), "durum": goster}[kip]()
