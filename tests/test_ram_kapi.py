import sys, types
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), "..", "tools"))
import ram_kapi as R


def _sahte(ram, kayit):
    R.psutil = types.SimpleNamespace(virtual_memory=lambda: types.SimpleNamespace(percent=ram))
    R.uygula = lambda ad, esle, islem: kayit.append((ad, islem)) or 3
    R.say = lambda *a: None


def test_ustte_en_dusuk_oncelik_askiya():
    k = []
    _sahte(97.0, k)
    assert R.tur([]) == ["borsa-egit"] and k == [("borsa-egit", "suspend")]


def test_ustte_sonraki_is():
    k = []
    _sahte(96.0, k)
    assert R.tur(["borsa-egit"]) == ["borsa-egit", "kategori-kapsam"]


def test_altta_son_askiyi_devam():
    k = []
    _sahte(80.0, k)
    assert R.tur(["borsa-egit", "kategori-kapsam"]) == ["borsa-egit"] and k == [("kategori-kapsam", "resume")]


def test_arada_dokunma():
    k = []
    _sahte(93.0, k)
    assert R.tur(["borsa-egit"]) == ["borsa-egit"] and k == []
