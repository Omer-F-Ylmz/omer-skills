import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import envanter_4_uygula as e  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, dist = tmp_path / "ev", tmp_path / "dist"
    hedef = ev / "skills" / "yetenek-getir"
    (hedef / "tarifler").mkdir(parents=True)
    (hedef / "SKILL.md").write_text("canli", encoding="utf-8")
    (hedef / "tarifler" / "eski.md").write_text("eski", encoding="utf-8")
    assert e.main(["--kuru"], ev, dist) == 0 and not dist.exists() and not (hedef / "kilavuz").exists()
    assert e.main(["uygula"], ev, dist) == 0
    assert (hedef / "SKILL.md").read_text(encoding="utf-8") == "canli"
    assert not (hedef / "tarifler" / "eski.md").exists() and (hedef / "kilavuz").is_dir()
    tsv = (hedef / "derin.tsv").read_text(encoding="utf-8").splitlines()
    assert tsv[0].startswith("tur\tad\tdurum\tnasil") and all(s.count("\t") == 8 for s in tsv)
    adlar = zipfile.ZipFile(dist / "yetenek-getir.zip").namelist()
    assert "yetenek-getir/SKILL.md" in adlar and "yetenek-getir/derin.tsv" in adlar
    assert sum(a.startswith("yetenek-getir/kilavuz/") for a in adlar) == len(list((e.KAT / "kilavuz").glob("*.md")))
    assert (dist / "LISTE.md").read_text(encoding="utf-8").count(".zip") == 1 and not (dist / "yetenek-getir").exists()
    assert e.main(["--geri"], ev, dist) == 0
    assert (hedef / "tarifler" / "eski.md").read_text(encoding="utf-8") == "eski"
    assert not (hedef / "kilavuz").exists() and not (hedef / "derin.tsv").exists()
    assert not (ev / "skills-yedek-envanter4").exists()


def test_hedef_yoksa_durur(tmp_path):
    try:
        e.main(["uygula"], tmp_path / "ev", tmp_path / "dist")
    except SystemExit as s:
        assert "envanter_2_uygula" in str(s)
    else:
        raise AssertionError("hedef yokken uygula durmalıydı")
