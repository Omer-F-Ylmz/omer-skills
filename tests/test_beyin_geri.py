import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import beyin_dusun as b
import arka_ajan
from test_beyin_dusun import Taban

RG = ["Metin aramaları için `rg` kullan, `grep -r` yerine sınırlı dosya/sonuç sayısı belirleyerek",
      "grep yerine rg kullan, sınırlı dosya/sonuç sayısı belirle.",
      "grep yerine `rg --max-count=1` ile sınırlı arama yap, dosya/sonuç sınırını `head -n 5` ile",
      "`rg` (ripgrep) kullanarak `grep -r` yerine hızlı kod araması yapın.",
      "Dosya aramaları için grep yerine `rg` (ripgrep) kullan, daha az CPU ve RAM tüketir",
      "`grep -r` yerine `rg` kullan, çıktı ve dosya sınırı ekle"]


def oneri(i, metin, durum="kural", destek=3, tetik="t"):
    return {"id": str(i), "metin": metin, "tetik": tetik, "tur": "", "kural": False, "durum": durum, "destek": destek,
            "kaynaklar": ["a"], "olusma": 0, "deneme": 0, "sebep": "", "gecmis": []}


class GeriTaban(Taban):
    def setUp(self):
        super().setUp()
        d = b.OLAY.parent
        self.eski2 = {k: getattr(b, k, None) for k in ("ALARM", "OZET", "DESKTOP", "KASA", "TEKRAR", "IMZA", "KONTROL")}
        b.ALARM, b.OZET, b.DESKTOP, b.KASA = d / "alarm.txt", d / "ozet.md", d / "desktop.jsonl", d / "kasa"
        b.TEKRAR, b.IMZA, b.KONTROL = d / "tekrar.jsonl", d / "imza.json", d / "kontrol.md"

    def tearDown(self):
        for k, v in self.eski2.items():
            setattr(b, k, v)
        super().tearDown()


class Tekil(GeriTaban):
    def test_alti_rg_kurali_tek_gruba(self):
        g = b.tekillestir(RG + ["Rapor birleştirmeden önce satır aralıklarını karşılaştır"])
        self.assertEqual(sorted(s for _, s in g), [1, 6])

    def test_ozet_tek_rg_satiri_sayacli_ve_kapsam_artar(self):
        farkli = ["Paralel koş zamandan kazan", "Küçük işte haiku modeli seç", "Dosya yazmadan önce yolu doğrula", "Commit öncesi testi çalıştır"]
        b._oneri_yaz([oneri(i, m, destek=9 - i) for i, m in enumerate(RG)] + [oneri(10 + i, m, destek=2) for i, m in enumerate(farkli)])
        b.ozet_yaz()
        satir = b.OZET.read_text(encoding="utf-8").splitlines()
        kural = [s for s in satir if s.startswith("KURAL:")]
        self.assertEqual(sum("rg" in s.split() or "`rg`" in s for s in kural), 1)
        self.assertTrue(any("×6" in s for s in kural))
        self.assertEqual(len(kural), 5)
        self.assertLessEqual(len(satir), 20)


class Geri(GeriTaban):
    def test_geri_oku_ozet_ders_ve_ilgisizi_atlar(self):
        (b.KASA / "50-dersler").mkdir(parents=True)
        (b.KASA / "50-dersler" / "parfum-ajan-dersi.md").write_text("# Parfüm ajan dersi\nParfüm ajanı görsel üretiminde önce şablonu kopyala\n", encoding="utf-8")
        (b.KASA / "50-dersler" / "baska.md").write_text("# Muhasebe\nFatura numarası kontrolü\n", encoding="utf-8")
        b.OZET.write_text("BEYİN ÖZETİ x\nKURAL: bir kural\n", encoding="utf-8")
        m = b.geri_oku("parfum görsel üretimi yap", "parfum-ajan-2")
        self.assertIn("BEYİN ÖZETİ", m)
        self.assertIn("şablonu kopyala", m)
        self.assertNotIn("Fatura", m)

    def test_geri_oku_bos_ise_bos_ve_tavanli(self):
        self.assertEqual(b.geri_oku("x", "y"), "")
        b.OZET.write_text("\n".join("KURAL: " + "k" * 100 for _ in range(60)), encoding="utf-8")
        self.assertLessEqual(len(b.geri_oku("x", "y")), 2500)

    def test_arka_ajan_gorevin_basina_ekler(self):
        b.OZET.write_text("BEYİN ÖZETİ x\n", encoding="utf-8")
        eski = arka_ajan.geri_oku
        arka_ajan.geri_oku = lambda g, a: b.geri_oku(g, a)
        try:
            m = arka_ajan.girdi({"gorev": "İŞ METNİ", "max_turns": 7}, "is1")
        finally:
            arka_ajan.geri_oku = eski
        self.assertTrue(m.index("BEYİN ÖZETİ") < m.index("İŞ METNİ"))
        self.assertTrue(m.endswith("En fazla 7 tur kullan."))

    def test_kontrol_dosyasi_kisa(self):
        b._oneri_yaz([oneri(i, f"Ayrı kural numarası {i} konusu {chr(97 + i) * 6}") for i in range(10)])
        b.ozet_yaz()
        self.assertTrue(b.KONTROL.exists())
        self.assertLessEqual(len(b.KONTROL.read_text(encoding="utf-8").splitlines()), 10)


class Tekrar(GeriTaban):
    def _tekrar(self):
        return [json.loads(s) for s in b.TEKRAR.read_text(encoding="utf-8").splitlines()] if b.TEKRAR.exists() else []

    def test_ikinci_hata_kaynak_ve_kacirilan_dersi_yazar(self):
        b._oneri_yaz([oneri(1, "pytest öncesi venv etkinleştir", tetik="pytest venv modül")])
        b.olay("arac", "Bash", "pytest tests/x.py exit code 1 ModuleNotFoundError", True, "alt-ajan")
        self.assertEqual(self._tekrar(), [])
        b.olay("arac", "Bash", "pytest tests/x.py exit code 1 ModuleNotFoundError", True, "kopru-ajani")
        t = self._tekrar()
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0]["kaynak"], "kopru-ajani")
        self.assertEqual(t[0]["onceki_kaynak"], "alt-ajan")
        self.assertIn("venv", t[0]["ders"])

    def test_sayi_farki_ayni_imza(self):
        b.olay("arac", "Bash", "pytest 12 FAILED", True)
        b.olay("arac", "Bash", "pytest 7 FAILED", True)
        self.assertEqual(len(self._tekrar()), 1)

    def test_hatasiz_olay_kaydedilmez(self):
        b.olay("arac", "Bash", "ls", False)
        b.olay("arac", "Bash", "ls", False)
        self.assertEqual(self._tekrar(), [])

    def test_gosterge_canli_tekrar(self):
        b.olay("arac", "Bash", "rc=2 derleme", True)
        b.olay("arac", "Bash", "rc=2 derleme", True)
        self.assertIn("canlı tekrar 1", b.gosterge([], b._olay_oku(0)[0]))


if __name__ == "__main__":
    unittest.main()
