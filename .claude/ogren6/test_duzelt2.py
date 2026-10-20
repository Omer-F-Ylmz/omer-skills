import duzelt2

BEL = {"deger": "belirsiz — x", "alinti": ""}
M = "---\nname: demo-arac\ndescription: Demo\n---\n# Demo\nGenel bilgi satiri burada.\nNote: this tool requires a running server before use.\n"


def test_komut_name_satiri():
    o = duzelt2.duzelt({"ad": "demo-arac", "komut": dict(BEL), "sinirlar": dict(BEL)}, M)
    assert o["komut"] == {"deger": "name: demo-arac", "alinti": "name: demo-arac"}


def test_sinir_gevsek_satir_birebir():
    o = duzelt2.duzelt({"ad": "demo-arac", "komut": dict(BEL), "sinirlar": dict(BEL)}, M)
    assert o["sinirlar"]["alinti"] == "Note: this tool requires a running server before use."
    assert o["sinirlar"]["alinti"] in M


def test_kaynakta_yoksa_belirsiz_kalir():
    o = duzelt2.duzelt({"ad": "x", "komut": dict(BEL), "sinirlar": dict(BEL)}, "sade metin\nbaska sade metin satiri\n")
    assert o["komut"]["deger"].startswith("belirsiz") and o["sinirlar"]["deger"].startswith("belirsiz")


def test_dolu_alana_dokunmaz():
    d = {"deger": "x", "alinti": "y"}
    assert duzelt2.duzelt({"ad": "a", "komut": d, "sinirlar": d}, M) == {"ad": "a", "komut": d, "sinirlar": d}


def test_ders_yuvasi_isareti_sinir_degil():
    m = "# T\n<!-- ders-yuvasi:basla -->\nNEVER dosya degistirme, yalniz oku.\n"
    o = duzelt2.duzelt({"ad": "x", "komut": {"deger": "k", "alinti": "k"}, "sinirlar": {"deger": "Kaynaktaki kural: <!-- ders-yuvasi:basla -->", "alinti": "<!-- ders-yuvasi:basla -->"}}, m)
    assert o["sinirlar"]["alinti"] == "NEVER dosya degistirme, yalniz oku."


def test_komut_kendi_slash_adi():
    m = "---\nname: qa-only\n---\ngstack-skill-start --skill qa-only\nCalistir: /qa-only raporu uret\n"
    o = duzelt2.duzelt({"ad": "qa-only", "komut": {"deger": "gstack-skill-start --skill qa-only", "alinti": "gstack-skill-start --skill qa-only"}, "sinirlar": {"deger": "s", "alinti": "s"}}, m)
    assert o["komut"]["alinti"] == "Calistir: /qa-only raporu uret"
