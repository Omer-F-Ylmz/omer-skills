"""BLENDER-ARAC-1 K5: blender_bekci — yasak kategoriler, izinli örnekler, proje dışı yol, hook stdin."""
import json
import subprocess
import sys
import time
from pathlib import Path

import pytest

ARAC = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(ARAC))
import blender_bekci as bk  # noqa: E402

DIS = "C:/Windows/Temp"
ICI = (Path.home() / "Desktop" / "Proje" / "render.png").as_posix()
DUZELT = "mutlak yol yaz: " + str(Path.home() / "Desktop")

YASAK = {
    "silme": ["import os\nos.remove('a.txt')", "import os as o\no.unlink('a')", "from os import rmdir",
              "from pathlib import Path\nPath('a').unlink()", "import shutil\nshutil.rmtree('a')",
              "import shutil\nshutil.move('a', 'b')"],
    "surec": ["import subprocess", "import os\nos.system('dir')", "import os\nos.popen('dir')", "import ctypes"],
    "ag": ["import socket", "import urllib.request", "import requests", "import http.client", "from http import client"],
    "dinamik": ["exec('x=1')", "eval('1')", "compile('1', 'a', 'eval')", "__import__('os')",
                "import os\ngetattr(os, 'sys' + 'tem')('dir')", "import os\ngetattr(os, 'remove')('a')"],
    "yol": [f"open('{DIS}/x.txt', 'w')", "open(yol, 'w')",
            f"bpy.ops.wm.save_as_mainfile(filepath='{DIS}/a.blend')",
            f"bpy.ops.export_scene.gltf(filepath='{DIS}/a.glb')",
            f"bpy.context.scene.render.filepath = '{DIS}/r.png'",
            f"bpy.data.images['x'].save_render('{DIS}/r.png')",
            "bpy.ops.render.render(write_still=True)"],
}
IZINLI = [
    "import bpy\nbpy.ops.mesh.primitive_cube_add(size=2)",
    "bpy.data.objects.remove(bpy.data.objects['Kup'])",
    "bpy.context.scene.collection.objects.unlink(o)",
    f"bpy.context.scene.render.filepath = '{ICI}'\nbpy.ops.render.render(write_still=True)",
    f"open('{ICI}', 'w').write('x')",
    "open('C:/Windows/win.ini').read()",
    "bpy.ops.wm.save_mainfile()",
    "import math, json\nprint(json.dumps({'a': math.pi}))",
    "bpy.ops.import_scene.gltf(filepath='C:/indir/x.glb')",
]


@pytest.mark.parametrize("kod", [k for v in YASAK.values() for k in v])
def test_yasak_tek_satir_sebep_ve_duzeltme(kod):
    sebep = bk.denetle(kod)
    assert sebep and "→" in sebep and "\n" not in sebep


@pytest.mark.parametrize("kod", IZINLI)
def test_izinli(kod):
    assert bk.denetle(kod) is None


def test_proje_disi_yol_duzeltme_yolu():
    sebep = bk.denetle(f"bpy.context.scene.render.filepath = '{DIS}/r.png'")
    assert "Desktop" in sebep and DUZELT in sebep


def test_libraries_write_red_ve_duzeltme_yolu():
    # Blender 5.2.1: Scene içeren libraries.write → bpy_lib_write/scene_copy_data çökmesi (B-fincan-v3.crash.txt)
    sebep = bk.denetle("bpy.data.libraries.write('//kopya.blend', {bpy.context.scene})")
    assert sebep and "libraries.write" in sebep and "save_as_mainfile" in sebep and "copy=True" in sebep
    assert bk.denetle(f"bpy.ops.wm.save_as_mainfile(filepath='{ICI}', copy=True)") is None


def test_cift_egik_ve_goreli_yol_red_mutlak_izin(monkeypatch):
    kayit = "bpy.ops.wm.save_as_mainfile(filepath='{}', copy=True)"
    assert bk.denetle(kayit.format((Path.home() / "Desktop" / "Proje" / "x.blend").as_posix())) is None
    # hook cwd'si Desktop\<Proje> altında olsa da göreli yolu Blender kendi cwd'sine yazar
    monkeypatch.setattr(bk.bc, "proje_ici", lambda y: True)
    sebep = bk.denetle(kayit.format("x.blend"))
    assert sebep and DUZELT in sebep
    # Blender 5.2 save_as_mainfile // genişletmez, dosyayı kendi cwd'sine yazar: proje_ici geçse de red
    monkeypatch.setattr(bk.bc, "proje_ici", lambda _: True)
    assert DUZELT in bk.denetle(kayit.format("//x.blend"))
    assert DUZELT in bk.denetle("bpy.context.scene.render.filepath = '//r.png'")


def test_hook_stdin_red_izin_ve_hiz():
    bekci = [sys.executable, "-S", str(ARAC / "blender_bekci.py")]
    girdi = {"tool_name": "mcp__blender__execute_blender_code", "tool_input": {"code": f"open('{DIS}/x.txt', 'w')"}}
    r = subprocess.run(bekci, input=json.dumps(girdi), capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 2 and DUZELT in r.stderr and len(r.stderr.strip().splitlines()) == 1
    ok = subprocess.run(bekci, input=json.dumps({"tool_input": {"code": "import bpy"}}),
                        capture_output=True, text=True, encoding="utf-8")
    assert ok.returncode == 0 and ok.stderr == ""
    t = time.perf_counter()
    assert bk.denetle(("\n".join(IZINLI) + "\n") * 20) is None
    assert time.perf_counter() - t < 0.1
