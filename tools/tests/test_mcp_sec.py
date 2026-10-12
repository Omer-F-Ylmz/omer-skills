import runpy
from pathlib import Path


def test_mcp_sec_oz_denetim(capsys):
    runpy.run_path(str(Path(__file__).resolve().parents[1] / "olcum" / "mcp_sec.py"), run_name="__main__")
    assert capsys.readouterr().out.strip() == "ok"
