import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ogrenme"))
import ders  # noqa: E402
import onsoz  # noqa: E402

AJAN = b"---\r\nname: kod\r\ndescription: x\r\n---\r\n\r\nGovde.\r\n"


def test_enjekte_idempotent_ve_geri(tmp_path):
    f = tmp_path / "kod.md"
    f.write_bytes(AJAN)
    assert onsoz.enjekte(f) is True
    ilk = f.read_bytes()
    assert b"ders.py getir --ajan kod" in ilk and b"\r\n---\r\n<!-- ders-yuvasi:basla -->" in ilk
    assert b"\n" not in ilk.replace(b"\r\n", b"")  # CRLF korunur
    assert onsoz.enjekte(f) is False and f.read_bytes() == ilk
    assert onsoz.enjekte(f, geri=True) is True and f.read_bytes() == AJAN


def test_kuru_dosyaya_dokunmaz(tmp_path):
    f = tmp_path / "kod.md"
    f.write_bytes(AJAN)
    assert onsoz.enjekte(f, kuru=True) is True and f.read_bytes() == AJAN


def test_frontmattersiz_atlanir(tmp_path):
    f = tmp_path / "x.md"
    f.write_bytes(b"duz metin\n")
    assert onsoz.enjekte(f) is False


def test_blok_istem_onune(tmp_path, monkeypatch):
    monkeypatch.setenv("OGRENME_DIZIN", str(tmp_path))
    assert onsoz.istem("kod", "rapor yaz") == ("rapor yaz", [])
    ders.ekle("kod", "KURALLAR.md önce okunur", "proje klasöründe görev", "Türkçe İ kuralı KURALLAR.md'de",
              "basarisizlik", "k1")
    metin, ids = onsoz.istem("kod", "proje klasöründe görev: fonksiyonu düzelt")
    assert ids and metin.startswith("Dersler") and metin.endswith("fonksiyonu düzelt")


def test_fable_godmode_blogu_ile_bagimsiz(tmp_path):
    import godmode_onsoz
    f = tmp_path / "ajan.md"
    f.write_bytes(AJAN)
    godmode_onsoz.enjekte(f, "FABLE protokolü")
    assert onsoz.enjekte(f) is True
    m = f.read_text(encoding="utf-8")
    assert "<!-- godmode:basla -->" in m and "<!-- ders-yuvasi:basla -->" in m and "--ajan ajan " in m
    assert len(onsoz.ONSOZ) // 4 <= 150  # ders yuvası statik blok; getir çıktısı ayrıca ≤300 jeton
    assert onsoz.enjekte(f, geri=True) is True and "FABLE protokolü" in f.read_text(encoding="utf-8")
