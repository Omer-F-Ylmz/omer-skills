"""ÖĞREN-2.tur d3: kapı hakemi — tavan dolunca ayrışan alan 'yanlış' sayılmaz; 3. aileye gider, yoksa kararsız ve paydadan düşer."""
import importlib.util
from pathlib import Path

YOL = Path(__file__).resolve().parents[2] / ".kos/kopru/ogren/tur2_d2_kapi.py"
spec = importlib.util.spec_from_file_location("tur2_kapi", YOL)
K = importlib.util.module_from_spec(spec)
spec.loader.exec_module(K)

T = {a: True for a in K.ALAN}
AYR = {**T, "nasil": False}


def test_tavan_dolu_ucuncu_yok_kararsiz_paydadan_duser(monkeypatch):
    monkeypatch.setattr(K, "haiku_oy", lambda p: None)
    nihai, ayr, kar = K.birlestir([(T, "a", "x"), (AYR, "b", "y")], "p", lambda: None)
    assert nihai["nasil"] is None and (ayr, kar) == (1, 1)
    assert K.oran([nihai]) == (3, 3, 1)


def test_tavan_dolu_ucuncu_aile_karar_verir(monkeypatch):
    monkeypatch.setattr(K, "haiku_oy", lambda p: None)
    nihai, ayr, kar = K.birlestir([(T, "a", "x"), (AYR, "b", "y")], "p", lambda: AYR)
    assert nihai["nasil"] is False and kar == 0


def test_haiku_oncelikli(monkeypatch):
    monkeypatch.setattr(K, "haiku_oy", lambda p: T)
    nihai, _, kar = K.birlestir([(T, "a", "x"), (AYR, "b", "y")], "p", lambda: AYR)
    assert nihai["nasil"] is True and kar == 0
