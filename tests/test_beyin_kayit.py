import importlib.util
import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK / "tools"))
spec = importlib.util.spec_from_file_location("beyin_kayit", KOK / "tools" / "beyin_kayit.py")
bk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bk)
import ucretsiz_havuz as H  # noqa: E402

OZET = ["commit: abc1234", "ne bitti: test eklendi", "★: 12 test yeşil", "karar: -"]


@pytest.fixture
def kasa(tmp_path, monkeypatch):
    ciktı = tmp_path / "ajan-sira"
    ciktı.mkdir()
    proje = tmp_path / "40-projeler"
    proje.mkdir()
    monkeypatch.setattr(bk, "CIKTI", ciktı)
    monkeypatch.setattr(bk, "PROJELER", proje)
    monkeypatch.setattr(bk, "KARARLAR", tmp_path / "Kararlar.md")
    return ciktı


def is_json(ciktı, ad, metin):
    (ciktı / f"{ad}.json").write_text(json.dumps({"result": metin}) + "\n", encoding="utf-8")


def test_yazar_ve_ayni_adi_ikinci_kez_yazmaz(kasa, monkeypatch):
    is_json(kasa, "token-x-d1", "uzun sonuç")
    monkeypatch.setattr(bk, "ozetle", lambda m: OZET)
    assert bk.main("token-x-d1") == "yazıldı: token-x-d1 → omer-skills.md"
    assert bk.main("token-x-d1") == "zaten yazıldı: token-x-d1"
    not_ = (bk.PROJELER / "omer-skills.md").read_text(encoding="utf-8")
    assert not_.count("<!-- beyin-kayit:token-x-d1 -->") == 1
    assert "- commit: abc1234" in not_


def test_karar_varsa_kararlara_da_yazar(kasa, monkeypatch):
    is_json(kasa, "telve-a1", "sonuç")
    monkeypatch.setattr(bk, "ozetle", lambda m: OZET[:3] + ["karar: Ollama düşüşünü kullan"])
    bk.main("telve-a1")
    assert "Ollama düşüşünü kullan" in bk.KARARLAR.read_text(encoding="utf-8")
    assert (bk.PROJELER / "TELVE.md").exists()


def test_bozuk_json_atlar(kasa):
    (kasa / "ters-9.json").write_text("{bozuk\n", encoding="utf-8")
    assert bk.main("ters-9").startswith("atla ters-9")
    assert not (bk.PROJELER / "omer-skills.md").exists()


def test_eksik_dosya_ve_bos_sonuc_atlar(kasa):
    assert bk.main("yok-1").startswith("atla yok-1")
    is_json(kasa, "ordu-2", "  ")
    assert bk.main("ordu-2") == "atla ordu-2: sonuç boş"


def test_havuz_kapaliyken_yerel_dusus(monkeypatch):
    monkeypatch.setattr(H, "cagir", lambda *a, **k: (None, None, []))
    monkeypatch.setattr(bk, "yerel", lambda istem: "\n".join(OZET))
    assert bk.ozetle("sonuç") == OZET


def test_havuz_ve_yerel_kapaliyken_bos_doner(monkeypatch):
    monkeypatch.setattr(H, "cagir", lambda *a, **k: (None, None, []))

    def kapali(istem):
        raise OSError("ollama yok")

    monkeypatch.setattr(bk, "yerel", kapali)
    assert bk.ozetle("sonuç") == []


def test_cli_yardim_ve_olay(monkeypatch, capsys):
    import beyin_dusun
    gelen = []
    monkeypatch.setattr(beyin_dusun, "olay", lambda *a, **k: gelen.append((a, k)) or True)
    assert bk.cli(["--help"]).startswith("Kullanım") and not gelen  # '--help' ad sanılıp FileNotFoundError vermesin
    assert bk.cli(["olay", "ders", "K2m: arka planda bekleme", "--hata"]) == "olay yazıldı: ders"
    assert gelen == [(("ders", "claude", "K2m: arka planda bekleme"), {"hata": True})]
