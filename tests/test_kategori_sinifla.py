import csv, sys, unittest
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import kategori_sinifla as K  # noqa: E402

TSV = KOK / "docs/envanter/kategori.tsv"
csv.field_size_limit(10**9)


class Siniflandir(unittest.TestCase):
    def b(self, ad, tur="skill", ozet="", **kw):
        return K.siniflandir(ad, tur, ozet, **kw)[0]

    def test_alan_ornekleri(self):
        self.assertEqual(self.b("pdf-processing", ozet="Extract text from PDF files"), "belge")
        self.assertEqual(self.b("playwright-e2e-tests", ozet="end to end browser tests"), "test-qa")
        self.assertEqual(self.b("terraform-skill", ozet="infrastructure as code"), "bulut-devops")
        self.assertEqual(self.b("blender-geometry-nodes", ozet="procedural modeling"), "3d-blender")
        self.assertEqual(self.b("ffmpeg-skill", ozet="video transcoding"), "video")
        self.assertEqual(self.b("swiftui-pro", ozet="iOS apps"), "mobil")
        self.assertEqual(self.b("unity-ecs-patterns", ozet="game development"), "oyun")
        self.assertEqual(self.b("pentest-checklist", ozet="penetration testing"), "guvenlik")

    def test_alan_genel_sinifi_yener(self):
        self.assertEqual(self.b("cli-anything-blender", ozet="CLI for Blender"), "3d-blender")

    def test_sinyal_yoksa_tur_varsayilani(self):
        b, ik, g, y, _ = K.siniflandir("zzqx", "karar")
        self.assertEqual((b, g, y), ("surec-plan", "dusuk", "tur-varsayilan"))
        self.assertEqual(K.siniflandir("zzqx", "liste")[0], "diger-genel")

    def test_birincil_hep_gecerli(self):
        for ad in ("a", "ecc:x", "", "Ünlü-Çalışma"):
            self.assertIn(self.b(ad), K.KATEGORILER)

    def test_cok_yonlu_liste(self):
        for ad, beklenen in (("ecc:plan", "ECC"), ("claude-mem:mem-search", "claude-mem"), ("replica-skill:replica-build", "replica"),
                             ("graphify", "graphify"), ("rtk-desktop", "RTK"), ("obsidian-markdown", "Obsidian"), ("ruflo", "ruflo"),
                             ("autoharness:learn", "autoharness"), ("continuous-learning-v2", "continuous-learning"),
                             ("mattpocock-skills:tdd", "mattpocock"), ("headroom", "Headroom"), ("code-mode", "code-mode"),
                             ("context-mode:ctx-stats", "context-mode"), ("claude-code-setup:claude-automation-recommender", "claude-code-setup"),
                             ("agent-memory-mcp", "memory-MCP"), ("reverse-engineer-anything", "REA")):
            self.assertIn(beklenen, K.cok_yonlu(ad), ad)
        self.assertEqual(K.cok_yonlu("area-calculator"), []); self.assertNotIn("code-mode", K.cok_yonlu("code-modernization:scaffolder"))  # 'rea' sözcük içinde etiket değil

    def test_nasil(self):
        self.assertIn("python", K.nasil("betik", "x", "a.py"))
        self.assertIn("mcp__", K.nasil("mcp", "figma", ""))


class BackendAyrimi(unittest.TestCase):
    def b(self, ad, ozet=""):
        return K.siniflandir(ad, "skill", ozet)[0]

    def test_dotnet_ve_genel(self):
        self.assertIn("backend-genel", K.KATEGORILER)
        self.assertEqual(self.b("dotnet-backend", "ASP.NET Core"), "backend-dotnet")
        self.assertEqual(self.b("django-patterns", "Django patterns"), "backend-genel")
        self.assertEqual(self.b("laravel-security", "PHP Laravel"), "backend-genel")

    def test_kisa_kok_alt_dizge_degil(self):
        self.assertEqual(K.cok_yonlu("create-react-app"), [])


class YeniKalemAkisi(unittest.TestCase):
    """yeni kalem: kural -> ikinci model -> uyusmazsa hakem (model cagrilari sahte)."""

    def test_uyusursa_hakem_yok_uyusmazsa_hakem(self):
        import kategori_denetim as D
        ik, hk = D.ikinci_parti, D.hakem_parti
        cagri = []
        D.ikinci_parti = lambda g, haric=None: ({0: ("backend-genel", "5"), 1: ("gorsel", "5")}, "sahte/ikinci")
        D.hakem_parti = lambda g: (cagri.append(len(g)) or {0: ("bulut-devops", "kanitla")}, "sahte/hakem", "")
        try:
            r = D.kalem_kontrol([{"ad": "django-pro", "tur": "skill", "ozet": "Django backend"},
                                 {"ad": "terraform-skill", "tur": "skill", "ozet": "infrastructure as code"}])
        finally:
            D.ikinci_parti, D.hakem_parti = ik, hk
        self.assertEqual(r[0][0], "backend-genel"); self.assertEqual(r[0][3], "denetim-uyum")
        self.assertEqual((r[1][0], r[1][3]), ("bulut-devops", "denetim-hakem"))
        self.assertEqual(cagri, [1])

    def test_kimlik_ipucusuz(self):
        import kategori_denetim as D
        self.assertTrue(D.ipucusuz_kimlik({"ad": "DcCT3UfpFAn", "kanit": ""}))
        self.assertFalse(D.ipucusuz_kimlik({"ad": "DcCT3UfpFAn", "kanit": "x"}))


@unittest.skipUnless(TSV.exists(), "kategori.tsv uretilmemis")
class Cikti(unittest.TestCase):
    def test_kapsam_yuzde_yuz(self):
        with open(TSV, encoding="utf-8", newline="") as f:
            rs = list(csv.DictReader(f, delimiter="\t"))
        self.assertGreater(len(rs), 50000)
        self.assertTrue(all(r["birincil"] in K.KATEGORILER for r in rs))
        self.assertTrue(all(r["ikincil"] == "" or all(x in K.KATEGORILER for x in r["ikincil"].split(";")) for r in rs))


if __name__ == "__main__":
    unittest.main()
