import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ucretsiz_havuz as uh  # noqa: E402


def _sahte(monkeypatch, gonderilen, ertelenen):
    secildi = iter(["sahte"])
    monkeypatch.setattr(uh, "_sec", lambda *a, **k: next(secildi, None))
    monkeypatch.setattr(uh, "ad", lambda e: e)
    monkeypatch.setattr(uh, "_oran", lambda *a, **k: None)
    monkeypatch.setattr(uh, "_basari", lambda *a, **k: None)
    monkeypatch.setattr(uh, "_istek", lambda e, istem, *a, **k: gonderilen.append(istem) or "ok")
    monkeypatch.setattr(uh, "_ertele", lambda ad, is_: ertelenen.append((ad, is_)))


def test_zor_sablon_istemin_basina_eklenir(monkeypatch):
    gonderilen, ertelenen = [], []
    _sahte(monkeypatch, gonderilen, ertelenen)
    metin, kaynak, log = uh.cagir("kod-backend", "Mimariyi karşılaştır", zor=True)
    assert gonderilen == [uh.ZOR_SABLON + "Mimariyi karşılaştır"]
    assert len(uh.ZOR_SABLON) // 3 <= 300  # ≤300 jeton (kaba tahmin)


def test_zor_yok_ise_istem_degismez(monkeypatch):
    gonderilen, ertelenen = [], []
    _sahte(monkeypatch, gonderilen, ertelenen)
    uh.cagir("kod-backend", "Düz istem")
    assert gonderilen == ["Düz istem"]


def test_ertele_orijinal_istemi_ve_zor_bayragini_saklar(monkeypatch):
    gonderilen, ertelenen = [], []
    _sahte(monkeypatch, gonderilen, ertelenen)
    monkeypatch.setattr(uh, "_sec", lambda *a, **k: None)  # hiçbir halka yanıtlamaz
    uh.cagir("kod-backend", "Düz istem", zor=True, ertele="is-1")
    assert ertelenen[0][0] == "is-1"
    assert ertelenen[0][1]["istem"] == "Düz istem"  # şablon iki kez eklenmez
    assert ertelenen[0][1]["zor"] is True
