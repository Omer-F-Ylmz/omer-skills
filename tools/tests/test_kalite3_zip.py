import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import kalite3_zip as kz  # noqa: E402

GIRIS = ["gstack-devex-review", "gstack-plan-devex-review", "ui-ux-pro-max"]


def test_claudeai_adi():
    assert kz.claudeai_adi("ui-ux-pro-max", GIRIS) == "ui-ux-pro-max"
    assert kz.claudeai_adi("devex-review", GIRIS) == "gstack-devex-review"  # gstack-plan-devex-review: önek tek parça değil
    assert kz.claudeai_adi("yok", GIRIS) is None


def test_zip_ad_claudeai(tmp_path):
    sk = tmp_path / "devex-review"
    sk.mkdir()
    (sk / "SKILL.md").write_text("---\nname: devex-review\ndescription: d\n---\ngovde\n", encoding="utf-8")
    z = kz.zip_yap({"ad": "devex-review", "bolunmus": sk, "aciklama": ""}, tmp_path, "gstack-devex-review")
    assert z.name == "gstack-devex-review.zip"
    with zipfile.ZipFile(z) as zf:
        assert zf.namelist() == ["gstack-devex-review/SKILL.md"]
        assert "name: gstack-devex-review\n" in zf.read("gstack-devex-review/SKILL.md").decode()
