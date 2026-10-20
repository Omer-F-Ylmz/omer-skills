"""UCRETSIZ-HAVUZ-2: video koşusunu (video764_kos.py kos 50) parti sınırında yeni kodla yeniden başlatır; kaldığı yerden devam eder
(sirada() = ozet.txt'si olmayan videolar, ilerleme diskte). Varsayılan: yalnız plan basar. Çalıştırmayı Desktop onaylar.
python video764_yenile.py            # plan: pid, parti sayısı, ne yapılacak
python video764_yenile.py --uygula   # bir sonraki parti satırı video-764-parti.tsv'ye yazılınca eski süreci durdurur, yenisini arka.py ile başlatır
Parti sınırı = PARTI satır sayısının artması (parti sonu kararla() bittikten sonra); sınırda bir sonraki parti en fazla birkaç sn önce başlamış olur,
yarım kalan videolar sirada()'da kaldığı için yeniden işlenir (kayıp yok)."""
import subprocess, sys, time
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
PARTI = KOK / ".kos/kopru/ogren/video-764-parti.tsv"
KOMUT = "video764_kos.py kos"
LOG = ".kos/kopru/ogren/video764-yenile.log"
NW = 0x08000000


def ps(komut):
    return subprocess.run(["powershell", "-NoProfile", "-Command", komut], capture_output=True, text=True, creationflags=NW).stdout.strip()


def eski():
    """video764_kos.py kos çalıştıran süreçler (pid, komut satırı, n)."""
    s = ps("Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | ForEach-Object { \"$($_.ProcessId)`t$($_.CommandLine)\" }")
    return [(int(p), c, c.split()[-1]) for p, c in (x.split("\t", 1) for x in s.splitlines() if "\t" in x) if KOMUT in c]


def satir():
    return len(PARTI.read_text(encoding="utf-8").splitlines()) if PARTI.is_file() else 0


if __name__ == "__main__":
    sureclar = eski()
    print("koşan:", [(p, n) for p, _, n in sureclar], "· parti satırı:", satir())
    if "--uygula" not in sys.argv:
        print("plan: parti satırı artınca bu süreçler durdurulur, 'video764_kos.py kos <n>' arka.py ile yeniden başlar. --uygula ile çalıştır.")
        raise SystemExit
    if not sureclar:
        raise SystemExit("koşan video764_kos.py kos yok; yeniden başlatılacak bir şey yok")
    n0 = satir()
    while satir() == n0:
        time.sleep(2)
    for p, _, _ in sureclar:
        ps(f"Stop-Process -Id {p} -Force")
    n = sureclar[0][2]
    print(subprocess.run([sys.executable, str(KOK / ".kos/kopru/arka.py"), LOG, ".kos/kopru/video764_kos.py", "kos", n],
                         capture_output=True, text=True, creationflags=NW).stdout.strip())
