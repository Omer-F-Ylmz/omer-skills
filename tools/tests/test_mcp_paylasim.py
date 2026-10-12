import subprocess
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mcp_paylasim as mp  # noqa: E402


def test_bekci_asili_proxyyi_oldurur(tmp_path, monkeypatch):
    # 12 Eki 18:42: proxy süreci canlı ama port kapalı; bekçi p.wait()'te sonsuza dek bekledi, 21 MCP "failed" kaldı
    gercek = subprocess.Popen
    monkeypatch.setattr(mp.subprocess, "Popen", lambda a, **k: gercek(  # yalnız proxy komutu; taskkill gerçek
        [sys.executable, "-c", "import time; time.sleep(120)"], creationflags=0x08000000)
        if a[0] == str(mp.PROXY) else gercek(a, **k))
    uyu = mp.time.sleep
    monkeypatch.setattr(mp.time, "sleep", lambda s: uyu(0.01))
    monkeypatch.setattr(mp, "ayakta", lambda port: False)  # Windows'ta kapalı porta bağlanma ≈2 sn sürer
    cfg = tmp_path / "sunucular.json"
    cfg.write_text("{}")
    t = threading.Thread(target=mp.bekci, args=(str(cfg), 1, 1), daemon=True)  # port 1: dinleyen yok
    t.start()
    t.join(30)
    assert not t.is_alive()
