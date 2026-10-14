"""ÖĞREN-1 d3: claude.ai zip'leri → dist/ogren-1/. Skill'ler docs/ogren/token.md'yi andığı için dosya zip içine aynı göreli yolla girer
(claude.ai yerel yola bağlı kalmaz). Sonra: python tools/skill-paket/zip_denetle.py dist/ogren-1/*.zip
  python -X utf8 .claude/ogren1/zipla.py"""
import zipfile
from pathlib import Path

KOK = Path(r"C:\Projeler\omer-skills")
CIKTI = KOK / "dist/ogren-1"
CIKTI.mkdir(parents=True, exist_ok=True)
for ad, ek in [("is-akisi", True), ("departman-verimlilik", True), ("video-uygula", False)]:
    with zipfile.ZipFile(CIKTI / f"{ad}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted((KOK / "skills" / ad).rglob("*")):
            if f.is_file():
                z.write(f, f"{ad}/{f.relative_to(KOK / 'skills' / ad).as_posix()}")
        if ek:
            z.write(KOK / "docs/ogren/token.md", f"{ad}/docs/ogren/token.md")
    print(ad, len(zipfile.ZipFile(CIKTI / f"{ad}.zip").namelist()), "dosya")
