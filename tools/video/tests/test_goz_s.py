"""VİDEO-GÖZ-1b-1S: son rötuş — yeni bilgi süzgeci · gürültü sözlük/TERIM · yorum kırpma · DML yoksa künye · URL işe yarar/değersiz."""
from video import goz as g


def test_s1_yeni_cift_getiren_satir_tutulur():
    metin = [(10, ["Claude Code"]), (20, ["memory bank"]), (30, ["Claude memory"])]
    assert (30, "Claude memory") in g.ekran_metni(metin, "")


def test_s1_tamamen_tekrar_satir_atilir():
    metin = [(10, ["Claude Code memory"]), (20, ["Code memory"]), (30, ["claude code"])]
    assert g.ekran_metni(metin, "bugün Claude Code ile çalışıyoruz") == [(10, "Claude Code memory")]
