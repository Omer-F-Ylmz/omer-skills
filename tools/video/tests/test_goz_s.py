"""VİDEO-GÖZ-1b-1S: son rötuş — yeni bilgi süzgeci · gürültü sözlük/TERIM · yorum kırpma · DML yoksa künye · URL işe yarar/değersiz."""
from video import cli
from video import goz as g


def test_s1_yeni_cift_getiren_satir_tutulur():
    metin = [(10, ["Claude Code"]), (20, ["memory bank"]), (30, ["Claude memory"])]
    assert (30, "Claude memory") in g.ekran_metni(metin, "")


def test_s1_tamamen_tekrar_satir_atilir():
    metin = [(10, ["Claude Code memory"]), (20, ["Code memory"]), (30, ["claude code"])]
    assert g.ekran_metni(metin, "bugün Claude Code ile çalışıyoruz") == [(10, "Claude Code memory")]


def test_s2_kisaltma_cikarilir_sozluk_adi_korunur():
    assert not cli._ocr_gurultu("Principled BSDF")  # d_UE 0:32: anlamsiz_oran BSDF'yi sayıyordu
    assert cli._ocr_gurultu("BSDF") and cli._ocr_gurultu("XQZT VBNM")  # kalan boş → eski kural
    assert cli._ocr_gurultu("GSAP") and not cli._ocr_gurultu("GSAP", ["GSAP"])
