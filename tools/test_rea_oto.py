import os, sys, unittest
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rea_oto


class ParcaliGerek(unittest.TestCase):
    def test_oom_cikisi_parcali_ister(self):
        self.assertTrue(rea_oto.parcali_gerek({"cevap_var": False, "rea_cikis": 134, "ram_bekci_durdurdu": False}))

    def test_ram_bekcisi_durdurduysa_parcali_ister(self):
        self.assertTrue(rea_oto.parcali_gerek({"cevap_var": False, "rea_cikis": 1, "ram_bekci_durdurdu": True}))

    def test_cevap_geldiyse_parcali_istemez(self):
        self.assertFalse(rea_oto.parcali_gerek({"cevap_var": True, "rea_cikis": None, "ram_bekci_durdurdu": False}))

    def test_cevapsiz_ama_oom_degil_parcali_istemez(self):
        # zaman aşımı/bağlantı hatası parçalı modla çözülmez; sahte düşüş olmasın
        self.assertFalse(rea_oto.parcali_gerek({"cevap_var": False, "rea_cikis": None, "ram_bekci_durdurdu": False}))


if __name__ == "__main__":
    unittest.main()
