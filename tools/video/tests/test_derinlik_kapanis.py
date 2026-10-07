"""DERİNLİK-KAPANIŞ-1: hat sürümü V10 — tara_v10 (eleme@V10 yolu tek fonksiyonda) · parça yeniden denemesi · parti tarama adımı
yonlendirme "yontem": "V10" → tara_v10, hata ya da ön tahmin aşımında aynı adımda A geri dönüşü (video düşmez). Canlı çağrı 0."""
import json
from pathlib import Path

import pytest

import test_f3_v5 as v5
from test_f1 import Omni
from test_f3_v5 import E1, ENV, KARELER, P, SV
from test_m2a import V, Sahte, _ctx, _defter, _durum, _kurulum, _ns, _pid
from video import hafif
from video import parti as pt
from video import yonlendir as yon

ROTA10 = {"tarama": {"saglayici": "omniroute", "model": "openrouter/google/gemini-3.5-flash-lite", "yontem": "V10"}}
M10 = ROTA10["tarama"]["model"]


def _g(tmp_path, paket=P):
    kr = [tmp_path / x.rsplit("/", 1)[1] for x in KARELER]
    for x in kr:
        x.write_bytes(b"k")
    return ("S", paket, SV, kr)


def _orn(tmp_path):
    o = tmp_path / "ORN6.json"
    o.write_text('{"id": "ORN6"}', encoding="utf-8")
    return o


def test_eleme_v10_birebir_tara_v10(tmp_path):
    c1 = []
    v5._e6(tmp_path, [f"{E1}@V10"], c1)
    g, o, k = _g(tmp_path), tmp_path / "ORN6.json", yon.parca_k(P)[0]
    c2, c3 = [], []
    eski = yon._parcali(v5._b6(c2)(E1, ENV), lambda t: "S\n\n" + yon.EKSIKSIZLIK10 + yon.ORNEK_BASLIK + o.read_text(encoding="utf-8"),
                        g, k, {"kareler": g[3]}, E1, v6=True, alan=True, v10=True)  # bugünkü eleme@V10 ifadesi
    yeni = yon.tara_v10(g, ENV, E1, tas=v5._b6(c3)(E1, ENV), ornek=o)
    assert c3 == c2 and c1 == c2 * 2  # gövdeler (sistem · metin · kareler · son geçiş şeması) birebir; eleme 2 yanıt
    assert yeni["form"] == eski["form"] == v5._kayit(tmp_path, f"{E1}@V10")["form"]
    assert yeni["k"] == k and yeni["parca_yeniden"] == 0 and yeni["cagri"] == len(c2) and yeni["hata"] is None


def test_tara_v10_govde_ek_ve_ornek_yok(tmp_path):
    ge, c = [], []
    g = _g(tmp_path)
    yon.tara_v10(g, ENV, E1, ornek=_orn(tmp_path), b_kur=v5._b8(c, ge))
    assert ge == [{"temperature": 0.2, "seed": 7}] and c
    c2 = []
    y = yon.tara_v10(g, ENV, E1, ornek=tmp_path / "yok.json", b_kur=v5._b8(c2, ge))
    assert y["hata"] == "örnek yok" and c2 == [] and y["cagri"] == 0 and y["usd"] == 0.0
    assert json.loads(yon.ORNEK_V10.read_text(encoding="utf-8"))["id"] == "Pj2FnVE-W3c"  # docs/video-tarama/ornek-v10.json


BOZUK = {"JSON": {"form": None, "usage": {"input_tokens": 4}, "usd": 0.002, "sure": 0.1, "hata": "form JSON değil"},
         "şema": {"form": {"videolar": [{"id": "vid1"}]}, "usage": {"input_tokens": 4}, "usd": 0.002, "sure": 0.1, "hata": None}}


def _bozan(c, kac, bozuk):
    t, say = v5._b6(c)(E1, ENV), []

    def tas(sistem, metin, sema, kareler=(), model=None, **_):
        if sistem != yon.SON_SISTEM10 and len(say) < kac:
            say.append(1)
            c.append({"i": "bozuk", "metin": metin})
            return dict(bozuk)
        return t(sistem, metin, sema, kareler, model=model)
    return tas


@pytest.mark.parametrize("tur", ["JSON", "şema"])
def test_tara_v10_parca_yeniden(tmp_path, tur):
    g, o = _g(tmp_path), _orn(tmp_path)
    c = []
    y = yon.tara_v10(g, ENV, E1, tas=_bozan(c, 1, BOZUK[tur]), ornek=o)
    assert y["hata"] is None and y["parca_yeniden"] == 1 and y["cagri"] == 3 and abs(y["usd"] - 0.004) < 1e-9
    assert c[0]["metin"] == c[1]["metin"] and pt._denet(y["form"], SV, "form") == []  # aynı gövdeyle bir kez
    c2 = []
    y = yon.tara_v10(g, ENV, E1, tas=_bozan(c2, 2, BOZUK[tur]), ornek=o)
    assert y["hata"].startswith("parça 1: ") and y["form"] is None and y["parca_yeniden"] == 1 and len(c2) == 2  # ikinci hata: son geçiş yok


# parti tarama adımı
def _hazir(tmp_path, rota=ROTA10, **tavan):
    kok = _kurulum(tmp_path, V[:1], sure=300)
    with pytest.raises(KeyboardInterrupt):
        pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, Sahte(kes=1)))
    yol = kok / ".kos" / _pid(kok) / "durum.json"
    d = json.loads(yol.read_text(encoding="utf-8"))
    d["tavan"].update(tavan)
    yol.write_text(json.dumps({**d, "yonlendirme": rota}), encoding="utf-8")
    return kok


def _tarama(kok):
    return [x for x in _defter(kok) if x["adim"] == "tarama"][-1]


def test_parti_v10_tara_v10_cagrilir(tmp_path, monkeypatch):
    kok, gor, a = _hazir(tmp_path), [], Sahte()

    def v10(g, env, model, **k):
        gor.append((model, g[2]["properties"]["videolar"]["items"]["properties"]["id"]["enum"], Path(k["ornek"]).name))
        return {**a(*g[:3]), "usd": 0.004, "cagri": 3, "k": 2}
    monkeypatch.setattr(yon, "tara_v10", v10)
    s = Sahte()
    pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    t = _tarama(kok)
    assert s.cagrilar == [] and gor == [(M10, [V[0]], "ornek-v10.json")]
    assert _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"
    assert t["model"] == M10 and t["cagri"] == 3 and "geri_donus" not in t and pt._defter(kok / ".kos" / _pid(kok))[0] == 3


def test_parti_v10_hata_a_geri_donus(tmp_path, monkeypatch):
    kok = _hazir(tmp_path)
    monkeypatch.setattr(yon, "tara_v10", lambda g, env, model, **k: {"form": None, "usage": {"input_tokens": 5}, "usd": 0.003, "sure": 1.0,
                                                                     "hata": "parça 1: form JSON değil", "cagri": 2})
    s = Sahte()
    pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    t = _tarama(kok)
    assert len(s.cagrilar) == 1 and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"
    assert t["geri_donus"] == f"{V[0]}: parça 1: form JSON değil" and t["model"] == hafif.MODEL and t["cagri"] == 3 and abs(t["usd"] - 0.013) < 1e-9


# MÜKEMMEL-8a: geçici hata (boş yanıt/429 · 5xx · zaman aşımı) A'ya gitmez → "yeniden", parti sonunda ≥60 s sonra bir tur
def _gecici(tmp_path, monkeypatch, basari):
    kok, n, bek = _hazir(tmp_path), [], []
    a = Sahte()

    def v10(g, env, model, **k):
        n.append(1)
        return {**a(*g[:3]), "usd": 0.004, "cagri": 3} if len(n) in basari else \
            {"form": None, "usage": {}, "usd": 0.0, "sure": 1.0, "hata": 'parça 1: ölçülemedi: HTTP 429 "rate limit"', "cagri": 1}
    monkeypatch.setattr(yon, "tara_v10", v10)
    monkeypatch.setattr(pt, "BEKLE", bek.append)
    s = Sahte()
    pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    return kok, s, n, bek


def test_parti_v10_gecici_hata_a_yok_son_tur(tmp_path, monkeypatch):
    kok, s, n, bek = _gecici(tmp_path, monkeypatch, {2})
    t = [x for x in _defter(kok) if x["adim"] == "tarama"]
    assert s.cagrilar == [] and len(n) == 2 and bek.count(60) == 1 and pt.SON_TUR_SN == 60
    assert "geri_donus" not in t[0] and V[0] in t[0]["gecici"] and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tamam"


def test_parti_v10_gecici_iki_tur_yeniden_kalir(tmp_path, monkeypatch, capsys):
    kok, s, n, bek = _gecici(tmp_path, monkeypatch, set())
    assert s.cagrilar == [] and len(n) == 2 and bek.count(60) == 1
    assert _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "yeniden" in pt.YENIDEN and _durum(kok)["durum"] != "tamam"
    assert f"{V[0]} (tarama: parça 1: ölçülemedi: HTTP 429" in capsys.readouterr().out


@pytest.mark.parametrize("h", ["parça 1: boş yanıt", "parça 2: ölçülemedi: HTTP 503 x", "parça 1: ölçülemedi: TimeoutError: timed out", "zaman aşımı 600 sn"])
def test_gecici_sinif(h):
    assert pt.gecici(h) and not pt.gecici("parça 1: form JSON değil") and not pt.gecici("parça 1: şema: eksik id")


def test_parti_v10_kalici_geri_donus_ozette(tmp_path, monkeypatch, capsys):
    kok = _hazir(tmp_path)
    monkeypatch.setattr(yon, "tara_v10", lambda g, env, model, **k: {"form": None, "usage": {}, "usd": 0.0, "sure": 1.0, "hata": "parça 1: form JSON değil", "cagri": 1})
    pt.parti(_ns("devam", _pid(kok)), _ctx(kok, Sahte()))
    assert f"geri dönüş: {V[0]}: parça 1: form JSON değil" in capsys.readouterr().out


def test_parti_v10_on_tahmin_tavan_kalir(tmp_path, monkeypatch):
    kok = _hazir(tmp_path, usd=0.005)  # DERİNLİK-KAPANIŞ-2: tahmin_v10 > kalan $ → video tavanda (YENIDEN); A V10'dan pahalı, çağrılmaz
    monkeypatch.setattr(yon, "tara_v10", lambda *a, **k: pytest.fail("ön tahmin kalan $'ı aşınca tara_v10 çağrılmaz"))
    s = Sahte()
    pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    t = _tarama(kok)
    assert s.cagrilar == [] and _durum(kok)["videolar"][V[0]]["tarama"]["durum"] == "tavan" in pt.YENIDEN
    assert "geri_donus" not in t and t["form"].startswith("hata: tavan: ön tahmin $") and t["cagri"] == 0


def test_tahmin_v10_parca_ve_kare(tmp_path, monkeypatch):
    g = _g(tmp_path)
    t1, t0 = yon.tahmin_v10(g, M10), yon.tahmin_v10(g[:3] + ([],), M10)
    assert yon.parca_k(P)[0] == 1 and 0 < t0 < t1  # kare artınca artar
    monkeypatch.setattr(yon, "PARCA_YUK", yon.yuk(P) / 4)
    assert yon.parca_k(P)[0] == 4 and yon.tahmin_v10(g, M10) > t1  # k 1 < k 4


def test_tahmin_v10_cikti_yuk_olcekli(tmp_path, monkeypatch):  # MÜKEMMEL-1d: küçük yük → küçük çıktı payı, büyük yük → CIKTI_CAGRI üstü; çağrı başı girdi payı
    g = _g(tmp_path)
    n = len(yon.bolumle(g[1], yon.parca_k(g[1])[0], yuk=True)) + 1
    monkeypatch.setitem(yon.FIYAT, "_c", {"girdi": 0, "cikti": 1e6})
    monkeypatch.setitem(yon.FIYAT, "_g", {"girdi": 1e6, "cikti": 0})
    assert yon.CIKTI_TABAN * n <= yon.tahmin_v10(g, "_c") < yon.CIKTI_CAGRI * n
    gc, gi = yon.GIRDI_CAGRI, yon.tahmin_v10(g, "_g")
    monkeypatch.setattr(yon, "GIRDI_CAGRI", 0)
    assert gi - yon.tahmin_v10(g, "_g") == pytest.approx(gc * n)
    monkeypatch.setattr(yon, "CIKTI_YUK", 1e-3)
    assert yon.tahmin_v10(g, "_c") == pytest.approx(yon.CIKTI_CAGRI * n)


@pytest.mark.parametrize("ad", ["eleme.ps1", "ab-canli.ps1"])
def test_ps1_utf8_bom(ad):  # DERİNLİK-KAPANIŞ-2: PS 5.1 BOM'suz .ps1'i ANSI okur → here-string "·" Python'a "Â·" olarak gider
    b = (yon.ORNEK_V10.parent / ad).read_bytes()
    assert b.startswith(b"\xef\xbb\xbf") or b.isascii()


def test_parti_yontem_yok_bugunku_yol(tmp_path, monkeypatch):
    kok = _hazir(tmp_path, rota={"tarama": {"saglayici": "omniroute", "model": M10}})
    monkeypatch.setattr(yon, "tara_v10", lambda *a, **k: pytest.fail("yontem yokken tara_v10 çağrılmaz"))
    o = Omni(hata=KeyboardInterrupt())
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: yon.omni_cagir(m, env, gonder=o))
    s = Sahte()
    with pytest.raises(KeyboardInterrupt):
        pt.parti(_ns("devam", _pid(kok)), _ctx(kok, s))
    assert s.cagrilar == [] and o.cagrilar[0][1]["model"] == M10


def test_aracli_adim_etkilenmez():
    c = object()
    assert yon.sec({"model": hafif.MODEL, "yonlendirme": ROTA10}, "tarama", c, ENV, araclar=("WebFetch",)) == (c, hafif.MODEL)


def test_yeni_parti_varsayilan_yonlendirme(tmp_path, monkeypatch):
    monkeypatch.setattr(pt, "YONLENDIRME", ROTA10)  # conftest {} verir; burada gerçek varsayılan
    monkeypatch.setattr(yon, "tara_v10", lambda *a, **k: (_ for _ in ()).throw(KeyboardInterrupt()))
    for ad, anahtar in (("a", True), ("b", False)):
        (kok := tmp_path / ad).mkdir()
        _kurulum(kok, V[:1], sure=300)
        ctx = _ctx(kok, Sahte(kes=1))
        if anahtar:  # O78: anahtar olsun olmasın yeni parti V10 hattıyla açılır (eksik anahtar devam'da DUR)
            ctx["env"]["OMNIROUTE_KEY"] = "x"
        with pytest.raises(KeyboardInterrupt):
            pt.parti(_ns("baslat", kok / "kuyruk.md"), ctx)
        assert _durum(kok).get("yonlendirme") == ROTA10
