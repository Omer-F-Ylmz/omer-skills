import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import ekran_duzelt as ed  # noqa: E402
import ekran_yazi as ey  # noqa: E402


def test_ekrandaki_ad_duyulani_duzeltir(monkeypatch):
    monkeypatch.setattr(ed, "yaygin", lambda: set())
    yeni, ops = ed.duzelt("Veritabanı için Superbase kullandım", "Supabase Dashboard\nProject settings")
    assert "Supabase".lower() in yeni.lower() and "Superbase" not in yeni
    assert ops[0][0] == "Superbase"


def test_ekranda_olmayan_ad_degismez(monkeypatch):
    monkeypatch.setattr(ed, "yaygin", lambda: set())
    metin = "Veritabanı için Superbase kullandım"
    assert ed.duzelt(metin, "Hello world\nSettings") == (metin, [])


def test_yaygin_kelime_korunur(monkeypatch):
    monkeypatch.setattr(ed, "yaygin", lambda: {"revize"})
    metin = "Bunu revize edelim"
    assert ed.duzelt(metin, "review\nCode review")[0] == metin


def test_cogul_ve_ek_ad_degildir(monkeypatch):
    monkeypatch.setattr(ed, "yaygin", lambda: set())
    metin = "Claude'un agent yapısı"
    assert ed.duzelt(metin, "Claude Code agents")[0] == metin


def test_ek_korunur(monkeypatch):
    monkeypatch.setattr(ed, "yaygin", lambda: set())
    yeni, _ = ed.duzelt("Herder'in arayüzü", "herdr")
    assert yeni.lower().startswith("herdr'in")


def test_kat_aksani_esitler():
    assert ey.kat("Görünmez!") == ey.kat("Gorunmez") == "gorunmez"
    assert ey.kat("İstanbul") == ey.kat("istanbul")


def test_olaylar_kalici_basligi_atar_tekrari_birlestirir():
    kareler = [(i / 3, ["Sabit Baslik", "merhaba dunya" if i < 3 else "bugun hava guzel"]) for i in range(6)]
    assert [m for _, m in ey.olaylar(kareler)] == ["merhaba dunya", "bugun hava guzel"]


def test_olaylar_uzayan_satiri_gunceller():
    kareler = [(0, ["Anthropic Claude'in"]), (0.3, ["Anthropic Claude'in yazdigi"]), (0.6, ["Anthropic Claude'in yazdigi tum"]), (3, ["baska satir"])]
    assert [m for _, m in ey.olaylar(kareler)] == ["Anthropic Claude'in yazdigi tum", "baska satir"]
