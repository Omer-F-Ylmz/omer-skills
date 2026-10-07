"""MÜKEMMEL-6a (K4): tara_v10 parçaları eşzamanlı (≤ PARCA_PARALEL, varsayılan 4); son geçiş hepsi bittikten sonra.
Sahte gecikmeli çağrıcı; canlı çağrı 0."""
import threading
import time

import pytest

import test_f3_v5 as v5
from test_derinlik_kapanis import BOZUK, _g, _orn
from test_f3_v5 import E1, ENV
from video import yonlendir as yon

BEKLE = {"Alfa": 0.3, "Beta": 0.2, "Gama": 0.1}  # ilk parça en geç biter


@pytest.fixture(autouse=True)
def _k3(monkeypatch):
    monkeypatch.setattr(yon, "parca_k", lambda p: (3,))
    monkeypatch.setattr(yon, "ANLAMSAL", False)
    monkeypatch.delenv("PARCA_PARALEL", raising=False)


def _yavas(c, bekle=None, boz=None):
    t, kilit, an, say = v5._b6(c)(E1, ENV), threading.Lock(), [0], []

    def tas(sistem, metin, sema, kareler=(), model=None, **_):
        if sistem == yon.SON_SISTEM10:
            return t(sistem, metin, sema, kareler, model=model)
        with kilit:
            an[0] += 1
            say.append(an[0])
        ad = next(x for x in BEKLE if x in metin)
        time.sleep(bekle or BEKLE[ad])
        with kilit:
            an[0] -= 1
        if boz and ad == boz and sum(boz in x.get("metin", "") for x in c) == 0:
            c.append({"i": "bozuk", "metin": metin})
            return dict(BOZUK["JSON"])
        return t(sistem, metin, sema, kareler, model=model)
    tas.en_cok = lambda: max(say)
    return tas


def _kos(tmp_path, tas):
    return yon.tara_v10(_g(tmp_path), ENV, E1, tas=tas, ornek=_orn(tmp_path))


def test_sira_korunur_toplamlar_ayni(tmp_path, monkeypatch):
    par = _kos(tmp_path, t := _yavas([]))
    assert t.en_cok() == 3
    monkeypatch.setenv("PARCA_PARALEL", "1")
    sir = _kos(tmp_path, t1 := _yavas([]))
    assert t1.en_cok() == 1  # geri alma yolu: bugünkü sıralı davranış
    assert par["hata"] is None and par["form"] == sir["form"]
    assert (par["cagri"], par["usd"], par["usage"]) == (sir["cagri"], sir["usd"], sir["usage"]) and par["cagri"] == 4


def test_sure_siralinin_yarisindan_kisa(tmp_path, monkeypatch):
    par = _kos(tmp_path, _yavas([], bekle=0.3))
    monkeypatch.setenv("PARCA_PARALEL", "1")
    sir = _kos(tmp_path, _yavas([], bekle=0.3))
    assert par["sure"] < sir["sure"] / 2


def test_hata_yalniz_o_parcayi_yeniden_dener(tmp_path):
    c = []
    y = _kos(tmp_path, _yavas(c, boz="Beta"))
    parca = [x["metin"] for x in c if x.get("i") != "son"]
    assert y["hata"] is None and y["parca_yeniden"] == 1 and y["cagri"] == 5
    assert [sum(a in m for m in parca) for a in BEKLE] == [1, 2, 1]
