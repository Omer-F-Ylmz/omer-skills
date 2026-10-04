"""KÜÇÜK-2 çağrı sayacı hook'u (proje .claude/settings.json).

SessionStart → .claude/cagri-sayac.txt = 0. PostToolUse/PostToolUseFailure → +1
(alt ajan içi çağrılar sayılmaz); her 10'da .claude/dalga.md ilk satırı
"çağrı N/45"; 40'ta ve ≥45'te modele additionalContext. Her hata sessizce geçer.
"""
import json
import os
import sys
from pathlib import Path

TAVAN = 45


def main():
    try:
        olay = json.loads(sys.stdin.read() or "{}")
        claude = Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".") / ".claude"
        sayac = claude / "cagri-sayac.txt"
        ad = olay.get("hook_event_name")
        if ad == "SessionStart":
            sayac.write_text("0", encoding="utf-8")
            return
        if olay.get("agent_id"):
            return
        try:
            n = int(sayac.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            n = 0
        n += 1
        # ponytail: oku-yaz kilitsiz; paralel çağrılarda sayım kaybı kabul (KÜÇÜK-2)
        sayac.write_text(str(n), encoding="utf-8")
        if n % 10 == 0:
            dalga = claude / "dalga.md"
            if dalga.exists():
                metin = dalga.read_bytes().decode("utf-8")
                ilk, _, kalan = metin.partition("\n")
                son = "\r\n" if ilk.endswith("\r") else "\n"
                if ilk.startswith("çağrı "):
                    metin = kalan
                dalga.write_bytes(f"çağrı {n}/{TAVAN}{son}{metin}".encode("utf-8"))
        if n == 40:
            mesaj = f"çağrı 40/{TAVAN}: yeni madde başlatma"
        elif n >= TAVAN:
            mesaj = f"çağrı {n}/{TAVAN}: commit + push ve DUR"
        else:
            return
        # ASCII JSON (\u kaçışlı): cp1252 konsolda print UnicodeEncodeError vermesin
        print(json.dumps({"hookSpecificOutput": {"hookEventName": ad, "additionalContext": mesaj}}))
    except Exception:
        pass


if __name__ == "__main__":
    main()
