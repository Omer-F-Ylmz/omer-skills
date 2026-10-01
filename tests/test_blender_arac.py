"""BLENDER-ARAC-1 K7: blender_cli · dogrula · gorunum · glb_hat · bpy_kontrol — gerçek Blender (exe yoksa atlanır)."""
import json
import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import blender_oturum as bo  # noqa: E402
import blender_cli as bc  # noqa: E402
import blender_dogrula as bd  # noqa: E402
import blender_gorunum as bg  # noqa: E402
import bpy_kontrol as bk  # noqa: E402
import glb_hat as gh  # noqa: E402

FIXTURE = Path(__file__).with_name("blender_fixture.py")
pytestmark = pytest.mark.skipif(not Path(bo.BLENDER).is_file(), reason="Blender exe yok")


@pytest.fixture(scope="module")
def sahne(tmp_path_factory):
    kok = tmp_path_factory.mktemp("masaustu")
    d = kok / "Proje" / "blender"
    d.mkdir(parents=True)
    for tur in ("hatali", "temiz", "cam"):
        args = {"tur": tur, "cikti": str(d / f"{tur}.blend")}
        if tur == "temiz":
            args["glb"] = str(kok / "Proje" / "kup.glb")
        assert bc.calistir(FIXTURE, args, zaman_asimi=120)[0] == 0
    return kok


@pytest.fixture
def masaustu(sahne, monkeypatch):
    monkeypatch.setattr(bo, "MASAUSTU", sahne)
    return sahne


def calis(capsys, fn, argv):
    kod = fn([str(x) for x in argv])
    return kod, json.loads(capsys.readouterr().out or "null")


# --- K1 blender_cli
def test_cli_zaman_asimi_sureci_kapatir(tmp_path):
    betik = tmp_path / "uyu.py"
    betik.write_text("import time\ntime.sleep(120)\n")
    t = time.time()
    kod, sonuc, pid = bc.calistir(betik, zaman_asimi=8)
    assert kod == 3 and sonuc is None and time.time() - t < 40
    assert not bo.pid_canli(pid)


def test_cli_yol_disi_2(tmp_path):
    blend = tmp_path / "x.blend"
    blend.write_bytes(b"")
    assert bc.calistir(FIXTURE, {}, blend=blend)[0] == 2
    assert bc.main([str(FIXTURE), "--blend", str(blend)]) == 2


def test_cli_sonuc_yok_3(tmp_path):
    betik = tmp_path / "sessiz.py"
    betik.write_text("print('merhaba')\n")
    assert bc.calistir(betik, zaman_asimi=120)[0] == 3


# --- K2 dogrula
def test_dogrula_hatali_her_kontrol(masaustu, capsys):
    kod, r = calis(capsys, bd.main, [masaustu / "Proje/blender/hatali.blend", "--beklenen", "Acik=1x1x1"])
    assert kod == 1 and r["gecti"] is False
    kontroller = {b["kontrol"] for b in r["bulgular"]}
    assert {"olcek_dondurme", "non_manifold", "uv", "havada", "basibos_empty", "eksik_doku",
            "mutlak_yol", "bbox"} <= kontroller
    assert {b["nesne"] for b in r["bulgular"] if b["kontrol"] == "havada"} == {"Havada"}
    assert r["serbest"] == ["Serbest"]


def test_dogrula_serbest_cli(masaustu, capsys):
    kod, r = calis(capsys, bd.main, [masaustu / "Proje/blender/hatali.blend", "--serbest", "Havada"])
    assert kod == 1 and not [b for b in r["bulgular"] if b["kontrol"] == "havada"]
    assert set(r["serbest"]) == {"Havada", "Serbest"}


def test_dogrula_temiz_ve_glb(masaustu, capsys):
    kod, r = calis(capsys, bd.main, [masaustu / "Proje/blender/temiz.blend", "--beklenen", "Kup=2x2x2",
                                     "--glb", masaustu / "Proje/kup.glb"])
    assert kod == 0 and r["bulgular"] == [] and r["ucgen"] == 12
    assert r["glb"]["mesh"] >= 1 and r["glb"]["bbox_sapma"] <= 0.01 and r["glb"]["validate"]["hata"] == 0


# --- K3 gorunum
def test_gorunum_cam_opak_ve_iou(masaustu, capsys):
    blend = masaustu / "Proje/blender/cam.blend"
    kod, r = calis(capsys, bg.main, [blend])
    klasor = Path(r["klasor"])
    assert kod == 0 and klasor.parent == masaustu / "Proje/blender/kanit"
    for ad in ("on", "yan", "ust", "uc_ceyrek", "kahraman", "sayfa"):
        assert (klasor / f"{ad}.png").stat().st_size > 0
    assert json.loads((klasor / "dogrula.json").read_text(encoding="utf-8"))["gecti"] is True
    assert r["on_maske_piksel"] > 1000  # transmission=1 cam gizlenmez, opak silüet
    time.sleep(1.1)
    kod, r2 = calis(capsys, bg.main, [blend, "--referans", klasor / "on.png"])
    assert kod == 0 and r2["iou"] >= 0.99 and r2["esik_kaynak"] == "oneri"


# --- K4 glb_hat
def test_glb_hat_once_sonra_ve_bozuk(masaustu, capsys, tmp_path):
    kod, r = calis(capsys, gh.main, [masaustu / "Proje/kup.glb"])
    assert kod == 0 and r["once_kb"] > 0 and r["sonra_kb"] > 0 and Path(r["cikti"]).is_file()
    bozuk = masaustu / "Proje/bozuk.glb"
    bozuk.write_bytes(b"glTF\x02\x00\x00\x00" + b"\x00" * 64)
    assert gh.main([str(bozuk)]) == 1
    disari = tmp_path / "d.glb"
    disari.write_bytes((masaustu / "Proje/kup.glb").read_bytes())
    assert gh.main([str(disari)]) == 2


# --- K6 bpy_kontrol
def test_bpy_kontrol(tmp_path, capsys):
    yanlis = tmp_path / "yanlis.py"
    yanlis.write_text("import bpy\nbpy.ops.mesh.primitive_cube_addd()\nbpy.context.scene.frame_strat = 1\n")
    kod, r = calis(capsys, bk.main, [yanlis])
    metin = json.dumps(r)
    assert kod == 1 and "primitive_cube_addd" in metin and "frame_strat" in metin
    dogru = tmp_path / "dogru.py"
    dogru.write_text("import bpy\nbpy.ops.mesh.primitive_cube_add(size=2)\nbpy.context.scene.frame_start = 1\n")
    assert calis(capsys, bk.main, [dogru]) == (0, {"bulgular": []})
