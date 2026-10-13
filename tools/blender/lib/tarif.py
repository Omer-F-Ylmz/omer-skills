"""BLENDER-1 Faz 3: parametreli sahne tarifi — model bpy kodu yazmaz, spec JSON verir; tek headless koşu, çıktı özet JSON.

    python tools/blender_cli.py tools/blender/lib/tarif.py @spec.json [--blend Desktop\\<Proje>\\blender\\x.blend]

Sıra (her anahtar isteğe bağlı): nesneler → yigin → duzenle → patlat → isik → kamera → anim/kare → kaydet → glb →
onizle → render → ozet. --blend yoksa fabrika sahnesi boşaltılır. Hatalı spec Blender işi başlamadan reddedilir.
  nesneler: [{ad, tur: kup|silindir|kure|koni|duzlem|torus, boyut [m], konum, donus [derece], malzeme, bevel [m],
             ust (koni üst/alt yarıçap oranı, 0 sivri), ekler: [{tur, boyut, konum, donus}]}] — ekler (sap, ağız,
             tutamak) nesnenin merkezine göre konumlanır ve TEK nesneye birleşir: tanınır biçim için kullan
  malzeme : malzemeler.py tarif adı ya da {"renk": [r,g,b], "metal": 0..1, "puruz": 0..1}
  yigin   : "X"|"Y"|"Z" — nesneler sırayla üst üste;  patlat: {"eksen": "Z", "aralik": 0.05} — patlatılmış görünüm
  duzenle : [{nesne, bevel, subdiv, decimate (oran), uv: akilli|lightmap, malzeme}]
  isik    : isik_kur profili (3 nokta + world dolgu; boyut_m/merkez verilmezse mesh kutusundan). Render istenip
            sahnede ışık yoksa 'urun' kendiliğinden kurulur; malzemesiz mesh'e nötr gri atanır.
             kamera: "oto" | {konum, hedef, lens} — oto/ışık kutusu düz zemini (duzlem) saymaz, ürünü kadrajlar
  hdri    : .hdr/.exr yolu — world dolgusu (Poly Haven CC0: python tools/varlik_indir.py indir polyhaven <id>)
  anim    : [{nesne, kanal: location|rotation_euler|scale, kareler: [[kare, [x,y,z]]]}] — rotation_euler DERECE (tam tur 360);  kare: [baş, son]
  onizle  : {yol, px=256, motor=eevee};  render: {yol | klasor, px, motor: workbench|eevee|cycles, ornek, adim}
  ozet    : alan listesi (ad tur boyut konum malzeme ucgen uv) — yalnız mesh'ler, istenen alanlar
"""
import ast
import json
import math
import os
import sys
import time
from pathlib import Path

REF = Path(__file__).resolve().parent  # claude.ai zip: references/ içinde, isik_kur yanında
if not (REF / "isik_kur.py").is_file():
    REF = REF.parents[2] / "skills" / "blender-uretim" / "references"
TURLER = ("kup", "silindir", "kure", "koni", "duzlem", "torus")
KANALLAR = ("location", "rotation_euler", "scale")
ALANLAR = ("ad", "tur", "boyut", "konum", "malzeme", "ucgen", "uv")
ANAHTARLAR = ("nesneler", "yigin", "duzenle", "isik", "hdri", "boyut_m", "kamera", "patlat", "anim", "kare", "kaydet", "glb",
              "onizle", "render", "ozet")
DUZENLE = ("nesne", "bevel", "subdiv", "decimate", "uv", "malzeme")


def _ad_listesi():
    """isik_kur.PROFILLER ve malzemeler.TARIFLER adları — bpy'siz (ast)."""
    def atama(dosya, ad):
        agac = ast.parse((REF / dosya).read_text(encoding="utf-8"))
        return next(n.value for n in agac.body if isinstance(n, ast.Assign) and n.targets[0].id == ad)
    profiller = list(ast.literal_eval(atama("isik_kur.py", "PROFILLER")))
    tarifler = [n.id for n in ast.walk(atama("malzemeler.py", "TARIFLER").generators[0].iter) if isinstance(n, ast.Name)]
    return profiller, tarifler


def dogrula(spec):
    """Hata listesi; boş = geçerli. Blender açılmadan çağrılır."""
    profiller, tarifler = _ad_listesi()
    h = [f"bilinmeyen anahtar: {k}" for k in spec if k not in ANAHTARLAR]

    def malzeme(yer, m):
        if isinstance(m, str) and m not in tarifler:
            h.append(f"{yer}: malzeme '{m}' yok; mevcut {tarifler}")

    for i, n in enumerate(spec.get("nesneler", [])):
        if not n.get("ad"):
            h.append(f"nesneler[{i}]: ad zorunlu")
        if n.get("tur") not in TURLER:
            h.append(f"nesneler[{i}]: tur '{n.get('tur')}' yok; mevcut {TURLER}")
        for k in ("boyut", "konum", "donus"):
            if k in n and len(n[k]) != 3:
                h.append(f"nesneler[{i}]: {k} 3 sayı olmalı")
        malzeme(f"nesneler[{i}]", n.get("malzeme"))
        h += [f"nesneler[{i}].ekler[{j}]: tur '{e.get('tur')}' yok; mevcut {TURLER}"
              for j, e in enumerate(n.get("ekler", [])) if e.get("tur") not in TURLER]
    for i, d in enumerate(spec.get("duzenle", [])):
        h += [f"duzenle[{i}]: bilinmeyen anahtar: {k}" for k in d if k not in DUZENLE]
        malzeme(f"duzenle[{i}]", d.get("malzeme"))
    if "isik" in spec and spec["isik"] not in profiller:
        h.append(f"isik '{spec['isik']}' yok; mevcut {profiller}")
    if "hdri" in spec and not (Path(spec["hdri"]).suffix.lower() in (".hdr", ".exr") and Path(spec["hdri"]).is_file()):
        h.append(f"hdri '{spec['hdri']}' .hdr/.exr dosyası değil (indir: python tools/varlik_indir.py indir polyhaven <id>)")
    h += [f"anim: kanal '{a.get('kanal')}' yok; mevcut {KANALLAR}" for a in spec.get("anim", [])
          if a.get("kanal") not in KANALLAR]
    h += [f"ozet: alan '{a}' yok; mevcut {ALANLAR}" for a in spec.get("ozet", []) if a not in ALANLAR]
    return h


def _blender_ana():
    import bpy
    from mathutils import Vector
    sys.path.insert(0, str(REF))
    import isik_kur
    import malzemeler

    t0 = time.time()
    arg = sys.argv[sys.argv.index("--") + 1]
    spec = json.loads(Path(arg[1:]).read_text(encoding="utf-8") if arg.startswith("@") else arg)
    hatalar = dogrula(spec)
    if hatalar:
        print("SONUC:" + json.dumps({"gecti": False, "hatalar": hatalar}, ensure_ascii=False))
        return
    sc, ops = bpy.context.scene, bpy.ops
    kal = {} if os.environ.get("BLENDER_KALITE") == "0" else {"pah": []}  # BLENDER-3 eğitim varsayılanları (references/egitim.md)
    if not bpy.data.filepath:  # fabrika sahnesi: küp/ışık/kamera boşaltılır
        for o in list(bpy.data.objects):
            bpy.data.objects.remove(o)
    obj, mats = bpy.data.objects, {}

    def mat(m, ad):
        if isinstance(m, str):
            return mats.setdefault(m, malzemeler.kur(m))
        mt = bpy.data.materials.new("MAT-" + ad.removeprefix("GEO-"))
        isik_kur.ayarla(isik_kur.principled(mt)[1], {"Base Color": (*m.get("renk", (0.8, 0.8, 0.8)), 1),
                                                    "Metallic": m.get("metal", 0.0), "Roughness": m.get("puruz", 0.5)})
        return mt

    def ata(o, m):
        o.data.materials.clear()
        o.data.materials.append(mat(m, o.name))

    def bevel(o, w):
        b = o.modifiers.new("Bevel", "BEVEL")
        b.width, b.segments, b.limit_method = w, 2, "ANGLE"

    def ilkel(tur, ust=0.0):
        {"kup": lambda: ops.mesh.primitive_cube_add(size=1),
         "silindir": lambda: ops.mesh.primitive_cylinder_add(vertices=32, radius=0.5, depth=1),
         "kure": lambda: ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.5),
         "koni": lambda: ops.mesh.primitive_cone_add(vertices=32, radius1=0.5, radius2=0.5 * ust, depth=1),
         "duzlem": lambda: ops.mesh.primitive_plane_add(size=1),
         "torus": lambda: ops.mesh.primitive_torus_add(major_radius=0.375, minor_radius=0.125)}[tur]()
        if tur in ("silindir", "kure", "koni", "torus"):
            ops.object.shade_smooth_by_angle()
        return bpy.context.active_object

    yeni = []
    for n in spec.get("nesneler", []):
        tur = n["tur"]
        o = ilkel(tur, n.get("ust", 0.0))
        o.name = o.data.name = n["ad"]
        o["tur"] = tur
        o.scale = [b or 1 for b in n.get("boyut", (1, 1, 1))]
        ops.object.transform_apply(location=False, rotation=False, scale=True)
        for e in n.get("ekler", []):
            x = ilkel(e["tur"], e.get("ust", 0.0))
            x.scale, x.location = [b or 1 for b in e.get("boyut", (1, 1, 1))], e.get("konum", (0, 0, 0))
            x.rotation_euler = [math.radians(d) for d in e.get("donus", (0, 0, 0))]
            ops.object.transform_apply(location=True, rotation=True, scale=True)
            o.select_set(True)
            bpy.context.view_layer.objects.active = o
            ops.object.join()
        o.location = n.get("konum", (0, 0, 0))
        o.rotation_euler = [math.radians(d) for d in n.get("donus", (0, 0, 0))]
        if "malzeme" in n:
            ata(o, n["malzeme"])
        if n.get("bevel"):
            bevel(o, n["bevel"])
        elif kal and tur in ("kup", "silindir", "koni"):  # B Ml2t8uxPAQU/A 4H5W6C_Mbck: keskin kenar ışık yakalamaz; ~%0.6 pah
            bevel(o, round(0.006 * max(o.dimensions), 4))
            o.modifiers["Bevel"].harden_normals = True
            kal["pah"].append(o.name)
        yeni.append(o)

    if "yigin" in spec:
        e, imlec = "XYZ".index(spec["yigin"]), 0.0
        for o in yeni:
            o.location[e] = imlec + o.dimensions[e] / 2
            imlec += o.dimensions[e]

    for d in spec.get("duzenle", []):
        o = obj[d["nesne"]]
        if d.get("bevel"):
            bevel(o, d["bevel"])
        if d.get("subdiv"):
            s = o.modifiers.new("Subdiv", "SUBSURF")
            s.levels = s.render_levels = d["subdiv"]
        if d.get("decimate"):
            o.modifiers.new("Decimate", "DECIMATE").ratio = d["decimate"]
        if d.get("uv"):
            for x in sc.objects:
                x.select_set(x == o)
            bpy.context.view_layer.objects.active = o
            ops.object.mode_set(mode="EDIT")
            ops.mesh.select_all(action="SELECT")
            ops.uv.smart_project() if d["uv"] == "akilli" else ops.uv.lightmap_pack()
            ops.object.mode_set(mode="OBJECT")
        if "malzeme" in d:
            ata(o, d["malzeme"])

    meshler = [o for o in sc.objects if o.type == "MESH"]
    if "patlat" in spec:  # Faz 5 v2 g4: ışık/kamera patlatılmış hâli kadrajlamalı
        p = spec["patlat"]
        e = "XYZ".index(p.get("eksen", "Z"))
        for i, o in enumerate(sorted(meshler, key=lambda o: o.location[e])):
            o.location[e] += i * p.get("aralik", 0.05)
    bpy.context.view_layer.update()
    urun = [o for o in meshler if min(o.dimensions) > 1e-4] or meshler  # Faz 5 v2 g1: 1 m zemin fincanı minik yapıyordu

    def kutu():
        dg = bpy.context.evaluated_depsgraph_get()
        ks = [o.matrix_world @ Vector(k) for o in urun for k in o.evaluated_get(dg).bound_box]
        return Vector([min(k[i] for k in ks) for i in range(3)]), Vector([max(k[i] for k in ks) for i in range(3)])

    isiksiz = not any(o.type == "LIGHT" for o in sc.objects) and ("onizle" in spec or "render" in spec)
    if meshler and ("isik" in spec or isiksiz):  # Faz 5 g2: ışıksız --blend sahnesi siyah render veriyordu
        mn, mx = kutu()
        isik_kur.kur(spec.get("isik", "urun"), spec.get("boyut_m", max(mx - mn)), merkez=(mn + mx) / 2, hdri=spec.get("hdri"))

    def kamera_oto():
        mn, mx = kutu()
        merkez, r = (mn + mx) / 2, max((mx - mn).length / 2, 1e-3)
        lens = 85 if kal else 50  # C xxKZ1EjyjjU/A: ürün 85–100 mm; geniş açı yakın kenarı şişirir
        fov = 2 * math.atan(18 / lens)  # 36 mm sensör
        return merkez + Vector((0.6, -1, 0.45)).normalized() * r / math.sin(fov / 2) * 1.1, merkez, lens

    k = spec.get("kamera") or ("oto" if not sc.camera and ("onizle" in spec or "render" in spec) else None)
    if k:
        konum, hedef, lens = kamera_oto() if k == "oto" else (Vector(k["konum"]), Vector(k["hedef"]), k.get("lens", 50))
        kam = sc.camera or obj.new("CAM-Ana", bpy.data.cameras.new("CAM-Ana"))
        if kam.name not in sc.objects:
            sc.collection.objects.link(kam)
        sc.camera, kam.data.lens, kam.location = kam, lens, konum
        kam.data.clip_end = max(100, (konum - hedef).length * 10)
        kam.rotation_euler = (hedef - konum).to_track_quat("-Z", "Y").to_euler()
        if kal:  # C xOUQUDoflxU: gerçek ölçekte küçük ürün → yakın kırpma; glz3-ZClzGc: odak üründe, f/4 fonu yumuşatır
            kam.data.clip_start = 0.01
            kam.data.dof.use_dof, kam.data.dof.focus_distance = True, (konum - hedef).length
            kam.data.dof.aperture_fstop = kal["dof"] = 4.0

    tercih = bpy.context.preferences.edit
    eski_ara = tercih.keyframe_new_interpolation_type
    if kal and spec.get("anim"):  # C glz3-ZClzGc: turntable sabit hızla döner; kolay giriş/çıkış döngüde duraklatır
        tercih.keyframe_new_interpolation_type = kal["ara"] = "LINEAR"
    for a in spec.get("anim", []):
        o = obj[a["nesne"]]
        for kare, v in a["kareler"]:
            setattr(o, a["kanal"], [math.radians(x) for x in v] if a["kanal"] == "rotation_euler" else v)
            o.keyframe_insert(a["kanal"], frame=kare)
    tercih.keyframe_new_interpolation_type = eski_ara  # kullanıcı tercihi kalıcı değişmez
    if "kare" in spec:
        sc.frame_start, sc.frame_end = spec["kare"]

    for o in meshler:  # Faz 5 g3: malzemesiz mesh render'da/GLB'de tanımsız kalıyordu
        if not any(o.data.materials):
            ata(o, {})
    if "kaydet" in spec:
        Path(spec["kaydet"]).parent.mkdir(parents=True, exist_ok=True)
        ops.wm.save_as_mainfile(filepath=spec["kaydet"])
    if "glb" in spec:
        ops.export_scene.gltf(filepath=spec["glb"], export_format="GLB", export_apply=True, export_yup=True)

    def motor(ad, px, ornek=64):
        sc.render.resolution_x = sc.render.resolution_y = px
        sc.render.resolution_percentage = 100
        sc.render.image_settings.file_format = "PNG"
        sc.view_settings.view_transform = "AgX"  # --blend eski dosyada Standard/Filmic kalmış olabilir
        if ad == "workbench":
            sc.render.engine = "BLENDER_WORKBENCH"
            sc.display.shading.color_type = "MATERIAL"
        elif ad == "eevee":
            try:
                sc.render.engine = "BLENDER_EEVEE"
            except TypeError:
                sc.render.engine = "BLENDER_EEVEE_NEXT"
            sc.eevee.taa_render_samples = ornek
            if kal:  # D manual + CG Boost RsCNKHSRk_s: 5.x varsayılanı RT kapalı; tam çözünürlük RT + Fast GI 384 px'de +0.09 sn
                e = sc.eevee
                e.use_raytracing, e.ray_tracing_options.resolution_scale, e.fast_gi_resolution = True, "1", "1"
                e.fast_gi_ray_count, e.fast_gi_step_count, e.shadow_ray_count, e.shadow_step_count = 4, 16, 2, 8
                kal["eevee_rt"] = True
        else:
            sys.path.insert(0, str(REF.parents[2] / "tools"))
            try:
                from blender_pisir import _gpu
                cihaz = _gpu(sc)  # CPU'da kalırsa aynı görüntü katlarca yavaş
            except ImportError:  # ponytail: claude.ai zip'inde blender_pisir yok → CPU; GPU gerekirse repo yolu
                cihaz = "CPU"
            isik_kur.cycles_denoise(sc, ornek)
            sc.cycles.use_adaptive_sampling = True  # gürültü eşiğine (0.01) ulaşan piksel erken durur
            sc.cycles.denoising_input_passes = "RGB_ALBEDO_NORMAL"  # kenar/doku ayrıntısı korunur
            if kal:  # D kYOsR9Kb8Ek/dLZEmfqob7k: stüdyo ürününde sekme tavanı süreyi %21 kısalttı (yerel ölçüm); clamp ateşböceği keser
                c = sc.cycles
                c.max_bounces, c.diffuse_bounces, c.glossy_bounces, c.sample_clamp_indirect = 6, 2, 3, 5
                kal["cycles_sekme"] = 6
            sonuc["motor"] = {"motor": sc.render.engine, "cihaz": cihaz, "ornek": sc.cycles.samples,
                              "adaptif": sc.cycles.use_adaptive_sampling, "denoise": sc.cycles.use_denoising,
                              "gecis": sc.cycles.denoising_input_passes}

    def cek(yol):
        sc.render.filepath = str(yol)
        ops.render.render(write_still=True)
        return str(yol)

    sonuc = {"gecti": True}
    if k:
        sonuc["kamera"] = {"konum": [round(x, 3) for x in konum], "hedef": [round(x, 3) for x in hedef], "lens": lens}
    if "onizle" in spec:
        o = spec["onizle"]
        motor(o.get("motor", "eevee"), o.get("px", 256))
        sonuc["onizle"] = cek(o["yol"])
    if "render" in spec:
        r = spec["render"]
        motor(r.get("motor", "eevee"), r.get("px", 512), r.get("ornek", 64))
        if "klasor" in r:
            sonuc["render"] = []
            for f in range(sc.frame_start, sc.frame_end + 1, r.get("adim", 1)):
                sc.frame_set(f)
                sonuc["render"].append(cek(Path(r["klasor"]) / f"{f:04d}.png"))
        else:
            sonuc["render"] = cek(r["yol"])

    if "ozet" in spec:
        dg = bpy.context.evaluated_depsgraph_get()

        def alan(o, a):
            if a == "ucgen":
                return sum(len(p.vertices) - 2 for p in o.evaluated_get(dg).data.polygons)
            return {"ad": lambda: o.name, "tur": lambda: o.get("tur"), "uv": lambda: len(o.data.uv_layers),
                    "boyut": lambda: [round(x, 4) for x in o.dimensions],
                    "konum": lambda: [round(x, 4) for x in o.location],
                    "malzeme": lambda: [m.name for m in o.data.materials if m]}[a]()
        sonuc["ozet"] = [{a: alan(o, a) for a in spec["ozet"]} for o in sc.objects if o.type == "MESH"]
        diger = {}
        for o in sc.objects:
            if o.type != "MESH":
                diger[o.type] = diger.get(o.type, 0) + 1
        sonuc["diger"] = diger
    if kal:
        sonuc["kalite"] = kal
    sonuc["sure"] = round(time.time() - t0, 1)
    print("SONUC:" + json.dumps(sonuc, ensure_ascii=False))


if __name__ == "__main__":
    _blender_ana()
