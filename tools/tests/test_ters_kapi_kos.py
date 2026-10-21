import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ters"))
import kapi_kos as K  # noqa: E402

HEDEFLER = json.loads((K.DIZ / "hedefler.json").read_text(encoding="utf-8"))["hedefler"]


def test_dotnet_kayitlarinda_derlenmis_var():
    dn = [h for h in HEDEFLER if h["tur"] == "dotnet"]
    assert dn and all(Path(h["derlenmis"]).exists() for h in dn)


def test_bir_hedefin_hatasi_kosuyu_cokertmez(tmp_path, monkeypatch):
    H = [{"id": 1, "ad": "bozuk", "tur": "dotnet"}, {"id": 2, "ad": "iyi", "tur": "js"}]
    (tmp_path / "hedefler.json").write_text(json.dumps({"hedefler": H}), encoding="utf-8")
    (tmp_path / "t").mkdir()
    (tmp_path / "t" / "sayac.json").write_text('{"n": 0}')
    monkeypatch.setattr(K, "DIZ", tmp_path); monkeypatch.setattr(K, "CIKTI", tmp_path / "t"); monkeypatch.setattr(K, "sunucu", lambda: 0)

    def sahte(h, port, sat, atlanan):
        if h["ad"] == "bozuk": raise KeyError("derlenmis")
        for kol in ("skill", "zemin"): sat.append({"id": 2, "ad": "iyi", "tur": "js", "kol": kol, "tekrar": 1, "c1": 1, "c2": 1, "c3": None, "puan": 1, "iddia": 5})
    monkeypatch.setattr(K, "hedef_kos", sahte)
    K.main()
    r = json.loads((tmp_path / "sonuc.json").read_text(encoding="utf-8"))
    assert r["hatalar"][0]["ad"] == "bozuk" and r["atlanan"] == ["bozuk"] and not r["gecti"] and len(r["satirlar"]) == 2


def test_oyla_cogunluk_ve_esitlikte_sifir():
    assert K.oyla([[[1, 1, 0, 0, 1], [0] * 5], [[1, 0, 0, 1, 1], [0] * 5]]) == [[1, 0, 0, 0, 1], [0] * 5]
    assert K.oyla([[[1] * 5, [0] * 5], [[0] * 5, [0] * 5], [[1, 1, 0, 0, 0], [1] * 5]])[0] == [1, 1, 0, 0, 0]


def test_hata_donen_hakem_cagrisi_sayilmaz(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "CIKTI", tmp_path)
    assert K.onbellekli("hakem", "a", lambda: "") == "" and K.onbellekli("hakem", "b", lambda: "ok") == "ok"
    assert json.loads((tmp_path / "sayac-hakem.json").read_text())["n"] == 1


def test_dusen_aile_atlanir_siradaki_aile_kullanilir(tmp_path, monkeypatch):
    monkeypatch.setattr(K, "CIKTI", tmp_path); monkeypatch.setattr(K, "DUSEN", {}); monkeypatch.setattr(K, "KULLANILAN", {})
    cevap = '{"A":[1,1,1,1,1],"B":[0,0,0,0,0]}'
    cagrilan = []

    def sahte(tur, istem, aile=None, **kw):
        cagrilan.append(aile)
        return (None, None, ["429"]) if aile == "meta" else (cevap, aile, [])
    monkeypatch.setattr(K.HAVUZ, "cagir", sahte)
    h = {"ad": "x", "maddeler": [{"madde": str(i)} for i in range(5)]}
    r = K.hakem(h, {"skill": [{"madde": "s"}], "zemin": [{"madde": "z"}]}, K.random.Random(0))
    assert sorted(r.values()) == [0.0, 1.0] and set(K.DUSEN) == {"meta"} and K.KULLANILAN == {"openai": 1, "mistral": 1} and "anthropic" not in cagrilan


def test_ozet_fark_ve_ga():
    sat = [{"ad": a, "kol": k, "puan": p} for a in "xyz" for k, p in (("skill", 0.9), ("skill", 0.8), ("zemin", 0.5), ("zemin", 0.5))]
    o = K.ozet(sat)
    assert abs(o["fark"] - 0.35) < 1e-9 and o["ga"][0] > 0 and abs(o["tekrar_sapma"] - 0.05) < 1e-9


def test_sunucu_kok_verilince_o_dizinden_sunar():
    import urllib.request
    port = K.sunucu("skills/tersine")
    assert b"tersine" in urllib.request.urlopen(f"http://127.0.0.1:{port}/SKILL.md").read().lower()


def test_kapi_kotu_degil_kurali():
    o = lambda f, s, ga: {"fark": f, "tekrar_sapma": s, "ga": ga}
    assert K.kapi({"skill": 0.95, "zemin": 0.80}, o(0.15, 0.02, [0.05, 0.2]), [])  # eski eşik
    assert K.kapi({"skill": 0.80, "zemin": 0.82}, o(-0.02, 0.05, [-0.1, 0.05]), [])  # fark gürültü içinde
    assert not K.kapi({"skill": 0.70, "zemin": 0.82}, o(-0.12, 0.05, [-0.2, -0.04]), [])  # belirgin kötü
    assert not K.kapi({"skill": 0.95, "zemin": 0.80}, o(0.15, 0.02, [0.05, 0.2]), ["x"])  # atlanan varsa geçmez
