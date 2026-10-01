"""BLENDER-SKILL K8: blender-uretim references/*.py bpy_kontrol'den temiz · gerçek Blender'da boş sahnede kurulur."""
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
REF = KOK / "skills" / "blender-uretim" / "references"
sys.path.insert(0, str(KOK / "tools"))
import blender_cli as bc  # noqa: E402
import blender_oturum as bo  # noqa: E402

blender = pytest.mark.skipif(not Path(bo.BLENDER).is_file(), reason="Blender yok")


@pytest.mark.parametrize("ad", ["isik_kur.py", "malzemeler.py"])
def test_bpy_kontrol_temiz(ad):
    r = subprocess.run([sys.executable, str(KOK / "tools" / "bpy_kontrol.py"), str(REF / ad)],
                       capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stdout + r.stderr


@blender
def test_isik_kur_bos_sahne():
    kod, s, _ = bc.calistir(REF / "isik_kur.py", zaman_asimi=300)
    assert kod == 0 and s["gecti"] and not s["hatalar"], s
    assert all(s["sonuc"][f"profil:{p}"]["dugum"] > 0 for p in ("urun", "cam", "ahsap", "kumas")), s


@blender
def test_malzemeler_bos_sahne():
    kod, s, _ = bc.calistir(REF / "malzemeler.py", zaman_asimi=300)
    assert kod == 0 and s["gecti"] and len(s["sonuc"]) == 9 and min(s["sonuc"].values()) > 0, s
