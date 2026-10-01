"""BLENDER-ARAC-2 K3: headless ışık/AO pişirme (UV2 lightmap + Cycles bake + denoise).

    python tools/blender_pisir.py <dosya.blend> --mod isik|ao [--nesneler a,b] [--boyut 1024|2048] [--hdr]

Kaynak .blend'e dokunmaz: <ad>-pismis.blend + <ad>-<mod>.png|exr aynı klasöre. Sıra: Apply Scale → UV2 "LightMap"
(smart unwrap, tek atlas, 8 px ada payı + 4 px bake taşması; UV1 render kanalı korunur) → Cycles bake (isik: diffuse
direct+indirect, renk yok; ao: AO) → denoise (compositor) → PNG'de yoğunluk <1 tutulur (önerilen lightMapIntensity
geri çarpar) ya da --hdr ile EXR (1). KARAR: yansıma pişmez, HDRI'de kalır; dönen ürün yalnız --mod ao.
GPU kilidi alınır (dolu → 2). Çıkış: blender_cli sözleşmesi 0/1/2/3.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import bpy
except ImportError:
    bpy = None

sys.path.insert(0, str(Path(__file__).parent))
import blender_cli as bc  # noqa: E402
import blender_oturum as bo  # noqa: E402
import gpu_kilit as gk  # noqa: E402

ORNEK = 64  # bake örneği; denoise gürültüyü alır


def _gpu(sc):
    try:
        pr = bpy.context.preferences.addons["cycles"].preferences
    except KeyError:
        return "CPU"
    for tur in ("OPTIX", "CUDA", "HIP", "ONEAPI"):
        try:
            pr.compute_device_type = tur
        except TypeError:
            continue
        pr.refresh_devices()
        if any(d.type == tur for d in pr.devices):
            for d in pr.devices:
                d.use = d.type == tur
            sc.cycles.device = "GPU"
            return tur
    return "CPU"


def _denoise(img, cikti, hdr, boyut):
    """Geçici sahnede yalnız compositor (Image → Denoise → çıkış); render katmanı yok, kamera gerekmez."""
    gs = bpy.data.scenes.new("pisir_denoise")
    ag = bpy.data.node_groups.new("pisir_denoise", "CompositorNodeTree")
    try:
        gs.render.resolution_x = gs.render.resolution_y = boyut
        gs.render.resolution_percentage = 100
        gs.view_settings.view_transform = "Standard"
        gs.compositing_node_group = ag
        ag.interface.new_socket(name="Image", in_out="OUTPUT", socket_type="NodeSocketColor")
        giris, dn, cik = (ag.nodes.new(t) for t in ("CompositorNodeImage", "CompositorNodeDenoise", "NodeGroupOutput"))
        giris.image = img
        ag.links.new(giris.outputs["Image"], dn.inputs["Image"])
        ag.links.new(dn.outputs["Image"], cik.inputs[0])
        gs.render.filepath = cikti
        gs.render.image_settings.file_format = "OPEN_EXR" if hdr else "PNG"
        gs.render.image_settings.color_mode = "RGB"
        bpy.ops.render.render(write_still=True, scene=gs.name)
        return True
    except Exception as e:  # ponytail: denoise düşerse ham bake yazılır, JSON'da denoise=hata
        img.filepath_raw, img.file_format = cikti, "OPEN_EXR" if hdr else "PNG"
        img.save()
        return f"{type(e).__name__}: {e}"
    finally:
        bpy.data.scenes.remove(gs)
        bpy.data.node_groups.remove(ag)


def _blender_ana():
    import numpy as np
    a = json.loads(sys.argv[sys.argv.index("--") + 1])
    t0, sc, boyut = time.time(), bpy.context.scene, a["boyut"]
    obs = [o for o in sc.objects if o.type == "MESH" and (not a["nesneler"] or o.name in a["nesneler"])]
    eksik = sorted(set(a["nesneler"] or []) - {o.name for o in obs})
    if not obs or eksik:
        print("SONUC:" + json.dumps({"gecti": False, "hata": f"nesne yok: {eksik or 'sahnede mesh yok'}"}))
        return
    for o in sc.objects:
        o.select_set(o in obs)
    bpy.context.view_layer.objects.active = obs[0]
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True, isolate_users=True)
    for o in obs:
        uv = o.data.uv_layers
        if len(uv):
            uv[0].active_render = True  # UV1 malzeme kanalı olarak kalır
        uv.active = uv.get("LightMap") or uv.new(name="LightMap")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(island_margin=8 / boyut, margin_method="FRACTION")  # çoklu edit → tek atlas
    bpy.ops.object.mode_set(mode="OBJECT")

    img = bpy.data.images.new(f"{a['ad']}-{a['mod']}", boyut, boyut, float_buffer=True)
    for o in obs:
        if not o.data.materials:
            o.data.materials.append(bpy.data.materials.new("pisir"))
        for m in filter(None, o.data.materials):
            if not m.node_tree:
                m.use_nodes = True
            n = m.node_tree.nodes.get("pisir_hedef") or m.node_tree.nodes.new("ShaderNodeTexImage")
            n.name, n.image = "pisir_hedef", img
            m.node_tree.nodes.active = n
    sc.render.engine = "CYCLES"
    cihaz = _gpu(sc)
    sc.cycles.samples = ORNEK
    if a["mod"] == "isik":
        bpy.ops.object.bake(type="DIFFUSE", pass_filter={"DIRECT", "INDIRECT"}, margin=4, use_clear=True)
    else:
        bpy.ops.object.bake(type="AO", margin=4, use_clear=True)

    px = np.empty(boyut * boyut * 4, np.float32)
    img.pixels.foreach_get(px)
    olcek = 1.0
    if not a["hdr"]:  # PNG'de 1 üstü kırpılır: p99.9 → 0.9'a indir, lightMapIntensity ile geri çarpılır
        olcek = max(1.0, float(np.percentile(px.reshape(-1, 4)[:, :3].max(1), 99.9)) / 0.9)
        px.reshape(-1, 4)[:, :3] /= olcek
        img.pixels.foreach_set(px)
    denoise = _denoise(img, a["cikti"], a["hdr"], boyut)
    img.filepath_raw, img.source = a["cikti"], "FILE"
    bpy.ops.wm.save_as_mainfile(filepath=a["pismis"], relative_remap=False)
    print("SONUC:" + json.dumps({
        "gecti": True, "mod": a["mod"], "nesneler": [o.name for o in obs], "uv_kanal": "LightMap",
        "uv_indeks": {o.name: o.data.uv_layers.find("LightMap") for o in obs}, "lightMapIntensity": round(olcek, 3),
        "goruntuler": [a["cikti"]], "pismis": a["pismis"], "sure_sn": round(time.time() - t0, 1), "cihaz": cihaz,
        "denoise": denoise}))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Headless ışık/AO pişirme (UV2 LightMap + Cycles + denoise)")
    ap.add_argument("blend")
    ap.add_argument("--mod", choices=["isik", "ao"], required=True)
    ap.add_argument("--nesneler", help="virgüllü nesne adları; yoksa tüm mesh")
    ap.add_argument("--boyut", type=int, choices=[1024, 2048], default=1024)
    ap.add_argument("--hdr", action="store_true", help="EXR (yoğunluk ölçeklenmez)")
    ap.add_argument("--zaman-asimi", type=int, default=900)
    a = ap.parse_args(argv)
    blend = Path(a.blend)
    if not (bo.yol_gecerli(blend) and blend.is_file()):
        print(f"yol kuralı: .blend Desktop\\<Proje>\\blender\\ altında ve var olmalı: {blend}", file=sys.stderr)
        return 2
    if (m := gk.al("blender_pisir", os.getpid())):
        print(f"DUR: {m}")
        return 2
    try:
        args = {"mod": a.mod, "nesneler": a.nesneler and a.nesneler.split(","), "boyut": a.boyut, "hdr": a.hdr,
                "ad": blend.stem, "pismis": str(blend.with_name(f"{blend.stem}-pismis.blend")),
                "cikti": str(blend.with_name(f"{blend.stem}-{a.mod}.{'exr' if a.hdr else 'png'}"))}
        kod, sonuc, _ = bc.calistir(Path(__file__), args, blend=blend, zaman_asimi=a.zaman_asimi)
    finally:
        gk.birak("blender_pisir")
    if sonuc is not None:
        print(json.dumps(sonuc, ensure_ascii=False))
    return kod


if __name__ == "__main__":
    if bpy:
        _blender_ana()
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.exit(main())
