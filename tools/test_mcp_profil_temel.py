"""AJAN-TAM-YETKI-1: her ajan profili her zaman açık çok yönlüleri içerir. Koşu: python -m unittest tools/test_mcp_profil_temel.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import mcp_profil  # noqa: E402

HER_ZAMAN = ["ruflo", "rea", "playwright", "headroom", "context7", "brave-search", "stalemap"]


class TemelProfil(unittest.TestCase):
    def test_bos_gorev_her_zaman_acik_listeyi_icerir(self):
        for m in HER_ZAMAN:
            self.assertIn(m, mcp_profil.sec("C# dotnet servisini düzelt"), m)

    def test_tanimi_olanlar_yazilir(self):
        t = mcp_profil.tanimlar()
        for m in ("ruflo", "rea", "playwright", "headroom", "context7", "brave-search", "stalemap"):
            self.assertIn(m, t, m)


if __name__ == "__main__":
    unittest.main()
