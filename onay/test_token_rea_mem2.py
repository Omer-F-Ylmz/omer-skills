import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_rea_mem2 as t  # noqa: E402


def test_kuru_uygula_geri(tmp_path):
    ev, kok = tmp_path / "ev", tmp_path / "kok"
    ev.mkdir(); kok.mkdir()
    (ev / "CLAUDE.md").write_bytes(b"# a\n")
    (kok / "CLAUDE.md").write_bytes(b"# b")
    assert t.main(["--kuru"], ev, kok) == 0 and (ev / "CLAUDE.md").read_bytes() == b"# a\n"
    t.main(["uygula"], ev, kok); t.main(["uygula"], ev, kok)
    for md in (ev / "CLAUDE.md", kok / "CLAUDE.md"):
        assert md.read_bytes().count(t.SATIR.encode("utf-8")) == 1 and b"\r" not in md.read_bytes()
    (ev / "CLAUDE.md").write_bytes((ev / "CLAUDE.md").read_bytes() + b"- sonradan\n")  # geri başkasının satırını silmez
    t.main(["--geri"], ev, kok)
    assert (ev / "CLAUDE.md").read_bytes() == b"# a\n- sonradan\n" and (kok / "CLAUDE.md").read_bytes() == b"# b\n"


def test_mem2_arama_biçimi(tmp_path, monkeypatch):
    import sqlite3
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".kos" / "kopru" / "token-rea"))
    import mem2
    db = tmp_path / "m.db"
    c = sqlite3.connect(db)
    c.executescript("CREATE TABLE observations(id INTEGER PRIMARY KEY, project, type, title, subtitle, narrative, text, facts, concepts, created_at);"
                    "CREATE VIRTUAL TABLE observations_fts USING fts5(title, subtitle, narrative, text, facts, concepts, content='observations', content_rowid='id');"
                    "INSERT INTO observations VALUES(1,'p','bugfix','Headroom retrieve hash','', 'anlati', '', '', '', '2026-10-20T10:00:00Z');"
                    "INSERT INTO observations VALUES(2,'p','change','Başka konu','', 'unrelated', '', '', '', '2026-10-20T11:00:00Z');"
                    "INSERT INTO observations_fts(observations_fts) VALUES('rebuild');")
    c.commit(); c.close()
    monkeypatch.setattr(mem2, "DB", str(db))
    r = mem2.ara("headroom hash", 5)
    assert [x[0] for x in r] == [1] and mem2.bicim(r).startswith("#1 10-20 10:00 ● Headroom retrieve hash")
    assert mem2.ara("a b", 5) == []
