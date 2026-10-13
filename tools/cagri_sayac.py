"""KÜÇÜK-2 çağrı sayacı hook'u (proje .claude/settings.json).

SessionStart → .claude/cagri-sayac/<session_id>.txt = 0 (alt ajan: <session_id>-alt.txt = 0).
PostToolUse/PostToolUseFailure → +1; alt ajan içi çağrılar ana bütçeye (45)
girmez, <session_id>-alt.txt'de ayrı sayılır. Her 10'da modele "çağrı N/45 · alt M",
40'ta ve ≥45'te uyarı additionalContext. dalga.md'ye dokunmaz. CAGRI_SAYAC_DIZIN
verilirse sayaç dosyaları orada (test ortamı). Her hata sessizce geçer.
MÜKEMMEL-2d: startup/clear sıfırlar, compact/resume korur.
KANCA-SAYAÇ-1: sayaç session_id başına (eşzamanlı oturumlar ayrı); session_id yoksa
sayılmaz; SessionStart 24 saatten eski *.txt sayaçlarını siler; transcript'teki son ana
istek bağlamı ≥140k jeton ise de ≥45 ile aynı DUR iletisi (okunamazsa yalnız sayı).
"""
import json
import os
import re
import sys
import time
from pathlib import Path

TAVAN = 45
BAGLAM_TAVAN = 140_000
GUN = 24 * 3600


def _oku(dosya):
    try:
        return int(dosya.read_text(encoding="utf-8").strip())
    except (OSError, ValueError):
        return 0


def _baglam(yol):
    """Transcript'teki son ana (sidechain olmayan) isteğin bağlam jetonu; okunamazsa 0."""
    if not isinstance(yol, str):
        return 0  # open(int) bir dosya tanımlayıcısını açıp kapatır
    try:
        with open(yol, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - 512_000))  # yalnız kuyruk: transcript MB'larca olabilir
            satirlar = f.read().decode("utf-8", "ignore").splitlines()
    except (OSError, TypeError, ValueError):
        return 0
    for s in reversed(satirlar):
        try:
            d = json.loads(s)
            if d.get("type") == "assistant" and not d.get("isSidechain"):
                u = d["message"]["usage"]
                return (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
                        + u.get("cache_read_input_tokens", 0))
        except (ValueError, AttributeError, KeyError, TypeError):
            continue
    return 0


def main():
    try:
        olay = json.loads(sys.stdin.read() or "{}")
        sid = olay.get("session_id")
        if not isinstance(sid, str) or not re.fullmatch(r"[\w-]+", sid):
            return  # sid dosya adına girer: yol geçişi olmasın
        dizin = Path(os.environ.get("CAGRI_SAYAC_DIZIN")
                     or Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".") / ".claude") / "cagri-sayac"
        dizin.mkdir(exist_ok=True)
        sayac = dizin / f"{sid}.txt"
        alt = dizin / f"{sid}-alt.txt"
        ad = olay.get("hook_event_name")
        if ad == "SessionStart":
            esik = time.time() - GUN
            for p in dizin.glob("*.txt"):
                if p.stat().st_mtime < esik:
                    p.unlink(missing_ok=True)
            if olay.get("source") not in ("compact", "resume"):
                sayac.write_text("0", encoding="utf-8")
                alt.write_text("0", encoding="utf-8")
            return
        if olay.get("agent_id"):
            alt.write_text(str(_oku(alt) + 1), encoding="utf-8")
            return
        n = _oku(sayac) + 1
        # ponytail: oku-yaz kilitsiz; paralel çağrılarda sayım kaybı kabul (KÜÇÜK-2)
        sayac.write_text(str(n), encoding="utf-8")
        if n >= TAVAN or _baglam(olay.get("transcript_path")) >= BAGLAM_TAVAN:
            mesaj = f"çağrı {n}/{TAVAN}: commit + push ve DUR"
        elif n == 40:
            mesaj = f"çağrı 40/{TAVAN}: yeni madde başlatma"
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
