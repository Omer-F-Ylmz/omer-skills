import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import usta_kart_hat as UH  # noqa: E402


def test_kapi_esigi_98():
    assert UH.gecer(10, 10) and UH.gecer(49, 50)
    assert not UH.gecer(9, 10) and not UH.gecer(0, 0)


def test_kaynak_siniri(monkeypatch):
    monkeypatch.setattr(UH, "ram_yuzde", lambda: 96)
    assert UH.kaynak_yeterli()[0] is False
    monkeypatch.setattr(UH, "ram_yuzde", lambda: 50)
    monkeypatch.setattr(UH.shutil, "disk_usage", lambda p: type("D", (), {"free": 10 * 2**30})())
    assert UH.kaynak_yeterli()[0] is False
    monkeypatch.setattr(UH.shutil, "disk_usage", lambda p: type("D", (), {"free": 100 * 2**30})())
    assert UH.kaynak_yeterli() == (True, "")


def test_durdu_devam_etmez(tmp_path, monkeypatch):
    monkeypatch.setattr(UH, "DURUM", tmp_path / "d.json")
    UH.durum_yaz({"durum": "DURDU", "kapi_gecen": 0, "partiler": []})
    monkeypatch.setattr(sys, "argv", ["x"])
    assert UH.main() == 2
