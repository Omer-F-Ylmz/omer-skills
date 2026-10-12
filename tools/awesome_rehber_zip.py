"""İKİ TARAF: /awesome-rehber claude.ai paketi. docs/kaynak/awesome/*.tsv zip içine references/ olarak gömülür
(claude.ai'de yerel yol yok); CC kurulumu da aynı düzeni kullanır (onay betiği).
  python tools/awesome_rehber_zip.py   → dist/yukle-claude-ai/awesome-rehber.zip"""
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
EN_COK_DOSYA = 200  # claude.ai: "Zip contains too many files (maximum 200)"


def paketle(skill, kaynak, cikti):
    cikti.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(skill / "SKILL.md", "awesome-rehber/SKILL.md")
        for t in sorted(kaynak.glob("*.tsv")):
            z.write(t, f"awesome-rehber/references/{t.name}")
        assert len(z.namelist()) <= EN_COK_DOSYA, f"{len(z.namelist())} dosya > {EN_COK_DOSYA}"
    return cikti


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(paketle(KOK / "skills/awesome-rehber", KOK / "docs/kaynak/awesome", KOK / "dist/yukle-claude-ai/awesome-rehber.zip"))
