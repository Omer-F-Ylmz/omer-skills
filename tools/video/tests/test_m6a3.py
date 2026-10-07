"""MÜKEMMEL-6a3 (K4): 200 + boş içerik JSON/şema hatasından ayrı geçici hata — 2 s, 6 s geri çekilmeli ≤ 2 yeniden deneme;
her deneme çağrı ve usd sayımına girer, bos_yanit sayılır. Sahte çağrıcı; canlı çağrı 0."""
import pytest

import test_f3_v5 as v5
from test_derinlik_kapanis import _g, _orn
from test_f1 import ENV as OENV, SEMA, Omni
from test_f3_v5 import E1, ENV
from video import yonlendir as yon

BOS = {"form": None, "usage": {"input_tokens": 4, "output_tokens": 0}, "usd": 0.001, "sure": 0.1, "hata": "boş yanıt"}


@pytest.fixture(autouse=True)
def _k3(monkeypatch):
    monkeypatch.setattr(yon, "parca_k", lambda p: (3,))
    monkeypatch.setattr(yon, "ANLAMSAL", False)
    monkeypatch.delenv("PARCA_PARALEL", raising=False)


def _bos_tas(c, kac):
    """kac: {"Beta" | "SON": ilk kaç denemesi boş}."""
    t, n = v5._b6(c)(E1, ENV), {}

    def tas(sistem, metin, sema, kareler=(), model=None, **_):
        ad = "SON" if sistem == yon.SON_SISTEM10 else next(x for x in ("Alfa", "Beta", "Gama") if x in metin)
        n[ad] = n.get(ad, 0) + 1
        return dict(BOS) if n[ad] <= kac.get(ad, 0) else t(sistem, metin, sema, kareler, model=model)
    tas.n = n
    return tas


def _kos(tmp_path, tas):
    return yon.tara_v10(_g(tmp_path), ENV, E1, tas=tas, ornek=_orn(tmp_path))


@pytest.mark.parametrize("sec, u", [
    # O99 kanıtı (call_logs 09:47:39Z): OpenRouter upstream 429 OmniRoute zarfında 200; içerik kısmi JSON, token 0
    ({"message": {"role": "assistant", "content": '{"a": "b"'}, "finish_reason": "error",
      "error": {"code": 429, "metadata": {"error_type": "rate_limit_exceeded"}}}, {"prompt_tokens": 0, "completion_tokens": 0}),
    ({"message": {"role": "assistant", "content": ""}, "finish_reason": "stop"}, {"prompt_tokens": 11, "completion_tokens": 0}),
])
def test_omni_bos_yanit_ayri_hata(sec, u):
    y = yon.omni_cagir("gpt-4o-mini", OENV, gonder=Omni(govde={"choices": [sec], "usage": u}))("s", "m", SEMA)
    assert y["form"] is None and y["hata"] == "boş yanıt"


def test_bos_yanit_geri_cekilmeyle_toparlanir(tmp_path, monkeypatch):
    uyku = []
    monkeypatch.setattr(yon.time, "sleep", uyku.append)
    taban = _kos(tmp_path, _bos_tas([], {}))
    y = _kos(tmp_path, t := _bos_tas([], {"Beta": 2, "SON": 1}))
    assert y["hata"] is None and y["form"] == taban["form"] and "son_hata" not in y
    assert y["bos_yanit"] == 3 and y["cagri"] == taban["cagri"] + 3 and t.n == {"Alfa": 1, "Beta": 3, "Gama": 1, "SON": 2}
    assert y["usd"] == pytest.approx(taban["usd"] + 3 * BOS["usd"])
    assert sorted(uyku) == [2, 2, 6] and "parca_yeniden" not in y  # JSON yeniden denemesinden ayrı


def test_bos_yanit_iki_yenidenden_sonra_hata(tmp_path, monkeypatch):
    monkeypatch.setattr(yon.time, "sleep", lambda s: None)
    y = _kos(tmp_path, t := _bos_tas([], {"Beta": 9}))
    assert y["form"] is None and y["hata"] == "parça 2: boş yanıt"
    assert t.n["Beta"] == 3 and y["bos_yanit"] == 2 and y["cagri"] == 5
