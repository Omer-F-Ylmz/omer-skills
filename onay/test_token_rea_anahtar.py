import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_rea_anahtar as t  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, mem = tmp_path / "ev", tmp_path / "settings.json"
    ilk = b'{\n  "CLAUDE_MEM_MODE": "code",\n  "x": 1\n}\n'
    mem.write_bytes(ilk)
    assert t.main(["--kuru"], ev, mem) == 0 and mem.read_bytes() == ilk
    t.main(["uygula"], ev, mem); t.main(["uygula"], ev, mem)
    assert mem.read_bytes() == ilk.replace(b'"code"', b'"code--anahtar"')
    mod = json.loads((tmp_path / "modes" / "code--anahtar.json").read_text("utf-8"))
    assert "TR:" in mod["prompts"]["xml_subtitle_placeholder"] and "EN:" in mod["prompts"]["xml_subtitle_placeholder"]
    t.main(["--geri"], ev, mem)
    assert mem.read_bytes() == ilk and not (tmp_path / "modes" / "code--anahtar.json").exists()


def test_isaretli_sayar(tmp_path):
    mem = tmp_path / "settings.json"
    c = sqlite3.connect(tmp_path / "claude-mem.db")
    c.execute("CREATE TABLE observations (subtitle TEXT)")
    c.executemany("INSERT INTO observations VALUES (?)", [("a | TR: x | EN: y",), ("b",)])
    c.commit(); c.close()
    assert t.isaretli(mem) == 1
