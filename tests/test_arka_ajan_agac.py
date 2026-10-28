"""ARKA-FIX-1: result sonrası süreç ağacı ~45 sn içinde kapanır; bayat kilit yeniden adlandırılır."""
import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path

ARKA = Path(__file__).resolve().parents[1] / "tools/arka_ajan.py"


def _yukle(kok, monkeypatch):
    monkeypatch.setenv("ARKA_KOK", str(kok))
    s = importlib.util.spec_from_file_location("arka_ajan_t", ARKA)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _sahte(tmp_path):
    # result yazar, sonra torun sürece 120 sn uyutur (ağaç)
    py = tmp_path / "sahte.py"
    py.write_text(
        "import subprocess, sys, time\n"
        "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)'])\n"
        "import json; print(json.dumps({'type': 'result', 'is_error': False, 'session_id': 's1', 'usage': {'input_tokens': 5}}, separators=(',', ':')), flush=True)\n"
        "time.sleep(120)\n", encoding="utf-8")
    cmd = tmp_path / "sahte.cmd"
    cmd.write_text(f'@"{sys.executable}" "{py}" %*\r\n', encoding="utf-8")
    return cmd


def test_result_sonrasi_agac_kapanir(tmp_path, monkeypatch):
    m = _yukle(tmp_path, monkeypatch)
    m.CLAUDE = str(_sahte(tmp_path))
    (tmp_path / "t.json").write_text(json.dumps({"cwd": str(tmp_path), "gorev": "x"}), encoding="utf-8")
    t0 = time.time()
    m.kos("t")
    assert time.time() - t0 < 60
    assert "kod sonuc-sonrasi-kapatildi" in (tmp_path / "t.log").read_text(encoding="utf-8")
    assert json.loads((tmp_path / "t.oturum").read_text(encoding="utf-8"))["temiz"] is True
    assert not (tmp_path / "t.kilit").exists()
    kalan = subprocess.run(["powershell", "-NoProfile", "-Command",
                            "(Get-CimInstance Win32_Process | ? { $_.CommandLine -like '*time.sleep(120)*' -or $_.CommandLine -like '*sahte.py*' }).Count"],
                           capture_output=True, text=True, creationflags=0x08000000).stdout.strip()
    assert kalan in ("", "0")


def test_bayat_kilit_eski_olur(tmp_path, monkeypatch):
    m = _yukle(tmp_path, monkeypatch)
    m.CLAUDE = str(_sahte(tmp_path))
    (tmp_path / "b.json").write_text(json.dumps({"cwd": str(tmp_path), "gorev": "x", "timeout_sn": 20}), encoding="utf-8")
    (tmp_path / "b.kilit").write_text("999999")
    m.kos("b")
    assert (tmp_path / "b.kilit-eski").exists() and (tmp_path / "b.log").exists()


def test_hafif_bayrak_varsayilan_bos_secenek_dolu(tmp_path, monkeypatch):
    m = _yukle(tmp_path, monkeypatch)
    assert m.hafif_bayrak({"cwd": "x"}, "h") == []
    a = m.hafif_bayrak({"mcp": [], "eklenti": [], "hafif": True}, "h")
    assert a[:2] == ["--strict-mcp-config", "--mcp-config"] and "--disable-slash-commands" in a
    assert json.loads((tmp_path / "h.mcp.json").read_text())["mcpServers"] == {}
    ep = json.loads((tmp_path / "h.eklenti.json").read_text())["enabledPlugins"]
    assert ep and not any(ep.values())
