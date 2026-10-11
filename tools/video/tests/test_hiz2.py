"""VİDEO-HIZ-2: süre ≥ ANAHTAR_SN → dhash ve kare çıkarma geçişleri yalnız anahtar kare çözer (aynı ızgara); -ss kareleri ve kısa video eski yol."""
import pytest
from test_hiz3b import _kur

from video import goz as gz

AK = ["-skip_frame", "nokey"]


def _ak(a):
    return any(a[i:i + 2] == AK for i in range(len(a)))


@pytest.mark.parametrize("esik, uzun", [(20, True), (3600, False)])
def test_uzun_videoda_iki_gecis_anahtar_kare(tmp_path, monkeypatch, esik, uzun):
    monkeypatch.setattr(gz, "ANAHTAR_SN", esik)  # _kur süre=30 sn
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"))
    dh, fc, ss = ([a for a, g in c if k(a, g)] for k in (lambda a, g: "rawvideo" in a, lambda a, g: g, lambda a, g: "-ss" in a))
    assert dh and fc and ss
    assert all(_ak(a) == uzun for a in dh + fc)
    assert not any(_ak(a) for a in ss)  # -ss tek kare: tam t karesi gerekir


def test_hw_dususunde_anahtar_kare_korunur(tmp_path, monkeypatch):
    monkeypatch.setattr(gz, "ANAHTAR_SN", 20)
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"), hw_hata=True)
    assert all(_ak(a) for a, g in c if "rawvideo" in a or g)
