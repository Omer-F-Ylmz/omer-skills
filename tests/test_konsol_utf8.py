"""DUMAN-FIX: araç girişi stdout/stderr'i UTF-8'e çevirir; PYTHONIOENCODING yokken Git Bash'te Türkçe bozulmaz."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
METIN = "açık şığ ÇĞİÖŞÜ"


@pytest.mark.parametrize("arac", ["gorsel_uret", "blender_oturum"])
def test_konsol_utf8(arac):
    kod = (f"import sys; sys.path.insert(0, r'{TOOLS}'); import {arac}\n"
           f"try: {arac}.main(['--help'])\nexcept SystemExit: pass\n"
           f"print({METIN!r}); print({METIN!r}, file=sys.stderr)")
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    r = subprocess.run([sys.executable, "-c", kod], capture_output=True, env=env, timeout=60)
    assert METIN in r.stdout.decode("utf-8", "replace")
    assert METIN in r.stderr.decode("utf-8", "replace")
