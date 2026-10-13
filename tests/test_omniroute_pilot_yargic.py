"""TOKEN-8 iş 3: omniroute1 pilot — opus yargıcı hafif bayraklarla, claude() görev koşucusu değişmeden."""
import importlib.util
import json
from pathlib import Path

_s = importlib.util.spec_from_file_location("pilot", Path(__file__).resolve().parents[1] / ".claude" / "omniroute1" / "pilot.py")
pilot = importlib.util.module_from_spec(_s)
_s.loader.exec_module(pilot)


def test_yargic_hafif_kosucu_tam(monkeypatch):
    argv = []

    class P:
        stdout, stderr = json.dumps({"result": "0 8"}), ""

    monkeypatch.setattr(pilot, "ram_bekle", lambda: None)
    monkeypatch.setattr(pilot.subprocess, "run", lambda a, **k: argv.append(a) or P)
    pilot.claude("x", "sonnet")
    puan, hata = pilot.opus_yargila([(0, {"gorev": pilot.ISTEM + "t", "yanit": "y"})])
    assert puan == {0: 8.0} and not hata
    assert "--setting-sources" not in argv[0] and "--tools" not in argv[0]
    assert argv[1][-4:] == ["--setting-sources", "", "--tools", ""] and "opus" in argv[1]
