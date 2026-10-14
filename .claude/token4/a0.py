"""TOKEN-4 A0: tasarruf araçları tablosu — bugünkü transkriptler + rtk gain/discover + headroom savings.
Kullanım: python .claude/token4/a0.py [YYYY-MM-DD] → docs/kutuphane/olcum/token-4-arac.tsv (+ stdout öz)."""
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
KOK = Path(__file__).resolve().parents[2]
PROJ = Path.home() / ".claude" / "projects"
GUN = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
CIKTI = KOK / "docs/kutuphane/olcum/token-4-arac.tsv"

# araç → (araç adı/komut kalıbı); Bash komutu ya da tool adı üstünde aranır
KALIP = {
    "rtk": r"^\s*rtk\b",
    "context-mode": r"mcp__plugin_context-mode",
    "cc-kopru oku": r"mcp__.*(cc-kopru|jev).*__(oku|ilgili|log|triage)|\bjev (ilgili|log|triage|oku)\b",
    "bekle.py": r"bekle\.py",
    "ucuz_alt/Gemini": r"ucuz_alt|ucuz-ajan|gemini",
    "Agent Reach": r"agent-reach|agent_reach",
    "qmd": r"\bqmd\b|mcp__.*qmd",
    "smart-explore": r"smart_(outline|search|unfold)|smart-explore",
    "mem-search": r"mem-search|get_observations|mcp__.*claude-mem.*search",
    "headroom retrieve": r"headroom_retrieve",
    "headroom-compress": r"headroom-compress",
    "strategic-compact": r"strategic-compact",
    "graphify": r"\bgraphify\b",
    "cc_profil": r"cc_profil",
}


def _json(argv):
    r = subprocess.run(argv, capture_output=True, encoding="utf-8", errors="replace")
    return json.loads(r.stdout)


def _sonuc_boy(c):
    if isinstance(c, str):
        return len(c)
    return sum(len(x.get("text", "")) for x in c if isinstance(x, dict)) if isinstance(c, list) else 0


def transkriptler():
    adim = durma = durma_girdi = 0
    kullanim, sonuc_kr = Counter(), Counter()
    mem_kr, mem_n = [], 0
    for j in PROJ.rglob("*.jsonl"):
        if date.fromtimestamp(j.stat().st_mtime).isoformat() < GUN:
            continue
        gorulen, bekleyen = set(), {}
        with j.open(encoding="utf-8", errors="replace") as f:
            for s in f:
                if GUN not in s[:400] and '"timestamp"' in s[:400]:
                    continue
                try:
                    o = json.loads(s)
                except ValueError:
                    continue
                if not str(o.get("timestamp", "")).startswith(GUN):
                    continue
                if "recent context, " in s and o.get("type") in ("attachment", "system", "user"):
                    m = re.search(r"recent context, .*?(?=\\n# |\"\})", s)
                    mem_kr.append(len(m.group(0)) if m else 0)
                m = o.get("message")
                if not isinstance(m, dict):
                    continue
                u = m.get("usage")
                if o.get("type") == "assistant" and isinstance(u, dict) and m.get("id") not in gorulen:
                    gorulen.add(m.get("id"))
                    adim += 1
                    if not u.get("cache_creation_input_tokens") and (u.get("input_tokens") or 0) >= 3000:
                        durma += 1
                        durma_girdi += u.get("input_tokens") or 0
                for b in m.get("content") or []:
                    if not isinstance(b, dict):
                        continue
                    if b.get("type") == "tool_use":
                        metin = b.get("name", "") + " " + json.dumps(b.get("input", {}), ensure_ascii=False)[:600]
                        for ad, k in KALIP.items():
                            if re.search(k, metin, re.I | re.M):
                                kullanim[ad] += 1
                                bekleyen[b.get("id")] = ad
                    elif b.get("type") == "tool_result" and b.get("tool_use_id") in bekleyen:
                        sonuc_kr[bekleyen.pop(b["tool_use_id"])] += _sonuc_boy(b.get("content"))
    return dict(adim=adim, durma=durma, durma_girdi=durma_girdi, kullanim=kullanim, sonuc_kr=sonuc_kr,
                mem_kr=mem_kr)


def main():
    t = transkriptler()
    gain = _json(["rtk", "gain", "-f", "json"])["summary"]
    disc = _json(["rtk", "discover", "-a", "-s", "1", "-f", "json"])
    hr = _json(["headroom", "savings", "--days", "1", "--json"])["windows"]["today"]
    kacak = sum(s["estimated_savings_tokens"] for s in disc["supported"])
    mem = t["mem_kr"]
    satir = [
        ("RTK", f"{gain.get('total_saved', '')} (tüm zaman)", f"{disc['already_rtk']}/{disc['total_commands']} Bash (1 gün)",
         "kayıpsız filtre", f"ort {gain.get('avg_time_ms', '')} ms",
         f"kaçak {sum(s['count'] for s in disc['supported'])} komut ≈{kacak} token; grep/read en düşük oran"),
        ("Headroom", f"{hr['tokens_saved']} ({hr['savings_percent']}%)", f"{hr['calls']} istek",
         "sıkıştırma; retrieve ile geri", "-",
         f"durma {t['durma']}/{t['adim']} adım ({100 * t['durma'] / max(t['adim'], 1):.1f}%) önbelleksiz {t['durma_girdi']} token"),
        ("claude-mem", "-", f"{len(mem)} enjeksiyon", "oturum başı bağlam",
         "-", f"blok medyan {sorted(mem)[len(mem) // 2] if mem else 0} kar.; dakika damgası msg1'de (istem sonrası)"),
    ]
    for ad in KALIP:
        if ad in ("rtk",):
            continue
        satir.append((ad, "-", f"{t['kullanim'][ad]} çağrı", "-", "-", f"dönüş {t['sonuc_kr'][ad]} kar."))
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    with CIKTI.open("w", encoding="utf-8", newline="\n") as f:
        f.write(f"# TOKEN-4 A0 {GUN} — araç\ttasarruf_token\tkullanım\tkalite\tsüre\tzayıf_nokta\n")
        for s in satir:
            f.write("\t".join(map(str, s)) + "\n")
    for s in satir:
        print(" | ".join(map(str, s)))


if __name__ == "__main__":
    main()
