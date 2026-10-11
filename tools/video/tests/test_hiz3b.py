"""VİDEO-HIZ-3b: AV1 goz-video çözmesi NVDEC (cuda + format=yuv420p) — hwaccel başlatılamazsa aynı komut eski yolla; SAHNE semaforu 2."""
from pathlib import Path

import pytest
from test_goz_r import _goz_sahte

from video import cli
from video import goz as gz

HW = ["-hwaccel", "cuda", "-c:v", "av1"]


def _kur(tmp_path, monkeypatch, probe, hw_hata=False, hata_bayrak="-hwaccel"):
    """_goz'u koşar; ffmpeg çağrıları (argüman, filter_complex betiği) sırayla döner. probe: ffprobe (rc, çıktı).
    hw_hata: hata_bayrak'lı ffmpeg rc 1 döner."""
    ctx, d, _ = _goz_sahte(tmp_path, monkeypatch, {0.0: ["Cursor editor opens the terminal window"], 10.0: ["Supabase console creates a new database"]})
    monkeypatch.setattr(gz, "yogun_zaman", lambda *a: [5.0])
    asil, cagri = ctx["kos"], []

    def kos(a, timeout=None):
        if a[0] == "ffprobe":
            return probe[0], probe[1], b""
        if a[0] == "ffmpeg" and a[a.index("-i") + 1].endswith("goz-video.mp4"):
            cagri.append((list(a), Path(a[a.index("-/filter_complex") + 1]).read_text() if "-/filter_complex" in a else None))
            if hw_hata and hata_bayrak in a:
                return 1, b"", b"No device available for decoder"
        return asil(a, timeout)
    ctx["kos"] = kos
    cli._goz(ctx, d, 30, "", [0.0], 2, {})
    return cagri


def test_av1_dhash_kare_ss_cuda_format(tmp_path, monkeypatch):
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"))
    dh, fc, ss = ([a for a, g in c if k(a, g)] for k in (lambda a, g: "rawvideo" in a, lambda a, g: g, lambda a, g: "-ss" in a))
    assert dh and fc and ss
    assert all(a[a.index("-i") - 4:a.index("-i")] == HW for a, g in c if not g)
    assert dh[0][dh[0].index("-vf") + 1].startswith("format=yuv420p,fps=")
    assert "-vf" not in ss[0]  # -ss karesi ölçülen yol: süzgeçsiz


def test_kare_cikar_cuda_cikis_kodlayici_tek_is_parcacigi(tmp_path, monkeypatch):
    """VİDEO-10: kare çıkarma kareleri GPU'da tutar (hwdownload) ve dal başı mjpeg kodlayıcı -threads 1 — 10 dk 9 sa AV1 kesitte
    tepe özel bellek 3.57 → 0.66 GB, süre 48 → 25 sn, 300 kare md5 aynı."""
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"))
    a, g = next((a, g) for a, g in c if g)
    assert a[a.index("-i") - 6:a.index("-i")] == HW + ["-hwaccel_output_format", "cuda"]
    assert g.startswith("[0:v]hwdownload,format=nv12,format=yuv420p,fps=")
    assert a.count("-map") == a.count("-threads") and all(a[i + 1] == "1" for i, x in enumerate(a) if x == "-threads")


def test_hw_baslatilamazsa_ayni_komut_eski_yolla(tmp_path, monkeypatch):
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"), hw_hata=True)
    assert len(c) >= 6 and ["-hwaccel" in a for a, _ in c] == [i % 2 == 0 for i in range(len(c))]
    for (hw, _), (sw, gsw) in zip(c[::2], c[1::2]):
        assert hw[-1] == sw[-1] and not any("format=yuv420p," in x for x in sw) and (gsw is None or gsw.startswith("[0:v]fps="))
    assert c[1][0][c[1][0].index("-vf") + 1].startswith("fps=")
    sw = next(a for a, g in c[1::2] if g)  # VİDEO-11: kare çıkarmanın eski yolu cuda çıkışsız, -threads 1 ve -start_number korunur
    assert "-hwaccel_output_format" not in sw and sw.count("-map") == sw.count("-threads") == sw.count("-start_number")


def test_10bit_cuda_cikis_hatasi_yalniz_kare_cikarma_eski_yola_duser(tmp_path, monkeypatch):
    """VİDEO-11: 10-bit (p010) kare hwdownload,format=nv12'de hata verir → yalnız o komut eski yolla; dhash GPU'da kalır."""
    c = _kur(tmp_path, monkeypatch, (0, b"av1\n"), hw_hata=True, hata_bayrak="-hwaccel_output_format")
    i = next(i for i, (a, g) in enumerate(c) if g)
    (hw, ghw), (sw, gsw) = c[i], c[i + 1]
    assert "-hwaccel_output_format" in hw and ghw.startswith("[0:v]hwdownload,")
    assert "-hwaccel" not in sw and gsw.startswith("[0:v]fps=") and hw[-1] == sw[-1]
    assert sw.count("-map") == sw.count("-threads") == sw.count("-start_number")
    assert all(a[a.index("-i") - 4:a.index("-i")] == HW for a, g in c if not g)  # dhash / -ss yolu cuda'da kaldı


@pytest.mark.parametrize("probe", [(0, b"h264\n"), (0, b"vp9\n"), (1, b"")])
def test_av1_degilse_veya_ffprobe_hatasi_eski_yol(tmp_path, monkeypatch, probe):
    c = _kur(tmp_path, monkeypatch, probe)
    assert c and not any("-hwaccel" in a for a, _ in c)


def test_sahne_semaforu_2_ocr_1():
    assert (cli.SAHNE._value, cli.OCR._value) == (2, 1)
