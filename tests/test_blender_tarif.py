"""BLENDER-1 Faz 3: tarif kütüphanesi — saf doğrulama (Blender'sız) + 4 temsilî görev (gerçek Blender, exe yoksa atlanır).

Blender açan testler yalnız ortak sırayla: python .kos/kopru/arka.py <log> .kos/kopru/olcum_sira.py -m pytest ... -k blender
"""
import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / "tools" / "blender" / "lib"))
sys.path.insert(0, str(KOK / "tools" / "blender"))
import blender_cli as bc  # noqa: E402
import blender_oturum as bo  # noqa: E402
import tarif  # noqa: E402

TARIF = KOK / "tools" / "blender" / "lib" / "tarif.py"
blender = pytest.mark.skipif(not Path(bo.BLENDER).is_file(), reason="Blender exe yok")


# --- saf: spec Blender açılmadan reddedilir (boş koşu = boşa jeton + dakika)
def test_dogrula_temiz_spec():
    assert tarif.dogrula({"nesneler": [{"ad": "GEO-A", "tur": "kup", "boyut": [1, 1, 1], "malzeme": "bakir"}],
                          "isik": "urun", "onizle": {"yol": "x.png"}}) == []


def test_dogrula_hdri_dosyasi(tmp_path):
    (tmp_path / "studio_1k.hdr").write_bytes(b"#?RADIANCE")
    assert tarif.dogrula({"isik": "urun", "hdri": str(tmp_path / "studio_1k.hdr")}) == []


@pytest.mark.parametrize("spec, parca", [
    ({"bilinmez": 1}, "bilinmez"),
    ({"nesneler": [{"ad": "A", "tur": "ucgen"}]}, "tur"),
    ({"nesneler": [{"ad": "A", "tur": "kup", "boyut": [1, 1]}]}, "boyut"),
    ({"nesneler": [{"ad": "A", "tur": "kup", "malzeme": "altin"}]}, "malzeme"),
    ({"nesneler": [{"tur": "kup"}]}, "ad"),
    ({"isik": "disko"}, "isik"),
    ({"anim": [{"nesne": "A", "kanal": "renk", "kareler": [[1, 0]]}]}, "kanal"),
    ({"duzenle": [{"nesne": "A", "uçur": 1}]}, "uçur"),
    ({"ozet": ["ad", "ruh"]}, "ruh"),
    ({"isik": "urun", "hdri": "yok/studio.hdr"}, "hdri"),
    ({"hdri": __file__}, "hdri"),
])
def test_dogrula_hatalar(spec, parca):
    hatalar = tarif.dogrula(spec)
    assert hatalar and any(parca in h for h in hatalar), hatalar


def test_cli_spec_dosyadan(tmp_path, monkeypatch):
    spec = tmp_path / "s.json"
    spec.write_text(json.dumps({"ozet": ["ad"]}), encoding="utf-8")
    gelen = {}
    monkeypatch.setattr(bc, "calistir", lambda b, a, bl, z: (gelen.update(a), (0, {"gecti": True}, 1))[1])
    assert bc.main([str(TARIF), "@" + str(spec)]) == 0 and gelen == {"ozet": ["ad"]}


# --- gerçek Blender: Faz 1'in 3 temsilî görevi + zor görev, her biri TEK headless koşu
@pytest.fixture(scope="module")
def proje(tmp_path_factory):
    kok = tmp_path_factory.mktemp("masaustu")
    (kok / "P" / "blender").mkdir(parents=True)
    eski, bo.MASAUSTU = bo.MASAUSTU, kok
    yield kok / "P" / "blender"
    bo.MASAUSTU = eski


def kos(spec, blend=None):
    kod, sonuc, _ = bc.calistir(TARIF, spec, blend, zaman_asimi=300)
    assert kod == 0, sonuc
    return sonuc


@blender
def test_gorev1_sahne_malzeme_isik(proje):
    s = kos({"nesneler": [{"ad": "GEO-Fincan", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "konum": [0, 0, 0.045],
                           "malzeme": "seramik_sirli", "bevel": 0.002},
                          {"ad": "GEO-Zemin", "tur": "duzlem", "boyut": [1, 1, 0], "malzeme": {"renk": [0.8, 0.8, 0.8]}}],
             "isik": "urun", "boyut_m": 0.09, "kamera": "oto",
             "kaydet": str(proje / "g1.blend"), "onizle": {"yol": str(proje / "g1.png"), "px": 256},
             "ozet": ["ad", "boyut", "malzeme"]})
    assert s["gecti"] and Path(proje / "g1.blend").is_file() and Path(proje / "g1.png").is_file()
    ad = {n["ad"]: n for n in s["ozet"]}
    assert ad["GEO-Fincan"]["malzeme"] == ["MAT-SeramikSirli"] and abs(ad["GEO-Fincan"]["boyut"][2] - 0.09) < 1e-3
    assert len(json.dumps(s)) < 1500  # özet küçük kalır: MCP sahne JSON'u yerine


@blender
def test_gorev2_duzenle_uv(proje):
    s = kos({"duzenle": [{"nesne": "GEO-Fincan", "subdiv": 1, "uv": "akilli"}],
             "kaydet": str(proje / "g2.blend"), "ozet": ["ad", "ucgen", "uv"]}, blend=proje / "g1.blend")
    f = next(n for n in s["ozet"] if n["ad"] == "GEO-Fincan")
    assert f["uv"] >= 1 and f["ucgen"] > 100


@blender
def test_gorev3_anim_render(proje):
    s = kos({"anim": [{"nesne": "GEO-Fincan", "kanal": "rotation_euler", "kareler": [[1, [0, 0, 0]], [12, [0, 0, 90]]]}],
             "kare": [1, 12], "render": {"klasor": str(proje / "kareler"), "px": 128, "motor": "workbench", "adim": 4}},
            blend=proje / "g2.blend")
    assert len(s["render"]) == 3 and all(Path(p).is_file() for p in s["render"])


@blender
def test_cycles_gpu_adaptif_denoise(proje):
    s = kos({"nesneler": [{"ad": "GEO-Kup", "tur": "kup", "boyut": [0.1, 0.1, 0.1]}], "isik": "urun", "boyut_m": 0.1,
             "render": {"yol": str(proje / "c.png"), "px": 32, "motor": "cycles", "ornek": 16}})
    m = s["motor"]  # hız kaliteyi düşürmeden: GPU varsa GPU, adaptif örnekleme + albedo/normal destekli denoise
    assert m["motor"] == "CYCLES" and m["cihaz"] != "" and m["ornek"] == 16
    assert m["adaptif"] and m["denoise"] and m["gecis"] == "RGB_ALBEDO_NORMAL"


@blender
def test_zor_patlatilmis_kahve_makinesi_glb(proje):
    parcalar = [("GEO-Taban", "kup", [0.25, 0.2, 0.04]), ("GEO-Govde", "kup", [0.2, 0.18, 0.25]),
                ("GEO-Hazne", "silindir", [0.1, 0.1, 0.15]), ("GEO-Kapak", "silindir", [0.11, 0.11, 0.02])]
    s = kos({"nesneler": [{"ad": a, "tur": t, "boyut": b, "malzeme": "pirinc" if a == "GEO-Kapak" else {"renk": [0.1, 0.1, 0.1]}}
                          for a, t, b in parcalar],
             "yigin": "Z", "patlat": {"eksen": "Z", "aralik": 0.05},
             "kaydet": str(proje / "telve.blend"), "glb": str(proje / "telve.glb"), "ozet": ["ad", "konum", "ucgen"]})
    assert Path(proje / "telve.glb").stat().st_size > 1000
    ad = {n["ad"]: n for n in s["ozet"]}
    z = [ad[a]["konum"][2] for a, _, _ in parcalar]
    assert z == sorted(z) and min(b - a for a, b in zip(z, z[1:])) > 0.05
    assert sum(n["ucgen"] for n in s["ozet"]) < 5000  # düşük poli


def test_dogrula_ekler():
    assert tarif.dogrula({"nesneler": [{"ad": "A", "tur": "koni", "ust": 0.6, "ekler": [{"tur": "kup"}]}]}) == []
    assert any("ekler" in h for h in tarif.dogrula({"nesneler": [{"ad": "A", "tur": "kup", "ekler": [{"tur": "yok"}]}]}))


def test_yalin_oturum_bayraklari():
    import yalin
    b = yalin.bayraklar()
    assert {"--strict-mcp-config", "--disable-slash-commands", "--setting-sources"} <= set(b)
    sistem = b[b.index("--system-prompt") + 1]
    assert "seramik_sirli" in sistem and "pirinc" in sistem and str(TARIF) in sistem  # tek seferde doğru spec için


def parlaklik(png):
    Image = pytest.importorskip("PIL.Image")
    h = Image.open(png).convert("L").histogram()
    return sum(i * n for i, n in enumerate(h)) / sum(h) / 255, sum(h[250:]) / sum(h)


@blender
def test_isiksiz_malzemesiz_sahne_karanlik_kalmaz(proje):
    """Faz 5 g2/g3: --blend ışıksız/malzemesiz sahnede render siyah, malzeme_hepsi düşük çıkıyordu."""
    kos({"nesneler": [{"ad": "GEO-Fincan", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "konum": [0, 0, 0.045]}],
         "kaydet": str(proje / "ham.blend")})
    s = kos({"kaydet": str(proje / "ham2.blend"), "onizle": {"yol": str(proje / "ham.png"), "px": 128},
             "ozet": ["ad", "malzeme"]}, blend=proje / "ham.blend")
    assert s["diger"].get("LIGHT", 0) >= 3 and all(n["malzeme"] for n in s["ozet"])
    ort, yanik = parlaklik(proje / "ham.png")
    assert 0.2 < ort < 0.9 and yanik < 0.02


@blender
def test_beyaz_seramik_yanmaz(proje):
    """Faz 5 g1: seramik_sirli profilinde karenin %55-62'si yanık (≥250) çıkıyordu; taban-2 (kör 9/10) %0.1."""
    kos({"nesneler": [{"ad": "GEO-Zemin", "tur": "duzlem", "boyut": [1, 1, 1], "malzeme": {"renk": [0.75, 0.75, 0.75], "puruz": 0.9}},
                      {"ad": "GEO-Fincan", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "konum": [0, 0, 0.055],
                       "malzeme": "seramik_sirli"}],
         "isik": "seramik_sirli", "kamera": {"konum": [0.35, -0.5, 0.25], "hedef": [0, 0, 0.05], "lens": 85},
         "onizle": {"yol": str(proje / "beyaz.png"), "px": 128}})
    ort, yanik = parlaklik(proje / "beyaz.png")
    assert 0.35 < ort < 0.85 and yanik < 0.02


@blender
def test_sirli_seramik_vurgu_verir(proje):
    """Faz 5 v3 g1: oto kamerada sırlı fincan mat (max 228, ≥235 %0; kör isik 4) — taban-2 (isik 8) ≥235 %0.5."""
    kos({"nesneler": [{"ad": "GEO-Zemin", "tur": "duzlem", "boyut": [1, 1, 1], "malzeme": {"renk": [0.7, 0.7, 0.7], "puruz": 0.9}},
                      {"ad": "GEO-Tabak", "tur": "silindir", "boyut": [0.14, 0.14, 0.01], "konum": [0, 0, 0.005],
                       "malzeme": "seramik_sirli"},
                      {"ad": "GEO-Fincan", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "konum": [0, 0, 0.055],
                       "malzeme": "seramik_sirli"}],
         "isik": "seramik_sirli", "kamera": "oto", "onizle": {"yol": str(proje / "sir.png"), "px": 192}})
    h = pytest.importorskip("PIL.Image").open(proje / "sir.png").convert("L").histogram()
    assert sum(h[235:]) / sum(h) > 0.002 and sum(h[250:]) / sum(h) < 0.02


@blender
def test_koni_ust_ve_ekler_tek_nesne(proje):
    s = kos({"nesneler": [{"ad": "GEO-Cezve", "tur": "koni", "ust": 0.7, "boyut": [0.1, 0.1, 0.1],
                           "ekler": [{"tur": "kup", "boyut": [0.08, 0.01, 0.01], "konum": [0.08, 0, 0.03]}]}],
             "ozet": ["ad", "boyut"]})
    assert [n["ad"] for n in s["ozet"]] == ["GEO-Cezve"] and s["ozet"][0]["boyut"][0] > 0.15


@blender
def test_oto_kamera_zemini_kadraja_katmaz(proje):
    """Faz 5 v2 g1: oto kamera 1×1 m zemini de kutuya katıyordu → fincan karede minik (kör kompozisyon 2)."""
    s = kos({"nesneler": [{"ad": "GEO-Zemin", "tur": "duzlem", "boyut": [1, 1, 1]},
                          {"ad": "GEO-Fincan", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "konum": [0, 0, 0.055]}],
             "kamera": "oto"})
    konum, hedef = (s["kamera"][a] for a in ("konum", "hedef"))
    assert sum((a - b) ** 2 for a, b in zip(konum, hedef)) ** 0.5 < 0.6 and abs(hedef[2] - 0.055) < 0.02


@blender
def test_patlat_kadraj_ve_isik_parca_degil(proje):
    """Faz 5 v2 g4: kamera patlatmadan önce kuruluyordu (üst parçalar kadraj dışı); metal şeritleri MESH'ti
    (denetçi patlatma_aralik'ta parça saydı, GLB'ye girdi)."""
    s = kos({"nesneler": [{"ad": f"GEO-P{i}", "tur": "silindir", "boyut": [0.1, 0.1, 0.05]} for i in range(5)],
             "yigin": "Z", "patlat": {"eksen": "Z", "aralik": 0.06}, "isik": "metal", "kamera": "oto",
             "ozet": ["ad", "konum"]})
    assert all(n["ad"].startswith("GEO-") for n in s["ozet"])
    z = [n["konum"][2] for n in s["ozet"]]
    assert abs(s["kamera"]["hedef"][2] - (min(z) + max(z)) / 2) < 0.02


def test_anim_donus_birimi_derece():
    """Faz 5 v2 g3: anim'de birim yazmıyordu → model radyan verdi (2π = 6.28°), donus_360 düştü."""
    assert "360" in next(s for s in tarif.__doc__.splitlines() if "anim" in s and "kareler" in s)


@blender
@pytest.mark.parametrize("acik", ["1", "0"])
def test_egitim_varsayilanlari(proje, monkeypatch, acik):
    """BLENDER-3: eğitim mekanizmaları (85 mm, DOF yok — f/4 küçük ürünü bütünüyle bulandırdı (b3c), ürün kenar pahı, doğrusal turntable; AgX kontrast look sırlı seramikte %2 yanma kapısını aştı → yok); BLENDER_KALITE=0 eskisi."""
    monkeypatch.setenv("BLENDER_KALITE", acik)
    s = kos({"nesneler": [{"ad": "GEO-Kutu", "tur": "kup", "boyut": [0.1, 0.1, 0.1], "konum": [0, 0, 0.05]},
                          {"ad": "GEO-Zemin", "tur": "duzlem", "boyut": [1, 1, 0]}],
             "kamera": "oto", "anim": [{"nesne": "GEO-Kutu", "kanal": "rotation_euler", "kareler": [[1, [0, 0, 0]], [9, [0, 0, 360]]]}],
             "kare": [1, 8], "onizle": {"yol": str(proje / f"k{acik}.png"), "px": 64, "motor": "workbench"}})
    k = s.get("kalite", {})
    if acik == "1":
        assert s["kamera"]["lens"] == 85 and "dof" not in k and k["pah"] == ["GEO-Kutu"] and k["ara"] == "LINEAR"
    else:
        assert s["kamera"]["lens"] == 50 and not k
