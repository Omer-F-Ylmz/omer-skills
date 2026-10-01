"""RAM-1 K6 - mcp_guncelle surum dogrulamasi.

Dogrudan baslatma sabit surum ister: latest, ^, ~, >= ya da bos surum kurulumdan
once reddedilir (exit 2); kurulan surum hedeften farkliysa yakalanir.
"""
import os
import subprocess
import sys

import pytest

TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools")
sys.path.insert(0, TOOLS)
import mcp_guncelle as g  # noqa: E402


@pytest.mark.parametrize("surum", ["latest", "^0.6.2", "~1.2.0", ">=1.0", "", "1.x", "0.6.2 "])
def test_sabit_olmayan_surum_reddedilir(surum):
    with pytest.raises(ValueError):
        g.surum_dogrula(surum)


@pytest.mark.parametrize("surum", ["0.6.2", "2026.8.31", "0.0.83", "1.0.0-beta.1"])
def test_sabit_surum_kabul(surum):
    g.surum_dogrula(surum)


def test_kurulu_surum_hedeften_farkliysa_yakalanir():
    assert g.surum_kontrol("0.6.2", "0.6.2") is None
    assert "0.6.3" in g.surum_kontrol("0.6.3", "0.6.2")


@pytest.mark.parametrize("argv", [["mcp-time", "latest"], ["olmayan-sunucu", "1.0.0"]])
def test_cli_gecersiz_girdi_kurmadan_exit_2(argv):
    r = subprocess.run([sys.executable, os.path.join(TOOLS, "mcp_guncelle.py")] + argv,
                       capture_output=True, text=True, encoding="utf-8", timeout=30)
    assert r.returncode == 2


ESKI = r"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_x\node-v24.19.0-win-x64\node.exe"
YENI = r"C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_x\node-v24.20.1-win-x64\node.exe"


def test_node_yolu_surum_klasoru_yenilenir_diger_argumanlara_dokunulmaz():
    tanim = {"command": ESKI, "args": [r"C:\AI\mcp\mcp-memory\node_modules\x\dist\index.js", "--port", "1"],
             "env": {"MEMORY_FILE_PATH": r"C:\AI\mcp\mcp-memory\memory.jsonl"}}
    assert g.node_tanim(tanim, YENI) == dict(tanim, command=YENI)
    cmd = f'@echo off\r\n"{ESKI}" "C:\\AI\\mcp\\x\\index.js" %*\r\n'
    assert g.node_degistir(cmd, YENI) == cmd.replace(ESKI, YENI)
