"""TOKEN-6d orta görev kabul testleri — ana suite DIŞINDA.
Koş: cd tools/video && uv run --with pytest pytest -q -p no:cacheprovider ../../olcum/token6d"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "tools" / "video"))
from video.kur import esik, takas, tasarruf  # noqa: E402


# 1. takas: d < 0 (kalite arttı) = düşüş yok → d == 0 ile aynı karar; kademe "kalite arttı" der
def test_takas_negatif_dusus_esik_asildi():
    k, kademe = takas(10, -5, True)
    assert k == "AL" and "kalite arttı" in kademe


def test_takas_negatif_dusus_esik_asilmadi():
    for s in (5, 40):  # 40: eskiden "düşüş ≤%10 & tasarruf ≥%25" kademesinden AL dönüyordu
        k, kademe = takas(s, -3.5, False)
        assert k == "RED(token)" and "kalite arttı" in kademe
        assert "düşüş >0" not in kademe and "≤%10" not in kademe


def test_takas_sifir_ve_pozitif_degismez():
    assert takas(10, 0, True) == ("AL", "düşüş 0, eşik aşıldı")
    assert takas(10, 0, False) == ("RED(token)", "düşüş 0, eşik aşılmadı")
    assert takas(30, 12, False) == ("AL", "düşüş ≤%15 & tasarruf ≥%30")
    assert takas(10, 5, True) == ("RED(takas)", "tasarruf <%25, düşüş >0")


# 2. esik: yüzde sonda da olabilir; bir alanın sayısı yalnız kendi ifadesinden okunur
def test_esik_sonda_yuzde():
    assert esik("çıktı ≥ 30%") == {"cikti": 30, "maliyet": None}
    assert esik("girdi 10% · maliyet 20,5 %") == {"cikti": None, "girdi": 10, "maliyet": 20.5}
    assert esik("çıktı %40 · girdi 15%") == {"cikti": 40, "girdi": 15, "maliyet": None}
    assert esik("çıktı 30% · girdi %10") == {"cikti": 30, "girdi": 10, "maliyet": None}


def test_esik_baska_alanin_sayisini_almaz():
    assert esik("çıktı ölçülmez · maliyet %20") == {"cikti": 25, "maliyet": 20}
    assert esik("çıktı ölçülmez · maliyet 20%") == {"cikti": 25, "maliyet": 20}
    assert esik("girdi belirsiz, çıktı %30") == {"cikti": 30, "maliyet": None}


def test_esik_onek_bicimi_bozulmaz():
    assert esik("çıktı token −%30 ve toplam maliyet −%3 ya da daha iyi, kabul 3/3") == {"cikti": 30, "maliyet": 3}
    assert esik("") == {"cikti": 25, "maliyet": None}
    assert esik("girdi ≥%15, maliyet %25") == {"cikti": None, "girdi": 15, "maliyet": 25}


# 3. tasarruf: b'de alan yoksa ya da None ise o alan 0.0; mevcut davranış korunur
def test_tasarruf_eksik_ya_da_none_alan_sifir():
    assert tasarruf({"cikti": 100, "girdi": 50, "maliyet": 2.0}, {"cikti": 60}) == {"cikti": 40.0, "girdi": 0.0, "maliyet": 0.0}
    assert tasarruf({"cikti": 100, "girdi": None, "maliyet": 1}, {"cikti": None, "girdi": 5, "maliyet": 0.5}) == \
        {"cikti": 0.0, "girdi": 0.0, "maliyet": 50.0}


def test_tasarruf_mevcut_davranis():
    assert tasarruf({"cikti": 200, "girdi": 100, "maliyet": 4}, {"cikti": 150, "girdi": 100, "maliyet": 3}) == \
        {"cikti": 25.0, "girdi": 0.0, "maliyet": 25.0}
    assert tasarruf({"cikti": 0, "girdi": 10, "maliyet": 1}, {"cikti": 5, "girdi": 12, "maliyet": 1}) == \
        {"cikti": 0.0, "girdi": -20.0, "maliyet": 0.0}
