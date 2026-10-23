"""ARKA-BEKCI-1: arka.py ile başlayan işleri izler; sessiz ölümü ve askıyı yakalar (Claude yok, $0).
  python tools/arka_bekci.py [--tek]     tek tarama (varsayılan; Görev Zamanlayıcı her 2 dk çağırır)
  python tools/arka_bekci.py --dongu     2 dk'da bir sonsuz tarama
  python tools/arka_bekci.py --kur       "omer-arka-bekci" zamanlanmış görevini kurar (pythonw, pencere yok)
  python tools/arka_bekci.py --durum     kayıttaki işler
  python tools/arka_bekci.py ekle <ad> <pid|-> <günlük> <betik> [bitiş-regex] [--bitti]   çalışan/bitmiş işi kayda ekler
Kayıt: .kos/kopru/arka-kayit.json (arka.py yazar). Ölü + günlükte bitiş işareti yok → beyne hata + beyin-alarm.txt (ajan-sira alarm kanalı);
kayıtta yeniden=true ise arka.py --bagimsiz ile 1 kez yeniden başlatır. Canlı ama günlük ASKI_DK dk yazılmıyorsa "askıda" uyarısı.
Yollar ARKA_KOPRU / ARKA_KAYIT ortam değişkeniyle değiştirilebilir (test)."""
import ctypes
import json
import os
import re
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
KOP = Path(os.environ.get("ARKA_KOPRU") or KOK / ".kos" / "kopru")
KAYIT = Path(os.environ.get("ARKA_KAYIT") or KOP / "arka-kayit.json")
ALARM, OLAY = KOP / "beyin-alarm.txt", KOP / "beyin-olay.jsonl"
ARKA = KOK / ".kos" / "kopru" / "arka.py"
ASKI_DK = 20
BASLANGIC_TOLERANS = 120  # sn: sarmalayıcı/pid kayıt anından bu kadar sonra doğmuş olabilir; daha geç doğmuş pid = yeniden kullanılmış
PENCERE_YOK = 0x08000000
GOREV = "omer-arka-bekci"


def olusturma(pid):
    """Süreç yaratılış zamanı (epoch); süreç yok → None; erişim reddi → 0.0 (canlı say)."""
    k32 = ctypes.windll.kernel32
    k32.OpenProcess.restype = wintypes.HANDLE
    h = k32.OpenProcess(0x1000, False, int(pid))
    if not h:
        return 0.0 if ctypes.GetLastError() == 5 else None
    try:
        ft = [wintypes.FILETIME() for _ in range(4)]
        kod = wintypes.DWORD()
        k32.GetExitCodeProcess(h, ctypes.byref(kod))
        if kod.value != 259:  # STILL_ACTIVE
            return None
        k32.GetProcessTimes(h, *(ctypes.byref(f) for f in ft))
        return ((ft[0].dwHighDateTime << 32 | ft[0].dwLowDateTime) - 116444736000000000) / 1e7
    finally:
        k32.CloseHandle(h)


def sarmalayici_pid(ad):
    """--bagimsiz işin pythonw sarmalayıcısı (`arka.py --ic <ad>`); yoksa None."""
    ps = f"(Get-CimInstance Win32_Process -Filter \"CommandLine like '%--ic {ad}%'\" | Select -First 1).ProcessId"
    c = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, creationflags=PENCERE_YOK).stdout.strip()
    return int(c) if c.isdigit() else None


def oku():
    try:
        return json.loads(KAYIT.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def yaz(k):
    tmp = KAYIT.with_name(KAYIT.name + f".{os.getpid()}.tmp")
    tmp.write_text(json.dumps(k, ensure_ascii=False, indent=1), encoding="utf-8", newline="\n")
    os.replace(tmp, KAYIT)


def beyne_hata(ozet):
    s = json.dumps({"t": round(time.time(), 1), "tur": "hata", "arac": "arka-bekci", "ozet": ozet[:200], "hata": True, "kaynak": "bekci"}, ensure_ascii=False)
    with OLAY.open("ab") as f:
        f.write((s + "\n").encode("utf-8"))


def alarm(ozet):
    with ALARM.open("ab") as f:
        f.write(f"{time.strftime('%d %H:%M')} ARKA-BEKCI: {ozet}\n".encode("utf-8"))
    beyne_hata("ARKA-BEKCI " + ozet)


def bitti_mi(e):
    try:
        with open(e["gunluk"], "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 8192))
            return re.search(e.get("bitis") or "BITTI|BITIS", f.read().decode("utf-8", "replace")) is not None
    except OSError:
        return False


def yeniden_baslat(ad, e):
    bayrak = ["--bitis", e["bitis"]] if e.get("bitis") else []
    py = Path(sys.executable).with_name("python.exe")
    r = subprocess.run([str(py if py.is_file() else sys.executable), str(ARKA), "--bagimsiz", "--cwd", e["cwd"], *bayrak, *e["arg"]],
                       capture_output=True, text=True, errors="replace", creationflags=PENCERE_YOK)
    return r.returncode == 0, (r.stdout + r.stderr).strip()[:120]


def tara(simdi=None, aski_dk=ASKI_DK):
    """Her 'calisiyor' kaydı denetler; olay listesi döner: (ad, 'bitti'|'oldu'|'yeniden'|'askida')."""
    simdi = simdi or time.time()
    k, olaylar = oku(), []
    for ad, e in k.items():
        if e.get("durum") != "calisiyor":
            continue
        if not e.get("pid"):
            e["pid"] = sarmalayici_pid(ad) if e.get("bagimsiz") else None
        yas = simdi - e["basladi"]
        dogum = olusturma(e["pid"]) if e.get("pid") else None
        canli = dogum is not None and (dogum == 0.0 or dogum <= e["basladi"] + BASLANGIC_TOLERANS)
        if not e.get("pid") and e.get("bagimsiz") and yas < 90:
            continue  # görev henüz başlamadı
        if canli:
            try:
                son = int(os.path.getmtime(e["gunluk"]))
            except OSError:
                son = int(e["basladi"])
            sessiz = (simdi - son) / 60
            if sessiz >= aski_dk and e.get("askida") != son:  # aynı sessizlik için bir kez uyar
                e["askida"] = son
                alarm(f"{ad} askıda: {Path(e['betik']).name} günlüğü {sessiz:.0f} dk yazılmadı, pid {e['pid']} canlı")
                olaylar.append((ad, "askida"))
            continue
        if bitti_mi(e):
            e["durum"] = "bitti"
            olaylar.append((ad, "bitti"))
            continue
        e["durum"] = "oldu"
        alarm(f"{ad} bitiş işareti yazmadan öldü: {Path(e['betik']).name} (pid {e.get('pid')}, günlük {e['gunluk']})")
        olaylar.append((ad, "oldu"))
        if e.get("yeniden") and not e.get("yeniden_say"):
            e["yeniden_say"] = 1
            ok, cikti = yeniden_baslat(ad, e)
            beyne_hata(f"ARKA-BEKCI {ad} yeniden başlatıldı: {'tamam' if ok else 'DÜŞTÜ'} {cikti}")
            olaylar.append((ad, "yeniden" if ok else "yeniden-dustu"))
    # yeniden başlatma arka.py üzerinden kayıt dosyasına yeni giriş ekledi; eski durum yazımı onu ezmesin
    taze = oku()
    for ad, e in k.items():
        taze[ad] = e
    yaz(taze)
    return olaylar


def ekle(ad, pid, gunluk, betik, bitis="BITTI|BITIS", bitti=False):
    k = oku()
    pid = int(pid) if pid != "-" else None
    k[ad] = {"betik": str(betik), "gunluk": str(Path(gunluk).resolve()), "pid": pid, "basladi": (pid and olusturma(pid)) or time.time(),
             "bitis": bitis, "yeniden": False, "cwd": str(KOK), "arg": [str(gunluk), str(betik)], "bagimsiz": False,
             "durum": "bitti" if bitti else "calisiyor"}
    yaz(k)


def kur():
    pw = Path(sys.executable).with_name("pythonw.exe")
    tr = subprocess.list2cmdline([str(pw), str(Path(__file__).resolve()), "--tek"])
    r = subprocess.run(["schtasks", "/create", "/tn", GOREV, "/sc", "minute", "/mo", "2", "/f", "/tr", tr],
                       capture_output=True, text=True, errors="replace", creationflags=PENCERE_YOK)
    return r.stdout.strip() + r.stderr.strip()


def main(argv):
    if argv[:1] == ["ekle"]:
        ekle(*[a for a in argv[1:] if a != "--bitti"], bitti="--bitti" in argv)
    elif argv[:1] == ["--kur"]:
        print(kur())
    elif argv[:1] == ["--durum"]:
        for ad, e in oku().items():
            print(ad, e["durum"], e.get("pid"), Path(e["betik"]).name)
    elif argv[:1] == ["--dongu"]:
        while True:
            tara()
            time.sleep(120)
    else:
        print(tara() or "olay yok")


if __name__ == "__main__":
    main(sys.argv[1:])
