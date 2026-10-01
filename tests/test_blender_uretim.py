"""BLENDER-ARAC-2 K7: gpu_kilit · varlik_indir (sahte sunucu) · blender_pisir · kontur_profil · NodeToPython."""
import hashlib
import json
import os
import struct
import subprocess
import sys
import threading
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import numpy as np
import pytest

ARAC = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(ARAC))
import blender_cli as bc  # noqa: E402
import blender_oturum as bo  # noqa: E402
import blender_pisir as bp  # noqa: E402
import gpu_kilit as gk  # noqa: E402
import varlik_indir as vi  # noqa: E402

YARDIMCI = Path(__file__).with_name("blender_uretim_yardimci.py")
NTP = Path(os.environ.get("APPDATA", "")) / "Blender Foundation" / "Blender" / "5.2" / "extensions"
blender = pytest.mark.skipif(not Path(bo.BLENDER).is_file(), reason="Blender exe yok")


@pytest.fixture
def kilit(tmp_path, monkeypatch):
    monkeypatch.setattr(gk, "YOL", tmp_path / "gpu-kilit.json")


def calis(capsys, fn, argv):
    kod = fn(argv)
    return kod, json.loads(capsys.readouterr().out or "null")


# --- K1 gpu_kilit ---
def test_kilit_dolu_2(kilit, capsys):
    assert gk.al("gorsel_uret", os.getpid()) is None
    assert gk.main(["al", "blender_pisir", "--pid", str(os.getpid())]) == 2
    assert f"GPU şu işte: gorsel_uret (PID {os.getpid()})" in capsys.readouterr().out
    gk.birak("gorsel_uret")
    assert gk.durum() is None


def test_kilit_olu_pid_duser(kilit):
    p = subprocess.Popen([sys.executable, "-c", "pass"])
    p.wait()
    gk.YOL.write_text(json.dumps({"pid": p.pid, "is": "gorsel_uret", "baslangic": 0}), encoding="utf-8")
    assert gk.al("blender_pisir", os.getpid()) is None
    assert gk.durum()["is"] == "blender_pisir"


# --- K2 varlik_indir (sahte Poly Haven) ---
VERI = b"#?RADIANCE sahte hdr " * 500


class PH(BaseHTTPRequestHandler):
    istekler = []

    def do_GET(self):
        PH.istekler.append((self.path, self.headers.get("User-Agent", "")))
        taban = f"http://127.0.0.1:{self.server.server_port}"
        dogru = hashlib.md5(VERI).hexdigest()
        yanit = {"/info/studio_x": {"authors": {"Greg Zaal": "All"}},
                 "/info/bozuk": {"authors": {"Biri": "All"}},
                 "/files/studio_x": {"hdri": {"1k": {"hdr": {"url": f"{taban}/dl/studio_x_1k.hdr", "size": len(VERI),
                                                             "md5": dogru}}}},
                 "/files/bozuk": {"hdri": {"1k": {"hdr": {"url": f"{taban}/dl/bozuk_1k.hdr", "size": len(VERI),
                                                          "md5": "0" * 32}}}}}.get(self.path)
        govde = VERI if self.path.startswith("/dl/") else json.dumps(yanit).encode()
        self.send_response(200 if yanit or self.path.startswith("/dl/") else 404)
        self.end_headers()
        self.wfile.write(govde)

    def log_message(self, *_):
        pass


@pytest.fixture
def ph(tmp_path, monkeypatch):
    s = ThreadingHTTPServer(("127.0.0.1", 0), PH)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    monkeypatch.setattr(vi, "PH_API", f"http://127.0.0.1:{s.server_port}")
    monkeypatch.setattr(bo, "MASAUSTU", tmp_path / "Desktop")
    PH.istekler = []
    yield tmp_path / "Desktop"
    s.shutdown()


def test_varlik_yol_disi_2(ph):
    assert vi.main(["indir", "polyhaven", "studio_x", "--hedef", str(ph)]) == 2
    assert vi.main(["indir", "polyhaven", "studio_x", "--hedef", str(ph.parent / "disari")]) == 2
    assert PH.istekler == [] and not any(ph.parent.rglob("*.hdr"))


def test_varlik_ozet_uyusmazligi_1(ph):
    hedef = ph / "Kum" / "varlik"
    assert vi.main(["indir", "polyhaven", "bozuk", "--hedef", str(hedef)]) == 1
    assert not (hedef / "bozuk" / "bozuk_1k.hdr").exists() and not (hedef / "bozuk" / "bozuk.json").exists()


def test_varlik_json_alanlari(ph):
    hedef = ph / "Kum" / "varlik"
    assert vi.main(["indir", "polyhaven", "studio_x", "--hedef", str(hedef)]) == 0
    k = json.loads((hedef / "studio_x" / "studio_x.json").read_text(encoding="utf-8"))
    assert k["kaynak_sayfa"] == "https://polyhaven.com/a/studio_x" and k["lisans"] == "CC0"
    assert k["yazar"] == "Greg Zaal" and k["tarih"] and "Powered by Poly Haven" in k["not"]
    d = k["dosyalar"][0]
    assert d["sha256"] == hashlib.sha256(VERI).hexdigest() and d["api_ozet"] == hashlib.md5(VERI).hexdigest()
    assert (hedef / "studio_x" / "studio_x_1k.hdr").read_bytes() == VERI
    assert all("omer-skills" in ua for _, ua in PH.istekler)


# --- K3 blender_pisir ---
@pytest.fixture(scope="module")
def pisir_sahne(tmp_path_factory):
    kok = tmp_path_factory.mktemp("pisir")
    blend = kok / "Kum" / "blender" / "pisir.blend"
    blend.parent.mkdir(parents=True)
    assert bc.calistir(YARDIMCI, {"tur": "pisir", "cikti": str(blend)}, zaman_asimi=120)[0] == 0
    return kok, blend


@pytest.fixture
def masaustu(pisir_sahne, kilit, monkeypatch):
    monkeypatch.setattr(bo, "MASAUSTU", pisir_sahne[0])
    return pisir_sahne[1]


def oku(blend, goruntu=None):
    kod, s, _ = bc.calistir(YARDIMCI, {"tur": "oku", "goruntu": goruntu}, blend=blend, zaman_asimi=120)
    assert kod == 0
    return s


@blender
def test_pisir_isik(masaustu, capsys):
    once = hashlib.sha256(masaustu.read_bytes()).hexdigest()
    o0 = oku(masaustu)
    kod, s = calis(capsys, bp.main, [str(masaustu), "--mod", "isik"])
    assert kod == 0, s
    assert s["uv_kanal"] == "LightMap" and s["lightMapIntensity"] >= 1 and s["sure_sn"] > 0
    o = oku(masaustu.with_name("pisir-pismis.blend"), s["goruntuler"][0])
    assert o["Kup"]["olcek"] == [1, 1, 1] and o["Kup"]["boyut"] == [2, 4, 1]
    assert o["Kup"]["uv"] == ["UVMap", "LightMap"] and o["Kup"]["uv1"] == o0["Kup"]["uv1"]
    assert "LightMap" in o["Zemin"]["uv"]
    assert o["goruntu"]["maks"] > 0.1 and 0.05 < o["goruntu"]["ort"] < 0.95
    assert hashlib.sha256(masaustu.read_bytes()).hexdigest() == once


@blender
def test_pisir_ao_tek_nesne(masaustu, capsys):
    kod, s = calis(capsys, bp.main, [str(masaustu), "--mod", "ao", "--nesneler", "Kup"])
    assert kod == 0 and s["nesneler"] == ["Kup"], s
    o = oku(masaustu.with_name("pisir-pismis.blend"), s["goruntuler"][0])
    assert "LightMap" in o["Kup"]["uv"] and "LightMap" not in o["Zemin"]["uv"]
    assert o["goruntu"]["maks"] > 0.1


@blender
def test_pisir_kilit_dolu_2(masaustu, capsys):
    assert gk.al("gorsel_uret", os.getpid()) is None
    assert bp.main([str(masaustu), "--mod", "ao"]) == 2
    assert "GPU şu işte: gorsel_uret" in capsys.readouterr().out


# --- K4 kontur_profil (uv betik ortamı, opencv) ---
def png(yol, m, alfa=True):
    """Bağımlılıksız PNG: alfa → RGBA (gövde opak), değilse gri (siyah gövde, beyaz zemin)."""
    h, w = m.shape
    px = (np.where(m[..., None], [0, 0, 0, 255], [0, 0, 0, 0]) if alfa else np.where(m, 0, 255)).astype(np.uint8)
    ham = zlib.compress(b"".join(b"\x00" + px[y].tobytes() for y in range(h)))
    parca = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))  # noqa: E731
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6 if alfa else 0, 0, 0, 0)
    yol.write_bytes(b"\x89PNG\r\n\x1a\n" + parca(b"IHDR", ihdr) + parca(b"IDAT", ham) + parca(b"IEND", b""))


def siluet(ad):
    if ad == "silindir":  # 600 px = 60 mm, yarıçap 150 px = 15 mm, eksen 249.5
        m = np.zeros((700, 500), bool)
        m[50:650, 100:400] = True
        return m, False
    m = np.zeros((700, 700), bool)  # fincan: 500 px = 80 mm, ağız yarıçapı 150 px = 24 mm, ayak 90 px, eksen 299.5
    for y in range(100, 600):
        r = 90 if y >= 560 else round(150 - 40 * (y - 100) / 459)
        m[y, 300 - r:300 + r] = True
    if ad == "kulplu":  # sağda C kulp, gövdeye bitişik
        m[220:420, 420:520] = True
        m[250:390, 450:505] = False
    return m, True


@blender
@pytest.mark.parametrize("ad,yuk,yar,eksen,kulp", [("silindir", 60, 15, 249.5, "yok"), ("fincan", 80, 24, 299.5, "yok"),
                                                  ("kulplu", 80, 24, 299.5, "sag")])
def test_kontur_profil(tmp_path, ad, yuk, yar, eksen, kulp):
    m, alfa = siluet(ad)
    png(tmp_path / f"{ad}.png", m, alfa)
    blend = tmp_path / "Desktop" / "Kum" / "blender" / f"{ad}.blend"
    blend.parent.mkdir(parents=True)
    p = subprocess.run(["uv", "run", "-q", str(ARAC / "kontur_profil.py"), str(tmp_path / f"{ad}.png"),
                        "--yukseklik-mm", str(yuk), "--kulp", kulp, "--blend", str(blend)],
                       capture_output=True, text=True, encoding="utf-8", timeout=900,
                       env={**os.environ, "USERPROFILE": str(tmp_path)})  # Desktop = tmp_path\Desktop
    assert p.returncode == 0, p.stdout[-800:] + p.stderr[-1500:]
    s = json.loads(p.stdout.strip().splitlines()[-1])
    assert abs(s["yukseklik_mm"] - yuk) <= 0.01 * yuk and abs(s["yaricap_mm"] - yar) <= 0.02 * yar, s
    assert abs(s["eksen_px"] - eksen) <= 1 and s["iou"] >= 0.95, s


# --- K5 NodeToPython ---
@blender
@pytest.mark.skipif(not any(NTP.glob("*/node_to_python")), reason="NodeToPython kurulu değil")
def test_nodetopython_tarif(tmp_path):
    kod, s, _ = bc.calistir(YARDIMCI, {"tur": "ntp", "cikti": str(tmp_path / "tarif.py")}, zaman_asimi=180)
    assert kod == 0 and s["gecti"], s
    assert s["sonra"] == s["once"] and s["kod_satir"] > 10
