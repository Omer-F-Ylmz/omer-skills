import os
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
import mcp_hafif_kabul as k  # noqa: E402


def test_torunlar_pid_yeniden_kullanim_dongusunde_biter():
    """12 Eki 18:22 / 19:28 (15.4 GB / 37 GB): arka.py çıkınca olcum_sira'nın ppid'i (ölü PID) claude ağacındaki yeni bir
    bash'e verildi → claude → bash(999) → olcum_sira → ben → claude döngüsü; yığın sınırsız büyüdü, sonuc().join() hiç dönmedi."""
    ben = os.getpid()
    d = {500: (999, "python.exe", 0), ben: (500, "python.exe", 0), 700: (ben, "claude.exe", 0),
         800: (700, "bash.exe", 0), 999: (800, "bash.exe", 0), 801: (700, "node.exe", 0)}
    sonuc = []
    t = threading.Thread(target=lambda: sonuc.append(k.torunlar(d, 700)), daemon=True)
    t.start()
    t.join(3)
    assert not t.is_alive(), "torunlar döngüde takıldı"
    assert len(sonuc[0]) <= len(d) and ben not in sonuc[0] and 700 not in sonuc[0]
    assert {800, 801, 999} <= set(sonuc[0])
