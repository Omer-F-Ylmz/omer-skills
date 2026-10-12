import importlib.util
import pathlib

KOK = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("t2u", KOK / "onay/tasarim_2_uygula.py")
t2u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t2u)


def test_uygula_geri_tur(tmp_path):
    ev = tmp_path / ".claude"
    fc = ev / "plugins/cache/omer-skills/frontend-craft/1.5.7/skills/frontend-craft"
    fc.mkdir(parents=True)
    (fc / "SKILL.md").write_text("eski", encoding="utf-8")
    yedek = tmp_path / "yedek"
    t2u.uygula(ev, yedek)
    assert (fc / "scripts/yakinsama.mjs").exists() and (fc / "references/yon-hatti.md").exists()
    assert "3a" in (fc / "SKILL.md").read_text(encoding="utf-8")
    t2u.geri(ev, yedek)
    assert (fc / "SKILL.md").read_text(encoding="utf-8") == "eski"
    assert not (fc / "scripts/yakinsama.mjs").exists()


def test_kurulu_yoksa_bos(tmp_path):
    assert t2u.hedefler(tmp_path) == []
