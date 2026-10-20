"""SLASH-ÖĞREN adım 1: alt ajan / köprü oturumu skill+komut görüyor mu? 3 `claude -p` (plan, ücretsiz). Sonuç .kos/ogrenme/slash-deneme.json."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import cc_profil  # noqa: E402

CLAUDE = shutil.which("claude")
SKILL = "brand-guidelines"
BOS_MCP = ["--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']

ALT = (f"Agent aracıyla bir general-purpose alt ajan aç. Alt ajan: (a) Skill aracıyla '{SKILL}' skill'ini çağırsın; "
       "Skill aracı yoksa 'SKILL-ARACI-YOK' yazsın; çağırabildiyse yüklenen metnin ilk satırını alıntılasın. "
       "(b) Read ile şu .md'yi okuyup ilk başlık satırını alıntılasın: {md}. (c) kendi araç adlarının listesini versin. "
       "Alt ajanın yanıtını AYNEN ver; sen ayrıca kendi araç listende 'Skill' var mı yaz.")
ANA = (f"Kendi araç listende 'Skill' aracı var mı? Varsa '{SKILL}' skill'ini çağır ve yüklenen metnin ilk satırını alıntıla; "
       "yoksa 'SKILL-ARACI-YOK' yaz. Sonra Agent aracıyla general-purpose alt ajan aç, aynı şeyi o da denesin ve araç adlarını listelesin. "
       "Hepsini ≤8 satırda ver.")


def kos(ad, argv, istem):
    p = subprocess.run([CLAUDE, "-p", "--output-format", "json", "--model", "sonnet", "--max-turns", "10", *argv],
                       input=istem, capture_output=True, text=True, encoding="utf-8", cwd=str(KOK), timeout=900)
    try:
        j = json.loads(p.stdout)
        return {"ad": ad, "yanit": j.get("result"), "tur": j.get("num_turns"), "ret": j.get("permission_denials"), "maliyet": j.get("total_cost_usd")}
    except ValueError:
        return {"ad": ad, "hata": (p.stdout + p.stderr)[-600:]}


if __name__ == "__main__":
    md = next(Path.home().joinpath(".claude", "plugins", "cache").rglob("commands/*.md"))
    ajan = cc_profil.kur("ajan")[0]
    # T3: köprü profili, --disable-slash-commands yok, --tools'a Skill eklenmiş
    ajan_skill = [("Skill," + a if i and ajan[i - 1] == "--tools" else a) for i, a in enumerate(ajan)]
    sonuc = [
        kos("T1 normal CC + alt ajan", BOS_MCP, ALT.format(md=md)),
        kos("T2 köprü argv (disable-slash + tools listesi)", ["--disable-slash-commands", *ajan, *BOS_MCP], ANA),
        kos("T3 köprü + Skill aracı, disable-slash yok", [*ajan_skill, *BOS_MCP], ANA),
    ]
    out = KOK / ".kos" / "ogrenme" / "slash-deneme.json"
    out.write_text(json.dumps({"md": str(md), "sonuc": sonuc}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(sonuc, ensure_ascii=False, indent=1)[:4000])
