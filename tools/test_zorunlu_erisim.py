"""AJAN-TAM-YETKI-1: zorunlu liste yalnız erişilebilir araçları dayatır; claude-mem MCP tanımı KAYNAK'ta. Koşu: python -m unittest tools/test_zorunlu_erisim.py"""
import sys
import unittest
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / ".kos/kopru"))
import mcp_profil  # noqa: E402
import zorunlu_arac  # noqa: E402


class Erisim(unittest.TestCase):
    def test_olmayan_cli_erisim_yok(self):
        self.assertTrue(zorunlu_arac.erisim_yok({"ad": "supabase-yok-cli-xyz", "tur": "cli"}))

    def test_var_olan_cli_erisilebilir(self):
        self.assertFalse(zorunlu_arac.erisim_yok({"ad": "python", "tur": "cli"}))

    def test_npm_paketi_ve_skill_denetlenmez(self):
        self.assertFalse(zorunlu_arac.erisim_yok({"ad": "@scope/yok-paket", "tur": "cli"}))
        self.assertFalse(zorunlu_arac.erisim_yok({"ad": "supabase-yok-xyz", "tur": "skill"}))

    def test_claude_mem_mcp_tanimi_kaynakta(self):
        self.assertIn("mcp-search", mcp_profil.tanimlar())


if __name__ == "__main__":
    unittest.main()
