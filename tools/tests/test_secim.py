import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "secim"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "olcum"))
import dizin_uret  # noqa: E402
import secim_olc  # noqa: E402


def test_ilk_secim_yonlendirme_ve_genel_ajani_atlar():
    a = ["Skill:anthropic-skills:departman-frontend", "Grep", "Agent:general-purpose", "Agent:fe-animasyon-tasarimci", "Skill:x"]
    assert secim_olc.ilk_secim(a) == ("fe-animasyon-tasarimci", 4)
    assert secim_olc.ilk_secim(["Skill:secim:departman-belge", "Glob"]) == ("", 2)


def test_toplu_tavan_asilacaksa_cagri_yapmaz(tmp_path, monkeypatch):
    s = tmp_path / "usd.txt"
    s.write_text("8.5")
    monkeypatch.setattr(secim_olc, "SAYAC", s)
    monkeypatch.setattr(secim_olc, "CIKTI", tmp_path)
    monkeypatch.setattr(secim_olc, "kos", lambda *a, **k: (_ for _ in ()).throw(AssertionError("çağrı yapıldı")))
    secim_olc.toplu("once")  # 8.5 + 3.0 > 10
    assert s.read_text() == "8.5"


def test_dizin_satiri_yenisiyle_degisir_tek_kalir(tmp_path, monkeypatch):
    d = tmp_path / "skills" / "departman-belge"
    d.mkdir(parents=True)
    (d / "SKILL.md").write_text("---\nname: departman-belge\n---\nGiriş\nSkill dizini: eski satır\n\n## Adımlar\n1. a\n", encoding="utf-8")
    monkeypatch.setattr(dizin_uret, "KALITE3", {})
    for _ in range(2):
        dizin_uret.yaz(tmp_path, {"belge": [("ajan:dok-x", "teklif")]}, "dizin.md")
    g = (d / "SKILL.md").read_text(encoding="utf-8")
    assert g.count("Skill dizini:") == 1 and dizin_uret.SATIR in g and "eski satır" not in g
    assert re.search(r"^- ajan:dok-x — teklif$", (d / "dizin.md").read_text(encoding="utf-8"), re.M)
