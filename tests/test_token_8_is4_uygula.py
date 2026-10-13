import importlib.util, json, os, shutil, subprocess
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("token_8_is4_uygula", KOK / "onay" / "token_8_is4_uygula.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SP = b"""#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
escape_for_json() {
    local s="$1"
    s="${s//\\\\/\\\\\\\\}"
    s="${s//\\"/\\\\\\"}"
    s="${s//$'\\n'/\\\\n}"
    printf '%s' "$s"
}
session_context="<EXTREMELY_IMPORTANT>\\nuzun metin\\n</EXTREMELY_IMPORTANT>"
printf '{"hookSpecificOutput": {"additionalContext": "%s"}}\\n' "$session_context"
"""
CM = b"async function f() {\n  let additionalContext = ROUTING_BLOCK;\n  return additionalContext;\n}\n"


def test_uygula_kisaltir_geri_tam_doner(tmp_path):
    ev = tmp_path / ".claude"
    sp = ev / "plugins/cache/claude-plugins-official/superpowers/9.9/hooks/session-start"
    cm = ev / "plugins/cache/context-mode/context-mode/9.9/hooks/sessionstart.mjs"
    for p, b in ((sp, SP), (cm, CM)):
        p.parent.mkdir(parents=True)
        p.write_bytes(b)

    assert m.main(["--kuru"], ev) == 0 and sp.read_bytes() == SP and cm.read_bytes() == CM
    assert m.main(["uygula"], ev) == 0
    assert m.main(["uygula"], ev) == 0  # ikinci koşu: zaten yamalı, yedek ezilmez
    assert b"\r" not in sp.read_bytes()
    assert json.dumps(m.KISA_CM).encode() in cm.read_bytes()
    bash = shutil.which("bash")
    if bash:
        cikti = subprocess.run([bash, sp.as_posix()], capture_output=True, check=True).stdout
        assert json.loads(cikti)["hookSpecificOutput"]["additionalContext"] == m.KISA_SP

    assert m.main(["--geri"], ev) == 0
    assert sp.read_bytes() == SP and cm.read_bytes() == CM
    assert not (sp.parent / "token8-kisa.md").exists()


def test_capa_yoksa_dokunmaz(tmp_path):
    ev = tmp_path / ".claude"
    cm = ev / "plugins/cache/context-mode/context-mode/9.9/hooks/sessionstart.mjs"
    cm.parent.mkdir(parents=True)
    cm.write_bytes(b"degismis\n")
    assert m.main(["uygula"], ev) == 1
    assert cm.read_bytes() == b"degismis\n" and not list(cm.parent.glob("*.token8-yedek"))
