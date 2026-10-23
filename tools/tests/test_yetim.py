import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".kos", "kopru"))
import yetim

S = 100000.0
YONETICI = r'"C:\Python312\pythonw.exe" "C:\Projeler\omer-skills\.kos\kopru\yonetici_gorev.py"'


def p(pid, ppid, name, cmd="", create=1000.0):
    return {"ProcessId": pid, "ParentProcessId": ppid, "Name": name, "WorkingSetSize": 1 << 20, "T": create, "Cmd": cmd}


class YetimYonetici(unittest.TestCase):
    """YONETICI-OLUM-3: Görev Zamanlayıcı'dan koşan yönetici (svchost → ölü atası) ≥30 dk'da yetim sanılıp öldürülüyordu."""

    def tablo(self, cmd):
        return {2240: p(2240, 1584, "svchost.exe"), 500: p(500, 2240, "pythonw.exe", YONETICI if cmd else "")}

    def test_yonetici_yetim_degil(self):
        self.assertEqual([x[0]["ProcessId"] for x in yetim.yetimler(self.tablo(True), simdi=S)], [])

    def test_komutsuz_ayni_surec_hala_yetim(self):
        self.assertEqual([x[0]["ProcessId"] for x in yetim.yetimler(self.tablo(False), simdi=S)], [500])


if __name__ == "__main__":
    unittest.main()
