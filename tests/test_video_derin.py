import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import video_derin  # noqa: E402


@pytest.fixture
def atla(tmp_path, monkeypatch):
    dosya = tmp_path / "video-atla.txt"
    dosya.write_text("KALICI1\n", encoding="utf-8")
    monkeypatch.setattr(video_derin, "ATLA_DOSYA", dosya)
    return dosya


def test_atla_listesindeki_video_indirilmeden_atlanir(atla, monkeypatch):
    monkeypatch.setattr(video_derin, "indir", lambda *a: pytest.fail("indirme çağrılmamalı"))
    assert video_derin.isle("https://www.youtube.com/watch?v=KALICI1") == ("KALICI1", "atla")


def test_format_yok_hatasi_kalici_atla_listesine_yazilir(atla, monkeypatch):
    monkeypatch.setattr(video_derin, "indir", lambda url, d: (None, "ERROR: No video formats found!"))
    assert video_derin.isle("https://www.youtube.com/watch?v=YENI123") == ("YENI123", "atla")
    assert "YENI123" in atla.read_text(encoding="utf-8").split()


def test_gecici_indirme_hatasi_atla_listesine_yazilmaz(atla, monkeypatch):
    monkeypatch.setattr(video_derin, "indir", lambda url, d: (None, "ERROR: HTTP Error 503"))
    kod, durum = video_derin.isle("https://www.youtube.com/watch?v=GECICI1")
    assert durum.startswith("indirilemedi")
    assert "GECICI1" not in atla.read_text(encoding="utf-8").split()
