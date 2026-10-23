"""Yöneticiyi (ajan_sira.py) yeni kodla yeniden başlat: kilitteki PID'i (yalnız o süreç, /T YOK) kapat, Görev Zamanlayıcı'daki "AjanSira" görevini
tetikle (Desktop job'u dışında; kurulum: yonetici_gorev_kur.ps1). Çalışan ajan varsa DEĞİŞTİRMEZ (YÖNETİCİ-BAĞIMSIZ-1 d6): bitmesini bekle, sonra yeniden koş."""
import subprocess, sys, time
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
K = Path(r"C:\Projeler\omer-skills\.kos\kopru")
sys.path.insert(0, str(K))
import ajan_sira

n = ajan_sira.dis_calisan(set())
if n:
    sys.exit(f"{n} ajan çalışıyor · geçiş ertelendi (ajan-sira.log'da açık BAŞLAT yok iken yeniden koş)")
try:
    pid = int((K / "ajan-sira.kilit").read_text(encoding="utf-8").split()[0])
    r = subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True, text=True, errors="replace")
    print("eski yönetici", pid, "kapatıldı" if r.returncode == 0 else r.stderr.strip()[:120])
except (OSError, ValueError, IndexError) as e:
    print("kilit yok:", e)
time.sleep(2)
(K / "ajan-sira.kilit").unlink(missing_ok=True)
r = subprocess.run(["schtasks", "/Run", "/TN", "AjanSira"], capture_output=True, text=True, errors="replace")
print("yeni yönetici (görev):", (r.stdout or r.stderr).strip()[:160])
time.sleep(8)
print("log son:", (K / "ajan-sira.log").read_text(encoding="utf-8", errors="replace").splitlines()[-3:])
print("job testi:", subprocess.run([sys.executable, str(K / "job_uyelik.py")], capture_output=True, text=True, errors="replace").stdout.strip()[:200])
