"""BİRLEŞTİR-21: main HEAD blob'larından dist/claude-ai-21 (plan-kur.zip yeni + yetenek-getir.zip replace)."""
import io, shutil, subprocess, sys, tarfile, tempfile, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "onay"), str(KOK / "tools" / "skill-paket"), str(KOK / "tools")]
import zip_denetle  # noqa: E402
import envanter_3_uygula as e3  # noqa: E402
import envanter_4_uygula as e4  # noqa: E402

bas = subprocess.run(["git", "rev-parse", "HEAD"], cwd=KOK, capture_output=True, text=True, check=True).stdout.strip()
tmp = Path(tempfile.mkdtemp())
tar = subprocess.run(["git", "archive", "--format=tar", bas, "skills/yetenek-getir", "skills/plan-kur", "docs/katalog"],
                     cwd=KOK, capture_output=True, check=True).stdout
tarfile.open(fileobj=io.BytesIO(tar)).extractall(tmp)

dist = KOK / "dist" / "claude-ai-21"
dist.mkdir(parents=True, exist_ok=True)
e3.zip_yaz(tmp / "skills" / "plan-kur", dist)
e4.KOK, e4.KAT = tmp, tmp / "docs" / "katalog"
ev = tmp / "ev"
shutil.copytree(tmp / "skills" / "yetenek-getir", ev / "skills" / "yetenek-getir")  # sahte CC hedefi; gerçek ~/.claude'a dokunmaz
assert e4.main(["--uygula"], ev=ev, dist=tmp / "d4") == 0
shutil.copyfile(tmp / "d4" / "yetenek-getir.zip", dist / "yetenek-getir.zip")
for ad in ("plan-kur", "yetenek-getir"):
    z = dist / f"{ad}.zip"
    adlar = zipfile.ZipFile(z).namelist()
    print(z.name, len(adlar), "dosya", z.stat().st_size // 1024, "KB · denetim:", zip_denetle.denetle(z) or "TEMİZ",
          "· skill.md:", [a for a in adlar if a.split("/")[-1].lower() == "skill.md"])
print("HEAD", bas[:7])
shutil.rmtree(tmp, ignore_errors=True)
