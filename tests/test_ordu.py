import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ordu  # noqa: E402


def test_sinif_kademe():
    assert ordu.sinif("dosyaları listele")["kademe"] == "T1"
    assert ordu.sinif("dosyaları listele")["capraz"] is False
    assert ordu.sinif("özet çıkar")["capraz"] is True
    assert ordu.sinif("küçük bug düzelt")["kademe"] == "T3"
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
