import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import gpu_sinir  # noqa: E402


class Karar(unittest.TestCase):
    def test_askiya_sayaci(self):
        d = gpu_sinir.yeni_durum()
        sonuc = [gpu_sinir.karar(d, u) for u in (50, 99, 99, 60, 60)]
        self.assertTrue(sonuc[1])  # tek 99 tepesi anında askıya alır
        self.assertEqual(d["askiya"], sum(sonuc))
        self.assertGreaterEqual(d["askiya"], 1)
        self.assertEqual(d["tepe"], 99)

    def test_alt_esikte_birakir(self):
        d = gpu_sinir.yeni_durum()
        gpu_sinir.karar(d, 99)
        for _ in range(3):
            gpu_sinir.karar(d, 10)
        self.assertFalse(d["sinirda"])

    def test_sayac_dosyaya_yazilir(self):
        d = gpu_sinir.yeni_durum()
        gpu_sinir.karar(d, 99)
        with tempfile.TemporaryDirectory() as t:
            yol = os.path.join(t, "sayac.json")
            gpu_sinir.sayac_yaz(d, yol)
            import json
            with open(yol, encoding="utf-8") as f:
                self.assertEqual(json.load(f)["askiya"], d["askiya"])


if __name__ == "__main__":
    unittest.main()
