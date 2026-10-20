import sys
sys.path.insert(0, "tools/olcum"); sys.path.insert(0, "tools")
import ordu_olc as o
COZUM = ("import threading\nimport time\n\nclass Sinirli:\n    def __init__(self, sinir):\n        self.sinir = sinir\n        self.n = 0\n        self._k = threading.Lock()\n\n"
         "    def al(self):\n        with self._k:\n            if self.n < self.sinir:\n                time.sleep(0)\n                self.n += 1\n                return True\n            return False\n")
dogru = o.GOREV["I1"][1]
print("kilitli:", [bool(dogru(COZUM)) for _ in range(6)])
print("kilitsiz (kırmızı beklenir):", [bool(dogru(o.SINIRLI)) for _ in range(3)])
