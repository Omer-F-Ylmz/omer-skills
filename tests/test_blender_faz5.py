"""BLENDER-1 Faz 5 ölçüm koşucusunun saf parçaları: glb geçerliliği + görev başına nesnel kontrol."""
import importlib.util
import json
import struct
from pathlib import Path

_s = importlib.util.spec_from_file_location("blender_faz5", Path(__file__).resolve().parents[1] / "tools" / "olcum" / "blender_faz5.py")
f5 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(f5)


def glb(yol, js):
    j = json.dumps(js).encode().ljust(-(-len(json.dumps(js)) // 4) * 4, b" ")
    yol.write_bytes(struct.pack("<4sII", b"glTF", 2, 20 + len(j)) + struct.pack("<I4s", len(j), b"JSON") + j)
    return yol


def test_glb_gecerli(tmp_path):
    assert f5.glb_mesh(glb(tmp_path / "a.glb", {"meshes": [{}, {}]})) == 2
    (tmp_path / "b.glb").write_bytes(b"bozuk")
    assert f5.glb_mesh(tmp_path / "b.glb") == 0 and f5.glb_mesh(tmp_path / "yok.glb") == 0


def mesh(ad, z0, z1, ucgen=100):
    return {"ad": ad, "boyut": [0.1, 0.1, z1 - z0], "z": [z0, z1], "ucgen": ucgen, "malzeme": True, "uv": 1, "fcurve": 0, "rz": [0, 0]}


def test_g4_patlatma_araligi(tmp_path):
    glb(tmp_path / "telve.glb", {"meshes": [{}] * 5})
    den = {"mesh": [mesh(f"GEO-{i}", i * 0.2, i * 0.2 + 0.1) for i in range(5)], "png": {"x": 0.1}, "isik": 3, "kamera": True}
    assert all(dict(f5.kontrol("g4", tmp_path, den)).values())
    den["mesh"][1]["z"] = [0.05, 0.25]  # bir öncekine 5 cm'den yakın
    k = dict(f5.kontrol("g4", tmp_path, den))
    assert not k["patlatma_aralik"] and k["glb"]


def test_g1_eksik_malzeme_ve_bos_render(tmp_path):
    den = {"mesh": [mesh("GEO-Fincan", 0, 0.09), mesh("GEO-Tabak", 0, 0.01), mesh("GEO-Zemin", 0, 0)], "png": {"x": 0.0},
           "isik": 3, "kamera": True}
    den["mesh"][0]["boyut"] = [0.08, 0.08, 0.09]
    den["mesh"][1]["malzeme"] = False
    k = dict(f5.kontrol("g1", tmp_path, den))
    assert k["fincan_olcu"] and not k["malzeme_hepsi"] and not k["render_dolu"]


def test_yargic_hafif_argv(tmp_path, monkeypatch):
    """TOKEN-8 iş 3: kör yargı ayar önekini yüklemez, yalnız Read; görev koşusu IZIN ile tam."""
    g = next(iter(f5.GOREV))
    for y in ("taban", "tarif"):
        (tmp_path / f"{g}-{y}-1").mkdir()
        (tmp_path / f"{g}-{y}-1" / "onizleme.png").write_bytes(b"x")
    ek = []
    monkeypatch.setattr(f5, "PROJE", tmp_path)
    monkeypatch.setattr(f5, "YARGI", tmp_path / "yargi.json")
    monkeypatch.setattr(f5.kosucu, "kos", lambda *a, **k: ek.append(k["ek"]) or {"metin": "{}", "usd": 0})
    f5.yargi5(("taban", "tarif"), (1,), (g,))
    assert ek == [f5.YARGIC]
    assert f5.YARGIC[:4] == ["--setting-sources", "", "--tools", "Read"]
    assert "Bash" in f5.IZIN and "--setting-sources" not in f5.IZIN
