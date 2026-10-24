"""HERMES-KUR-1 PARÇA 6: Hermes'in kendi ürettiği skill'ler (bundled olmayanlar) → gitleaks kapısı → .kos/kopru/aday-skill/hermes/<ad> + 2. beyin olayı.
Kullanım: python tools/hermes_ogrenme.py [hermes_home] [aday_dizin]. Aday, omer-skills'e ancak inceleme + zip_denetle'den sonra girer (otomatik kopyalanmaz)."""
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def adaylar(home):
    manifest = home / "skills/.bundled_manifest"
    hazir = {s.split(":")[0] for s in manifest.read_text(encoding="utf-8").splitlines() if ":" in s} if manifest.exists() else set()
    return [d.parent for d in sorted((home / "skills").rglob("SKILL.md")) if d.parent.name not in hazir]


def temiz(dizin):
    r = subprocess.run(["gitleaks", "detect", "--no-git", "-s", str(dizin), "--exit-code", "1", "--redact"], capture_output=True, timeout=120)
    return r.returncode == 0


def main(home=KOK / "araclar/hermes-home", hedef=KOK / ".kos/kopru/aday-skill/hermes"):
    sonuc = {"aday": [], "kirmizi": []}
    for d in adaylar(Path(home)):
        if temiz(d):
            shutil.copytree(d, Path(hedef) / d.name, dirs_exist_ok=True)
            sonuc["aday"].append(d.name)
        else:
            sonuc["kirmizi"].append(d.name)
    if sonuc["aday"] or sonuc["kirmizi"]:
        subprocess.run([sys.executable, "-I", str(KOK / "tools/beyin_kayit.py"), "olay", "ders",
                        f"hermes-ogrenme: aday skill {len(sonuc['aday'])} ({','.join(sonuc['aday'])}), gitleaks kırmızı {len(sonuc['kirmizi'])}"], capture_output=True, timeout=60)
    return sonuc


if __name__ == "__main__":
    print(main(*[Path(a) for a in sys.argv[1:3]]))
