"""Hazır varlığa küçük düzenleme şablonu (TELVE-R2d cezve deneyiminden): yalnız -b, çıktı tek satır JSON, görüntü yok.
  blender -b -P duzenle_b.py -- <gir.glb|gltf> <cik.glb> [--yukseklik 1.0] [--ucgen 3000] [--doku <ambientCG klasörü>] [--bak]
--bak: yalnız incele (nesne/üçgen/bbox/malzeme/UV/doku boyutu), yazma yok. Diğer: birleştir → dönüşüm uygula → taban merkezi orijin
→ yükseklik ölçeği → üçgen tavanına decimate → (ops.) CC0 doku malzemesi → GLB. Özel adım (sap ayrı malzeme vb.) gerekirse bu dosyayı
projeye kopyala ve orada genişlet; TELVE r2d/duzen.py örneği: normal haritayı koru, parçaya göre malzeme ata."""
import bpy, json, os, sys
from mathutils import Vector

a = sys.argv[sys.argv.index("--") + 1:]
sec = lambda ad, v=None: a[a.index(ad) + 1] if ad in a else v
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=a[0])
ms = [o for o in bpy.data.objects if o.type == "MESH"]


def ozet(nesneler):
    vs = [o.matrix_world @ Vector(c) for o in nesneler for c in o.bound_box]
    for o in nesneler:
        o.data.calc_loop_triangles()
    return {"nesne": len(nesneler), "ucgen": sum(len(o.data.loop_triangles) for o in nesneler),
            "bbox": [[round(min(v[i] for v in vs), 3) for i in range(3)], [round(max(v[i] for v in vs), 3) for i in range(3)]],
            "mal": sorted({s.material.name for o in nesneler for s in o.material_slots if s.material}),
            "uv_yok": [o.name for o in nesneler if not o.data.uv_layers],
            "doku": [[i.name, *i.size] for i in bpy.data.images][:12]}


if "--bak" in a:
    print("JSON", json.dumps(ozet(ms), ensure_ascii=False)); sys.exit(0)
for o in ms:
    mw = o.matrix_world.copy(); o.parent = None; o.matrix_world = mw
bpy.ops.object.select_all(action="DESELECT")
for o in ms:
    o.select_set(True)
bpy.context.view_layer.objects.active = ms[0]
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.join()
c = bpy.context.view_layer.objects.active; c.name = os.path.splitext(os.path.basename(a[1]))[0]
vs = [v.co for v in c.data.vertices]
lo, hi = [min(v[i] for v in vs) for i in range(3)], [max(v[i] for v in vs) for i in range(3)]
S = float(sec("--yukseklik", 0)) / (hi[2] - lo[2]) if sec("--yukseklik") else 1.0  # Blender Z yukarı
for v in c.data.vertices:
    v.co = (v.co - Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2]))) * S
c.data.update(); c.data.calc_loop_triangles()
if sec("--ucgen") and len(c.data.loop_triangles) > int(sec("--ucgen")):
    d = c.modifiers.new("d", "DECIMATE"); d.ratio = int(sec("--ucgen")) / len(c.data.loop_triangles)
    bpy.ops.object.modifier_apply(modifier="d")
if sec("--doku"):  # ambientCG klasörü: <id>_1K-JPG_Color/Roughness/Metalness/NormalGL.jpg
    k = sec("--doku"); kok = os.path.basename(os.path.normpath(k))
    m = bpy.data.materials.new(kok); m.use_nodes = True; t = m.node_tree; p = t.nodes["Principled BSDF"]
    for son, giris, renk in (("Color", "Base Color", True), ("Roughness", "Roughness", False), ("Metalness", "Metallic", False)):
        y = next((os.path.join(k, f) for f in os.listdir(k) if f.endswith(f"_{son}.jpg")), None)
        if y:
            n = t.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(y)
            if not renk:
                n.image.colorspace_settings.name = "Non-Color"
            t.links.new(n.outputs[0], p.inputs[giris])
    y = next((os.path.join(k, f) for f in os.listdir(k) if f.endswith("_NormalGL.jpg")), None)
    if y:
        n = t.nodes.new("ShaderNodeTexImage"); n.image = bpy.data.images.load(y); n.image.colorspace_settings.name = "Non-Color"
        nm = t.nodes.new("ShaderNodeNormalMap"); t.links.new(n.outputs[0], nm.inputs["Color"]); t.links.new(nm.outputs[0], p.inputs["Normal"])
    c.data.materials.clear(); c.data.materials.append(m)
for im in list(bpy.data.images):
    if im.users == 0:
        bpy.data.images.remove(im)
bpy.ops.export_scene.gltf(filepath=a[1], export_format="GLB", export_yup=True, export_apply=True, export_animations=False)
print("JSON", json.dumps(ozet([c]) | {"olcek": round(S, 4), "kb": round(os.path.getsize(a[1]) / 1024)}, ensure_ascii=False))
