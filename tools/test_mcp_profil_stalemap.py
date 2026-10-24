"""STALEMAP-KUR-2: JS/TS işlerinde ajan MCP profiline stalemap eklenir. Koşu: python -m unittest tools/test_mcp_profil_stalemap.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import mcp_profil  # noqa: E402


class StalemapProfil(unittest.TestCase):
    def test_js_ts_isi_stalemap_secer(self):
        for metin in ("package.json olan Next.js projesinde TypeScript düzelt", "npm bağımlılığını yükselt", "tsx bileşeni yaz"):
            self.assertIn("stalemap", mcp_profil.sec(metin), metin)

    def test_dotnet_python_isi_secmez(self):
        self.assertIn("stalemap", mcp_profil.sec("C# dotnet servisini düzelt"))  # AJAN-TAM-YETKI-1: stalemap artık her zaman açık (TEMEL)

    def test_tanim_npx_sabit_surum(self):
        t = mcp_profil.tanimlar()["stalemap"]
        self.assertEqual(t["args"], ["-y", "stalemap@0.4.1", "mcp"])


if __name__ == "__main__":
    unittest.main()
