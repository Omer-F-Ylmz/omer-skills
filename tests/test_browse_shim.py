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


# --- KURULUM-9c: stop/yeniden baglanma, bilinmeyen @ref, argumansiz yol ---

import importlib.util
import socket
import threading
import time

_spec = importlib.util.spec_from_file_location("gstack_browse", SHIM)
_sb = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_sb)


def test_stop_sonrasi_komut_hemen_calisir(tmp_path_factory):
    """stop -> hemen komut: 5 ardisik dongude 5/5 exit 0, traceback yok."""
    d = tmp_path_factory.mktemp("browse-stop")
    ortam = dict(os.environ, GSTACK_BROWSE_HOME=str(d))
    try:
        for tur in range(5):
            assert kos("goto", SAYFA, ortam=ortam).returncode == 0, tur
            assert kos("stop", ortam=ortam).returncode == 0, tur
            r = kos("url", ortam=ortam)
            assert r.returncode == 0, "tur %d: %s" % (tur, r.stderr)
            assert "Traceback" not in r.stderr, r.stderr
    finally:
        kos("stop", ortam=ortam)


def test_bilinmeyen_ref_beklemeden_hata(ev):
    kos("goto", SAYFA, ortam=ev)
    bas = time.time()
    r = kos("click", "@e999", ortam=ev)
    assert r.returncode == 1
    assert time.time() - bas < 2.0
    assert "@e999 yok" in (r.stdout + r.stderr)
    assert "snapshot -i" in (r.stdout + r.stderr)


def test_argumansiz_screenshot_istemci_cwdsine_yazar(ev, tmp_path):
    kos("goto", SAYFA, ortam=ev)
    r = subprocess.run([sys.executable, str(SHIM), "screenshot"], cwd=str(tmp_path),
                       capture_output=True, text=True, timeout=180, env=ev)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "screenshot.png").exists()


def test_yavas_yanitta_yeniden_baslatmaz(tmp_path_factory):
    """socket.timeout yeniden baslatma tetiklemez: tek baglanti, komut bir kez islenir."""
    d = tmp_path_factory.mktemp("browse-yavas")
    if _sb.unix_soket_var():
        srv = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        srv.bind(str(d / "browse.sock"))
    else:
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind(("127.0.0.1", 0))
        (d / "browse.port").write_text(str(srv.getsockname()[1]), encoding="utf-8")
    srv.listen(4)
    baglantilar = []

    def dinle():
        while True:
            try:
                c, _ = srv.accept()
            except OSError:
                return
            baglantilar.append(1)
            time.sleep(3)          # istemci zaman asimi 1 sn
            try:
                c.close()
            except OSError:
                pass

    threading.Thread(target=dinle, daemon=True).start()
    ortam = dict(os.environ, GSTACK_BROWSE_HOME=str(d), GSTACK_BROWSE_TIMEOUT="1")
    try:
        r = kos("url", ortam=ortam)
    finally:
        srv.close()
    assert r.returncode == 1
    assert "Traceback" not in r.stderr, r.stderr
    assert baglantilar == [1], "yeniden baslatildi: %d baglanti" % len(baglantilar)


# --- KURULUM-9d: snapshot bayraklari + viewport ---

@pytest.fixture
def tek_ev(tmp_path_factory):
    """Tek teste ozel sunucu: -D'nin 'onceki snapshot yok' durumu paylasilmaz."""
    d = tmp_path_factory.mktemp("browse-tek")
    ortam = dict(os.environ, GSTACK_BROWSE_HOME=str(d))
    yield ortam
    kos("stop", ortam=ortam)


def test_bayraksiz_snapshot_da_isaretler(ev):
    kos("goto", SAYFA, ortam=ev)
    snap = kos("snapshot", ortam=ev).stdout
    r = kos("click", ref(snap, "Gonder"), ortam=ev)
    assert r.returncode == 0, r.stderr
    assert "TIKLANDI" in kos("text", ortam=ev).stdout


def test_i_bayragi_listeyi_etkilesimliye_daraltir(ev):
    kos("goto", SAYFA, ortam=ev)
    genis = kos("snapshot", ortam=ev).stdout
    dar = kos("snapshot", "-i", ortam=ev).stdout
    assert "SAYFA_ISARETCISI" in genis
    assert "SAYFA_ISARETCISI" not in dar
    assert "Gonder" in genis and "Gonder" in dar


def test_a_bayragi_png_yazar_ve_overlay_birakmaz(ev, tmp_path):
    kos("goto", SAYFA, ortam=ev)
    hedef = tmp_path / "isaretli.png"
    r = kos("snapshot", "-i", "-a", "-o", str(hedef), ortam=ev)
    assert r.returncode == 0, r.stderr
    assert hedef.exists() and hedef.read_bytes()[1:4] == b"PNG"
    assert "@e1" in r.stdout
    assert r.stdout.strip().splitlines()[-1].endswith("isaretli.png")
    kalan = kos("js", "document.querySelectorAll('[data-gsoverlay]').length", ortam=ev)
    assert kalan.stdout.strip() == "0"


def test_a_bayragi_o_suz_istemci_cwdsine_yazar(ev, tmp_path):
    kos("goto", SAYFA, ortam=ev)
    r = subprocess.run([sys.executable, str(SHIM), "snapshot", "-a"], cwd=str(tmp_path),
                       capture_output=True, text=True, timeout=180, env=ev)
    assert r.returncode == 0, r.stderr
    assert (tmp_path / "annotated.png").exists()


def test_D_bayragi_fark_dondurur(tek_ev):
    kos("goto", SAYFA, ortam=tek_ev)
    ilk = kos("snapshot", "-D", ortam=tek_ev)
    assert ilk.returncode == 0, ilk.stderr
    assert "onceki snapshot yok" in ilk.stdout
    assert "Gonder" in ilk.stdout
    assert "fark yok" in kos("snapshot", "-D", ortam=tek_ev).stdout
    # araya baska bir snapshot girmez: saklanan metin karsilastirilan listeyle ayni kapsamda kalsin
    kos("click", ref(ilk.stdout, "Gonder"), ortam=tek_ev)
    fark = kos("snapshot", "-D", ortam=tek_ev).stdout
    assert any(s.startswith("+") and "TIKLANDI" in s for s in fark.splitlines()), fark
    assert any(s.startswith("-") and "baslangic" in s for s in fark.splitlines()), fark


def test_bilinmeyen_snapshot_bayragi_exit_2(ev):
    r = kos("snapshot", "-C", ortam=ev)
    assert r.returncode == 2
    assert "desteklenmez: -C" in (r.stdout + r.stderr)


def test_viewport_iki_bicimi_de_kabul_eder(ev):
    kos("goto", SAYFA, ortam=ev)
    assert kos("viewport", "375x812", ortam=ev).returncode == 0
    assert kos("js", "innerWidth", ortam=ev).stdout.strip() == "375"
    assert kos("viewport", "800", "600", ortam=ev).returncode == 0
    assert kos("js", "innerWidth", ortam=ev).stdout.strip() == "800"


def test_viewport_gecersiz_girdi_tek_satir_hata(ev):
    r = kos("viewport", "abc", ortam=ev)
    assert r.returncode == 1
    assert "Traceback" not in r.stderr
    assert len([s for s in r.stderr.splitlines() if s.strip()]) == 1, r.stderr
