"""Patlatılmış görünüm animasyonu (exploded view) — Blender arka planda, pencere açmaz.

Kullanım:
    blender -b --factory-startup --python blender_patlat.py -- --cikti <klasör>
        [--blend <dosya.blend>] [--kare 72] [--bosluk 0.06] [--fps 24] [--render 4] [--cozunurluk 384]
Çıktı: <klasör>/kare_NNNN.png (--render adet), <klasör>/telve_anim.glb; stdout'a tek satır JSON özet.

Nasıl uyarlanır:
- Kendi .blend'in: parça mesh'lerini `GEO-` ile adlandır, `--blend` ver; Z'ye göre sıralanıp o sırayla açılır.
- Eksen değiştirme: `EKSEN = 2` (Z) satırını 0 (X) ya da 1 (Y) yap; `--bosluk` o eksende parça başına aralık.
- Geri birleşme (ping-pong): `anahtar()`'a kare `--kare`'de birleşik konumla bir anahtar daha ekle (patlak kareyi ortaya al).
"""
import argparse
import json
import math
import sys
import time
from pathlib import Path

import bpy

EKSEN = 2  # 0=X 1=Y 2=Z


def arg():
    p = argparse.ArgumentParser()
    p.add_argument("--blend")
    p.add_argument("--cikti", required=True)
    p.add_argument("--kare", type=int, default=72)
    p.add_argument("--bosluk", type=float, default=0.06)
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--render", type=int, default=4)
    p.add_argument("--cozunurluk", type=int, default=384)
    return p.parse_args(sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else [])


def malzeme(ad, renk, metal=0.0, puruz=0.5):
    m = bpy.data.materials.new("MAT-" + ad)
    if m.node_tree is None:  # 5.x'te ağaç hazır; use_nodes 6.0'da kalkıyor
        m.use_nodes = True
    b = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    b.inputs["Base Color"].default_value = (*renk, 1)
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = puruz
    return m


def ornek_telve():
    """Düşük poli TELVE kahve makinesi: 5 parça, üst üste değil — Z merkezleri farklı."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    parcalar = [  # ad, tür, konum, ölçek, renk, metal, pürüz
        ("Taban", "kup", (0, 0, 0.02), (0.16, 0.13, 0.02), (0.05, 0.05, 0.05), 0.0, 0.4),
        ("Cezve", "silindir", (0, -0.07, 0.085), (0.035, 0.035, 0.045), (0.72, 0.45, 0.2), 1.0, 0.25),
        ("Govde", "kup", (0, 0.04, 0.17), (0.14, 0.08, 0.13), (0.55, 0.06, 0.06), 0.0, 0.35),
        ("Hazne", "silindir", (0, 0.05, 0.33), (0.07, 0.07, 0.03), (0.6, 0.75, 0.85), 0.0, 0.1),
        ("Kapak", "kup", (0, 0.04, 0.375), (0.14, 0.08, 0.015), (0.08, 0.08, 0.08), 0.3, 0.3),
    ]
    for ad, tur, konum, olcek, renk, metal, puruz in parcalar:
        if tur == "kup":
            bpy.ops.mesh.primitive_cube_add(size=2, location=konum)
        else:
            bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1, depth=2, location=konum)
        o = bpy.context.object
        o.name = o.data.name = "GEO-" + ad
        o.scale = olcek
        o.data.materials.append(malzeme(ad, renk, metal, puruz))


def fcurveler(action, o):
    """Blender 5.x: katmanlı (slotted) action — fcurve'ler layers/strips/channelbag altında; 4.x: action.fcurves."""
    if hasattr(action, "layers") and action.layers:
        slot = o.animation_data.action_slot
        return [fc for ly in action.layers for st in ly.strips
                for fc in (st.channelbag(slot).fcurves if st.channelbag(slot) else [])]
    return list(action.fcurves)


def anahtar(o, kare_patlak, kayma):
    z0 = o.location[EKSEN]
    o.keyframe_insert("location", index=EKSEN, frame=1)
    o.location[EKSEN] = z0 + kayma
    o.keyframe_insert("location", index=EKSEN, frame=kare_patlak)
    o.location[EKSEN] = z0
    for fc in fcurveler(o.animation_data.action, o):
        for k in fc.keyframe_points:
            k.interpolation, k.easing = "BEZIER", "EASE_IN_OUT"
            k.handle_left_type = k.handle_right_type = "AUTO_CLAMPED"  # uçlarda düz teğet → yumuşak giriş/çıkış
        fc.update()


def sahne_kur(sc, parcalar, a):
    alt = min(min((o.matrix_world @ v.co)[2] for v in o.data.vertices) for o in parcalar)
    ust = max(max((o.matrix_world @ v.co)[2] for v in o.data.vertices) for o in parcalar) + a.bosluk * (len(parcalar) - 1)
    yuk = ust - alt
    merkez = (0, 0, (alt + ust) / 2)

    bpy.ops.object.empty_add(location=merkez)
    hedef = bpy.context.object
    hedef.name = "YORUNGE"
    hedef.rotation_euler[2] = 0
    hedef.keyframe_insert("rotation_euler", index=2, frame=1)
    hedef.rotation_euler[2] = math.radians(90)
    hedef.keyframe_insert("rotation_euler", index=2, frame=a.kare)
    for fc in fcurveler(hedef.animation_data.action, hedef):
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"

    kam_veri = bpy.data.cameras.new("Kamera")
    kam_veri.lens = 50
    kam = bpy.data.objects.new("Kamera", kam_veri)
    sc.collection.objects.link(kam)
    kam.parent = hedef
    uzak = yuk * 3.2
    kam.location = (uzak * 0.75, -uzak * 0.75, yuk * 0.45)
    iz = kam.constraints.new("TRACK_TO")
    iz.target, iz.track_axis, iz.up_axis = hedef, "TRACK_NEGATIVE_Z", "UP_Y"
    sc.camera = kam

    for ad, konum, guc, boy in [("Ana", (2, -2, 2.5), 300, 1.0), ("Dolgu", (-2.5, -1.5, 1), 100, 1.5),
                                ("Kontur", (0, 2.5, 2), 200, 1.0)]:
        lv = bpy.data.lights.new(ad, "AREA")
        lv.energy, lv.size = guc * yuk, boy
        lo = bpy.data.objects.new(ad, lv)
        sc.collection.objects.link(lo)
        lo.location = konum
        c = lo.constraints.new("TRACK_TO")
        c.target, c.track_axis, c.up_axis = hedef, "TRACK_NEGATIVE_Z", "UP_Y"

    if sc.world is None:
        sc.world = bpy.data.worlds.new("Dunya")
    sc.world.color = (0.18, 0.18, 0.2)


def motor(sc, px):
    gecerli = {e.identifier for e in sc.render.bl_rna.properties["engine"].enum_items}
    sc.render.engine = "BLENDER_EEVEE" if "BLENDER_EEVEE" in gecerli else "BLENDER_EEVEE_NEXT"
    sc.eevee.taa_render_samples = 16
    sc.render.resolution_x = sc.render.resolution_y = px
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.film_transparent = False
    return sc.render.engine


def main():
    t0 = time.time()
    a = arg()
    cikti = Path(a.cikti).resolve()
    cikti.mkdir(parents=True, exist_ok=True)
    if a.blend:
        bpy.ops.wm.open_mainfile(filepath=a.blend)
    else:
        ornek_telve()
    sc = bpy.context.scene
    bpy.context.view_layer.update()  # ölçek/konum matrix_world'e işlensin; yoksa sınırlar ölçeksiz hesaplanır
    parcalar = sorted((o for o in sc.objects if o.type == "MESH" and o.name.startswith("GEO-")),
                      key=lambda o: o.matrix_world.translation[EKSEN])
    if not parcalar:
        sys.exit("GEO- ile başlayan mesh yok")
    sc.render.fps = a.fps
    sc.frame_start, sc.frame_end = 1, a.kare
    kare_patlak = max(2, round(a.kare * 0.6))
    for i, o in enumerate(parcalar):
        anahtar(o, kare_patlak, i * a.bosluk)
    sahne_kur(sc, parcalar, a)
    motor_adi = motor(sc, a.cozunurluk)

    n = max(1, a.render)
    kareler = sorted({round(1 + i * (a.kare - 1) / max(1, n - 1)) for i in range(n)})
    pngler = []
    for f in kareler:
        sc.frame_set(f)
        sc.render.filepath = str(cikti / f"kare_{f:04d}.png")
        bpy.ops.render.render(write_still=True)
        pngler.append(sc.render.filepath)
    sc.frame_set(1)

    bpy.ops.object.select_all(action="DESELECT")
    for o in parcalar:
        o.select_set(True)
    glb = cikti / "telve_anim.glb"
    bpy.ops.export_scene.gltf(filepath=str(glb), export_format="GLB", use_selection=True,
                              export_animations=True, export_force_sampling=True, export_cameras=False,
                              export_lights=False, export_animation_mode="SCENE",
                              export_optimize_animation_keep_anim_object=True)  # sabit Taban kanalı da kalsın
    print(json.dumps({"parca": [o.name for o in parcalar], "kare": a.kare, "patlak_kare": kare_patlak,
                      "motor": motor_adi, "blender": bpy.app.version_string, "png": pngler, "glb": str(glb),
                      "sure_sn": round(time.time() - t0, 1)}, ensure_ascii=False))


main()
