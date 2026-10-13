"""VİDEO-16 d5 onay betiği: kuru değiştirmez · uygula birleştirir (commitsiz dosya korunur) · örtüşmede reddeder · --geri revert eder."""
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import video16_uygula as vu  # noqa: E402


def _repo(tmp_path, monkeypatch):
    for k in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{k}_NAME", "t")
        monkeypatch.setenv(f"GIT_{k}_EMAIL", "t@t")
    g = lambda *a: subprocess.run(["git", "-C", str(tmp_path), *a], check=True, capture_output=True)
    g("init", "-q", "-b", "main")
    (tmp_path / "a.py").write_text("x = 0\n")
    g("add", "."), g("commit", "-qm", "1")
    g("checkout", "-qb", "kol/video-shorts")
    (tmp_path / "a.py").write_text("x = 1\n")
    g("commit", "-qam", "2")
    g("checkout", "-q", "main")
    (tmp_path / "omer.py").write_text("commitsiz\n")
    return g


def test_kuru_uygula_geri(tmp_path, monkeypatch):
    g = _repo(tmp_path, monkeypatch)
    vu.main("--kuru", tmp_path)
    assert (tmp_path / "a.py").read_text() == "x = 0\n"
    vu.main("uygula", tmp_path)
    assert (tmp_path / "a.py").read_text() == "x = 1\n" and (tmp_path / "omer.py").read_text() == "commitsiz\n"
    vu.main("--geri", tmp_path)
    assert (tmp_path / "a.py").read_text() == "x = 0\n" and (tmp_path / "omer.py").is_file()
    assert not (tmp_path / ".kos" / "v16" / "onay-once.txt").exists()


def test_commitsiz_ortusmede_reddeder(tmp_path, monkeypatch):
    _repo(tmp_path, monkeypatch)
    (tmp_path / "a.py").write_text("omer degistirdi\n")
    with pytest.raises(SystemExit):
        vu.main("uygula", tmp_path)
    assert (tmp_path / "a.py").read_text() == "omer degistirdi\n"
