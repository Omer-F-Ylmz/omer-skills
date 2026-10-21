import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ordu  # noqa: E402


def test_sinif_kademe():
    assert ordu.sinif("dosyaları listele")["kademe"] == "T1"
    assert ordu.sinif("dosyaları listele")["capraz"] is False
    assert ordu.sinif("özet çıkar")["capraz"] is True
    assert ordu.sinif("küçük bug düzelt")["kademe"] == "T2"
    assert ordu.sinif("çok dosyalı mimari")["kademe"] == "T4"
    assert ordu.sinif("bilinmeyen iş")["sinif"] == "zor"


def test_boyut_risk_artirir_ama_imkansiz_yapmaz():
    assert ordu.sinif("dosyaları listele", "buyuk")["sinif"] == "orta"
    assert ordu.sinif("dosyaları listele", "buyuk", ["guvenlik"])["sinif"] == "zor"
    assert ordu.sinif("küçük bug düzelt", "buyuk", ["guvenlik"])["sinif"] == "zor"
    assert ordu.sinif("dosyaları listele", "kucuk", ["guvenlik"])["dogrulama"] == "full"


def test_kapi():
    a = {"claude_token": 1000, "kalite": 0.9, "basarisiz": 1}
    assert ordu.kapi(a, {"claude_token": 500, "kalite": 0.9, "basarisiz": 1})
    assert not ordu.kapi(a, {"claude_token": 501, "kalite": 0.9, "basarisiz": 1})
    assert not ordu.kapi(a, {"claude_token": 400, "kalite": 0.8, "basarisiz": 1})
    assert not ordu.kapi(a, {"claude_token": 400, "kalite": 0.9, "basarisiz": 2})


def test_heldout_etiketleri_gecerli():
    assert len(ordu.HELDOUT) == 20 and all(e in ordu.SINIF for _, e in ordu.HELDOUT)


def test_merdiven_omer_sirasi():
    assert [b["ad"] for b in ordu.MERDIVEN] == ["ucretsiz", "haiku-medium", "haiku-high", "sonnet-medium", "sonnet-high",
                                                "opus-medium", "opus-high"]
    assert [(b["model"].split("-")[1] if "-" in b["model"] else b["model"], b["effort"]) for b in ordu.MERDIVEN[1:]] == [
        ("haiku", "medium"), ("haiku", "high"), ("sonnet", "medium"), ("sonnet", "high"), ("opus", "medium"), ("opus", "high")]
    assert [ordu.BASLA[s] for s in ordu.SINIF] == [0, 0, 3, 5]


def _kayit(tmp_path, monkeypatch):
    monkeypatch.setattr(ordu.yonlendir, "KAYIT", tmp_path / "kayit.jsonl")
    monkeypatch.setattr(ordu.yonlendir, "SIRA", tmp_path / "SIRA.md")


def test_merdiven_kos_kaskad_ve_ogrenme(tmp_path, monkeypatch):
    _kayit(tmp_path, monkeypatch)
    gidilen = []
    cikti, i = ordu.merdiven_kos("etiket", "orta", lambda b: (gidilen.append(b["ad"]) or b["ad"], {}), lambda c, b: b["ad"] == "haiku-high")
    assert (cikti, i) == ("haiku-high", 2) and gidilen == ["ucretsiz", "haiku-medium", "haiku-high"]
    ordu.merdiven_kos("etiket", "orta", lambda b: (b["ad"], {}), lambda c, b: b["ad"] == "haiku-high")  # ikinci kayıt → öğrenme açılır
    assert ordu.basla("etiket", "orta") == 2
    assert ordu.basla("baska-tur", "orta") == 0  # kayıt yok → sınıf başlangıcı


def test_merdiven_tukenince_sira_satiri(tmp_path, monkeypatch):
    _kayit(tmp_path, monkeypatch)
    assert ordu.merdiven_kos("x", "zor", lambda b: ("", {}), lambda c, b: False, "is1") == (None, 6)
    assert "ORDU-1 MERDİVEN TÜKENDİ: is1" in (tmp_path / "SIRA.md").read_text(encoding="utf-8")
    assert (tmp_path / "SIRA.md").read_text(encoding="utf-8").endswith("bakmalı\n")


def test_kapi3_uc_olcut_birlikte():
    a = {"claude_is": 20, "agirlikli_token": 1000, "kalite": 1.0}
    assert ordu.kapi3(a, {"claude_is": 10, "agirlikli_token": 600, "kalite": 1.0})
    assert not ordu.kapi3(a, {"claude_is": 11, "agirlikli_token": 600, "kalite": 1.0})
    assert not ordu.kapi3(a, {"claude_is": 10, "agirlikli_token": 601, "kalite": 1.0})
    assert not ordu.kapi3(a, {"claude_is": 10, "agirlikli_token": 600, "kalite": 0.95})


def test_agirlik_model_sirasi():
    assert ordu.AGIRLIK["haiku"] < ordu.AGIRLIK["sonnet"] == 1 < ordu.AGIRLIK["opus"]


def test_norm_json_dizgesi_ve_bicim():
    assert ordu.norm('```json\n{"a": " X  y."}\n```') == {"a": "x y"}
    assert ordu.norm('{"1":"a"}') == ordu.norm({"1": "a"})


def test_kabul_bayrak_kapali_birebir_ayni():
    assert ordu.kabul(["a", "a"], gevsek=False) == "a"
    assert ordu.kabul(['{"1":"a"}', {"1": "a"}], hakem_=lambda a, b: True, gevsek=False) is None


def test_kabul_gevsek_normalize_ve_hakem():
    assert ordu.kabul(['{"1":"a"}', {"1": "a"}], gevsek=True, tur="json") == {"1": "a"}
    assert ordu.kabul(["bir şey.", "farklı"], gevsek=True, tur="metin") is None
    assert ordu.kabul(["bir şey", "farklı"], hakem_=lambda a, b: True, gevsek=True, tur="metin") == "bir şey"
    assert ordu.kabul(["bir şey", "farklı"], hakem_=lambda a, b: None, gevsek=True, tur="metin") is None
    assert ordu.kabul(["x", None], hakem_=lambda a, b: True, gevsek=True, tur="metin") is None  # tek yanıt kabul olmaz


def test_kabul_json_tip_ve_buyuk_harf_korunur():
    # d9: json dalı True==1 ve küçük harfe indirmeyle iki farklı yanıtı birleştirebiliyordu; yalnız anahtar sırası/boşluk/çit/iç içe dizge/1.0≡1 yutulur.
    assert ordu.kabul(['{"a": true}', '{"a": 1}'], gevsek=True, tur="json") is None
    assert ordu.kabul(['{"a": "Ömer"}', '{"a": "ömer"}'], gevsek=True, tur="json") is None
    assert ordu.kabul(['{"a": "x."}', '{"a": "x"}'], gevsek=True, tur="json") is None
    assert ordu.kabul(['{"a": 1.0, "b": "Y"}', '```json\n{ "b": "Y",\n "a": 1 }\n```'], gevsek=True, tur="json") == {"a": 1, "b": "Y"}
    assert ordu.kabul([json.dumps({"1": "a"}), {"1": "a"}], gevsek=True, tur="json") == {"1": "a"}
    assert ordu.kabul(['{"1": "a"}', json.dumps(json.dumps({"1": "a"}))], gevsek=True, tur="json") == {"1": "a"}  # çift kodlanmış (d8 O3/O4/O6)


def test_kabul_test_ve_donus_ozgun_metin():
    # d9: test varken norm kodu küçük harfe indirip girintiyi daraltıyordu; test ve dönen yanıt özgün (kenar boşluğu atılmış) metin.
    kod = "def F(x):\n    return x + 1"
    gorulen = []
    assert ordu.kabul([" " + kod + "\n", "yanlış"], test=lambda y: gorulen.append(y) or y == kod, gevsek=True) == kod
    assert gorulen[0] == kod
    assert ordu.kabul(["Bir Şey.", "bir şey"], hakem_=lambda a, b: False, gevsek=True, tur="metin") == "Bir Şey."


def test_kabul_kesin_regex_hakem_yok():
    # d8 O5: alibaba "r'...'" sarmalı yanlış regex, openai doğru regex; LLM hakem AYNI dedi → yanlış kabul. kesin türde hakem çağrılmaz.
    yanlis = r"r'(0[1-9]|[12]\d|3[01])\.(0[1-9]|1[0-2])\.\d{4}'"
    dogru = r"(?:0[1-9]|[12][0-9]|3[01])\.(?:0[1-9]|1[0-2])\.\d{4}"
    assert ordu.kabul([yanlis, dogru], hakem_=lambda a, b: True, gevsek=True) is None  # varsayılan tur = kesin
    assert ordu.kabul([yanlis, dogru], hakem_=lambda a, b: True, gevsek=True, tur="json") is None
    assert ordu.kabul([" " + dogru + "\n", dogru], gevsek=True) == dogru
    assert ordu.kabul(["[A-Z]+", "[a-z]+"], gevsek=True) is None  # normalize küçük harfe indirip birleştirmez
    assert ordu.kabul(['{"INFO": 3}', {"INFO": "3"}], gevsek=True, tur="json") is None  # sayı ≠ dizge


def test_kabul_gevsek_test_varsa_testi_gecen():
    assert ordu.kabul([{"1": "a"}, {"1": "b"}], test=lambda y: y == {"1": "b"}, gevsek=True) == {"1": "b"}
    assert ordu.kabul([{"1": "a"}, {"1": "a"}], test=lambda y: False, gevsek=True) is None
