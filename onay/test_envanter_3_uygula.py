import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envanter_3_uygula as e  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, dist = tmp_path / "ev", tmp_path / "dist"
    eski = ev / "skills" / "yetenek-getir"
    eski.mkdir(parents=True)
    (eski / "SKILL.md").write_text("eski", encoding="utf-8")
    md = ev / "CLAUDE.md"
    md.write_bytes(b"# kurallar\n- a\n")
    assert e.main(["--kuru"], ev, dist) == 0
    assert md.read_bytes() == b"# kurallar\n- a\n" and not (ev / "skills" / "plan-kur").exists()
    assert (eski / "SKILL.md").read_text() == "eski"
    assert {"plan-kur/plan_kur.py", "plan-kur/SKILL.md"} <= set(zipfile.ZipFile(dist / "plan-kur.zip").namelist())
    assert "yetenek-getir/ogrenim.jsonl" in zipfile.ZipFile(dist / "yetenek-getir.zip").namelist()
    assert (dist / "LISTE.md").read_text(encoding="utf-8").count(".zip") == 2
    assert e.main(["uygula"], ev, dist) == 0
    assert (ev / "skills" / "plan-kur" / "plan_kur.py").exists() and (eski / "ogrenim.jsonl").exists()
    assert md.read_bytes().count(e.SATIR.encode("utf-8")) == 1 and b"\r" not in md.read_bytes()
    assert e.main(["--geri"], ev, dist) == 0
    assert md.read_bytes() == b"# kurallar\n- a\n" and (eski / "SKILL.md").read_text() == "eski"
    assert not (ev / "skills" / "plan-kur").exists() and not (ev / "skills-yedek-envanter3").exists()
