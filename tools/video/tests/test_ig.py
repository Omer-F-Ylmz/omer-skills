"""VİDEO-PLATFORM-1: Instagram kimlik · embed ayrıştırma · engel/bekleme · çerez · sızıntı · paket (ağ yok, OCR/ASR taklit)."""
import json
import os
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from video import cli
from video import instagram as ig
from video import metin as m
from video import parti as pt
from video.cli import main

FIX = Path(__file__).parent / "fixture" / "ig"
REEL, CAR = (FIX / "DdUf3qJOvTO.html").read_text(encoding="utf-8"), (FIX / "DeL7DvgFLRM.html").read_text(encoding="utf-8")
GERCEK_AL = ig._al  # autouse sahteden önce


@pytest.fixture(autouse=True)
def _ocr_yalitimi(tmp_path, monkeypatch):
    """test_goz_r ile aynı sınıf: ortak %TEMP%/video-ocr kilidi + gerçek boş RAM canlı koşucularda testi bekletip düşürüyordu."""
    monkeypatch.setattr(cli, "OCR_KILIT", tmp_path / "ocr-kilit")
    monkeypatch.setattr(cli, "bos_ram", lambda: 1e6)
IMZALI = "https://instagram.fist1-1.fna.fbcdn.net/v/t50/x.mp4?oh=00_SIR&oe=6A1B2C3D&_nc_ht=x"


def sayfa(sm):
    ic = json.dumps({"context": {}, "gql_data": {"shortcode_media": sm}}).replace("/", "\\/")
    return '<script>{"require":[[{"contextJSON":%s}]]}</script>' % json.dumps(ic)


def sm_of(html):
    i = html.index('"contextJSON":') + 14
    return json.loads(json.JSONDecoder().raw_decode(html, i)[0])["gql_data"]["shortcode_media"]


@pytest.fixture(autouse=True)
def igsiz(monkeypatch):
    istek, uyku = [], []
    monkeypatch.setattr(ig, "_SON", [None])
    monkeypatch.setattr(ig, "_ENGEL", [0])
    monkeypatch.setattr(ig, "uyku", uyku.append)
    monkeypatch.setattr(ig, "saat", lambda: 1000.0)
    monkeypatch.setattr(ig, "_al", lambda u: (_ for _ in ()).throw(AssertionError("test: ağ yok")))
    return istek, uyku


def _sahte_al(monkeypatch, *yanit):
    cagri = []

    def al(u):
        cagri.append(u)
        return yanit[min(len(cagri), len(yanit)) - 1]
    monkeypatch.setattr(ig, "_al", al)
    return cagri


# --- kimlik
@pytest.mark.parametrize("u", ["https://www.instagram.com/reel/DdUf3qJOvTO/?igsh=MWx0b2x5", "https://instagram.com/reels/DdUf3qJOvTO/",
                               "https://www.instagram.com/p/DdUf3qJOvTO/", "https://www.instagram.com/tv/DdUf3qJOvTO", "ig-DdUf3qJOvTO"])
def test_kimlik_ig(u):
    assert m.vid(u) == "ig-DdUf3qJOvTO"


def test_kimlik_youtube_degismez():
    assert m.vid("dQw4w9WgXcQ") == "dQw4w9WgXcQ" and m.vid("https://youtu.be/dQw4w9WgXcQ?t=3") == "dQw4w9WgXcQ"
    assert m.vid("https://www.youtube.com/watch?v=-_S3KD0ZIfI") == "-_S3KD0ZIfI"


def test_ig_kimligi_asla_youtube_degil():
    assert m.ID.search("ig-DdUf3qJOvTO") is None and m.ID.search("x ig-DdUf3qJOvTO y") is None
    assert m.vid("ig-DdUf3qJOvTO") != "DdUf3qJOvTO" and m.vid("DdUf3qJOvTO") == "DdUf3qJOvTO"  # öneksiz 11 karakter YouTube kalır
    assert cli.yt_url("ig-DdUf3qJOvTO") == "https://www.instagram.com/p/DdUf3qJOvTO/" and "youtube" in cli.yt_url("DdUf3qJOvTO")


# --- ayrıştırma
def test_reel_ayristir():
    p = ig.ayristir(REEL)
    assert p["tur"] == "reel" and p["hesap"] == "mahemas.ai" and p["sure"] == pytest.approx(68.079) and p["aciklama"]
    assert len(p["ogeler"]) == 1 and p["ogeler"][0]["video"].endswith("?REDACTED") and "\\/" not in p["ogeler"][0]["video"]


def test_carousel_sirali():
    sm = sm_of(CAR)
    p = ig.ayristir(CAR)
    beklenen = [e["node"]["display_url"] for e in sm["edge_sidecar_to_children"]["edges"]]
    assert p["tur"] == "post" and p["hesap"] == "onurhuseyinkocak.ai" and p["aciklama"] and p["sure"] is None
    assert len(p["ogeler"]) == 6 and [o["gorsel"] for o in p["ogeler"]] == beklenen and all(o["video"] is None for o in p["ogeler"])


def test_karisik_sidecar():
    sm = sm_of(CAR)
    sm["edge_sidecar_to_children"]["edges"][1]["node"].update(is_video=True, video_url="https://v.example/b.mp4")
    p = ig.ayristir(sayfa(sm))
    assert [o["video"] for o in p["ogeler"]][:3] == [None, "https://v.example/b.mp4", None] and all(o["gorsel"] for o in p["ogeler"])


def test_video_url_yok():
    sm = sm_of(REEL)
    del sm["video_url"]
    p = ig.ayristir(sayfa(sm))
    assert p["tur"] == "reel" and p["ogeler"][0]["video"] is None


def test_embed_verisi_yok():
    with pytest.raises(ig.IgHata, match="embed verisi yok"):
        ig.ayristir('<html>"pageID":"httpErrorPage"</html>')


# --- engel / bekleme
def test_429_bekle_bir_tekrar(monkeypatch, igsiz):
    cagri = _sahte_al(monkeypatch, (429, "u", ""), (200, "u", REEL))
    assert ig.sayfa("DdUf3qJOvTO") == ig.ayristir(REEL) and len(cagri) == 2 and igsiz[1] == [120]


def test_engel_not(monkeypatch, igsiz):
    cagri = _sahte_al(monkeypatch, (200, "https://www.instagram.com/accounts/login/?next=x", ""))
    with pytest.raises(ig.IgHata, match="ig: engellendi"):
        ig.sayfa("DdUf3qJOvTO")
    assert len(cagri) == 2 and igsiz[1] == [120]


def test_art_arda_3_engel_parti_durur(monkeypatch, igsiz):
    cagri = _sahte_al(monkeypatch, (429, "u", ""))
    for _ in range(3):
        with pytest.raises(ig.IgHata, match="engellendi"):
            ig.sayfa("DdUf3qJOvTO")
    with pytest.raises(ig.IgHata, match="durdu"):
        ig.sayfa("DeL7DvgFLRM")
    assert len(cagri) == 6


def test_basari_engel_sayacini_sifirlar(monkeypatch):
    _sahte_al(monkeypatch, (429, "u", ""), (429, "u", ""), (200, "u", REEL))
    with pytest.raises(ig.IgHata):
        ig.sayfa("a")
    assert ig.sayfa("a") == ig.ayristir(REEL) and ig._ENGEL[0] == 0


def test_istekler_arasi_10_20_sn(monkeypatch, igsiz):
    _sahte_al(monkeypatch, (200, "u", REEL))
    ig.sayfa("a")
    ig.sayfa("b")
    assert len(igsiz[1]) == 1 and 10 <= igsiz[1][0] <= 20


HATA_SAYFASI = '<html>"pageID":"httpErrorPage"</html>'


def test_sessiz_engel_sayilir_3te_durur(monkeypatch):  # DEVAM-3 c: 200 dönen hata sayfası = sessiz engel
    cagri = _sahte_al(monkeypatch, (200, "u", HATA_SAYFASI))
    for _ in range(3):
        with pytest.raises(ig.IgHata, match="embed verisi yok"):
            ig.sayfa("a")
    with pytest.raises(ig.IgHata, match="durdu"):
        ig.sayfa("b")
    assert len(cagri) == 3


def test_sessiz_engel_basari_sifirlar(monkeypatch):
    _sahte_al(monkeypatch, (200, "u", HATA_SAYFASI), (200, "u", HATA_SAYFASI), (200, "u", REEL))
    for _ in range(2):
        with pytest.raises(ig.IgHata):
            ig.sayfa("a")
    assert ig._ENGEL[0] == 2 and ig.sayfa("a") == ig.ayristir(REEL) and ig._ENGEL[0] == 0


@pytest.mark.parametrize("hata", [urllib.error.URLError("dns"), TimeoutError("timed out"), ConnectionResetError("reset")])
def test_al_ag_hatasi_ighata(monkeypatch, hata):  # DEVAM-3 b
    def urlopen(req, timeout=None):
        raise hata
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(ig, "_al", GERCEK_AL)
    with pytest.raises(ig.IgHata, match="ig: ağ"):
        ig._al("https://www.instagram.com/p/a/embed/captioned/")


# --- çerez
class _Yanit:
    status, headers = 200, {"Set-Cookie": "sessionid=SAHTE; csrftoken=SAHTE"}

    def __init__(self, url):
        self.url = url

    def geturl(self):
        return self.url

    def read(self):
        return REEL.encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_cerez_basligi_yok(monkeypatch, tmp_path):
    giden = []

    def urlopen(req, timeout=None):
        giden.append(req)
        return _Yanit(req.full_url)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    monkeypatch.setattr(ig, "_al", GERCEK_AL)
    ig._al("https://www.instagram.com/p/a/embed/captioned/")
    ig._al("https://www.instagram.com/p/b/embed/captioned/")  # sahte oturum çerezi döndü; ikinci istek taşımamalı
    ig._indir(IMZALI, tmp_path / "x.mp4")
    assert len(giden) == 3 and all(not any(k.lower() == "cookie" for k, _ in r.header_items()) for r in giden)
    assert all(r.get_header("Sec-fetch-mode") == "navigate" for r in giden[:2])
    assert "--cookies" not in Path(cli.__file__).read_text(encoding="utf-8")


# --- sızıntı + paket
def _ortam(tmp_path):
    return {**os.environ, "VIDEO_CACHE": str(tmp_path / "c"), "VIDEO_TARAMA_DIZIN": str(tmp_path / "t"), "CAGRI_SAYAC_DIZIN": str(tmp_path / "s")}


def _kos(a, timeout=None):
    raise AssertionError(f"test: dış komut yok {a[:2]}")


def _al(u):
    raise urllib.error.URLError("test: ağ yok")


class _Ocr:
    def __init__(self):
        self.yollar = []

    def __call__(self):  # yükleyici → motor
        return self

    def motor(self, y):
        self.yollar.append(Path(y).name)
        return [(f"Bu gorselde {Path(y).stem} kurulum adimi anlatiliyor", 0.99, 10)]


def _paketle(monkeypatch, tmp_path, html, hedef, capsys):
    cagri = {"asr": 0, "goz": 0}
    _sahte_al(monkeypatch, *[(200, "u", h) for h in (html if isinstance(html, tuple) else (html,))])
    monkeypatch.setattr(ig, "_indir", lambda u, yol: yol.write_bytes(b"\xff\xd8sahte"))

    def asr(ctx, d, sure, dil, prompt):
        cagri["asr"] += 1
        return [(0.0, "merhaba bu bir reel konuşması")], "groq"

    def goz(*a, **k):
        cagri["goz"] += 1
        return []
    monkeypatch.setattr(cli, "_asr", asr)
    monkeypatch.setattr(cli, "_goz", goz)
    o = _Ocr()
    monkeypatch.setattr(cli, "_MOTOR", [None])
    env = _ortam(tmp_path)
    kw = dict(env=env, kos=_kos, uyku=lambda s: None, al=_al, ocr=lambda: o.motor)
    assert main(["ozet", "--", hedef], **kw) == 0
    vid = m.vid(hedef)
    assert main(["paket", "--kare", "1", "--istek-tavan", "0", "--", vid], **kw) == 0
    d = Path(env["VIDEO_CACHE"]) / vid
    return cagri, o, d, (d / "paket.md").read_text(encoding="utf-8"), capsys.readouterr()


def test_paket_reel_asr(monkeypatch, tmp_path, capsys):
    cagri, o, d, md, _ = _paketle(monkeypatch, tmp_path, REEL, "https://www.instagram.com/reel/DdUf3qJOvTO/?igsh=abc", capsys)
    kunye = md.splitlines()[0]
    assert d.name == "ig-DdUf3qJOvTO" and cagri == {"asr": 1, "goz": 1} and o.yollar == []
    assert "· https://www.instagram.com/reel/DdUf3qJOvTO/ ·" in kunye and "youtu.be" not in kunye
    assert "platform: instagram · tür: reel · yorum: girişsiz alınamıyor" in kunye and "mahemas.ai" in kunye
    assert "## Açıklama" in md and "merhaba bu bir reel" in md
    pk = pt.paket_oku(d / "paket.md")
    assert pk["id"] == "ig-DdUf3qJOvTO" and pk["url"] == "https://www.instagram.com/reel/DdUf3qJOvTO/" and pk["kareler"] == []


def test_paket_post_ocr_sirali(monkeypatch, tmp_path, capsys):
    cagri, o, d, md, _ = _paketle(monkeypatch, tmp_path, CAR, "https://www.instagram.com/p/DeL7DvgFLRM/", capsys)
    assert cagri == {"asr": 0, "goz": 0} and o.yollar == [f"gorsel-{i}.jpg" for i in range(1, 7)]
    assert "tür: görsel gönderi" in md.splitlines()[0] and "https://www.instagram.com/p/DeL7DvgFLRM/" in md.splitlines()[0]
    yer = [md.index(f"### görsel {i}\n") for i in range(1, 7)]
    assert yer == sorted(yer) and "gorsel-3 kurulum" in md
    assert [Path(k).name for k in pt.paket_oku(d / "paket.md")["kareler"]] == [f"gorsel-{i}.jpg" for i in range(1, 7)]  # DEVAM-3 d: AKIL'a da


def test_paket_post_kareler_8_tavan(monkeypatch, tmp_path, capsys):
    sm = sm_of(CAR)
    sm["edge_sidecar_to_children"]["edges"] *= 2  # 12 görsel
    _, o, d, md, _ = _paketle(monkeypatch, tmp_path, sayfa(sm), "ig-DeL7DvgFLRM", capsys)
    assert len(o.yollar) == 12 and [Path(k).name for k in pt.paket_oku(d / "paket.md")["kareler"]] == [f"gorsel-{i}.jpg" for i in range(1, 9)]


def test_reel_video_yok_goz_notu(monkeypatch, tmp_path, capsys):
    sm = sm_of(REEL)
    del sm["video_url"]
    cagri, _, _, md, _ = _paketle(monkeypatch, tmp_path, sayfa(sm), "ig-DdUf3qJOvTO", capsys)
    assert cagri == {"asr": 0, "goz": 0} and "göz: yok (embed video vermedi)" in md.splitlines()[0] and "## Açıklama" in md


def test_imzali_adres_sizmaz(monkeypatch, tmp_path, capsys):
    sm = sm_of(CAR)
    for e in sm["edge_sidecar_to_children"]["edges"]:
        e["node"]["display_url"] = IMZALI
    sm["display_url"] = IMZALI
    _, _, d, md, cik = _paketle(monkeypatch, tmp_path, sayfa(sm), "ig-DeL7DvgFLRM", capsys)
    metin = md + cik.out + cik.err + "".join(p.read_text(encoding="utf-8", errors="replace") for p in d.rglob("*") if p.suffix in (".json", ".md", ".txt"))
    assert "oe=" not in metin and "oh=" not in metin


def test_indirme_hatasi_adresi_gizler(monkeypatch, tmp_path):
    def urlopen(req, timeout=None):
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", {}, None)
    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    with pytest.raises(ig.IgHata) as e:
        ig._indir(IMZALI, tmp_path / "x.mp4")
    assert "imzalı adres gizlendi" in str(e.value) and "fbcdn.net" in str(e.value) and "oe=" not in str(e.value) and "oh=" not in str(e.value)


# --- YouTube künye/rapor eşdeğerliği
class _F(dict):
    def __missing__(self, k):
        return []


def test_youtube_rapor_bayt_esdeger():
    yol = Path(r"C:\Projeler\.video-cache\d_UE-wHLoZY\paket.md")
    if not yol.is_file():
        pytest.skip("altın paket önbellekte yok")
    pk = pt.paket_oku(yol)
    assert pk["url"] == "https://youtu.be/d_UE-wHLoZY"
    f = _F(ozet="ö", bolumler=[], iz=None)
    assert pt.rapor_md(f, pk, []) == pt.rapor_md(f, {**pk, "url": None}, [])  # url'siz = eski biçim (sabit youtu.be)


def test_youtube_kunye_akis_url_sizmaz(tmp_path):  # DEVAM-3 a: yt-dlp üst düzey 'url' imzalı akış adresi
    d = tmp_path / "c" / "dQw4w9WgXcQ"
    d.mkdir(parents=True)
    (d / "meta.json").write_text(json.dumps({"id": "dQw4w9WgXcQ", "title": "t", "channel": "k", "duration": 0, "chapters": [], "description": "",
                                             "url": "https://rr1---sn-x.googlevideo.com/videoplayback?sig=SAHTE"}), encoding="utf-8")
    (d / "segmentler.jsonl").write_text(json.dumps({"bas": 0, "son": 5, "metin": "merhaba bu bir deneme konuşması"}) + "\n", encoding="utf-8")
    (d / "yorumlar.json").write_text(json.dumps({"durum": "✓", "ham": []}), encoding="utf-8")
    assert main(["paket", "--kare", "0", "--istek-tavan", "0", "--", "dQw4w9WgXcQ"], env=_ortam(tmp_path), kos=_kos, uyku=lambda s: None, al=_al) == 0
    kunye = (d / "paket.md").read_text(encoding="utf-8").splitlines()[0]
    assert "· https://youtu.be/dQw4w9WgXcQ ·" in kunye and "googlevideo" not in kunye


# --- kuyruk / parti (taklitli: ağ, yt-dlp, model yok)
def _parti_kur(monkeypatch, tmp_path, html, url):
    from test_m2a import Sahte, _ctx
    cagri = {"asr": 0, "goz": 0, "alt": []}
    _sahte_al(monkeypatch, (200, "u", html))
    monkeypatch.setattr(ig, "_indir", lambda u, yol: yol.write_bytes(b"\xff\xd8sahte"))
    monkeypatch.setattr(cli, "_asr", lambda *a: cagri.update(asr=cagri["asr"] + 1) or ([(0.0, "merhaba bu bir reel konuşması aracı anlatıyor")], "groq"))
    monkeypatch.setattr(cli, "_goz", lambda *a, **k: cagri.update(goz=cagri["goz"] + 1) or [])
    monkeypatch.setattr(cli, "_MOTOR", [None])
    o, env = _Ocr(), _ortam(tmp_path)
    (tmp_path / "kuyruk.md").write_text(f"### Sıra 1\n| id | dk | başlık | not | durum |\n|---|---|---|---|---|\n| {url} | 1.1 | t | - | bekliyor |\n", encoding="utf-8")
    ctx = {**_ctx(tmp_path, Sahte()), "kok": Path(env["VIDEO_CACHE"]),
           "alt": lambda a: cagri["alt"].append(a) or (main(a, env=env, kos=_kos, uyku=lambda s: None, al=_al, ocr=lambda: o.motor) if a[0] in ("ozet", "paket") else 0)}
    return cagri, o, ctx


@pytest.mark.parametrize("url,vid,asr,goz,ocr", [("https://www.instagram.com/reel/DdUf3qJOvTO/?igsh=abc", "ig-DdUf3qJOvTO", 1, 1, 0),
                                                 ("https://www.instagram.com/p/DeL7DvgFLRM/", "ig-DeL7DvgFLRM", 0, 0, 6)])
def test_parti_kuyruk_ig(monkeypatch, tmp_path, url, vid, asr, goz, ocr):
    from test_m2a import _ns, _pid
    cagri, o, ctx = _parti_kur(monkeypatch, tmp_path, REEL if "reel" in url else CAR, url)
    assert pt.parti(_ns("baslat", tmp_path / "kuyruk.md"), ctx) == 0
    assert {a[0] for a in cagri["alt"]} >= {"ozet", "paket"} and all(a[-1] == vid for a in cagri["alt"] if a[0] in ("ozet", "paket"))
    assert (cagri["asr"], cagri["goz"], len(o.yollar)) == (asr, goz, ocr)
    d = json.loads((tmp_path / ".kos" / _pid(tmp_path) / "durum.json").read_text(encoding="utf-8"))
    assert d["videolar"][vid]["paket"]["durum"] == "tamam" and d["videolar"][vid]["tarama"]["durum"] == "tamam"
    rapor = Path(d["videolar"][vid]["tarama"]["cikti"]).read_text(encoding="utf-8")
    assert f"https://www.instagram.com/{'reel' if asr else 'p'}/{vid[3:]}/" in rapor.split("## Özet")[0] and "youtu.be" not in rapor


def test_parti_link_ig(monkeypatch, tmp_path):
    from test_m2a import _ns
    cagri, _, ctx = _parti_kur(monkeypatch, tmp_path, REEL, "x")
    assert pt.parti(_ns("link", "https://www.instagram.com/reels/DdUf3qJOvTO/"), ctx) == 0
    assert cagri["alt"][0] == ["ozet", "--", "ig-DdUf3qJOvTO"]


# --- SMOKE-DÜZELT B1: köprü süreci User kapsamı anahtarları görmüyor → HKCU\Environment
class _Winreg:
    HKEY_CURRENT_USER = "HKCU"

    def __init__(self, deger):
        self.deger, self.sorulan = deger, []

    def OpenKey(self, kok, yol):
        assert (kok, yol) == ("HKCU", "Environment")
        import contextlib
        return contextlib.nullcontext(self)

    def QueryValueEx(self, k, ad):
        self.sorulan.append(ad)
        if ad not in self.deger:
            raise FileNotFoundError(ad)
        return self.deger[ad], 1


def test_kullanici_env_hkcu(monkeypatch, capsys):
    import sys
    sahte = _Winreg({"GROQ_API_KEY": "s1", "OPENROUTER_API_KEY": "s2"})
    monkeypatch.setitem(sys.modules, "winreg", sahte)
    monkeypatch.setattr(sys, "platform", "win32")
    env = {"OPENROUTER_API_KEY": "s3"}
    cli._kullanici_env(env)
    assert ("GROQ_API_KEY" in env, "GEMINI_API_KEY" in env, env["OPENROUTER_API_KEY"] == "s3") == (True, False, True)  # yalnız varlık; dolu olana dokunulmaz
    assert "OPENROUTER_API_KEY" not in sahte.sorulan
    assert capsys.readouterr() == ("", "")


def test_kullanici_env_windows_disi(monkeypatch):
    import sys
    monkeypatch.setattr(sys, "platform", "linux")
    env = {}
    cli._kullanici_env(env)
    assert env == {}


# --- SMOKE-DÜZELT B2: IG rapor künyesi platform/tür/yorum eki
def test_ig_rapor_kunye_eki():
    f = _F(ozet="ö", bolumler=[], iz=None)
    pk = {"id": "ig-DdUf3qJOvTO", "baslik": "b", "kanal": "k", "sure": 68, "dil": "?", "metin": ""}
    reel = pt.rapor_md(f, {**pk, "url": "https://www.instagram.com/reel/DdUf3qJOvTO/"}, []).splitlines()[2]
    post = pt.rapor_md(f, {**pk, "id": "ig-DeL7DvgFLRM", "url": "https://www.instagram.com/p/DeL7DvgFLRM/"}, []).splitlines()[2]
    assert reel.endswith("/reel/DdUf3qJOvTO/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor")
    assert post.endswith("/p/DeL7DvgFLRM/ · platform: instagram · tür: görsel gönderi · yorum: girişsiz alınamıyor")
    assert "platform:" not in pt.rapor_md(f, {**pk, "id": "abcdefghijk", "url": None}, []).splitlines()[2]
    # ONARIM-5: tür ve göz notu paket künyesinden (gömme kapalı reel: url /p/, tür kısıtlı gönderi)
    kis = pt.rapor_md(f, {**pk, "id": "ig-DcY-csFDG6f", "url": "https://www.instagram.com/p/DcY-csFDG6f/",
                          "metin": "# ig-DcY-csFDG6f · b · k · süre 0:00 · göz: yok (gömme kapalı; yalnız kapak + açıklama) · platform: instagram · tür: kısıtlı gönderi · yorum: girişsiz alınamıyor\n"}, []).splitlines()[2]
    assert kis.endswith("/p/DcY-csFDG6f/ · platform: instagram · tür: kısıtlı gönderi · göz: yok (gömme kapalı; yalnız kapak + açıklama) · yorum: girişsiz alınamıyor")


# --- ONARIM-5: gömme kapalı (contextJSON null) → ana sayfa og meta yedeği
KAPALI = '<script>{"require":[[{"contextJSON":null}]]}</script>'
ANA = (FIX / "DcY-csFDG6f-ana.html").read_text(encoding="utf-8")


def test_og_ayristir_onek_ayiklanir():
    p = ig.og_ayristir(ANA)
    assert p["tur"] == "kısıtlı" and p["hesap"] == "oguzhanxkaragoz" and p["sure"] is None
    assert p["aciklama"] == "Claude’u aşırı zeki yapan 176k Like’lı dosya 🤩"
    assert p["ogeler"] == [{"video": None, "gorsel": "https://scontent.cdninstagram.com/v/t51.82787-15/783616854_18620543956004211_7801888052023116321_n.jpg?REDACTED"}]


def test_gomme_kapali_ana_sayfa_yedegi(monkeypatch, tmp_path, capsys, igsiz):
    cagri, o, d, md, _ = _paketle(monkeypatch, tmp_path, (KAPALI, ANA), "ig-DcY-csFDG6f", capsys)
    kunye = md.splitlines()[0]
    assert "tür: kısıtlı gönderi" in kunye and "göz: yok (gömme kapalı; yalnız kapak + açıklama)" in kunye
    assert cagri == {"asr": 0, "goz": 0} and o.yollar == ["gorsel-1.jpg"] and "aşırı zeki" in md and "likes" not in md
    assert [Path(k).name for k in pt.paket_oku(d / "paket.md")["kareler"]] == ["gorsel-1.jpg"]
    assert len(igsiz[1]) == 1 and 10 <= igsiz[1][0] <= 20 and ig._ENGEL[0] == 0  # aynı istek aralığı; engel sayılmaz


def test_gomme_kapali_ana_sayfa_bos_engel_sayilir(monkeypatch):
    cagri = _sahte_al(monkeypatch, (200, "u", KAPALI), (200, "u", "<html></html>"))
    with pytest.raises(ig.IgHata, match="embed verisi yok"):
        ig.sayfa("DcY-csFDG6f")
    assert cagri == ["https://www.instagram.com/p/DcY-csFDG6f/embed/captioned/", "https://www.instagram.com/p/DcY-csFDG6f/"] and ig._ENGEL[0] == 1


# --- IG-KARUSEL-1: karuselin tüm slaytları (video slayt dahil) · slayt N/M künyesi · kısmi işareti
def _karisik():
    sm = sm_of(CAR)
    sm["edge_sidecar_to_children"]["edges"][1]["node"].update(is_video=True, video_url="https://v.example/b.mp4")
    return sayfa(sm)


def test_karisik_karusel_video_slayt_indirilir(monkeypatch, tmp_path):
    _sahte_al(monkeypatch, (200, "u", _karisik()))
    monkeypatch.setattr(ig, "_indir", lambda u, yol: yol.write_bytes(b"x"))
    d = tmp_path / "ig-DeL7DvgFLRM"
    d.mkdir()
    meta = ig.getir(d)
    assert meta["slayt_toplam"] == 6 and meta["slayt_video"] == ["slayt-2.mp4"] and (d / "slayt-2.mp4").is_file() and len(meta["gorseller"]) == 6


def test_paket_karisik_karusel_kunye_ve_video_kareleri(monkeypatch, tmp_path, capsys):
    def kos(ctx, a, timeout=None):
        assert a[0] == "ffmpeg" and a[-1].endswith("slayt-2-%d.jpg")
        for k in (1, 2):
            Path(a[-1] % k).write_bytes(b"\xff\xd8")
    monkeypatch.setattr(cli, "_kos", kos)
    _, o, d, md, _ = _paketle(monkeypatch, tmp_path, _karisik(), "https://www.instagram.com/p/DeL7DvgFLRM/", capsys)
    assert " · slayt 6/6 · yorum:" in md.splitlines()[0] and "karusel kısmi" not in md.splitlines()[0]
    assert "slayt-2-1.jpg" in o.yollar and "### slayt 2 (video) kare 2\n" in md and "ses işlenmedi" in md


def test_kisitli_karusel_kismi(monkeypatch, tmp_path, capsys):
    _, _, d, md, _ = _paketle(monkeypatch, tmp_path, (KAPALI, ANA), "ig-DcY-csFDG6f", capsys)
    assert " · slayt 1/? · karusel kısmi: 1/? · yorum:" in md.splitlines()[0]
