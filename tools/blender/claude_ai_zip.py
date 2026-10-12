"""BLENDER-1-devam-5: blender-oturum + blender-uretim claude.ai zip'leri (yerel yola bağlı değil).
    python tools/blender/claude_ai_zip.py <hedef klasör>   → <hedef>/blender-*.zip + zip_denetle sonucu (temizse rc 0)
tarif.py references/'e girer (isik_kur/malzemeler yanında, `blender -b -P references/tarif.py -- @spec.json`);
mutlak yerel yollar repo-göreli yazılır. CC tarafı (skills/) değişmez."""
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
SKILLER = ("blender-oturum", "blender-uretim")
DEGIS = [  # sıra önemli: özel önce
    ("`blender_cli.py C:/Projeler/omer-skills/tools/blender/lib/tarif.py @<spec.json> [--blend B]`",
     "`blender -b [B] -P <blender-uretim>/references/tarif.py -- @<spec.json>`"),
    ("tools/blender/lib/tarif.py", "references/tarif.py"),
    ("C:/Projeler/omer-skills/", ""), ("C:\\Projeler\\omer-skills\\", ""), ("C:\\Users\\pc\\Desktop", "Desktop"),
]


def metin(veri):
    s = veri.decode("utf-8")
    for a, b in DEGIS:
        s = s.replace(a, b)
    return s.encode("utf-8")


def paketle(hedef):
    hedef = Path(hedef)
    hedef.mkdir(parents=True, exist_ok=True)
    zipler = []
    for ad in SKILLER:
        kaynak = KOK / "skills" / ad
        dosyalar = [(p, p.relative_to(kaynak.parent).as_posix()) for p in sorted(kaynak.rglob("*"))
                    if p.is_file() and "__pycache__" not in p.parts]
        if ad == "blender-uretim":
            dosyalar.append((KOK / "tools/blender/lib/tarif.py", f"{ad}/references/tarif.py"))
        zp = hedef / f"{ad}.zip"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for p, yol in dosyalar:
                veri = p.read_bytes()
                z.writestr(yol, metin(veri) if p.suffix in (".md", ".py") else veri)
        zipler.append(zp)
    return zipler


if __name__ == "__main__":
    sys.path.insert(0, str(KOK / "tools" / "skill-paket"))
    import zip_denetle
    sys.stdout.reconfigure(encoding="utf-8")
    kirli = 0
    for zp in paketle(sys.argv[1]):
        sorun = zip_denetle.denetle(zp)
        kirli += bool(sorun)
        print(zp, "TEMİZ" if not sorun else sorun)
    sys.exit(kirli)
