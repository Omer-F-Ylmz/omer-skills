"""VİDEO-GÖZ-1b-1R R0: push kapısı — gitleaks git temiz (çıkış 0) değilse push yok; push yalnız tools/push-kapi.sh ile."""
import os
import shutil
import subprocess
from pathlib import Path

BETIK = Path(__file__).resolve().parents[2] / "push-kapi.sh"
BASH = Path(shutil.which("git")).parents[1] / "usr" / "bin" / "bash.exe"  # Git'in MSYS bash'i: PATH'e yol eklemez, sahteler önce bulunur


def _kos(tmp_path, gl_rc):
    """Sahte gitleaks (çıkış gl_rc) ve git PATH başında; cwd repo değil → gerçek git push bulunsa da itemez."""
    b, kayit = tmp_path / "bin", (tmp_path / "kayit.txt").as_posix()
    b.mkdir()
    (b / "gitleaks").write_text(f'#!/bin/sh\necho "gitleaks $*" >> "{kayit}"\nexit {gl_rc}\n', newline="\n")
    (b / "git").write_text(f'#!/bin/sh\necho "git $*" >> "{kayit}"\n', newline="\n")
    r = subprocess.run([str(BASH), BETIK.as_posix(), "origin", "main"], cwd=tmp_path, capture_output=True, text=True,
                       env={**os.environ, "PATH": f"{b}{os.pathsep}{os.environ['PATH']}"})
    return r.returncode, (tmp_path / "kayit.txt").read_text() if (tmp_path / "kayit.txt").is_file() else ""


def test_gitleaks_kirli_push_yok(tmp_path):
    rc, kayit = _kos(tmp_path, 1)
    assert rc != 0 and "gitleaks git --exit-code 1" in kayit and "git push" not in kayit


def test_gitleaks_temiz_push_argumanlarla(tmp_path):
    rc, kayit = _kos(tmp_path, 0)
    assert rc == 0 and kayit.splitlines() == ["gitleaks git --exit-code 1", "git push origin main"]
