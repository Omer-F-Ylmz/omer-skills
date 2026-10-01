"""RAM-1 K6 - MCP envanter karsilastirmasi.

Baslatma bicimi degisirken sunucu ve arac seti birebir ayni kalmali: eksik/fazla
arac ya da sunucu, ya da baslamayan sunucu fark raporu verir ve CLI exit 1 doner.
"""
import copy
import json
import os
import subprocess
import sys

TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools")
sys.path.insert(0, TOOLS)
import mcp_envanter as e  # noqa: E402

ONCE = {"cc:mcp-time": {"arac_sayisi": 2, "araclar": ["convert_time", "get_current_time"]},
        "desktop:mcp-git": {"arac_sayisi": 1, "araclar": ["git_status"]}}


def test_ayni_envanter_fark_vermez():
    assert e.karsilastir(ONCE, copy.deepcopy(ONCE)) == []


def test_eksik_arac_raporlanir():
    sonra = copy.deepcopy(ONCE)
    sonra["cc:mcp-time"] = {"arac_sayisi": 1, "araclar": ["get_current_time"]}
    fark = e.karsilastir(ONCE, sonra)
    assert any("eksik" in f and "convert_time" in f for f in fark)


def test_fazla_arac_raporlanir():
    sonra = copy.deepcopy(ONCE)
    sonra["desktop:mcp-git"] = {"arac_sayisi": 2, "araclar": ["git_status", "git_push"]}
    assert any("fazla" in f and "git_push" in f for f in e.karsilastir(ONCE, sonra))


def test_eksik_ve_fazla_sunucu_raporlanir():
    sonra = copy.deepcopy(ONCE)
    del sonra["desktop:mcp-git"]
    sonra["cc:yeni"] = {"arac_sayisi": 0, "araclar": []}
    fark = " | ".join(e.karsilastir(ONCE, sonra))
    assert "desktop:mcp-git" in fark and "cc:yeni" in fark


def test_baslamayan_sunucu_esit_sayilmaz():
    hatali = {"cc:mcp-time": {"hata": "INIT-YOK"}}
    assert e.karsilastir(hatali, copy.deepcopy(hatali))


def test_cc_degisken_genisletme():
    os.environ["RAM1_DENEME"] = "x"
    assert e.genislet("${RAM1_DENEME}") == "x"
    assert e.genislet("${RAM1_YOK:-varsayilan}") == "varsayilan"


def _cli(tmp_path, once, sonra):
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    a.write_text(json.dumps(once), encoding="utf-8")
    b.write_text(json.dumps(sonra), encoding="utf-8")
    return subprocess.run([sys.executable, os.path.join(TOOLS, "mcp_envanter.py"), "karsilastir", str(a), str(b)],
                          capture_output=True, text=True, encoding="utf-8")


def test_cli_fark_varsa_exit_1_ve_rapor(tmp_path):
    sonra = copy.deepcopy(ONCE)
    sonra["cc:mcp-time"]["araclar"] = ["get_current_time"]
    r = _cli(tmp_path, ONCE, sonra)
    assert r.returncode == 1 and "convert_time" in r.stdout


def test_cli_birebir_ayniysa_exit_0(tmp_path):
    assert _cli(tmp_path, ONCE, ONCE).returncode == 0
