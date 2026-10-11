import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ajan_getir_zip as az  # noqa: E402


def test_istemler_zipe_gomulur_yol_goreli(tmp_path):
    a = tmp_path / "x.md"
    a.write_text("---\nname: Code Reviewer\n---\ngövde\n", encoding="utf-8")
    sk = tmp_path / "skill"
    sk.mkdir()
    (sk / "SKILL.md").write_text("---\nname: ajan-getir\ndescription: d\n---\n", encoding="utf-8")
    (sk / "katalog.tsv").write_text(f"ad\tmodel\ttek_satir\tyol\nocto:droids:Code Reviewer\tsonnet\tt\t{a.as_posix()}\n", encoding="utf-8")
    zp = az.paketle(sk, tmp_path / "out.zip")
    with zipfile.ZipFile(zp) as z:
        assert z.read("ajan-getir/references/ajanlar/octo-droids-code-reviewer.md") == a.read_bytes()
        assert z.read("ajan-getir/katalog.tsv").decode().splitlines()[1].endswith("\treferences/ajanlar/octo-droids-code-reviewer.md")
        assert "ajan-getir/SKILL.md" in z.namelist()
