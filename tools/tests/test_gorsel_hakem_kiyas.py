import importlib.util
import sys
from pathlib import Path

import pytest

YOL = Path(__file__).resolve().parents[2] / ".kos" / "kopru" / "gorsel_hakem.py"


@pytest.fixture
def hakem(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gorsel_hakem.py"])  # main() içe aktarmada koşar; PNG yok → çıktı yok
    spec = importlib.util.spec_from_file_location("gorsel_hakem", YOL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_kiyas_yaniti_kalite_farki_verir(hakem):
    assert hakem.ayikla('x {"kalite_farki": 7} y', kiyas=True) == {"kalite_farki": 7}


def test_kiyas_alani_eksikse_hata(hakem):
    with pytest.raises(KeyError):
        hakem.ayikla('{"puan": 7}', kiyas=True)


def test_ref_iki_gorsel_gonderir_ve_kiyas_bicimi_kullanir(hakem, monkeypatch):
    gorulen = {}

    def sahte(e, icerik, *_):
        gorulen["icerik"] = icerik
        return '{"kalite_farki": 8}'

    monkeypatch.setattr(hakem, "veri_url", lambda p: f"data:{p}")
    monkeypatch.setattr(hakem.h, "_istek", sahte)
    s = hakem.sor("aday.png", "soru", ref="ref.png")
    assert len(s) == hakem.CIFT and all(v["kalite_farki"] == 8 for v in s.values())
    urller = [c["image_url"]["url"] for c in gorulen["icerik"] if c["type"] == "image_url"]
    assert urller == ["data:ref.png", "data:aday.png"]
    assert "REFERANS" in gorulen["icerik"][0]["text"]
