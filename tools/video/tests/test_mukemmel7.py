# MÜKEMMEL-7 K5 (test_m7.py eski M7 dalgasının): `video on` web_ara → kos(["mcporter", ...]) Windows'ta FileNotFoundError (mcporter.cmd uzantısız bulunmaz)
import os
import sys

import pytest

from video import cli


@pytest.mark.skipif(sys.platform != "win32", reason=".cmd çözümü yalnız Windows")
def test_kos_cmd_sarmalayiciyi_bulur(tmp_path, monkeypatch):
    (tmp_path / "k5arac.cmd").write_text("@echo k5\n")
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
    rc, out, _ = cli.kos(["k5arac"])
    assert (rc, out.strip()) == (0, b"k5")
