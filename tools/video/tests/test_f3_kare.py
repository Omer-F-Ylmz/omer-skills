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


@pytest.mark.parametrize("m, g, c", [("openai/gpt-6-luna", 0.1, 0.5), ("cohere/command-a-plus", 0.3, 1.5), ("qwen/qwen3.7-plus", 0.32, 1.28),
                                     ("mistralai/mistral-large-2512", 0.5, 1.5), ("google/gemini-3.5-flash-lite", 0.3, 2.5)])
def test_fiyat_eleme_adaylari_kaynakli_bantta(m, g, c):
    # F3-ELEME adım 3: OpenRouter listesi (6 Eki); tahmini çağrı = girdi × 15k + çıktı × 6k (+ 27 × gorsel) ≤ $0.02
    f = yon.FIYAT["openrouter/" + m]
    assert (f["girdi"], f["cikti"]) == (g, c) and f["kaynak"] == "https://openrouter.ai/api/v1/models · 2026-10-06"
    assert (g * 15000 + c * 6000) / 1e6 + 27 * f.get("gorsel", 0) <= 0.02


def test_usd_gorsel_kare_basi():
    m = "openrouter/google/gemini-3.5-flash-lite"
    assert yon.FIYAT[m]["gorsel"] == 3e-7  # pricing.image $/görsel
    assert yon._usd(m, {"prompt_tokens": 1000, "completion_tokens": 100}, {}, kare=27) == pytest.approx((1000 * 0.3 + 100 * 2.5) / 1e6 + 27 * 3e-7)


def test_omni_cagir_kare_sayisi_usd_ye(tmp_path):
    ks = [tmp_path / "1.png", tmp_path / "2.png"]
    for k in ks:
        k.write_bytes(b"kare")
    y = yon.omni_cagir("openrouter/google/gemini-3.5-flash-lite", ENV, _gonder([]))("S", "metin", SEMA, kareler=[str(k) for k in ks])
    assert y["usd"] == pytest.approx(2 * 3e-7)


def test_usd_onbellek_ikinci_kez_sayilmaz():
    # O57 id5: OmniRoute tokens_input 22832 = 11440 + cache_read 11392 (aynı girdi sha256); prompt_tokens önbelleği zaten içerir, eklenmez
    u = {"prompt_tokens": 11440, "completion_tokens": 0, "prompt_tokens_details": {"cached_tokens": 11392}}
    assert yon._usd("openrouter/nex-agi/nex-n2.5-mini", u, {}) == pytest.approx(11440 * 0.025 / 1e6)


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


# F3-ELEME adım 2: çıktı tavanı (O57 kaçak üretim 131072) — max_tokens 32768; finish_reason "length" → form None, usd FIYAT'tan (faturalandı).
def test_omni_cagir_max_tokens_32768():
    g = []
    yon.omni_cagir("m", ENV, _gonder(g))("S", "metin", SEMA)
    assert g[0]["max_tokens"] == 32768


def test_omni_cagir_cikti_tavani_hata_usd_fiyattan():
    m = "openrouter/nex-agi/nex-n2.5-mini"
    y = yon.omni_cagir(m, ENV, lambda u, g, b: (200, {"choices": [{"finish_reason": "length", "message": {"content": '{"a": "x"}'}}],
                                                       "usage": {"prompt_tokens": 1000, "completion_tokens": 32768}}, {}))("S", "metin", SEMA)
    assert y["form"] is None and y["hata"] == "çıktı tavanı (max_tokens 32768)"
    assert y["usd"] == pytest.approx((1000 * 0.025 + 32768 * 0.1) / 1e6)


# F3-ELEME adım 2: A kolu önbelleği — anahtar sistem+metin+şema+kare içerikleri, model, tekrar sırası; kayıt varsa A çağrılmaz; B önbelleğe girmez.
def _ab_onbellekli(monkeypatch, tmp_path, a, b, model=hafif.MODEL):
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _tas(b))
    return yon.ab({"model": model}, "tarama", [("S", "M", SEMA, [str(tmp_path / "1.png")])], KOL_B, _tas(a), ENV,
                  lambda ms: [0.8] * len(ms), tavan=8, onbellek=tmp_path / "ab")


def test_ab_a_onbellek_isabet_a_cagri_0_b_cagrilir(monkeypatch, tmp_path):
    (tmp_path / "1.png").write_bytes(b"kare")
    a1, a2, b = [], [], []
    _ab_onbellekli(monkeypatch, tmp_path, a1, b)
    s = _ab_onbellekli(monkeypatch, tmp_path, a2, b)
    assert len(a1) == 2 and a2 == [] and len(b) == 4 and not s["karar"].startswith("DUR") and s["a"]["kalite"] == 0.8


def test_ab_a_onbellek_anahtar_kare_ve_model(monkeypatch, tmp_path):
    (tmp_path / "1.png").write_bytes(b"kare")
    _ab_onbellekli(monkeypatch, tmp_path, [], [])
    (tmp_path / "1.png").write_bytes(b"baska kare")
    a = []
    _ab_onbellekli(monkeypatch, tmp_path, a, [])
    m = []
    _ab_onbellekli(monkeypatch, tmp_path, m, [], model="baska-model")
    assert len(a) == 2 and len(m) == 2


def test_ab_a_hatali_yanit_onbellege_girmez(monkeypatch, tmp_path):
    (tmp_path / "1.png").write_bytes(b"kare")
    monkeypatch.setitem(yon.SAGLAYICI, "omniroute", lambda m, env: _tas([]))
    yon.ab({"model": hafif.MODEL}, "tarama", [("S", "M", SEMA, [str(tmp_path / "1.png")])], KOL_B, _hatali(["x", "x"]), ENV,
           lambda ms: [0.8] * len(ms), tavan=8, onbellek=tmp_path / "ab")
    a = []
    _ab_onbellekli(monkeypatch, tmp_path, a, [])
    assert len(a) == 2


# F3-ELEME adım 4: yon.eleme — aday başı çağrı 1, şema geçerse 2 (240 s); ön kontrol · tavanlar · reasoning · A önbelleği · karar + öneri.
E1, E2 = "openrouter/openai/gpt-6-luna", "openrouter/qwen/qwen3.7-plus"
IYI = {"form": {"a": "x"}, "usage": {"input_tokens": 10, "output_tokens": 5}, "usd": 0.001, "sure": 1.0, "hata": None}


def _b_kur(cagri, yanit=None, kur_=None):
    def kur(m, env, timeout=600, govde_ek=None):
        if kur_ is not None:
            kur_.append((m, timeout, govde_ek))
        return lambda sistem, metin, sema, kareler=(), model=None, **_: cagri.append(m) or (yanit or {}).get(m, IYI)
    return kur


def _eleme(tmp_path, adaylar, b, a=None, puan=None, yokla=lambda m, env, gorsel=False: None, **k):
    return yon.eleme(("S", "M", SEMA, []), adaylar, _tas([] if a is None else a), hafif.MODEL, ENV, puan or (lambda ms: [0.8] * len(ms)),
                     onbellek=tmp_path / "ab", b_kur=b, yokla=yokla, **k)


def test_eleme_on_kontrol_cagri_0(tmp_path):
    c, y, a = [], [], []
    s = _eleme(tmp_path, ["openrouter/~x/y", "openrouter/yok/x", E1], _b_kur(c), a,
               yokla=lambda m, env, gorsel=False: y.append(m) or "model yok: " + m)
    assert c == [] and y == [E1] and a == [] and s["oneri"].startswith("öneri: yok")
    assert s["satirlar"] == ["openrouter/~x/y · hata: kol sabit değil · çağrı 0", "openrouter/yok/x · hata: fiyat yok · çağrı 0",
                             f"{E1} · hata: model yok: {E1} · çağrı 0"]


def test_eleme_aday_tavani(tmp_path):
    c = []
    assert _eleme(tmp_path, [E1] * 6, _b_kur(c))["oneri"] == "TAVAN aday 6 > 5" and c == []


def test_eleme_harcama_tavani_sonraki_cagri_yok(tmp_path):
    c, pahali = [], {**IYI, "usd": 0.06}
    s = _eleme(tmp_path, [E1, E2], _b_kur(c, {E1: pahali, E2: pahali}))
    # E1 0.06 + 0.06; E2 ilk çağrı tahmini (15k×0.32 + 6k×1.28)/1e6 ≈ 0.0125 → 0.1325 ≤ 0.15 yapılır; ikincisi 0.18 + 0.06 > 0.15 → tavan
    assert c == [E1, E1, E2] and s["satirlar"][1].endswith(" · tavan") and s["b_usd"] == pytest.approx(0.18)


def test_eleme_cagri_tavani(tmp_path):
    c = []
    s = _eleme(tmp_path, [E1, E2], _b_kur(c), tavan_cagri=3)
    assert c == [E1, E1, E2] and s["satirlar"][1].endswith(" · tavan")


def test_eleme_zaman_asimi_240_gecer(tmp_path):
    k = []
    _eleme(tmp_path, [E1], _b_kur([], kur_=k))
    assert k == [(E1, 240, None)]


def test_post_ve_omni_cagir_timeout_gecer(monkeypatch):
    from video import ikinci_goz as ig
    t = []
    _zaman_asimi(monkeypatch, t)
    with pytest.raises(TimeoutError):
        ig._post("http://x:1", None, {}, timeout=240)
    assert yon.omni_cagir("m", ENV, timeout=240)("S", "metin", SEMA)["hata"] == "ölçülemedi: TimeoutError: timed out" and t == [240, 240]


def test_eleme_sema_hatasi_ikinci_cagri_yok_a_cagrilmaz(tmp_path):
    c, a = [], []
    s = _eleme(tmp_path, [E1], _b_kur(c, {E1: {**IYI, "form": {"b": 1}}}), a)
    assert c == [E1] and a == [] and " · hata: şema geçmedi · " in s["satirlar"][0] and s["satirlar"][0].endswith(" · ELENDİ")


def test_eleme_reasoning_istenir_etkisizse_isaret(tmp_path):
    k, akil = [], {**IYI, "usage": {"input_tokens": 10, "output_tokens": 5, "reasoning": 1500}}  # F3-VARYANT: işaret yalnız > 1000
    s = _eleme(tmp_path, [E1, E2], _b_kur([], {E1: akil}, k), destek={E1: ["reasoning", "max_tokens"], E2: ["max_tokens"]})
    assert k == [(E1, 240, {"reasoning": {"effort": "minimal"}}), (E2, 240, None)]
    assert s["satirlar"][0].endswith(" · reasoning parametresi etkisiz") and "etkisiz" not in s["satirlar"][1]
    assert " · token 20/10/3000 · " in s["satirlar"][0]


def test_omni_cagir_govde_ek_ve_reasoning_token():
    g = []
    y = yon.omni_cagir("m", ENV, lambda u, gv, b: g.append(gv) or (200, {"choices": [{"message": {"content": '{"a": "x"}'}}], "usage": {
        "prompt_tokens": 1, "completion_tokens": 2, "completion_tokens_details": {"reasoning_tokens": 7}}}, {}),
        govde_ek={"reasoning": {"effort": "minimal"}})("S", "metin", SEMA)
    assert g[0]["reasoning"] == {"effort": "minimal"} and y["usage"] == {"input_tokens": 1, "output_tokens": 2, "reasoning": 7}


def test_eleme_a_onbellek_isabet_a_cagri_0(tmp_path):
    a1, a2 = [], []
    s1 = _eleme(tmp_path, [E1], _b_kur([]), a1)
    s2 = _eleme(tmp_path, [E1], _b_kur([]), a2)
    assert len(a1) == 2 and a2 == [] and s1["a_usd"] == pytest.approx(0.02) and s2["a_usd"] == 0


def test_eleme_karar_ve_oneri(tmp_path):
    s = _eleme(tmp_path, [E1, E2], _b_kur([], {E2: {**IYI, "usd": 0.0005}}))  # kalite eşit → ucuz olan
    assert all(" · AL" in r for r in s["satirlar"]) and s["oneri"].startswith(f"öneri: {E2} ")
    s = _eleme(tmp_path, [E1, E2], _b_kur([], {E2: {**IYI, "usd": 0.0005}}), puan=lambda ms: [0.8, 0.8, 0.9, 0.9, 0.8, 0.8])  # sıra A, E1, E2
    assert s["oneri"].startswith(f"öneri: {E1} ") and " · kalite 0.90 · başarı 1.00 · AL" in s["satirlar"][0]


def test_eleme_betik_girdi_ve_cikti(monkeypatch, tmp_path, capsys):
    from video import ikinci_goz as ig
    p = tmp_path / "vid1" / "paket.md"
    p.parent.mkdir()
    p.write_text("p", encoding="utf-8")
    monkeypatch.setenv("AB_PAKET", str(p))
    monkeypatch.setenv("ELEME_ADAYLAR", f" {E1}, {E2} ")
    monkeypatch.setattr(hafif, "GORSEL", False)
    monkeypatch.setattr(ig, "_post", lambda u, g, b: (200, {"data": [{"id": "openai/gpt-6-luna", "supported_parameters": ["reasoning"]}]}))
    g = []
    monkeypatch.setattr(yon, "eleme", lambda *a, **k: g.append((a, k)) or {"satirlar": ["r1"], "oneri": "öneri: yok", "a_usd": 0.0, "b_usd": 0.0})
    monkeypatch.setitem(sys.modules, "jev", types.SimpleNamespace(cekirdek=types.SimpleNamespace(Tasiyici=lambda **k: None)))
    exec(re.search(r"@'\r?\n(.*?)\r?\n'@", BETIK.with_name("eleme.ps1").read_text(encoding="utf-8"), re.S)[1], {"__name__": "__main__"})
    (a, k), = g
    assert a[0][1].startswith("=== VIDEO vid1 ===\n") and a[1] == [E1, E2] and k["onbellek"] == tmp_path / "ab"
    assert k["destek"] == {E1: ["reasoning"]}
    assert capsys.readouterr().out.splitlines()[-3:] == ["r1", "öneri: yok", "toplam: A $0.0000 · B $0.0000 · Jev ≤4 istek (usd ölçülmüyor)"]


# F3-VARYANT
def _b_kayit(c, yanit=None):
    def kur(m, env, timeout=600, govde_ek=None):
        def tas(sistem, metin, sema, kareler=(), model=None, **_):
            c.append({"m": m, "sistem": sistem, "kareler": list(kareler), "govde_ek": govde_ek})
            return (yanit or {}).get(m, IYI)
        return tas
    return kur


def _v(tmp_path, adaylar, c, kareler=(), **k):
    return yon.eleme(("S", "=== VIDEO vid1 ===\nM", SEMA, list(kareler)), adaylar, _tas([]), hafif.MODEL, ENV,
                     k.pop("puanla", lambda ms: [0.8] * len(ms)), onbellek=tmp_path / "ab", b_kur=_b_kayit(c),
                     yokla=lambda m, env, gorsel=False: None, **k)


def test_eleme_varyant_ayristirma_bilinmeyen_cagri_0(tmp_path):
    c = []
    s = _v(tmp_path, [E1, f"{E1}@V0", f"{E1}@V9"], c)
    assert [x["m"] for x in c] == [E1] * 4
    assert s["satirlar"][0].startswith(f"{E1} · geçti") and s["satirlar"][1].startswith(f"{E1}@V0 · geçti")
    assert s["satirlar"][2] == f"{E1}@V9 · hata: bilinmeyen varyant: V9 · çağrı 0"


def test_eleme_v1_ornek_govdede_test_videosu_disindan(tmp_path):
    c, o = [], tmp_path / "ORN1.json"
    o.write_text('{"id": "ORN1", "ozet": "x"}', encoding="utf-8")
    _v(tmp_path, [f"{E1}@V1", E2], c, ornek=o)
    assert c[0]["sistem"].startswith("S\n") and '"id": "ORN1"' in c[0]["sistem"] and c[2]["sistem"] == "S"
    (tmp_path / "vid1.json").write_text('{"id": "vid1"}', encoding="utf-8")
    c = []
    s = _v(tmp_path, [f"{E1}@V1"], c, ornek=tmp_path / "vid1.json")
    assert c == [] and s["satirlar"] == [f"{E1}@V1 · hata: V1 örneği test videosundan (vid1) · çağrı 0"]
    assert _v(tmp_path, [f"{E1}@V1"], c)["satirlar"] == [f"{E1}@V1 · hata: V1 örneği yok · çağrı 0"] and c == []


def test_eleme_v3_effort_low_desteksizse_cagri_0(tmp_path):
    c = []
    s = _v(tmp_path, [f"{E1}@V3", f"{E2}@V3", E1], c, destek={E1: ["reasoning"], E2: []})
    assert [x["govde_ek"] for x in c] == [{"reasoning": {"effort": "low"}}] * 2 + [{"reasoning": {"effort": "minimal"}}] * 2
    assert s["satirlar"][1] == f"{E2}@V3 · hata: V3: reasoning desteklenmiyor · çağrı 0"


def test_eleme_v4_kucuk_kare_27_dosyalar_degismez(tmp_path):
    ks = []
    for i in range(27):
        (k := tmp_path / f"k{i:02}.png").write_bytes(b"orj%d" % i)
        ks.append(k)
    c, kc = [], []
    _v(tmp_path, [f"{E1}@V4", E2], c, kareler=ks, kucult=lambda kl, d: kc.append(d) or [d / Path(x).name for x in kl])
    assert len(c[0]["kareler"]) == 27 and all(Path(x).parent == kc[0] for x in c[0]["kareler"])
    assert c[2]["kareler"] == ks and all(k.read_bytes() == b"orj%d" % i for i, k in enumerate(ks))


def _png(p, w, h):
    import struct, zlib
    blok = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + blok(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                  + blok(b"IDAT", zlib.compress(b"".join(b"\0" + b"\x80" * 3 * w for _ in range(h)))) + blok(b"IEND", b""))


def test_kucult_uzun_kenar_512(tmp_path):
    import struct
    _png(tmp_path / "a.png", 1024, 600)
    _png(tmp_path / "b.png", 300, 200)
    cik = yon._kucult([tmp_path / "a.png", tmp_path / "b.png"], tmp_path / "k")
    boy = [struct.unpack(">II", Path(x).read_bytes()[16:24]) for x in cik]
    assert boy == [(512, 300), (300, 200)] and struct.unpack(">II", (tmp_path / "a.png").read_bytes()[16:24]) == (1024, 600)


def test_eleme_kayit_yanit_ve_jev_gerekce(tmp_path):
    c, k = [], tmp_path / "kayit"
    s = _v(tmp_path, [E1, f"{E2}@V3"], c, kayit=k, puanla=lambda ms: [{"score": 0.8, "reasoning": "r"}] * len(ms))
    a0 = json.loads((k / "A" / "0.json").read_text(encoding="utf-8"))
    b1 = json.loads((k / "openrouter_openai_gpt-6-luna" / "1.json").read_text(encoding="utf-8"))
    assert a0["puan"] == {"score": 0.8, "reasoning": "r"} and b1["yanit"]["form"] == {"a": "x"} and b1["puan"]["score"] == 0.8
    assert " · kalite 0.80 · " in s["satirlar"][0]


def test_alan_farki():
    sema = {"type": "object", "properties": {"a": {"type": "string"}, "l": {"type": "array", "items": {"type": "object", "properties": {
        "t": {"type": "string"}}}}, "bos": {"type": "string"}, "eksik": {"type": "string"}}}
    r = yon.alan_farki([{"a": "xxxx", "l": [{"t": "yy"}, {"t": "z"}, {"t": ""}], "bos": "q"}], [{"a": "x", "l": [], "bos": None}], sema)
    assert "boş alan A 1.0 → B 2.0" in r["ozet"] and "şemada yok: eksik, l[].t" in r["ozet"]
    assert "en çok fark: l 3.0→0.0, l[].t 3.0→0.0, bos 1.0→0.0, a 4.0→1.0" in r["ozet"]
    assert "| l | 3.0 | 0.0 | 100 |" in r["satirlar"]


def test_eleme_rapor_aday_basi(tmp_path):
    s = _v(tmp_path, [E1], [])
    assert set(s["rapor"]) == {E1} and "en çok fark: a " in s["rapor"][E1]["ozet"]


def test_eleme_girdi_onbellek_dahil(tmp_path):
    a = lambda *x, **k: {**IYI, "usage": {"input_tokens": 2, "cache_read_input_tokens": 100, "cache_creation_input_tokens": 898,
                                          "output_tokens": 5}, "usd": 0.01}
    s = yon.eleme(("S", "M", SEMA, []), [E1], a, hafif.MODEL, ENV, lambda ms: [0.8] * len(ms), onbellek=tmp_path / "ab",
                  b_kur=_b_kayit([]), yokla=lambda m, env, gorsel=False: None)
    assert " · girdi −%99.0" in s["satirlar"][0]


def test_karar_a_girdi_0_yuzde_yazilmaz():
    from video import kur
    a = {"kalite": 0.8, "basari": 1.0, "girdi": 0, "cikti": 10, "maliyet": 0.1}
    assert "girdi" not in kur.karar(a, {**a, "girdi": 50, "maliyet": 0.01}, None, 0, [])


def test_eleme_reasoning_1000_alti_isaret_yok(tmp_path):
    s = _eleme(tmp_path, [E1], _b_kur([], {E1: {**IYI, "usage": {"input_tokens": 10, "output_tokens": 5, "reasoning": 1000}}}),
               destek={E1: ["reasoning"]})
    assert "etkisiz" not in s["satirlar"][0]


@pytest.mark.parametrize("ad", ["eleme.ps1", "ab-canli.ps1"])
def test_ps1_python_borusu_utf8(ad):
    t = BETIK.with_name(ad).read_text(encoding="utf-8")
    assert "$OutputEncoding = [Text.UTF8Encoding]::new($false)" in t.split("@'")[0]


def test_fiyat_ref_kaynakli():
    assert yon.FIYAT["openrouter/google/gemini-3.8-flash"]["kaynak"].startswith("https://openrouter.ai/api/v1/models")
