"""VİDEO-KAPANIŞ-3: (1) gizli değer süzgeci — key/token/secret/sig/password=… değeri "[gizlendi]"; (2) "(düşük güven)" KAÇAN?
otomatik kapanır (denetim.md'de toplu sayı + kural adı), gerçek KAÇAN? .kos/kopru/kacan-gercek.md'ye dökülür; (4) geçersiz
sebepli "aday değil" İz satırı ayıklanır, "İz: yok (geçersiz sebep ayıklandı)" notu kalır."""
from video import akil as ak
from video import tarama as tr

S = "abcDEF123secret"


def test_gizle_sorgu_ve_ciplak():
    m = (f"https://x.dev/login?key={S}&page=2 · https://api.a.com/v2/me?token={S} · token={S} · "
         f"?api_key={S}&sig={S}&Password={S}#x · sort_key=1 · monkey=2")
    g = tr.gizle(m)
    assert S not in g and g.count("[gizlendi]") == 6
    assert "page=2" in g and "sort_key=1" in g and "monkey=2" in g and tr.gizle(g) == g


def _z(**k):
    z = {"bahis": 0, "baglanan": 0, "aday_degil": 0, "kacan": [], "dusuk": [], "degil": [], "iz_yok": [], "konusma_yok": [],
         "erisilemedi": [], "eski_sema": []}
    return {**z, **k}


def test_cikti_ve_denetim_md_gizler():
    z = _z(erisilemedi=[("v1", f"https://api.apify.com/v2/users/me?token={S}", "403")], kacan=[("v1", "URL", f"https://a.b/?key={S}")])
    assert S not in "\n".join(ak._denetim_satir(z)) and S not in ak.denetim_md({"parti": "p"}, z, {})


def test_dusuk_guven_otomatik_kapanir_toplu_sayi():
    z = _z(dusuk=[("v1", "konuşma", "Foo"), ("v2", "kare", "Bar"), ("v2", "kare", "Baz")])
    k = tr.bolum(ak.denetim_md({"parti": "p"}, z, {}), "KAÇAN?")
    assert "Foo" not in k and "düşük güven — otomatik (OCR gürültüsü / genel terim): 3" in k
    s = "\n".join(ak._denetim_satir(z))
    assert "Foo" not in s and "düşük güven — otomatik (OCR gürültüsü / genel terim): 3" in s


def test_gercek_kacan_desktopa_dokulur_tekrar_yazmaz(tmp_path):
    z = _z(kacan=[("v1", "URL", "https://foo.dev/kit"), ("v2", "sözlük", "Cursor")])
    for _ in range(2):
        ak.kacan_dok(tmp_path, "p1", z)
    ak.kacan_dok(tmp_path, "p2", _z(kacan=[("v9", "URL", "x/y")]))
    t = (tmp_path / ".kos" / "kopru" / "kacan-gercek.md").read_text(encoding="utf-8")
    assert t.count("- p1 · v1 · URL · https://foo.dev/kit") == 1 and "- p1 · v2 · sözlük · Cursor" in t and "- p2 · v9 · URL · x/y" in t


R = ("## Künye\nBaşlık · süre: 10:00 · şema 2\n## İz\n| kaynak | ne | bağlandığı | kanıt |\n|---|---|---|---|\n"
     "| konuşma 01:00 | rtk | rtk | geçti |\n| konuşma 02:00 | GitHub | aday değil: yalnız genel kavram | geçti |\n"
     "| konuşma 03:00 | Foo | aday değil: konu dışı | geçti |\n## Sonraki\nx\n")


def test_iz_gecersiz_sebep_ayiklanir():
    y = tr.iz_ayikla(R)
    assert not any(h.startswith("İz sebebi geçersiz") for h in tr.denetle(y))
    assert "GitHub" not in tr.bolum(y, "İz").split("İz: yok")[0] and "- İz: yok (geçersiz sebep ayıklandı) · GitHub" in y
    assert "| Foo | aday değil: konu dışı |" in y and "| rtk | rtk |" in y and "## Sonraki\nx" in y and tr.iz_ayikla(y) == y
