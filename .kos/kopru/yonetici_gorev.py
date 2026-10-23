"""Görev Zamanlayıcı girişi (YÖNETİCİ-BAĞIMSIZ-1 d2): pythonw ile, Desktop job'u DIŞINDA yöneticiyi (ajan_sira.main) koşar.
pythonw'nin konsolu/stdout'u yok → çıktı günlüğe, alt süreçler pencere açmasın diye CREATE_NO_WINDOW. Tek kopya kilidi ajan_sira.kilit_al'da."""
import os, subprocess, sys
from pathlib import Path

K = Path(__file__).resolve().parent
os.chdir(K.parent.parent)
sys.path.insert(0, str(K))
sys.stdout = sys.stderr = open(K / "ajan-sira.log", "a", encoding="utf-8", buffering=1)
_init = subprocess.Popen.__init__


def _gizli(self, *a, **k):
    k["creationflags"] = k.get("creationflags", 0) | 0x08000000
    _init(self, *a, **k)


subprocess.Popen.__init__ = _gizli
import ajan_sira

try:  # 10 dk'lık bekçi turu: canlı yönetici varsa günlüğü kirletmeden çık
    eski = int(ajan_sira.KILIT.read_text(encoding="utf-8").split()[0])
except (OSError, ValueError, IndexError):
    eski = 0
if eski and eski != os.getpid() and ajan_sira.ajan_sira_canli(eski):
    sys.exit(0)
ajan_sira.main()
