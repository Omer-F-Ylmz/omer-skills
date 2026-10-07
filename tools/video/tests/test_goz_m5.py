"""VİDEO-GÖZ-1b-1 M5: ad sözlüğü (sozluk.txt) · Sözlük eşleşmeleri (kesin + sesde bulanık öneri) · kapsam (a) sözlüksüz."""
from pathlib import Path

from video import altin as au
from video import cli
from video import goz as g

SZ = [("Claude Sonnet", ["Sonnet", "Sonet"]), ("v0", []), ("Topview", ["Top View"]), ("Behance", [])]


def test_sozluk_oku(tmp_path):
    y = tmp_path / "s.txt"
    y.write_text("# yorum\n\nClaude Sonnet | Sonnet, Sonet\nv0 |\n", encoding="utf-8")
    assert g.sozluk_oku(y) == [("Claude Sonnet", ["Sonnet", "Sonet"]), ("v0", [])]
    assert g.sozluk_oku(tmp_path / "yok.txt") == []


def test_kesin_eslesme_kaynak_ve_ilk_zaman():
    k = [("ses", 40, "v0 ile yaptık"), ("ekran", 12, "Top View Studio"), ("ses", 50, "nv0x değil"), ("açıklama", 0, "behance.net/gallery")]
    assert g.eslesmeler(k, SZ) == [("Behance", "açıklama", 0, None), ("Topview", "ekran", 12, None), ("v0", "ses", 40, None)]


def test_seste_bulanik_oneri_ekranda_yok():
    assert g.eslesmeler([("ses", 3, "bugün Sonnnet çıktı")], SZ) == [("Claude Sonnet", "ses", 3, "sonnnet")]
    assert g.eslesmeler([("ekran", 3, "bugün Sonnnet çıktı")], SZ) == []
    assert g.eslesme_satirlari([("Claude Sonnet", "ses", 63, "sonnnet"), ("Behance", "açıklama", 0, None)]) == [
        "Claude Sonnet · ses · 1:03 · bulanık: sonnnet", "Behance · açıklama · -"]


def test_sozluk_dosyasi_bicim_ve_tavan():
    y = Path(__file__).parents[3] / "docs" / "video-tarama" / "sozluk.txt"
    satir = y.read_text(encoding="utf-8").splitlines()
    assert 50 <= len(satir) <= 300 and all("|" in s for s in satir if s.strip() and not s.startswith("#"))


def test_kapsam_sozluksuz_bolumu_atar(tmp_path, capsys):
    p = tmp_path / "paket.md"
    p.write_text("# x\n## Segmentler\n[0:01] merhaba\n## Sözlük eşleşmeleri\nTopview · ses · 0:01 · bulanık: tabiew\n## Kareler\n", encoding="utf-8")
    (tmp_path / "a.json").write_text('{"adaylar": [{"ad": "Topview", "tur": "a", "kaynak": "ses"}]}', encoding="utf-8")
    assert cli.main(["altin", "kapsam", str(p), str(tmp_path / "a.json"), "--sozluk", "yok"], env={}) == 0
    assert "aday 0/1" in capsys.readouterr().out
    assert au.kapsam(p.read_text(encoding="utf-8"), {"adaylar": [{"ad": "Topview", "kaynak": "ses"}]}, boyut=lambda y: None)["aday"] == (1, 1)
