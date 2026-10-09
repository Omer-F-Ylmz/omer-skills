"""VİDEO-KAPANIŞ-4: Desktop KAÇAN? triyajı (tsv: parti · video · kaynak · terim · karar(kapat|aday) · sebep) dosyadan uygulanır —
`video parti kacan-karar <tsv>` kararları docs/kurulumlar/kacan-karar.tsv'ye yazar (aday → kurulum turu sebebi), kacan-gercek.md'den
kararlı satırları düşer, eşleşmeyenleri sayar; denetim kararlı KAÇAN?'ı sebebiyle kapatır (kapat'ı durdurmaz)."""
from video import akil as ak
from video import tarama as tr

S = "abcDEF123secret"


def _tsv(p, *satir):
    p.write_text("parti\tvideo\tkaynak\tterim\tkarar\tsebep\n" + "".join("\t".join(s) + "\n" for s in satir), encoding="utf-8")
    return p


def _gercek(kok, *satir):
    y = kok / ".kos" / "kopru" / "kacan-gercek.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text("# Gerçek KAÇAN? — Desktop kararı bekliyor\n" + "".join(f"- {' · '.join(s)}\n" for s in satir), encoding="utf-8")
    return y


def test_kacan_karar_uygular_sayar(tmp_path, capsys):
    g = _gercek(tmp_path, ("p1", "v1", "paket", "learn"), ("p1", "v1", "paket", "https://github.com/a/b"), ("p2", "v9", "kare", "Foo"))
    t = _tsv(tmp_path / "k.tsv", ("p1", "v1", "paket", "learn", "kapat", "genel terim"),
             ("p1", "v1", "paket", "https://github.com/a/b", "aday", "x"), ("p3", "v7", "paket", f"https://a.b/?key={S}", "kapat", "site"))
    assert ak.kacan_karar(tmp_path, t) == 1  # eşleşmeyen var → rc 1
    out = capsys.readouterr().out
    assert "uygulanan 2" in out and "eşleşmeyen KAÇAN? 1" in out and "eşleşmeyen karar 1" in out
    r = (tmp_path / ak.KACAN_KARAR).read_text(encoding="utf-8")
    assert f"p1\tv1\tpaket\thttps://github.com/a/b\taday\t{ak.ADAY_SEBEP}" in r and S not in r
    assert g.read_text(encoding="utf-8").splitlines()[1:] == ["- p2 · v9 · kare · Foo"]
    assert ak.kacan_karar(tmp_path, t) == 1 and "uygulanan 0" in capsys.readouterr().out  # ikinci kez: kayıt tekil


def test_denetim_kararli_kacani_sebebiyle_kapatir(tmp_path):
    _tsv(tmp_path / "k.tsv", ("p1", "v1", "paket", "learn", "kapat", "genel terim"), ("p1", "v1", "paket", "a/b", "aday", ""))
    ak.kacan_karar(tmp_path, tmp_path / "k.tsv")
    z = ak.kacan_kapat(tmp_path, "p1", {"kacan": [("v1", "paket", "learn"), ("v1", "paket", "a/b"), ("v2", "kare", "Foo")]})
    assert z["kacan"] == [("v2", "kare", "Foo")]
    assert z["kapanan"] == [("v1", "paket", "learn", "genel terim"), ("v1", "paket", "a/b", ak.ADAY_SEBEP)]
    z = {"bahis": 0, "baglanan": 0, "aday_degil": 0, "dusuk": [], "degil": [], "iz_yok": [], "konusma_yok": [], "erisilemedi": [],
         "eski_sema": [], **z}
    for m in ("\n".join(ak._denetim_satir(z)), tr.bolum(ak.denetim_md({"parti": "p1"}, z, {}), "KAÇAN?")):
        assert "Desktop kararıyla kapandı — genel terim: 1" in m and f"Desktop kararıyla kapandı — {ak.ADAY_SEBEP}: 1" in m
