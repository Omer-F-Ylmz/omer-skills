"""SLASH-ÖĞREN d2 adım 1: köprü argv'sinde Skill aracı kapalı/açık → gerçek API girdi token'ı. En fazla 4 `claude -p` (kapalı,açık × 2). Sonuç .kos/ogrenme/slash-olc.json."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(KOK / "tools"))
import cc_profil  # noqa: E402

BOS_MCP = ["--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}']


def argv(acik):
    a = cc_profil.kur("ajan")[0]
    if not acik:
        return ["--disable-slash-commands", *a, *BOS_MCP]
    return [("Skill," + x if i and a[i - 1] == "--tools" else x) for i, x in enumerate(a)] + BOS_MCP


def kos(ek):
    p = subprocess.run([shutil.which("claude"), "-p", "--output-format", "json", "--model", "sonnet", "--max-turns", "2", *ek],
                       input="Yalnız 'tamam' yaz.", capture_output=True, text=True, encoding="utf-8", cwd=str(KOK), timeout=300)
    u = json.loads(p.stdout)["usage"]
    return {"girdi": u["input_tokens"], "yaz": u.get("cache_creation_input_tokens", 0), "oku": u.get("cache_read_input_tokens", 0)}


if __name__ == "__main__":
    sonuc = []
    for acik in (False, True, False, True):
        r = kos(argv(acik))
        r["acik"] = acik
        r["toplam"] = r["girdi"] + r["yaz"] + r["oku"]
        sonuc.append(r)
        print(r, flush=True)
    kapali = [r["toplam"] for r in sonuc if not r["acik"]]
    acik = [r["toplam"] for r in sonuc if r["acik"]]
    fark = sum(acik) / 2 - sum(kapali) / 2
    print(f"ort kapalı {sum(kapali) / 2:.0f} · açık {sum(acik) / 2:.0f} · fark {fark:.0f} (%{100 * fark / (sum(kapali) / 2):.1f})")
    (KOK / ".kos" / "ogrenme" / "slash-olc.json").write_text(json.dumps(sonuc, indent=1), encoding="utf-8")
