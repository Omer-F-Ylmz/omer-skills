"""ORDU-1 d11 (b): önsözlü köprü oturumlarında alt ajan kullanımını transkriptten say.
Kullanım: python tools/olcum/ordu_onsoz_tara.py [gün_sayısı]  -> iş başına: önsöz var mı, önsöz konumu/uzunluk, araç sayıları."""
import json, re, sys, time
from pathlib import Path

DIZIN = Path.home() / ".claude/projects/C--Projeler-omer-skills"
ONSOZ = "ORDU-1 derleyici"


def tara(yol):
    ilk, araclar, ucuz = None, {}, 0
    for s in yol.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(s)
        except ValueError:
            continue
        m = o.get("message") or {}
        c = m.get("content")
        if ilk is None and o.get("type") == "user":
            ilk = c if isinstance(c, str) else " ".join(b.get("text", "") for b in c if isinstance(b, dict))
        if o.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if b.get("type") == "tool_use":
                    araclar[b["name"]] = araclar.get(b["name"], 0) + 1
                    if b["name"] == "Bash" and re.search(r"python\S* \S*ucuz_alt\.py", b["input"].get("command", "")):
                        ucuz += 1
    return ilk or "", araclar, ucuz


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    gun = float(sys.argv[1]) if len(sys.argv) > 1 else 1
    esik = time.time() - gun * 86400
    for y in sorted(DIZIN.glob("*.jsonl"), key=lambda p: p.stat().st_mtime):
        if y.stat().st_mtime < esik:
            continue
        ilk, ar, ucuz = tara(y)
        if ONSOZ not in ilk:
            continue
        print(y.name[:8], "önsöz@", ilk.find(ONSOZ), "istem", len(ilk), "Agent", ar.get("Agent", 0) + ar.get("Task", 0),
              "ucuz_alt", ucuz, "araç", sum(ar.values()), ilk[ilk.find("[bütçe]") - 0 : 0].replace("\n", " "))


if __name__ == "__main__":
    main()
