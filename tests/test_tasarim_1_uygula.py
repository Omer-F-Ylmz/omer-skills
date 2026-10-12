import importlib.util
import pathlib

KOK = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("t1u", KOK / "onay/tasarim_1_uygula.py")
t1u = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t1u)


def test_uygula_geri_tur(tmp_path):
    ev = tmp_path / ".claude"
    fc = ev / "plugins/cache/omer-skills/frontend-craft/1.5.7/skills/frontend-craft"
    fc.mkdir(parents=True)
    (fc / "SKILL.md").write_text("eski", encoding="utf-8")
    yedek = tmp_path / "yedek"
    t1u.uygula(ev, yedek)
    assert (ev / "skills/tasarim-katalog/references/siteler.tsv").exists()
    assert (fc / "scripts/slop.mjs").exists() and (fc / "SKILL.md").read_text(encoding="utf-8") != "eski"
    t1u.geri(ev, yedek)
    assert (fc / "SKILL.md").read_text(encoding="utf-8") == "eski"
    assert not (fc / "scripts/slop.mjs").exists() and not (ev / "skills/tasarim-katalog").exists()
