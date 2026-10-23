import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ucretsiz_havuz as uh  # noqa: E402


def _agsiz(monkeypatch, tmp_path):
    """Gerçek ağ/anahtar/durum yok: istekler yakalanır, durum dosyası geçici."""
    secilen = []
    monkeypatch.setattr(uh, "DURUM", tmp_path / "durum.json")
    monkeypatch.setattr(uh, "_anahtar", lambda k: "x")
    monkeypatch.setattr(uh, "_url", lambda p: "http://yok")
    monkeypatch.setattr(uh, "_omni_serbest", lambda: True)
    monkeypatch.setattr(uh, "_istek", lambda e, *a, **k: secilen.append(e) or "cevap")
    return secilen


@pytest.mark.parametrize("tur", ["ozet", "hakem", "yazim", "kod", "uzun", "kolay", "orta", "zor"])
def test_cagir_aday_secer_kota_aciksa_none_donmez(monkeypatch, tmp_path, tur):
    secilen = _agsiz(monkeypatch, tmp_path)
    y, k, log = uh.cagir(tur, "merhaba", max_tokens=20)
    assert y == "cevap" and k and len(secilen) == 1 and log == []  # HAVUZ-ONAR-1: kolay/orta → (None, None, [])


def test_zorluk_sinifi_gecerli_turun_halkasina_gider(monkeypatch, tmp_path):
    secilen = _agsiz(monkeypatch, tmp_path)
    for sinif in ("kolay", "orta", "zor"):
        uh.cagir(sinif, "x", max_tokens=20)
    assert [uh.SINIF_TUR[s] for s in ("kolay", "orta", "zor")] and all(uh.SINIF_TUR[s] in e.turler for s, e in zip(("kolay", "orta", "zor"), secilen))


def test_bilinmeyen_tur_sessiz_bos_degil_hata(monkeypatch, tmp_path):
    _agsiz(monkeypatch, tmp_path)
    with pytest.raises(ValueError, match="bilinmeyen tür"):
        uh.cagir("yok-boyle-tur", "x", max_tokens=20)
