import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import ders_dongu as dd  # noqa: E402


@pytest.fixture(autouse=True)
def gecici(tmp_path, monkeypatch):
    monkeypatch.setattr(dd, "DOSYA", tmp_path / "dersler.jsonl")
    monkeypatch.setattr(dd, "OBSIDIAN", tmp_path / "50-dersler")
    monkeypatch.setattr(dd, "ADAY", tmp_path / "aday.jsonl")


def test_kanitsiz_ders_reddedilir():
    with pytest.raises(ValueError):
        dd.ekle("video", "t", "h", "d", "")


def test_sirli_ders_reddedilir():
    with pytest.raises(ValueError):
        dd.ekle("video", "t", "api_key=abcdef123456", "d", "x.md:1")


def test_benzer_ders_birlesir():
    a = dd.ekle("video", "referans verildi", "benzer üretti", "birebir kullan", "x.md:1")
    b = dd.ekle("video", "referans verildi", "benzer üretti", "birebir kullan", "y.md:2")
    assert a["id"] == b["id"] and b["durum"] == "birlesti"
    assert json.loads(dd.DOSYA.read_text(encoding="utf-8").splitlines()[0])["destek"] == 2


def test_getir_en_fazla_5_ve_150_jeton():
    for i in range(9):
        dd.ekle("genel", f"ortak anahtar kelime kural{i} alan{i}x", "hata " * 30, "doğru " * 30, f"k.md:{i}")
    blok, ids = dd.getir("genel", "ortak anahtar kelime kural alan")
    assert len(ids) <= 5 and len(blok) // 3 <= 150


def test_getir_alakasiz_gorevde_bos():
    dd.ekle("video", "referans verildi", "benzer üretti", "birebir kullan", "x.md:1")
    assert dd.getir("video", "muhasebe tablosu vergi")[0] == ""


def test_bhs5_dersi_kayitli_ve_gelir():
    d = dd.tohum()
    blok, ids = dd.getir("video", "Ömer referans ses verdi, videoda anlatım sesi üret")
    assert d and ids and "birebir" in blok


def test_topla_kanitli_aday_cikarir(tmp_path):
    (tmp_path / "r.md").write_text("giriş\nDUR: referans ses yerine Kokoro kullanıldı, Ömer reddetti\nkısa DUR\n", encoding="utf-8")
    adaylar = dd.topla([tmp_path])
    assert len(adaylar) == 1 and adaylar[0]["kanit"].endswith("r.md:2")


def test_yansit_obsidian_yazar():
    dd.ekle("video", "referans verildi", "benzer üretti", "birebir kullan kesinlikle", "x.md:1")
    assert dd.yansit() == 1
    assert list(dd.OBSIDIAN.glob("ders-dongu-*.md"))


def test_vaka_dosyasi_her_dersi_getirir():
    """Regresyon: tools/ders_test/vakalar.json her vakada beklenen ders id'si getir() ile gelir."""
    vakalar = json.loads((KOK / "tools/ders_test/vakalar.json").read_text(encoding="utf-8"))
    dd.tohum()
    kacan = [v["ad"] for v in vakalar if v["bekle"] not in dd.getir(v["tur"], v["gorev"])[1]]
    assert not kacan, kacan


def test_dongu_topla_aday_onayla_yansit(monkeypatch):
    sira = []
    monkeypatch.setattr(dd, "topla", lambda: [{"kanit": "a.md:1", "satir": "DUR " * 12}])
    monkeypatch.setattr(dd, "onayla", lambda n: sira.append(("onayla", n)) or [{"id": "z1"}])
    monkeypatch.setattr(dd, "yansit", lambda: sira.append(("yansit",)) or 1)
    assert dd.dongu() == 1
    assert sira == [("onayla", 10), ("yansit",)]
    assert dd.oku(dd.ADAY)[0]["kanit"] == "a.md:1"
