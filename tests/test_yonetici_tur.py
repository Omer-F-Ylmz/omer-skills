"""YONETICI-API-1: yönetici kontrol turu (20 dk, günlük ≤$2 aşılınca 40 dk)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import yonetici_tur as yt  # noqa: E402

LOG = ("07:00:00 BİTTİ a-1 rc 0 5 dk\n07:01:00 RAM-BEKÇİ x\n07:02:00 BİTTİ b-2 rc 1 3 dk\n")


def test_biten_isler_ofsetten_sonrasi():
    adlar, ofs = yt.biten_isler(LOG, 0)
    assert adlar == ["a-1", "b-2"] and ofs == len(LOG.encode())
    assert yt.biten_isler(LOG + "07:09:00 BİTTİ c-3 rc 0 1 dk\n", ofs)[0] == ["c-3"]


def test_aralik_gunluk_tavanda_seyrek():
    assert yt.aralik(0.5) == 1200 and yt.aralik(2.0) == 2400


def test_vakit_geldi():
    assert yt.vakit(0, 1300, 0.1) and not yt.vakit(100, 1250, 0.1) and not yt.vakit(0, 1300, 2.5) and yt.vakit(0, 2400, 2.5)


def test_tur_ozet_ve_desktop_satiri(tmp_path):
    kontrol = lambda ad: ("DUR eksik kanıt", "konsol") if ad == "b-2" else ("KABUL ok", "ucretsiz/x")
    ozet = tmp_path / "yonetici-ozet.md"
    sat = yt.tur(["a-1", "b-2"], kontrol, ozet, ram=70)
    m = ozet.read_text(encoding="utf-8").splitlines()
    assert len(m) <= 5 and "a-1 KABUL" in m[1] and m[2].startswith("DESKTOP: b-2 DUR")
    assert sat == m


def test_bos_tur_ozeti_ezmez(tmp_path):
    ozet = tmp_path / "o.md"
    ozet.write_text("DESKTOP: eski", encoding="utf-8")
    assert yt.tur([], lambda ad: ("KABUL", "x"), ozet, ram=50) == []
    assert ozet.read_text(encoding="utf-8") == "DESKTOP: eski"


def test_dur_gerekce_cok_satir(tmp_path):
    ozet = tmp_path / "o.md"
    assert "kanıt yok" in yt.tur(["z"], lambda ad: ("DUR\nkanıt yok", "k"), ozet, ram=1)[1]


def test_tur_kontrol_bos_atlanir(tmp_path):
    ozet = tmp_path / "o.md"
    yt.tur(["x"], lambda ad: (None, None), ozet, ram=50)
    assert "x KONTROL-BOŞ" in ozet.read_text(encoding="utf-8")
