"""İKİ TARAF: /ajan-getir claude.ai paketi. Katalogdaki yerel `yol` dosyaları zip içine references/ajanlar/ altına gömülür,
katalog yolu skill klasörüne göreli yazılır (claude.ai'de ~/.claude yok).
  python tools/ajan_getir_zip.py   → dist/kalite-3/ajan-getir.zip"""
import re
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def paketle(skill, cikti):
    satirlar = skill.joinpath("katalog.tsv").read_text(encoding="utf-8").splitlines()
    cikti.parent.mkdir(parents=True, exist_ok=True)
    yeni, gorulen = [satirlar[0]], set()
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(skill / "SKILL.md", "ajan-getir/SKILL.md")
        for s in satirlar[1:]:
            ad, model, tek, yol = s.split("\t")
            goreli = f"references/ajanlar/{re.sub(r'[^a-z0-9._-]+', '-', ad.lower()).strip('-')}.md"
            assert goreli not in gorulen, f"ad çakışması: {goreli}"
            gorulen.add(goreli)
            z.writestr(f"ajan-getir/{goreli}", Path(yol).read_bytes())
            yeni.append("\t".join((ad, model, tek, goreli)))
        z.writestr("ajan-getir/katalog.tsv", "\n".join(yeni) + "\n")
    return cikti


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(paketle(KOK / "skills/ajan-getir", KOK / "dist/kalite-3/ajan-getir.zip"))
