import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_rea_baglam as t  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, mem = tmp_path / "ev", tmp_path / "settings.json"
    ilk = b'{\n  "CLAUDE_MEM_CONTEXT_OBSERVATIONS": "15",\n  "x": 1\n}\n'
    mem.write_bytes(ilk)
    assert t.main(["--kuru"], ev, mem) == 0 and mem.read_bytes() == ilk
    t.main(["uygula"], ev, mem); t.main(["uygula"], ev, mem)
    assert mem.read_bytes() == ilk.replace(b'"15"', b'"7"')
    t.main(["--geri"], ev, mem)
    assert mem.read_bytes() == ilk
