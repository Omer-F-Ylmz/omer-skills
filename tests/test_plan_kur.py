"""ENVANTER-3: plan_kur.py tek çağrı çıktısı + katalog_ara öğrenim grubu."""
import json
import os
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import katalog_ara as ka  # noqa: E402
import plan_kur as pk  # noqa: E402

ENV = dict(os.environ, PYTHONIOENCODING="utf-8")


def kos(*a):
    return subprocess.run([sys.executable, str(KOK / "tools" / "plan_kur.py"), *a], capture_output=True, text=True,
                          encoding="utf8", env=ENV).stdout


def test_rutin_tek_satir():
    o = kos("README'deki yazım hatasını düzelt.")
    assert "RUTİN" in o and "<aday-listesi>" not in o and len(o) < 600


def test_zor_tum_bolumler_ve_tavan():
    o = kos("Pazarlama sitesi yap: KVKK uyumlu iletişim formu, SEO, güvenlik testi ve yayın")
    for s in ("Konsey", "Kapanış (6)", "<aday-listesi>", "semgrep", "gitleaks"):
        assert s in o, s
    # tarif varsa (ENVANTER-4) bölümler tarif başlığıyla gelir
    assert "kapılar:" in o or "## Güvenlik ve kalite kapıları" in o
    assert "inceleme ajanları:" in o or "## İnceleme ajanları" in o
    assert len(o) < 20000  # ~≤5k jeton (Desktop notu 1)


def test_cok_is_tek_komut():
    o = kos("ffmpeg ile videonun ilk 10 saniyesini kes.", "Three.js oyununa çok oyunculu mod ve hile önleme ekle")
    assert "# İŞ 1" in o and "# İŞ 2" in o and o.count("RUTİN") == 1


def test_tur_tablosu_araclari_katalogda():
    ad = {json.loads(s)["ad"].lower() for s in (KOK / "docs" / "katalog" / "yetenek.jsonl").read_text(encoding="utf8").splitlines()}
    # plugin ajanları (Agent listesinde) ve kurulmamış ZAP katalogda yok: bilinçli istisna
    istisna = {"zap", "ecc:code-reviewer", "ecc:csharp-reviewer", "differential-review:adversarial-modeler",
               "finish-gate"}  # "UI Finish-Gate Reviewer" çok kelimeli agency ajan adı
    for k, v in pk.TUR.items():
        for parca in " · ".join(v[1:3]).replace(">", "·").split("·"):
            for w in parca.replace(":", " ", 1).split()[1:] if ":" in parca.split()[0] else parca.split():
                w = w.strip("(),").lower()
                if "-" in w.lstrip("-") and w not in istisna and not w.startswith(("ecc:", "differential-review:")):
                    assert w in ad or any(a.endswith(":" + w) for a in ad), (k, w)


def test_ogrenim_ayri_grup(tmp_path, monkeypatch):
    f = tmp_path / "ogrenim.jsonl"
    f.write_text(json.dumps({"ne": "Hero GLB 2 MB altında tutulur", "is": "3D web sitesi", "kaynak": "x.md:3",
                             "alan": "3d,frontend", "araclar": "glb_hat"}, ensure_ascii=False) + "\n", encoding="utf8")
    monkeypatch.setattr(ka, "OGRENIM", f)
    r = ka.ogrenim_ara("3D web sitesi hero GLB boyutu")
    assert len(r) == 1 and r[0]["tur"] == "ogrenim" and r[0]["cagri"] == "x.md:3"


# PLAN-KUR-2: v2 çıktısı (≤6k), yığın + kurulu süzgeci, determinizm
ZOR_IS = "Astro + three.js ile ürün sitesi yap: iyzico ödeme, KVKK formu, SEO, güvenlik testi ve yayın"


def _k(ad, durum="CC", is_=""):
    return {"ad": ad, "tur": "skill", "durum": durum, "is": is_, "metin": "", "tetik": "", "cagri": f"Skill {ad}"}


def test_v2_zor_tavan_ve_sayisal_kapi():
    o = kos(ZOR_IS)
    assert len(o) <= 6000, len(o)
    for s in ("faz 1", "faz 4", "inceleme ajanları:", "Konsey: yok", "elendi:", "LCP ≤2.5 s", "idempotency", "3DS", "SAQ-A"):
        assert s in o, s
    assert o.count("öğrenim:") <= 3


def test_v2_faz_basina_en_fazla_3_arac():
    o = kos(ZOR_IS)
    for s in o.splitlines():
        if s.startswith("faz "):
            assert s.count(" | ") <= 2, s


def test_yigin_metinden_ve_cwd(tmp_path):
    assert {"astro", "three"} <= set(ka.yigin(ZOR_IS, tmp_path))
    (tmp_path / "astro.config.mjs").write_text("", encoding="utf8")
    (tmp_path / "package.json").write_text('{"dependencies": {"astro": "4", "gsap": "3"}}', encoding="utf8")
    assert "astro" in ka.yigin("siteyi hızlandır", tmp_path) and "react" not in ka.yigin("siteyi hızlandır", tmp_path)
    (tmp_path / "package.json").write_text('{"dependencies": {"react": "18"}}', encoding="utf8")
    assert "react" in ka.yigin("siteyi hızlandır", tmp_path)


def test_yigin_suzgeci():
    rows = [_k("react-x", is_="React components only"), _k("cok", is_="React, Vue, Astro islands"),
            _k("notr", is_="Web performance audit"), _k("dn", is_="ASP.NET Core APIs")]
    kal, elen, _ = ka.suz(rows, ["astro"])
    assert [o["ad"] for o in kal] == ["cok", "notr", "dn"] and elen == 1
    kal, elen, _ = ka.suz(rows, ["astro", "django"])
    assert [o["ad"] for o in kal] == ["cok", "notr"] and elen == 2
    assert len(ka.suz(rows, [])[0]) == 4  # yığın bilinmiyorsa eleme yok


def test_kurulu_suzgeci():
    rows = [_k("a"), _k("b", "aday"), _k("c", "ikisi · kapalı(override off)"), _k("d", "repo"), _k("e", "ikisi")]
    kal, _, yok = ka.suz(rows, [])
    assert [o["ad"] for o in kal] == ["a", "e"] and [o["ad"] for o in yok] == ["b", "c", "d"]  # kapalı da çağrılamaz
    # Ömer 06:38: kurulu olmayan araç çıktıda HİÇ yok (kurulum önerisi satırı da yok)
    o = kos(ZOR_IS)
    assert "kurulum önerisi" not in o and "firecrawl" not in o.lower()
    kat = {r["ad"]: r for r in map(json.loads, (KOK / "docs" / "katalog" / "yetenek.jsonl").read_text(encoding="utf8").splitlines())}
    adlar = aday_adlari(o)  # v3: fazsız tek satır/aday
    assert adlar and all(ka.kurulu(kat[a]) for a in adlar), adlar
    assert not any(ka.kurulu(r) for a, r in kat.items() if "firecrawl" in a.lower())  # katalog durumu doğru: aday


def test_yigin_uctan_uca():
    assert "fe-react" not in kos(ZOR_IS)  # Astro işinde React-yalnız araç önerilmez


def test_v2_deterministik():
    assert kos(ZOR_IS) == kos(ZOR_IS)


def test_rutin_bir_satir():
    o = kos("Bir JPEG fotoğrafı PNG'ye dönüştür.")  # bekletilmiş küme (r2) dışında
    assert sum(1 for s in o.splitlines() if s.startswith("RUTİN")) == 1 and "faz 1" not in o


def test_ac_ayrinti():
    o = kos("--ac", "semgrep")
    assert "semgrep" in o.lower() and "çağrı:" in o and "RUTİN" not in o and len(o) < 3000


def test_katalog_ara_suzgec_satiri():
    o = subprocess.run([sys.executable, str(KOK / "tools" / "katalog_ara.py"), ZOR_IS], capture_output=True, text=True,
                       encoding="utf8", env=ENV).stdout
    assert "elendi:" in o and "<aday-listesi>" in o


def aday_adlari(o):
    return [s.split(" · ")[0] for s in o.split("<aday-listesi>\n```text\n")[1].split("\n```")[0].splitlines()]


def test_v3_alan_uzmani_listede():  # (a) PLAN-KUR-2 iş 4 kaybı
    a = aday_adlari(kos("Express.js REST API'sini GraphQL'e kademeli taşı: şema tasarımı, N+1 önleme, JWT kimlik doğrulama, hız sınırı ve geriye uyumluluk."))
    assert "dil-graphql" in a and any(x.startswith("sec-jwt") for x in a), a


def test_v3_unity_isinde_gorsel_uret_yok():  # (b)
    a = aday_adlari(kos("Unity ile 2D platform oyunu ve seviye editörü geliştir: tilemap tabanlı bölüm tasarımı, JSON ile kayıt ve yükleme, oynanış testi, düşman yapay zekası ve Steam için paketleme yap."))
    assert a and not any("gorsel-uret" in x for x in a), a


def test_v3_aday_sayisi_en_fazla_k():  # (c)
    o = kos(ZOR_IS)
    assert 0 < len(aday_adlari(o)) <= pk.K and len(o) <= 6000


def test_v3_genel_sozcuk_varlik_sayilmaz():  # (d)
    assert pk.varliklar("Uygulama sunucusu tasarımı yap, yeni sistem kur") == set()
    assert {"graphql", "jwt"} <= pk.varliklar("GraphQL API'ye JWT ekle")
