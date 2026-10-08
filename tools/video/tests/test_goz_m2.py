"""VİDEO-GÖZ-1b-1 M2: yerel video → dHash sahne (aşama 1) → OCR değişim süzgeci (aşama 2) · tavanlar · model karesi seçimi."""
from video import goz as g


def test_fps_uzun_videoda_yarim():
    assert g.fps(599) == 1 and g.fps(600) == 0.5


def test_sahne_son_tutulana_hamming_5ten_buyuk():
    h6 = 0b111111
    assert g.sahneler([0, 0, h6, h6 ^ 0b1, h6 ^ (0b111111 << 6)], 1) == [(0, 64), (2, 6), (4, 6)]
    assert g.sahneler([0, 0b11111], 0.5) == [(0, 64)]  # Hamming 5 sahne değil


def test_ocr_kare_tavani():
    assert g.tavan_ocr(180, 10) == 46 and g.tavan_ocr(600, 151) == 271 and g.tavan_ocr(40 * 60, 600) == 800  # 1b-1T T3: sahne+dk×12/800


def test_tavan_asilinca_en_az_degisen_atilir_zaman_sirasi_korunur():
    assert g.sahne_sec([(0, 64), (5, 6), (9, 30), (12, 7)], 3) == [(0, 64), (9, 30), (12, 7)]


def test_ocr_degisim_esigi_ve_metinsiz_kare():
    okunan = [(0, ["npx skills add topview"]), (1, ["npx skills add topview."]), (2, []), (3, ["Behance galerisi açık"]),
              (4, ["npx skills add topview"])]
    assert [t for t, _ in g.ocr_sec(okunan)] == [0, 3, 4]


def test_ekran_metni_butcesi_sureye_bagli():
    assert g.butce(5 * 60) == 1500 and g.butce(15 * 60) == 4500  # 1b-1S S1: dk×300 and g.butce(40 * 60) == 5000


def test_model_karesi_yeni_terim_sonra_isaret_taban_min6():
    okunan = [(1, ["Topview Pro"]), (2, ["Topview Pro", "https://x.dev"]), (3, []), (10, [])]
    assert g.model_sec(okunan, "", [10], 3) == [1, 2, 10]
    assert g.model_sec(okunan, "", [10]) == [1, 2, 3, 10]  # sahne < 6 → hepsi
    assert g.model_sec([(1, ["Topview Pro"])], "topview pro anlatıyoruz", [], 6) == [1]
