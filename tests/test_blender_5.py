"""BLENDER-5: M5a şablon/arketip/göreli yerleşim · M5b takma ad · M5c aşamalı istem · M5d fark özeti · M5e ölçü oturtma ·
K1 fon · K2 metal softbox · K3 arketip biçimi. Saf testler Blender'sız; @blender olanlar yalnız ortak sırayla (olcum_sira)."""
import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(KOK / "tools"), str(KOK / "tools" / "blender" / "lib"), str(KOK / "tools" / "blender"),
                str(KOK / "tools" / "olcum")]
import blender_cli as bc  # noqa: E402
import blender_oturum as bo  # noqa: E402
import tarif  # noqa: E402
import yalin  # noqa: E402

TARIF = KOK / "tools" / "blender" / "lib" / "tarif.py"
blender = pytest.mark.skipif(not Path(bo.BLENDER).is_file(), reason="Blender exe yok")


# --- M5a: şablon + klasör + turntable doldurma (saf)
def test_sablon_turntable_doldurur():
    s = tarif.duzelt({"sablon": "turntable", "klasor": "C:/d", "turntable": {"nesne": "GEO-F", "son": 48},
                      "nesneler": [{"ad": "GEO-F", "arketip": "fincan", "boyut": [0.08, 0.08, 0.09]}]})
    assert tarif.dogrula(s) == []
    assert s["kaydet"] == "C:/d/sahne.blend" and s["onizle"] == {"yol": "C:/d/onizleme.png", "px": 384, "motor": "eevee"}
    assert s["kamera"] == "oto" and s["isik"] and s["kare"] == [1, 48]
    assert s["anim"][0]["kareler"] == [[1, [0, 0, 0]], [48, [0, 0, 360]]]
    assert s["render"] == {"klasor": "C:/d/kareler", "px": 256, "motor": "eevee", "adim": 12}
    assert s["nesneler"][0]["tur"] == "silindir"


def test_kaydet_true_klasor_varsayilani():  # b5p g3/g4: Path(True) Blender'da çöktü
    s = tarif.duzelt({"klasor": "C:/d", "kaydet": True, "onizle": True})
    assert s["kaydet"] == "C:/d/sahne.blend" and s["onizle"]["yol"] == "C:/d/onizleme.png"
    assert tarif.dogrula({"kaydet": True, "glb": True}) == ["kaydet: dosya yolu olmalı", "glb: dosya yolu olmalı"]


def test_sablon_acik_anahtari_ezmez():
    s = tarif.duzelt({"sablon": "kahraman_metal", "klasor": "C:/d", "isik": "urun", "onizle": {"yol": "C:/d/x.png"}})
    assert s["isik"] == "urun" and s["onizle"] == {"yol": "C:/d/x.png"}


def test_sablon_metal_cycles_patlatilmis_yigin():
    assert tarif.duzelt({"sablon": "kahraman_metal", "klasor": "C:/d"})["onizle"]["motor"] == "cycles"
    p = tarif.duzelt({"sablon": "patlatilmis"})
    assert p["yigin"] == "Z" and p["patlat"]["aralik"] >= 0.05


@pytest.mark.parametrize("spec, parca", [
    ({"sablon": "disko"}, "sablon"),
    ({"nesneler": [{"ad": "A", "arketip": "vazo"}]}, "arketip"),
    ({"nesneler": [{"ad": "A", "tur": "kup", "bitisik": {"hedef": "B", "yon": "+Z"}}]}, "hedef"),
    ({"nesneler": [{"ad": "B", "tur": "kup"}, {"ad": "A", "tur": "kup", "bitisik": {"hedef": "B", "yon": "yan"}}]}, "yon"),
])
def test_dogrula_yeni_alanlar(spec, parca):
    h = tarif.dogrula(tarif.duzelt(spec))
    assert h and any(parca in x for x in h), h


# --- M5b: takma adlar gerçek anahtarlarla çakışmaz, duzelt açar
def test_takma_ad():
    assert not set(tarif.TAKMA) & set(tarif.ANAHTARLAR) and not set(tarif.TAKMA_N) & {*tarif.ALANLAR, "donus", "ekler", "ust"}
    s = tarif.duzelt({"n": [{"ad": "A", "a": "sap", "b": [0.1, 0.01, 0.01], "m": "ahsap_koyu"}]})
    assert s["nesneler"][0] == {"ad": "A", "arketip": "sap", "tur": "kup", "boyut": [0.1, 0.01, 0.01], "malzeme": "ahsap_koyu"}


# --- M5c: aşamalı istem — çekirdek kısa, modül yalnız istekte geçerse
G1 = ("Ürün sahnesi kur: GEO-Fincan (silindir, çap 8 cm, yükseklik 9 cm, parlak beyaz sırlı seramik), GEO-Tabak. "
      "Kaydet: C:\\d\\sahne.blend; 384 px EEVEE önizleme render: C:\\d\\onizleme.png.")


def test_sistem5_cekirdek_kisa_ve_asamali():
    s = yalin.sistem5(G1)
    assert len(s) <= 1300 + len(", ".join(tarif._ad_listesi()[1])) + 200, len(s)
    assert len(s) < len(yalin.sistem(tek=True)) / 2
    assert not any(m in s for m in yalin.MODUL.values())
    assert yalin.MODUL[("dön", "360", "turntable")] in yalin.sistem5("Fincan 360° dönsün, kare 1-48")
    assert yalin.MODUL[("patlat",)] in yalin.sistem5("patlatılmış görünüm") and yalin.MODUL[("glb",)] in yalin.sistem5("GLB: x.glb")
    assert "duzenle:" in yalin.sistem5("2 mm bevel, subdivision")


# --- M5d: fark özeti ≤300 kr, hatalı nesneyi taşır
def test_fark_ozeti_kisa():
    spec = {"nesneler": [{"ad": f"GEO-P{i}", "tur": "kup", "boyut": [0.1, 0.1, 0.1], "malzeme": "pirinc"} for i in range(8)],
            "onizle": {"yol": "C:/uzun/yol/" * 10 + "x.png"}}
    f = yalin.fark(spec, ["nesneler[3]: tur 'yok' yok", "ölçü sapması GEO-P5: beklenen [1, 1, 1]"])
    assert len(f) <= 300 and "GEO-P3" in f and "GEO-P5" in f and "GEO-P0" not in f


# --- M5e: tek eksenli ≤%50 sapma Blender'dan önce oturtulur; çok eksen/büyük sapma hata
def test_olcu_oturt():
    s = {"nesneler": [{"ad": "F", "tur": "silindir", "boyut": [0.08, 0.08, 0.12]}]}
    assert tarif.olcu_oturt(s, {"F": [0.08, 0.08, 0.09]}) == [] and s["nesneler"][0]["boyut"] == [0.08, 0.08, 0.09]
    s = {"nesneler": [{"ad": "F", "tur": "silindir", "boyut": [0.12, 0.12, 0.09]}]}
    assert tarif.olcu_oturt(s, {"F": [0.08, 0.08, 0.09]})
    s = {"nesneler": [{"ad": "F", "tur": "silindir", "boyut": [0.08, 0.08, 0.2]}]}
    assert tarif.olcu_oturt(s, {"F": [0.08, 0.08, 0.09]})


def _kos(yanitlar, istemler):
    def kos(istem, ek):
        istemler.append((istem, ek))
        return {"metin": yanitlar.pop(0), "usage": {"output_tokens": 100}, "tur": 1, "usd": 0.0, "sure": 1.0}
    return kos


def test_tek5_kisa_istem_ve_oturtma_tek_tur():
    istemler, kosulan = [], []
    spec = {"nesneler": [{"ad": "F", "a": "fincan", "b": [0.08, 0.08, 0.12]}], "beklenen": {"F": [0.08, 0.08, 0.09]}}
    o = yalin.tek(G1, kos=_kos([json.dumps(spec)], istemler), bes=True,
                  calistir=lambda b, a, bl: kosulan.append(a) or (0, {"gecti": True, "ozet": [{"ad": "F", "boyut": [0.08, 0.08, 0.09]}]}, 1))
    ek = istemler[0][1]
    assert o["rc"] == 0 and o["tur"] == 1 and kosulan[0]["nesneler"][0]["boyut"] == [0.08, 0.08, 0.09]
    assert ek[ek.index("--system-prompt") + 1] == yalin.sistem5(G1)


def test_tek5_duzeltme_turu_fark_ozeti():
    istemler = []
    yalin.tek("x", kos=_kos(['{"n": [{"ad": "A", "t": "yok"}]}', '{"n": [{"ad": "A", "t": "kup"}]}'], istemler), bes=True,
              calistir=lambda b, a, bl: (0, {"gecti": True}, 1))
    assert "Önceki spec" not in istemler[1][0] and len(istemler[1][0]) <= len("x") + 400


# --- gerçek Blender
def kos(spec, blend=None, kal="5", monkeypatch=None):
    kod, sonuc, _ = bc.calistir(TARIF, spec, blend, zaman_asimi=300)
    assert kod == 0, sonuc
    return sonuc


@blender
def test_bitisik_ve_zemine_oturma(tmp_path, monkeypatch):
    monkeypatch.delenv("BLENDER_KALITE", raising=False)
    s = kos({"nesneler": [{"ad": "T", "arketip": "tabak", "boyut": [0.14, 0.14, 0.01]},
                          {"ad": "F", "tur": "silindir", "boyut": [0.08, 0.08, 0.09], "bitisik": {"hedef": "T", "yon": "+Z"}},
                          {"ad": "S", "tur": "kup", "boyut": [0.1, 0.01, 0.01], "bitisik": {"hedef": "F", "yon": "+X"}}],
             "ozet": ["ad", "konum"]})
    k = {o["ad"]: o["konum"] for o in s["ozet"]}
    assert k["T"][2] == pytest.approx(0.005, abs=1e-3) and k["F"][2] == pytest.approx(0.055, abs=1e-3)
    assert 0.04 + 0.05 * 0.7 <= k["S"][0] <= 0.04 + 0.05 and k["S"][2] == pytest.approx(k["F"][2], abs=1e-3)


@blender
def test_fon_yalniz_render_icin(tmp_path, monkeypatch):
    monkeypatch.delenv("BLENDER_KALITE", raising=False)
    monkeypatch.setattr(bo, "MASAUSTU", tmp_path)  # --blend yalnız Desktop/<Proje>/blender altından
    tmp_path = tmp_path / "P" / "blender"
    tmp_path.mkdir(parents=True)
    s = kos({"nesneler": [{"ad": "GEO-Fincan", "arketip": "fincan", "boyut": [0.08, 0.08, 0.09]}],
             "kaydet": str(tmp_path / "s.blend"), "glb": str(tmp_path / "f.glb"),
             "onizle": {"yol": str(tmp_path / "o.png"), "px": 64}, "ozet": ["ad", "boyut", "ucgen"]})
    assert [o["ad"] for o in s["ozet"]] == ["GEO-Fincan"] and s["kalite"]["fon"]
    assert s["ozet"][0]["boyut"] == pytest.approx([0.08, 0.08, 0.09], rel=0.02)
    assert s["ozet"][0]["ucgen"] > 2 * 124  # K3: ağız oyuğu (cidar) → düz silindirden fazla yüz
    s2 = kos({"ozet": ["ad"]}, tmp_path / "s.blend")
    assert [o["ad"] for o in s2["ozet"]] == ["GEO-Fincan"]  # fon kayıtlı sahnede yok
    import blender_faz5 as f5
    assert f5.glb_mesh(tmp_path / "f.glb") == 1


@blender
def test_metal_softbox_ve_kalite1_kapali(tmp_path, monkeypatch):
    spec = {"nesneler": [{"ad": "GEO-Cezve", "tur": "koni", "ust": 0.7, "boyut": [0.07, 0.07, 0.08], "malzeme": "pirinc"},
                         {"ad": "GEO-Zemin", "tur": "duzlem", "boyut": [1, 1, 0]}],
            "isik": "metal", "onizle": {"yol": str(tmp_path / "o.png"), "px": 64}, "ozet": ["ad"]}
    monkeypatch.delenv("BLENDER_KALITE", raising=False)
    s = kos(json.loads(json.dumps(spec)))
    assert s["kalite"]["softbox"] == 2 and "fon" not in s["kalite"] and len(s["ozet"]) == 2
    monkeypatch.setenv("BLENDER_KALITE", "1")  # 1.3.0 kolu: K1–K3 yok
    s = kos(json.loads(json.dumps(spec)))
    assert "softbox" not in s["kalite"]
