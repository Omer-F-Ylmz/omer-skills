"""B4: genel web araması (aday başına en fazla N sorgu, ayarda; Agent Reach yolu = mcporter exa.web_search_exa): inceleme, karşılaştırma,
alternatif, bilinen sorun + yazarın duyuru/blog yazısı (B3'ten). Forum/sosyal "düşük güven". Sorgu hatası adayı düşürmez → erisilemedi.
Sahte kos + sahte saat; ağ yok."""
import io
import json
import urllib.error

import pytest

from video import getir as gt
from video import tarama as tr

from test_uygula import kok  # noqa: F401 (kok fixture)
from test_video import VID, ortam  # noqa: F401 (ortam fixture)


@pytest.fixture
def saat(monkeypatch):
    t = [1000.0]
    monkeypatch.setattr(gt, "saat", lambda: t[0])
    monkeypatch.setattr(gt, "uyku", lambda s: t.__setitem__(0, t[0] + s))
    monkeypatch.setattr(gt, "_son", [float("-inf")])
    return t


def kos_yap(t):
    q = [s.format(ad="arac") for s in gt.SORGU]
    yanit = {q[0]: (0, json.dumps({"results": [{"title": "İnceleme", "url": "https://blog.x/r"},
                                               {"title": "Konu", "url": "https://www.reddit.com/r/a/1"},
                                               {"title": "Üçüncü", "url": "https://e.x/3"},
                                               {"title": "Fazla", "url": "https://e.x/4"}]}).encode(), b""),
             q[1]: (0, "Title: Karşı\nURL: https://c.x/k\nText: uzun\n\nTitle: İnceleme\nURL: https://blog.x/r\n".encode(), b""),
             q[2]: (1, b"", b"mcporter: timeout")}

    def kos(args):
        a = " ".join(args)
        kos.cagri.append((a, t[0]))
        if args[0] != "mcporter":
            return 0, (b"[]" if "releases" in a else b"# R"), b""
        return yanit.get(next(x[6:] for x in args if x.startswith("query=")), (0, b"[]", b""))
    kos.cagri = []
    return kos


def test_web_bolumu_sorgu_tavani_dusuk_guven_tekil(tmp_path, saat):
    kos = kos_yap(saat)
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", kos=kos, web=True).read_text(encoding="utf-8"), "Web araması")
    m = [a for a, _ in kos.cagri if a.startswith("mcporter call exa.web_search_exa")]
    assert len(m) == min(len(gt.SORGU), gt.WEB["sorgu"]) and all("arac" in a for a in m)
    assert any("duyuru" in s or "blog" in s for s in gt.SORGU)  # B3'ten kalan: yazarın duyuru/blog yazısı
    assert "İnceleme · https://blog.x/r" in b and b.count("https://blog.x/r") == 1  # aynı URL tek satır
    assert [s for s in b.splitlines() if "reddit.com" in s][0].endswith("düşük güven") and "https://blog.x/r · düşük güven" not in b
    assert "Karşı · https://c.x/k" in b and ("https://e.x/4" in b) == (gt.WEB["sonuc"] >= 4)  # Title:/URL: metin biçimi · sonuç tavanı


def test_sorgu_hatasi_erisilemedi_aday_dusmez(tmp_path, saat):
    kj = tmp_path / "kapsam.json"
    kj.write_text(json.dumps({"izleme": "tam", "incelenmedi": []}), encoding="utf-8")
    kos = kos_yap(saat)
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", kos=kos, kapsam=kj, web=True).read_text(encoding="utf-8"), "Web araması")
    q2 = gt.SORGU[2].format(ad="arac")
    assert f"- erişilemedi: web: {q2} (" in b and "timeout" in b and "https://blog.x/r" in b
    assert json.loads(kj.read_text(encoding="utf-8"))["erisilemedi"] == [[f"web: {q2}", "mcporter: timeout · brave: BRAVE_API_KEY yok"]]


def test_web_istekleri_arasi_en_az_iki_sn(tmp_path, saat):
    kos = kos_yap(saat)
    gt.on(tmp_path, "VID", "arac", kos=kos, web=True)
    z = [z for a, z in kos.cagri if a.startswith("mcporter")]
    assert all(b - a >= 2 for a, b in zip(z, z[1:]))


def test_web_verilmezse_arama_yok(tmp_path, saat):
    kos = kos_yap(saat)
    y = gt.on(tmp_path, "VID", "arac", "o/r", kos=kos)
    assert not any(a.startswith("mcporter") for a, _ in kos.cagri) and "## Web araması" not in y.read_text(encoding="utf-8")


# B4 düzeltmeleri (Ömer kararı, 5 Eki)
EXA = ("Title: Taste review\nURL: https://blog.x/t\nPublished: 2026-09-14T10:00:00.000Z\nAuthor: a\nHighlights:\n"
       "Güçlü yanı   tasarım... zayıf yanı\nyavaş ... kurulum kolay\n---\n"
       "Title: Uzun\nURL: https://e.x/u\nPublished: 2026-01-02T00:00:00.000Z\nAuthor: b\nHighlights:\n" + "x" * 700 + "\n")


def test_highlights_ozet_tarih_600(tmp_path, saat):
    def kos(args):
        return 0, (EXA.encode() if args[0] == "mcporter" else b"[]"), b""
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", kos=kos, web=True).read_text(encoding="utf-8"), "Web araması")
    s = b.splitlines()
    i = next(n for n, x in enumerate(s) if "https://blog.x/t" in x)
    assert s[i].endswith("· Taste review · 2026-09-14 · https://blog.x/t")
    assert s[i + 1] == "  > Güçlü yanı tasarım zayıf yanı yavaş kurulum kolay"
    j = next(n for n, x in enumerate(s) if "https://e.x/u" in x)
    assert "2026-01-02 · https://e.x/u" in s[j] and s[j + 1] == "  > " + "x" * gt.WEB["ozet"] and gt.WEB["ozet"] == 600


@pytest.mark.parametrize("ad, repo, tur, q", [("taste", None, "skill", "taste skill review"),
                                               ("everything-claude-code", "affaan-m/everything-claude-code", "plugin", "everything-claude-code plugin review")])
def test_sorgu_repo_ya_da_ad_tur(tmp_path, saat, ad, repo, tur, q):
    kos = kos_yap(saat)
    gt.on(tmp_path, "VID", ad, repo, kos=kos, web=True, tur=tur)
    assert f"mcporter call exa.web_search_exa query={q} numResults={gt.WEB['sonuc'] + gt.WEB['fazla']}" in [a for a, _ in kos.cagri]


def test_gh_ara_crlf_govde_ve_oran_basligi(monkeypatch):
    bekle, cevap = [], [(1, b"HTTP/2.0 403 Forbidden\r\nRetry-After: 7\r\nX-RateLimit-Reset: 1\r\n\r\n{}", b"API rate limit exceeded"),
                        (0, b'HTTP/2.0 200 OK\r\nX-Ratelimit-Limit: 30\r\nX-Ratelimit-Resource: search\r\n\r\n{"items": [{"title": "a"}]}\r\n', b"")]
    monkeypatch.setattr(gt, "uyku", lambda s: bekle.append(s))
    assert json.loads("\n".join(gt._gh_ara(lambda a: cevap.pop(0), "search/issues"))) == {"items": [{"title": "a"}]}
    assert 7 in bekle  # Retry-After CRLF başlıkta okundu


def test_video_on_web_ara(monkeypatch, ortam, kok):  # noqa: F811
    from video.cli import main
    cagri = []
    monkeypatch.setattr(gt, "web_ara", lambda ad, kos, hata, repo=None, tur=None: cagri.append((ad, repo, tur)) or "## Web araması\n")
    assert main(["on", VID, "cm", "--tur", "skill"], env=ortam, kos=lambda a, timeout=None: (0, b"", b"")) == 0
    assert cagri == [("cm", None, "skill")]


# B4 eki (Ömer kararı, 5 Eki): exa'da sessiz boş YASAK + sağlayıcı zinciri exa → brave (BRAVE_API_KEY) → erisilemedi
LIMIT = "You've hit Exa's free MCP rate limit. Please try again later or add your own API key."
BRAVE = {"web": {"results": [{"title": "<strong>Brave</strong> &amp; inceleme", "url": "https://b.x/1", "page_age": "2026-08-01T00:00:00",
                              "description": "Kısa <strong>açıklama</strong>", "extra_snippets": ["ek bir", "y" * 700]}]}}


def tek(cevap):  # her mcporter sorgusu aynı yanıtı alır
    def kos(args):
        return cevap if args[0] == "mcporter" else (0, b"[]", b"")
    return kos


@pytest.fixture
def brave(monkeypatch, saat):
    monkeypatch.setenv("BRAVE_API_KEY", "test-anahtar")
    monkeypatch.setattr(gt, "_bson", [float("-inf")])

    def ac(req, timeout=None):
        ac.istek.append((req.full_url, req.get_header("X-subscription-token"), saat[0]))
        if ac.hata:
            raise urllib.error.HTTPError(req.full_url, 429, "Too Many Requests", {}, None)
        return io.BytesIO(json.dumps(BRAVE).encode())
    ac.istek, ac.hata = [], False
    monkeypatch.setattr(gt.urllib.request, "urlopen", ac)
    return ac


def web(tmp_path, kos):
    kj = tmp_path / "kapsam.json"
    kj.write_text(json.dumps({"izleme": "tam", "incelenmedi": []}), encoding="utf-8")
    b = tr.bolum(gt.on(tmp_path, "VID", "arac", kos=kos, kapsam=kj, web=True).read_text(encoding="utf-8"), "Web araması")
    return b, json.loads(kj.read_text(encoding="utf-8")).get("erisilemedi", [])


@pytest.mark.parametrize("o", [LIMIT, json.dumps({"content": [{"type": "text", "text": LIMIT}]})])
def test_exa_sessiz_bos_yasak_metin_hata(tmp_path, saat, o):
    b, e = web(tmp_path, tek((0, o.encode(), b"")))
    q = gt.SORGU[0].format(ad="arac")
    assert e[0] == [f"web: {q}", f"{LIMIT} · brave: BRAVE_API_KEY yok"] and len(e) == gt.WEB["sorgu"]
    assert f"- erişilemedi: web: {q} ({LIMIT} · brave: BRAVE_API_KEY yok)" in b


@pytest.mark.parametrize("o", [b"", b"[]", b'{"results": []}', b'{"content": []}'])
def test_exa_gercekten_bos_hata_degil(tmp_path, brave, o):
    b, e = web(tmp_path, tek((0, o, b"")))
    assert e == [] and "erişilemedi" not in b and brave.istek == []  # boş sonuç hata değil, brave'e gidilmez


def test_exa_satiri_saglayici(tmp_path, saat):
    b, _ = web(tmp_path, kos_yap(saat))
    assert "- arac review · exa · İnceleme · https://blog.x/r" in b


def test_exa_hata_brave_yedek(tmp_path, brave):
    b, e = web(tmp_path, tek((1, b"", b"mcporter: timeout")))
    s = b.splitlines()
    i = next(n for n, x in enumerate(s) if "https://b.x/1" in x)
    assert s[i] == "- arac review · brave · Brave & inceleme · 2026-08-01 · https://b.x/1" and b.count("https://b.x/1") == 1
    assert s[i + 1] == "  > " + ("Kısa açıklama ek bir " + "y" * 700)[:gt.WEB["ozet"]]  # açıklama + ek parçacıklar, 600 kuralı
    assert e == [] and len(brave.istek) == gt.WEB["sorgu"]
    u, anahtar, _ = brave.istek[0]
    assert u.startswith("https://api.search.brave.com/res/v1/web/search?") and "q=arac+review" in u and anahtar == "test-anahtar"
    assert f"count={gt.WEB['sonuc'] + gt.WEB['fazla']}" in u and "extra_snippets=true" in u and "text_decorations=false" in u
    z = [t for *_, t in brave.istek]
    assert gt.WEB["brave_aralik"] >= 1 and all(y - x >= gt.WEB["brave_aralik"] for x, y in zip(z, z[1:]))


def test_brave_hata_erisilemedi(tmp_path, brave):
    brave.hata = True
    _, e = web(tmp_path, tek((0, LIMIT.encode(), b"")))
    assert e[0] == [f"web: {gt.SORGU[0].format(ad='arac')}", f"{LIMIT} · brave: HTTP Error 429: Too Many Requests"]
