import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import beyin_kanca


class Yeni(unittest.TestCase):
    def test_yalniz_kasada_olmayan_gecerli_olgun_dosya(self):
        d = Path(tempfile.mkdtemp())
        eski, yeni, bos, taze = (d / n for n in ("eski.json", "yeni.json", "bos.json", "taze.json"))
        for p in (eski, yeni, taze):
            p.write_text('{"result": "x"}', encoding="utf-8")
        bos.write_text("", encoding="utf-8")
        durum = d / "durum.json"
        durum.write_text(json.dumps({str(eski): {"sha": "1"}}), encoding="utf-8")
        simdi = taze.stat().st_mtime + 5  # taze: bekleme süresinden genç
        for p in (eski, yeni, bos):
            import os
            os.utime(p, (simdi - 100, simdi - 100))
        self.assertEqual(beyin_kanca.yeni(d, durum, simdi), [yeni])


if __name__ == "__main__":
    unittest.main()
