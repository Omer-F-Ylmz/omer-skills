"""kurulum_v1_d2_tara.run: zaman aşımında torun süreç de ölmeli, çağrı süresinde dönmeli.
Betik üst düzey sys.argv okuduğundan run() kaynak diliminden yüklenir.
Çalıştır: python -I -m unittest .kos/kopru/ogren/test_kurulum_v1_d2_tara.py"""
import os, subprocess, sys, time, unittest
from pathlib import Path

KAYNAK = Path(__file__).with_name("kurulum_v1_d2_tara.py").read_text(encoding="utf-8")
DILIM = KAYNAK[KAYNAK.index("def run("):KAYNAK.index("def say(")]
# torun süreç stdout borusunu miras alıp 40 sn uyur; ana süreç de uyur
TORUNLU = ("import subprocess,sys,time;"
           "subprocess.Popen([sys.executable,'-c','import time;time.sleep(40)']);time.sleep(40)")


class ZamanAsimi(unittest.TestCase):
    def test_torunlu_surec_zaman_asiminda_doner(self):
        g = {"subprocess": subprocess, "ENV": dict(os.environ)}
        exec(DILIM, g)
        t0 = time.time()
        kod, cikti = g["run"]([sys.executable, "-c", TORUNLU], 3)
        self.assertLess(time.time() - t0, 15)
        self.assertEqual(kod, -1)
        self.assertIn("ZAMAN AŞIMI", cikti)


if __name__ == "__main__":
    unittest.main()
