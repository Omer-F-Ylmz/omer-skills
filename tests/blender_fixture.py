"""BLENDER-ARAC-1 test yardımcısı (Blender içinde koşar): hatali / temiz / cam .blend (+ isteğe GLB) üretir."""
import json
import sys

import bmesh
import bpy

a = json.loads(sys.argv[sys.argv.index("--") + 1])
bpy.ops.wm.read_factory_settings(use_empty=True)


def malzeme(ad):
    m = bpy.data.materials.new(ad)
    if not m.node_tree:
        m.use_nodes = True
    return m


def kup(ad, konum, olcek=1.0, m=None):
    bpy.ops.mesh.primitive_cube_add(size=2, location=konum)
    o = bpy.context.object
    o.name, o.scale = ad, (olcek,) * 3
    if m:
        o.data.materials.append(m)
    return o


beyaz = malzeme("Beyaz")
if a["tur"] == "temiz":
    kup("Kup", (0, 0, 1), m=beyaz)
elif a["tur"] == "cam":
    bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=2, location=(0, 0, 1))
    o = bpy.context.object
    o.name = "Cam"
    cam = malzeme("Cam")
    cam.node_tree.nodes["Principled BSDF"].inputs["Transmission Weight"].default_value = 1.0
    o.data.materials.append(cam)
else:
    kup("Olcekli", (4, 0, 2), 2.0, beyaz)
    o = kup("Acik", (8, 0, 1), m=beyaz)
    bm = bmesh.new()
    bm.from_mesh(o.data)
    bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm, geom=[bm.faces[0]], context="FACES_ONLY")
    bm.to_mesh(o.data)
    bm.free()
    o = kup("Dokulu", (12, 0, 1))
    doku = malzeme("Doku")
    dugum = doku.node_tree.nodes.new("ShaderNodeTexImage")
    dugum.image = bpy.data.images.new("doku", 4, 4)
    dugum.image.source, dugum.image.filepath = "FILE", "C:/yok/doku.png"
    o.data.materials.append(doku)
    while o.data.uv_layers:
        o.data.uv_layers.remove(o.data.uv_layers[0])
    kup("Havada", (16, 0, 5), m=beyaz)
    kup("Serbest", (20, 0, 5), m=beyaz)["dogrula_serbest"] = True
    bpy.context.scene.collection.objects.link(bpy.data.objects.new("Bos", None))

bpy.ops.wm.save_as_mainfile(filepath=a["cikti"], relative_remap=False)
if a.get("glb"):
    bpy.ops.export_scene.gltf(filepath=a["glb"], export_format="GLB")
print("SONUC:" + json.dumps({"gecti": True}))
