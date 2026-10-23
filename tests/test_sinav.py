import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools" / "ogrenme"))
import sinav as s


class SinavTest(unittest.TestCase):
    def test_senaryolar_tekil_ve_sinirli(self):
        log = Path(tempfile.mkdtemp()) / "l.log"
        log.write_text("10:00:00 DUR a hâlâ eksik: x\n10:01:00 DUR b hâlâ eksik: x\n10:02:00 DUR c rtk proxy grep yavaş\n10:03:00 BAŞLAT d\n", encoding="utf-8")
        r = s.senaryolar(5, log, [{"hata": True, "arac": "Bash", "tur": "arac", "ozet": "boru kopt"}])
        self.assertEqual([x["is"] for x in r], ["Bash", "c", "b"])
        self.assertEqual(len(s.senaryolar(1, log)), 1)

    def test_ders_secimi_yalniz_elenmemis_ve_ortak_kelime(self):
        sen = {"is": "x", "neden": "rtk proxy grep yavaş"}
        on = [{"metin": "proxy grep yerine Grep aracı", "durum": "kural"}, {"metin": "proxy grep", "durum": "elendi"}, {"metin": "alakasız cümle", "durum": "kural"}]
        self.assertEqual(s.secili_dersler(sen, on), ["proxy grep yerine Grep aracı"])

    def test_sinav_dersli_derssiz_fark(self):
        def sor(tur, istem, mt, **kw):
            if tur == "hakem":
                return ("2" if "ZZ" in istem else "0"), "m/x"
            return ("plan ZZ" if "Öğrenilmiş" in istem else "plan"), "m/x"
        sens = [{"is": "a", "neden": "grep yavaş"}, {"is": "b", "neden": "başka"}]
        sonuc = s.sinav(sens, [{"metin": "grep yavaş değil Grep", "durum": "kural"}], sor)
        o = s.ozet(sonuc)
        self.assertEqual((o["dersli_olculen"], o["ortalama_fark"], o["iyilesen"]), (1, 2.0, 1))

    def test_model_yoksa_puansiz(self):
        sonuc = s.sinav([{"is": "a", "neden": "n"}], [], lambda *a, **k: (None, None))
        self.assertEqual(s.ozet(sonuc)["puansiz"], 1)


if __name__ == "__main__":
    unittest.main()
