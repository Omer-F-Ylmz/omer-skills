"""USTA-BLENDER-1 S1 alıştırmaları (headless): blender -b -P ex.py -- <A1|B1|C1|D1> <v1|v2> <out_dir>
v1 = taban (varsayılan ayarlar), v2 = kaynak tariflerine göre iyileştirilmiş."""
import math
import sys

import bpy

ex, ver, out = sys.argv[sys.argv.index("--") + 1:][:3]
v2 = ver == "v2"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = "BLENDER_EEVEE"
sc.render.resolution_x, sc.render.resolution_y = 640, 360
sc.render.image_settings.file_format = "PNG"


def mat(name, color, metal=0.0, rough=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = color
    b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough
    return m


def cam(loc, target=(0, 0, 0.5), lens=50):
    c = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
    sc.collection.objects.link(c)
    c.location = loc
    d = (c.location - bpy.context.view_layer.objects.active.location) if False else None
    from mathutils import Vector
    c.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    c.data.lens = lens
    sc.camera = c


def light(kind, loc, energy, size=1.0):
    l = bpy.data.lights.new(kind, kind)
    l.energy = energy
    if kind == "AREA":
        l.size = size
    o = bpy.data.objects.new(kind, l)
    sc.collection.objects.link(o)
    o.location = loc
    from mathutils import Vector
    o.rotation_euler = (Vector((0, 0, 0.5)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def world_sky(strength=1.0):
    w = bpy.data.worlds.new("W")
    w.use_nodes = True
    sc.world = w
    n = w.node_tree.nodes
    sky = n.new("ShaderNodeTexSky")
    w.node_tree.links.new(sky.outputs[0], n["Background"].inputs[0])
    n["Background"].inputs[1].default_value = strength


def floor(color=(0.6, 0.6, 0.6, 1)):
    bpy.ops.mesh.primitive_plane_add(size=20)
    f = bpy.context.object
    f.data.materials.append(mat("Floor", color, 0, 0.6))
    return f


def render(path):
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


if ex == "A1":  # cezve (lathe) — v1: ham silindir, v2: profil + bevel + bakır + saplı
    floor()
    if v2:
        prof = [(0.0, 0), (0.7, 0), (0.8, 0.08), (0.78, 0.5), (0.55, 0.95), (0.42, 1.15), (0.52, 1.32)]
        me = bpy.data.meshes.new("Cezve")
        me.from_pydata([(x, 0, z) for x, z in prof], [(i, i + 1) for i in range(len(prof) - 1)], [])
        o = bpy.data.objects.new("Cezve", me)
        sc.collection.objects.link(o)
        s = o.modifiers.new("Screw", "SCREW")
        s.steps = s.render_steps = 48
        s.axis = "Z"
        o.modifiers.new("Solid", "SOLIDIFY").thickness = 0.03
        o.modifiers.new("Sub", "SUBSURF").levels = 2
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.shade_smooth()
        o.data.materials.append(mat("Bakir", (0.95, 0.5, 0.28, 1), 1.0, 0.35))
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.1, location=(1.3, 0, 0.75), rotation=(0, math.radians(75), 0))
        h = bpy.context.object
        h.data.materials.append(mat("Sap", (0.08, 0.04, 0.02, 1), 0, 0.5))
        bpy.ops.object.shade_smooth()
        world_sky(0.45)
        light("AREA", (3, -3, 4), 800, 3)
    else:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.8, depth=1.3, location=(0, 0, 0.65))
        light("POINT", (3, -3, 4), 500)
    cam((3.5, -4.5, 2.2), (0.3, 0, 0.7))
    render(f"{out}/{ex}-{ver}.png")

elif ex == "B1":  # PBR + gökyüzü ışığı — v1: gri difüz küre, v2: bakır PBR + sky + yansıtıcı zemin + dolgu
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 1))
    bpy.ops.object.shade_smooth()
    s = bpy.context.object
    if v2:
        floor((0.8, 0.8, 0.8, 1))
        s.data.materials.append(mat("Bakir", (0.95, 0.5, 0.28, 1), 1.0, 0.3))
        world_sky(0.5)
        light("AREA", (3, -3, 4), 600, 3)
        sc.eevee.use_raytracing = True
    else:
        floor()
        s.data.materials.append(mat("Gri", (0.5, 0.5, 0.5, 1), 0, 0.5))
        light("POINT", (3, -3, 4), 500)
    cam((4, -4.5, 2.5), (0, 0, 1))
    render(f"{out}/{ex}-{ver}.png")

elif ex == "C1":  # zıplayan top — v1: lineer, 2 anahtar; v2: ease + squash/stretch + yavaş-giriş/çıkış
    floor()
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(-3, 0, 0.5))
    b = bpy.context.object
    bpy.ops.object.shade_smooth()
    b.data.materials.append(mat("Top", (0.9, 0.15, 0.1, 1), 0, 0.3))
    sc.frame_start, sc.frame_end = 1, 48
    if v2:
        # bırakma-yükselme: apeks z=3, temas z=0.5, her 12 karede; temas anında squash, havada stretch
        pts = [(1, 3), (12, 0.5), (24, 3), (36, 0.5), (48, 3)]
        for i, (f, z) in enumerate(pts):
            b.location = (-3 + 6 * (f - 1) / 47, 0, z)
            b.scale = (1.35, 1.35, 0.6) if z == 0.5 else ((0.9, 0.9, 1.2) if i % 2 else (1, 1, 1))
            b.keyframe_insert("location", frame=f)
            b.keyframe_insert("scale", frame=f)
        for fc in b.animation_data.action.fcurves if hasattr(b.animation_data.action, "fcurves") else []:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"
    else:
        for f, z in [(1, 3), (48, 0.5)]:
            b.location = (-3 + 6 * (f - 1) / 47, 0, z)
            b.keyframe_insert("location", frame=f)
    for fc in (b.animation_data.action.fcurves if hasattr(b.animation_data.action, "fcurves") else []):
        if not v2:
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"
    light("AREA", (3, -5, 6), 900, 4)
    (sc.world or bpy.data.worlds.new('W')) if False else None
    if v2:
        w = bpy.data.worlds.new('W'); w.use_nodes = True; sc.world = w
        w.node_tree.nodes['Background'].inputs[0].default_value = (0.25, 0.27, 0.3, 1)
    cam((0, -9, 2.5), (0, 0, 1.8), 40)
    for f in (1, 8, 12, 18, 24, 30):
        sc.frame_set(f)
        render(f"{out}/C1-{ver}-f{f:02d}.png")

elif ex == "D1":  # duman — v1: varsayılan quick smoke; v2: ayar (çözünürlük, buoyancy, noise, vorticity)
    bpy.ops.mesh.primitive_plane_add(size=0.6, location=(0, 0, 0.3))
    e = bpy.context.object
    bpy.ops.object.quick_smoke()
    dom = [o for o in bpy.data.objects if o.modifiers and o.modifiers[0].type == "FLUID" and o.modifiers[0].fluid_type == "DOMAIN"][0]
    ds = dom.modifiers[0].domain_settings
    ds.resolution_max = 48
    sc.frame_start, sc.frame_end = 1, 40
    if v2:
        ds.use_noise = True
        ds.noise_scale = 2
        ds.vorticity = 0.3
        ds.alpha = 1.5
        ds.beta = 0.5
        ds.use_dissolve_smoke = False
    ds.cache_directory = out + "/cache_" + ver
    bpy.ops.fluid.bake_all()
    sc.frame_set(40)
    w = bpy.data.worlds.new('W'); w.use_nodes = True; sc.world = w
    w.node_tree.nodes['Background'].inputs[0].default_value = (0.02, 0.02, 0.03, 1)
    light('AREA', (3, -4, 3), 1500, 3)
    sc.frame_set(30); sc.frame_set(40)
    c = dom.location; d = dom.dimensions
    print('DOM', tuple(c), tuple(d))
    cam((c.x, c.y - max(d) * 1.6, c.z), tuple(c), 40)
    render(f"{out}/D1-{ver}.png")
