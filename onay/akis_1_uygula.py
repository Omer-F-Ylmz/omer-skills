"""AJAN-AKIS-1 onay betiği: skills/{opus-akis,fable-dusunme} → ~/.claude/skills (eski sürüm ~/.claude/skills-yedek/'e) + haiku|sonnet ajan profillerine çekirdek bloğu.
Opus profillerine dokunmaz. claude.ai tarafı: dist/opus-akis.zip + dist/fable-dusunme.zip (yükleme Ömer'de).
Kullanım: python onay/akis_1_uygula.py [--geri]   (geri: skill yedeklerini döner; ajan blokları <!-- ajan-cekirdek --> işaretiyle elle çıkarılır)"""
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SK = Path.home() / ".claude/skills"
YEDEK = Path.home() / ".claude/skills-yedek"
AD = ("opus-akis", "fable-dusunme")


def uygula():
    YEDEK.mkdir(exist_ok=True)
    for a in AD:
        if (SK / a).exists():
            shutil.move(str(SK / a), str(YEDEK / f"{a}.akis1"))
        shutil.copytree(KOK / "skills" / a, SK / a)
        print("kuruldu:", SK / a)
    subprocess.run([sys.executable, "-I", str(KOK / "tools/ajan_cekirdek_bagla.py"), "--uygula"], check=True)


def geri():
    for a in AD:
        y = YEDEK / f"{a}.akis1"
        if (SK / a).exists():
            shutil.rmtree(SK / a)
        if y.exists():
            shutil.move(str(y), str(SK / a))
        print("geri alındı:", a)


if __name__ == "__main__":
    geri() if "--geri" in sys.argv else uygula()
