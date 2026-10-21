"""Maliyet defteri (.kos/kopru/maliyet.tsv): her biten iş için zaman · ad · model · $ · tur · success.
Haftalık: son 7 günde Haiku'da başarısız olan iş türleri → ajan_sira bu türleri sonnet medium'dan başlatır."""
import re
import time
from pathlib import Path

DEFTER = Path(__file__).resolve().parent / "maliyet.tsv"
BASLIK = "zaman\tad\tmodel\tusd\ttur\tsuccess\n"


def tur(ad):
    """'token-2-d3' → 'token'."""
    m = re.match(r"[^\W\d_]+", ad)
    return m.group(0).lower() if m else ad


def yaz(ad, model, usd, ok, yol=None):
    yol = yol or DEFTER
    if not yol.exists():
        yol.write_text(BASLIK, encoding="utf-8")
    with yol.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{ad}\t{model}\t{usd:.2f}\t{tur(ad)}\t{int(ok)}\n")


def oku(yol=None):
    yol = yol or DEFTER
    if not yol.exists():
        return []
    rows = []
    for s in yol.read_text(encoding="utf-8").splitlines()[1:]:
        p = s.split("\t")
        if len(p) == 6:
            rows.append({"zaman": p[0], "ad": p[1], "model": p[2], "usd": float(p[3]), "tur": p[4], "ok": p[5] == "1"})
    return rows


def gunluk(rows, gun):
    """gun = 'YYYY-MM-DD' → (toplam $, en pahalı 3 iş)."""
    bugun = [r for r in rows if r["zaman"].startswith(gun)]
    return sum(r["usd"] for r in bugun), sorted(bugun, key=lambda r: -r["usd"])[:3]


def haiku_zayif(rows, simdi=None):
    """Son 7 günde Haiku'da başarısız kalan iş türleri (küme)."""
    simdi = time.time() if simdi is None else simdi
    sinir = time.strftime("%Y-%m-%d %H:%M", time.localtime(simdi - 7 * 86400))
    return {r["tur"] for r in rows if r["model"].startswith("haiku") and not r["ok"] and r["zaman"] >= sinir}
