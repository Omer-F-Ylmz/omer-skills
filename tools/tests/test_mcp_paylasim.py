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


def test_onay_yalniz_asili_mcp_proxy_oldurulur():
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "onay"))
    import mcp_hafif_2_uygula as u
    assert u.karar(False, "mcp-proxy.exe")
    assert not u.karar(True, "mcp-proxy.exe")  # port açık → dokunma
    assert not u.karar(False, "python.exe")  # pid yeniden kullanılmış → dokunma
    assert not u.karar(False, None)


def test_bekci_onay_yalniz_bekci_komutunu_tanir():
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "onay"))
    import mcp_hafif_2_bekci as b
    assert b.bizim_bekci(r'"C:\P\pythonw.exe" "C:\Projeler\omer-skills\tools\mcp_paylasim.py" "bekci" "s.json" "47800"')
    assert not b.bizim_bekci(r'"C:\P\python.exe" "C:\x\baska.py"')  # pid yeniden kullanılmış
    assert not b.bizim_bekci("")  # süreç yok
