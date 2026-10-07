"""VİDEO-GÖZ-1b-1 M4: yorumlar (sabit · kanal sahibi · link/kod/zaman/sözlük satırı, ≤800 tk) · ekranda/konuşmada URL'ler · altyazı 429."""
import json

from video import cli
from video import goz as g

HAM = [{"text": "harika video", "pinned": False, "sahip": False},
       {"text": "Repo burada:\nhttps://github.com/a/b\nteşekkürler", "pinned": True, "sahip": False},
       {"text": "3:15'te npx skills add x dedin\nçok iyi", "pinned": False, "sahip": False},
       {"text": "evet aynen", "pinned": False, "sahip": True},
       {"text": "Topview ile denedim süper", "pinned": False, "sahip": False}]


def test_yorum_sabit_sahip_ve_isaretli_satirlar():
    assert g.yorum_sec(HAM, ["Topview"]) == ["[sabit] Repo burada: / https://github.com/a/b / teşekkürler", "[sahip] evet aynen",
                                            "3:15'te npx skills add x dedin", "Topview ile denedim süper"]


def test_yorum_butcesi_oncelikle():
    out = g.yorum_sec(HAM, ["Topview"], butce=20, token=lambda s: 10)
    assert out == ["[sabit] Repo burada: / https://github.com/a/b / teşekkürler", "[sahip] evet aynen"]


def test_url_ekran_ve_konusmadan_tekil_ilk_zaman():
    out = g.urller_bul([("ekran", 30, "open localhost:5174 now"), ("ekran", 10, "dala.craftedbygc.com"),
                        ("ses", 5, "topview dot ai adresine girin"), ("ses", 40, "tekrar dala.craftedbygc.com")])
    assert out == [("topview.ai", "ses", 5), ("dala.craftedbygc.com", "ekran", 10), ("localhost:5174", "ekran", 30)]


def test_yorumlar_60_top_ham_saklanir_baglanti_yalniz_sabit_sahip(tmp_path):
    js = {"comments": [{"text": "x https://a.dev", "is_pinned": True}, {"text": "y https://b.dev", "author_is_uploader": True, "parent": "c1"},
                       {"text": "z https://c.dev"}]}
    cagri = []

    def kos(a, timeout):
        cagri.append(a)
        return 0, json.dumps(js).encode(), b""
    d = tmp_path / "abcdefghijk"
    d.mkdir()
    linkler, durum = cli._yorumlar({"kos": kos, "uyku": lambda s: None}, d)
    assert linkler == ["https://a.dev", "https://b.dev"] and durum == "✓"
    assert "max_comments=60" in " ".join(cagri[0]) and "comment_sort=top" in " ".join(cagri[0])
    assert [h["sahip"] for h in json.loads((d / "yorumlar.json").read_text(encoding="utf-8"))["ham"]] == [False, True, False]


def test_eski_yorum_onbellegi_yeniden_cekilir(tmp_path):
    d = tmp_path / "abcdefghijk"
    d.mkdir()
    (d / "yorumlar.json").write_text('{"durum": "✓", "yorumlar": ["eski"]}', encoding="utf-8")
    n = []
    cli._yorumlar({"kos": lambda a, timeout: (n.append(1), (0, b'{"comments": []}', b""))[1], "uyku": lambda s: None}, d)
    assert n == [1]
