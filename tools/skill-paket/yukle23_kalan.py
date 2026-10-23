"""SKILL-YUKLE-1 kalanlar: gstack (yalnız metin dosyaları, node_modules/ikili yok) ve küçük harf skill.md'li iki wix skill'i.
Kullanım: python -I yukle23_kalan.py <cikti_dizini>  (y23-gstack*.zip, y23-wix-entry.zip üretir)"""
import os, sys, shutil, pathlib, tempfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from paketle import buyuk

HOME = pathlib.Path.home() / ".claude"
GSTACK = HOME / "skills" / "gstack"
WIX = HOME / "plugins/cache/knowledge-work-plugins/wix/1.19.1/skills"
ATLA = {"node_modules", ".git", "extension", "bin", "browse", "hosts", "patches", "licenses", "contrib"}
UZANTI = {".md", ".tmpl", ".txt", ".json", ".yaml", ".yml"}
SINIR = 200_000


def kopyala(kaynak, hedef, derin):
    for kok, dizinler, dosyalar in os.walk(kaynak):
        dizinler[:] = [d for d in dizinler if d not in ATLA and (derin or not (pathlib.Path(kok) / d / "SKILL.md").exists())]
        for f in dosyalar:
            p = pathlib.Path(kok) / f
            if p.suffix.lower() in UZANTI and p.stat().st_size <= SINIR and f != "bun.lock":
                h = hedef / p.relative_to(kaynak)
                h.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, h)


def main(cikti):
    sahne = pathlib.Path(tempfile.mkdtemp(prefix="y23kalan-"))
    gs = []
    for sk in [GSTACK] + [p.parent for p in GSTACK.rglob("SKILL.md") if not (set(p.parts) & ATLA) and p.parent != GSTACK]:
        h = sahne / "gstack" / sk.relative_to(GSTACK).as_posix().replace("/", "__") if sk != GSTACK else sahne / "gstack" / "_kok"
        kopyala(sk, h, False)
        gs.append(str(h))
    wx = []
    for ad, alt in (("wix-headless-entry", "wix-headless/entry"), ("wix-headless-fast-entry", "wix-headless-fast/entry")):
        h = sahne / "wix" / ad
        shutil.copytree(WIX / alt, h)
        (h / "skill.md").rename(h / "SKILL.md")
        wx.append(str(h))
    for ad, konu, kay in (("y23-gstack", "gstack takımı", gs), ("y23-wix-entry", "wix entry skill'leri", wx)):
        for zp, n in buyuk(ad, konu, kay, cikti):
            print(zp, n)
    shutil.rmtree(sahne, ignore_errors=True)


if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1]))
