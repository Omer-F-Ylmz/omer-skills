"""1b-2a KAPANIŞ: ikili parti (sonnet + haiku → birlestir) · tek kol künyesi. Sahte çağrıcı; canlı çağrı 0."""
import importlib.util

import pytest

from video import parti as pt
from test_m2a import V, Sahte, _ctx, _durum, _kurulum, _ns, _pid

SON, HAI = "claude-sonnet-5-5", "claude-haiku-5-5"


# a: adaylar gecer ile iki yönde tekil (kısa ad uzun adın içinde geçer)
@pytest.mark.parametrize("a_ad, b_ad", [("Claude Code CLI", "Claude Code"), ("Claude Code", "Claude Code CLI")])
def test_birlestir_aday_iki_yonde_tekil(a_ad, b_ad):
    f = pt.birlestir({"adaylar": [{"ad": a_ad}]}, {"adaylar": [{"ad": b_ad}, {"ad": "Başka Araç"}]})
    assert [x["ad"] for x in f["adaylar"]] == [a_ad, "Başka Araç"]


# b: URL + komut birleşimi, url_norm / norm sonrası tekrar yok
def test_birlestir_url_komut_birlesim():
    a = {"urller": [{"url": "https://github.com/x/y/", "sinif": "repo"}], "kurulum_komutlar": [{"komut": "npm i -g foo"}],
         "aciklama_baglantilari": [{"url": "https://a.com/p"}]}
    b = {"urller": [{"url": "http://www.github.com/x/y?z=1", "sinif": "diger"}, {"url": "https://z.dev", "sinif": "site"}],
         "kurulum_komutlar": [{"komut": "npm  i -g  foo"}, {"komut": "pip install bar"}], "aciklama_baglantilari": [{"url": "https://A.com/p/"}, {"url": "https://b.com"}]}
    f = pt.birlestir(a, b)
    assert [x["url"] for x in f["urller"]] == ["https://github.com/x/y/", "https://z.dev"]
    assert [x["komut"] for x in f["kurulum_komutlar"]] == ["npm i -g foo", "pip install bar"]
    assert [x["url"] for x in f["aciklama_baglantilari"]] == ["https://a.com/p", "https://b.com"]


# c: aynı URL, farklı sınıf → birincil (sonnet) sınıfı kalır; a'da olmayan alan b'den
def test_birlestir_sinif_birincilden():
    f = pt.birlestir({"urller": [{"url": "https://github.com/x/y", "sinif": "repo"}], "iz": []},
                     {"urller": [{"url": "https://github.com/x/y", "sinif": "diger"}], "iz": ["i1"], "promptlar": ["p"]})
    assert f["urller"] == [{"url": "https://github.com/x/y", "sinif": "repo"}] and f["iz"] == ["i1"] and f["promptlar"] == ["p"]


def _ikili():
    spec = importlib.util.spec_from_file_location("video._parti_kopya", pt.__file__)
    spec.loader.exec_module(kopya := importlib.util.module_from_spec(spec))
    return kopya.YONLENDIRME


def test_yeni_parti_varsayilan_ikili(tmp_path, monkeypatch):
    assert _ikili()["tarama"] == {"yontem": "ikili", "modeller": [SON, HAI]}
    monkeypatch.setattr(pt, "YONLENDIRME", _ikili())
    _kurulum(tmp_path, V[:1], sure=300)
    with pytest.raises(KeyboardInterrupt):
        pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), _ctx(tmp_path, Sahte(kes=1)))
    assert _durum(tmp_path)["yonlendirme"]["tarama"]["yontem"] == "ikili"


def _kos_ikili(tmp_path, monkeypatch, haiku):
    monkeypatch.setattr(pt, "YONLENDIRME", _ikili())
    kok, say, sahte = _kurulum(tmp_path, V[:1], sure=300), [], Sahte()

    def cagir(sistem, metin, sema, **k):
        say.append(k["model"])
        if k["model"] == HAI and haiku:
            return {"form": None, "usage": {}, "usd": 0.0, "sure": 0.1, "hata": haiku}
        return {**sahte(sistem, metin, sema), "model": k["model"] + "-20260101"}
    assert pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, cagir)) == 0
    return kok, say


# d: haiku kolu hata → sonnet formu tek başına; künye "tek kol:"; rapor md'de; video başına tam 2 çağrı
def test_tek_kol_kunyesi_raporda(tmp_path, monkeypatch):
    kok, say = _kos_ikili(tmp_path, monkeypatch, "rc 1: x")
    t = _durum(kok)["videolar"][V[0]]["tarama"]
    assert say == [SON, HAI] and t["durum"] == "tamam"
    assert f"{HAI} rc 1: x" in t["kunye"] and "tek kol:" in t["kunye"] and f"{SON}: {SON}-20260101 · 160 tk" in t["kunye"]
    md = (kok / "docs" / "video-tarama").glob(f"*-{V[0]}.md")
    assert "tek kol: " + HAI + " rc 1: x" in next(md).read_text(encoding="utf-8")


def test_iki_kol_kunyesi_ve_iki_cagri(tmp_path, monkeypatch):
    kok, say = _kos_ikili(tmp_path, monkeypatch, None)
    t = _durum(kok)["videolar"][V[0]]["tarama"]
    assert say == [SON, HAI] and t["durum"] == "tamam" and "tek kol" not in t["kunye"]
    assert t["kunye"] == f"{SON}: {SON}-20260101 · 160 tk · {HAI}: {HAI}-20260101 · 160 tk"


def test_iki_kol_hata_form_red(tmp_path, monkeypatch):
    monkeypatch.setattr(pt, "YONLENDIRME", _ikili())
    kok = _kurulum(tmp_path, V[:1], sure=300)
    say = []
    cagir = lambda *a, **k: say.append(k["model"]) or {"form": None, "usage": {}, "usd": 0.0, "sure": 0.1, "hata": "rc 1: x"}
    pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, cagir))
    assert len(say) == 2 and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] in ("hata", "form_red")


def test_usage_ic_ice_sozluk_toplam_bozmaz(tmp_path, monkeypatch):  # canlı bulgu: claude -p usage'ında "cache_creation": {...} gibi iç içe alanlar var
    monkeypatch.setattr(pt, "YONLENDIRME", _ikili())
    kok, sahte = _kurulum(tmp_path, V[:1], sure=300), Sahte()

    def cagir(sistem, metin, sema, **k):
        y = sahte(sistem, metin, sema)
        return {**y, "usage": {**y["usage"], "cache_creation": {"ephemeral_5m_input_tokens": 7}, "service_tier": "standard"}}
    assert pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, cagir)) == 0
    assert _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"
