import json

from video import kisa


def test_blok_katalog_ve_iz(tmp_path):
    g = {"konusma_ozet": "x", "ekran_metni": ["a" * 300], "araclar": [{"ad": "AirLLM", "ne_dedi": "y", "zaman": "0:03"}, {"ad": "Claude", "ne_dedi": "z", "zaman": "0:05"}],
         "linkler": [], "komutlar": [], "iddialar": [], "_iz": {"model": "m"}}
    b = json.loads(kisa.blok("ig-1", g, {"Claude": "kurulu:yerlesik"}, {"AirLLM": {"lisans": "MIT"}}).split("\n", 1)[1])
    assert "_iz" not in b and len(b["ekran_metni"][0]) == 160
    assert b["araclar"][0]["katalog"] == "bilinmeyen" and b["araclar"][0]["arastirma"] == {"lisans": "MIT"}
    assert b["araclar"][1]["katalog"] == "kurulu:yerlesik" and "arastirma" not in b["araclar"][1]


def test_rapor_arac_basi_en_cok_4_satir():
    v = {"id": "ig-1", "ozet": "ö", "linkler": ["github.com/a/b"], "araclar": [{"ad": "A", "tur": "CLI", "link": "", "not": "n"}, {"ad": "B", "tur": "skill", "link": "l", "not": "m"}]}
    s = kisa.rapor(v, "gemini").splitlines()
    i = s.index("## Araçlar")
    assert s[i + 1].startswith("- **A** · CLI") and s[i + 3] == "- **B** · skill · l" and len(s[i + 1:s.index("## Linkler") - 1]) <= 4 * 2


def test_katalog_karar_onceligi(tmp_path, monkeypatch):
    t = tmp_path / "k.tsv"
    t.write_text("sira\tkalem\tkarar\n1\tMiroFish\tÖĞREN\n", encoding="utf-8")
    monkeypatch.setattr(kisa, "KARAR", t)
    monkeypatch.setattr(kisa.tr, "sozluk_kur", lambda ev, k: [("graphify", "skill")])
    assert kisa.katalog(["mirofish", "graphify", "YokBöyle"]) == {"mirofish": "ÖĞREN (ig-41)", "graphify": "kurulu:skill", "YokBöyle": None}


def test_izle_zaman_asiminda_siradaki_model(tmp_path, monkeypatch):
    def iste(url, key, govde, zaman):
        if kisa.MODELLER[0] in url:
            raise TimeoutError
        return {"candidates": [{"content": {"parts": [{"text": '{"araclar": []}'}]}}]}
    monkeypatch.setattr(kisa, "_iste", iste)
    monkeypatch.setattr(kisa, "parcalar", lambda d, m, k: [])
    j, iz = kisa.izle(tmp_path, env={"GEMINI_API_KEY": "x"})
    assert j == {"araclar": []} and iz["model"] == kisa.MODELLER[1]


def test_izle_hepsi_503_ise_bekleyip_yeniden(tmp_path, monkeypatch):
    import io, urllib.error
    cagri = []
    def iste(url, key, govde, zaman):
        cagri.append(url)
        if len(cagri) <= len(kisa.MODELLER):
            raise urllib.error.HTTPError(url, 503, "high demand", {}, io.BytesIO(b""))
        return {"candidates": [{"content": {"parts": [{"text": '{"araclar": [{"ad": "pip", "ne_dedi": "", "zaman": "0:01"}], "adlar": ["PIP", "uv", "uv", "<script src=\\"a.js\\"></script>"]}'}]}}]}
    monkeypatch.setattr(kisa, "_iste", iste)
    monkeypatch.setattr(kisa, "parcalar", lambda d, m, k: [])
    monkeypatch.setattr(kisa.time, "sleep", lambda s: None)
    j, iz = kisa.izle(tmp_path, env={"GEMINI_API_KEY": "x"})
    assert iz["model"] == kisa.MODELLER[0] and len(cagri) == len(kisa.MODELLER) + 1
    assert [a["ad"] for a in j["araclar"]] == ["pip", "uv"] and "adlar" not in j  # adlar araclar'a tekrarsız katılır


def test_paket_linkleri(tmp_path):
    (tmp_path / "paket.md").write_text("açıklama: https://github.com/a/b ve x.dev/y, yine https://github.com/a/b", encoding="utf-8")
    assert kisa.paket_linkleri(tmp_path) == ["https://github.com/a/b", "https://x.dev/y"] and kisa.paket_linkleri(tmp_path / "yok") == []


def test_sozluk_tara_kendi_raporu_ve_sik_ad_disarida(tmp_path, monkeypatch):
    env = tmp_path / "envanter.jsonl"
    env.write_text("\n".join(json.dumps(x) for x in [{"ad": "GliFormer", "kaynak": "docs/x-ig-Baska.md"}, {"ad": "AirLLM", "kaynak": "docs/x-ig-Bu.md"},
                                                     {"ad": "Agent", "kaynak": "a"}]), encoding="utf-8")
    monkeypatch.setattr(kisa, "ENVANTER", env)
    monkeypatch.setattr(kisa, "_TARAMA", {})
    for i in range(4):
        (tmp_path / f"ig-D{i}").mkdir()
        (tmp_path / f"ig-D{i}" / "paket.md").write_text("an agent", encoding="utf-8")
    d = tmp_path / "ig-Bu"
    d.mkdir()
    (d / "paket.md").write_text("AirLLM ile GliFormer ve agent", encoding="utf-8")
    assert [a["ad"] for a in kisa.sozluk_tara(d, {"araclar": []})] == ["GliFormer"]  # AirLLM kendi raporundan, Agent sık
    assert kisa.sozluk_tara(d, {"araclar": [{"ad": "gliformer"}]}) == []


def test_birlestir_tekrarsiz():
    g = kisa.birlestir({"araclar": [{"ad": "Browser Use"}]}, {"adlar": ["browser-use", "pip", "pip"]})
    assert [a["ad"] for a in g["araclar"]] == ["Browser Use", "pip"]
