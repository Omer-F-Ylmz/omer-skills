import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envanter_2_uygula as e  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, dist = tmp_path / "ev", tmp_path / "dist"
    eski = ev / "skills" / "yetenek-getir"
    eski.mkdir(parents=True)
    (eski / "SKILL.md").write_text("eski", encoding="utf-8")
    assert e.main(["--kuru"], ev, dist) == 0 and not dist.exists() and (eski / "SKILL.md").read_text() == "eski"
    assert e.main(["uygula"], ev, dist) == 0
    assert (eski / "katalog_ara.py").exists() and (eski / "SKILL.md").read_text(encoding="utf-8") != "eski"
    zipler = sorted(dist.glob("*.zip"))
    assert len(zipler) == len(e.kaynaklar()) == 14
    assert "yetenek-getir/yetenek.tsv" in zipfile.ZipFile(dist / "yetenek-getir.zip").namelist()
    assert (dist / "LISTE.md").read_text(encoding="utf-8").count(".zip") == 14
    assert e.main(["--geri"], ev, dist) == 0
    assert (eski / "SKILL.md").read_text() == "eski" and not (eski / "katalog_ara.py").exists()
    assert not (ev / "skills-yedek-envanter2").exists()
