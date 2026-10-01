"""BLENDER-ARAC-1 K4: GLB hattı — optimize (meshopt + webp) → validate → inspect özeti → önce/sonra KB.

    python tools/glb_hat.py <girdi.glb> [--cikti X.glb] [--doku 2048]

Girdi ve çıktı yalnız Desktop\\<Proje>\\ altında. Çıkış: 0 · 1 optimize/validate hatası · 2 kullanım/yol.
gltf-transform: npm.cmd i -g @gltf-transform/cli@4.5.1 (MIT).
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import blender_cli as bc


def gt(*args):
    exe = shutil.which("gltf-transform.cmd") or shutil.which("gltf-transform")
    if not exe:
        raise FileNotFoundError("gltf-transform yok: npm.cmd i -g @gltf-transform/cli@4.5.1")
    return subprocess.run([exe, *map(str, args)], capture_output=True, text=True, encoding="utf-8", errors="replace")


def validate(glb):
    """{"hata", "uyari", "kodlar"} — tablo satırlarının severity sütunundan (0 hata · 1 uyarı)."""
    r = gt("validate", glb)
    satirlar = [[h.strip() for h in s.split("│")[1:-1]] for s in r.stdout.splitlines() if s.count("│") >= 5]
    satirlar = [h for h in satirlar if h[2] in ("0", "1", "2", "3")]
    hata = sum(h[2] == "0" for h in satirlar)
    return {"hata": max(hata, int(r.returncode != 0)), "uyari": sum(h[2] == "1" for h in satirlar),
            "kodlar": sorted({h[0] for h in satirlar if h[2] == "0"})[:10]}


def main(argv=None):
    ap = argparse.ArgumentParser(description="GLB optimize + validate")
    ap.add_argument("girdi")
    ap.add_argument("--cikti")
    ap.add_argument("--doku", type=int, default=2048)
    a = ap.parse_args(argv)
    girdi = Path(a.girdi)
    cikti = Path(a.cikti) if a.cikti else girdi.with_name(girdi.stem + "-opt.glb")
    if not girdi.is_file() or not (bc.proje_ici(girdi) and bc.proje_ici(cikti)):
        print(f"yol kuralı: girdi var olmalı, girdi/çıktı yalnız Desktop\\<Proje>\\ altında: {girdi} → {cikti}", file=sys.stderr)
        return 2
    try:
        r = gt("optimize", girdi, cikti, "--compress", "meshopt", "--texture-compress", "webp",
               "--texture-size", a.doku)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        return 2
    if r.returncode != 0 or not cikti.is_file():
        print(f"optimize hatası:\n{(r.stderr or r.stdout)[-1500:]}", file=sys.stderr)
        return 1
    v = validate(cikti)
    inspect = [s.strip() for s in gt("inspect", cikti, "--format", "md").stdout.splitlines() if s.startswith("|")][:12]
    sonuc = {"gecti": v["hata"] == 0, "cikti": str(cikti), "once_kb": round(girdi.stat().st_size / 1024, 1),
             "sonra_kb": round(cikti.stat().st_size / 1024, 1), "validate": v, "inspect": inspect}
    print(json.dumps(sonuc, ensure_ascii=False))
    return 0 if sonuc["gecti"] else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
