"""TASARIM-2: frontend-craft scripts/yakinsama.mjs — zemin sınıfı, eş çift oranı, geçmiş (proje başına tek satır, son 5)."""
import json
import os
import pathlib
import shutil
import subprocess

import pytest

KOK = pathlib.Path(__file__).resolve().parents[1]
Y = KOK / "plugins/frontend-craft/skills/frontend-craft/scripts/yakinsama.mjs"

pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="node yok")


def js(kod, env=None):
    r = subprocess.run(["node", "--input-type=module", "-e", f"const m = await import({json.dumps(Y.as_uri())});" + kod],
                       capture_output=True, text=True, encoding="utf-8", check=True, env=env)
    return json.loads(r.stdout)


def d(fontlar, bg, orta=False, kart=0):
    return {"fontsUsed": fontlar, "bg": bg, "heroCentered": orta, "cards3": kart}


def test_zemin_sinifi():
    assert js("console.log(JSON.stringify(['#f1e9dc','#ffffff','#111111','#3d6a99'].map(m.zemin)))") == \
        ["açık-sıcak", "açık-nötr", "koyu-nötr", "orta-soğuk"]


def test_oran_hepsi_ayni_ve_hepsi_farkli():
    ayni = [d(["georgia", "system-ui"], "#f6efe6")] * 4
    farkli = [d(["georgia"], "#f6efe6"), d(["space mono"], "#111111", True), d(["archivo"], "#1f3a5f", False, 1),
              d(["bricolage"], "#ffffff", True, 1)]
    o = js(f"console.log(JSON.stringify([m.oran({json.dumps(ayni)}.map(m.imza)), m.oran({json.dumps(farkli)}.map(m.imza))]))")
    assert o[0] == {"font": 1, "zemin": 1, "duzen": 1, "toplam": 1}
    assert o[1]["font"] == 0 and o[1]["zemin"] == 0 and o[1]["toplam"] < .2


def test_ortak_aile_font_esi_sayilir():
    o = js("console.log(JSON.stringify(m.oran([{fontsUsed:['Segoe UI','Iowan Old Style'],bg:'#f1e9dc'},"
           "{fontsUsed:['avenir next','iowan old style'],bg:'#f1e9dc'}].map(m.imza))))")
    assert o["font"] == 1


def test_gecmis_proje_basina_tek_satir_son_bes(tmp_path):
    env = {**os.environ, "FC_GECMIS": str(tmp_path / "g.tsv")}
    kod = ("for (let i = 0; i < 7; i++) m.gecmisYaz({fontsUsed:['f'+i],bg:'#ffffff'}, 'p'+i);"
           "m.gecmisYaz({fontsUsed:['yeni'],bg:'#111111'}, 'p6');"
           "console.log(JSON.stringify(m.gecmisOku()))")
    g = js(kod, env)
    assert [s[1] for s in g] == ["p2", "p3", "p4", "p5", "p6"]
    assert g[-1][2:4] == ["yeni", "koyu-nötr"]
