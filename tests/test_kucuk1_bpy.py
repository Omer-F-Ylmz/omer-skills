"""KÜÇÜK-1 K4: pyright çıktısı çözülemezse mesajda stderr'in ve ham stdout'un ilk satırları; çıkış 2."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import bpy_kontrol as B  # noqa: E402


def test_cozulemeyen_cikti_stderr_ve_ham_ilk_satirlar(tmp_path, monkeypatch, capsys):
    betik = tmp_path / "b.py"
    betik.write_text("x = 1\n", encoding="utf-8")
    ham = "ham-ilk\n" + "dolgu\n" * 400
    monkeypatch.setattr(B.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(a, 1, ham, "err-ilk\nerr-iki\n"))
    assert B.main([str(betik)]) == 2
    e = capsys.readouterr().err
    assert "err-ilk" in e and "ham-ilk" in e
