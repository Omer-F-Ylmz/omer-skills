import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skill-paket"))
import awesome_rehber_zip as az  # noqa: E402
import zip_denetle  # noqa: E402


def test_zip_tsvleri_references_icine_gomer(tmp_path):
    skill, kaynak = tmp_path / "skill", tmp_path / "kaynak"
    skill.mkdir(), kaynak.mkdir()
    (skill / "SKILL.md").write_text("---\nname: awesome-rehber\ndescription: test\n---\nx\n", encoding="utf-8")
    (kaynak / "katalog.tsv").write_text("a\tb\n", encoding="utf-8")
    (kaynak / "awesome-python.tsv").write_text("ad\turl\n", encoding="utf-8")
    z = az.paketle(skill, kaynak, tmp_path / "out.zip")
    assert sorted(zipfile.ZipFile(z).namelist()) == [
        "awesome-rehber/SKILL.md", "awesome-rehber/references/awesome-python.tsv", "awesome-rehber/references/katalog.tsv"]
    assert zip_denetle.denetle(z) == []
