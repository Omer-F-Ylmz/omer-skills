"""HER-ADIM-1 damıtıcı (model yok, 0 jeton): tools/adim_log.jsonl istatistik kalıpları + .kos/kopru/akis/kaliplar.jsonl
→ Obsidian 50-dersler/adim-kaliplari.md (üzerine yazar) + ruflo pattern-store (yalnız daha önce yazılmamış)."""
import hashlib
import json
import os
import sys
from collections import Counter
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
LOG = KOK / "tools" / "adim_log.jsonl"
KALIPLAR = KOK / ".kos/kopru/akis/kaliplar.jsonl"
YAZILAN = KOK / ".kos/kopru/akis/yazilan.txt"
VAULT = Path(os.environ.get("BEYIN_VAULT") or Path.home() / "Desktop/Obsidian") / "50-dersler" / "adim-kaliplari.md"


def jsonl(yol):
    if not yol.exists():
        return []
    out = []
    for s in yol.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(s))
        except ValueError:
            pass
    return out


def istatistik(adimlar):
    """Adım logundan kalıplar: yüksek hata oranlı araç · ardışık tekrar · pahalı araç."""
    k, say, hata, jeton = [], Counter(), Counter(), Counter()
    for a in adimlar:
        say[a["arac"]] += 1
        hata[a["arac"]] += a["sonuc"] == "hata"
        jeton[a["arac"]] += a.get("jeton") or 0
    for ad, n in say.items():
        if n >= 3 and hata[ad] / n >= 0.3:
            k.append({"kalip": f"{ad} adımı %{round(100 * hata[ad] / n)} hata veriyor ({hata[ad]}/{n}): çağırmadan önce girdiyi doğrula.", "kanit": "adim_log"})
    seri, onceki, boy = set(), None, 0
    for a in adimlar:
        boy = boy + 1 if a["arac"] == onceki else 1
        if boy == 5:
            seri.add(a["arac"])
        onceki = a["arac"]
    for ad in sorted(seri):
        k.append({"kalip": f"{ad} art arda ≥5 kez çağrıldı: tek toplu çağrı ya da betikle birleştir.", "kanit": "adim_log"})
    if say:
        ad, j = max(jeton.items(), key=lambda x: x[1] / say[x[0]])
        if j:
            k.append({"kalip": f"En pahalı adım türü {ad} (ort. {j // say[ad]} jeton bağlam): dilimle/alt ajana ver.", "kanit": "adim_log"})
    return k


def damit(ruflo=None, vault=VAULT, adimlar=None, kaliplar=None):
    kaliplar = jsonl(KALIPLAR) if kaliplar is None else kaliplar
    liste = istatistik(jsonl(LOG) if adimlar is None else adimlar) + [
        {"kalip": x["kalip"], "kanit": f"oturum {x.get('oturum', '?')[:8]} L{x.get('satir')}"} for x in kaliplar]
    vault.parent.mkdir(parents=True, exist_ok=True)
    vault.write_text("# Adım kalıpları (otomatik, adim_damit.py)\n\n" + "".join(f"- {x['kalip']} — {x['kanit']}\n" for x in liste), encoding="utf-8")
    yazilan = set(YAZILAN.read_text(encoding="utf-8").split()) if YAZILAN.exists() else set()
    yeni = [(hashlib.sha1(x["kalip"].encode("utf-8")).hexdigest()[:12], x["kalip"]) for x in liste]
    yeni = [(h, k) for h, k in yeni if h not in yazilan] if ruflo else []
    if yeni:
        o = ruflo([("tools/call", {"name": "agentdb_pattern-store", "arguments": {"pattern": k, "type": "is-akisi", "confidence": 0.7}}) for _, k in yeni])
        tamam = [h for i, (h, _) in enumerate(yeni) if "error" not in o[i + 2] and not o[i + 2].get("result", {}).get("isError")]
        YAZILAN.write_text(chr(10).join(sorted(yazilan | set(tamam))), encoding="utf-8")
        yeni = tamam
    return len(liste), len(yeni)


if __name__ == "__main__":
    sys.path[:0] = [str(KOK / "tools" / "ruflo")]
    import saglik  # noqa: F401  (CLAUDE_FLOW_MCP_TOOLS ayarı)
    import mcp_dene
    n, yeni = damit(lambda c: mcp_dene.kos(c)[0])
    print(f"kalıp={n} ruflo_yeni={yeni} not={VAULT}")
