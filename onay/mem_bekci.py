"""claude-mem bekçisi zamanlanmış görevi — Ömer koşar.
python onay/mem_bekci.py --kuru   # plan (varsayılan; hiçbir şey yazmaz)
python onay/mem_bekci.py uygula   # "omer-claude-mem-bekci" görevi: oturum açılışında + her 5 dk, pythonw ile (pencere yok)
python onay/mem_bekci.py --geri   # görevi siler
Bekçi yalnız worker kapalıysa başlatır; açıkken hiçbir şey yapmaz. Ayar/plugin dosyasına dokunmaz."""
import os
import subprocess
import sys

AD = "omer-claude-mem-bekci"
PYW = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
BETIK = r"C:\Projeler\omer-skills\tools\mem_bekci.py"
TR = f'"{PYW}" "{BETIK}"'


def var():
    return subprocess.run(["schtasks", "/Query", "/TN", AD], capture_output=True).returncode == 0


kip = sys.argv[1] if len(sys.argv) > 1 else "--kuru"
if kip == "--kuru":
    print(f"görev {AD}: {'VAR' if var() else 'yok'}")
    print(f"uygula: schtasks /Create /TN {AD} /SC MINUTE /MO 5 /TR {TR} /F  (+ ONLOGON tetikleyicisi)")
    print(f"pythonw mevcut: {os.path.exists(PYW)} · betik mevcut: {os.path.exists(BETIK)}")
elif kip == "uygula":
    if not os.path.exists(PYW):
        sys.exit("pythonw.exe yok: " + PYW)
    r1 = subprocess.run(["schtasks", "/Create", "/TN", AD, "/SC", "MINUTE", "/MO", "5", "/TR", TR, "/F"], capture_output=True, text=True)
    r2 = subprocess.run(["schtasks", "/Create", "/TN", AD + "-acilis", "/SC", "ONLOGON", "/TR", TR, "/F"], capture_output=True, text=True)
    print(r1.stdout.strip() or r1.stderr.strip())
    print(r2.stdout.strip() or r2.stderr.strip())
    subprocess.Popen([PYW, BETIK])
elif kip == "--geri":
    for ad in (AD, AD + "-acilis"):
        r = subprocess.run(["schtasks", "/Delete", "/TN", ad, "/F"], capture_output=True, text=True)
        print(ad, r.stdout.strip() or r.stderr.strip())
else:
    sys.exit("kip: --kuru | uygula | --geri")
