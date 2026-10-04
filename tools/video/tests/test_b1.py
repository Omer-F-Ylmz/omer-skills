"""DERİNLİK-MASTER B1: link toplama — açıklama + yorum + OCR + altyazıda geçen URL/alan adları, sınıf (github · gist · doküman · blog ·
ürün/marketplace · video · sosyal · diğer), linkli sayfalardaki ilgili linkler (1 derinlik); aynı URL bütün partilerde bir kez okunur."""
import json
import urllib.error
from pathlib import Path

from video import getir as gt, tarama as tr
from test_c3 import KUTU, OcrKos
from test_video import VID, ortam  # noqa: F401 (ortam fixture)
from test_video import onbellek
from video.cli import main


def test_sinif():
    beklenen = {
        "https://github.com/o/r": "github", "https://gist.github.com/u/abc": "gist",
        "https://docs.anthropic.com/en/x": "doküman", "https://foo.readthedocs.io/a": "doküman", "https://foo.com/docs/kur": "doküman",
        "https://medium.com/@a/yazi": "blog", "https://dev.to/a/b": "blog", "https://blog.foo.com/x": "blog", "https://foo.com/blog/y": "blog",
        "https://www.npmjs.com/package/x": "ürün/marketplace", "https://marketplace.visualstudio.com/items?itemName=a.b": "ürün/marketplace",
        "https://smithery.ai/server/x": "ürün/marketplace", "https://cursor.com": "ürün/marketplace",
        "https://youtu.be/abc": "video", "https://www.youtube.com/watch?v=abc": "video",
        "https://x.com/a/status/1": "sosyal", "https://www.linkedin.com/in/a": "sosyal",
        "https://foo.com/fiyat/plan": "diğer",
    }
    assert {u: tr.link_sinif(u) for u in beklenen} == beklenen


def test_dort_kaynak_tekil_cıplak_alan_adi_dosya_adi_degil():
    b = tr.link_topla({"açıklama": "Repo: https://github.com/o/r.", "yorum": "bkz https://dev.to/a/b",
                       "ocr": "github.com/o/r · cursor.com · SKILL.md · install.sh · node.js · ali@foo.com",
                       "altyazı": "docs.anthropic.com/en/x adresinde anlatılıyor"})
    assert b == [{"url": "https://github.com/o/r", "sinif": "github", "kaynak": ["açıklama", "ocr"]},
                 {"url": "https://dev.to/a/b", "sinif": "blog", "kaynak": ["yorum"]},
                 {"url": "https://cursor.com", "sinif": "ürün/marketplace", "kaynak": ["ocr"]},
                 {"url": "https://docs.anthropic.com/en/x", "sinif": "doküman", "kaynak": ["altyazı"]}]


SAYFA = {"https://dev.to/a/b": '<html><main><p>Kurulum</p><a href="https://github.com/o/yeni">r</a><a href="https://x.com/a">s</a>'
                               '<a href="/a/c">aynı site yazı</a><a href="https://github.com/o/r">eski</a></main></html>',
         "https://cursor.com": "<html><main>ürün</main></html>"}


def test_derinlik1_ilgili_linkler_onbellek_partiler_arasi(tmp_path):
    cagri = []

    def al(u):
        cagri.append(u)
        if u not in SAYFA:
            raise urllib.error.URLError("yok")
        return SAYFA[u]

    b = tr.link_topla({"açıklama": "https://github.com/o/r https://dev.to/a/b https://cursor.com https://youtu.be/v https://ölü.dev/x"})
    yeni = gt.derinlik1(b, tmp_path, al=al)
    assert yeni == [{"url": "https://github.com/o/yeni", "sinif": "github", "kaynak": ["sayfa https://dev.to/a/b"]}]  # sosyal/blog/eski düşer
    assert "https://youtu.be/v" not in cagri and "https://github.com/o/r" not in cagri  # video/sosyal açılmaz; github B3'te gh ile
    ilk = len(cagri)
    assert gt.derinlik1(b, tmp_path, al=al) == yeni and cagri[ilk:] == ["https://ölü.dev/x"]  # ikinci parti: okunan önbellekten, yalnız erişilemeyen yeniden


def test_paket_baglantilar_json(ortam):
    onbellek(ortam, ["kurulum docs.anthropic.com/en/x adresinde"], duration=600)
    kos = OcrKos({"k00030": {"tr": [["github.com/o/r", *KUTU(0)]], "en": []}})
    assert main(["paket", VID, "--kare", "1", "--istek-tavan", "0"], env=ortam, kos=kos, uyku=lambda s: None) == 0
    b = json.loads((Path(ortam["VIDEO_CACHE"]) / VID / "baglantilar.json").read_text(encoding="utf-8"))
    assert {x["url"]: x["kaynak"] for x in b} == {"https://a.com/x": ["açıklama"], "https://b.io/y": ["açıklama"],
                                                  "https://docs.anthropic.com/en/x": ["altyazı"], "https://github.com/o/r": ["ocr"]}
