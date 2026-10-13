"""IG-41-KUR d4: dist/ig-41-kur — değişen departman/tasarim-katalog klasörleri düz zip (yayin-13eki biçimi) + 3. taraf aile paketi (paketle --buyuk)."""
import sys, zipfile
from pathlib import Path

WT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WT / "tools" / "skill-paket"))
import paketle
sys.path.insert(0, str(WT / "tools" / "secim"))
from dizin_uret import dosyalar  # KAPI-25: kabulsüz ajan zip'e girmez

cikti, kaynak = Path(sys.argv[1]), Path(sys.argv[2])  # kaynak: 3. taraf klonları (yalnız okunur)
cikti.mkdir(parents=True, exist_ok=True)
for ad in ["departman-arastirma-ogrenme", "departman-frontend", "departman-surec-ajan-arac",
           "departman-surec-inceleme", "departman-surec-plan", "tasarim-katalog"]:
    d = WT / "skills" / ad
    with zipfile.ZipFile(cikti / f"{ad}.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in (dosyalar(d) if ad.startswith("departman-") else sorted(p for p in d.rglob("*") if p.is_file())):
            z.write(f, f"{ad}/{f.relative_to(d).as_posix()}")
    print(cikti / f"{ad}.zip")
dizinler = [kaynak / "anatomy", kaynak / "hairline" / "skills" / "hairline-create", kaynak / "img2threejs",
            kaynak / "animation-performance", *sorted((kaynak / "youtube-agent-skill" / "skills").iterdir())]
for zp, n in paketle.buyuk("ig41-ucuncu-taraf", "3D/anatomi/saç modelleme, three.js sahne, animasyon performansı ve YouTube kanal işleri",
                           [str(x) for x in dizinler], str(cikti)):
    print(zp, n, "dosya", zp.stat().st_size // 1024, "KB")
