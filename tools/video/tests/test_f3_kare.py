"""F3-HAZIRLIK-2 madde 3: A/B aynı girdi şartı — girdi 4. öğe kareler iki kola birebir aynı gider; omni_cagir her kareyi image_url
(data:<mime>;base64) parçası yapar; omni_yokla(gorsel=True) görselsiz modelde hata döner (model çağrısı yok). Testler sahte, canlı çağrı 0."""
import re
import sys
import types
from pathlib import Path

import pytest

from video import hafif
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
