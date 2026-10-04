"""DERİNLİK-MASTER D2 kancalama + iki ek (Ömer, 5 Eki): (a) sözlük = kurulu araçlar + aday adları + docs/video-tarama/bilinen-araclar.txt;
(b) engelleyen KAÇAN? (URL · owner/repo · kurulum komutu · sözlük) ve "KAÇAN? (düşük güven)" (cümle başı değil, yaygın değil, ≥2 kez geçen
büyük harfli tek kelime). Kaynaklar: paket.md Segmentler · Ekran metni (OCR) · Açıklama bağlantıları + yanındaki ocr-gurultu.txt."""

from video import tarama as tr

RAPOR = "## Künye\nşema 2\n## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n| konuşma 01:00 | rtk | rtk | geçti |\n"


def _kok(tmp_path):
    (tmp_path / "docs" / "kurulumlar" / "adaylar").mkdir(parents=True)
    (tmp_path / "docs" / "kurulumlar" / "adaylar" / "stop-slop.md").write_text("x", encoding="utf-8")
    (tmp_path / "docs" / "departmanlar").mkdir(parents=True)
    (tmp_path / "docs" / "departmanlar" / "envanter.json").write_text('[{"ad": "rtk", "tur": "cli"}]', encoding="utf-8")
    (tmp_path / "docs" / "video-tarama").mkdir(parents=True)
    (tmp_path / "docs" / "video-tarama" / "bilinen-araclar.txt").write_text("supabase\n\n", encoding="utf-8")
    return tmp_path


def test_sozluk_uc_kaynak(tmp_path):
    assert set(tr.kacan_sozluk(_kok(tmp_path))) == {"rtk", "stop-slop", "supabase"}


def test_dusuk_guven_cursor_iki_kez_cumle_basi_yok():
    k = [("paket", "we open it in Cursor today. The editor is nice.\nThis one is Cursor again and Windsurf once")]
    assert tr.kacan_dusuk(RAPOR, k, ["supabase"]) == [("paket", "Cursor")]


def test_video_kancalama_paket_ve_gurultu(tmp_path):
    p = tmp_path / "v1"
    p.mkdir()
    (p / "paket.md").write_text("## Künye\nhttps://www.youtube.com/watch?v=v1\n## Açıklama bağlantıları\nyok\n## Segmentler\n"
                                "[00:01] then install supabase and rtk with Cursor, see Cursor docs\n## Kareler\nC:/x/k.jpg · 00:01\n", encoding="utf-8")
    (p / "ocr-gurultu.txt").write_text("00:05 · uvx stop-slop\n", encoding="utf-8")
    eng, dus = tr.kacan_video(RAPOR, p / "paket.md", ["supabase", "rtk", "stop-slop"])
    assert sorted(t for _, t in eng) == ["stop-slop", "supabase"]  # künyedeki video URL'si ve kare yolu taranmaz; rtk İz'de
    assert ("gürültü", "stop-slop") in eng and dus == [("paket", "Cursor")]


def test_kapanista_yeni_aday_adi_eklenir_tekrar_yok(tmp_path):
    kok = _kok(tmp_path)
    tr.bilinen_ekle(kok, ["supabase", "graphify", "graphify"])
    assert (kok / "docs" / "video-tarama" / "bilinen-araclar.txt").read_text(encoding="utf-8").split() == ["supabase", "graphify"]
