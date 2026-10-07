"""MÜKEMMEL-5c: Jev eksik yön etiketi (O93 seçenek a)."""
from pathlib import Path

from video import kur

ETIKET = ("eksik yok", "aday eksik", "prompt/komut eksik", "kare okuma eksik", "yüzeysel (ayrıntı az)", "dayanaksız iddia")


def test_etiket_listesi_tek_yerde():
    assert kur.EKSIK_ETIKET == ETIKET
    assert kur.EKSIK_Q["type"] == "choice" and list(kur.EKSIK_Q["criteria"]) == list(ETIKET)
    assert kur.EKSIK_Q["instructions"] == "Bu formun en büyük eksiği hangisi?"


def test_jev_puanla_puan_ve_etiket_ayni_istekte():
    goren = []

    class Sahte:
        def __init__(self, env=None, en_fazla=5, istek_tavan=250, **_):
            goren.append(("tavan", istek_tavan))

        def yargila(self, ms, q):
            goren.append(("q", tuple(q)))
            return [{"kalite": {"type": "score", "score": 0.7}, "eksik": {"type": "choice", "choice": "aday eksik",
                                                                        "probabilities": {"aday eksik": 0.6, "yüzeysel (ayrıntı az)": 0.3}}} for _ in ms]
    p = kur.jev_puanla(["a", "b"], {}, tas=Sahte)
    assert goren == [("tavan", 2), ("q", ("kalite", "eksik"))]  # form başı tek istek: tavan = form sayısı
    assert p[0]["score"] == 0.7 and p[0]["eksik"]["choice"] == "aday eksik"


def test_eksik_yazi_ikinci_etiket_esigi():
    e = lambda pr: {"score": 0.5, "eksik": {"type": "choice", "probabilities": pr}}  # noqa: E731
    assert kur.eksik_yazi(e({"aday eksik": 0.6, "yüzeysel (ayrıntı az)": 0.25, "eksik yok": 0.15})) == "aday eksik (0.60) · yüzeysel (ayrıntı az) (0.25)"
    assert kur.eksik_yazi(e({"aday eksik": 0.8, "eksik yok": 0.2})) == "aday eksik (0.80)"
    assert kur.eksik_yazi(0.5) == "-" and kur.eksik_yazi(None) == "-"


def test_yeniden_etiketsiz_puan_yeniden_sorulur():
    assert kur.puan_eksik(None) and kur.puan_eksik({"type": "score", "score": 0.6})
    assert not kur.puan_eksik({"score": 0.6, "eksik": {}}) and not kur.puan_eksik(0.6)  # skaler (eski sahte) kayıt korunur


def test_eleme_etiketi_kullanir():
    y = (Path(kur.__file__).parent / "yonlendir.py").read_text(encoding="utf-8")
    assert "kur.puan_eksik" in y and "kur.eksik_yazi" in y
    ps = (Path(__file__).resolve().parents[3] / "docs" / "video-tarama" / "eleme.ps1").read_text(encoding="utf-8-sig")
    assert "kur.jev_puanla(ms, env)" in ps and "KALITE_Q" not in ps.split("boyut =")[0]
