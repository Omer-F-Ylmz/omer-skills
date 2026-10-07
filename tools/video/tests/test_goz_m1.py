"""VİDEO-GÖZ-1b-1 M1: ekran metni — RapidOCR güven süzgeci · tekrar/altyazı ayıklama · öncelikli bütçe · model karesi ölçeği."""
from video import cli
from video import goz as g


def test_guven_esigi_ve_satir_sirasi():
    sonuc = [("alt satır", 0.9, 300), ("bulanık", 0.3, 100), ("üst satır", 0.8, 50)]
    assert g.ocr_satirlar(sonuc) == ["üst satır", "alt satır"]


def test_tekrar_ve_altyazida_gecen_satir_atilir():
    metin = [(10, ["npx skills add x", "Bugün çok güzel bir gün"]), (20, ["npx skills add x", "Topview Pro"])]
    out = g.ekran_metni(metin, "bugün çok güzel bir gün diyoruz")
    assert out == [(10, "npx skills add x"), (20, "Topview Pro")]


def test_turkce_karakter_korunur_ve_katlanmadan_eslesir():
    metin = [(5, ["Çağrı ŞİŞE ığdır ÖZGÜR üzüm"]), (6, ["Görüldüğü gibi ekranda"])]
    out = g.ekran_metni(metin, "görüldüğü gibi ekranda bir şey var")
    assert out == [(5, "Çağrı ŞİŞE ığdır ÖZGÜR üzüm")]


def test_butce_onceligi_sozluk_url_terim_diger():
    metin = [(1, ["sıradan bir açıklama satırı burada"]), (2, ["GPT4o modeli"]), (3, ["https://dala.craftedbygc.com"]),
             (4, ["Nano Banana ile üret"])]
    tk = lambda s: 10  # noqa: E731
    assert g.ekran_metni(metin, "", sozluk=["Nano Banana"], butce=20, token=tk) == [(3, "https://dala.craftedbygc.com"), (4, "Nano Banana ile üret")]
    assert g.ekran_metni(metin, "", sozluk=["Nano Banana"], butce=30, token=tk)[0] == (2, "GPT4o modeli")


def test_model_karesi_768_ve_28_kati():
    assert g.olcek(1920, 1080) == (756, 420)
    assert g.olcek(1080, 1920) == (420, 756)
    assert g.olcek(640, 360) == (616, 336)


def test_rapidocr_yoksa_windows_yedegi_ve_motor_adi():
    def yukle():
        raise ImportError("rapidocr yok")
    ctx = {"rapid": yukle, "kos": lambda a, t, env=None: b'{"k1.jpg": {"tr": [["Merhaba", 0, 0, 10, 10]], "en": []}}', "env": {}}
    assert cli._ocr(ctx, ["C:/x/k1.jpg"]) == {"k1.jpg": ["Merhaba"]}
    assert ctx["ocr_motor"].startswith("windows")


def test_rapidocr_birincil():
    ctx = {"rapid": lambda: lambda yol: [("Topview", 0.95, 10), ("gürültü", 0.2, 20)]}
    assert cli._ocr(ctx, ["C:/x/k2.jpg"]) == {"k2.jpg": ["Topview"]} and ctx["ocr_motor"] == "rapidocr"
