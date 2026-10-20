"""RAM büyüme alarmı (bekçi çağırır, öldürmez): imza başına toplam MB, ≥ARALIK_DK önceki anlık görüntüden ≥ESIK_MB büyüdüyse
.kos/kopru/ram-buyume.log'a ve uyku-ozet.txt'e bir satır yazar. python tools/ram/buyume.py  |  python tools/ram/buyume.py --test
shortcut: uyku-ozet.txt makara_gece her gece yeniden yazar, satır o zamana dek kalır; imza = agac.imza ilk 60 karakter."""
import collections
import json
import os
import sys
import time

KOK = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DURUM = os.path.join(KOK, ".kos", "kopru", "ram-buyume.json")
LOG = os.path.join(KOK, ".kos", "kopru", "ram-buyume.log")
OZET = os.path.join(KOK, ".kos", "kopru", "uyku-ozet.txt")
ESIK_MB, ARALIK_DK = 150, 25


def buyuyenler(eski, yeni, esik=ESIK_MB):
    d = sorted(((yeni[k] - eski.get(k, 0), k) for k in yeni), reverse=True)
    return [(round(a), k) for a, k in d if a >= esik]


def anlik():
    import psutil
    sys.path.insert(0, os.path.dirname(__file__))
    from agac import SISTEM, imza
    t = collections.Counter()
    for p in psutil.process_iter():
        try:
            if not SISTEM.match(p.exe() or ""):
                t[imza(p)[:60]] += p.memory_info().rss / 2**20
        except psutil.Error:
            pass
    return {k: round(v) for k, v in t.items()}


def main():
    yeni, simdi = anlik(), time.time()
    try:
        d = json.load(open(DURUM, encoding="utf-8"))
    except (OSError, ValueError):
        d = None
    if d and simdi - d["ts"] < ARALIK_DK * 60:
        return
    if d:
        b = buyuyenler(d["mb"], yeni)
        if b:
            satir = f"{time.strftime('%Y-%m-%d %H:%M:%S')} RAM büyüme ({int((simdi - d['ts']) / 60)} dk): " + "; ".join(f"+{a} MB {k}" for a, k in b[:5])
            for yol in (LOG, OZET):  # bayt ekle: write_text CRLF'e çevirir
                with open(yol, "ab") as f:
                    f.write((satir + "\n").encode("utf-8"))
    json.dump({"ts": simdi, "mb": yeni}, open(DURUM, "w", encoding="utf-8"))


if __name__ == "__main__":
    if "--test" in sys.argv:
        assert buyuyenler({"a": 100, "b": 500}, {"a": 400, "b": 520, "c": 200}) == [(300, "a"), (200, "c")]
        assert buyuyenler({}, {}) == []
        print("ok")
    else:
        main()
