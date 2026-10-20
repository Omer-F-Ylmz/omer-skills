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
