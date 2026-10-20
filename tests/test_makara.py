"""MAKARA: ders sayacı (çift not yok), mekanik denetim, çift-aile hakem kararı, onay uygula/geri."""
import json
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
