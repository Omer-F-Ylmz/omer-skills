import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
import mcp_hafif_kabul as k  # noqa: E402


def test_torunlar_pid_dongusunde_biter():
    """Windows PID yeniden kullanımı ebeveyn döngüsü yaratır (ölü ebeveynin PID'i torununa verilir): 10→20→30→20.
    Ziyaret kümesi yoksa yığın sonsuz büyür (18:22 KABUL 15.4 GB). Bellek tavanı: çıktı ≤ süreç sayısı."""
    d = {10: (1, "claude.exe", 0), 20: (30, "bash.exe", 0), 30: (20, "bash.exe", 0), 40: (40, "x", 0)}
    d[20] = (10, "bash.exe", 0)
    d[50] = (30, "bash.exe", 0)
    d[20] = (50, "bash.exe", 0)  # 20→50→30→20 döngü; 20 ayrıca 10'un çocuğu sayılsın diye ikinci kayıt yok → 10 kökünden erişilemez
    d[60] = (10, "node.exe", 0)
    d[30] = (60, "bash.exe", 0)  # 10→60→30→20→50→30 ...
    sonuc = []
    t = threading.Thread(target=lambda: sonuc.append(k.torunlar(d, 10)), daemon=True)
    t.start()
    t.join(3)
    assert not t.is_alive(), "torunlar döngüde takıldı"
    assert sorted(sonuc[0]) == [20, 30, 50, 60]
    assert len(k.torunlar(d, 40)) <= len(d)  # öz-ebeveyn (pp == pid)
