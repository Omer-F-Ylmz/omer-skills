"""TASARIM-1: frontend-craft scripts/slop.mjs puan() kalibrasyonu (17 referans ölçümü) + uç durumlar."""
import json
import pathlib
import shutil
import subprocess

import pytest

KOK = pathlib.Path(__file__).resolve().parents[1]
SLOP = KOK / "plugins/frontend-craft/skills/frontend-craft/scripts/slop.mjs"
OLCUM = KOK / "docs/tasarim/olcum"

pytestmark = pytest.mark.skipif(not shutil.which("node"), reason="node yok")


def puanla(girdiler):
    js = (f"const m = await import({json.dumps(SLOP.as_uri())});"
          "let s=''; process.stdin.on('data', c => s += c); process.stdin.on('end', () =>"
          " console.log(JSON.stringify(JSON.parse(s).map(m.puan))));")
    r = subprocess.run(["node", "--input-type=module", "-e", js], input=json.dumps(girdiler),
                       capture_output=True, text=True, encoding="utf-8", check=True)
    return json.loads(r.stdout)


def test_referanslar_stripe_disinda_temiz():
    adlar, d = [], []
    for f in sorted(OLCUM.glob("*.json")):
        j = json.loads(f.read_text(encoding="utf-8"))
        adlar.append(j["ad"])
        d.append(j["d"])
    assert len(adlar) == 17
    sonuc = dict(zip(adlar, puanla(d)))
    assert [a for a, p in sonuc.items() if p["slop"]] == ["stripe"]
    assert all(len(p["bayrak"]) <= 1 for a, p in sonuc.items() if a != "stripe")


def test_tipik_ai_sayfasi_slop():
    d = {"gradText": 1, "pbGrads": 2, "glassCard": 3, "heroCentered": True, "cards3": 1, "ratio": 2.5,
         "fontsUsed": ["__Inter_20b187"], "accents": 2, "slopWords": 3, "emojiIcons": 3}
    p = puanla([d])[0]
    assert p["slop"] and len(p["bayrak"]) == 7


def test_tek_bayrak_slop_degil_ve_bos_font():
    p = puanla([{"heroCentered": True, "cards3": 1, "ratio": 2, "fontsUsed": []}])[0]
    assert len(p["bayrak"]) == 1 and not p["slop"]
