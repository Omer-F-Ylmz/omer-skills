import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import video_derin  # noqa: E402


@pytest.fixture
def atla(tmp_path, monkeypatch):
    dosya = tmp_path / "video-atla.txt"
    dosya.write_text("KALICI1\n", encoding="utf-8")
    monkeypatch.setattr(video_derin, "ATLA_DOSYA", dosya)
    return dosya


def test_atla_listesindeki_video_indirilmeden_atlanir(atla, monkeypatch):
    monkeypatch.setattr(video_derin, "indir", lambda *a: pytest.fail("indirme çağrılmamalı"))
    assert video_derin.isle("https://www.youtube.com/watch?v=KALICI1") == ("KALICI1", "atla")


def test_format_yok_hatasi_kalici_atla_listesine_yazilir(atla, monkeypatch):
    monkeypatch.setattr(video_derin, "indir", lambda url, d: (None, "ERROR: No video formats found!"))
    assert video_derin.isle("https://www.youtube.com/watch?v=YENI123") == ("YENI123", "atla")
    assert "YENI123" in atla.read_text(encoding="utf-8").split()


def test_kareler_sahne_degisiminde_kare_secer(tmp_path):
    v = tmp_path / "v.mp4"
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=red:s=160x120:d=2", "-f", "lavfi", "-i", "color=c=blue:s=160x120:d=2",
                    "-filter_complex", "[0][1]concat=n=2:v=1:a=0", str(v)], check=True, capture_output=True)
    d = tmp_path / "kare"
    d.mkdir()
    assert len(video_derin.kareler(v, d)) == 2  # ilk kare + renk değişimi; fps=2 olsaydı 8


def test_gecici_indirme_hatasi_atla_listesine_yazilmaz(atla, monkeypatch):
    monkeypatch.setattr(video_derin, "indir", lambda url, d: (None, "ERROR: HTTP Error 503"))
    kod, durum = video_derin.isle("https://www.youtube.com/watch?v=GECICI1")
    assert durum.startswith("indirilemedi")
    assert "GECICI1" not in atla.read_text(encoding="utf-8").split()


def test_groq_anahtar_yoksa_none_doner(monkeypatch, tmp_path):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    wav = tmp_path / "a.wav"
    wav.write_bytes(b"x")
    assert video_derin.groq_asr(wav) is None


def test_groq_kota_kapaliyken_istek_atilmaz(monkeypatch, tmp_path):
    monkeypatch.setenv("GROQ_API_KEY", "x")
    monkeypatch.setitem(video_derin.groq_durum, "kapali", 9e18)
    wav = tmp_path / "a.wav"
    wav.write_bytes(b"x")
    monkeypatch.setattr(video_derin.urllib.request, "urlopen", lambda *a, **k: pytest.fail("istek atilmamali"))
    assert video_derin.groq_asr(wav) is None


def test_cerez_yalniz_instagram_icin_ve_dosya_varsa(tmp_path, monkeypatch):
    c = tmp_path / "c.txt"
    monkeypatch.setenv("IG_COOKIES", str(c))
    assert video_derin.cerez_arg("https://www.instagram.com/reel/X/") == []
    c.write_text("x")
    assert video_derin.cerez_arg("https://www.instagram.com/reel/X/") == ["--cookies", c]
    assert video_derin.cerez_arg("https://youtu.be/X") == []


def test_genel_python_gpu_venve_yonlenir(tmp_path, monkeypatch):
    gpu = tmp_path / "Scripts" / "python.exe"
    gpu.parent.mkdir()
    gpu.write_text("")
    cagri = []
    monkeypatch.setattr(video_derin, "GPU_PY", gpu)
    monkeypatch.setattr(subprocess, "call", lambda cmd, **kw: cagri.append(cmd) or 0)
    monkeypatch.setattr(sys, "argv", ["video_derin.py", "--en", "1"])
    with pytest.raises(SystemExit) as e:
        video_derin.main()
    assert e.value.code == 0 and cagri == [[str(gpu), "video_derin.py", "--en", "1"]]
