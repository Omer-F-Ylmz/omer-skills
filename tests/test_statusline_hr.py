"""TOKEN-6b K3: ~/.claude/statusline.ps1 HR segmenti — env var + port açık · env yok · port kapalı."""
import json
import os
import socket
import subprocess
from pathlib import Path

SL = Path.home() / ".claude" / "statusline.ps1"
GIRDI = json.dumps({"model": {"display_name": "Opus"}, "context_window": {"used_percentage": 12}})


def kos(tmp_path, env_var, port):
    (tmp_path / ".claude").mkdir(exist_ok=True)
    ayar = {"env": {"ANTHROPIC_BASE_URL": "http://127.0.0.1:6767"} if env_var else {}}
    (tmp_path / ".claude" / "settings.json").write_text(json.dumps(ayar), encoding="utf-8")
    env = {**os.environ, "USERPROFILE": str(tmp_path), "TEMP": str(tmp_path), "TMP": str(tmp_path), "HR_PORT": str(port)}
    p = subprocess.run(["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(SL)],
                       input=GIRDI, capture_output=True, text=True, env=env, timeout=30)
    assert p.returncode == 0, p.stderr
    return p.stdout


def bos_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def test_env_var_port_acik(tmp_path):
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        s.listen()
        out = kos(tmp_path, True, s.getsockname()[1])
    assert out.startswith("HR | ") and "KAPALI" not in out
    assert "Opus" in out and "ctx 12%" in out


def test_env_yok(tmp_path):
    out = kos(tmp_path, False, bos_port())
    assert out.startswith("!!HR KAPALI:env | ") and "Opus" in out


def test_port_kapali(tmp_path):
    out = kos(tmp_path, True, bos_port())
    assert out.startswith("!!HR KAPALI:port | ") and "ctx 12%" in out
