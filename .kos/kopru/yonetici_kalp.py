"""YONETICI-OLUM-2: yönetici (yonetici_gorev.py) iz bırakmadan ölürse kanıt bırakır.
Kalp atışı dosyası 30 sn'de bir yazılır; temiz çıkışta "cikis" alanı eklenir. Yeni yönetici başlarken önceki kalbi okur:
pid ölü + "cikis" yok = zorla öldürüldü / güç-oturum kesildi; boot zamanı değişmişse makine yeniden başlamış."""
import atexit, ctypes, faulthandler, json, os, sys, threading, time, traceback
from pathlib import Path


def boot_zamani():
    ctypes.windll.kernel32.GetTickCount64.restype = ctypes.c_ulonglong
    return int(time.time() - ctypes.windll.kernel32.GetTickCount64() / 1000)


def _canli(pid):
    h = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return False
    kod = ctypes.c_ulong()
    ok = ctypes.windll.kernel32.GetExitCodeProcess(h, ctypes.byref(kod))
    ctypes.windll.kernel32.CloseHandle(h)
    return bool(ok) and kod.value == 259


def kalp_yaz(yol, ram, calisan, son_olay, cikis=None):
    d = {"pid": os.getpid(), "saat": time.strftime("%H:%M:%S"), "boot": boot_zamani(), "ram": ram, "calisan": calisan, "son_olay": son_olay}
    if cikis:
        d["cikis"] = cikis
    Path(yol).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def onceki_olum(yol):
    """Önceki yöneticinin ölüm özeti; dosya yok / önceki hâlâ canlı ise None."""
    try:
        d = json.loads(Path(yol).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if d.get("pid") == os.getpid() or _canli(d.get("pid", 0)):
        return None
    ozet = f"önceki yönetici pid {d.get('pid')} son kalp {d.get('saat')} RAM %{d.get('ram')} çalışan {d.get('calisan')} son olay {d.get('son_olay')!r}"
    if d.get("cikis"):
        return f"{ozet} · çıkış: {d['cikis']}"
    if abs(d.get("boot", 0) - boot_zamani()) > 120:
        return f"{ozet} · makine yeniden başlatma (boot değişti), çıkış izi yok"
    return f"{ozet} · çıkış izi yok (zorla sonlandırma / oturum kesilmesi)"


def kur(klasor, log_yolu, ram_fn, sure=30):
    """excepthook + atexit + faulthandler + kalp atışı iş parçacığı. Dönüş: önceki ölüm özeti (ya da None)."""
    klasor = Path(klasor)
    kalp = klasor / "yonetici-kalp.txt"
    olum = onceki_olum(kalp)
    if olum:
        with open(klasor / "yonetici-olum.log", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%d.%m %H:%M:%S')} {olum}\n")
    son = {"cikis": None}

    def son_olay():
        try:
            with open(log_yolu, "rb") as f:
                f.seek(0, 2)
                f.seek(max(0, f.tell() - 400))
                return f.read().decode("utf-8", "replace").strip().splitlines()[-1][:120]
        except (OSError, IndexError):
            return ""

    def yaz(cikis=None):
        try:
            import psutil
            cocuk = len(psutil.Process().children())
            kalp_yaz(kalp, ram_fn(), cocuk, son_olay(), cikis or son["cikis"])
        except Exception:
            pass

    def kanca(tip, deger, tb):
        son["cikis"] = f"istisna {tip.__name__}: {deger}"
        print(time.strftime("%H:%M:%S"), "YÖNETİCİ İSTİSNA", "".join(traceback.format_exception(tip, deger, tb)), flush=True)
        yaz()

    sys.excepthook = kanca
    atexit.register(lambda: (print(time.strftime("%H:%M:%S"), "YÖNETİCİ ÇIKIŞ (atexit)", flush=True), yaz(son["cikis"] or "atexit")))
    faulthandler.enable(open(klasor / "yonetici-fault.txt", "a", encoding="utf-8"), all_threads=True)

    def dongu():
        while True:
            yaz()
            time.sleep(sure)

    threading.Thread(target=dongu, daemon=True).start()
    return olum
