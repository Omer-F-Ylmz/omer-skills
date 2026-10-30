"""yayinci: slot ve kuru-koşu testi (ağ yok). python -I -m unittest tools/postiz/test_yayinci.py"""
import json, sys, tempfile, unittest, datetime as dt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import yayinci


class T(unittest.TestCase):
    def test_slot_bos_olani_secer_ve_10dk_sonrasi(self):
        a = yayinci.sonraki_slot("g", {})
        b = yayinci.sonraki_slot("g", {"slotlar": {"g": [a.isoformat()]}})
        self.assertGreater(b, a)
        self.assertGreater(a, dt.datetime.now(a.tzinfo) + dt.timedelta(minutes=9))
        self.assertIn(a.strftime("%H:%M"), yayinci.SLOT_ET)

    def test_kuru_ag_cagirmaz_ve_kuyruk_dosyasi_yazmaz(self):
        with tempfile.TemporaryDirectory() as d:
            k = Path(d) / "v1"; k.mkdir()
            (k / "video.mp4").write_bytes(b"x"); (k / "meta.json").write_text(json.dumps({"grup": "a"}))
            yayinci.istek = lambda *a, **kw: self.fail("ağ çağrıldı")
            yayinci.log = lambda *a, **kw: None
            yayinci.yayin(k, True, True, {"free-ai-drop": {"youtube": "1"}}, {})
            self.assertFalse((k / "POSTIZ-KUYRUK.json").exists())

    def test_hesapsiz_grup_atlanir(self):
        hatalar = []
        yayinci.log = lambda m, h=False: hatalar.append(h)
        with tempfile.TemporaryDirectory() as d:
            k = Path(d); (k / "meta.json").write_text(json.dumps({"grup": "b"}))
            yayinci.yayin(k, False, False, {}, {})
        self.assertEqual(hatalar, [True])


if __name__ == "__main__":
    unittest.main()
