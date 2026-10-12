import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "onay"))
import mcp_hafif_2_env as o  # noqa: E402


def test_yama_tek_satir_ve_tekrarsiz():
    m = "a\n" + o.CAPA + "    const p = spawn();\n"
    y = o.yama(m)
    assert y == "a\n" + o.CAPA + o.EK + "    const p = spawn();\n"
    assert o.yama(y) == y


def test_capa_yoksa_dokunmaz():
    with pytest.raises(SystemExit):
        o.yama("degismis dosya\n")
