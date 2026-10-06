"""F3-HAZIRLIK-2 madde 3: A/B aynı girdi şartı — girdi 4. öğe kareler iki kola birebir aynı gider; omni_cagir her kareyi image_url
(data:<mime>;base64) parçası yapar; omni_yokla(gorsel=True) görselsiz modelde hata döner (model çağrısı yok). Testler sahte, canlı çağrı 0."""
import json
import re
import sys
import types
from pathlib import Path

import pytest

from video import akil, hafif
from video import parti as pt
from video import yonlendir as yon

SEMA = {"type": "object", "required": ["a"], "properties": {"a": {"type": "string"}}}
KOL_B = {"saglayici": "omniroute", "model": "ucuz-model"}
ENV = {"OMNIROUTE_URL": "http://x:1", "OMNIROUTE_KEY": "gizli-anahtar"}


def _tas(gorulen):
    def cagir(sistem, metin, sema, kareler=(), model=None, **_):
        gorulen.append(tuple(kareler))
        return {"form": {"a": metin}, "usage": {"input_tokens": 1, "output_tokens": 1}, "usd": 0.01, "sure": 0, "hata": None}
    return cagir


def test_iki_kol_ayni_kareleri_gorur(monkeypatch):
    a, b = [], []
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _tas(b))
    girdi = [("SİS", "M0", SEMA, ["k1.png", "k2.jpg"]), ("SİS", "M1", SEMA)]
    yon.ab({"model": hafif.MODEL}, "tarama", girdi, KOL_B, _tas(a), {}, lambda ms: [0.8] * len(ms), tavan=8)
    assert a == b == [("k1.png", "k2.jpg")] * 2 + [()] * 2


def _gonder(gorulen):
    def gonder(url, govde, bas):
        gorulen.append(govde)
        return 200, {"choices": [{"message": {"content": '{"a": "x"}'}}], "usage": {}}, {}
    return gonder


def test_omni_cagir_her_kare_image_url(tmp_path):
    ks = [tmp_path / "1.png", tmp_path / "2.jpg"]
    for k in ks:
        k.write_bytes(b"\x89kare")
    g = []
    yon.omni_cagir("m", ENV, _gonder(g))("S", "metin", SEMA, kareler=[str(k) for k in ks])
    parca = g[0]["messages"][1]["content"]
    urls = [p["image_url"]["url"] for p in parca if p["type"] == "image_url"]
    assert len(urls) == 2 and urls[0].startswith("data:image/png;base64,") and urls[1].startswith("data:image/jpeg;base64,")


def test_omni_cagir_karesiz_govde_bugunku_gibi():
    g = []
    yon.omni_cagir("m", ENV, _gonder(g))("S", "metin", SEMA)
    assert g[0]["messages"][1]["content"] == [{"type": "text", "text": "metin"}]


def _getir(kayit):
    gorulen = []

    def getir(url, govde, bas):
        gorulen.append(url)
        return 200, {"data": [{"id": "a/m1"}, {"id": "b/m2", **kayit}]}
    return getir, gorulen


def test_gorselsiz_model_hata_cagri_yok():
    g, gorulen = _getir({"capabilities": {"tools": True}, "input_modalities": ["text"]})
    assert yon.omni_yokla("b/m2", ENV, g, gorsel=True) == "model görsel girdi desteklemiyor: b/m2"
    assert gorulen == ["http://x:1/api/v1/models"]
    assert yon.omni_yokla("b/m2", ENV, g) is None  # varsayılan gorsel=False: bugünkü davranış


def test_gorselli_model_gecer():
    assert yon.omni_yokla("b/m2", ENV, _getir({"capabilities": {"vision": True}})[0], gorsel=True) is None
    assert yon.omni_yokla("b/m2", ENV, _getir({"input_modalities": ["text", "image"]})[0], gorsel=True) is None


# Madde 2: FIYAT gemma-3-4b-it (OpenRouter /api/v1/models, 5 Eki; token başı USD × 1e6) + ab-canli.ps1 ön kontrolleri (çağrı 0).
OR = "https://openrouter.ai/api/v1/models · 2026-10-05"
M = "openrouter/inclusionai/ling-3.0-flash-vl"
BETIK = Path(__file__).resolve().parents[3] / "docs" / "video-tarama" / "ab-canli.ps1"


def test_fiyat_gemma_kaynakli():
    assert yon.FIYAT["openrouter/google/gemma-3-4b-it"] == {"girdi": 0.05, "cikti": 0.1, "kaynak": OR}
    assert yon.FIYAT[M] == {"girdi": 0.021, "cikti": 0.0616, "kaynak": OR}  # aynı listeden doğrulandı, değişmedi


def test_fiyat_nex_usage_cost_ile_uyumlu():
    # F3-MODEL-2 canlı yoklama (5 Eki, Nex AGI): b2QkhmQ0sT0 27 kare, şema geçti; usage 11440/40169 token → usage.cost 0.0043029
    m = "openrouter/nex-agi/nex-n2.5-mini"
    assert "Nex AGI" in yon.FIYAT[m]["kaynak"]
    usd = yon._usd(m, {"prompt_tokens": 11440, "completion_tokens": 40169}, {})
    assert abs(usd - 0.0043029) <= 0.0043029 * 0.10


def test_fiyat_takma_ad_yok():
    assert not [m for m in yon.FIYAT if "/~" in m or ":free" in m or "openrouter/free" in m]


@pytest.mark.parametrize("m", ["openrouter/~deepseek/deepseek-flash-latest", "~deepseek/deepseek-flash-latest",
                               "openrouter/google/gemma-3-4b-it:free", "openrouter/openrouter/free"])
def test_betik_kol_sabit_degil_cagri_yok(monkeypatch, tmp_path, m):
    assert _betik(monkeypatch, tmp_path, m, [], False) == ("hata: kol sabit değil: " + m, [])


def _betik(monkeypatch, tmp_path, model, kareler, gorsel):
    """ab-canli.ps1'in Python gövdesi sahte modüllerle; omni_yokla 'dur' döner (ab'ye inilmez) → (çıkış metni, omni_yokla gorsel değerleri)."""
    paket = tmp_path / "paket.md"
    paket.write_text("p", encoding="utf-8")
    for k, v in {"AB_VIDEO": "v1", "AB_PAKET": str(paket), "AB_MODEL": model}.items():
        monkeypatch.setenv(k, v)
    yokla = []
    monkeypatch.setattr(yon, "omni_yokla", lambda m, env, gorsel=False: yokla.append(gorsel) or "dur")
    monkeypatch.setattr(pt, "paket_oku", lambda p: {"kareler": kareler})
    monkeypatch.setattr(hafif, "GORSEL", gorsel)
    monkeypatch.setitem(sys.modules, "jev", types.SimpleNamespace(cekirdek=None))
    kod = re.search(r"@'\r?\n(.*?)\r?\n'@", BETIK.read_text(encoding="utf-8"), re.S)[1]
    with pytest.raises(SystemExit) as e:
        exec(kod, {"__name__": "__main__"})
    return e.value.code, yokla


def test_betik_fiyat_yok_cagri_yok(monkeypatch, tmp_path):
    assert _betik(monkeypatch, tmp_path, "openrouter/yok/x", [], False) == ("hata: fiyat yok: openrouter/yok/x", [])


def test_betik_gorsel_acik_kare_yok_cagri_yok(monkeypatch, tmp_path):
    assert _betik(monkeypatch, tmp_path, M, [str(tmp_path / "yok.png")], True) == ("hata: kare yok", [])


def test_betik_yokla_gorsel_kareye_gore(monkeypatch, tmp_path):
    k = tmp_path / "1.png"
    k.write_bytes(b"x")
    assert _betik(monkeypatch, tmp_path, M, [str(k)], False) == ("hata: dur", [False])
    assert _betik(monkeypatch, tmp_path, M, [str(k)], True) == ("hata: dur", [True])


# Madde 1: araç kapısı — araç kullanan adım OmniRoute'a gitmez (sec); ab araçlı adımda B kolu kurmaz, çağrı 0, karar DUR (A-A yok).
ARAC = ("WebSearch",)
ROTA = {"arastirma": KOL_B}


def test_sec_aracli_adim_yonlenmez(tmp_path, monkeypatch):
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: pytest.fail("araçlı adım OmniRoute'a gitmemeli"))
    c = object()
    assert yon.sec({"model": hafif.MODEL, "yonlendirme": ROTA}, "arastirma", c, ENV, araclar=ARAC) == (c, hafif.MODEL)
    s = []  # _form_al varsayılan araclar=ARASTIRMA_ARAC → bugünkü taşıyıcı
    akil._form_al(tmp_path, {"model": hafif.MODEL, "butce": 0.5, "tavan": {"usd": 1.0, "cagri": 5}, "yonlendirme": ROTA},
                  lambda *a, **k: s.append(k["model"]) or {"form": {"a": "b"}, "usage": {}, "usd": 0.0, "sure": 0, "hata": None},
                  "s", "m", SEMA, "arastirma", "aday", ENV)
    assert s == [hafif.MODEL]


def test_ab_aracli_adim_dur_cagri_yok(monkeypatch):
    cagri = []
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: cagri.append(m) or _tas(cagri))
    s = yon.ab({"model": hafif.MODEL}, "arastirma", [("S", "M", SEMA)], KOL_B, _tas(cagri), ENV,
               lambda ms: cagri.append(ms) or [0.8] * len(ms), tavan=8, araclar=ARAC)
    assert s == {"karar": "DUR (araç kullanıyor: arastirma)", "yonlendirme": None} and cagri == []


# F3-TEŞHİS-2: kolun bütün çağrıları hatalıysa takas yok, puanla yok → DUR (kol yanıt vermedi); kısmi hata bugünkü gibi; kol başı ilk hata.
HATA = 'HTTP 400: {"message": "Provider returned error gizli-anahtar", "metadata": {"raw": "' + "x" * 200 + '"}}'


def _hatali(hatalar):
    it = iter(hatalar)
    return lambda *a, **k: {"form": None if (h := next(it)) else {"a": "x"}, "usage": {}, "usd": 0.0, "sure": 0, "hata": h}


def test_ab_kol_hep_hatali_dur_puanla_yok(monkeypatch):
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _hatali([HATA, HATA]))
    puan = []
    s = yon.ab({"model": hafif.MODEL}, "tarama", [("S", "M", SEMA)], KOL_B, _tas([]), ENV,
               lambda ms: puan.append(ms) or [0.8] * len(ms), tavan=8)
    ilk = HATA.replace("gizli-anahtar", "***")
    assert s["karar"] == f"DUR (kol yanıt vermedi: b — {ilk[:120]})" and s["yonlendirme"] is None and puan == []
    assert s["b"]["ilk_hata"] == ilk and s["a"]["ilk_hata"] is None and "gizli-anahtar" not in json.dumps(s)


def test_ab_kismi_hata_bugunku_karar_ilk_hata_var(monkeypatch):
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _hatali([None, "zaman aşımı"]))
    s = yon.ab({"model": hafif.MODEL}, "tarama", [("S", "M", SEMA)], KOL_B, _tas([]), ENV, lambda ms: [0.8] * len(ms), tavan=8)
    assert not s["karar"].startswith("DUR") and s["b"]["ilk_hata"] == "zaman aşımı" and s["a"]["ilk_hata"] is None


# F3-HAZIR: B kolu önce (nex ~182 s/çağrı); B'nin bütün çağrıları hatalıysa A hiç çağrılmaz; çıktı biçimi (kol sırası a, b) aynı.
def _sirali(sira, ad, tas):
    return lambda *x, **k: sira.append(ad) or tas(*x, **k)


def test_ab_b_hep_hatali_a_cagrilmaz(monkeypatch):
    sira, b = [], _hatali([HATA, HATA])
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _sirali(sira, "b", b))
    s = yon.ab({"model": hafif.MODEL}, "tarama", [("S", "M", SEMA)], KOL_B, _sirali(sira, "a", _tas([])), ENV,
               lambda ms: [0.8] * len(ms), tavan=8)
    assert sira == ["b", "b"] and s["karar"].startswith("DUR (kol yanıt vermedi: b — ") and list(s)[:2] == ["a", "b"]


def test_ab_b_once_cagrilir_bicim_ayni(monkeypatch):
    sira = []
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _sirali(sira, "b", _tas([])))
    s = yon.ab({"model": hafif.MODEL}, "tarama", [("S", "M", SEMA)], KOL_B, _sirali(sira, "a", _tas([])), ENV,
               lambda ms: [0.8] * len(ms), tavan=8)
    assert sira == ["b", "b", "a", "a"] and list(s)[:2] == ["a", "b"] and not s["karar"].startswith("DUR")


def test_omni_cagir_vision_bridge_kapali_basligi():
    bas = []
    yon.omni_cagir("m", ENV, lambda u, g, b: bas.append(b) or (200, {"choices": [{"message": {"content": "{}"}}]}, {}))("S", "m", SEMA)
    assert bas[0]["x-omniroute-disabled-guardrails"] == "vision-bridge"


def test_betik_kol_satiri_ilk_hata(monkeypatch, tmp_path, capsys):
    paket = tmp_path / "paket.md"
    paket.write_text("p", encoding="utf-8")
    for k, v in {"AB_VIDEO": "v1", "AB_PAKET": str(paket), "AB_MODEL": M}.items():
        monkeypatch.setenv(k, v)
    monkeypatch.setattr(yon, "omni_yokla", lambda m, env, gorsel=False: None)
    monkeypatch.setattr(hafif, "GORSEL", False)
    monkeypatch.setattr(yon, "ab", lambda *a, **k: {"karar": "DUR (kol yanıt vermedi: b — HTTP 400)", "yonlendirme": None,
                                                    "a": {"model": "A", "ilk_hata": None}, "b": {"model": M, "ilk_hata": "HTTP 400"}})
    monkeypatch.setitem(sys.modules, "jev", types.SimpleNamespace(cekirdek=types.SimpleNamespace(Tasiyici=lambda **k: None)))
    exec(re.search(r"@'\r?\n(.*?)\r?\n'@", BETIK.read_text(encoding="utf-8"), re.S)[1], {"__name__": "__main__"})
    satir = [l for l in capsys.readouterr().out.splitlines() if l.startswith("b ")]
    assert satir == [f"b {M} ilk_hata HTTP 400"]


def _zaman_asimi(monkeypatch, gorulen):
    def urlopen(r, timeout=None):
        gorulen.append(timeout)
        raise TimeoutError("timed out")
    monkeypatch.setattr("urllib.request.urlopen", urlopen)


def test_omniroute_yolu_gercek_post_600s_zaman_asimi(monkeypatch):
    """F3-SÜRE: SAGLAYICI['omniroute'] → omni_cagir varsayılan gonder = ig._post; urlopen'a geçen değer 600, TimeoutError hata alanında."""
    t = []
    _zaman_asimi(monkeypatch, t)
    y = yon.SAGLAYICI["omniroute"]("m", ENV)("S", "metin", SEMA)
    assert t == [600] and y["form"] is None and y["hata"] == "ölçülemedi: TimeoutError: timed out"


def test_omni_cagir_zaman_asiminda_usd_bilinmiyor(monkeypatch):
    """F3-SÜRE adım 3: zaman aşımında upstream faturalamış olabilir → usd None (0 harcama sayılmaz)."""
    _zaman_asimi(monkeypatch, [])
    assert yon.omni_cagir("m", ENV)("S", "metin", SEMA)["usd"] is None
