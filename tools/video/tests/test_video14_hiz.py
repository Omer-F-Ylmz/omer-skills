"""VİDEO-14 Faz 2: uzun video hızlandırma bayrakları (varsayılan kapalı; altın ölçümüyle açılır)."""
import sys
import types

from video import cli
from video import goz as gz


def test_uzun_hiz_esik(monkeypatch):
    """VIDEO_UZUN_HIZ=1 → 10-60 dk video da melez anahtar-kare yolu (+ es_kare OCR eşi, paralel dilim); bayraksız eşik ANAHTAR_SN."""
    monkeypatch.delenv("VIDEO_HIZ2", raising=False)
    monkeypatch.delenv("VIDEO_UZUN_HIZ", raising=False)
    assert cli._hiz2(880) == ""
    monkeypatch.setenv("VIDEO_UZUN_HIZ", "1")
    assert cli._hiz2(880) == "2" and cli._hiz2(599) == "" and cli._hiz2(6407) == "2"
    monkeypatch.setenv("VIDEO_HIZ2", "0")
    assert cli._hiz2(880) == ""


class _E:
    def __getattr__(self, a):
        return a


def _params(monkeypatch, tmp_path):
    for f in gz.MODEL_DOSYA.values():
        (tmp_path / f).write_bytes(b"")
    monkeypatch.setenv("VIDEO_OCR_MODEL", str(tmp_path))
    al = {}
    monkeypatch.setitem(sys.modules, "rapidocr", types.SimpleNamespace(
        LangCls=_E(), LangDet=_E(), LangRec=_E(), ModelType=_E(), OCRVersion=_E(), RapidOCR=lambda params: al.update(params)))
    gz.rapid_yukle("cpu")
    return al


def test_ocr_det_bayrak(monkeypatch, tmp_path):
    """VIDEO_OCR_DET=<px> → algılama girdisi uzun kenar ≤ px (Det.limit_type max); bayraksız RapidOCR varsayılanı, önbellek anahtarı ayrışır."""
    monkeypatch.delenv("VIDEO_OCR_DET", raising=False)
    assert "Det.limit_side_len" not in _params(monkeypatch, tmp_path) and gz.ocr_det() == 0
    monkeypatch.setenv("VIDEO_OCR_DET", "1280")
    p = _params(monkeypatch, tmp_path)
    assert p["Det.limit_type"] == "max" and p["Det.limit_side_len"] == 1280 and gz.ocr_det() == 1280


def test_ocr_cls_bayrak(monkeypatch, tmp_path):
    """VIDEO_OCR_CLS=0 → yön sınıflayıcı kapalı (ekran metni hep yatay; HYMD 60 kare −28% süre, cls 180° çevirip çöp okuyordu); bayraksız RapidOCR varsayılanı."""
    monkeypatch.delenv("VIDEO_OCR_CLS", raising=False)
    assert "Global.use_cls" not in _params(monkeypatch, tmp_path) and gz.ocr_cls0() is False
    monkeypatch.setenv("VIDEO_OCR_CLS", "0")
    assert _params(monkeypatch, tmp_path)["Global.use_cls"] is False and gz.ocr_cls0() is True
