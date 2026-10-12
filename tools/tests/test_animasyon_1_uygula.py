"""onay/animasyon_1_uygula.py: uygula kopyalar ve eskiyi yedekler, --geri eski hâle döndürür."""
import importlib.util
from pathlib import Path

YOL = Path(__file__).resolve().parents[2] / "onay" / "animasyon_1_uygula.py"
spec = importlib.util.spec_from_file_location("animasyon_1_uygula", YOL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_uygula_geri_yeni(tmp_path):
    m.uygula(ev=tmp_path)
    hedef = tmp_path / ".claude" / "skills" / m.AD
    assert (hedef / "SKILL.md").is_file() and not list(hedef.rglob("__pycache__"))
    m.geri(ev=tmp_path)
    assert not hedef.exists()


def test_uygula_geri_eski(tmp_path):
    hedef = tmp_path / ".claude" / "skills" / m.AD
    hedef.mkdir(parents=True)
    (hedef / "eski.txt").write_text("e")
    m.uygula(ev=tmp_path)
    assert not (hedef / "eski.txt").exists()
    m.geri(ev=tmp_path)
    assert (hedef / "eski.txt").read_text() == "e" and not (hedef / "SKILL.md").exists()
