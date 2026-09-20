"""gstack-core/bin/browse shim testleri -- hepsi agsiz, yerel file:// sayfasi uzerinde."""
import os
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parents[1]
SHIM = KOK / "tools" / "gstack_browse.py"
SAYFA = (KOK / "tests" / "fixtures" / "sayfa.html").as_uri()


@pytest.fixture(scope="module")
def ev(tmp_path_factory):
    """Testlere ozel, izole bir browse durum dizini; sonunda sunucuyu kapatir."""
    d = tmp_path_factory.mktemp("browse-ev")
    ortam = dict(os.environ, GSTACK_BROWSE_HOME=str(d))
    yield ortam
    kos("stop", ortam=ortam)


def kos(*args, ortam=None):
    return subprocess.run(
        [sys.executable, str(SHIM), *args],
        capture_output=True, text=True, timeout=180,
        env=ortam if ortam is not None else os.environ,
    )


def ref(cikti, metin):
    """snapshot ciktisindan, icinde `metin` gecen satirin @eN referansini cikarir."""
    import re
    for satir in cikti.splitlines():
        if metin in satir:
            m = re.search(r"@e\d+", satir)
            if m:
                return m.group(0)
    raise AssertionError("referans bulunamadi: %r icinde %r" % (cikti, metin))


def test_goto_ve_url(ev):
    assert kos("goto", SAYFA, ortam=ev).returncode == 0
    r = kos("url", ortam=ev)
    assert r.returncode == 0
    assert "sayfa.html" in r.stdout


def test_snapshot_referans_uretir(ev):
    kos("goto", SAYFA, ortam=ev)
    r = kos("snapshot", "-i", ortam=ev)
    assert r.returncode == 0
    assert "@e1" in r.stdout
    assert "Gonder" in r.stdout


def test_click_dom_degistirir(ev):
    kos("goto", SAYFA, ortam=ev)
    snap = kos("snapshot", "-i", ortam=ev).stdout
    assert kos("click", ref(snap, "Gonder"), ortam=ev).returncode == 0
    assert "TIKLANDI" in kos("text", ortam=ev).stdout


def test_fill_deger_yazar(ev):
    kos("goto", SAYFA, ortam=ev)
    snap = kos("snapshot", "-i", ortam=ev).stdout
    assert kos("fill", ref(snap, "ad"), "abc", ortam=ev).returncode == 0
    assert "abc" in kos("js", "document.getElementById('ad').value", ortam=ev).stdout


def test_text_sayfa_metnini_dondurur(ev):
    kos("goto", SAYFA, ortam=ev)
    r = kos("text", ortam=ev)
    assert r.returncode == 0
    assert "SAYFA_ISARETCISI" in r.stdout


def test_screenshot_png_yazar(ev, tmp_path):
    kos("goto", SAYFA, ortam=ev)
    hedef = tmp_path / "vurus.png"
    assert kos("screenshot", str(hedef), ortam=ev).returncode == 0
    assert hedef.exists()
    assert hedef.read_bytes()[:4] == b"\x89PNG"


def test_console_mesaji_yakalar(ev):
    kos("goto", SAYFA, ortam=ev)
    r = kos("console", ortam=ev)
    assert r.returncode == 0
    assert "KONSOL_ISARETCISI" in r.stdout


def test_js_degerlendirir(ev):
    kos("goto", SAYFA, ortam=ev)
    r = kos("js", "1+1", ortam=ev)
    assert r.returncode == 0
    assert "2" in r.stdout


def test_links_baglari_listeler(ev):
    kos("goto", SAYFA, ortam=ev)
    r = kos("links", ortam=ev)
    assert r.returncode == 0
    assert "ornek.test/bir" in r.stdout


def test_kapsam_disi_komut_exit_2(ev):
    r = kos("handoff", ortam=ev)
    assert r.returncode == 2
    assert "desteklenmez" in (r.stdout + r.stderr)


def test_durum_cagrilar_arasi_korunur(ev):
    """Ayri iki surec: goto'dan sonra yeni bir surec ayni sayfayi gormeli."""
    kos("goto", SAYFA, ortam=ev)
    snap = kos("snapshot", "-i", ortam=ev).stdout
    kos("click", ref(snap, "Gonder"), ortam=ev)
    assert "TIKLANDI" in kos("text", ortam=ev).stdout
    assert "sayfa.html" in kos("url", ortam=ev).stdout
