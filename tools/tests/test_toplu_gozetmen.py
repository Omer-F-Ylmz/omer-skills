"""Toplu iş gözetmeni (tools/toplu_gozetmen.py): bitiş satırsız ölüm → en fazla 3 yeniden başlatma."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import toplu_gozetmen as tg  # noqa: E402


def _betik(tmp_path, govde):
    p = tmp_path / "is.py"
    p.write_text(govde, encoding="utf-8")
    return [sys.executable, str(p)]


def _kos(tmp_path, govde, **kw):
    log = tmp_path / "g.log"
    rc = tg.gozet(_betik(tmp_path, govde), str(log), bekle=0, ram_bekle=False, **kw)
    return rc, log.read_text(encoding="utf-8")


def test_temiz_bitis_tek_kosu(tmp_path):
    rc, log = _kos(tmp_path, "print('BITIS')")
    assert rc == 0 and log.count("DURUM basladi") == 1 and "DURUM bitti" in log


def test_bitis_satirsiz_olum_yeniden_baslar_uc_kez(tmp_path):
    rc, log = _kos(tmp_path, "print('x')")  # rc 0 ama BITIS yok → ölü sayılır
    assert rc != 0 and log.count("DURUM basladi") == 4 and "DURUM vazgecti" in log


def test_rc_hata_bir_kez_sonra_basari(tmp_path):
    isaret = tmp_path / "i"
    govde = f"import pathlib,sys\np=pathlib.Path(r'{isaret}')\nif p.exists(): print('BITIS')\nelse: p.write_text('1'); sys.exit(3)"
    rc, log = _kos(tmp_path, govde)
    assert rc == 0 and log.count("DURUM basladi") == 2 and "DURUM oldu rc=3" in log
