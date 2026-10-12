"""BLENDER-2 onay betiği: önkoşul denetimi (yerel kapı + uzak sürüm) ve zip'lerin temizliği."""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "onay"))
import blender_2_uygula as u  # noqa: E402


def test_onkosul_tamam():
    assert u.onkosul(KOK, uzak_surum=u.YENI) == []


def test_onkosul_eksikler(tmp_path):
    (tmp_path / "tools" / "blender").mkdir(parents=True)
    (tmp_path / "tools" / "blender" / "yalin.py").write_text("eski", encoding="utf-8")
    eksik = u.onkosul(tmp_path, uzak_surum="1.0.0")
    assert len(eksik) == 2 and "birleşme" in eksik[0] and "push" in eksik[1]


def test_zipler_temiz(tmp_path, monkeypatch):
    monkeypatch.setattr(u, "DIST", tmp_path)
    z = u.zipler()
    assert len(z) == 2 and set(z.values()) == {"TEMİZ"}
