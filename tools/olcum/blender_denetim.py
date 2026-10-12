"""BLENDER-1 Faz 5: nesnel kalite denetimi — Blender içinde koşar (blender_cli sözleşmesi), sahneyi değiştirmez.
    python tools/blender_cli.py tools/olcum/blender_denetim.py '{"png": [..]}' --blend <sahne.blend>
SONUC: mesh başına ad/boyut/z aralığı/üçgen/malzeme/uv/dönüş z (ilk-son kare), ışık/kamera sayısı, png başına parlaklık std.
"""
import json
import sys

import bpy
from mathutils import Vector

a = json.loads(sys.argv[sys.argv.index("--") + 1])
sc, dg = bpy.context.scene, bpy.context.evaluated_depsgraph_get()


def mesh_bilgi(o):
    e = o.evaluated_get(dg)
    m = e.to_mesh()
    ks = [o.matrix_world @ Vector(k) for k in e.bound_box]
    rz = []
    for f in (sc.frame_start, sc.frame_end):
        sc.frame_set(f)
        rz.append(round(o.matrix_world.to_euler().z if not o.animation_data else o.rotation_euler.z, 4))
    b = {"ad": o.name, "boyut": [round(x, 4) for x in o.dimensions], "z": [round(min(k.z for k in ks), 4), round(max(k.z for k in ks), 4)],
         "ucgen": sum(len(p.vertices) - 2 for p in m.polygons), "malzeme": any(s.material for s in o.material_slots),
         "uv": len(o.data.uv_layers), "fcurve": len(o.animation_data.action.fcurves) if o.animation_data and o.animation_data.action
         and hasattr(o.animation_data.action, "fcurves") else int(bool(o.animation_data and o.animation_data.action)), "rz": rz}
    e.to_mesh_clear()
    return b


def png_std(yol):
    try:
        im = bpy.data.images.load(yol)
    except RuntimeError:
        return -1.0
    p = im.pixels[:]
    lum = [0.3 * p[i] + 0.59 * p[i + 1] + 0.11 * p[i + 2] for i in range(0, len(p), 16)]
    ort = sum(lum) / max(len(lum), 1)
    return round((sum((x - ort) ** 2 for x in lum) / max(len(lum), 1)) ** 0.5, 4)


sonuc = {"gecti": True, "mesh": [mesh_bilgi(o) for o in sc.objects if o.type == "MESH"],
         "isik": sum(o.type == "LIGHT" for o in sc.objects) + sum(1 for o in sc.objects if o.type == "MESH" and any(
             s.material and s.material.use_nodes and any(n.type == "EMISSION" for n in s.material.node_tree.nodes) for s in o.material_slots)),
         "world": bool(sc.world), "kamera": bool(sc.camera), "kare": [sc.frame_start, sc.frame_end],
         "png": {p: png_std(p) for p in a.get("png", [])}}
print("SONUC:" + json.dumps(sonuc, ensure_ascii=False))
