import importlib.util
from pathlib import Path

import pytest

_s = importlib.util.spec_from_file_location("varlik_getir", Path(__file__).parents[1] / "skills/blender-uretim/varlik_getir.py")
vg = importlib.util.module_from_spec(_s)
_s.loader.exec_module(vg)


def test_atif_metni_cc0_bos_ccby_dolu():
    assert vg.atif_metni("Cezve", "avlasova11", "CC0", "u") == ""
    assert vg.atif_metni("Cezve", "avlasova11", "CC-BY-4.0", "u") == '"Cezve" — avlasova11 (u), CC-BY-4.0'


def test_atif_ayni_kaynak_id_gunceller(tmp_path):
    vg.atif({"kaynak": "polyhaven", "id": "a", "ad": "1"}, tmp_path)
    vg.atif({"kaynak": "polyhaven", "id": "b", "ad": "2"}, tmp_path)
    hepsi = vg.atif({"kaynak": "polyhaven", "id": "a", "ad": "3"}, tmp_path) and __import__("json").loads((tmp_path / "atif.json").read_text(encoding="utf-8"))
    assert [(k["id"], k["ad"]) for k in hepsi] == [("b", "2"), ("a", "3")]


def test_icinde_dizin_disina_cikamaz(tmp_path):
    assert vg._icinde(tmp_path, "textures/x.jpg").startswith(str(tmp_path))
    with pytest.raises(ValueError):
        vg._icinde(tmp_path, "../x.jpg")
