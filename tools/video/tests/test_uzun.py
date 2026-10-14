from video import uzun


def test_araliklar_kisa_kuyruk_oncekine_katilir():
    assert uzun.araliklar(6407) == [(0, 1200), (1200, 2400), (2400, 3600), (3600, 4800), (4800, 6000), (6000, 6408)]
    assert uzun.araliklar(2500) == [(0, 1200), (1200, 2501)]
    assert uzun.araliklar(3000) == [(0, 1200), (1200, 2400), (2400, 3001)]


def test_birlestir_tekrarsiz():
    a = {"konusma_ozet": "a", "ekran_metni": "", "araclar": [{"ad": "Claude Code", "ne_dedi": "x", "zaman": "1:00"}], "adlar": ["uv"],
         "linkler": ["https://x.dev"], "komutlar": [], "iddialar": []}
    b = {"konusma_ozet": "b", "ekran_metni": "e", "araclar": [{"ad": "claude code", "ne_dedi": "y", "zaman": "21:00"}, {"ad": "Cursor", "ne_dedi": "z", "zaman": "22:00"}],
         "adlar": ["uv", "pip"], "linkler": ["https://x.dev"], "komutlar": ["uv sync"], "iddialar": []}
    j = uzun.birlestir([a, b])
    assert [x["ad"] for x in j["araclar"]] == ["Claude Code", "Cursor"]
    assert j["adlar"] == ["uv", "pip"] and j["linkler"] == ["https://x.dev"] and j["konusma_ozet"] == "a\nb"


def test_rapor_md_altin_puan_okur():
    from video import altin
    md = uzun.rapor_md(["Cursor | IDE"], ["https://x.dev"], ["https://y.dev"], ["uv sync"])
    p = altin.puan(md, {"adaylar": [{"ad": "Cursor", "tur": "uygulama"}], "linkler": [{"url": "https://x.dev"}], "urller": [{"url": "https://y.dev"}],
                        "komutlar": [{"komut": "uv sync"}]})
    assert p["yakalama"] == (1, 1) and p["link_aciklama"]["yakalama"] == (1, 1) and p["urller"] == (1, 1) and p["komutlar"] == (1, 1)


def test_pencereler_ortusur_ve_kuyrugu_kapsar():
    m = "".join(chr(97 + i % 26) for i in range(5000))
    p = uzun.pencereler(m, boy=2000, ortusme=100)
    assert all(len(x) <= 2000 for x in p) and p[-1] == m[-len(p[-1]):]
    assert all(p[i][-100:] == p[i + 1][:100] for i in range(len(p) - 1))
    assert uzun.pencereler("kısa", boy=2000, ortusme=100) == ["kısa"]
