"""MAKARA: ders sayacı (çift not yok), mekanik denetim, çift-aile hakem kararı, onay uygula/geri."""
import json
import re
import pytest
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "onay"))
import makara_gece as g  # noqa: E402
import makara_ders as d  # noqa: E402
import makara_onay as o  # noqa: E402


def test_ders_sayac_tekrar_ve_idempotent(tmp_path):
    sira, durum = tmp_path / "sira", tmp_path / "ders.json"
    sira.mkdir()
    d.DURUM = durum
    for ad, sonuc in (("a-1", "Ders: kapı soruya bakıp ayar yapılmaz\nbaşka satır"), ("a-2", "- **Ders:** kapı soruya bakıp ayar yapılmaz")):
        (sira / f"{ad}.json").write_text(json.dumps({"result": sonuc, "total_cost_usd": 0.5, "modelUsage": {"m": {}}}), encoding="utf-8")
    simdi = time.time() + 100
    assert d.tara(sira, durum, simdi) == (2, 1, 1)
    assert d.tara(sira, durum, simdi) == (0, 0, 0)  # aynı dosya ikinci kez işlenmez
    e = list(d.yukle()["dersler"].values())
    assert len(e) == 1 and e[0]["sayac"] == 2
    y = d.not_yaz(time.strftime("%Y-%m-%d", time.localtime()), d.yukle(), tmp_path)
    assert "×2" in y.read_text(encoding="utf-8") and "$1.0" in y.read_text(encoding="utf-8")


def test_mekanik():
    assert g.mekanik("a\nb", "En fazla 3 satır") is True and g.mekanik("a\nb\nc\nd", "En fazla 3 satır") is False
    assert g.mekanik("Bir. İki. Üç.", "En fazla 2 cümle") is False
    assert g.mekanik("x", "yorum") is None and g.mekanik(" ", "yorum") is False


def test_karar_ikinci_aile_ayrisirsa_ret():
    assert g.karar({"h1": ["B", "B", "EQ"], "h2": ["B", "EQ", "B"]}, 1, 1)[0] is True
    assert g.karar({"google": ["B", "B", "B"], "nvidia": ["A", "EQ", "B"]}, 1, 1)[0] is False
    assert g.karar({"google": ["B"]}, 1, 1)[0] is False  # tek aile
    assert g.karar({"google": ["B", None], "nvidia": ["B", "B"]}, 1, 1)[0] is False  # eksik oy
    assert g.karar({"google": ["B"], "nvidia": ["B"]}, 2, 1)[0] is False  # mekanik kötüleşti


def test_onay_uygula_geri(tmp_path):
    hedef = tmp_path / "SKILL.md"
    hedef.write_bytes(b"# x\r\nsatir\r\n")
    (tmp_path / "kum").mkdir()
    (tmp_path / "kum/m1.json").write_text(json.dumps({"id": "m1", "hedef": str(hedef), "kural": "Kısa yaz", "durum": "bekliyor"}), encoding="utf-8")
    assert o.uygula("m1", m=tmp_path).startswith("uygulandi")
    assert hedef.read_bytes().endswith(b"- K\xc4\xb1sa yaz\r\n") and b"\r\n## Makara" in hedef.read_bytes()
    hedef.write_bytes(hedef.read_bytes() + b"+")
    assert "reddedildi" in o.uygula("m1", True, tmp_path)  # sonradan değişen hedef ezilmez
    hedef.write_bytes(hedef.read_bytes()[:-1])
    assert o.uygula("m1", True, tmp_path).startswith("geri") and hedef.read_bytes() == b"# x\r\nsatir\r\n"


def _gece_ortam(mp, tmp_path, havuz):
    hedef = tmp_path / "hedef.md"
    hedef.write_text("# hedef metin", encoding="utf-8")
    cagrilar = []

    def sahte(tur, istem, **kw):
        cagrilar.append(kw)
        y = havuz(tur, istem)
        return (y, "fake/x", []) if y else (None, None, [])

    def yasak(*a, **k):
        raise AssertionError("Claude/Haiku çağrıldı")

    mp.setattr(g.H, "cagir", sahte)
    mp.setattr(g.H, "_haiku", yasak)
    mp.setattr(g.subprocess, "run", yasak)
    mp.setattr(g.H, "ERT", tmp_path / "ertelenen.jsonl")
    mp.setattr(g.H, "DIZIN", tmp_path)
    mp.setattr(g, "M", tmp_path / "makara")
    mp.setattr(g, "KASA", tmp_path / "kasa")
    mp.setattr(g, "OZET", tmp_path / "uyku-ozet.txt")
    mp.setattr(g, "HAFTA", tmp_path / "makara-hafta-ozet.txt")
    mp.setattr(g, "ram", lambda: 10)
    mp.setattr(g.makara_ders, "yukle", lambda: {"dersler": {}})
    mp.setattr(g, "hedefler", lambda serit, n, imlec: [str(hedef)][:n])
    g.Say.n = 0
    return hedef, cagrilar


def _saglam(tur, istem):
    if tur == "hakem":  # yeni yanıt hangi konumdaysa onu seç
        a = istem.split("=== Yanıt A ===")[1].split("=== Yanıt B ===")[0]
        return "SONUC: " + ("A" if "YENI" in a else "B")
    if istem.startswith("Kural:"):
        return "YENI yanıt"
    return "eski yanıt" if "Hedef:" not in istem else "Her değişiklikten önce testi çalıştır ve kanıtı raporla."


def test_makara_koşusunda_claude_cagrisi_sifir_ve_ozet_kisa(tmp_path):
    with pytest.MonkeyPatch.context() as mp:
        hedef, cagrilar = _gece_ortam(mp, tmp_path, _saglam)
        kabul, toplam, _ = g.gece("router", 1)
        assert (kabul, toplam) == (1, 1)
        assert cagrilar and all(kw["haiku_tavan"] == 0 for kw in cagrilar) and g.Say.claude == 0
        ozet = (tmp_path / "uyku-ozet.txt").read_text(encoding="utf-8").splitlines()
        assert len(ozet) <= 12 and ozet[-1].startswith("Claude çağrısı=0") and "kabul 1" in ozet[1]
        assert (tmp_path / "kasa/90-log" / f"uyku-ozet-{time.strftime('%Y-%m-%d')}.md").read_text(encoding="utf-8").splitlines() == ozet
        hafta = (tmp_path / "makara-hafta-ozet.txt").read_text(encoding="utf-8").splitlines()
        assert len(hafta) <= 15 and "onay bekleyen 1" in hafta[0]


def test_makara_haiku_tavan_acilamaz_ve_kaynakta_claude_yok():
    kaynak = Path(g.__file__).read_text(encoding="utf-8")
    assert not re.search(r"anthropic|claude-haiku|--model|[\"']claude[\"']|os\.system", kaynak, re.I)
    assert set(re.findall(r"haiku_tavan\s*=\s*(\w+)", kaynak)) == {"0"}
    with pytest.raises(TypeError):
        g.cagri("yazim", "x", haiku_tavan=3)


def test_havuz_tukenirse_oneri_atilmaz_ertelenir_ve_ertesi_gece_alinir(tmp_path):
    with pytest.MonkeyPatch.context() as mp:
        hedef, _ = _gece_ortam(mp, tmp_path, lambda tur, istem: None)
        mp.setattr(g.H, "cagir", lambda tur, istem, **kw: (None, None, ["x:429"]))
        g.gece("router", 1)
        ert = [json.loads(s) for s in g.H.ERT.read_text(encoding="utf-8").splitlines()]
        assert [e["id"] for e in ert] == ["makara:" + str(hedef)] and ert[0]["etiket"] == "makara"
        assert "ertelenen 1" in (tmp_path / "uyku-ozet.txt").read_text(encoding="utf-8").splitlines()[1]
        assert g.H.tekrar() == (0, 1)  # havuz tekrarı makara kaydına dokunmaz
        mp.setattr(g.H, "cagir", lambda tur, istem, **kw: (_saglam(tur, istem), "fake/x", []))
        g.Say.n = 0
        assert g.gece("router", 1)[0] == 1  # ertesi gece aynı hedef işlenir
        assert not g.H.ERT.read_text(encoding="utf-8").strip()
