"""KÜÇÜK-2 çağrı sayacı hook'u (proje .claude/settings.json).

SessionStart → .claude/cagri-sayac.txt = 0 (alt ajan: cagri-sayac-alt.txt = 0).
PostToolUse/PostToolUseFailure → +1; alt ajan içi çağrılar ana bütçeye (45)
girmez, cagri-sayac-alt.txt'de ayrı sayılır. Her 10'da modele "çağrı N/45 · alt M",
40'ta ve ≥45'te uyarı additionalContext. dalga.md'ye dokunmaz. CAGRI_SAYAC_DIZIN
verilirse sayaç dosyaları orada (test ortamı). Her hata sessizce geçer.
"""
import json
import os
import sys
from pathlib import Path

TAVAN = 45


def _oku(dosya):
    try:
        return int(dosya.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return 0


def main():
    try:
        olay = json.loads(sys.stdin.read() or "{}")
        dizin = Path(os.environ.get("CAGRI_SAYAC_DIZIN")
                     or Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".") / ".claude")
        sayac = dizin / "cagri-sayac.txt"
        alt = dizin / "cagri-sayac-alt.txt"
        ad = olay.get("hook_event_name")
        if ad == "SessionStart":
            sayac.write_text("0", encoding="utf-8")
            alt.write_text("0", encoding="utf-8")
            return
        if olay.get("agent_id"):
            alt.write_text(str(_oku(alt) + 1), encoding="utf-8")
            return
        n = _oku(sayac) + 1
        # ponytail: oku-yaz kilitsiz; paralel çağrılarda sayım kaybı kabul (KÜÇÜK-2)
        sayac.write_text(str(n), encoding="utf-8")
        if n == 40:
            mesaj = f"çağrı 40/{TAVAN}: yeni madde başlatma"
        elif n >= TAVAN:
            mesaj = f"çağrı {n}/{TAVAN}: commit + push ve DUR"
        elif n % 10 == 0:
            mesaj = f"çağrı {n}/{TAVAN} · alt {_oku(alt)}"
        else:
            return
        # ASCII JSON (\u kaçışlı): cp1252 konsolda print UnicodeEncodeError vermesin
        print(json.dumps({"hookSpecificOutput": {"hookEventName": ad, "additionalContext": mesaj}}))
    except Exception:
        pass


if __name__ == "__main__":
    main()
