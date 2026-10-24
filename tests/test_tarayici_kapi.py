# TARAYICI-KAPI-1: varsayılan tarayıcıyı (Opera) açan komutlar PreToolUse kancasında engellenir
import json
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
sys.path.insert(0, str(KOK / ".kos/kopru"))
import pytest  # noqa: E402
import tarayici_kapi  # noqa: E402
import ajan_ram_bekci  # noqa: E402

ENGEL = [
    "npx @modelcontextprotocol/inspector --version",
    "npx -y @modelcontextprotocol/inspector node server.js",
    "start http://localhost:6274",
    'start "" https://example.com',
    "start https://example.com",
    "explorer http://localhost:3000",
    "explorer.exe https://example.com",
    'cmd /c start "" chrome',
    "cmd.exe /c start foo.html",
    'python -c "import webbrowser; webbrowser.open(\'http://x\')"',
    "python -m webbrowser http://x",
    'python -c "import os; os.startfile(\'http://x\')"',
    "npx vite --open",
    "vite --open /index.html",
    "npm run dev -- --open",
    "ng serve --open",
    "gh browse",
    "gh browse -n",
    "npm docs react",
    "Start-Process http://localhost:5173",
    "Start-Process 'https://example.com'",
    'Start-Process -FilePath "https://example.com"',
]

IZIN = [
    "npx @modelcontextprotocol/inspector --cli node server.js --method tools/list",
    "npx @modelcontextprotocol/inspector --method tools/list --cli node s.js",
    "npx vite build",
    "npx vite --port 5173",
    "npm run dev",
    "gh pr list",
    "gh issue view 3",
    "npm install react",
    "git status",
    "rg start src",
    "python -m http.server 8000",
    "Start-Process notepad.exe",
    "start chrome.exe",
    "ls docs",
]


@pytest.mark.parametrize("komut", ENGEL)
def test_engellenir(komut):
    assert tarayici_kapi.karar(komut), komut


@pytest.mark.parametrize("komut", IZIN)
def test_izin(komut):
    assert tarayici_kapi.karar(komut) is None, komut


def _kanca(komut):
    girdi = json.dumps({"tool_name": "Bash", "tool_input": {"command": komut}})
    return subprocess.run([sys.executable, "-S", str(KOK / "tools" / "tarayici_kapi.py")], input=girdi.encode(), capture_output=True)


def test_kanca_engel_cikis_2_turkce_gerekce():
    r = _kanca("start http://x.test")
    assert r.returncode == 2
    assert "tarayıcı".encode() in r.stderr


def test_kanca_izin_cikis_0():
    assert _kanca("git status").returncode == 0
    assert subprocess.run([sys.executable, "-S", str(KOK / "tools" / "tarayici_kapi.py")], input=b"", capture_output=True).returncode == 0


def test_ajan_ortami_tarayici_kapali():
    assert ajan_ram_bekci.TARAYICI_ENV["BROWSER"] == "none"
    assert ajan_ram_bekci.TARAYICI_ENV["CI"] == "1"
    assert ajan_ram_bekci.TARAYICI_ENV["OPEN_BROWSER"] == "false"
    import ajan_sira
    _, env = ajan_sira.baslat_argv("")
    for k, v in ajan_ram_bekci.TARAYICI_ENV.items():
        assert env[k] == v


MB = 2**20
# (pid, ppid, ad, ws_bayt, komut)
AGAC = [
    (10, 1, "claude.exe", 900 * MB, "claude -p"),
    (11, 10, "bash.exe", 5 * MB, "bash"),
    (12, 11, "opera.exe", 200 * MB, "opera.exe http://127.0.0.1:6274"),   # ajan torunu → kapanır
    (13, 12, "opera.exe", 90 * MB, "opera.exe --type=renderer"),          # onun çocuğu → kapanır
    (14, 10, "msedge.exe", 150 * MB, "msedge.exe http://x"),               # ajan çocuğu → kapanır
    (15, 10, "chrome.exe", 300 * MB, "chrome --headless"),                 # Chrome serbest
    (40, 1, "explorer.exe", 100 * MB, "explorer.exe"),
    (41, 40, "opera.exe", 400 * MB, "opera.exe"),                          # Ömer'in Opera'sı: ajan ağacı dışı
    (42, 41, "opera.exe", 90 * MB, "opera.exe --type=gpu-process"),
]


def test_bekci_yalniz_ajan_agacindaki_tarayiciyi_kapatir():
    oldurulen, kayit = [], []
    pidler = ajan_ram_bekci.tarayici_kapat(AGAC, {10}, oldurulen.extend, lambda *a: kayit.append(a))
    assert sorted(pidler) == [12, 13, 14]
    assert sorted(oldurulen) == [12, 13, 14]
    assert kayit and kayit[0][0] == "TARAYICI-KAPI"


def test_bekci_tarayici_yoksa_sessiz():
    oldurulen, kayit = [], []
    assert ajan_ram_bekci.tarayici_kapat([s for s in AGAC if s[0] in (10, 11, 15)], {10}, oldurulen.extend, lambda *a: kayit.append(a)) == []
    assert not oldurulen and not kayit
