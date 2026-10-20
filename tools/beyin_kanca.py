"""BEYIN-2 kanca: ajan-sira/*.json içinde kasada olmayan yeni biten oturum varsa beyin_al'ı koşar, yoksa hiçbir şey yapmaz.
mem_bekci.py zamanlanmış görevi (5 dk, pythonw) sonunda çağırır; model ve pencere yok, beyin_al sha ile idempotent."""
import json
import time
from pathlib import Path

import beyin_al

BEKLE = 30  # sn; yazılmakta olan dosyaya dokunma


def yeni(sira=None, durum_yol=None, simdi=None):
    sira = sira or beyin_al.KOK / ".kos/kopru/ajan-sira"
    durum_yol = durum_yol or beyin_al.KASA / ".beyin/durum.json"
    durum = json.loads(durum_yol.read_text(encoding="utf-8")) if durum_yol.exists() else {}
    simdi = simdi or time.time()
    out = []
    for p in sorted(Path(sira).glob("*.json")):
        if str(p) in durum or simdi - p.stat().st_mtime < BEKLE:
            continue
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except ValueError:  # boş/yarım dosya beyin_al'da da atlanır; her turda tetiklemesin
            continue
        out.append(p)
    return out


def main():
    n = len(yeni())
    if n:
        beyin_al.main([])
    return n


if __name__ == "__main__":
    main()
