"""ÖĞREN-2.tur d5: kosul/nasil mekanik hakemi — alıntı kaynak satırında, komut kaynakta birebir bulunmalı."""
import importlib.util
from pathlib import Path

YOL = Path(__file__).resolve().parents[2] / ".kos/kopru/ogren/tur2_d5.py"
spec = importlib.util.spec_from_file_location("tur2_d5", YOL)
D = importlib.util.module_from_spec(spec)
spec.loader.exec_module(D)


def kart(tmp_path, **kw):
    f = tmp_path / "SKILL.md"
    f.write_text("# x\nGerekir: Node.js 20 ve npm.\nKoş: `npx foo --json`\n", encoding="utf-8")
    return {"kanit": str(f), **kw}


def test_dogru_alinti_ve_komut(tmp_path):
    k = kart(tmp_path, nasil="npx foo --json", kosul_alinti="Node.js 20 ve npm", kosul_satir=2)
    assert D.mekanik(k) == (True, True)


def test_uydurma_komut_ve_yanlis_satir(tmp_path):
    k = kart(tmp_path, nasil="npx bar", kosul_alinti="Node.js 20 ve npm", kosul_satir=3)
    assert D.mekanik(k) == (False, True)  # satır 3 komşu aralığında (±1 satır)
    k["kosul_satir"] = 1
    k["kosul_alinti"] = "Python 3 gerekir"
    assert D.mekanik(k)[1] is False


def test_uzun_alinti_ve_bos_alan(tmp_path):
    k = kart(tmp_path, nasil=None, kosul_alinti=" ".join(["kelime"] * 16), kosul_satir=2)
    assert D.mekanik(k) == (None, False)
    assert D.mekanik(kart(tmp_path, nasil="", kosul_alinti=None, kosul_satir=None)) == (None, None)
