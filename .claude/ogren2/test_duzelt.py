import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from duzelt import duzelt_satir

KAYNAK = "---\nname: ornek-arac\n---\nAraç.\nNEVER use this on production databases directly.\n"


def satir(sinirlar="belirsiz — yok", komut="belirsiz — yok"):
    return {"ad": "x", "sinirlar": {"deger": sinirlar, "alinti": ""}, "komut": {"deger": komut, "alinti": ""}}


def test_belirsiz_kaynaktan_dolar():
    o = satir()
    assert duzelt_satir(o, KAYNAK) == ["sinirlar", "komut"]
    assert o["sinirlar"]["alinti"] == "NEVER use this on production databases directly."
    assert o["komut"]["alinti"] == "name: ornek-arac"


def test_caution_satiri_sinir_sayilir():
    o = satir()
    duzelt_satir(o, "# Carson\nCaution: Use sparingly; avoid on navigation and legal text.\n")
    assert o["sinirlar"]["alinti"].startswith("Caution: Use sparingly")


def test_dolu_alana_dokunmaz():
    o = satir("Gerçek sınır", "/ornek")
    assert duzelt_satir(o, KAYNAK) == [] and o["komut"]["deger"] == "/ornek"


def test_kaynakta_yoksa_belirsiz_kalir():
    o = satir()
    assert duzelt_satir(o, "Sadece bir cümle burada.") == [] and o["sinirlar"]["deger"].startswith("belirsiz")
