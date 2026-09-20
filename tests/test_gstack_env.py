"""gstack-core/bin/gstack-env: aynayi bir kez kurar, ikinci source kopyalamaz."""
import os
import shutil
import subprocess
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
ENV = KOK / "tools" / "gstack_env.sh"
BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="bash yok")


def sahte_ro(d):
    """Minik bir gstack-core kopyasi: bin/ altinda iki dosya + bir SKILL.md."""
    ro = d / "gstack-core"
    (ro / "bin").mkdir(parents=True)
    (ro / "SKILL.md").write_text("x\n", encoding="utf-8")
    (ro / "bin" / "browse").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
    (ro / "bin" / "gstack-yardimci").write_text("#!/usr/bin/env bash\n", encoding="utf-8")
    return ro


def kos(betik, ro, ev):
    return subprocess.run([BASH, "-c", betik], capture_output=True, text=True, timeout=60,
                          env=dict(os.environ, GSTACK_CORE_RO=str(ro), HOME=str(ev)))


def test_ayna_kurulur_ve_degiskenler_disari_verilir(tmp_path):
    ro, ev = sahte_ro(tmp_path / "ro"), tmp_path / "ev"
    ev.mkdir()
    r = kos('. "%s"; echo "GS=$GS"; echo "B=$B"; echo "D=[$D]"' % ENV.as_posix(), ro, ev)
    assert r.returncode == 0, r.stderr
    assert r.stderr == ""
    ayna = ev / ".gstack" / "core"
    assert sorted(p.relative_to(ayna).as_posix() for p in ayna.rglob("*") if p.is_file()) == \
        sorted(p.relative_to(ro).as_posix() for p in ro.rglob("*") if p.is_file())
    # Git Bash yolu MSYS bicimine cevirir; bicim degil ucu ve B/GS iliskisi onemli
    satir = dict(s.split("=", 1) for s in r.stdout.splitlines())
    assert satir["GS"].endswith("/.gstack/core")
    assert satir["B"] == "python3 " + satir["GS"] + "/bin/browse"
    assert satir["D"] == "[]"
    assert os.access(ayna / "bin" / "browse", os.X_OK)


def test_ikinci_source_kopyalamaz(tmp_path):
    ro, ev = sahte_ro(tmp_path / "ro"), tmp_path / "ev"
    ev.mkdir()
    assert kos('. "%s"' % ENV.as_posix(), ro, ev).returncode == 0
    (ro / "bin" / "sonradan-eklendi").write_text("#!/bin/sh\n", encoding="utf-8")
    r = kos('. "%s"; echo bitti' % ENV.as_posix(), ro, ev)
    assert r.returncode == 0, r.stderr
    assert "bitti" in r.stdout
    assert not (ev / ".gstack" / "core" / "bin" / "sonradan-eklendi").exists()
