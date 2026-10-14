"""ATLAS-1 d1: claude.ai zip'leri HEAD blob'larından (dist19 yöntemi). Atıf satırındaki docs/atlas/ yolu zip içinde aynı göreli yolda
bulunur (claude.ai yerel yola bağlı kalmaz). python .claude/atlas/dist.py → dist/claude-ai-22/<skill>.zip + LISTE.md"""
import io, subprocess, sys, tarfile, tempfile, zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(KOK / "tools" / "skill-paket"), str(KOK / "tools" / "secim")]
import zip_denetle, dizin_uret  # noqa: E402

DIST = KOK / "dist" / "claude-ai-22"
BASLIK = "ATLAS-1 d1"  # ATLAS-2: .claude/atlas2/dist.py DIST/BASLIK/EK'i ezer
EK = {"departman-frontend": ["docs/atlas/site-3d.md", "docs/atlas/kart.jsonl"], "blender-uretim": ["docs/atlas/site-3d.md"]}


def git(*a):
    return subprocess.run(["git", "-C", str(KOK), *a], capture_output=True, check=True).stdout


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    DIST.mkdir(parents=True, exist_ok=True)
    rev = git("rev-parse", "--short", "HEAD").decode().strip()
    satir, sorunlar = [], []
    with tempfile.TemporaryDirectory() as t:
        tarfile.open(fileobj=io.BytesIO(git("archive", "HEAD", "skills"))).extractall(t, filter="data")
        for ad, ekler in EK.items():
            d = Path(t) / "skills" / ad
            dosya = dizin_uret.dosyalar(d) if ad.startswith("departman-") else sorted(p for p in d.rglob("*") if p.is_file())
            zp = DIST / f"{ad}.zip"
            with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
                for f in dosya:  # core.autocrlf=true → blob baytı
                    rel = f"{ad}/{f.relative_to(d).as_posix()}"
                    z.writestr(rel, git("show", f"HEAD:skills/{rel}"))
                for e in ekler:
                    z.writestr(f"{ad}/{e}", git("show", f"HEAD:{e}"))
            s = zip_denetle.denetle(zp)
            sorunlar += s
            satir.append(f"- **{ad}** · replace · {len(dosya) + len(ekler)} dosya, {zp.stat().st_size / 1024:.1f} KB · "
                         f"+ {', '.join(ekler)} · {'TEMİZ' if not s else 'SORUN'}")
    (DIST / "LISTE.md").write_text(
        f"# dist/{DIST.name} — {BASLIK} (HEAD {rev})\n\nclaude.ai'de mevcut skill'in yerine yüklenir (replace). Atıf satırındaki "
        "`docs/atlas/*.md` zip içinde aynı yolda; içindeki `python tools/...` komutları CC içindir, claude.ai'de araç adı rehberi.\n\n"
        + "\n".join(satir) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(satir + sorunlar))
    return 1 if sorunlar else 0


if __name__ == "__main__":
    sys.exit(main())
