import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import gorsel_dogrula as G  # noqa: E402


@pytest.mark.parametrize("yanit, beklenen", [
    ("HAVUZ 42", True),
    ("Görseldeki yazı:\nHAVUZ 42.", True),
    ('1. "HAVUZ 42" yazısını okuyorum.\nZ42 VUAH', False),  # düşünme metni cevap sayılmaz
    ("Mavi.", False),
])
def test_ocr_son_satir(yanit, beklenen):
    assert G._kontrol(yanit, ["havuz42"], None, "son") is beklenen


def test_renk_son_satir():
    assert G._kontrol("Mavi.", ["mavi", "blue"], None, "son")
    assert not G._kontrol("Gri", ["mavi", "blue"], None, "son")


def test_sahne_iki_grup():
    yanit = "Gökyüzü mavi, ortada sarı bir güneş, altta yeşil çimen."
    assert G._kontrol(yanit, ["sarı", "yellow"], ["güneş", "daire"], "tum")
    assert not G._kontrol("Mavi bir zemin.", ["sarı", "yellow"], ["güneş", "daire"], "tum")
