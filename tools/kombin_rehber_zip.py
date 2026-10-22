"""İKİ TARAF: kombin-rehber claude.ai paketi. tools/kombinler.json → references/kombinler.md (claude.ai'de yerel yol yok, içerik zip'te).
  python tools/kombin_rehber_zip.py   → dist/kombin-rehber.zip"""
import json
import sys
import zipfile
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]


def md():
    ks = json.loads((KOK / "tools/kombinler.json").read_text(encoding="utf-8"))["kombinler"]
    s = ["# Kombinler (tools/kombinler.json'dan üretilir)", ""]
    for tur in dict.fromkeys(k["tur"] for k in ks):
        s += [f"## {tur}", ""]
        for k in (k for k in ks if k["tur"] == tur):
            s.append(f"- **{k['id']}** · {k['amac']} · jeton: {k['jeton']}")
            s.append("  - " + " → ".join(f"{a} ({c})" for a, c in k["adimlar"]))
            s.append(f"  - neden: {k['neden']}")
        s.append("")
    return "\n".join(s)


def paketle(cikti):
    cikti.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(KOK / "skills/kombin-rehber/SKILL.md", "kombin-rehber/SKILL.md")
        z.writestr("kombin-rehber/references/kombinler.md", md())
    return cikti


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(paketle(KOK / "dist/kombin-rehber.zip"))
