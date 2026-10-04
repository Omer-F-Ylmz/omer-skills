"""BLENDER-ARAC-1 K6: bpy statik kontrol — var olmayan bpy özniteliği/operatörü listeler.

    python tools/bpy_kontrol.py <betik.py>

Ayrı uv ortamı (önbellekli, projeye dokunmaz): fake-bpy-module-5.2 + pyright CLI; pyright-lsp eklentisi yok.
Çıkış: 0 temiz · 1 bulgu · 2 kullanım/çalışma hatası.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

PAKETLER = ["fake-bpy-module-5.2==20260730", "pyright==1.1.414"]


def main(argv=None):
    ap = argparse.ArgumentParser(description="bpy statik kontrol")
    ap.add_argument("betik")
    a = ap.parse_args(argv)
    betik = Path(a.betik)
    if not betik.is_file():
        print(f"betik yok: {betik}", file=sys.stderr)
        return 2
    paket = [x for p in PAKETLER for x in ("--with", p)]
    r = subprocess.run(["uv", "run", "--no-project", "--quiet", *paket, "--", "pyright", "--outputjson", str(betik)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
    try:
        veri = json.loads(r.stdout[r.stdout.find("{"):])
    except ValueError:
        ilk = lambda s: "\n".join((s or "").splitlines()[:15]) or "(boş)"  # noqa: E731  KÜÇÜK-1 K4
        print(f"pyright çıktısı çözülemedi (çıkış {r.returncode}):\n--- stderr ilk satırlar ---\n{ilk(r.stderr)}"
              f"\n--- ham çıktı ilk satırlar ---\n{ilk(r.stdout)}", file=sys.stderr)
        return 2
    bulgular = [{"satir": d["range"]["start"]["line"] + 1, "mesaj": d["message"]}
                for d in veri.get("generalDiagnostics", []) if d.get("rule") == "reportAttributeAccessIssue"]
    print(json.dumps({"bulgular": bulgular}, ensure_ascii=False))
    return 1 if bulgular else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
