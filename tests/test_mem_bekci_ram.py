import sys
sys.path.insert(0, "tools")
from mem_bekci import llama_bosta, en_buyuk_bosta


def test_llama_ilk_gozlemde_bosta_degil():
    assert llama_bosta(None, 7, 5.0, 100.0) is False


def test_llama_cpu_degisti_bosta_degil():
    assert llama_bosta({"pid": 7, "cpu": 5.0, "t": 0.0}, 7, 6.0, 100.0) is False


def test_llama_cpu_sabit_60sn_bosta():
    assert llama_bosta({"pid": 7, "cpu": 5.0, "t": 0.0}, 7, 5.0, 100.0) is True


def test_llama_cpu_sabit_ama_60sn_dolmadi():
    assert llama_bosta({"pid": 7, "cpu": 5.0, "t": 50.0}, 7, 5.0, 100.0) is False


def test_llama_pid_degisti_bosta_degil():
    assert llama_bosta({"pid": 3, "cpu": 5.0, "t": 0.0}, 7, 5.0, 100.0) is False


def test_en_buyuk_bosta_cpu_yuksegi_atlar():
    liste = [("chrome", 1, 900, 0.2), ("build", 2, 2000, 40.0), ("opera", 3, 500, 0.0)]
    assert en_buyuk_bosta(liste) == ("chrome", 1, 900)


def test_en_buyuk_bosta_yoksa_none():
    assert en_buyuk_bosta([("a", 1, 10, 50.0)]) is None
