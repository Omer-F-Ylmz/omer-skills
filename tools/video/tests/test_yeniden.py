"""VİDEO-YENİDEN-1: getir HTTP hatası · eski biçimli rapordan kalem · yeni karar eşlemesi · yeniden izleme puanı."""
import io
import urllib.error
import urllib.request

from video import tarama as tr
from video.cli import main

ESKI = """# Eski video
kanal: X · süre: 20 dk
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| greensock/GSAP | YENİ | ELENDİ | proje bağımlılığı |
| ekran kaydıyla analiz | YENİ | BİLGİ | REF girdisi statik |
- Oxylabs AI Studio → ELE (ücretli proxy)
- shadcn/ui → ZATEN VAR
"""


def test_getir_http_hatasi_anlamli_rc(tmp_path, monkeypatch, capsys):
    def at(*a, **k):
        raise urllib.error.HTTPError("https://s.test/yok", 404, "Not Found", {}, io.BytesIO())
    monkeypatch.setattr(urllib.request, "urlopen", at)
    rc = main(["getir", "https://s.test/yok"], env={"VIDEO_CACHE": str(tmp_path)})
    out = capsys.readouterr().out
    assert rc != 0 and "hata:" in out and "https://s.test/yok" in out and "404" in out and "Traceback" not in out


def test_eski_kalemler_tablo_ve_madde():
    k = tr.eski_kalemler(ESKI)
    assert k[0] == ("greensock/GSAP", "YENİ", "ELENDİ", "proje bağımlılığı")
    assert ("Oxylabs AI Studio", "", "ELE", "ücretli proxy") in k
    assert [x[0] for x in k] == ["greensock/GSAP", "ekran kaydıyla analiz", "Oxylabs AI Studio", "shadcn/ui"]


def _x(**k):
    return {"ad": "a", "durum": "YENİ", "etiket": "ELENDİ", "not": "", "tur": "araç", "kural": None, "es": None,
            "ko": "olgu", "token": False, "departman": "diger", **k}


def test_yeni_karar_esleme():
    assert tr.yeni_karar(_x(kural="omer-kurallar:12"))[0] == "ZATEN VAR"
    assert tr.yeni_karar(_x(es=("x", "skill", 0.9)))[0] == "ZATEN VAR"
    assert tr.yeni_karar(_x())[0] == "RED"                                   # eski ELENDİ, token değil
    assert tr.yeni_karar(_x(token=True))[0] == "DENE"                        # K4: kanıtsız RED token'da DENE
    assert tr.yeni_karar(_x(token=True, **{"not": "ücretli lisans"}))[0] == "RED"
    assert tr.yeni_karar(_x(etiket="BİLGİ"))[0] == "DENE"
    assert tr.yeni_karar(_x(tur="teknik", ko="kural"))[0] == "KURAL"
    assert tr.yeni_karar(_x(tur="prompt", departman="frontend"))[0] == "UYARLA"
    assert tr.yeni_karar(_x(tur="ipucu"))[0] == "ÖĞREN"


def test_celiski_eski_zaten_var_bugun_yok():
    assert tr.celiski_mi(_x(durum="ZATEN VAR", tur="teknik")) and not tr.celiski_mi(_x(durum="ZATEN VAR", kural="k:1"))


def test_puan_agirliklar():
    v = {"tur": tr.ICERIK[0], "kararlar": ["DENE", "UYARLA", "ÖĞREN", "RED"], "token": 1, "kare_zayif": True}
    assert tr.puan(v) == 3 + 2 * 2 + 1 * 2 + 1
    assert tr.puan({**v, "tur": tr.ICERIK[1]}) == tr.puan(v)                 # prompt/şablon da ×3
    assert tr.puan({**v, "tur": tr.ICERIK[2], "kare_zayif": False}) == 4 + 2


# VİDEO-YENİDEN-1b: tam envanter · sahte aday · --yalniz
ENV = [{"ad": "impeccable", "tur": "plugin"}, {"ad": "impeccable:impeccable", "tur": "skill"}, {"ad": "strix", "tur": "cli"},
       {"ad": "anthropic-skills:penetration-testing-with-strix", "tur": "skill"}]


def test_arac_esle_tam_envanter():
    s = tr.envanter_sozluk(ENV)
    for ad in ("impeccable", "impeccable / front end design yeteneği", "usestrix/strix"):
        es = tr.arac_esle(ad, s, [])
        assert es and tr.yeni_karar(_x(etiket="ADAY", es=es))[0] == "ZATEN VAR", ad
    assert tr.arac_esle("TestSprite/testsprite-cli (TestSprite)", s, []) is None
    assert tr.yeni_karar(_x(etiket="ADAY", es=None))[0] == "DENE"


SAHTE = """## kalemler
- Context7 → ZATEN VAR
- mob.ai (MobAI-App/mobai-mcp) → TETİKLEYİCİ · koşul: iOS/Android mobil proje başlarsa
- zeki model yalnız plan/mimari karar ve rapor sentezinde, keşif/araştırma/mekanik kod ucuz model alt-ajanda; effort işe göre, max varsayılan değil → CLAUDE.md (CONTEXT DİSİPLİNİ: delege edilen işte model/effort seçimi)
- Tasarım kadranları: deneysellik / hareket / yoğunluk seviyesi açıkça yazılır (taste-skill README'de 1-10 kadran) → DESIGN.md şablonu (Token'lar)
- ayar: API anahtarı — testsprite.com'a üye ol → API anahtarları → sağ üstten yeni anahtar oluştur (ad: "video") → testsprite setup'a yapıştır
"""


def test_sahte_aday_buyuk_harf_hedef_aday_olmaz():
    k = tr.eski_kalemler(SAHTE)
    assert [x[0] for x in k] == ["Context7", "mob.ai (MobAI-App/mobai-mcp)"]
    assert all(x[2] not in ("CLAUDE", "DESIGN", "API") for x in k)
    assert [a[:12] for a in tr.sahte_kalemler(SAHTE)] == ["zeki model y", "Tasarım kadr", "ayar: API an"]


def test_yalniz_yalniz_verilen_kalemler(tmp_path, monkeypatch, capsys):
    import json
    from jev import cekirdek as c
    V = "AAAAAAAAAAA"
    d, kok = tmp_path / "tarama", tmp_path / "kok"
    (kok / "docs" / "departmanlar").mkdir(parents=True)
    (kok / "docs" / "kurulumlar" / "yeniden").mkdir(parents=True)
    d.mkdir()
    (kok / "docs" / "departmanlar" / "envanter.json").write_text(json.dumps(ENV), encoding="utf-8")
    rapor = kok / "docs" / "kurulumlar" / "yeniden" / "2026-09-24-toplu.md"
    rapor.write_text("# eski\n", encoding="utf-8")
    (d / f"{V}.md").write_text("# v\n| ad | durum | etiket | not |\n|---|---|---|---|\n| impeccable | YENİ | ADAY | x |\n"
                               "| yeni-arac/x | YENİ | ADAY | y |\n| başka | YENİ | ELENDİ | z |\n- kural metni → CLAUDE.md'ye ekle\n", encoding="utf-8")
    eski = (json.dumps({"id": V, "tarih": "2026-09-15", "rapor": f"{V}.md", "adaylar": [], "ele": []}) + "\n"
            + json.dumps({"id": V, "tarih": "2026-09-24", "rapor": "../kurulumlar/yeniden/2026-09-24-toplu.md", "adaylar": ["impeccable"], "ele": [],
                          "etiket": "yeniden:2026-09-24", "tur": "araç/skill tanıtımı", "puan": 4,
                          "kararlar": {"impeccable": "DENE", "yeni-arac/x": "DENE", "başka": "RED", "kural metni": "KURAL"}}, ensure_ascii=False) + "\n")
    (d / "kayit.jsonl").write_text(eski, encoding="utf-8", newline="\n")
    (tmp_path / "liste.txt").write_text(f"{V}\timpeccable\n{V}\tyeni-arac/x\n{V}\tkural metni\n", encoding="utf-8")
    goren = []

    def yargila(self, states, q):
        goren.extend(states)
        self.istek += len(states)
        return [{k: {"type": "choice", "probabilities": {next(iter(v.get("criteria") or {"?": 0})): 1.0}} if v["type"] == "choice"
                 else {"type": "noul", "noul": 0.0} for k, v in q.items()} for _ in states]
    monkeypatch.setattr(c.Tasiyici, "yargila", yargila)
    env = {"VIDEO_TARAMA_DIZIN": str(d), "VIDEO_UYGULA_KOK": str(kok), "VIDEO_EV": str(tmp_path / "ev"),
           "VIDEO_CACHE": str(tmp_path / "c"), "VIDEO_KURALLAR": str(tmp_path / "yok.md")}
    assert main(["yeniden", "--yalniz", str(tmp_path / "liste.txt"), "--istek-tavan", "20"], env=env) == 0
    assert not any("başka" in s for s in goren) and not any("kural metni" in s for s in goren) and len(goren) == 2
    b = (d / "kayit.jsonl").read_text(encoding="utf-8")
    assert b.startswith(eski)
    son = json.loads(b.splitlines()[-1])
    assert son["etiket"] == "yeniden:2026-09-24b" and son["sahte"] == ["kural metni"]
    assert son["kararlar"] == {"impeccable": "ZATEN VAR", "yeni-arac/x": "DENE", "başka": "RED", "kural metni": "SAHTE"}
    r = rapor.read_text(encoding="utf-8")
    assert r.startswith("# eski\n") and "## Düzeltme (1b)" in r and "impeccable" in r
