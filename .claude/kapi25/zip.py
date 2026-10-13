"""KAPI-25: KABUL 5 ajanı KALITE3'e ekleyip departman zip'lerini üretir; claude.ai'deki sürümden (dist/skill-secim-1/kendi) farklı
olanları dist/kapi-25/ altına koyar + LISTE.md. Kayıp ya da değişen dosya varsa rc=1 (yalnız ekleme beklenir)."""
import shutil, sys, tempfile, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "secim"), str(KOK / "onay")]
import dizin_uret  # noqa: E402
from kapi_25_uygula import plan  # noqa: E402

YUKLU = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/Projeler/omer-skills/dist/skill-secim-1/kendi")
CIKTI = KOK / "dist" / "kapi-25"


def icerik(z):
    with zipfile.ZipFile(z) as f:
        return {n: f.read(n) for n in f.namelist()}


sys.stdout.reconfigure(encoding="utf-8")
dizin_uret.KALITE3.update(dict(plan(KOK)))
satirlar, hata = [], False
with tempfile.TemporaryDirectory() as tmp:
    for z in sorted(dizin_uret.zipla(KOK, Path(tmp)).glob("*.zip")):
        yeni, eski = icerik(z), icerik(YUKLU / z.name)
        ek = sorted(set(yeni) - set(eski))
        kayip = sorted(set(eski) - set(yeni))
        degisen = sorted(n for n in set(yeni) & set(eski) if yeni[n] != eski[n])
        if not (ek or kayip or degisen):
            continue
        CIKTI.mkdir(parents=True, exist_ok=True)
        shutil.copy2(z, CIKTI / z.name)
        hata |= bool(kayip or degisen)
        skill = z.stem
        satirlar.append(f"- **{z.name}** → claude.ai skill `{skill}` (Upload and replace)\n"
                        f"  - eklenen ajanlar: {', '.join(Path(n).stem for n in ek) or '-'}\n"
                        f"  - claude.ai sürümüne göre: +{len(ek)} dosya · kayıp {len(kayip)} · değişen {len(degisen)}"
                        + (f" ({', '.join(kayip + degisen)})" if kayip or degisen else ""))
(CIKTI / "LISTE.md").write_text(
    "# KAPI-25 departman zip'leri\n\nKarşılaştırma tabanı: dist/skill-secim-1/kendi (claude.ai'de yüklü sürüm). "
    "Kalan departman zip'leri birebir aynı → yeniden yüklenmez.\n\n" + "\n".join(satirlar) + "\n", encoding="utf-8", newline="\n")
print("\n".join(satirlar))
sys.exit(int(hata))
