import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import departman_katalog  # noqa: E402


def test_katalog_skill_klasorune_yazilir_ve_skill_yolu_verir(tmp_path):
    (tmp_path / "skills/departman-x").mkdir(parents=True)
    (tmp_path / "docs/departmanlar").mkdir(parents=True)
    (tmp_path / "skills/departman-x/SKILL.md").write_text("---\nname: departman-x\n---\n# X\n\n## Adımlar\n1. a\n", encoding="utf-8")
    (tmp_path / "docs/departmanlar/x.md").write_text("# Departman: x\nmetin\n| araç | ne zaman |\n|---|---|\n| pw | e2e |\n", encoding="utf-8")
    assert list(departman_katalog.uret(tmp_path)) == ["departman-x"]
    k = (tmp_path / "skills/departman-x/katalog.md").read_text(encoding="utf-8")
    assert "| pw | e2e |" in k and "metin" not in k
    list(departman_katalog.uret(tmp_path))  # ikinci koşu satırı çoğaltmaz
    assert (tmp_path / "skills/departman-x/SKILL.md").read_text(encoding="utf-8").count("katalog.md") == 1
