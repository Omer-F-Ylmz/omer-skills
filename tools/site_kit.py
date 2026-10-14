"""Scroll-anlatı site kiti (TELVE'den): Astro + GSAP/Lenis + bölüm şablonu + sahne yükleyici + poster AVIF + reduced-motion + kapı (kapi.mjs, eşik) + DESIGN.md storyboard + sıvı modülü; `python tools/site_kit.py <boş klasör> [ad]` kurar."""
import shutil
import sys
from pathlib import Path

SABLON = Path(__file__).parent / "site-kit" / "sablon"


def kur(hedef: Path, ad: str):
    if hedef.exists() and any(hedef.iterdir()):
        sys.exit(f"hedef boş değil: {hedef}")
    shutil.copytree(SABLON, hedef, dirs_exist_ok=True)
    for f in (hedef / "package.json", hedef / "src/pages/index.astro", hedef / "DESIGN.md"):
        f.write_bytes(f.read_bytes().replace(b"__AD__", ad.encode("utf8")))
    print(f"kuruldu: {hedef}\nsonra: cd {hedef} && npm install && npm run dev · kapı: npm run kapi")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    h = Path(sys.argv[1]).resolve()
    kur(h, sys.argv[2] if len(sys.argv) > 2 else h.name)
