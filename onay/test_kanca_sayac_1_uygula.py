"""KANCA-SAYAÇ-1 onay betiği: kuru dokunmaz, uygula yedekler + kopyalar, --geri geri koyar."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import kanca_sayac_1_uygula as k  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    kaynak, hedef = tmp_path / "yeni.py", tmp_path / "cagri_sayac.py"
    kaynak.write_text("yeni", encoding="utf-8")
    hedef.write_text("eski", encoding="utf-8")
    yedek = tmp_path / ("cagri_sayac.py" + k.YEDEK)
    assert k.main([], kaynak, hedef) == 0 and hedef.read_text() == "eski" and not yedek.exists()
    assert k.main(["uygula"], kaynak, hedef) == 0
    assert hedef.read_text() == "yeni" and yedek.read_text() == "eski"
    assert k.main(["uygula"], kaynak, hedef) == 0 and yedek.read_text() == "eski"
    assert k.main(["--geri"], kaynak, hedef) == 0 and hedef.read_text() == "eski" and not yedek.exists()
    assert k.main(["--geri"], kaynak, hedef) == 1
