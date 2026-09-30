"""MOTOR-M7: kare okuması kütüphaneye girmez (M2f kararı tersine) · yalnız teknik tablosu (site_ui) · eski `video teknik` yolu da gözlem süzgecinden geçer."""
from types import SimpleNamespace

from test_m2a import V
from test_m2g import _fe, _md
from test_m6 import GOZLEM, TEKNIK

from video import akil
from video import parti as pt
from video import uygula as uy

KARE = "Başlıkta mix-blend-mode: difference ile ters renk"  # süzgeçten teknik diye geçerdi; kaynağı kare → yine girmez


# --- K1 Kareden okunanlar ne tek'te (panel Site/UI = tek, akil.py:575) ne frontend.md'de; site_ui tekniği girer
def test_k1_kare_okumasi_kutuphaneye_ve_panele_girmez(tmp_path):
    site = [{"teknik": TEKNIK[5], "ne": "ekran", "nasil": "-", "kutuphane": "-", "kanit_zamani": "1:05", "kaynak": "kare"}]
    tek, _, _ = akil.site_ogren(tmp_path, [(V[0], _md(site_ui=site, kare=[{"kare": "2:10", "okunan": KARE}]))])
    assert [x[0] for x in tek] == [TEKNIK[5]]
    fe = _fe(tmp_path)
    assert "backdrop-filter blur" in fe and "mix-blend-mode" not in fe


# --- K3 `video teknik` (uygula.teknik) aynı süzgeç: gözlem satırı frontend.md'ye girmez, teknik girer
def test_k3_video_teknik_gozlem_suzgeci(tmp_path):
    site = [{"teknik": s, "ne": "ekran", "nasil": "-", "kutuphane": "-", "kanit_zamani": "1:00", "kaynak": "altyazı"} for s in (GOZLEM[0], TEKNIK[5])]
    r = tmp_path / "rapor.md"
    r.write_text(_md(site_ui=site), encoding="utf-8")
    assert uy.teknik(SimpleNamespace(raporlar=[str(r)]), {"env": {"VIDEO_UYGULA_KOK": str(tmp_path)}}) == 0
    fe = _fe(tmp_path)
    assert "backdrop-filter blur" in fe and "BLAZING" not in fe
