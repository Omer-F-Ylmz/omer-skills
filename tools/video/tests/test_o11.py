"""DERİNLİK-MASTER O11: C4/C3 ikinci düzeltme (canlı b2QkhmQ0sT0 --kare 20 → seçilen 44 · model 20 · incelenmedi 8 "kare tavanı 20")."""

from video import parti as pt
from test_video import jpeg


def test_tek_girdi_hesabi_gercek_kare_jetonu_28_kare_7k_metin_dusmez(tmp_path):
    """(1) kare_sigdir PAKET_BUTCE ile aynı hesap: gerçek kare jetonu (~442) + tam metin; KARE_TK 1600 varsayımı 28 kareyi keserdi."""
    kareler = []
    for i in range(28):
        (y := tmp_path / f"k{i}.jpg").write_bytes(jpeg())
        kareler.append(y.as_posix())
    metin = ""
    while pt.c.token(metin) < 7_000:
        metin += "kelime " * 100
    pk = {"e1": {"short": False, "metin": metin, "kareler": list(kareler), "kare_zaman": list(range(28))}}
    pt.kare_sigdir(pk)
    assert pk["e1"]["kareler"] == kareler and "kare_not" not in pk["e1"]
    assert pt.girdi_tk(metin, kareler) == pt.c.token(metin) + 28 * 442
