"""BLENDER-ARAC-2 test yardımcısı (Blender içinde koşar): pisir sahnesi · oku (ölçek/UV/görüntü)."""
import hashlib
import json
import sys

import bpy
import numpy as np

a = json.loads(sys.argv[sys.argv.index("--") + 1])
r = {"gecti": True}


def malzeme(ad):
    m = bpy.data.materials.new(ad)
    if not m.node_tree:
        m.use_nodes = True
    return m


if a["tur"] == "pisir":  # zemin + ölçekli küp (aynı malzeme) + area ışık
    bpy.ops.wm.read_factory_settings(use_empty=True)
    m = malzeme("Beyaz")
    bpy.ops.mesh.primitive_plane_add(size=10)
    bpy.context.object.name = "Zemin"
    bpy.context.object.data.materials.append(m)
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0.5))
    k = bpy.context.object
    k.name, k.scale = "Kup", (1, 2, 0.5)
    k.data.materials.append(m)
    bpy.ops.object.light_add(type="AREA", location=(0, 0, 4))
    bpy.context.object.data.energy, bpy.context.object.data.size = 800, 3
    bpy.ops.wm.save_as_mainfile(filepath=a["cikti"], relative_remap=False)
elif a["tur"] == "oku":
    for o in bpy.context.scene.objects:
        if o.type == "MESH":
            uv = o.data.uv_layers
            r[o.name] = {"olcek": [round(v, 4) for v in o.scale], "boyut": [round(v, 4) for v in o.dimensions],
                         "uv": [k.name for k in uv],
                         "uv1": hashlib.md5(np.array([d.uv[:] for d in uv[0].data]).round(5).tobytes()).hexdigest()
                         if len(uv) else None}
    if a.get("goruntu"):
        im = bpy.data.images.load(a["goruntu"])
        px = np.empty(len(im.pixels), np.float32)
        im.pixels.foreach_get(px)
        lum = px.reshape(-1, 4)[:, :3].mean(1)
        dolu = lum[lum > 0.002]
        r["goruntu"] = {"maks": float(lum.max()), "ort": float(dolu.mean()) if dolu.size else 0.0}
print("SONUC:" + json.dumps(r))
