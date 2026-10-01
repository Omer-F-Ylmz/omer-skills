"""blender-uretim K3 · malzeme tarifleri — Blender 5.2.1 (Principled girişleri canlı sorgulandı 2026-10-01).

Kullanım: import malzemeler; m = malzemeler.kur("bakir")  → MAT-Bakir. Değerler öneri (malzemeler.md).
Soket adı tutmazsa isik_kur.soket mevcut adları listeler → search_api_docs ile yeniden sorgula.
Kanıt: blender_cli ile doğrudan koştur → boş sahnede 9 tarif, SONUC {gecti, sonuc: {tarif: düğüm sayısı}, hatalar}.
"""
import json
import sys
from pathlib import Path

import bpy

sys.path.insert(0, str(Path(__file__).parent))
from isik_kur import ayarla, bagla, principled  # noqa: E402


def _kabartma(nt, p, tip, ayar, guc, cikis="Factor"):
    d, b = nt.nodes.new(tip), nt.nodes.new("ShaderNodeBump")
    ayarla(d, ayar)
    ayarla(b, {"Strength": guc})
    bagla(nt, d, cikis, b, "Height")
    bagla(nt, b, "Normal", p, "Normal")


def _rampa(nt, kaynak, cikis, hedef, giris, renk0, renk1):
    cr = nt.nodes.new("ShaderNodeValToRGB")
    bagla(nt, kaynak, cikis, cr, "Factor")
    bagla(nt, cr, "Color", hedef, giris)
    cr.color_ramp.elements[0].color = renk0
    cr.color_ramp.elements[1].color = renk1


def seramik_sirli(nt, p):  # sır = coat katmanı
    ayarla(p, {"Base Color": (0.92, 0.9, 0.86, 1), "Roughness": 0.25, "IOR": 1.5,
               "Coat Weight": 1.0, "Coat Roughness": 0.03, "Coat IOR": 1.5})


def seramik_mat(nt, p):
    ayarla(p, {"Base Color": (0.85, 0.83, 0.8, 1), "Roughness": 0.65, "Specular IOR Level": 0.35})
    _kabartma(nt, p, "ShaderNodeTexNoise", {"Scale": 400.0}, 0.03)


def bakir(nt, p):  # cezve: dövme yüzey
    ayarla(p, {"Base Color": (0.955, 0.638, 0.538, 1), "Metallic": 1.0, "Roughness": 0.28})
    _kabartma(nt, p, "ShaderNodeTexVoronoi", {"Scale": 60.0}, 0.15, cikis="Distance")


def pirinc(nt, p):
    ayarla(p, {"Base Color": (0.91, 0.78, 0.42, 1), "Metallic": 1.0, "Roughness": 0.32})


def cam(nt, p):
    ayarla(p, {"Base Color": (1, 1, 1, 1), "Roughness": 0.0, "IOR": 1.5, "Transmission Weight": 1.0})


def ahsap_koyu(nt, p):
    tc, dalga = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeTexWave")
    ayarla(dalga, {"Scale": 3.0, "Distortion": 6.0, "Detail": 4.0})
    bagla(nt, tc, "Object", dalga, "Vector")
    _rampa(nt, dalga, "Factor", p, "Base Color", (0.05, 0.025, 0.012, 1), (0.16, 0.08, 0.04, 1))
    ayarla(p, {"Roughness": 0.45})


def kahve_sivi(nt, p):
    ayarla(p, {"Base Color": (0.03, 0.012, 0.005, 1), "Roughness": 0.05, "IOR": 1.33})


def kahve_kopuk(nt, p):  # köpük/krema: yumuşak saçılma + ince kabarcık
    ayarla(p, {"Base Color": (0.42, 0.26, 0.13, 1), "Roughness": 0.6, "Subsurface Weight": 0.3,
               "Subsurface Radius": (1.0, 0.5, 0.25), "Subsurface Scale": 0.002})
    _kabartma(nt, p, "ShaderNodeTexVoronoi", {"Scale": 300.0}, 0.1, cikis="Distance")


def cekirdek(nt, p):  # kavrulmuş; yağlı parlama
    no = nt.nodes.new("ShaderNodeTexNoise")
    ayarla(no, {"Scale": 25.0})
    _rampa(nt, no, "Factor", p, "Base Color", (0.1, 0.05, 0.025, 1), (0.22, 0.11, 0.05, 1))
    ayarla(p, {"Roughness": 0.35, "Coat Weight": 0.3, "Coat Roughness": 0.2})


TARIFLER = {f.__name__: f for f in (seramik_sirli, seramik_mat, bakir, pirinc, cam, ahsap_koyu,
                                     kahve_sivi, kahve_kopuk, cekirdek)}


def kur(ad, isim=None):
    m = bpy.data.materials.new(isim or "MAT-" + ad.title().replace("_", ""))
    nt, p = principled(m)
    TARIFLER[ad](nt, p)
    return m


def _kanit():
    sonuc, hatalar = {}, {}
    for ad in TARIFLER:
        try:
            sonuc[ad] = len(kur(ad).node_tree.nodes)
        except Exception as e:
            hatalar[ad] = f"{type(e).__name__}: {e}"
    print("SONUC:" + json.dumps({"gecti": not hatalar and all(v > 0 for v in sonuc.values()),
                                 "blender": bpy.app.version_string, "sonuc": sonuc, "hatalar": hatalar},
                                ensure_ascii=False))


if __name__ == "__main__":
    _kanit()
