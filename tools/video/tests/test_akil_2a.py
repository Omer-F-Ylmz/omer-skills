"""VİDEO-AKIL-1b-2a: rapor formu (urller · is_akisi · promptlar · link sınıfı) + altın puanı + talimat önek önbelleği + bekçi. Canlı çağrı 0."""
import json
import re
from pathlib import Path

from test_f3_v5 import E1, ENV, P
from video import akil, bekci as bk
from video import altin as au
from video import parti as pt
from video import yonlendir as yon

ALTIN_DIZ = Path(__file__).resolve().parents[3] / "docs" / "video-tarama" / "altin"


def _rapor(**bol):
    return "# b\n## Özet\nmetin\n" + "".join(f"## {k}\n{v}\n" for k, v in bol.items())


# --- puan: urller / is_akisi / promptlar (1 eşleşen + 1 eşleşmeyen) ---
def test_urller_puan():
    a = {"urller": [{"url": "https://mcp.topview.ai/claude", "zaman": "3:01", "kaynak": "ekran"},
                    {"url": "https://pear.no/", "zaman": "4:00", "kaynak": "ekran"},
                    {"url": "https://mcp.example.com/mcp", "zaman": "5:00", "kaynak": "ekran"}]}
    r = _rapor(**{"URL'ler": "| url | zaman | kaynak | aday |\n|---|---|---|---|\n| https://www.mcp.topview.ai/claude/ | 3:02 | ekran | evet |"})
    p = au.puan(r, a)
    assert p["urller"] == (1, 3) and p["urller_iy"] == (1, 2)  # example.* DEĞERSİZ → iy paydası 2


def test_is_akisi_puan():
    a = {"is_akisi": [{"adim": "Blender sahnesini kur", "zaman": "1:00", "araclar": []}, {"adim": "Vercel üzerinde yayınla", "zaman": "2:00", "araclar": []}]}
    r = _rapor(**{"İş akışı": "- 1. adım — Blender sahnesini hazırla — araçlar: Blender"})
    assert au.puan(r, a)["is_akisi"] == (1, 2)


def test_promptlar_puan_yalniz_promptlar_bolumu():
    a = {"promptlar": [{"zaman": "1:00", "konu": "x", "kaynak": "ekran", "ozet": "evi çevreleyen kamera hareketi"},
                       {"zaman": "2:00", "konu": "y", "kaynak": "ekran", "ozet": "gece havuz aydınlatması"}]}
    r = _rapor(Promptlar="- kamera — evi çevreleyen kamera hareketi tarif edilir")
    assert au.puan(r, a)["promptlar"] == (1, 2)
    dis = _rapor(Promptlar="- yok").replace("metin", "evi çevreleyen kamera hareketi")  # başka bölümde geçen sayılmaz
    assert au.puan(dis, a)["promptlar"] == (0, 2)


def test_alan_yok_bos():
    assert au.ALAN_YOK == () and au.puan(_rapor(), {})["alan_yok"] == []


# --- link sınıfı (madde 2) ---
def test_sinif_affiliate_sponsor_sayilmaz():
    s = "- https://x.io/?via=ab — site · aday: hayır · neden · sınıf: affiliate · sponsor değil"
    assert au._rapor_linkler(f"## Açıklama bağlantıları\n{s}\n")["x.io"]["sponsor"] is False
    assert au._rapor_linkler("## Açıklama bağlantıları\n" + s.replace("affiliate · sponsor değil", "sponsor") + "\n")["x.io"]["sponsor"] is True


def _f(link):
    return {"ozet": "o", "bolumler": [], "adaylar": [], "aciklama_baglantilari": [link], "site_ui": [], "promptlar": [], "iddialar": [],
            "kareden_okunanlar": [], "belirsizlikler": [], "urller": [], "is_akisi": []}


PK = {"id": "v", "baslik": "B", "kanal": "K", "sure": 60, "dil": "tr", "metin": "## Segmentler\n[0:00] a\n", "kareler": []}


def _md(url="https://www.topview.ai/?via=dlws", ne="TopView", **k):
    return pt.rapor_md(_f({"url": url, "ne": ne, "aday_mi": True, "neden": "n", "aday_adi": "TopView", **k}), PK, [])


def test_rapor_md_sinif():
    assert "sınıf: sponsor" in _md(sinif="sponsor")  # ?via= + açık sponsor beyanı → sponsor; affiliate ezmez
    assert "sınıf: affiliate" in _md(sinif="diğer")
    assert "sınıf: affiliate" in _md(url="https://x.io/", ne="Promo code ABC ile indirim")
    assert "sınıf: diğer" in _md(url="https://y.io/", ne="site")


def test_rapor_md_yeni_bolumler():
    f = _f({"url": "https://y.io/", "ne": "s", "aday_mi": False, "neden": "n", "aday_adi": None, "sinif": "diğer"})
    f["urller"] = [{"url": "https://mcp.topview.ai/mcp", "zaman": "2:45", "kaynak": "ekran", "aday": True}]
    f["is_akisi"] = [{"adim": "Sahneyi kur", "araclar": ["Blender", "Codex"]}, {"adim": "Render al", "araclar": []}]
    f["promptlar"] = [{"metin": "evi çevir", "amac": "kamera", "kanit_zamani": "1:00", "kaynak": "ekran"}]
    md = pt.rapor_md(f, PK, [])
    assert "## URL'ler\n| url | zaman | kaynak | aday |\n|---|---|---|---|\n| https://mcp.topview.ai/mcp | 2:45 | ekran | evet |" in md
    assert "## İş akışı\n- 1. adım — Sahneyi kur — araçlar: Blender, Codex\n- 2. adım — Render al — araçlar: yok" in md
    assert "## Promptlar\n- kamera — evi çevir" in md
    bos = pt.rapor_md({**f, "urller": [], "is_akisi": [], "promptlar": []}, PK, [])
    assert "## URL'ler\n- yok" in bos and "## İş akışı\n- yok" in bos and "## Promptlar\n- yok" in bos
    eski = {k: v for k, v in f.items() if k not in ("urller", "is_akisi")}
    assert "## URL'ler\n- yok" in pt.rapor_md(eski, PK, [])  # eski form kırılmaz


def test_sema_yeni_alanlar_opsiyonel():
    s = pt.sema(["v"])["properties"]["videolar"]["items"]
    assert "urller" in s["properties"] and "urller" not in s["required"] and "is_akisi" not in s["required"]
    assert s["properties"]["aciklama_baglantilari"]["items"]["properties"]["sinif"]["enum"] == ["sponsor", "affiliate", "diğer"]
    assert "urller" in pt.LISTE and "is_akisi" in pt.LISTE


# --- talimat (madde 3) ---
def _altin_adlar():
    out = set()
    for p in ALTIN_DIZ.glob("*.json"):
        for a in json.loads(p.read_text(encoding="utf-8")).get("adaylar", []):
            for x in (a["ad"], *a.get("alias", [])):
                out.add(au.norm(x))
    muaf = {au.norm(x) for x in akil.CEKIRDEK} | {"claude"}
    return {x for x in out if len(x) >= 5 and x not in muaf}


def test_talimatta_altin_adi_yok():
    kel = [au.norm(w) for w in re.findall(r"\w+", " ".join([pt.SISTEM, yon.EKSIKSIZLIK10, yon.ALAN_KURALI, yon.SON_SISTEM10]).casefold())]
    pencere = {"".join(kel[i:i + k]) for k in range(1, 6) for i in range(len(kel))}  # kelime sınırı: "segment" adı "segmentleri" içinde sayılmaz
    assert [x for x in _altin_adlar() if x in pencere] == []
    o = json.loads(yon.ORNEK_V10.read_text(encoding="utf-8"))
    assert o["id"] not in {p.stem for p in ALTIN_DIZ.glob("*.json")}


def test_onek_onbellegi_iki_paket_ayni_onek():
    def kos(paket):
        c = []

        def tas(sis, msg, sema, **k):
            c.append((sis, msg))
            return {"form": None, "usage": {}, "usd": 0.0, "hata": "x"}
        yon.tara_v10(("S", paket, pt.sema(["vid1"]), []), ENV, E1, tas=tas, ek={})
        return c
    a, b = kos(P), kos(P.replace("Alfa", "Zeta").replace("Beta", "Teta"))
    assert a and b and {x[0] for x in a + b} == {a[0][0]}  # sistem metni bayt bayt aynı
    assert {x[1].split(yon.DEGERLENDIR)[0] for x in a + b} == {a[0][1].split(yon.DEGERLENDIR)[0]}  # DEĞERLENDİR'e kadar aynı


# --- bekçi (madde 4) ---
PAKET = """# v · Başlık
## Açıklama bağlantıları
https://www.topview.ai/?via=x https://youtu.be/abc
## Segmentler
[0:10] Burada MCP ve three.js kullanıyoruz, claude-code açık. Sonra npm i gsap yazıyoruz.
[0:20] Space Grotesk fontu ve GitHub hesabı, Burada biz.
## Ekran metni (OCR)
[0:30] https://mcp.topview.ai/mcp
## Kareler
kare_01.jpg · ZZZ
"""


def test_terimler_kume():
    assert bk.terimler(PAKET) == {"three.js", "claude-code", "gsap", "Space Grotesk", "GitHub", "topview.ai", "mcp.topview.ai"}


RAPOR = ("# b\n## Adaylar\n| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |\n|---|---|---|---|---|---|---|\n"
         "| Three.js | yok | CLI | yok | n | 0:10 | k |\n\n## Açıklama bağlantıları\n- yok\n")


def test_kalan_aday_dusurur_ve_tavan():
    assert bk.kalan(RAPOR, {"three.js", "gsap"}) == ["gsap"]
    assert len(bk.kalan(RAPOR, {f"terim{i}x" for i in range(70)})) == 60


def test_bekci_tek_cagri_ve_bos_cagri_yok():
    c = []

    def tas(sis, msg, sema, **k):
        c.append(msg)
        return {"form": {"kararlar": [{"terim": "gsap", "aday": True, "tur": "CLI", "neden": "animasyon kütüphanesi", "kanit": "npm i gsap yazıyoruz"},
                                     {"terim": "GitHub", "aday": False, "tur": "CLI", "neden": "genel", "kanit": ""}]}, "usage": {"input_tokens": 5}, "usd": 0.001}
    md, ozet = bk.bekci(RAPOR, PAKET, tas)
    assert len(c) == 1 and ozet["cagri"] == 1 and ozet["eklenen"] == ["gsap"]
    assert re.search(r"^\| gsap \| yok \| CLI \| yok \| .* \| kaynak: bekçi \|$", md, re.M) and "## Açıklama bağlantıları" in md
    md2, o2 = bk.bekci(RAPOR, "# v\nhiçbir şey yok\n", tas)
    assert o2["cagri"] == 0 and o2["eklenen"] == [] and md2 == RAPOR and len(c) == 1


def test_terimler_kisa_buyuk_harf_ve_genel_terim_dusurur():
    assert bk.terimler("[0:10] HTML CSS API GPU FAQ ASAP kullandık, ANTHROPIC ve three.js var.\n") == {"ANTHROPIC", "three.js"}
    assert bk.kalan("# b\n## Adaylar\n", {"html", "Json", "UI", "gsap"}) == ["gsap"]


def test_bekci_kanit_paketten_birebir_yoksa_reddeder():
    def tas(kanit):
        return lambda *a, **k: {"form": {"kararlar": [{"terim": "gsap", "aday": True, "tur": "CLI", "neden": "n", "kanit": kanit}]}}
    assert bk.bekci(RAPOR, PAKET, tas("npm i gsap yazıyoruz"))[1]["eklenen"] == ["gsap"]
    assert bk.bekci(RAPOR, PAKET, tas("NPM  i   GSAP yazıyoruz"))[1]["eklenen"] == ["gsap"]  # boşluk/büyük-küçük harf esnek
    assert bk.bekci(RAPOR, PAKET, tas("gsap yazıyoruz"))[1]["eklenen"] == []  # < 3 kelime
    assert bk.bekci(RAPOR, PAKET, tas("gsap ile animasyon yapıyoruz"))[1]["eklenen"] == []  # pakette yok
    assert "kanit" in bk.SEMA["properties"]["kararlar"]["items"]["required"]
