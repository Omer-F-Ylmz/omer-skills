"""blender-uretim K2 · ışık profilleri — Blender 5.2.1 (öznitelik/soket adları canlı sorgulandı 2026-10-01).

Sahne betiğinde:  sys.path.insert(0, r"C:\\Projeler\\omer-skills\\skills\\blender-uretim\\references")
                  import isik_kur;  isik_kur.kur("urun", boyut_m=0.08)
Kanıt: blender_cli ile doğrudan koştur → boş sahnede her profil + ek kurulur, SONUC {gecti, sonuc, hatalar}.
Kaynak/öneri ayrımı references/isik-profilleri.md'de. Kamera -Y'de, +Y'ye bakar varsayılır.
"""
import json
import math
from typing import Any

import bpy
from mathutils import Vector

# oran = anahtar:dolgu:kenar güç oranı; K = renk sıcaklığı; hdri = world dolgu gücü
PROFILLER = {
    "urun": {"oran": (5, 1, 1.5), "K": 5000, "hdri": 0.3},  # #1
    "cam": {"oran": (3, 1, 1.2), "K": None, "hdri": 0.3, "gradyan": True},  # #1 + Q2 metal/cam
    "ahsap": {"oran": (4, 1, 1.5), "K": 3000, "hdri": 0.3},  # #1
    "kumas": {"oran": (3, 1, 0.5), "K": None, "hdri": 0.3},  # #1
    "metal": {"oran": (5, 1, 1.5), "K": 5000, "hdri": 0.1, "serit": True},  # ZYk3OOf-gBk: uzun alan, az HDRI
    "seramik_sirli": {"oran": (5, 1, 1.5), "K": 5000, "hdri": 0.3, "serit": True},  # öneri
    "seramik_mat": {"oran": (5, 1, 1), "K": 5000, "hdri": 0.3},  # öneri: kenar 1
}
ANAHTAR_W = 300  # öneri: 1 m'de anahtar gücü (W), uzaklığın karesiyle büyür; kalibrasyon düğmesi budur


def agac(idb) -> Any:
    """Malzeme/world/ışık düğüm ağacı; 5.x'te boş gelebilir."""
    if idb.node_tree is None:
        idb.use_nodes = True
    return idb.node_tree


def dugum(nt, tip) -> Any:
    return next((n for n in nt.nodes if n.bl_idname == tip), None) or nt.nodes.new(tip)


def soket(n, ad, cikis=False):
    """Soket canlı aranır (yalnız etkin olan); yoksa mevcut adlarla durur → search_api_docs ile yeniden sorgula."""
    soketler = [s for s in (n.outputs if cikis else n.inputs) if s.enabled]
    for s in soketler:
        if s.name == ad:
            return s
    raise KeyError(f"{n.bl_idname}: '{ad}' yok; mevcut {[s.name for s in soketler]} -> search_api_docs")


def ayarla(n, degerler):
    for ad, v in degerler.items():
        soket(n, ad).default_value = v


def bagla(nt, a, a_cikis, b, b_giris):
    nt.links.new(soket(a, a_cikis, cikis=True), soket(b, b_giris))


def principled(mat):
    nt = agac(mat)
    p, out = dugum(nt, "ShaderNodeBsdfPrincipled"), dugum(nt, "ShaderNodeOutputMaterial")
    if not soket(out, "Surface").is_linked:
        bagla(nt, p, "BSDF", out, "Surface")
    return nt, p


def _sahneye(o) -> Any:
    bpy.context.scene.collection.objects.link(o)
    return o


def _bak(o, hedef, eksen="-Z"):
    o.rotation_euler = (Vector(hedef) - o.location).to_track_quat(eksen, "Y").to_euler()


def kure(merkez, d, azimut, yukseklik):
    """azimut 0 = kamera tarafı (-Y), + = sağ; yukseklik derece."""
    a, y = math.radians(azimut), math.radians(yukseklik)
    return Vector(merkez) + d * Vector((math.sin(a) * math.cos(y), -math.cos(a) * math.cos(y), math.sin(y)))


def isik(ad, tur, enerji, konum, hedef, boyut=0.5, K=None):
    L: Any = bpy.data.lights.new(ad, tur)
    L.energy = enerji
    if tur == "AREA":
        L.size = boyut
    if K:
        L.use_temperature, L.temperature = True, K
    o = _sahneye(bpy.data.objects.new(ad, L))
    o.location = konum
    _bak(o, hedef)
    return o


def duzlem(ad, en, boy, konum, hedef):
    me = bpy.data.meshes.new(ad)
    w, h = en / 2, boy / 2
    me.from_pydata([(-w, -h, 0), (w, -h, 0), (w, h, 0), (-w, h, 0)], [], [(0, 1, 2, 3)])
    o = _sahneye(bpy.data.objects.new(ad, me))
    o.location = konum
    _bak(o, hedef, "Z")
    return o


def isima(ad, guc, renk=(1, 1, 1, 1)):
    m = bpy.data.materials.new(ad)
    nt = agac(m)
    nt.nodes.clear()
    em, out = nt.nodes.new("ShaderNodeEmission"), nt.nodes.new("ShaderNodeOutputMaterial")
    ayarla(em, {"Color": renk, "Strength": guc})
    bagla(nt, em, "Emission", out, "Surface")
    return m, nt, em


def _gorunmez_duzlem(ad, en, boy, konum, hedef, guc):
    o = duzlem(ad, en, boy, konum, hedef)
    o.data.materials.append(isima("MAT-" + ad[4:], guc)[0])
    o.visible_camera = False  # Visibility > Camera kapalı
    return o


def kur(profil="urun", boyut_m=0.1, merkez=(0, 0, 0), etiket=None, hdri=None):
    """Üç nokta (#1) + profil ekleri. etiket: anahtarın hedefi (wySOWP-MevI); hdri: .hdr/.exr yolu (varlik_indir)."""
    p, m = PROFILLER[profil], Vector(merkez)
    d = max(boyut_m * 1.5, 1.0)  # #1
    a, f, k = p["oran"]
    birim = ANAHTAR_W * d * d / a
    s = max(boyut_m * 2, 0.3)  # öneri: alan ışığı ürüne göre geniş ve yakın (wySOWP-MevI, 4Uy2SzB-Kuk)
    obs = [isik("LGT-Anahtar", "AREA", birim * a, kure(m, d, -40, 30), etiket or m, s, p["K"]),
           isik("LGT-Dolgu", "AREA", birim * f, kure(m, d, 60, 10), m, s * 1.5, p["K"]),
           isik("LGT-Kenar", "AREA", birim * k, kure(m, d, 160, 45), m, s * 0.5, p["K"])]
    if p.get("serit"):
        obs += serit(m, d, boyut_m)
    if p.get("gradyan"):
        obs.append(gradyan_duzlem(m, d, boyut_m))
    hdri_dolgu(hdri, p["hdri"])
    return obs


def hdri_dolgu(yol=None, guc=0.3):
    """Yeni world WLD-Dolgu; mevcut world ezilmez (Q2). yol yoksa nötr gri."""
    w = bpy.data.worlds.new("WLD-Dolgu")
    nt = agac(w)
    bg, out = dugum(nt, "ShaderNodeBackground"), dugum(nt, "ShaderNodeOutputWorld")
    ayarla(bg, {"Strength": guc})
    if yol:
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(yol, check_existing=True)
        bagla(nt, env, "Color", bg, "Color")
    else:
        ayarla(bg, {"Color": (0.5, 0.5, 0.5, 1)})
    if not soket(out, "Surface").is_linked:
        bagla(nt, bg, "Background", out, "Surface")
    bpy.context.scene.world = w
    return w


def serit(m=(0, 0, 0), d=1.0, boyut_m=0.1, guc=5.0):
    """İki dikey şerit softbox, kameraya görünmez: sırlı yüzeyde/metalde uzun vurgu çizgisi."""
    h = max(boyut_m * 3, 0.5)
    return [_gorunmez_duzlem(ad, h / 6, h, kure(m, d, az, 5), m, guc)
            for ad, az in (("LGT-SeritSol", -70), ("LGT-SeritSag", 70))]


def gorunmez_dolgu(m=(0, 0, 0), d=1.0, guc=2.0):
    """Dolgu = kameraya görünmez ışıyan düzlem (ZYk3OOf-gBk)."""
    return _gorunmez_duzlem("LGT-DolguDuzlem", d, d, kure(m, d, 70, 15), m, guc)


def sekme_duvari(m=(0, 0, 0), d=1.0, ton=0.6):
    """Işıksız duvar: anahtarın sekmesi dolgu olur; ton kısılarak ayarlanır (wySOWP-MevI, 4Uy2SzB-Kuk)."""
    o = duzlem("GEO-SekmeDuvari", d, d, kure(m, d, 80, 10), m)
    mat = bpy.data.materials.new("MAT-SekmeDuvari")
    ayarla(principled(mat)[1], {"Base Color": (ton, ton, ton, 1), "Roughness": 0.9})
    o.data.materials.append(mat)
    return o


def zemini_ayir(isik_o, zemin):
    """Light Linking: ışık zemini aydınlatmaz (alıcı koleksiyonda EXCLUDE) (ZYk3OOf-gBk)."""
    c = bpy.data.collections.new(f"{isik_o.name}-Alici")
    c.objects.link(zemin)
    isik_o.light_linking.receiver_collection = c
    c.collection_objects[0].light_linking.link_state = "EXCLUDE"
    return c


def kivrimli_zemin(en=2.0, derin=2.0, yuk=1.5, r=0.4, adim=12):
    """Kıvrımlı beyaz zemin: zemin → çeyrek daire → duvar, +Y yönünde (ZYk3OOf-gBk, wySOWP-MevI)."""
    y0 = derin / 2 - r
    yay = [(y0 + r * math.sin(t), r - r * math.cos(t)) for t in (math.pi / 2 * i / adim for i in range(adim + 1))]
    prof = [(-derin / 2, 0.0)] + yay + [(y0 + r, yuk)]
    n = len(prof)
    me = bpy.data.meshes.new("GEO-Zemin")
    me.from_pydata([(x, y, z) for x in (-en / 2, en / 2) for y, z in prof], [],
                   [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)])
    me.shade_smooth()
    o = _sahneye(bpy.data.objects.new("GEO-Zemin", me))
    mat = bpy.data.materials.new("MAT-Zemin")
    ayarla(principled(mat)[1], {"Base Color": (0.8, 0.8, 0.8, 1), "Roughness": 0.8})
    o.data.materials.append(mat)
    return o


def gradyan_duzlem(m=(0, 0, 0), d=1.0, boyut_m=0.1, guc=8.0):
    """Cam/metal: kameraya görünmez, gradyan dokulu ışıyan düzlem → yumuşak geçişli yansıma (Q2, ZYk3OOf-gBk)."""
    e = max(boyut_m * 4, 0.6)
    o = duzlem("LGT-GradyanDuzlem", e, e, kure(m, d, 110, 20), m)
    mat, nt, em = isima("MAT-GradyanDuzlem", guc)
    tc, gr, cr = (nt.nodes.new(t) for t in ("ShaderNodeTexCoord", "ShaderNodeTexGradient", "ShaderNodeValToRGB"))
    bagla(nt, tc, "Generated", gr, "Vector")
    bagla(nt, gr, "Factor", cr, "Factor")
    bagla(nt, cr, "Color", em, "Color")
    cr.color_ramp.elements[0].color = (0, 0, 0, 1)
    o.data.materials.append(mat)
    o.visible_camera = False
    return o


def gobo(hedef=(0, 0, 0), d=2.0, doku=None, renk=(1, 1, 1, 1), guc=500.0):
    """Spot + desen: doku verilirse görüntü, yoksa Voronoi; renk ile renkli gobo (ZYk3OOf-gBk, wySOWP-MevI)."""
    o = isik("LGT-Gobo", "SPOT", guc, kure(hedef, d, -100, 40), hedef)
    nt = agac(o.data)
    em = dugum(nt, "ShaderNodeEmission")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    tex = nt.nodes.new("ShaderNodeTexImage" if doku else "ShaderNodeTexVoronoi")
    if doku:
        tex.image = bpy.data.images.load(doku, check_existing=True)
    mx = nt.nodes.new("ShaderNodeMix")
    mx.data_type, mx.blend_type = "RGBA", "MULTIPLY"
    ayarla(mx, {"Factor": 1.0, "B": renk})
    bagla(nt, tc, "Normal", tex, "Vector")
    bagla(nt, tex, "Color", mx, "A")
    bagla(nt, mx, "Result", em, "Color")
    return o


def teaser(m=(0, 0, 0), boyut_m=0.1):
    """Teaser karesi: yalnız iki arka ışık, silüet kenarı (ZYk3OOf-gBk)."""
    d = max(boyut_m * 1.5, 1.0)
    return [isik(f"LGT-Arka{i}", "AREA", ANAHTAR_W * d * d, kure(m, d, az, 30), m, max(boyut_m, 0.2))
            for i, az in ((1, 150), (2, -150))]


def bevel(o, genislik=0.001, mat=None, yaricap=0.0005):
    """Keskin kenar ışık yakalamaz: modifier (geometri) + shader Bevel (yalnız Cycles) (ZYk3OOf-gBk)."""
    mod: Any = o.modifiers.new("GEO-Bevel", "BEVEL")
    mod.width, mod.segments, mod.limit_method = genislik, 3, "ANGLE"
    if mat:
        nt, p = principled(mat)
        b = nt.nodes.new("ShaderNodeBevel")
        ayarla(b, {"Radius": yaricap})
        bagla(nt, b, "Normal", p, "Normal")
    return mod


def dof(kamera, hedef, fstop=2.8):
    """Alan derinliği: odak nesnede (4Uy2SzB-Kuk); fstop öneri."""
    kamera.data.dof.use_dof = True
    kamera.data.dof.focus_object = hedef
    kamera.data.dof.aperture_fstop = fstop


def compositing(sahne=None, bozulma=-0.01, vinyet=0.15, gurultu=0.03):
    """Ölçülü son katman: Lens Distortion + vinyet + sensör gürültüsü (wySOWP-MevI); değerler öneri, az olan iyi."""
    sc = sahne or bpy.context.scene
    ag: Any = bpy.data.node_groups.new("SCN-Compositing", "CompositorNodeTree")
    sc.compositing_node_group = ag
    ag.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl, ld, el, bl, vm, wn, nm, out = (ag.nodes.new(t) for t in (
        "CompositorNodeRLayers", "CompositorNodeLensdist", "CompositorNodeEllipseMask", "CompositorNodeBlur",
        "ShaderNodeMix", "ShaderNodeTexWhiteNoise", "ShaderNodeMix", "NodeGroupOutput"))
    ayarla(ld, {"Distortion": bozulma, "Dispersion": 0.005})
    ayarla(el, {"Size": (0.95, 0.95)})
    ayarla(bl, {"Size": (200.0, 200.0)})
    for mx, tur, f in ((vm, "MULTIPLY", vinyet), (nm, "OVERLAY", gurultu)):
        mx.data_type, mx.blend_type = "RGBA", tur
        ayarla(mx, {"Factor": f})
    bagla(ag, rl, "Image", ld, "Image")
    bagla(ag, ld, "Image", vm, "A")
    bagla(ag, el, "Mask", bl, "Image")
    bagla(ag, bl, "Image", vm, "B")
    bagla(ag, vm, "Result", nm, "A")
    bagla(ag, wn, "Color", nm, "B")
    ag.links.new(soket(nm, "Result", cikis=True), out.inputs[0])
    return ag


def cycles_denoise(sahne=None, ornek=256):
    """Teslim render'ı: Cycles + denoise, OptiX varsa yoksa OIDN (4Uy2SzB-Kuk). GPU seçimi blender_pisir._gpu sırası."""
    sc: Any = sahne or bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = ornek
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPTIX"
    except TypeError:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    return sc.cycles.denoiser


def _temizle():
    for koll in (bpy.data.objects, bpy.data.meshes, bpy.data.lights, bpy.data.cameras, bpy.data.materials,
                 bpy.data.worlds, bpy.data.node_groups, bpy.data.collections):
        bpy.data.batch_remove(list(koll))


def _say():
    agaclar = [x.node_tree for x in (*bpy.data.materials, *bpy.data.worlds, *bpy.data.lights) if x.node_tree]
    return {"nesne": len(bpy.context.scene.objects),
            "dugum": sum(len(t.nodes) for t in agaclar) + sum(len(g.nodes) for g in bpy.data.node_groups)}


def _kanit():
    isler = {f"profil:{p}": (lambda p=p: kur(p, 0.08)) for p in PROFILLER}
    isler.update({
        "gorunmez_dolgu": gorunmez_dolgu, "sekme_duvari": sekme_duvari, "kivrimli_zemin": kivrimli_zemin,
        "zemini_ayir": lambda: zemini_ayir(kur("urun", 0.08)[0], kivrimli_zemin()),
        "gradyan_duzlem": gradyan_duzlem, "gobo": gobo, "teaser": teaser,
        "bevel": lambda: bevel(duzlem("GEO-Kup", 0.1, 0.1, (0, 0, 0), (0, 0, 1)), mat=bpy.data.materials.new("MAT-Kup")),
        "dof": lambda: dof(_sahneye(bpy.data.objects.new("CAM-Ana", bpy.data.cameras.new("CAM-Ana"))), kivrimli_zemin()),
        "compositing": compositing, "cycles_denoise": cycles_denoise,
    })
    sonuc, hatalar = {}, {}
    for ad, f in isler.items():
        _temizle()
        try:
            donus = f()
            sonuc[ad] = _say() | ({"donus": donus} if isinstance(donus, str) else {})
        except Exception as e:
            hatalar[ad] = f"{type(e).__name__}: {e}"
    gecti = not hatalar and all(v["dugum"] > 0 for k, v in sonuc.items() if k.startswith("profil:"))
    print("SONUC:" + json.dumps({"gecti": gecti, "blender": bpy.app.version_string, "sonuc": sonuc,
                                 "hatalar": hatalar}, ensure_ascii=False))


if __name__ == "__main__":
    _kanit()
