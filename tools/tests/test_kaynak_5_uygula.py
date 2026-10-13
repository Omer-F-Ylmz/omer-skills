import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "onay"))
import kaynak_5_uygula as k  # noqa: E402


def test_uygula_idempotent_geri(tmp_path):
    s = k.EKLE[0][0]
    shutil.copytree(KOK / "skills" / s, tmp_path / "skills" / s)
    shutil.copytree(KOK / "tools" / "skill-paket", tmp_path / "tools" / "skill-paket")
    f = tmp_path / "skills" / s / "SKILL.md"
    k.geri(tmp_path, tmp_path)
    assert k.plan(tmp_path) == [(s, False)]
    assert k.uygula(tmp_path, tmp_path) and k.uygula(tmp_path, tmp_path)  # zip TEMİZ, MCP önce=sonra
    assert f.read_text(encoding="utf-8").count(k.EKLE[0][1]) == 1
    assert (tmp_path / "dist" / "kaynak-5" / "kendi" / f"{s}.zip").exists()
    k.geri(tmp_path, tmp_path)
    assert k.plan(tmp_path) == [(s, False)]
