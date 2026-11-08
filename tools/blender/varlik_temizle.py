"""Hunyuan3D vb. ham GLB'yi oyun varlığına temizler (F7). Blender headless:
blender -b -P tools/blender/varlik_temizle.py -- <girdi.glb> <cikti.glb> [yukseklik_m=0.1] [ucgen=20000]
İçe aktar → tek mesh → ölçek (yükseklik m) → taban z=0, merkez x,y=0 → Decimate (üçgen hedefi) → normaller → dışa aktar. Çıktıyı JSON satırı olarak yazar."""
import json, sys
import bpy
girdi, cikti = sys.argv[sys.argv.index("--") + 1:][:2]
yuks = float((sys.argv[sys.argv.index("--") + 3:] or ["0.1"])[0])
hedef = int((sys.argv[sys.argv.index("--") + 4:] or ["20000"])[0])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=girdi)
meshler = [o for o in bpy.context.scene.objects if o.type == "MESH"]
assert meshler, "mesh yok"
for o in bpy.context.scene.objects: o.select_set(o in meshler)
bpy.context.view_layer.objects.active = meshler[0]
if len(meshler) > 1: bpy.ops.object.join()
o = bpy.context.view_layer.objects.active
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
once = len(o.data.polygons)
z = o.dimensions.z or 1.0
o.scale = (yuks / z,) * 3
bpy.ops.object.transform_apply(scale=True)
mn = [min(v.co[i] for v in o.data.vertices) for i in range(3)]
mx = [max(v.co[i] for v in o.data.vertices) for i in range(3)]
o.location = (-(mn[0] + mx[0]) / 2, -(mn[1] + mx[1]) / 2, -mn[2])
bpy.ops.object.transform_apply(location=True)
if once > hedef:
    m = o.modifiers.new("dec", "DECIMATE"); m.ratio = hedef / once
    bpy.ops.object.modifier_apply(modifier=m.name)
bpy.ops.object.shade_smooth()
bpy.ops.export_scene.gltf(filepath=cikti, export_format="GLB")
print(json.dumps({"giris_yuz": once, "cikis_yuz": len(o.data.polygons), "boyut_m": [round(x, 4) for x in o.dimensions]}))
