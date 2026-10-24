"""cp1254 konsolda ucuz_alt '→' yazarken UnicodeEncodeError vermemeli (CODE-MODE-REA-2)."""
import os
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent

KOD = (
    "import sys; sys.path.insert(0, 'tools'); import ucuz_alt;"
    "ucuz_alt.coz = lambda *a: (None, '', 0, {}, False);"
    "sys.exit(ucuz_alt.main(['--tur', 'ozet', 'soru', 'cikti.md']))"
)


def test_cp1254_konsolda_ok_yazilir():
    env = {**os.environ, "PYTHONIOENCODING": "cp1254"}
    env.pop("PYTHONUTF8", None)
    r = subprocess.run([sys.executable, "-c", KOD], cwd=KOK, env=env, capture_output=True)
    assert b"UnicodeEncodeError" not in r.stderr, r.stderr.decode("utf-8", "replace")
    assert r.returncode == 5
