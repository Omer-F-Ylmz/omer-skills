import json

from video import kisa


def test_ek_adlar_platform_ve_aciklama_alani(tmp_path):
    (tmp_path / "paket.md").write_text("## Açıklama\nRepo: agenthubstack.dev · @x.dev · instagram.com/a\n## Ekran metni (OCR)\n[0:01] GitHub Go to page, S3 bucket\n"
                                       "## Sözlük eşleşmeleri\nClaude\n", encoding="utf-8")
    e = {a["ad"]: a for a in kisa.ek_adlar(tmp_path, [{"ad": "github"}])}
    assert set(e) == {"S3", "agenthubstack.dev"}  # GitHub zaten var · "Go to" fiil · Claude yalnız sözlük bölümünde · @x.dev tutamak
    assert e["S3"]["tur"] == "platform" and e["agenthubstack.dev"]["link"] == "https://agenthubstack.dev"


def test_ek_adlar_ocr_dosya_adi(tmp_path):
    (tmp_path / "paket.md").write_text("## Ekran metni (OCR)\n[0:25] FILE=docker-compose.yml:docker-compose.rustfs.yml\n[0:22] TS vila.config.ts\n"
                                       "[0:30] cat .lefthookrc · tailwind.config.js · .envrc\n[0:31] Lefthook ve Tailwind\n## Açıklama\nyok\n", encoding="utf-8")
    e = {a["ad"]: a for a in kisa.ek_adlar(tmp_path, [{"ad": "Tailwind"}])}
    assert set(e) == {"rustfs", "lefthook"}  # compose servis adı tek başına yeter · config/rc ikinci geçiş ister (vila OCR bozuğu) · Tailwind zaten var · env genel
    assert e["rustfs"]["ne_dedi"] == "(OCR dosya adı: docker-compose.rustfs.yml)"


def test_rapor_sablon_alanlari_platform_ayri():
    v = {"id": "ig-1", "ozet": "ö", "linkler": ["github.com/a/b"], "iddialar": ["i"], "araclar": [
        {"ad": "A", "tur": "", "link": "", "not": "n", "katalog": "bilinmeyen", "karar": ("KUR", "MIT")},
        {"ad": "B", "tur": "skill", "link": "l", "not": "m", "katalog": "kurulu:x", "fark": False, "karar": None},
        {"ad": "Go", "tur": "platform", "link": "", "not": "", "katalog": "bilinmeyen"}]}
    s = kisa.rapor(v, "gemini").splitlines()
    i = s.index("## Araçlar")
    assert s[i + 1:i + 5] == ["- **A** · araç", "  n · katalogda yok · karar: KUR — MIT", "- **B** · skill · l", "  m · katalogda: kurulu:x · fark yok"]
    assert s[s.index("## Platformlar") + 1] == "Go" and "- i" in s


def test_katalog_karar_onceligi(tmp_path, monkeypatch):
    t = tmp_path / "k.tsv"
    t.write_text("sira\tkalem\tkarar\n1\tMiroFish\tÖĞREN\n", encoding="utf-8")
    monkeypatch.setattr(kisa, "KARAR", t)
    monkeypatch.setattr(kisa.tr, "sozluk_kur", lambda ev, k: [("graphify", "skill")])
    assert kisa.katalog(["mirofish", "graphify", "YokBöyle"]) == {"mirofish": "ÖĞREN (ig-41)", "graphify": "kurulu:skill", "YokBöyle": None}


def test_link_tamamla_karar_ve_kunye(tmp_path, monkeypatch):
    t = tmp_path / "k.tsv"
    t.write_text("sira\tkalem\tlink\tkarar\n1\tLaya\thttps://github.com/N/laya\tKUR\n2\tCCXT\t-\tÖĞREN\n", encoding="utf-8")
    monkeypatch.setattr(kisa, "KARAR", t)
    x = {"linkler": ["a.com"], "araclar": [{"ad": "laya", "link": ""}, {"ad": "CCXT", "link": ""}, {"ad": "Z", "link": ""}, {"ad": "Q", "link": "q.com"}]}
    kisa.link_tamamla(x, {"Z": "https://github.com/o/z"})
    assert [a["link"] for a in x["araclar"]] == ["https://github.com/N/laya", "", "https://github.com/o/z", "q.com"]
    assert x["linkler"] == ["a.com", "https://github.com/N/laya", "https://github.com/o/z", "q.com"]


def test_link_tamamla_kod_parcasi_arac_degil():
    x = {"linkler": [], "araclar": [{"ad": "agent = new PageAgent()", "link": ""}, {"ad": '<script src="a.js"></script>', "link": ""}, {"ad": "Page Agent", "link": ""}]}
    kisa.link_tamamla(x, {})
    assert [a["ad"] for a in x["araclar"]] == ["Page Agent"]


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


def test_paket_linkleri_ocr_github_basligi_dogrulanir(tmp_path, monkeypatch):
    (tmp_path / "paket.md").write_text("[0:13] logan-markewich /jeff\n[0:20] uydu / yok\n[0:40] src/jeff\n[0:41] bir cümle / iki kelime\n", encoding="utf-8")
    monkeypatch.setattr(kisa, "_repo_var", lambda r: r != "uydu/yok")
    assert kisa.paket_linkleri(tmp_path) == ["https://github.com/logan-markewich/jeff"]


def test_izle_teknik_ve_kurulum_komutu_araca_katilir(tmp_path, monkeypatch):
    y = '{"araclar": [{"ad": "AirLLM", "ne_dedi": "", "zaman": "0:01"}], "teknikler": ["katmanlı yükleme"], "komutlar": ["pip install airllm", "strix --target ."]}'
    monkeypatch.setattr(kisa, "_iste", lambda url, key, govde, zaman: {"candidates": [{"content": {"parts": [{"text": y}]}}]})
    monkeypatch.setattr(kisa, "parcalar", lambda d, m, k: [])
    j, _ = kisa.izle(tmp_path, env={"GEMINI_API_KEY": "x"})
    assert [a["ad"] for a in j["araclar"]] == ["AirLLM", "katmanlı yükleme", "pip install airllm"] and "teknikler" not in j


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


def test_repo_bul_arama_onbellekte(tmp_path, monkeypatch):
    monkeypatch.setattr(kisa, "ARASTIRMA", tmp_path)
    cagri = []
    monkeypatch.setattr(kisa.subprocess, "run", lambda a, **k: cagri.append(a) or type("R", (), {"returncode": 0, "stdout": "o/hermes-agent\n", "stderr": ""})())
    assert kisa.repo_bul("Hermes Agent", []) == ("o/hermes-agent", "gh arama, doğrulanmadı")
    assert kisa.repo_bul("Hermes Agent", []) == ("o/hermes-agent", "gh arama, doğrulanmadı")
    assert len(cagri) == 1


def test_calistir_paketin_reel_mp4unu_kullanir_ig_istegi_yok(tmp_path, monkeypatch):
    from video import instagram
    d = tmp_path / "kok" / "ig-X"
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps({"slayt_video": [], "gorseller": []}), encoding="utf-8")
    (d / "goz-video.mp4").write_bytes(b"v")
    gor = []
    monkeypatch.setattr(instagram, "getir", lambda m: (_ for _ in ()).throw(AssertionError("IG'ye ikinci istek")))
    monkeypatch.setattr(kisa, "izle", lambda k, m, env: (gor.append((m, (m / "goz-video.mp4").is_file())) or ({"araclar": [], "linkler": []}, {})))
    monkeypatch.setattr(kisa, "metin_gec", lambda k, env: {"_iz": {}})
    monkeypatch.setattr(kisa, "birlestir", lambda g, mg: g)
    monkeypatch.setattr(kisa, "paket_linkleri", lambda k: [])
    monkeypatch.setattr(kisa, "katalog", lambda adlar, kok, vid: {})
    monkeypatch.setattr(kisa.kr, "ver", lambda *a, **k: ({}, []))
    kisa.calistir(["ig-X"], tmp_path / "kok", tmp_path / "cik")
    assert gor == [(d, True)] and not (d / "goz-video.mp4").exists()


def test_calistir_claudesiz_deterministik_liste(tmp_path, monkeypatch):
    d = tmp_path / "kok" / "ig-X"
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps({"video": "u"}), encoding="utf-8")
    (d / "goz-video.mp4").write_bytes(b"v")
    g = {"araclar": [{"ad": "Bytebase", "ne_dedi": "x"}, {"ad": "veri göçü", "ne_dedi": "(teknik)"}], "linkler": ["https://a.dev"]}
    monkeypatch.setattr(kisa, "izle", lambda k, m, env: (g, {}))
    monkeypatch.setattr(kisa, "metin_gec", lambda k, env: {"_iz": {}})
    monkeypatch.setattr(kisa, "paket_linkleri", lambda k: ["https://b.dev"])
    monkeypatch.setattr(kisa, "katalog", lambda adlar, kok, vid: {a: "kurulu" for a in adlar})
    monkeypatch.setattr(kisa.kr, "ver", lambda *a, **k: (_ for _ in ()).throw(AssertionError("claude -p")))
    _, y = kisa.calistir(["ig-X"], tmp_path / "kok", tmp_path / "cik", claude=False, sil=False)
    x = y["form"]["videolar"][0]
    assert [(a["ad"], a["tur"]) for a in x["araclar"]] == [("Bytebase", ""), ("veri göçü", "teknik")]
    assert x["linkler"] == ["https://a.dev", "https://b.dev"] and (d / "goz-video.mp4").exists()


def test_metin_gec_ek_ornek_yalniz_pakette_gecen(tmp_path, monkeypatch):
    (tmp_path / "paket.md").write_text("Bytebase ile Slack botu", encoding="utf-8")
    monkeypatch.setattr(kisa, "anahtar", lambda env=None: "k")
    monkeypatch.setattr(kisa, "sozluk_tara", lambda d, g: [])
    yanit = {0: ["Slack"], 1: ["Bytebase", "Uydurma"]}
    monkeypatch.setattr(kisa, "_uret", lambda g, k, t, **kw: ({"adlar": yanit[g["generationConfig"]["temperature"]]}, {"model": "m"}))
    assert kisa.metin_gec(tmp_path)["adlar"] == ["Slack", "Bytebase"]


def test_metin_gec_ek_ornek_asilirsa_atlanir(tmp_path, monkeypatch):
    (tmp_path / "paket.md").write_text("Bytebase ile Slack botu", encoding="utf-8")
    monkeypatch.setattr(kisa, "anahtar", lambda env=None: "k")
    monkeypatch.setattr(kisa, "sozluk_tara", lambda d, g: [])
    gelen = []

    def uret(g, k, t, **kw):
        gelen.append(kw.get("zaman", kisa.IZLE_ZAMAN))
        if kw:
            raise RuntimeError("gemini: zaman aşımı")
        return {"adlar": ["Slack"]}, {"model": "m"}
    monkeypatch.setattr(kisa, "_uret", uret)
    assert kisa.metin_gec(tmp_path)["adlar"] == ["Slack"]
    assert sorted(gelen) == [kisa.EK_ZAMAN, kisa.EK_ZAMAN, kisa.IZLE_ZAMAN]
