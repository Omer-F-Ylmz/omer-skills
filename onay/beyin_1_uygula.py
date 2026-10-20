"""BEYIN-1 onay betiği (Ömer koşar): skills/beyin → ~/.claude/skills/beyin.
Desktop: cc-kopru allowlist'inde `python` (dosyaGerek, -c yasak) zaten açık → `python tools/beyin.py ara` değişiksiz geçer.
Öneri (uygulanmaz, Ömer karar verir): görev diyeti `python tools/beyin_diyet.py .kos/kopru/gorev/<ad>.md --uygula`.
Kullanım: python onay/beyin_1_uygula.py [--geri]
"""
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HEDEF = Path.home() / ".claude/skills/beyin"


def uygula():
    if HEDEF.exists():
        shutil.move(str(HEDEF), str(HEDEF) + ".bak-beyin1")  # silinmez, yedeklenir
    shutil.copytree(KOK / "skills/beyin", HEDEF)
    print("kuruldu:", HEDEF)


def geri():
    yedek = Path(str(HEDEF) + ".bak-beyin1")
    if HEDEF.exists():
        shutil.move(str(HEDEF), str(HEDEF) + ".geri-beyin1")
    if yedek.exists():
        shutil.move(str(yedek), str(HEDEF))
    print("geri alındı:", HEDEF)


if __name__ == "__main__":
    geri() if "--geri" in sys.argv else uygula()
