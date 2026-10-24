"""İKİ TARAF: kombin-rehber claude.ai paketi. tools/kombinler.json → references/kombinler.md (claude.ai'de yerel yol yok, içerik zip'te).
  python tools/kombin_rehber_zip.py   → dist/kombin-rehber.zip"""
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arac_kart  # noqa: E402

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


def kart_md():
    """BEYIN-ARAC-KART-1: docs/arac-kart/kart.jsonl → references/arac-kartlari.md (claude.ai'de yerel yol yok; tür başlığı + ≤150 jeton kart satırı, yol/hash yok)."""
    ks = arac_kart._jsonl(KOK / "docs/arac-kart/kart.jsonl")
    s = ["# Araç kartları (docs/arac-kart/kart.jsonl'dan üretilir)", "", "Başlıkta ara, satırı oku; ayrıntı için aracın kendi SKILL.md'si.", ""]
    for tur in dict.fromkeys(k["tur"] for k in ks):
        s += [f"## {tur}", ""] + [f"- {arac_kart.kart_metni(k)}" for k in ks if k["tur"] == tur] + [""]
    return "\n".join(s)


def gecmis_md():
    kb = json.loads((KOK / "docs/arac-kart/kombin.json").read_text(encoding="utf-8"))
    return "\n".join(["# Geçmişte başarılı araç kümeleri (ajan işleri, KABUL × birlikte kullanım)", ""] + [f"- **{t}**: " + ", ".join(a) for t, a in kb.items()]) + "\n"


def paketle(cikti):
    cikti.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(cikti, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(KOK / "skills/kombin-rehber/SKILL.md", "kombin-rehber/SKILL.md")
        z.writestr("kombin-rehber/references/kombinler.md", md())
        z.writestr("kombin-rehber/references/arac-kartlari.md", kart_md())
        z.writestr("kombin-rehber/references/kombin-gecmis.md", gecmis_md())
    return cikti


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(paketle(KOK / "dist/kombin-rehber.zip"))
