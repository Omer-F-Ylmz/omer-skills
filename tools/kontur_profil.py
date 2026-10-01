# /// script
# requires-python = ">=3.12"
# dependencies = ["opencv-python-headless", "numpy"]
# ///
"""BLENDER-ARAC-2 K4: silüetten dönel model (7-blender.md Q4).

    uv run tools/kontur_profil.py <siluet.png> --yukseklik-mm N [--kulp sag|sol|yok] [--ic-profil] [--blend <çıktı.blend>]

Maske: alfa varsa alfa>127, yoksa kenar medyanından ayrışan pikseller; en büyük bileşen. Eksen: üst ve alt %15
bantlarındaki satır sol/sağ kenar orta noktalarının medyanı (kulp bandı dışı). Profil kulpsuz yarıdan (--kulp sag →
sol yarı aynalanır). piksel→mm: --yukseklik-mm / silüet piksel yüksekliği. Çıktı JSON: sadeleştirilmiş vertex zinciri
(x=yarıçap, z=yükseklik, mm; tabandan başlar, dudak dahil). --ic-profil: görüntü kesittir, iç duvar konturdan gelir;
yoksa üst kapak düşer (açık kap) ve Solidify 3 mm içe.
--blend: XZ düzleminde x=0 eksenli profil + Screw 360° Z (32/64, Merge; normal dışa) + Subdivision 1 (+ Solidify) →
blender_gorunum --referans (kulpsuz gövde maskesi aynalanmış, gorunum'un ön ortho çerçevesine oturtulmuş) → IoU.
opencv-python-headless Apache-2.0 (uv betik ortamı). Çıkış: 0 · 1 IoU < 0.95 · 2 yol/girdi · 3 Blender çöktü.
"""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

try:
    import bpy
except ImportError:
    bpy = None

sys.path.insert(0, str(Path(__file__).parent))
import blender_cli as bc  # noqa: E402
import blender_oturum as bo  # noqa: E402

ESIK_IOU = 0.95
SOLIDIFY_MM = 3.0
BOY = 512  # blender_gorunum.BOY


def profil(yol, yukseklik_mm, kulp, ic):
    import cv2
    import numpy as np
    g = cv2.imread(str(yol), cv2.IMREAD_UNCHANGED)
    if g is None:
        return None
    if g.ndim == 3 and g.shape[2] == 4 and g[..., 3].min() < 255:
        m = g[..., 3] > 127
    else:
        gri = g if g.ndim == 2 else cv2.cvtColor(g[..., :3], cv2.COLOR_BGR2GRAY)
        kenar = np.concatenate([gri[0], gri[-1], gri[:, 0], gri[:, -1]])
        m = np.abs(gri.astype(int) - int(np.median(kenar))) > 40
    n, etiket, ist, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8))
    if n < 2:
        return None
    m = etiket == 1 + int(np.argmax(ist[1:, cv2.CC_STAT_AREA]))
    ys = np.where(m.any(1))[0]
    ust, alt = int(ys[0]), int(ys[-1])
    h = alt - ust + 1
    bant = max(1, int(h * 0.15))
    orta = [(np.argmax(m[y]) + m.shape[1] - 1 - np.argmax(m[y, ::-1])) / 2
            for y in [*range(ust, ust + bant), *range(alt - bant + 1, alt + 1)]]
    eksen = float(np.median(orta))
    c0 = int(round(eksen + 0.5))  # eksenin sağındaki ilk sütun
    yari = m[:, :c0][:, ::-1] if kulp == "sag" else m[:, c0:]
    s = yukseklik_mm / h  # mm/piksel

    cs, _ = cv2.findContours(yari.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    k = max(cs, key=cv2.contourArea)[:, 0, :]
    eks = k[:, 0] <= 0
    if eks.any() and not eks.all():  # eksen üstündeki koşuyu at, zinciri eksenden sonra başlat
        i = next(j for j in range(len(k)) if not eks[j] and eks[j - 1])
        k, eks = np.roll(k, -i, 0), np.roll(eks, -i)
        k = k[:int(np.argmax(eks))]
    if k[0][1] < k[-1][1]:
        k = k[::-1]  # tabandan başlasın
    if not ic:  # açık kap: üst kapak (dudak köşesi hariç) düşer
        while len(k) > 2 and k[-1][1] <= ust + 1 and k[-2][1] <= ust + 1 and k[-2][0] > k[-1][0]:
            k = k[:-1]
    k = cv2.approxPolyDP(np.ascontiguousarray(k).reshape(-1, 1, 2).astype(np.int32), 0.75, False)[:, 0, :]
    zincir = [[round((x + 0.5) * s, 3), round((alt + 0.5 - y) * s, 3)] for x, y in k]
    zincir = [[0.0, zincir[0][1]], *zincir] + ([[0.0, zincir[-1][1]]] if ic else [])
    xs, zs = [p[0] for p in zincir], [p[1] for p in zincir]
    rp = int(np.where(yari.any(0))[0].max()) + 1
    govde = yari[ust:alt + 1, :rp]
    return {"eksen_px": eksen, "mm_px": round(s, 5), "yukseklik_mm": round(max(zs) - min(zs), 3),
            "yaricap_mm": round(max(xs), 3), "nokta": len(zincir), "zincir": zincir,
            "_govde": np.hstack([govde[:, ::-1], govde])}


def referans(govde, yol):
    """Kulpsuz gövde maskesini gorunum ön kamerasının çerçevesine (bbox merkezi, ortho 2r·1.05, BOY²) yerleştirir."""
    import cv2
    import numpy as np
    h, w = govde.shape
    r = 0.5 * math.sqrt(2 * w * w + h * h)  # yarı-köşegen (2R × 2R × H)
    k = BOY / (2 * r * 1.05)
    gw, gh = max(1, round(w * k)), max(1, round(h * k))
    kucuk = cv2.resize(govde.astype(np.uint8) * 255, (gw, gh), interpolation=cv2.INTER_AREA) > 127
    t = np.zeros((BOY, BOY), np.uint8)
    t[(BOY - gh) // 2:(BOY - gh) // 2 + gh, (BOY - gw) // 2:(BOY - gw) // 2 + gw] = kucuk * 255
    cv2.imwrite(str(yol), np.dstack([t, t, t, t]))


def _blender_ana():
    a = json.loads(sys.argv[sys.argv.index("--") + 1])
    bpy.ops.wm.read_factory_settings(use_empty=True)
    vs, adim = [], max(z for _, z in a["zincir"]) / 100  # sık zincir: Subsurf köşe yuvarlaması yerel kalır
    for (x0, z0), (x1, z1) in zip(a["zincir"], a["zincir"][1:]):
        n = max(1, math.ceil(math.hypot(x1 - x0, z1 - z0) / adim))
        vs += [((x0 + (x1 - x0) * i / n) / 1000, 0, (z0 + (z1 - z0) * i / n) / 1000) for i in range(n)]
    vs.append((a["zincir"][-1][0] / 1000, 0, a["zincir"][-1][1] / 1000))
    me = bpy.data.meshes.new(a["ad"])
    me.from_pydata(vs, [(i, i + 1) for i in range(len(vs) - 1)], [])
    o = bpy.data.objects.new(a["ad"], me)
    bpy.context.scene.collection.objects.link(o)
    vida = o.modifiers.new("Screw", "SCREW")
    vida.axis, vida.angle, vida.steps, vida.render_steps = "Z", 2 * math.pi, 32, 64
    vida.use_merge_vertices = True
    dg = bpy.context.evaluated_depsgraph_get()
    ev = o.evaluated_get(dg)
    em = ev.to_mesh()
    if sum(p.normal.x * p.center.x + p.normal.y * p.center.y for p in em.polygons) < 0:
        vida.use_normal_flip = True  # normal dışa → Solidify -1 içe kalınlaşır, silüet değişmez
    ev.to_mesh_clear()
    alt_b = o.modifiers.new("Subdivision", "SUBSURF")
    alt_b.levels = alt_b.render_levels = 1
    if not a["ic"]:
        kat = o.modifiers.new("Solidify", "SOLIDIFY")
        kat.thickness, kat.offset, kat.use_even_offset = SOLIDIFY_MM / 1000, -1, True
    bpy.ops.wm.save_as_mainfile(filepath=a["cikti"], relative_remap=False)
    print("SONUC:" + json.dumps({"gecti": True, "cikti": a["cikti"]}))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Silüetten dönel profil (+ Screw modeli, IoU öz-doğrulama)")
    ap.add_argument("siluet")
    ap.add_argument("--yukseklik-mm", type=float, required=True)
    ap.add_argument("--kulp", choices=["sag", "sol", "yok"], default="yok")
    ap.add_argument("--ic-profil", action="store_true")
    ap.add_argument("--blend")
    a = ap.parse_args(argv)
    if a.blend and not bo.yol_gecerli(Path(a.blend)):
        print(f"yol kuralı: .blend Desktop\\<Proje>\\blender\\ altında olmalı: {a.blend}", file=sys.stderr)
        return 2
    p = profil(a.siluet, a.yukseklik_mm, a.kulp, a.ic_profil) if Path(a.siluet).is_file() else None
    if p is None:
        print(f"silüet okunamadı ya da boş: {a.siluet}", file=sys.stderr)
        return 2
    govde = p.pop("_govde")
    if not a.blend:
        print(json.dumps(p, ensure_ascii=False))
        return 0
    blend = Path(a.blend)
    blend.parent.mkdir(parents=True, exist_ok=True)
    args = {"zincir": p["zincir"], "ic": a.ic_profil, "cikti": str(blend), "ad": blend.stem}
    kod, sonuc, _ = bc.calistir(Path(__file__), args, zaman_asimi=300)
    if kod:
        print(json.dumps({**p, "blender": sonuc}, ensure_ascii=False))
        return kod
    ref = blend.with_name(f"{blend.stem}-referans.png")
    referans(govde, ref)
    g = subprocess.run([sys.executable, str(Path(__file__).with_name("blender_gorunum.py")), str(blend),
                        "--referans", str(ref), "--iou-esik", str(ESIK_IOU)],
                       capture_output=True, text=True, encoding="utf-8")
    try:
        gr = json.loads(g.stdout)
        iou = gr["iou"]
    except (ValueError, KeyError):
        print(json.dumps({**p, "gorunum_hata": (g.stdout + g.stderr)[-500:]}, ensure_ascii=False))
        return 3
    p.update(blend=str(blend), referans=str(ref), iou=iou, iou_esik=ESIK_IOU, gecti=iou >= ESIK_IOU,
             kanit=gr.get("klasor"))
    print(json.dumps(p, ensure_ascii=False))
    return 0 if p["gecti"] else 1


if __name__ == "__main__":
    if bpy:
        _blender_ana()
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.exit(main())
