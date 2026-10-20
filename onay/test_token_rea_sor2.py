import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_rea_sor2 as t  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, kok = tmp_path / "ev", tmp_path / "kok"
    ev.mkdir(); kok.mkdir()
    (ev / "CLAUDE.md").write_bytes(b"# a\n")
    (kok / "CLAUDE.md").write_bytes(b"# b")
    assert t.main(["--kuru"], ev, kok) == 0 and (ev / "CLAUDE.md").read_bytes() == b"# a\n"
    t.main(["uygula"], ev, kok); t.main(["uygula"], ev, kok)
    for md in (ev / "CLAUDE.md", kok / "CLAUDE.md"):
        assert md.read_bytes().count(t.SATIR.encode("utf-8")) == 1 and b"\r" not in md.read_bytes()
    t.main(["--geri"], ev, kok)
    assert (ev / "CLAUDE.md").read_bytes() == b"# a\n" and (kok / "CLAUDE.md").read_bytes() == b"# b"
