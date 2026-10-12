"""animasyon-atolyesi: SKILL.md'deki tarifler var, olc.glb sayar, video tarifi istenen mp4'ü üretir."""
import json
import re
import shutil
import struct
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1] / "skills" / "animasyon-atolyesi"
sys.path.insert(0, str(SKILL))
import olc  # noqa: E402


def test_tarifler_var():
    adlar = re.findall(r"`tarifler/([\w.-]+)`", (SKILL / "SKILL.md").read_text(encoding="utf-8"))
    assert len(adlar) == 5
    for ad in adlar:
        assert (SKILL / "tarifler" / ad).is_file(), ad


def test_glb_sayar(tmp_path):
    j = json.dumps({"meshes": [{}, {}], "animations": [{"channels": [{}, {}, {}]}]}).encode()
    j += b" " * (-len(j) % 4)
    p = tmp_path / "a.glb"
    p.write_bytes(struct.pack("<4sII", b"glTF", 2, 20 + len(j)) + struct.pack("<I4s", len(j), b"JSON") + j)
    assert olc.glb(p) == {"gecerli": True, "animasyon": 1, "kanal": 3, "mesh": 2, "kb": 0.1}
    p.write_bytes(b"xxxx" + bytes(16))
    assert olc.glb(p) == {"gecerli": False}


@pytest.mark.parametrize("ad", ["giris-scroll.html", "sayfa-gecisi.html", "parcacik-three.html"])
def test_uyarla(tmp_path, ad):
    import uyarla
    hedef = tmp_path / "index.html"
    ayar = uyarla.uyarla(ad, hedef, {"renk": {"vurgu": "#8b4513"}, "metin": {"baslik": "Telve"}, "yeni": [1]})
    assert ayar["metin"]["baslik"] == "Telve" and ayar["yeni"] == [1]
    assert len(ayar["metin"]) > 1  # derin birleştirme: verilmeyen anahtarlar kalır
    s = hedef.read_text(encoding="utf-8")
    assert "<title>Telve</title>" in s and uyarla.oku(s) == ayar


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="ffmpeg yok")
def test_video_intro(tmp_path):
    mp4 = tmp_path / "x.mp4"
    subprocess.run([sys.executable, str(SKILL / "tarifler" / "video_intro.py"), "--baslik", "Deneme", "--alt", "alt",
                    "--cikti", str(mp4), "--sure", "2", "--en", "320", "--boy", "180", "--fps", "24"],
                   check=True, capture_output=True, timeout=120)
    o = olc.video(mp4, tmp_path)
    assert (o["en"], o["boy"], o["fps"], o["sure_sn"], o["dolu"]) == (320, 180, 24.0, 2.0, True)
