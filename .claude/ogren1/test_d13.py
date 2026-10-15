"""d13 sert denetim: yalnız alıntı/komut birebir + kapalı liste + kaynaksız RET; sahiplik/belirsiz yalnız uyarı"""
from d13 import sert

M = "# aracim\nKurulum ve kullanım bölümü burada.\n\n## Usage\n\n    other-tool run --fast\n\nOnly works on Linux hosts.\n"
ADLAR = {"aracim"}


def r(**k):
    o = {"ne_yapar": "x", "komut": "belirsiz — yok", "sinirlar": "y", "mekanizma": ["sıkıştırma"], "kanit": "Kurulum ve kullanım bölümü burada.",
         "alinti": {"ne_yapar": "Kurulum ve kullanım bölümü burada.", "sinirlar": "Only works on Linux hosts."}}
    o.update(k)
    return o


def test_sahiplik_uyari_ret_degil():
    o = r(komut="other-tool run --fast", alinti=dict(r()["alinti"], komut="other-tool run --fast"))
    ret, uyari = sert(o, M, ADLAR)
    assert ret is None and any("kendi adını" in u for u in uyari)


def test_kendi_ifadesi_komut_ret():
    o = r(komut="aracim çalıştır", alinti=dict(r()["alinti"], komut="Kurulum ve kullanım bölümü burada."))
    assert sert(o, M, ADLAR)[0] == "komut belgede birebir değil"


def test_alinti_birebir_degil_ret():
    o = r(alinti=dict(r()["alinti"], sinirlar="Works only on Linux hosts."))
    assert sert(o, M, ADLAR)[0] == "sinirlar alıntısı belgede yok"


def test_mekanizma_kapali_liste():
    assert sert(r(mekanizma=["hızlandırma"]), M, ADLAR)[0] == "mekanizma/kanıt geçersiz"


def test_kaynaksiz_tahmin_ret():
    assert sert(r(), "tek satır\n", ADLAR)[0] == "kaynaksız kalemde tahmin"
