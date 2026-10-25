"""KONSOL-GECIS-2: kontrol_onoku karar/tavan yolu + eski iki boş koşunun BAŞARISIZ sayılması."""
import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(KOK / "tools"), str(KOK / ".kos/kopru")]
import kontrol_onoku as ko  # noqa: E402
import ucretsiz_motor as um  # noqa: E402


@pytest.mark.parametrize("ad", ["yarim-h1-24eki", "zip-yukle-24eki"])
def test_eski_bos_kosu_basarisiz(ad):
    yol = KOK / ".kos/kopru/ajan-sira" / f"{ad}.json"
    if not yol.exists():
        pytest.skip("eski koşu çıktısı yok")
    j = json.loads(yol.read_text(encoding="utf-8").strip().splitlines()[-1])
    assert um.bos_kosu(j, um.anahtarlar(ad, ""))


def test_ucretsiz_basarili_krediye_dusmez(monkeypatch, tmp_path):
    monkeypatch.setattr(ko, "LOG", tmp_path / "l.log")
    monkeypatch.setattr(ko, "sonuc_metni", lambda ad: "bitti")
    monkeypatch.setattr(ko, "kabul_satiri", lambda g: "KABUL: x")
    monkeypatch.setattr(ko.ucretsiz_havuz, "cagir", lambda *a, **k: ("KABUL\nkanıt var", "nvidia/x", []))
    monkeypatch.setattr(ko, "konsol", lambda *a: pytest.fail("kredi kullanıldı"))
    assert ko.kontrol("a", "g")[1].startswith("ucretsiz/")


def test_ucretsiz_bos_krediye_duser(monkeypatch, tmp_path):
    monkeypatch.setattr(ko, "LOG", tmp_path / "l.log")
    monkeypatch.setattr(ko, "sonuc_metni", lambda ad: "bitti")
    monkeypatch.setattr(ko, "kabul_satiri", lambda g: "KABUL: x")
    monkeypatch.setattr(ko.ucretsiz_havuz, "cagir", lambda *a, **k: (None, None, ["429"]))
    monkeypatch.setattr(ko, "konsol", lambda ad, istem: "DUR\neksik")
    assert ko.kontrol("a", "g") == ("DUR\neksik", "konsol")


def test_konsol_gunluk_tavan_cagri_yapmaz(monkeypatch, tmp_path):
    monkeypatch.setattr(ko, "LOG", tmp_path / "l.log")
    monkeypatch.setattr(ko, "anahtar", lambda: "sahte")
    monkeypatch.setattr(ko.maliyet_defter, "oku", lambda: [])
    monkeypatch.setattr(ko.maliyet_defter, "konsol_harcama", lambda rows, gun=None: 0.999)
    monkeypatch.setattr(ko.urllib.request, "urlopen", lambda *a, **k: pytest.fail("çağrı yapıldı"))
    assert ko.konsol("a", "x" * 3000) is None
