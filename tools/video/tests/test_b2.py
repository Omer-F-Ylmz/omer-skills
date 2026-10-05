"""B2: getir.derinlik1 pakete bağlı (okuyucu ctx'ten, sahte) · yeni bağlantılar paket.md'de kendi bölümünde + kaçak kaynağında ·
erişilemeyen 'erişilemedi (sebep)' · B ek: bağlantılı video kuyruğa (kanal takibi yok, tekrar yok)."""
import json
import urllib.error
from pathlib import Path

from video import tarama as tr
from test_c3 import KUTU, OcrKos
from test_video import VID, ortam  # noqa: F401 (ortam fixture)
from test_video import onbellek
from video.cli import main

SAYFA = {"https://a.com/x": '<html><main><p>Kurulum</p><a href="https://github.com/yeni/arac">r</a>'
                            '<a href="https://youtu.be/BBBBBBBBBBB">v</a></main></html>'}


def al(u):
    if u not in SAYFA:
        raise urllib.error.HTTPError(u, 403, "Forbidden", {}, None)
    return SAYFA[u]


class Kos(OcrKos):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.yt = []

    def __call__(self, args, timeout=None):
        if args[0] == "yt-dlp" and str(args[-1]).startswith("https://youtu.be/"):  # yalnız B ek meta isteği; paketin kendi -J'si OcrKos'ta
            self.yt.append(args[-1])
            return 0, json.dumps({"duration": 300, "title": "Bağlı | T"}).encode(), b""
        return super().__call__(args, timeout)


def _paket(ortam, kos, *ek):
    return main(["paket", VID, "--kare", "1", "--istek-tavan", "0", *ek], env=ortam, kos=kos, uyku=lambda s: None, al=al)


def test_derinlik_paket_bolumu_erisilemedi_ve_kacan(ortam):
    d = onbellek(ortam, ["kurulum anlatılıyor"], duration=600)
    assert _paket(ortam, Kos({"k00030": {"tr": [], "en": []}})) == 0
    md = (d / "paket.md").read_text(encoding="utf-8")
    bb = tr.bolum(md, "Bağlantılı sayfalar")
    assert "https://github.com/yeni/arac (sayfa https://a.com/x)" in bb
    assert "erişilemedi" not in md and "b.io" not in bb  # Ömer kararı (O21 seçenek 2): erişilemeyen paket.md'ye yazılmaz
    ek = json.loads((d / "kapsam.json").read_text(encoding="utf-8"))["erisilemedi"]
    assert [u for u, _ in ek] == ["https://b.io/y"] and "403" in ek[0][1]
    b ={x["url"]: x["kaynak"] for x in json.loads((d / "baglantilar.json").read_text(encoding="utf-8"))}
    assert b["https://github.com/yeni/arac"] == ["sayfa https://a.com/x"] and b["https://youtu.be/BBBBBBBBBBB"] == ["sayfa https://a.com/x"]
    eng, _ = tr.kacan_video("# r\n## İz\nyok\n", d / "paket.md", [])
    assert any("yeni/arac" in str(x) for x in eng)  # İz'de olmayan derinlik aracı KAÇAN?


def test_bagli_video_kuyruga_tekrar_yok(ortam, tmp_path):
    onbellek(ortam, ["x"], duration=600, description="https://youtu.be/AAAAAAAAAAA https://youtu.be/CCCCCCCCCCC https://a.com/x")
    ky = tmp_path / "kuyruk.md"
    ky.write_text("# kuyruk\n| id | süre | başlık | not | durum |\n|---|---|---|---|---|\n| AAAAAAAAAAA | 3.0 | a | x | işlendi: abc |\n", encoding="utf-8")
    kos = Kos({"k00030": {"tr": [], "en": []}})
    assert _paket(ortam, kos, "--kuyruk", str(ky)) == 0
    k = ky.read_text(encoding="utf-8")
    assert f"| CCCCCCCCCCC | 5.0 | Bağlı / T | bağlantılı video ({VID}) | bekliyor |" in k
    assert f"| BBBBBBBBBBB | 5.0 | Bağlı / T | bağlantılı video ({VID}) | bekliyor |" in k  # sayfadan
    assert k.count("AAAAAAAAAAA") == 1 and sorted(kos.yt) == ["https://youtu.be/BBBBBBBBBBB", "https://youtu.be/CCCCCCCCCCC"]
    assert _paket(ortam, kos, "--kuyruk", str(ky)) == 0
    assert ky.read_text(encoding="utf-8") == k and len(kos.yt) == 2  # kuyrukta → tekrar eklenmez, meta isteği yok
    assert all("--flat-playlist" not in a for a in kos.cagri)  # kanal çözümü/takibi yok (yalnız tek video -J)


def test_paket_kuyruksuz_kuyruga_dokunmaz(ortam):
    onbellek(ortam, ["x"], duration=600, description="https://youtu.be/CCCCCCCCCCC")
    kos = Kos({"k00030": {"tr": [], "en": []}})
    assert _paket(ortam, kos) == 0 and kos.yt == []


def test_erisilemeyen_iki_sayfa_paket_md_yok_kapsam_denetim(ortam, tmp_path, monkeypatch, capsys):
    """Ömer kararı (O21 seçenek 2): erişilemeyen → paket.md'de bölüm yok · kapsam.json erisilemedi · Denetim satırı · kapat durmaz."""
    d = onbellek(ortam, ["x"], duration=600, description="https://c.com/p https://d.io/q")
    assert _paket(ortam, Kos({"k00030": {"tr": [], "en": []}})) == 0
    assert "Bağlantılı sayfalar" not in (d / "paket.md").read_text(encoding="utf-8")
    k = json.loads((d / "kapsam.json").read_text(encoding="utf-8"))
    assert sorted(u for u, _ in k["erisilemedi"]) == ["https://c.com/p", "https://d.io/q"] and "erişilemedi" not in k["izleme"]
    from video import akil as ak
    from test_d3_konusma import _d
    onb = tmp_path / "onb"
    pd = _d(tmp_path, "altyazı")
    (onb / "v1" / "kapsam.json").write_text(json.dumps({"izleme": "x", "erisilemedi": k["erisilemedi"]}), encoding="utf-8")
    monkeypatch.setattr(tr, "denetle", lambda m: [])
    monkeypatch.setattr(ak, "_islenmemis", lambda kok, p: ["sonraki kapı"])
    assert ak.kapat(tmp_path / "pd", pd, tmp_path, {"kok": onb}) == 1
    out = capsys.readouterr().out
    assert "Denetim → DUR" not in out and "kayda işlenmemiş" in out  # erişilemedi kapat'ı durdurmaz
    sat = ak._denetim_satir(ak.denetim(pd, tmp_path, onb))
    assert "erişilemedi 2" in sat[0] and "- erişilemedi: v1 · https://c.com/p (" in "\n".join(sat)
