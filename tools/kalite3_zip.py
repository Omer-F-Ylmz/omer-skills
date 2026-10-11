"""KALİTE-3 İKİ TARAF: kabul edilen skill'lerin claude.ai zip'i — CC onay betiğinin yazacağıyla aynı içerik
(.kalite3/pilot/<ad> + aciklama-yeni.jsonl açıklaması). Canlıya dokunmaz.
  python tools/kalite3_zip.py dist/yukle-15        # kabul listesi: docs/kutuphane/kalite3-kabul.txt
"""
import shutil, sys, tempfile, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "onay"))
from kalite_3_uygula import aciklama_yaz, plan  # noqa: E402


def zip_yap(p, cikti):
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / p["ad"]
        shutil.copytree(p["bolunmus"], d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        if p["aciklama"] and not aciklama_yaz(d / "SKILL.md", p["aciklama"]):
            print(f"  {p['ad']}: açıklama çok satırlı, eskisi kaldı")
        z = cikti / f"{p['ad']}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(d.rglob("*")):
                if f.is_file():
                    zf.write(f, f"{p['ad']}/{f.relative_to(d).as_posix()}")
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1] if len(sys.argv) > 1 else KOK / "dist" / "yukle-15")
    cikti.mkdir(parents=True, exist_ok=True)
    for p in plan():
        if p["bolunmus"]:
            print(zip_yap(p, cikti))


if __name__ == "__main__":
    main()
