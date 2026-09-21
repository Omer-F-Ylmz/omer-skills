"""KURULUM-11l K13 - mcp_kurutest.py argument resolution pins.

--cwd ciplak ad: Desktop'in cwd'si C:\\Windows\\System32; kuru testte bu dizini
her seferinde tam yol yazmak yerine `--cwd System32` kabul edilir.
--spawner node: NODE_GIRIS haritasi yalnizca uc npm sunucusunu taniyor; haritada
olmayan sunucu (ornegin claude-design/tasarim) KeyError yerine config'teki
komutla kosar, boylece bayrak butun sunucularda guvenle kullanilabilir.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import mcp_kurutest as m  # noqa: E402


def test_cwd_ciplak_ad_sistem_koku_altinda_cozulur():
    assert m.cwd_coz("System32") == os.path.join(os.environ["SystemRoot"], "System32")


def test_cwd_tam_yol_aynen_kalir():
    assert m.cwd_coz(r"C:\Projeler") == r"C:\Projeler"


def test_cwd_verilmezse_none():
    assert m.cwd_coz(None) is None


def test_spawner_node_haritadaki_sunucuyu_node_exe_ile_kosar():
    komut, cagri = m.spawner_uygula("puppeteer", "cmd.exe", ["/c", "x"], "node")
    assert komut.endswith("node.exe")
    assert cagri[0].endswith(os.path.join("puppeteer-mcp-server", "dist", "index.js"))


def test_spawner_node_haritada_olmayan_sunucu_configteki_komutla_kosar():
    komut, cagri = m.spawner_uygula("claude-design", r"C:\x\claude-design.cmd", ["--t"], "node")
    assert komut == r"C:\x\claude-design.cmd"
    assert cagri == ["--t"]


def test_spawner_verilmezse_config_aynen_kalir():
    assert m.spawner_uygula("x", "c", ["a"], None) == ("c", ["a"])
