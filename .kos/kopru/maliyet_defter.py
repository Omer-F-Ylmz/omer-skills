"""Maliyet defteri (.kos/kopru/maliyet.tsv): her biten iş için zaman · ad · model · $ · tur · success.
Haftalık: son 7 günde Haiku'da başarısız olan iş türleri → ajan_sira bu türleri sonnet medium'dan başlatır."""
import re
import time
from pathlib import Path

DEFTER = Path(__file__).resolve().parent / "maliyet.tsv"
BASLIK = "zaman\tad\tmodel\tusd\ttur\tsuccess\n"
BUTCE_DEFTER = Path(__file__).resolve().parent / "butce.tsv"  # BÜTÇE-KAPI-1: iş başına bütçe/harcanan/oran (maliyet.tsv'ye dokunmaz)
BUTCE_BASLIK = "zaman\tad\tbutce\tusd\toran\tdurum\n"


def tur(ad):
    """'token-2-d3' → 'token'."""
    m = re.match(r"[^\W\d_]+", ad)
    return m.group(0).lower() if m else ad


def yaz(ad, model, usd, ok, yol=None, kaynak=None, cache=None):
    """KONSOL-GECIS-1: kaynak (konsol) verilirse 7. sütun kaynak, 8. sütun cache isabeti (okunan/toplam girdi) eklenir; yoksa eski 6 sütun."""
    yol = yol or DEFTER
    if not yol.exists():
        yol.write_text(BASLIK, encoding="utf-8")
    ek = f"\t{kaynak}\t{cache or 0:.2f}" if kaynak else ""
    with yol.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{ad}\t{model}\t{usd:.2f}\t{tur(ad)}\t{int(ok)}{ek}\n")


def yaz_butce(ad, butce, usd, durum, yol=None):
    """BÜTÇE-KAPI-1: iş başına bütçe · harcanan · oran · sonuç alt türü (error_max_budget_usd = bütçe doldu)."""
    yol = yol or BUTCE_DEFTER
    if not yol.exists():
        yol.write_text(BUTCE_BASLIK, encoding="utf-8")
    with yol.open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M')}\t{ad}\t{butce:.2f}\t{usd:.2f}\t{usd / butce:.2f}\t{durum}\n")


def butce_asan(gun, yol=None):
    """gun = 'YYYY-MM-DD' → o gün bütçesi dolup durdurulan iş adları."""
    yol = yol or BUTCE_DEFTER
    if not yol.exists():
        return []
    return [p[1] for p in (s.split("\t") for s in yol.read_text(encoding="utf-8").splitlines()[1:])
            if len(p) == 6 and p[0].startswith(gun) and p[5] == "error_max_budget_usd"]


def oku(yol=None):
    yol = yol or DEFTER
    if not yol.exists():
        return []
    rows = []
    for s in yol.read_text(encoding="utf-8").splitlines()[1:]:
        p = s.split("\t")
        if len(p) in (6, 8):
            rows.append({"zaman": p[0], "ad": p[1], "model": p[2], "usd": float(p[3]), "tur": p[4], "ok": p[5] == "1",
                         "kaynak": p[6] if len(p) == 8 else "abonelik", "cache": float(p[7]) if len(p) == 8 else None})
    return rows


def konsol_harcama(rows, gun=None):
    """KONSOL-GECIS-1: Console (API) harcaması; gun = 'YYYY-MM-DD' → o gün, yoksa toplam."""
    return sum(r["usd"] for r in rows if r["kaynak"] == "konsol" and (gun is None or r["zaman"].startswith(gun)))


def gunluk(rows, gun):
    """gun = 'YYYY-MM-DD' → (toplam $, en pahalı 3 iş)."""
    bugun = [r for r in rows if r["zaman"].startswith(gun)]
    return sum(r["usd"] for r in bugun), sorted(bugun, key=lambda r: -r["usd"])[:3]


def ucretsiz_oran(rows, simdi=None):
    """UCRETSIZ-MOTOR-1: son 7 günde ücretsiz motorda tür → (başarılı, toplam)."""
    simdi = time.time() if simdi is None else simdi
    sinir = time.strftime("%Y-%m-%d %H:%M", time.localtime(simdi - 7 * 86400))
    oran = {}
    for r in rows:
        if r["model"].startswith("ucretsiz") and r["zaman"] >= sinir:
            ok, n = oran.get(r["tur"], (0, 0))
            oran[r["tur"]] = (ok + r["ok"], n + 1)
    return oran


def ucretsiz_zayif(rows, simdi=None):
    """Ücretsiz başarı oranı <%80 olan türler → ajan_sira bu türleri doğrudan haiku'dan başlatır (haftalık pencere)."""
    return {t for t, (ok, n) in ucretsiz_oran(rows, simdi).items() if ok / n < 0.8}


def haiku_zayif(rows, simdi=None):
    """Son 7 günde Haiku'da başarısız kalan iş türleri (küme)."""
    simdi = time.time() if simdi is None else simdi
    sinir = time.strftime("%Y-%m-%d %H:%M", time.localtime(simdi - 7 * 86400))
    return {r["tur"] for r in rows if r["model"].startswith("haiku") and not r["ok"] and r["zaman"] >= sinir}
