"""VİDEO-14-devam-2: uzun video bölüm bölüm paralel tarama (VIDEO_UZUN_PARALEL) + indirme kenarı (VIDEO_INDIR_KENAR); varsayılan kapalı."""
from pathlib import Path

from video import cli
from video import parti

METIN = """# V1 · Başlık · Kanal · süre 1:10:00 · sure_sn 4200 · short: false
## Chapter
0:00 Giriş
22:10 Kurulum
47:30 Ajanlar
## Açıklama bağlantıları
https://ornek.dev/a
## Segmentler
[0:05] merhaba
[23:00] kurulum anlatımı
devamı satırı
[1:05:00] son söz
## Ekranda/konuşmada URL'ler
ornek.dev/b · ekran · 48:00
## Kareler
C:/c/V1/goz/kareler/k000050.jpg · 0:05
C:/c/V1/goz/kareler/k013800.jpg · 23:00
C:/c/V1/goz/kareler/k039000.jpg · 1:05:00
"""


def test_bolum_sinir():
    """Bölüm başı ≥ UZUN_BOLUM_SN, en çok 3; sınır eşit bölme noktasına en yakın Chapter başı; Chapter yoksa eşit; kısa video tek bölüm."""
    assert parti.bolum_sinir({"sure": 4200, "metin": METIN}) == [(0, 1330), (1330, 2850), (2850, 4201)]
    assert parti.bolum_sinir({"sure": 2400, "metin": "# x\n"}) == [(0, 1200), (1200, 2401)]
    assert parti.bolum_sinir({"sure": 880, "metin": METIN}) == [(0, 881)]


def test_bolum_metin():
    """Zamanlı bölümlerde yalnız aralık satırları (zamansız satır öncekine bağlı, 1:05:00 saat biçimi), açıklama bağlantıları yalnız ilk bölümde."""
    b2 = parti.bolum_metin(METIN, 1330, 2850, False)
    assert "kurulum anlatımı\ndevamı satırı" in b2 and "merhaba" not in b2 and "son söz" not in b2
    assert "k013800" in b2 and "k000050" not in b2 and "k039000" not in b2 and "ornek.dev/a" not in b2 and "22:10 Kurulum" in b2
    b1 = parti.bolum_metin(METIN, 0, 1330, True)
    assert "ornek.dev/a" in b1 and "merhaba" in b1 and "ornek.dev/b" not in b1
    assert "son söz" in parti.bolum_metin(METIN, 2850, 4201, False)


def test_bolum_birlestir():
    """Yinelenen aday/url tek; öbür listeler uç uca; özet birleşik."""
    a = {"id": "V1", "ozet": "bir", "adaylar": [{"ad": "Claude Code"}], "urller": [{"url": "https://x.dev"}], "iddialar": ["i1"], "bolumler": [{"baslik": "a"}]}
    b = {"id": "V1", "ozet": "iki", "adaylar": [{"ad": "claude code"}, {"ad": "Ollama"}], "urller": [{"url": "x.dev/"}, {"url": "https://y.dev"}],
         "iddialar": ["i1", "i2"], "bolumler": [{"baslik": "b"}]}
    f = parti.bolum_birlestir([a, b])
    assert [x["ad"] for x in f["adaylar"]] == ["Claude Code", "Ollama"] and len(f["urller"]) == 2
    assert f["iddialar"] == ["i1", "i2"] and len(f["bolumler"]) == 2 and f["ozet"] == "bir iki"


def test_tara_ikili_bolumlu(monkeypatch, tmp_path):
    """Bayrakla uzun video bölüm × model eşzamanlı çağrı; bölüm istemi küçük, şema id enum'suz (A: ortak önek); bayraksız tek bölüm 2 çağrı."""
    yol = tmp_path / "paket.md"
    yol.write_text(METIN, encoding="utf-8")
    pk = {"V1": {**parti.paket_oku(yol), "metin": METIN}}
    cag, ad = [], {"sonnet": ["Ollama", "Cursor", "Zed"], "haiku": ["Warp", "Docker", "Figma"]}

    def cagir(sis, istem, sema, kareler, model, butce, env):
        cag.append((istem, sema["properties"]["videolar"]["items"]["properties"]["id"], model))
        b = int(x[1]) - 1 if (x := __import__("re").search(r"BÖLÜM (\d)", istem)) else 0
        return {"form": {"videolar": [{"id": "V1", "ozet": model, "adaylar": [{"ad": ad[model.split("-")[1]][b]}]}]}, "usd": .01, "usage": {}}

    d = {"butce": 1, "tavan": {"usd": 9}, "videolar": {"V1": {"tarama": {}}}}
    monkeypatch.setattr(parti, "_defter", lambda p: (0, 0))
    monkeypatch.setattr(parti.hafif, "GORSEL", False)
    env = {"VIDEO_JETON": "0", "VIDEO_UZUN_PARALEL": "1"}
    y = parti._tara_ikili(["V1"], pk, {}, lambda s: s, d, tmp_path, env, cagir, ["claude-sonnet-5-5", "claude-haiku-5-5"])
    assert y["cagri"] == 6 and len(y["form"]["videolar"]) == 1 and len(y["form"]["videolar"][0]["adaylar"]) == 6
    assert all(len(i) < len(METIN) + 200 and "BÖLÜM" in i for i, _, _ in cag) and all("enum" not in s for _, s, _ in cag)
    cag.clear()
    y = parti._tara_ikili(["V1"], pk, {}, lambda s: s, d, tmp_path, {"VIDEO_JETON": "0"}, cagir, ["claude-sonnet-5-5", "claude-haiku-5-5"])
    assert y["cagri"] == 2 and all("enum" in s for _, s, _ in cag)


def test_tara_ikili_paralel_b(monkeypatch, tmp_path):
    """PARALEL-2: VIDEO_UZUN_PARALEL=2 → birincil model yalnız 1. bölümde (3+1 = 4 çağrı), bölüm şemasında urller + kurulum_komutlar zorunlu
    (v14p tekrar 2: b3 iki kol da bu opsiyonel alanları boş geçti → url 14/20, komut 16/31)."""
    yol = tmp_path / "paket.md"
    yol.write_text(METIN, encoding="utf-8")
    pk = {"V1": {**parti.paket_oku(yol), "metin": METIN}}
    cag = []

    def cagir(sis, istem, sema, kareler, model, butce, env):
        cag.append((model, "BÖLÜM 1/" in istem, sema["properties"]["videolar"]["items"]["required"]))
        return {"form": {"videolar": [{"id": "V1", "ozet": model, "adaylar": [{"ad": model}]}]}, "usd": .01, "usage": {}}

    d = {"butce": 1, "tavan": {"usd": 9}, "videolar": {"V1": {"tarama": {}}}}
    monkeypatch.setattr(parti, "_defter", lambda p: (0, 0))
    monkeypatch.setattr(parti.hafif, "GORSEL", False)
    y = parti._tara_ikili(["V1"], pk, {}, lambda s: s, d, tmp_path, {"VIDEO_JETON": "0", "VIDEO_UZUN_PARALEL": "2"}, cagir,
                          ["claude-sonnet-5-5", "claude-haiku-5-5"])
    assert y["cagri"] == 4 and [b for m, b, _ in cag if "sonnet" in m] == [True] and sum("haiku" in m for m, _, _ in cag) == 3
    assert all({"urller", "kurulum_komutlar"} <= set(r) for _, _, r in cag)
    cag.clear()
    parti._tara_ikili(["V1"], pk, {}, lambda s: s, d, tmp_path, {"VIDEO_JETON": "0", "VIDEO_UZUN_PARALEL": "1"}, cagir, ["claude-sonnet-5-5", "claude-haiku-5-5"])
    assert len(cag) == 6 and not any("urller" in r for _, _, r in cag)


def test_indir_kenar(monkeypatch, tmp_path):
    """VIDEO_INDIR_KENAR=<px> → yt-dlp biçimi uzun kenar ≤ px, akış URL önbelleği kenara ayrışır; bayraksız 1920."""
    monkeypatch.delenv("VIDEO_INDIR_KENAR", raising=False)
    assert cli.indir_bicim() == "bv*[width<=1920][height<=1920][vcodec!=none]"
    monkeypatch.setenv("VIDEO_INDIR_KENAR", "1280")
    assert cli.indir_bicim() == "bv*[width<=1280][height<=1280][vcodec!=none]"
    (tmp_path / "akis.url").write_text("https://eski?expire=9999999999", encoding="utf-8")
    al = []
    monkeypatch.setattr(cli, "_kos", lambda ctx, a, t: al.append(a) or b"https://yeni")
    assert cli._akis_url({}, tmp_path) == "https://yeni" and "1280" in al[0][4] and (tmp_path / "akis1280.url").is_file()
