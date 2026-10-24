import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import mcp_paylasim as mp  # noqa: E402
import mcp_profil  # noqa: E402


def _kaynak(tmp_path, monkeypatch):
    f = tmp_path / "c.json"
    f.write_text(json.dumps({"mcpServers": {n: {"command": "x", "args": []} for n in ("ruflo", "premiere-pro", "rea")}}), encoding="utf-8")
    monkeypatch.setattr(mcp_profil, "KAYNAK", [f])


def test_havuz2_ayaktaysa_http(tmp_path, monkeypatch):
    _kaynak(tmp_path, monkeypatch)
    monkeypatch.setattr(mp, "ayakta", lambda port: port == mp.PORT2)
    t = mcp_profil.tanimlar()
    assert t["ruflo"] == {"type": "http", "url": mp.url("ruflo", mp.PORT2)}
    assert t["premiere-pro"]["type"] == "http"
    assert "type" not in t["rea"]  # durumlu: havuza girmez


def test_havuz2_kapaliysa_stdio(tmp_path, monkeypatch):
    _kaynak(tmp_path, monkeypatch)
    monkeypatch.setattr(mp, "ayakta", lambda port: False)
    assert mcp_profil.tanimlar()["ruflo"] == {"command": "x", "args": []}


def test_sonuc_kisa_hook_hata_metnini_yok_sayar(tmp_path):
    import subprocess
    k = Path(__file__).resolve().parents[2] / ".kos" / "kopru"
    ad = "zz-test-sonuc-kisa"
    j = k / "ajan-sira" / f"{ad}.json"
    j.write_text('{"result": "tamam", "num_turns": 3}\nSessionEnd hook [bash x] failed: Executable not found in $PATH: bash\n', encoding="utf-8")
    try:
        o = subprocess.run([sys.executable, str(k / "sonuc_kisa.py"), ad], capture_output=True, text=True, encoding="utf-8").stdout
    finally:
        j.unlink()
    assert "tamam" in o and "okunamadı" not in o
