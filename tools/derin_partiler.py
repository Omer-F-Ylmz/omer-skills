"""DERIN-TAMAMLA parça koşucusu: derin-liste.txt'i 10 linklik partilerle bitirir (python arka.py ile koşulur).
Her partiden sonra ilerleme dosyasına satır yazar; .kos/kopru/derin-dur varsa durur; parti 0 yeni iş işlerse durur (kalan = erişilemeyenler)."""
import os, subprocess, sys, time
from datetime import datetime
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
GPU_PY = KOK / ".kos/kopru/venv-ocr/Scripts/python.exe"
LISTE = KOK / ".kos/kopru/derin-liste.txt"
ILERLEME = KOK / ".kos/kopru/derin-parti-ilerleme.txt"
DUR = KOK / ".kos/kopru/derin-dur"
CIKTI = KOK / "docs/video-tarama/derin"
PARTI = 10


def yaz(s):
    with open(ILERLEME, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {s}\n")


def main():
    parti = 0
    while not DUR.exists():
        once = len(list(CIKTI.glob("*.json")))
        r = subprocess.run([str(GPU_PY), str(KOK / "tools/video_derin.py"), "--liste", str(LISTE), "--en", str(PARTI), "--es", "2"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(KOK), env=dict(os.environ), timeout=3600, creationflags=0x08000000)
        sonra = len(list(CIKTI.glob("*.json")))
        parti += 1
        bitis = [s for s in r.stdout.splitlines() if s.startswith("BITIS")]
        yaz(f"parti={parti} rc={r.returncode} json {once}->{sonra} {bitis[-1] if bitis else 'BITIS yok'}")
        if sonra == once and bitis:
            yaz("DURUM bitti-ya-da-ilerleme-yok")
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
