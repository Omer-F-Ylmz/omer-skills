import sys
from collections import deque
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kalite3_hiz as kh  # noqa: E402

AD = "deneme-ajan"
MD = f"---\nname: {AD}\ndescription: d\ntools: Read\n---\ngövde\n"


def o(metin):
    return {"metin": metin, "usd": 0.01, "sure": 1, "model": {}}


@pytest.fixture
def ortam(tmp_path, monkeypatch):
    monkeypatch.setattr(kh, "TSV", tmp_path / "hiz.tsv")
    monkeypatch.setattr(kh, "IS", tmp_path / "is")
    monkeypatch.setattr(kh, "DUR", tmp_path / "olcum.dur")
    monkeypatch.setitem(kh.gorev, AD, {"istem": "soru", "rubrik": [{"regex": "(?i)x", "puan": 1}], "model": "sonnet"})
    (tmp_path / "is").mkdir()
    yol = tmp_path / f"{AD}.md"
    yol.write_text(MD, encoding="utf-8")
    return yol


def test_es_tavani_16_ram_93te_artar_95ten_sonra_azalir():
    assert kh.ES_TAVAN == 16 and kh.RAM_DUR == 95
    assert kh.es_ayarla(4, 93) == 5 and kh.es_ayarla(4, 95) == 4 and kh.es_ayarla(4, 96) == 3 and kh.es_ayarla(16, 50) == 16


def test_jev_onbellekli_ayni_yanit_ikinci_kez_yargilanmaz(ortam, monkeypatch, tmp_path):
    n = []

    class Sahte:
        def __init__(self, **k):
            pass

        def yargila(self, states, questions):
            n.append(len(states))
            return [{"kalite": {"score": 3.5}} for _ in states]
    monkeypatch.setattr(kh, "Tasiyici", Sahte)
    monkeypatch.setattr(kh, "JEV_OB", tmp_path / "jev-ob.json")
    assert kh.jev(AD, "x yanıt") == kh.jev(AD, "x yanıt") == 7.0 and n == [1]


def test_ana_kolu_ayni_gorev_icin_yeniden_kullanilir(ortam, monkeypatch):
    monkeypatch.setitem(kh.gorev, "ikiz", dict(kh.gorev[AD]))  # aynı istem + model, farklı ajan
    olculen = []

    def olc(ad, kol, tur, *a):
        olculen.append((ad, kol))
        return {"ajan": ad, "kol": kol, "puan": "1", "jev": "8", "usd": "0.01", "alt_usd": "", "alt_model": ""}, "x"
    monkeypatch.setattr(kh, "olc", olc)
    k = kh.Kosu.__new__(kh.Kosu)
    k.q, k.calisan, k.ardisik, k.ut, k.gecen = deque(), 1, 0, {}, []
    k.ana = {kh.ana_anahtar(AD, "sonnet"): {"ajan": AD, "kol": "ana", "puan": "1", "jev": "6", "usd": "0.01"}}
    monkeypatch.setattr(k, "kabul", lambda *a: k.gecen.append(a[0]))
    k.isle("ikiz", 0, ortam, "sonnet", ortam.parent, None)
    assert olculen == [("ikiz", "ajan")] and k.gecen == ["ikiz"]


def test_ek_kokler_sirada_ve_kuyrukta(tmp_path, monkeypatch):
    for kok, aile, ad in (("kalite3", "frontend", "fe-a"), ("kalite3-d15", "dil-cerceve", "dil-b"), ("kalite3-d15", "altyapi", "ops-c"),
                          ("kalite3-ruflo", "surec-plan", "pln-d")):
        (tmp_path / kok / aile).mkdir(parents=True, exist_ok=True)
        (tmp_path / kok / aile / f"{ad}.md").write_text(MD, encoding="utf-8")
        monkeypatch.setitem(kh.gorev, ad, {"istem": "s", "rubrik": [], "model": "sonnet"})
    monkeypatch.setattr(kh.mo, "AJAN", tmp_path / "kalite3")
    monkeypatch.setattr(kh, "EK", [tmp_path / "kalite3-d15", tmp_path / "kalite3-ruflo", tmp_path / "yok"])
    assert [ad for _, ad in kh.sira()] == ["fe-a"]  # d13 parti dilimi yalnız ana kökten
    k = kh.Kosu.__new__(kh.Kosu)
    k.q, k.ele_alinan = deque(), {"ops-c"}
    k.ek_aday()
    assert [(i[0], i[1], i[4].name) for i in k.q] == [("dil-b", 0, "dil-cerceve"), ("pln-d", 0, "surec-plan")]


def test_api_hatasi_olcum_sayilmaz(ortam, monkeypatch):
    monkeypatch.setattr(kh.cagri, "dene", lambda *a, **k: o("API Error: 502 getaddrinfo failed"))
    with pytest.raises(kh.Gecici):
        kh.olc(AD, "ana", 0, ortam, "sonnet", ortam.parent)
    assert not kh.TSV.exists()


def test_jev_istisnasi_olcum_sayilmaz(ortam, monkeypatch):
    monkeypatch.setattr(kh.cagri, "dene", lambda *a, **k: o("x yanıt"))

    def bozuk(*a):
        raise RuntimeError("OPENROUTER: bağlanılamadı")
    monkeypatch.setattr(kh, "jev", bozuk)
    with pytest.raises(kh.Gecici, match="Jev"):
        kh.olc(AD, "ana", 0, ortam, "sonnet", ortam.parent)
    assert not kh.TSV.exists()


def test_gecici_kuyruga_doner_3_ardisikta_durur(ortam, monkeypatch):
    def gecici(*a):
        raise kh.Gecici("API Error: 502")
    monkeypatch.setattr(kh, "olc", gecici)
    k = kh.Kosu.__new__(kh.Kosu)
    k.q, k.calisan, k.ardisik = deque(), 3, 0
    for i in range(3):
        k.isle(AD, i, ortam, "sonnet", ortam.parent, None)
        assert kh.DUR.exists() == (i == 2)
    assert [x[1] for x in k.q] == [2, 1, 0] and k.calisan == 0


def test_plan_limiti_olcum_sayilmaz_ve_bekletir(ortam, monkeypatch):
    monkeypatch.setattr(kh.cagri, "dene", lambda *a, **k: o("You've hit your session limit · resets 11:40pm (Europe/Istanbul)"))
    with pytest.raises(kh.Gecici, match="limit"):
        kh.olc(AD, "ana", 0, ortam, "sonnet", ortam.parent)
    assert not kh.TSV.exists()
    k = kh.Kosu.__new__(kh.Kosu)
    k.q, k.calisan, k.ardisik, k.bekle = deque(), 4, 0, 0
    for i in range(4):
        k.geri((AD, i), kh.Gecici("You've hit your session limit · resets 11:40pm"))
    assert not kh.DUR.exists() and k.ardisik == 0 and k.bekle > kh.time.time() + 600  # limit: DUR yok, kendiliğinden bekler


def test_onarilan_tanim_geri_donerse_yeniden_onarilmaz(ortam, monkeypatch):
    yeni = ortam.parent / "yeni.md"
    yeni.write_text(MD, encoding="utf-8")
    monkeypatch.setattr(kh, "onar", lambda *a: yeni)
    monkeypatch.setattr(kh, "olc", lambda *a: (_ for _ in ()).throw(kh.Gecici("Jev")))
    k = kh.Kosu.__new__(kh.Kosu)
    k.q, k.calisan, k.ardisik = deque(), 1, 0
    k.isle(AD, 1, ortam, "sonnet", ortam.parent, ("neden", "yanıt"))
    assert k.q[0][2] == yeni and k.q[0][5] is None


def test_onarim_bicim_eslesmezse_bir_kez_hatirlatir(ortam, monkeypatch):
    yanit = iter([o("İşte tanım:\n" + MD), o(f"<<<AJAN\n{MD}AJAN>>>")])
    istemler = []
    monkeypatch.setattr(kh.cagri, "kos", lambda e, istem, *a, **k: istemler.append(istem) or next(yanit))
    y = kh.onar(AD, 1, ortam, "neden", "yanıt")
    assert y and kh.mo.tanim(y, "x")[0] == AD
    assert len(istemler) == 2 and "<<<AJAN" in istemler[1].split("Current definition:")[-1]


def test_onarim_bicim_iki_kez_bozuksa_none(ortam, monkeypatch):
    istemler = []
    monkeypatch.setattr(kh.cagri, "kos", lambda e, istem, *a, **k: istemler.append(istem) or o("biçimsiz"))
    assert kh.onar(AD, 1, ortam, "neden", "yanıt") is None and len(istemler) == 2


def test_onarim_api_hatasi_gecici(ortam, monkeypatch):
    monkeypatch.setattr(kh.cagri, "kos", lambda *a, **k: o("API Error: 502"))
    with pytest.raises(kh.Gecici):
        kh.onar(AD, 1, ortam, "neden", "yanıt")


def test_devam_yarim_ajani_sonraki_tura_alir(ortam, monkeypatch):
    monkeypatch.setattr(kh, "sira", lambda kokler=None: [(ortam.parent, AD)])
    s = dict.fromkeys(kh.ALAN, "")
    s.update(aile=str(ortam.parent), ajan=AD, kol="ajan", tur="0", model="sonnet", puan="1.0", usd="0.01", jev="4.0", strict="1")
    with kh.TSV.open("w", encoding="utf-8", newline="\n") as f:
        f.write("\t".join(kh.ALAN) + "\n" + "\t".join(str(s[a]) for a in kh.ALAN) + "\n")
    (kh.IS / "yanit").mkdir()
    (kh.IS / "yanit" / f"{AD}-ajan-t0.md").write_text("eski yanıt", encoding="utf-8")
    k = kh.Kosu.__new__(kh.Kosu)
    k.q, k.gecen, k.ut = deque(), [], {}
    k.ana = {kh.ana_anahtar(AD, "sonnet"): dict(s, kol="ana", jev="6.0")}
    k.devam()
    assert [(x[0], x[1], x[5][1]) for x in k.q] == [(AD, 1, "eski yanıt")] and "judge" in k.q[0][5][0]
