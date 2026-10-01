"""BLENDER-ARAC-1 K3: görünüm kanıtı — 4 Workbench (ön · yan · üst · 3/4) + 1 Eevee kahraman + tek sayfa + dogrula.json.

    python tools/blender_gorunum.py <dosya.blend> [--referans on.png] [--iou-esik 0.90] [--bbox-esik 0.03]

Kanıt: Desktop\\<Proje>\\blender\\kanit\\<ad>-<zaman>\\. Workbench FLAT + SINGLE, X-ray kapalı; saydam ve
yansıtıcı nesneler de opak silüet (gizlenmez). Kamera uzaklığı bbox'tan. --referans: ön görünümde silüet IoU +
bbox oranı; eşikler öneri (kaynakta yok), rapora "esik_kaynak": "oneri".
Çıkış: blender_cli sözleşmesi (referans eşiği tutmazsa 1).
"""
import argparse
import json
import math
import sys
import time
from pathlib import Path

try:
    import bpy
except ImportError:
    bpy = None

BOY = 512
SIRA = ("on", "yan", "ust", "uc_ceyrek", "kahraman")


def _oku(yol):
    import numpy as np
    im = bpy.data.images.load(str(yol))
    w, h = im.size
    px = np.empty(w * h * 4, np.float32)
    im.pixels.foreach_get(px)
    bpy.data.images.remove(im)
    return px.reshape(h, w, 4)


def _kutu(m):
    import numpy as np
    ys, xs = np.nonzero(m)
    return (int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)) if len(xs) else (0, 0)


def _blender_ana():
    import numpy as np
    from mathutils import Vector
    sys.path.insert(0, str(Path(__file__).parent))
    import blender_dogrula
    a = json.loads(sys.argv[sys.argv.index("--") + 1])
    klasor = Path(a["klasor"])
    klasor.mkdir(parents=True, exist_ok=True)
    (klasor / "dogrula.json").write_text(json.dumps(blender_dogrula.kontroller(), ensure_ascii=False, indent=1),
                                         encoding="utf-8")
    sc, dg = bpy.context.scene, bpy.context.evaluated_depsgraph_get()
    ks = [o.matrix_world @ Vector(k) for o in sc.objects if o.type == "MESH" for k in o.evaluated_get(dg).bound_box]
    if not ks:
        print("SONUC:" + json.dumps({"gecti": False, "hata": "sahnede mesh yok"}))
        return
    mn, mx = Vector([min(k[i] for k in ks) for i in range(3)]), Vector([max(k[i] for k in ks) for i in range(3)])
    merkez, r = (mn + mx) / 2, max((mx - mn).length / 2, 1e-3)
    kv = bpy.data.cameras.new("dogrula_kam")
    kam = bpy.data.objects.new("dogrula_kam", kv)
    sc.collection.objects.link(kam)
    sc.camera = kam
    kv.clip_end = r * 20
    sc.render.resolution_x = sc.render.resolution_y = BOY
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = True
    sc.render.image_settings.file_format, sc.render.image_settings.color_mode = "PNG", "RGBA"

    def cek(ad, yon, orto):
        yon = Vector(yon).normalized()
        kv.type = "ORTHO" if orto else "PERSP"
        kv.ortho_scale = 2 * r * 1.05
        uzak = r * 3 if orto else r / math.sin(kv.angle / 2) * 1.05
        kam.location = merkez + yon * uzak
        kam.rotation_euler = (-yon).to_track_quat("-Z", "Y").to_euler()
        sc.render.filepath = str(klasor / f"{ad}.png")
        bpy.ops.render.render(write_still=True)

    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type, sh.single_color, sh.show_xray = "FLAT", "SINGLE", (0.8, 0.8, 0.8), False
    for ad, yon, orto in (("on", (0, -1, 0), True), ("yan", (1, 0, 0), True), ("ust", (0, 0, 1), True),
                          ("uc_ceyrek", (1, -1, 0.8), False)):
        cek(ad, yon, orto)

    try:
        sc.render.engine = "BLENDER_EEVEE"
    except TypeError:
        sc.render.engine = "BLENDER_EEVEE_NEXT"
    sc.eevee.taa_render_samples = 16
    if not sc.world:  # world yoksa cam/metal siyah görünür; nötr gri
        w = sc.world = bpy.data.worlds.new("dogrula_world")
        w.color = (0.5, 0.5, 0.5)
        if w.node_tree and "Background" in w.node_tree.nodes:
            w.node_tree.nodes["Background"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
    if not any(o.type == "LIGHT" for o in sc.objects):
        gunes = bpy.data.objects.new("dogrula_gunes", bpy.data.lights.new("dogrula_gunes", "SUN"))
        gunes.data.energy, gunes.rotation_euler = 3.0, (0.8, 0.2, 0.6)
        sc.collection.objects.link(gunes)
    cek("kahraman", (1, -1, 0.8), False)

    hucre = [_oku(klasor / f"{ad}.png") for ad in SIRA]
    sayfa = np.ones((2 * BOY, 3 * BOY, 4), np.float32)
    for i, p in enumerate(hucre):
        satir, sutun = divmod(i, 3)
        alfa = p[..., 3:4]
        sayfa[(1 - satir) * BOY:(2 - satir) * BOY, sutun * BOY:(sutun + 1) * BOY, :3] = p[..., :3] * alfa + (1 - alfa)
    im = bpy.data.images.new("sayfa", 3 * BOY, 2 * BOY, alpha=True)
    im.pixels.foreach_set(sayfa.ravel())
    im.filepath_raw, im.file_format = str(klasor / "sayfa.png"), "PNG"
    im.save()

    on = hucre[0][..., 3] > 0.5
    r_ = {"gecti": True, "klasor": str(klasor), "goruntuler": [str(klasor / f"{ad}.png") for ad in SIRA],
          "sayfa": str(klasor / "sayfa.png"), "on_maske_piksel": int(on.sum())}
    if a.get("referans"):
        ref = _oku(a["referans"])
        if ref[..., 3].min() < 0.99:
            rm = ref[..., 3] > 0.5
        else:  # alfasız referans: köşe rengi arka plan sayılır
            rm = np.abs(ref[..., :3] - ref[0, 0, :3]).max(-1) > 0.1
        h, w = rm.shape
        rm = rm[np.arange(BOY) * h // BOY][:, np.arange(BOY) * w // BOY]
        birlesim = int((on | rm).sum())
        iou = int((on & rm).sum()) / birlesim if birlesim else 0.0
        (w1, h1), (w2, h2) = _kutu(on), _kutu(rm)
        sapma = max(abs(w1 / w2 - 1), abs(h1 / h2 - 1)) if w2 and h2 else 1.0
        r_.update(iou=round(iou, 4), bbox_sapma=round(sapma, 4), iou_esik=a["iou_esik"], bbox_esik=a["bbox_esik"],
                  esik_kaynak="oneri", gecti=iou >= a["iou_esik"] and sapma <= a["bbox_esik"])
    print("SONUC:" + json.dumps(r_))


def main(argv=None):
    import blender_cli as bc
    import blender_oturum as bo
    ap = argparse.ArgumentParser(description="Blender görünüm kanıtı")
    ap.add_argument("blend")
    ap.add_argument("--referans")
    ap.add_argument("--iou-esik", type=float, default=0.90)
    ap.add_argument("--bbox-esik", type=float, default=0.03)
    ap.add_argument("--zaman-asimi", type=int, default=600)
    a = ap.parse_args(argv)
    blend = Path(a.blend)
    if not (bo.yol_gecerli(blend) and blend.is_file()) or (a.referans and not Path(a.referans).is_file()):
        print(f"yol kuralı: .blend Desktop\\<Proje>\\blender\\ altında ve var olmalı; referans var olmalı: {blend}",
              file=sys.stderr)
        return 2
    proje = blend.resolve().relative_to(bo.MASAUSTU.resolve()).parts[0]
    klasor = bo.MASAUSTU.resolve() / proje / "blender" / "kanit" / f"{blend.stem}-{time.strftime('%Y%m%d-%H%M%S')}"
    args = {"klasor": str(klasor), "referans": a.referans and str(Path(a.referans).resolve()),
            "iou_esik": a.iou_esik, "bbox_esik": a.bbox_esik}
    kod, sonuc, _ = bc.calistir(Path(__file__), args, blend=blend, zaman_asimi=a.zaman_asimi)
    if sonuc is not None:
        print(json.dumps(sonuc, ensure_ascii=False))
    return kod


if __name__ == "__main__":
    if bpy:
        _blender_ana()
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
        sys.exit(main())
