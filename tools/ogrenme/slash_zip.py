"""SLASH-ÖĞREN d4: slash-katalog işaretçisi claude.ai zip'inde çözülsün. Katalog işaretçisi olan her skill (departman-* + yetenek-getir) için
dist/slash-2/<skill>.zip: skill klasörü + reference/slash-katalog.md kopyası; zip içi SKILL.md'de yol `reference/slash-katalog.md` olur
(repodaki dosya değişmez, tek kaynak). Kullanım: python tools/ogrenme/slash_zip.py  → sonra zip_denetle.py dist/slash-2"""
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
KATALOG = KOK / "skills" / "yetenek-getir" / "reference" / "slash-katalog.md"
ESKI, YENI = "`yetenek-getir/reference/slash-katalog.md`", "`reference/slash-katalog.md`"
COP = ("__pycache__", ".pyc", ".DS_Store")


def zip_yaz(skill, cikti):
    with zipfile.ZipFile(cikti / f"{skill.name}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(p for p in skill.rglob("*") if p.is_file() and not any(c in p.as_posix() for c in COP)):
            ic = f.relative_to(skill).as_posix()
            veri = f.read_bytes()
            if ic == "SKILL.md":
                veri = veri.decode("utf-8").replace(ESKI, YENI).encode("utf-8")
            z.writestr(f"{skill.name}/{ic}", veri)
        if skill.name != "yetenek-getir":
            z.writestr(f"{skill.name}/reference/slash-katalog.md", KATALOG.read_bytes())


if __name__ == "__main__":
    cikti = KOK / "dist" / "slash-2"
    cikti.mkdir(parents=True, exist_ok=True)
    adlar = [s for s in sorted((KOK / "skills").iterdir()) if (s / "SKILL.md").exists() and ESKI in (s / "SKILL.md").read_text(encoding="utf-8")]
    for s in adlar:
        zip_yaz(s, cikti)
    print(len(adlar), "zip →", cikti)
