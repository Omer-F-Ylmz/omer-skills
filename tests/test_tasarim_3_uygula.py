import importlib.util
import pathlib

KOK = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("t3u", KOK / "onay/tasarim_3_uygula.py")
t3u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t3u)


def test_uygula_geri_tur(tmp_path):
    ev = tmp_path / ".claude"
    fc = ev / "plugins/cache/omer-skills/frontend-craft/1.5.7/skills/frontend-craft"
    fc.mkdir(parents=True)
    (fc / "SKILL.md").write_text("eski", encoding="utf-8")
    yedek = tmp_path / "yedek"
    t3u.uygula(ev, yedek)
    assert (fc / "references/vitrin-teknikleri.md").exists()
    assert "3a" in (fc / "SKILL.md").read_text(encoding="utf-8")
    t3u.geri(ev, yedek)
    assert (fc / "SKILL.md").read_text(encoding="utf-8") == "eski"
    assert not (fc / "references/vitrin-teknikleri.md").exists()


def test_kurulu_yoksa_bos(tmp_path):
    assert t3u.hedefler(tmp_path) == []


def test_katalog_yalniz_acik_istekte():
    fc = KOK / "plugins/frontend-craft/skills/frontend-craft"
    skill = (fc / "SKILL.md").read_text(encoding="utf-8")
    assert "Desen (en çok 3" not in skill and "açıkça isterse" in skill
    assert "vitrin-teknikleri" not in (fc / "references/yon-hatti.md").read_text(encoding="utf-8")
    assert "vitrin-teknikleri" not in (KOK / "skills/web-sahne-desenleri/SKILL.md").read_text(encoding="utf-8")
