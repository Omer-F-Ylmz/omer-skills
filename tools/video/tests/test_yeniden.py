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
