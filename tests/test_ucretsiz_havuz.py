import sys, time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ucretsiz_havuz as H  # noqa: E402


@pytest.fixture(autouse=True)
def izole(tmp_path, monkeypatch):
    monkeypatch.setattr(H, "DIZIN", tmp_path); monkeypatch.setattr(H, "DURUM", tmp_path / "durum.json")
    monkeypatch.setattr(H, "_anahtar", lambda k: "x" * 12)
    monkeypatch.setattr(H, "_omni_serbest", lambda: True)


def sahte(monkeypatch, davranis):
    cagrilar = []

    def istek(e, istem, mt, z):
        cagrilar.append(H.ad(e)); return davranis(e)
    monkeypatch.setattr(H, "_istek", istek); return cagrilar


def test_429_bekleme_yok_sonrakine_gecer(monkeypatch):
    def d(e):
        if e.prov == "gemini": raise H.Hata(429, "per minute", 30)
        return "tamam"
    c = sahte(monkeypatch, d); t = time.time()
    y, k, log = H.cagir("hakem", "x")
    assert y == "tamam" and not k.startswith("gemini") and time.time() - t < 1
    assert any(":429" in l for l in log) or not c[0].startswith("gemini")


def test_soguma_atlar_ve_dolunca_tek_deneme(monkeypatch):
    e = next(x for x in H.ENT if x.prov == "gemini")
    H._dus(e, H.Hata(503, "x"))
    assert H._durum()["soguma"][H.ad(e)] > time.time()
    d = H._durum(); d["soguma"][H.ad(e)] = time.time() - 1; H._yaz(d)  # süre doldu
    assert H._sec("hakem", 100, "google", None, set()).model == e.model
    H._dus(e, H.Hata(503, "x"))  # tek deneme yine düştü → süre katlanır
    assert H._durum()["soguma"][H.ad(e)] - time.time() > 200


def test_200_ama_hata_govdesi_ve_bos_yanit_dusurulur(monkeypatch):
    import io, json, urllib.request
    gov = iter([{"error": {"code": 429, "message": "kota"}}, {"choices": []}, {"choices": [{"message": {"content": "  "}}]},
                {"choices": [{"message": {"content": "iyi"}, "finish_reason": "stop"}]}])
    class R(io.BytesIO):
        def __enter__(self): return self
        def __exit__(self, *a): pass
    monkeypatch.setattr(urllib.request, "urlopen", lambda q, timeout: R(json.dumps(next(gov)).encode()))
    e = H.ENT[0]
    for kod in (429, 502, 0):
        with pytest.raises(H.Hata) as x: H._istek(e, "s", 10, 5)
        assert x.value.kod == kod
    assert H._istek(e, "s", 10, 5) == "iyi"


def test_dogrula_reddi_sonraki_halkaya(monkeypatch):
    c = sahte(monkeypatch, lambda e: "kisa" if len(c_) == 0 else "uzun yanit"); c_ = []
    sahte_c = []
    def d(e):
        sahte_c.append(1); return "kisa" if len(sahte_c) == 1 else "uzun yanit"
    sahte(monkeypatch, d)
    y, k, log = H.cagir("hakem", "x", dogrula=lambda m: "kisa" if m == "kisa" else None)
    assert y == "uzun yanit" and len(log) == 1


def test_aile_ve_haric(monkeypatch):
    c = sahte(monkeypatch, lambda e: "ok")
    assert H.cagir("hakem", "x", aile="openai")[1].startswith(("groq/openai",))
    assert not H.cagir("hakem", "x", haric_aile="google")[1].endswith(("flash", "lite"))
    r = H.iki_aile("hakem", "x")
    assert len(r) == 2 and r[0][2] != r[1][2]


def test_dagitim_tek_saglayiciyi_tuketmez(monkeypatch):
    sahte(monkeypatch, lambda e: "ok")
    sayim = {}
    for _ in range(40):
        p = H.cagir("hakem", "x")[1].split("/")[0]; sayim[p] = sayim.get(p, 0) + 1
    assert max(sayim.values()) <= 20 and len(sayim) >= 3


def test_rpm_kovasi_dolunca_atlar(monkeypatch):
    c = sahte(monkeypatch, lambda e: "ok")
    for _ in range(80): H.cagir("ozet", "x")
    d = H._durum()
    assert all(len([x for x in v if x[0] > time.time() - 60]) <= 25 for v in d["dk"].values())


def test_haiku_yalniz_tavanla(monkeypatch):
    sahte(monkeypatch, lambda e: (_ for _ in ()).throw(H.Hata(503, "x")))
    monkeypatch.setattr(H, "_haiku", lambda i: "h")
    assert H.cagir("ozet", "x")[0] is None  # tavan 0 → Haiku yok
    assert H.cagir("ozet", "x", haiku_tavan=1, etiket="t")[1] == "haiku/claude-haiku-5-5"
    assert H.cagir("ozet", "x", haiku_tavan=1, etiket="t")[0] is None  # tavan doldu


def test_anahtar_sizmaz(monkeypatch):
    H._ANAHTAR["k"] = "gizliDEGER123456"
    assert "gizli" not in H._gizle("hata gizliDEGER123456 bitti")
    H._ANAHTAR.pop("k")
