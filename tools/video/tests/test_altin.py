"""VİDEO-GÖZ-1a K4: `video altin puan` — rapor.md altın JSON'a karşı (salt okur, LLM yok)."""
import json
from pathlib import Path

from video import altin as au
from video import cli

FX = Path(__file__).parent / "fixture" / "altin"


def _puan():
    return au.puan((FX / "rapor.md").read_text(encoding="utf-8"), json.loads((FX / "altin.json").read_text(encoding="utf-8")))


def test_eslesme_alias_ve_noktalama():
    assert au.eslesir("Sonet 5.5", "Sonnet 5.5", ["Sonet 5.5"])
    assert au.eslesir("ThreeJS", "Three.js", [])
    assert au.eslesir("gsap", "GSAP", [])


def test_levenshtein_yalniz_uzun_adda():
    assert au.eslesir("Sonnett 5.5", "Sonnet 5.5", [])  # 9 karakter, mesafe 1
    assert not au.eslesir("Vute", "Vite", [])  # ≤5 karakter: bulanık eşleşme yok
    assert not au.eslesir("Sonnet 5.5", "Opus 5.5", [])


def test_tur_bazinda_yakalama():
    p = _puan()
    assert p["tur"] == {"model": (1, 2), "kütüphane": (2, 3), "uygulama": (0, 1)}
    assert p["yakalama"] == (3, 6)


def test_isabet():
    assert _puan()["isabet"] == (3, 4)  # 'Uydurma Araç' altında yok


def test_ad_yazim_dogrulugu():
    assert _puan()["ad_yazim"] == (2, 3)  # Sonet≠Sonnet; ThreeJS=Three.js (noktalama)


def test_aciklama_linkleri_affiliate_parametresi_eslesmeyi_bozmaz():
    p = _puan()
    assert p["link_aciklama"] == {"yakalama": (2, 2), "sinif": (0, 2)}  # topview aday yanlış · dala sponsor yanlış


def test_yorum_linkleri_ayri_satir():
    assert _puan()["link_yorum"] == {"yakalama": (1, 2), "sinif": (1, 1)}


def test_site_ui_yakalama():
    assert _puan()["site_ui"] == (1, 2)


def test_komutlar_kurulum_tablosundan():
    assert _puan()["komutlar"] == (1, 2)


def test_yeni_alanlar_rapor_bolumu_yokken_sifir():  # 1b-2a: alan_yok boş; fixture raporunda URL'ler/İş akışı/Promptlar bölümü yok
    p = _puan()
    for k, n in (("urller", 1), ("is_akisi", 2), ("promptlar", 1)):
        assert p[k] == (0, n)
    assert p["alan_yok"] == []


def test_kacan_adaylar():
    assert _puan()["kacan"] == [("Opus 5.5", "model"), ("Lenis", "kütüphane"), ("TopView", "uygulama")]


def test_cli_altin_puan(capsys):
    assert cli.main(["altin", "puan", str(FX / "rapor.md"), str(FX / "altin.json")], env={}) == 0
    out = capsys.readouterr().out
    assert "yakalama 3/6" in out and "urller: yakalama 0/1" in out and "kaçan: Opus 5.5 (model)" in out


def _puan_ile(altin):
    return au.puan((FX / "rapor.md").read_text(encoding="utf-8"), altin)


BELIRSIZLI = {"adaylar": [{"ad": "Three.js", "tur": "kütüphane"},
                          {"ad": "Uydurma Araç", "tur": "uygulama", "belirsiz": True},
                          {"ad": "Hiç Geçmeyen", "tur": "model", "belirsiz": True}]}


def test_belirsiz_aday_paydada_yok_bulunursa_ayri_satirda():
    p = _puan_ile(BELIRSIZLI)
    assert p["yakalama"] == (1, 1) and p["kacan"] == []
    assert p["belirsiz"] == (1, 2)
    assert "  belirsiz bulundu 1/2" in au.satirlar(p)


def test_tur_kiriliminda_belirsizler_haric():
    assert _puan_ile(BELIRSIZLI)["tur"] == {"kütüphane": (1, 1)}


def test_ogrenimler_tum_metinde_ayni_satir_kelime_ortusmesi():
    metin = "# Rapor\n\n- Lenis kaydırmayı yumuşatır, GSAP ile birlikte\n- kamera sabit\n"
    p = au.puan(metin, {"ogrenimler": [
        {"ogrenim": "Lenis ile kaydırmayı yumuşat", "tur": "ipucu"},  # lenis+kaydırmayı aynı satır → 2/3
        {"ogrenim": "Kamera titreşimi gimbal ile azaltılır", "tur": "ipucu"},  # yalnız kamera → 1/4
        {"ogrenim": "Lenis kaydırmayı yumuşatır", "tur": "ipucu", "belirsiz": True}]})  # paydada yok
    assert p["ogrenimler"] == (1, 2)
    assert "öğrenimler: yakalama 1/2" in au.satirlar(p)


def test_ogrenimler_ve_belirsiz_yoksa_satir_cikmaz():
    s = au.satirlar(_puan())
    assert not any(x.startswith("öğrenimler") or "belirsiz" in x for x in s)
