import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rtk_onisle as ro  # noqa: E402


def kos(komut, arac="PowerShell", rtk_yazar=False):
    girdi = json.dumps({"tool_name": arac, "tool_input": {"command": komut}})
    out = io.StringIO()
    assert ro.main(io.StringIO(girdi), out, lambda _: rtk_yazar) == 0
    return json.loads(out.getvalue())["hookSpecificOutput"]["updatedInput"]["command"] if out.getvalue() else None


def test_git():
    assert kos("git status") == "rtk git status"


def test_dotnet_info_ve_test():
    assert kos("dotnet --info") == "rtk dotnet --info"
    assert kos("dotnet test x.csproj") == "rtk dotnet test x.csproj"


def test_npm_ve_npm_cmd():
    assert kos("npm test") == "rtk npm test"
    assert kos("npm.cmd test") == "rtk npm test"


def test_pytest_aileleri():
    assert kos("pytest -q tools/tests") == "rtk pytest -q tools/tests"
    assert kos("python -m pytest -q tests") == "rtk pytest -q tests"


def test_node_test_yalniz_test_bayragi():
    assert kos("node --test a.mjs") == "rtk node --test a.mjs"
    assert kos("node script.js") is None


def test_zincir_ve_pipe_tuketici():
    assert kos("cd tools; git status | Select-Object -First 5") == "cd tools; rtk git status | Select-Object -First 5"
    assert kos("cd x && npm test", "Bash") == "cd x && rtk npm test"


def test_bash_ek_aileler_yalniz_bash():
    assert kos("cd docs && ls -la | head -5", "Bash") == "cd docs && rtk ls -la | head -5"
    assert kos("grep -n foo bar", "Bash") == "rtk grep -n foo bar"
    assert kos("grep -n foo bar") is None  # PowerShell'de grep yok


def test_tirnak_icindeki_ayrac_bolmez():
    assert kos('git commit -m "a && b | c"') == 'rtk git commit -m "a && b | c"'


def test_icerik_dokenlere_dokunulmaz():
    for k in ("cat a.txt", "sed -n 1,5p a", "echo hi", "python x.py"):
        assert kos(k, "Bash") is None


def test_bilinmeyen_ve_cozulemeyen_ozgun_kalir():
    assert kos("Get-ChildItem") is None
    assert kos("git log $(echo x)", "Bash") is None
    assert kos('git commit -m "acik') is None
    assert kos("rtk git status") is None


def test_bos_ve_bozuk_girdi():
    assert kos("") is None
    assert kos("   ") is None
    out = io.StringIO()
    assert ro.main(io.StringIO("bozuk{"), out, lambda _: False) == 0 and out.getvalue() == ""


def test_bom_onekli_girdi():
    girdi = "﻿" + json.dumps({"tool_name": "PowerShell", "tool_input": {"command": "git status"}})
    out = io.StringIO()
    ro.main(io.StringIO(girdi), out, lambda _: False)
    assert "rtk git status" in out.getvalue()


def test_rtk_zaten_yaziyorsa_sessiz():
    assert kos("git status", rtk_yazar=True) is None


def test_diger_alanlar_korunur():
    girdi = json.dumps({"tool_name": "PowerShell", "tool_input": {"command": "git status", "timeout": 5}})
    out = io.StringIO()
    ro.main(io.StringIO(girdi), out, lambda _: False)
    assert json.loads(out.getvalue())["hookSpecificOutput"]["updatedInput"] == {"command": "rtk git status", "timeout": 5}
