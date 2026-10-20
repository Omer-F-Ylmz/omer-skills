import sys
sys.path.insert(0, "tools")
from mem_bekci import sebepler


def test_aktif_oturumda_eski_gozlem():
    assert sebepler(True, 45, None) == ["son gozlem 45 dk"]
    assert sebepler(True, None, None) == ["son gozlem yok dk"]


def test_oturum_yokken_eski_gozlem_sorun_degil():
    assert sebepler(False, 500, None) == []


def test_taze_kota_isareti():
    assert sebepler(False, 1, 10) == ["kota/429 10 dk once"]
    assert sebepler(True, 5, 120) == []
