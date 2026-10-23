import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools" / "ogrenme"))
import yansit as y  # noqa: E402


OLAYLAR = [
    {"t": 100, "tur": "arac", "arac": "Bash", "ozet": "pytest koştu", "hata": False},
    {"t": 101, "tur": "arac", "arac": "Bash", "ozet": "pytest koştu", "hata": True},
    {"t": 102, "tur": "maliyet", "arac": "", "ozet": "iş $0.91 model x", "hata": False},
]


class Ozet(unittest.TestCase):
    def test_sayilar_ve_hata_satiri(self):
        m = y.ozet_metni(OLAYLAR)
        self.assertIn("3 olay", m)
        self.assertIn("1 hata", m)
        self.assertIn("pytest koştu", m)
        self.assertIn("iş $0.91", m)

    def test_bos_olay(self):
        self.assertIn("0 olay", y.ozet_metni([]))


class Yansit(unittest.TestCase):
    def test_ucretsiz_model_yoksa_deterministik_kalir(self):
        m = y.yansit(OLAYLAR, sor=lambda tur, istem, n: (None, None))
        self.assertIn("3 olay", m)
        self.assertNotIn("DERS:", m)

    def test_model_yaniti_derse_eklenir(self):
        m = y.yansit(OLAYLAR, sor=lambda tur, istem, n: ("- pytest tekrarını azalt", "ollama/yerel"))
        self.assertIn("DERS: - pytest tekrarını azalt", m)


class Yaz(unittest.TestCase):
    def test_gunluk_ve_yama_dosyasi_yazilir(self):
        d = Path(tempfile.mkdtemp())
        y.yaz("metin", d / "icgoru" / "2026-10-23.md", d / "yama.md")
        self.assertEqual((d / "icgoru" / "2026-10-23.md").read_text(encoding="utf-8"), "metin\n")
        self.assertTrue((d / "yama.md").exists())


if __name__ == "__main__":
    unittest.main()
