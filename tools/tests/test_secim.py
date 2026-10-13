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


def test_dizin_skill_md_sonuna_gomulur_tek_kalir(tmp_path, monkeypatch):
    for dep in dizin_uret.ALAN:
        d = tmp_path / "skills" / f"departman-{dep}"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(f"---\nname: departman-{dep}\n---\nGiriş\nSkill dizini: eski satır\n\n## Adımlar\n1. a\n", encoding="utf-8")
        (d / "dizin.md").write_text("eski", encoding="utf-8")
    monkeypatch.setattr(dizin_uret, "KALITE3", {})
    for _ in range(2):  # idempotent
        dizin_uret.yaz(tmp_path, {"belge": [("ajan:db-sql-sorgu", "teklif")]}, {"belge": [("p:careful", "Use when running destructive commands. Long tail words here")]})
    d = tmp_path / "skills" / "departman-belge"
    g = (d / "SKILL.md").read_text(encoding="utf-8")
    assert "Skill dizini:" not in g and g.count(dizin_uret.BAS) == 1 and not (d / "dizin.md").exists()
    assert re.search(r"^ajan:db-sql-sorgu$", g, re.M)  # adı açık ajan: yalnız ad
    assert re.search(r"^careful: running destructive commands$", g, re.M)  # opak: ≤8 kelime ne zaman
    assert g.index("## Adımlar") < g.index(dizin_uret.BAS)  # sabit önek önce, dizin sonda


def test_secim_opak_ve_anahtar():
    k = [("p:dn-efcore-migration", "x"), ("p:defuddle", "Extract markdown with Defuddle"), ("p:careful", "Use when running destructive commands"), ("p:resolve-conflict", "x"), ("p:db-sema-tasarim", "x")]
    assert [a for a, _ in dizin_uret.sec(k)] == ["p:careful", "p:resolve-conflict"]
