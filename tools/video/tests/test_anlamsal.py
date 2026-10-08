"""VİDEO-AKIL-1b-2a DEVAM-1: serbest metin alanları anlamsal puan (fastembed çok dilli; gerçek model)."""
from video import altin as au


def _rapor(**bol):
    return "# b\n## Özet\nmetin\n" + "".join(f"## {k}\n{v}\n" for k, v in bol.items())


def test_turkce_altin_ayni_anlamli_ingilizce_satirla_eslesir():
    a = {"is_akisi": [{"adim": "Kullanıcı Blender'da arabanın modelini hazırlar", "zaman": "1:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- The user prepares the car model in Blender"})
    assert au.puan(r, a)["is_akisi"] == (1, 1)  # kelime örtüşmesi: ortak kelime yok → 0


def test_baska_videonun_maddesi_eslesmez():
    a = {"is_akisi": [{"adim": "Kullanıcı Blender'da arabanın modelini hazırlar", "zaman": "1:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- Supabase veritabanında kullanıcı tablosuna satır güvenliği politikası eklenir"})
    assert au.puan(r, a)["is_akisi"] == (0, 1)


def test_bir_rapor_satiri_iki_altin_maddeyi_karsilayamaz():
    a = {"is_akisi": [{"adim": "Blender'da araba modelini hazırla", "zaman": "1:00", "araclar": []},
                      {"adim": "Blender'da arabanın modelini kur", "zaman": "2:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- Prepare the car model in Blender"})
    assert au.puan(r, a)["is_akisi"] == (1, 2)
