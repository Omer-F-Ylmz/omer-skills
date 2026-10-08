"""VİDEO-PARTİ-YT1 2: konu etiketi (anahtar kelime eşiği 2) · kayit.jsonl satırında "konu"."""
from video import tarama as tr
from test_m2a import V, Sahte, _ctx, _kurulum, _ns


def test_konu_otomasyon_yalniz():
    assert tr.konu_etiketle("n8n ile workflow kurup müşteri bulduk, satış arttı") == ["otomasyon/iş"]


def test_konu_3d_yalniz():
    assert tr.konu_etiketle("Blender ile mesh kurup render aldık, three.js'e aktardık") == ["3d/blender"]


def test_konu_coklu_ve_esik():
    t = tr.konu_etiketle("Tailwind ile landing page, Blender 3d render; güvenlik için secret taraması. Tek token.")
    assert t == ["3d/blender", "site/frontend", "güvenlik"]  # "token" tek vuruş → eşik altı


def test_rapor_yaz_kayitta_konu(tmp_path):
    kok = _kurulum(tmp_path, V[:1], sure=300)
    import video.parti as pt
    assert pt.parti(_ns("baslat", kok / "kuyruk.md"), _ctx(kok, Sahte())) == 0
    s = tr.kayit_oku(kok / "docs" / "video-tarama" / "kayit.jsonl")
    assert s and "konu" in s[0] and isinstance(s[0]["konu"], list)
