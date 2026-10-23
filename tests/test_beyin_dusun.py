import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import beyin_dusun as b


class Taban(unittest.TestCase):
    def setUp(self):
        d = Path(tempfile.mkdtemp())
        self.eski = {k: getattr(b, k) for k in ("OLAY", "DURUM", "KOTA", "ONERI", "BESLEME", "IS_KAYDI", "ICGORU", "ONERILER", "ONAY", "KILIT", "KART", "LIMIT", "_havuz", "_kurallar", "_ollama", "ETKI", "_ram", "_derin_kaynak")}
        b.OLAY, b.DURUM, b.KOTA, b.ONERI, b.BESLEME = (d / n for n in ("olay.jsonl", "durum.json", "kota.json", "oneri.jsonl", "besleme.jsonl"))
        b.IS_KAYDI, b.ICGORU, b.ONERILER, b.ONAY, b.KILIT, b.KART = d / "is.tsv", d / "icgoru", d / "oneriler.md", d / "onay.md", d / "kilit", d / "kart.md"
        b.LIMIT = {p: 100 for p in b.SIRA}
        b._ram = lambda: 10
        b._derin_kaynak = lambda: "kaynak"
        b._kurallar = lambda: []
        self.cagrilar = []
        self.yanit = "[]"
        b._havuz = self._sahte

    def _sahte(self, tur, istem, **kw):
        self.cagrilar.append((tur, kw))
        return self.yanit, f"{kw.get('saglayici', 'x')}/m", []

    def tearDown(self):
        for k, v in self.eski.items():
            setattr(b, k, v)


class Olay(Taban):
    def test_olay_yazar_sirri_atlar(self):
        self.assertTrue(b.olay("arac", "Bash", "pytest -q", False))
        self.assertFalse(b.olay("arac", "Bash", "export password=hunter2xyz", False))
        satirlar = b.OLAY.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(satirlar), 1)
        self.assertEqual(json.loads(satirlar[0])["arac"], "Bash")

    def test_kanca_hata_isaretler(self):
        b.kanca({"hook_event_name": "PostToolUse", "tool_name": "Bash", "tool_input": {"command": "pytest"},
                 "tool_response": {"stderr": "Traceback (most recent call last)", "is_error": True}})
        j = json.loads(b.OLAY.read_text(encoding="utf-8").splitlines()[0])
        self.assertTrue(j["hata"])
        self.assertEqual(j["arac"], "Bash")


class Kota(Taban):
    def test_esik_asilinca_siradakine_gecer(self):
        b.LIMIT["gemini"] = 10
        for _ in range(8):
            b._kota_ekle("gemini")  # %80
        b.KOTA.write_text(b.KOTA.read_text(encoding="utf-8").replace('"son": "gemini"', '"son": "openrouter"'), encoding="utf-8")  # sıra başa dönsün
        self.assertEqual(b.siradaki(), "groq")

    def test_hepsi_doluysa_none(self):
        for p in b.SIRA:
            for _ in range(80):
                b._kota_ekle(p)
        self.assertIsNone(b.siradaki())

    def test_donusumlu_sira(self):
        a = b.siradaki(); b._kota_ekle(a, 1)
        c = b.siradaki()
        self.assertNotEqual(a, c)


class Tur(Taban):
    def test_olay_yoksa_atlar(self):
        self.assertEqual(b.tur(), "atla")
        self.assertEqual(self.cagrilar, [])

    def test_ram_yuksekse_uzak_havuz_koşar_yerel_ollama_açılmaz(self):
        b.olay("arac", "Bash", "x", False)
        b._ram = lambda: 85
        self.assertEqual(b.tur(), "ok")  # uzak ücretsiz havuz RAM yemez: döngü RAM yüzünden durmaz
        b.olay("arac", "Bash", "y", False)
        b.LIMIT = {p: 0 for p in b.SIRA}
        self.ollama_cagri = []
        b._ollama = lambda istem, mt: self.ollama_cagri.append(1)
        b._havuz = lambda tur, istem, **kw: (None, None, [])  # tüm bulut havuzu da dolu: yerel son çare ama RAM yüksek
        self.assertEqual(b.tur(), "kota-dolu")
        self.assertEqual(self.ollama_cagri, [])  # RAM yüksekken Ollama açılmaz

    def test_olaylar_tek_istekte_oneri_olur(self):
        for i in range(5):
            b.olay("arac", "Bash", f"komut {i}", i == 2)
        self.yanit = json.dumps([{"tur": "hata", "oneri": "Testi koşmadan bitti deme", "tetik": "test bitirme rapor", "kural": False}])
        self.assertEqual(b.tur(), "ok")
        self.assertEqual(len(self.cagrilar), 1)
        self.assertIn("saglayici", self.cagrilar[0][1])
        o = b.oneri_oku()
        self.assertEqual(len(o), 1)
        self.assertEqual(o[0]["durum"], "taslak")
        self.assertEqual(b.tur(), "atla")  # ofset ilerledi, aynı olaylar tekrar işlenmez

    def test_kota_sayaci_artar(self):
        b.olay("arac", "Bash", "x", False)
        b.tur()
        self.assertEqual(sum(v[0] for v in json.loads(b.KOTA.read_text(encoding="utf-8"))["p"].values()), 1)


class Oneri(Taban):
    def test_tekrar_destek_artirir_ikinci_kez_deneniyor(self):
        o = {"tur": "hata", "oneri": "Testi koşmadan bitti deme", "tetik": "test bitirme rapor", "kural": False}
        b.oneri_ekle(o, "a/m1")
        b.oneri_ekle(o, "b/m2")
        x = b.oneri_oku()
        self.assertEqual((len(x), x[0]["destek"], x[0]["durum"]), (1, 2, "deneniyor"))

    def test_kural_degistiren_onay_bekler_asla_otomatik(self):
        o = {"tur": "kalite", "oneri": "K2d kuralını kaldır, benzer üret", "tetik": "referans benzer üretim", "kural": True}
        for k in ("a/m1", "b/m2", "c/m3"):
            b.oneri_ekle(o, k)
        self.assertEqual(b.oneri_oku()[0]["durum"], "onay-bekliyor")
        b.yaz_oneriler()
        self.assertIn("K2d", b.ONAY.read_text(encoding="utf-8"))


class Kanit(Taban):
    def _is(self, satirlar):
        b.IS_KAYDI.write_text("zaman\tis\tefor\tdk\tadim\tagirlikli\tusd\tsonuc\tkalite\n" + "".join(
            f"{z}\t{i}\t-\t1\t1\t1\t{u}\t{s}\t-\n" for z, i, u, s in satirlar), encoding="utf-8")

    def test_iyilesen_kanitlandi_kotulesen_elendi(self):
        simdi = time.time()
        z = lambda dk: time.strftime("%Y-%m-%d %H:%M", time.localtime(simdi + dk * 60))  # noqa: E731
        b.oneri_ekle({"tur": "ucuz", "oneri": "Ucuz model dene", "tetik": "ucuz model", "kural": False}, "a/m")
        b.oneri_ekle({"tur": "ucuz", "oneri": "Ucuz model dene", "tetik": "ucuz model", "kural": False}, "b/m")
        o = b.oneri_oku()[0]
        o["olusma"] = simdi - 7200; b._oneri_yaz([o])
        # besleme: 3 iş bu öneriyle; her birinin ardından bir iş satırı
        besleme = [{"t": simdi + i * 600, "ids": [o["id"]]} for i in range(3)]
        b.BESLEME.write_text("".join(json.dumps(x) + "\n" for x in besleme), encoding="utf-8")
        # kıyas: öneri öncesi (çıkarılmış) işler 1.0$ ve 1 hata; önerili işler 0.4$ ve hatasız
        self._is([(z(-100), "e1", 1.0, "success"), (z(-90), "e2", 1.0, "fail"), (z(-80), "e3", 1.0, "success"),
                  (z(1), "y1", 0.4, "success"), (z(11), "y2", 0.4, "success"), (z(21), "y3", 0.4, "success")])
        b.kanitla()
        self.assertEqual(b.oneri_oku()[0]["durum"], "kanitlandi")
        # tersi: önerili işler pahalı ve hatalı
        o = b.oneri_oku()[0]; o["durum"] = "deneniyor"; b._oneri_yaz([o])
        self._is([(z(-100), "e1", 0.4, "success"), (z(-90), "e2", 0.4, "success"), (z(-80), "e3", 0.4, "success"),
                  (z(1), "y1", 1.0, "fail"), (z(11), "y2", 1.0, "success"), (z(21), "y3", 1.0, "fail")])
        b.kanitla()
        self.assertEqual(b.oneri_oku()[0]["durum"], "elendi")

    def test_yetersiz_ornekte_bekler(self):
        b.oneri_ekle({"tur": "ucuz", "oneri": "Ucuz model dene", "tetik": "ucuz model", "kural": False}, "a/m")
        b.oneri_ekle({"tur": "ucuz", "oneri": "Ucuz model dene", "tetik": "ucuz model", "kural": False}, "b/m")
        self._is([])
        b.kanitla()
        self.assertEqual(b.oneri_oku()[0]["durum"], "deneniyor")

    def test_elenen_duzeltilir_uc_denemeden_sonra_kalici(self):
        b.oneri_ekle({"tur": "ucuz", "oneri": "Ucuz model dene", "tetik": "ucuz model", "kural": False}, "a/m")
        for n in (1, 2, 3, 4):
            o = b.oneri_oku()[0]; o["durum"] = "elendi"; o["sebep"] = "pahalıya çıktı"; b._oneri_yaz([o])
            self.yanit = json.dumps({"oneri": f"Ucuz model dene v{n}", "tetik": "ucuz model"})
            b.duzelt()
            o = b.oneri_oku()[0]
            if n < 4:
                self.assertEqual((o["durum"], o["deneme"]), ("taslak", n))
            else:
                self.assertEqual(o["durum"], "kalici-elendi")
        self.assertEqual(len(self.cagrilar), 3)  # 4. elenişte düzeltme çağrısı yok: en fazla 3 yeniden deneme
        self.assertTrue(o["sebep"])


class Besleme(Taban):
    def _kanitli(self, metin, tetik, durum="kanitlandi", kural=False):
        b.oneri_ekle({"tur": "hata", "oneri": metin, "tetik": tetik, "kural": kural}, "a/m")
        o = b.oneri_oku(); o[-1]["durum"] = durum; b._oneri_yaz(o)

    def test_uyan_yoksa_bos(self):
        self._kanitli("Testi koş sonra bitir", "test bitirme rapor")
        self.assertEqual(b.satirlar("zeytin hasadı planı"), "")
        self.assertFalse(b.BESLEME.exists())

    def test_en_fazla_iki_madde_kisa(self):
        for m in ("Testi koş sonra bitir", "Raporu kanıtla teslim et", "Kodu küçük adımla yaz", "Çıktıyı sayıyla bildir"):
            self._kanitli(m, "test bitirme rapor kod")
        s = b.satirlar("kod test bitirme raporu yaz").splitlines()
        self.assertEqual(len(s), 2)
        self.assertTrue(all(len(x) <= 80 for x in s))
        self.assertEqual(len(b.BESLEME.read_text(encoding="utf-8").splitlines()), 1)

    def test_taslak_ve_onay_bekleyen_girmez(self):
        self._kanitli("A testi koş", "test bitirme rapor kod", durum="taslak")
        self._kanitli("B testi koş", "test bitirme rapor kod", durum="onay-bekliyor", kural=True)
        self.assertEqual(b.satirlar("kod test bitirme raporu yaz"), "")

    def test_kural_blogu_ile_ayni_onek(self):
        self._kanitli("Testi koş sonra bitir", "test bitirme rapor kod")
        import kural_uret
        self.assertIn("Testi koş sonra bitir", kural_uret.ilgili("kod test bitirme raporu yaz", kurallar=[("K0", "", [], "x")]))


class Kart(Taban):
    def test_kart_bos_oneride_bos_dolu_oneride_kisa(self):
        self.assertEqual(b.kart_metin(), "")
        b.oneri_ekle({"tur": "hata", "oneri": "Testi koş sonra bitir", "tetik": "test bitirme", "kural": False}, "a/m")
        o = b.oneri_oku(); o[0]["durum"] = "kanitlandi"; b._oneri_yaz(o)
        self.assertIn("Testi koş sonra bitir", b.kart_metin())
        self.assertLessEqual(len(b.kart_metin()) // 3, 150)


class Derin(Taban):
    def test_iki_aile_uyusursa_deneniyor_uyusmazsa_taslak(self):
        yanitlar = iter([json.dumps([{"tur": "ucuz", "oneri": "Hafif işte ucuz model seç", "tetik": "ucuz model seçim", "kural": False}]),
                         json.dumps([{"tur": "ucuz", "oneri": "Hafif işte ucuz model seç", "tetik": "ucuz model seçim", "kural": False},
                                     {"tur": "hiz", "oneri": "Paralel koş zamandan kazan", "tetik": "paralel hız", "kural": False}])])
        b._havuz = lambda tur, istem, **kw: (next(yanitlar), f"p{len(self.cagrilar)}/m", self.cagrilar.append(1) or [])
        b.derin()
        d = {x["metin"]: x["durum"] for x in b.oneri_oku()}
        self.assertEqual(d["Hafif işte ucuz model seç"], "deneniyor")
        self.assertEqual(d["Paralel koş zamandan kazan"], "taslak")
        self.assertTrue(any(b.ICGORU.glob("*.md")))


class Canli(Taban):
    """BEYIN-CANLI-1: herkes → beyin besleme, bekçi, kurala dönüş, ≤20 satır özet."""

    def setUp(self):
        super().setUp()
        d = b.OLAY.parent
        self.eski_canli = {k: getattr(b, k) for k in ("ALARM", "OZET", "DESKTOP", "_baslat")}
        b.ALARM, b.OZET, b.DESKTOP = d / "alarm.txt", d / "ozet.md", d / "desktop.jsonl"
        self.baslatildi = []
        b._baslat = lambda: self.baslatildi.append(1)

    def tearDown(self):
        for k, v in self.eski_canli.items():
            setattr(b, k, v)
        super().tearDown()

    def _olaylar(self):
        return [json.loads(s) for s in b.OLAY.read_text(encoding="utf-8").splitlines()]

    def test_is_olayi_alanlari(self):
        b.is_olayi("x-1", "haiku", 0.2, 3.0, True, {"num_turns": 4, "subtype": "success", "result": "tamam\nKalite: 3/3"})
        o = self._olaylar()[0]
        self.assertEqual(o["tur"], "is")
        for parca in ("x-1", "haiku", "$0.20", "KABUL", "Kalite: 3/3"):
            self.assertIn(parca, o["ozet"])
        self.assertFalse(o["hata"])

    def test_is_olayi_dur_ve_pahali(self):
        b.is_olayi("x-2", "opus", 1.4, 20.0, False, {"num_turns": 60, "usage": {"input_tokens": 10, "cache_read_input_tokens": 9000, "output_tokens": 5}})
        tur = [o["tur"] for o in self._olaylar()]
        self.assertEqual(tur, ["is", "maliyet"])
        o = self._olaylar()
        self.assertIn("DUR", o[0]["ozet"])
        self.assertTrue(o[0]["hata"])
        self.assertIn("tur", o[1]["ozet"])

    def test_ara_olay(self):
        b.ara_olay("x-3", 4.0)
        self.assertEqual((self._olaylar()[0]["tur"], self._olaylar()[0]["arac"]), ("ara", "x-3"))

    def test_bekci_olay_yok_alarm(self):
        b.olay("arac", "Bash", "eski")
        simdi = time.time() + 400
        _yaz = json.dumps({"tur_t": simdi - 10})
        b.DURUM.write_text(_yaz, encoding="utf-8")
        self.assertEqual(b.bekci(2, simdi), "alarm")
        self.assertIn("olay yok", b.ALARM.read_text(encoding="utf-8"))

    def test_bekci_taze_olay_sessiz(self):
        b.olay("arac", "Bash", "taze")
        b.DURUM.write_text(json.dumps({"tur_t": time.time()}), encoding="utf-8")
        self.assertEqual(b.bekci(2), "ok")
        self.assertFalse(b.ALARM.exists())

    def test_bekci_ajan_yoksa_olay_beklenmez(self):
        b.DURUM.write_text(json.dumps({"tur_t": time.time() + 3990}), encoding="utf-8")
        self.assertEqual(b.bekci(0, time.time() + 4000), "ok")

    def test_bekci_olu_dongu_yeniden_baslatir(self):
        b.DURUM.write_text(json.dumps({"tur_t": time.time() - 900}), encoding="utf-8")
        self.assertEqual(b.bekci(0), "alarm")
        self.assertEqual(self.baslatildi, [1])
        self.assertIn("döngü ölü", b.ALARM.read_text(encoding="utf-8"))

    def test_bekci_alarm_cozulunce_10_dk_sonra_temizlenir(self):
        b.ALARM.write_text("eski alarm\n", encoding="utf-8")
        t0 = b.ALARM.stat().st_mtime
        b.DURUM.write_text(json.dumps({"tur_t": t0 + 500}), encoding="utf-8")
        self.assertEqual(b.bekci(0, t0 + 300), "ok")  # sorun yok ama alarm 10 dk kalır (Desktop görsün)
        self.assertTrue(b.ALARM.exists())
        self.assertEqual(b.bekci(0, t0 + 601), "ok")
        self.assertFalse(b.ALARM.exists())

    def test_kurala_cevir(self):
        def oneri(metin, tetik, destek, durum="deneniyor", gecmis=()):
            return {"id": metin[:3], "metin": metin, "tetik": tetik, "tur": "", "kural": False, "durum": durum, "destek": destek, "kaynaklar": ["a/x"],
                    "olusma": 0, "deneme": 0, "sebep": "", "gecmis": list(gecmis)}
        b._oneri_yaz([oneri("Hafif işte ucuz model seç", "ucuz model", 3), oneri("Az destekli öneri metni", "az destek", 2),
                      oneri("Çelişkili öneri metni", "çelişki var", 4, gecmis=[{"metin": "m", "sebep": "s"}]),
                      oneri("Kural değiştiren öneri", "kural değişir", 5, durum="onay-bekliyor")])
        self.assertEqual(b.kurala_cevir(), 1)
        d = {x["metin"]: x["durum"] for x in b.oneri_oku()}
        self.assertEqual([d["Hafif işte ucuz model seç"], d["Az destekli öneri metni"], d["Çelişkili öneri metni"]], ["kural", "deneniyor", "deneniyor"])
        self.assertEqual(d["Kural değiştiren öneri"], "onay-bekliyor")

    def test_ozet_en_cok_20_satir(self):
        b._oneri_yaz([{"id": str(i), "metin": f"Kural cümlesi numara {i}", "tetik": "t", "tur": "", "kural": False, "durum": "kural", "destek": 3,
                       "kaynaklar": ["a"], "olusma": 0, "deneme": 0, "sebep": "", "gecmis": []} for i in range(30)])
        for i in range(30):
            b.olay("maliyet", f"is{i}", "pahalı iş")
        b.ALARM.write_text("alarm var", encoding="utf-8")
        b.ozet_yaz()
        satir = b.OZET.read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(satir), 20)
        self.assertTrue(any("alarm var" in s for s in satir))

    def test_desktop_notlari_olaya_dusar_bir_kez(self):
        b.DESKTOP.write_text(json.dumps({"t": "x", "kaynak": "desktop", "tur": "hata", "ozet": "beyin durmuştu", "ders": "canlılığı kontrol et"}) + "\n", encoding="utf-8")
        self.assertEqual(b.desktop_al(), 1)
        self.assertEqual(b.desktop_al(), 0)
        o = self._olaylar()[0]
        self.assertEqual(o["tur"], "desktop-hata")
        self.assertIn("canlılığı kontrol et", o["ozet"])

    def test_satirlar_kural_once(self):
        b._oneri_yaz([{"id": "k1", "metin": "Paralel koş zamandan kazan", "tetik": "paralel hız koş", "tur": "", "kural": False, "durum": "kural", "destek": 3,
                       "kaynaklar": ["a"], "olusma": 0, "deneme": 0, "sebep": "", "gecmis": []}])
        self.assertIn("Paralel koş", b.satirlar("paralel hız koş görevi"))



class Koc(Canli):
    """BEYIN-CANLI-1b: bozuk satır dayanıklılığı, Claude'suz, Ollama yedeği, koçluk, çelişki, geri çekme."""

    def setUp(self):
        super().setUp()
        b.ETKI = b.OLAY.parent / "etki.jsonl"
        self.ollama = []
        b._ollama = lambda istem, mt: self.ollama.append(istem) or "yerel yanıt"
        self.addCleanup(os.environ.pop, "BEYIN_DUSUN", None)  # calis() bunu açar

    def _kural(self, metin, tetik, durum="kural", destek=3, tur=""):
        return {"id": metin[:3], "metin": metin, "tetik": tetik, "tur": tur, "kural": False, "durum": durum, "destek": destek,
                "kaynaklar": ["a"], "olusma": 0, "deneme": 0, "sebep": "", "gecmis": []}

    def _etki_kur(self, ad, once, sonra):
        simdi = time.time()
        z = lambda dk: time.strftime("%Y-%m-%d %H:%M", time.localtime(simdi + dk * 60))  # noqa: E731
        o = self._kural(ad, "etki kural", durum="kural")
        o["olusma"] = simdi - 7200
        b._oneri_yaz([o])
        b.BESLEME.write_text("".join(json.dumps({"t": simdi + i * 600, "ids": [o["id"]]}) + "\n" for i in range(3)), encoding="utf-8")
        satir = [(z(-100 + 10 * i), f"e{i}", u, s) for i, (u, s) in enumerate(once)] + [(z(1 + 10 * i), f"y{i}", u, s) for i, (u, s) in enumerate(sonra)]
        b.IS_KAYDI.write_text("zaman\tis\tefor\tdk\tadim\tagirlikli\tusd\tsonuc\tkalite\n" + "".join(
            f"{zz}\t{i}\t-\t1\t1\t1\t{u}\t{s}\t-\n" for zz, i, u, s in satir), encoding="utf-8")
        return o

    def test_bozuk_olay_satiri_donguyu_cokertmez(self):
        b.olay("arac", "Bash", "ok")
        with b.OLAY.open("ab") as f:
            f.write(b'{"zaman": "2026-10-23", "olay": "ders", "konu": "X"}\n[1, 2]\n{"tur": "arac"}\n')
        olaylar, _ = b._olay_oku(0)
        self.assertEqual(len(olaylar), 2)
        self.assertTrue(all("tur" in o and "arac" in o and "hata" in o and "ozet" in o for o in olaylar))
        self.assertIn("olay", b._ozet_olay(olaylar))
        self.assertEqual(b.tur(), "ok")

    def test_dizgi_zaman_damgasi_gosterge_cokertmez(self):
        with b.OLAY.open("ab") as f:
            f.write(b'{"t": "2026-10-23", "tur": "ders", "konu": "X"}\n')
        olaylar, _ = b._olay_oku(0)
        self.assertEqual(olaylar[0]["t"], 0)
        self.assertIn("GÖSTERGE", b.gosterge([], olaylar))

    def test_calis_hatada_alarm_yazar_ve_tur_t_ilerler(self):
        def patla():
            raise RuntimeError("deneme")
        eski = b.tur
        b.tur = patla
        try:
            self.assertEqual(b.calis(), "hata")
        finally:
            b.tur = eski
        self.assertIn("RuntimeError", b.ALARM.read_text(encoding="utf-8"))
        self.assertIn("tur_t", b._json(b.DURUM, {}))

    def test_claude_yolu_yok(self):
        kaynak = Path(b.__file__).read_text(encoding="utf-8")
        for yasak in ("claude -p", '["claude"', "api.anthropic.com", "haiku_tavan=1", "haiku_tavan=2"):
            self.assertNotIn(yasak, kaynak)
        b.olay("arac", "Bash", "x")
        b.tur()
        b.kocluk_uret("is-1", "DUR · kalite düşük")
        self.assertTrue(self.cagrilar)
        self.assertTrue(all(kw.get("haiku_tavan", 0) == 0 for _, kw in self.cagrilar))

    def test_hepsi_doluysa_ollama_yerelde_claude_yok(self):
        b.LIMIT = {p: 0 for p in b.SIRA}  # hepsi %80 üstü
        b._havuz = lambda tur, istem, **kw: (None, None, [])  # HAVUZ-GENIS-2: önce tüm bulut havuzu denenir, boşsa yerel son çare
        self.assertEqual(b._sor("ozet", "soru", 100), ("yerel yanıt", "ollama/yerel"))
        self.assertEqual(self.cagrilar, [])

    def test_ollama_da_yoksa_bekler(self):
        b.LIMIT = {p: 0 for p in b.SIRA}
        b._ollama = lambda istem, mt: None
        b._havuz = lambda tur, istem, **kw: (None, None, [])  # bulut havuzu da boş
        self.assertEqual(b._sor("ozet", "soru", 100), (None, None))

    def test_kocluk_uret_ucretsiz_model_yazar(self):
        self.yanit = "Ben olsam önce testi koşardım, sonra commit ederdim."
        self.assertTrue(b.kocluk_uret("video-1", "DUR · eksik araç: markitdown"))
        o = [x for x in self._olaylar() if x["tur"] == "kocluk"]
        self.assertEqual(len(o), 1)
        self.assertIn("ucretsiz", o[0]["arac"])
        self.assertIn("testi koşardım", o[0]["ozet"])

    def test_kocluk_desktop_okuyucu_ve_oncelik(self):
        b.DESKTOP.write_text(json.dumps({"tur": "kocluk", "hedef": "test koş", "ozet": "Önce kırmızı testi gör", "ders": "kırmızıyı kanıtla"}) + "\n"
                             + json.dumps({"tur": "hata", "ozet": "x", "ders": "y"}) + "\n", encoding="utf-8")
        self.assertEqual(b.kocluk_oku(), 1)
        self.assertEqual(b.kocluk_oku(), 0)  # ofset ilerler
        b._oneri_yaz(b.oneri_oku() + [self._kural("Paralel koş zamandan kazan test", "test koş paralel", durum="kural", destek=9)])
        blok = b.satirlar("test koş kırmızı kanıtla işi")
        self.assertTrue(blok.splitlines()[0].startswith("- KOÇLUK"))

    def test_celiskili_ders_reddedilir(self):
        b._kurallar = lambda: ["K2h önce ücretsiz havuz kullan; Claude yalnız karar ve birleştirme"]
        self.yanit = "ÇELİŞİR"
        d, _ = b.oneri_ekle({"tur": "ucuz", "oneri": "Ağır işi doğrudan Claude ile yap ücretsiz havuzu atla", "tetik": "ağır iş ücretsiz havuz", "kural": False}, "a/m")
        self.assertEqual(d, "ret")
        self.assertEqual(b.oneri_oku(), [])
        self.assertIn("çelişki", " ".join(o["ozet"] for o in self._olaylar() if o["tur"] == "celiski"))
        self.yanit = "ÇELİŞMEZ"
        d, _ = b.oneri_ekle({"tur": "ucuz", "oneri": "Ağır işi ücretsiz havuzda iki aile ile doğrula", "tetik": "ağır iş ücretsiz havuz", "kural": False}, "a/m")
        self.assertEqual(d, "yeni")

    def test_zararli_kural_geri_cekilir(self):
        o = self._etki_kur("Zararlı kural metni burada", [(0.4, "success")] * 3, [(1.0, "fail"), (1.0, "success"), (1.0, "fail")])
        b.kanitla()
        self.assertEqual(b.oneri_oku()[0]["durum"], "geri-cekildi")
        self.assertIn("geri-cekildi", [x["tur"] for x in self._olaylar()])
        self.assertIn(o["id"], b.ETKI.read_text(encoding="utf-8"))
        self.assertNotIn("Zararlı", b.satirlar("etki kural işi"))

    def test_faydali_kural_kalir(self):
        self._etki_kur("Faydalı kural metni burada", [(1.0, "success")] * 3, [(0.4, "success")] * 3)
        b.kanitla()
        self.assertEqual(b.oneri_oku()[0]["durum"], "kural")
        self.assertIn('"karar": "kal"', b.ETKI.read_text(encoding="utf-8"))


class GostergeTest(unittest.TestCase):
    def test_tekrar_eden_hata_orani_ve_sayaclar(self):
        t = time.time()
        olaylar = [{"t": t, "hata": True, "ozet": "x"}, {"t": t, "hata": True, "ozet": "x"}, {"t": t, "hata": False, "ozet": "y"}]
        liste = [{"olusma": t, "durum": "kural"}, {"olusma": 0, "durum": "elendi"}]
        s = b.gosterge(liste, olaylar)
        self.assertIn("yeni ders 1", s)
        self.assertIn("kurala dönen 1", s)
        self.assertIn("geri çekilen 1", s)
        self.assertIn("tekrar eden hata %50 (2 hata)", s)


if __name__ == "__main__":
    unittest.main()
