"""F2: adım bazlı A/B — aynı girdi iki kol (A = bugünkü yönlendirme, B = aday); kalite (kör puan + görev başarısı) + $ → kur.karar
(24 Eyl takas tablosu, A1); maliyeti bilinmeyen kol → SOR (AL değil); yalnız AL yönlendirme önerir. Testler sahte, canlı çağrı 0."""
import pytest

from video import hafif
from video import yonlendir as yon

SEMA = {"type": "object", "required": ["a"], "properties": {"a": {"type": "string"}}}
GIRDI = [("SİS", f"METİN {i}", SEMA) for i in range(3)]
KOL_B = {"saglayici": "omniroute", "model": "ucuz-model"}


def _tas(usd, form=None, cagri=None):
    def cagir(sistem, metin, sema, model=None, **_):
        cagri is not None and cagri.append((model, metin))
        return {"form": form or {"a": metin}, "usage": {"input_tokens": 100, "output_tokens": 10}, "usd": usd, "sure": 0, "hata": None}
    return cagir


def _kur(monkeypatch, usd_b, form_b=None):
    cagri = []
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _tas(usd_b, form_b, cagri))
    return cagri


def _puan(sabit):
    gelen = []
    def puanla(metinler):
        gelen.extend(metinler)
        return [sabit(m) for m in metinler]
    return puanla, gelen


D = {"model": hafif.MODEL}


def test_ucuz_ayni_kalite_al_ve_yonlendirme(monkeypatch):
    cb, ca = _kur(monkeypatch, 0.001), []
    puanla, gelen = _puan(lambda m: 0.8)
    s = yon.ab(D, "arastirma", GIRDI, KOL_B, _tas(0.01, cagri=ca), {}, puanla, tavan=12)
    assert s["karar"].startswith("AL") and s["yonlendirme"] == {"arastirma": KOL_B}
    assert len(ca) == len(cb) == 6 and {m for m, _ in ca} == {hafif.MODEL} and {m for m, _ in cb} == {"ucuz-model"}
    assert len(gelen) == 12 and not any("ucuz-model" in m or hafif.MODEL in m for m in gelen)  # kör: puanlayıcı kolu görmez


def test_maliyeti_bilinmeyen_kol_sor(monkeypatch):
    _kur(monkeypatch, None)
    s = yon.ab(D, "arastirma", GIRDI, KOL_B, _tas(0.01), {}, _puan(lambda m: 0.8)[0], tavan=12)
    assert s["karar"].startswith("SOR") and "maliyet bilinmiyor: ucuz-model" in s["karar"] and s["yonlendirme"] is None


def test_kalite_dususu_al_degil(monkeypatch):
    _kur(monkeypatch, 0.008, form_b={"b": "x"})  # şema dışı form → görev başarısı 0
    s = yon.ab(D, "arastirma", GIRDI, KOL_B, _tas(0.01), {}, _puan(lambda m: 0.3 if '"b"' in m else 0.8)[0], tavan=12)
    assert not s["karar"].startswith("AL") and s["yonlendirme"] is None and s["b"]["basari"] == 0


def test_tavan_asilirsa_cagri_yok(monkeypatch):
    cb, ca = _kur(monkeypatch, 0.001), []
    s = yon.ab(D, "arastirma", GIRDI, KOL_B, _tas(0.01, cagri=ca), {}, _puan(lambda m: 0.8)[0], tavan=11)
    assert s["karar"].startswith("TAVAN") and "12 > 11" in s["karar"] and ca == cb == [] and s["yonlendirme"] is None


SEMA_T = {"type": "object", "required": ["a", "t"],
          "properties": {"a": {"type": "string"}, "t": {"type": "string", "enum": ["x", "y"]}}}


@pytest.mark.parametrize("form_b, beklenen", [
    ({"a": 5, "t": "x"}, 0),      # required tamam, tip yanlış
    ({"a": "m", "t": "z"}, 0),    # enum dışı
    ({"a": "m", "t": "x"}, 1),    # geçerli form
])
def test_gorev_basarisi_hattin_form_dogrulamasi(monkeypatch, form_b, beklenen):
    _kur(monkeypatch, 0.001, form_b=form_b)
    s = yon.ab(D, "arastirma", [("SİS", "METİN", SEMA_T)], KOL_B, _tas(0.01, form={"a": "m", "t": "x"}), {},
               _puan(lambda m: 0.8)[0], tavan=4)
    assert s["b"]["basari"] == beklenen and s["a"]["basari"] == 1
