"""r5 onarımı: netlify-config "## Secrets Controller" orijinal metinle çekirdeğe (r4'te 2/3 görevde okundu), ref silinir;
create-design-md: r4'te 2/3 yanıt tek tek ad sayıp `--color-*` ailelerini yazmadı → Validate'e yanıt kuralı.
r4 sürümü .kalite3/pilot-r4/ yedeğinde."""
import re, shutil
from pathlib import Path

K = Path(__file__).resolve().parent


def bolum(metin, baslik):
    m = re.search(rf"^{re.escape(baslik)}\s*$.*?(?=^## |\Z)", metin, re.M | re.S)
    assert m, baslik
    return m


for ad in ("netlify-config", "create-design-md"):
    yedek = K / "pilot-r4" / ad
    if not yedek.exists():
        shutil.copytree(K / "pilot" / ad, yedek)

ad = "netlify-config"
orj = (K / "olc" / "once" / ad / ".claude" / "skills" / f"k3-{ad}" / "SKILL.md").read_text(encoding="utf-8")
p = K / "pilot" / ad / "SKILL.md"
s = p.read_text(encoding="utf-8")
m = bolum(s, "## Secrets Controller")
s = s[:m.start()] + bolum(orj, "## Secrets Controller").group(0) + s[m.end():]
assert "references/secrets-controller.md" not in s
p.write_text(s, encoding="utf-8", newline="\n")
(K / "pilot" / ad / "references" / "secrets-controller.md").unlink(missing_ok=True)
print(ad, len(orj), "→", len(s))

ad = "create-design-md"
p = K / "pilot" / ad / "SKILL.md"
s = p.read_text(encoding="utf-8")
eski = "If `typography` is populated but the export contains neither `--font-*` nor `--text-*`, the document is invalid and must be rewritten before reporting.\n"
yeni = eski + ("\nWhen you cannot run the export yourself, give the user these family checks verbatim (`--color-*`, `--font-*`, "
               "`--text-*`, `--radius-*`, `--spacing-*` for each populated category), not only individual token names.\n")
if yeni not in s:
    assert s.count(eski) == 1
    s = s.replace(eski, yeni)
p.write_text(s, encoding="utf-8", newline="\n")
print(ad, len(s))
