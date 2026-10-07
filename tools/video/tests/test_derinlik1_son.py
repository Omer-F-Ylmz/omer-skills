"""DERİNLİK-1 SON: R4 short kare ipucu + yorum bağlantıları · R1b araştırılmış adaya Güncellik bölümü. Ağsız."""
import json

from test_derinlik1 import Ar, _ctx, _gh_ust, _kurulu_ortam, _ns, _uyku

from video import cli
from video import parti as pt


# R4 altyazıda repo/GitHub/link/prompt geçen short'ta kare tavanı 3 → 8
def test_r4_short_kare_ipucu():
    assert cli.kare_tavan(60, 8, "kod github'da, repo linki açıklamada") == 8
    assert cli.kare_tavan(60, 8, "sadece sohbet") == 3 and cli.kare_tavan(60, 8) == 3 and cli.kare_tavan(300, 8, "github") == 8
    assert pt.kare_sayisi(60, False, True) == (8, "short ipucu ≤8") and pt.kare_sayisi(60, False) == (3, "short ≤3")


def _kos_sahte(gelen, cikti):
    def kos(ctx, args, timeout):
        gelen.append(args)
        if isinstance(cikti, Exception):
            raise cikti
        return json.dumps(cikti).encode()
    return kos


# R4 sabitlenmiş/yazar yorumundaki bağlantılar kaynağa girer; en fazla 20 yorum, indirme yok
def test_r4_yorum_baglantilari(tmp_path, monkeypatch):
    gelen = []
    monkeypatch.setattr(cli, "_kos", _kos_sahte(gelen, {"comments": [
        {"text": "repo: https://github.com/a/b", "is_pinned": True},
        {"text": "spam https://spam.com/x"},
        {"text": "yazar notu https://x.io/p", "author_is_uploader": True}]}))
    lk, durum = cli._yorumlar({"uyku": lambda s: None}, tmp_path)
    assert lk == ["https://github.com/a/b", "https://x.io/p"] and durum == "✓"
    a = " ".join(gelen[0])
    assert "--write-comments" in a and "--skip-download" in a and "max_comments=60" in a
    assert json.loads((tmp_path / "yorumlar.json").read_text(encoding="utf-8"))["durum"] == "✓"


def test_r4_yorum_alinamadi_sebep(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "_kos", _kos_sahte([], cli.Hata("HTTP Error 403: Forbidden")))
    lk, durum = cli._yorumlar({"uyku": lambda s: None}, tmp_path)
    assert lk == [] and durum.startswith("yorum alınamadı (") and "403" in durum


# --- R1b fark bulunan, önceden araştırılmış aday: aday.md sonuna Güncellik bölümü; mevcut içerik değişmez
def test_r1b_guncellik_bolumu_eklenir(tmp_path):
    p, evi = _kurulu_ortam(tmp_path)
    y = tmp_path / "docs" / "kurulumlar" / "adaylar" / "hizli-paket.md"
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_bytes("# hizli-paket\neski içerik\n".encode("utf-8"))
    c = {**_ctx(tmp_path, Ar({})), "gh": _gh_ust, "uyku": _uyku()}
    c["env"]["CLAUDE_EVI"] = str(evi)
    pt.parti(_ns("akil", p.name), c)
    t = y.read_bytes().decode("utf-8")
    assert t.startswith("# hizli-paket\neski içerik\n")
    g = t.split("## Güncellik (", 1)[1]
    assert "kurulu aaaaaaa ↔ upstream bbbbbbb" in g and "skills/yeni-skill" in g
    pt.parti(_ns("akil", p.name, yeniden=True), c)
    assert y.read_bytes().decode("utf-8").count("## Güncellik (") == 1
