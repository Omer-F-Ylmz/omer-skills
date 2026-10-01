"""BLENDER-ARAC-1 K2: sayısal kapı — görüntü ölçeği, pivotu ve topolojiyi kanıtlamaz; önce bu.

    python tools/blender_dogrula.py <dosya.blend> [--beklenen "ad=GxDxY" ...] [--butce-ucgen 500000]
                                    [--glb dosya.glb] [--serbest ad1,ad2]

Tek dosya iki rol: Blender içinde (bpy varsa) kontrolleri koşar, dışarıda blender_cli üstünden çağırır.
Havada kontrolünden muaf: nesne özelliği dogrula_serbest = True ya da --serbest (exploded view).
Çıkış: blender_cli sözleşmesi (0 geçti · 1 kapı kaldı · 2 kullanım/yol · 3 çöktü).
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import bpy
except ImportError:
    bpy = None

TOL = 0.001
AYKIRI_ALAN, AYKIRI_UCGEN = 0.01, 10000  # öneri eşik: ekranın %1'inden küçük ve 10k üçgenden fazla


def _kutu(oe, mw):
    from mathutils import Vector
    ks = [mw @ Vector(k) for k in oe.bound_box]
    return Vector([min(k[i] for k in ks) for i in range(3)]), Vector([max(k[i] for k in ks) for i in range(3)])


def kontroller(beklenen=None, butce=500000, serbest=()):
    import bmesh
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc, dg = bpy.context.scene, bpy.context.evaluated_depsgraph_get()
    bulgular, kutular, ucgenler, serbestler = [], {}, {}, []

    def bul(kontrol, nesne, detay):
        bulgular.append({"kontrol": kontrol, "nesne": nesne, "detay": detay})

    for o in sc.objects:
        if o.type == "EMPTY" and not o.children and o.instance_type == "NONE":
            bul("basibos_empty", o.name, "çocuksuz, instance'sız empty")
        if o.type != "MESH":
            continue
        _, don, olcek = o.matrix_basis.decompose()
        if any(abs(s - 1) > 1e-6 for s in olcek) or don.angle > 1e-6:
            bul("olcek_dondurme", o.name, f"ölçek {tuple(round(s, 4) for s in olcek)}, dönüş {don.angle:.4f} rad")
        oe = o.evaluated_get(dg)
        me = oe.to_mesh()
        kutular[o.name] = mn, mx = _kutu(oe, o.matrix_world)
        me.calc_loop_triangles()
        ucgenler[o.name] = len(me.loop_triangles)
        bm = bmesh.new()
        bm.from_mesh(me)
        nm, acik = sum(not e.is_manifold for e in bm.edges), sum(e.is_boundary for e in bm.edges)
        bm.free()
        if nm:
            bul("non_manifold", o.name, f"{nm} non-manifold kenar, kapalı={acik == 0}")
        slot = [s.material for s in o.material_slots]
        if any(p.material_index >= len(slot) or slot[p.material_index] is None for p in me.polygons):
            bul("malzeme", o.name, "malzemesiz yüz var")
        if not me.uv_layers and any(m and m.node_tree and any(n.type == "TEX_IMAGE" for n in m.node_tree.nodes)
                                    for m in slot):
            bul("uv", o.name, "dokulu malzeme, UV yok")
        oe.to_mesh_clear()
        p = o.matrix_world.translation
        if any(p[i] < mn[i] - TOL or p[i] > mx[i] + TOL for i in range(3)):
            bul("pivot", o.name, f"pivot {tuple(round(v, 3) for v in p)} bbox dışında")

    # ponytail: havada = bbox temelli (alt z > TOL ve başka parçanın kutusuna değmiyor); kesin temas gerekirse BVH.
    for ad, (mn, mx) in kutular.items():
        if bpy.data.objects[ad].get("dogrula_serbest") or ad in serbest:
            serbestler.append(ad)
            continue
        degiyor = any(all(mn[i] <= m2[1][i] + TOL and m2[0][i] <= mx[i] + TOL for i in range(3))
                      for a2, m2 in kutular.items() if a2 != ad)
        if mn.z > TOL and not degiyor:
            bul("havada", ad, f"alt z={mn.z:.3f}, hiçbir parçaya değmiyor")

    for ad, olcu in (beklenen or {}).items():
        if ad not in kutular:
            bul("bbox", ad, "nesne yok")
            continue
        boy = kutular[ad][1] - kutular[ad][0]
        if any(abs(boy[i] - olcu[i]) > TOL for i in range(3)):
            bul("bbox", ad, f"{boy.x:.4f}x{boy.y:.4f}x{boy.z:.4f} ≠ {'x'.join(map(str, olcu))}")

    for im in bpy.data.images:
        if im.source not in ("FILE", "SEQUENCE", "TILED") or im.packed_file or not im.users:
            continue
        if not im.filepath.startswith("//"):
            bul("mutlak_yol", im.name, im.filepath)
        if not Path(bpy.path.abspath(im.filepath)).exists():
            bul("eksik_doku", im.name, im.filepath)
    for lib in bpy.data.libraries:
        if not lib.filepath.startswith("//"):
            bul("mutlak_yol", lib.name, lib.filepath)

    ucgen = sum(ucgenler.values())
    if ucgen > butce:
        bul("ucgen_butce", "*", f"{ucgen} > {butce}")

    aykiri = []
    if sc.camera:
        for ad, (mn, mx) in kutular.items():
            ks = [world_to_camera_view(sc, sc.camera, Vector((x, y, z)))
                  for x in (mn.x, mx.x) for y in (mn.y, mx.y) for z in (mn.z, mx.z)]
            alan = (max(0, min(1, max(k.x for k in ks)) - max(0, min(k.x for k in ks)))
                    * max(0, min(1, max(k.y for k in ks)) - max(0, min(k.y for k in ks))))
            if alan < AYKIRI_ALAN and ucgenler[ad] > AYKIRI_UCGEN:
                aykiri.append({"nesne": ad, "ekran_alani": round(alan, 5), "ucgen": ucgenler[ad]})
    return {"gecti": not bulgular, "bulgular": bulgular, "ucgen": ucgen, "serbest": serbestler,
            "aykiri": aykiri, "aykiri_not": "rapor alanı, kapı değil; eşik öneri" if sc.camera else "kamera yok"}


def _sahne_olcusu():
    dg = bpy.context.evaluated_depsgraph_get()
    meshler = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    kutular = [_kutu(o.evaluated_get(dg), o.matrix_world) for o in meshler]
    mn = [min(k[0][i] for k in kutular) for i in range(3)] if kutular else [0, 0, 0]
    mx = [max(k[1][i] for k in kutular) for i in range(3)] if kutular else [0, 0, 0]
    malzeme = {s.material.name for o in meshler for s in o.material_slots if s.material}
    return len(meshler), len(malzeme), [mx[i] - mn[i] for i in range(3)]


def glb_kontrol(glb):
    _, malzeme0, boy0 = _sahne_olcusu()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    mesh, malzeme, boy = _sahne_olcusu()
    sapma = max(abs(boy[i] - boy0[i]) / max(boy0[i], 1e-9) for i in range(3))
    return {"mesh": mesh, "malzeme": malzeme, "malzeme_blend": malzeme0, "bbox_sapma": round(sapma, 5),
            "gecti": mesh > 0 and malzeme == malzeme0 and sapma <= 0.01}


def _blender_ana():
    a = json.loads(sys.argv[sys.argv.index("--") + 1])
    r = kontroller(a.get("beklenen"), a.get("butce", 500000), set(a.get("serbest", [])))
    if a.get("glb"):
        r["glb"] = glb_kontrol(a["glb"])
        if not r["glb"]["gecti"]:
            r["bulgular"].append({"kontrol": "glb", "nesne": a["glb"], "detay": "mesh 0, malzeme farkı ya da bbox > %1"})
            r["gecti"] = False
    print("SONUC:" + json.dumps(r))


def main(argv=None):
    import blender_cli as bc
    import glb_hat
    ap = argparse.ArgumentParser(description="Blender sayısal kapı")
    ap.add_argument("blend")
    ap.add_argument("--beklenen", action="append", default=[], help='"ad=GxDxY" metre (X·Y·Z)')
    ap.add_argument("--butce-ucgen", type=int, default=500000)
    ap.add_argument("--glb")
    ap.add_argument("--serbest", default="", help="havada kontrolünden muaf nesneler: ad1,ad2")
    ap.add_argument("--zaman-asimi", type=int, default=300)
    a = ap.parse_args(argv)
    try:
        beklenen = {ad: [float(x) for x in olcu.lower().split("x")] for ad, olcu in (b.split("=", 1) for b in a.beklenen)}
        assert all(len(v) == 3 for v in beklenen.values())
    except (ValueError, AssertionError):
        print('--beklenen biçimi: "ad=GxDxY" (ör. Kup=2x2x2)', file=sys.stderr)
        return 2
    if a.glb and not Path(a.glb).is_file():
        print(f"glb yok: {a.glb}", file=sys.stderr)
        return 2
    args = {"beklenen": beklenen, "butce": a.butce_ucgen, "glb": a.glb and str(Path(a.glb).resolve()),
            "serbest": [s for s in a.serbest.split(",") if s]}
    kod, sonuc, _ = bc.calistir(Path(__file__), args, blend=Path(a.blend), zaman_asimi=a.zaman_asimi)
    if sonuc is not None and a.glb:
        sonuc["glb"]["validate"] = glb_hat.validate(a.glb)
        if sonuc["glb"]["validate"]["hata"]:
            sonuc["gecti"], kod = False, 1
    if sonuc is not None:
        print(json.dumps(sonuc, ensure_ascii=False))
    return kod


if __name__ == "__main__":
    if bpy:
        _blender_ana()
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
        sys.exit(main())
