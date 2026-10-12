"""KALİTE-3 İKİ TARAF: kabul edilen skill'lerin claude.ai zip'i — CC onay betiğinin yazacağıyla aynı içerik
(.kalite3/pilot/<ad> + aciklama-yeni.jsonl açıklaması). Canlıya dokunmaz. Zip/klasör/name = claude.ai'deki mevcut ad
(aynı ad → Replace; farklı ad kopya oluşturur). claude.ai'de tek başına yoksa (aile paketi üyesi) zip yazılmaz.
  python tools/kalite3_zip.py dist/yukle-15 [claudeai_adlar.json]   # kabul listesi: docs/kutuphane/kalite3-kabul.txt
"""
import json, re, shutil, sys, tempfile, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(KOK / "onay"))
from kalite_3_uygula import aciklama_yaz, plan  # noqa: E402


ADLAR = Path("C:/Projeler/omer-skills/.kos/kopru/claudeai_adlar.json")


def claudeai_adi(ad, giris):
    if ad in giris:
        return ad
    aday = [g for g in giris if g.endswith("-" + ad) and "-" not in g[:-len(ad) - 1]]  # gstack-x evet, gstack-plan-x hayır
    return aday[0] if len(aday) == 1 else None


def zip_yap(p, cikti, ad):
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / ad
        shutil.copytree(p["bolunmus"], d, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store"))
        if p["aciklama"] and not aciklama_yaz(d / "SKILL.md", p["aciklama"]):
            print(f"  {p['ad']}: açıklama çok satırlı, eskisi kaldı")
        sk = d / "SKILL.md"
        sk.write_text(re.sub(r"^name:.*$", f"name: {ad}", sk.read_text(encoding="utf-8"), count=1, flags=re.M),
                      encoding="utf-8", newline="\n")
        z = cikti / f"{ad}.zip"
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in sorted(d.rglob("*")):
                if f.is_file():
                    zf.write(f, f"{ad}/{f.relative_to(d).as_posix()}")
    return z


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cikti = Path(sys.argv[1] if len(sys.argv) > 1 else KOK / "dist" / "yukle-15")
    cikti.mkdir(parents=True, exist_ok=True)
    giris = json.loads(Path(sys.argv[2] if len(sys.argv) > 2 else ADLAR).read_text(encoding="utf-8"))["giris"]
    for p in plan():
        if p["bolunmus"]:
            ad = claudeai_adi(p["ad"], giris)
            print(zip_yap(p, cikti, ad) if ad else f"  {p['ad']}: claude.ai'de tek başına yok (aile paketi üyesi?), zip yazılmadı")


if __name__ == "__main__":
    main()
