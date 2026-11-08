"""BASLANGIC-HIZ-2 P4: tools/mod_yama.py — gerçek mod kopyasında uygula → geri bayt bayt aynı."""
import shutil
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "tools"))
import mod_yama as y  # noqa: E402

GERCEK = y.MODS
pytestmark = pytest.mark.skipif(not GERCEK.is_dir(), reason="claude-code-mods kurulu değil")


@pytest.fixture
def kopya(tmp_path):
    mods = tmp_path / "mods"
    for m in y.modlar(GERCEK):
        hedef = mods / m / "hooks"
        hedef.mkdir(parents=True)
        p = y.dosya(GERCEK, m)
        shutil.copyfile(p, hedef / p.name)
    return mods, tmp_path / "kayit.json", tmp_path / "yedek"


def anlik(mods):
    return {p: p.read_bytes() for p in mods.rglob("register.ts*")}


def test_uygula_geri_bayt_bayt_ayni(kopya):
    mods, kayit, yedek = kopya
    once = anlik(mods)
    y.uygula(mods, kayit, yedek)
    sonra = anlik(mods)
    yamali = [p for p in once if once[p] != sonra[p]]
    assert yamali, "hiçbir mod yamalanmadı"
    for p in yamali:
        t = sonra[p].decode("utf8")
        assert t.count("cmdRegistered") >= 3 and "$.command.register" in t
        assert t.count("$.command.register") == 1
        assert (b"\r\n" in once[p]) == (b"\r\n" in sonra[p])
    y.geri(mods, kayit, yedek)
    assert anlik(mods) == once
    assert y.yukle(kayit) == {}


def test_uygula_idempotent(kopya):
    mods, kayit, yedek = kopya
    y.uygula(mods, kayit, yedek)
    bir = anlik(mods)
    y.uygula(mods, kayit, yedek)
    assert anlik(mods) == bir


def test_guncellenmis_mod_geride_dokunulmaz(kopya):
    mods, kayit, yedek = kopya
    y.uygula(mods, kayit, yedek)
    mod = next(iter(y.yukle(kayit)))
    p = mods / mod / "hooks" / y.yukle(kayit)[mod]["dosya"]
    p.write_bytes(p.read_bytes() + b"\n// marketplace guncellemesi\n")
    kirli = p.read_bytes()
    y.geri(mods, kayit, yedek)
    assert p.read_bytes() == kirli


def test_kalip_tutmayan_atlanir():
    yeni, neden = y.yamala("export const register: Register = () => {}\n")
    assert yeni is None and neden
