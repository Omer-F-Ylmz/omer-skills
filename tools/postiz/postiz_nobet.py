"""Postiz nöbetçisi (15 dk'da bir, modelsiz): zamanlanmış paylaşım penceresinde Postiz'i açar, pencere dışında ve son açılıştan 30 dk sonra kapatır."""
import datetime as dt, json, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import postiz_ac as P

SOSYAL = Path(r"C:\Users\pc\Desktop\Claude ile yapılanlar\sosyal-oto")
LOG = Path(__file__).resolve().parent / "nobet.log"
ONCE, SONRA = dt.timedelta(minutes=20), dt.timedelta(minutes=40)


def pencerede(simdi):
    for f in SOSYAL.rglob("POSTIZ-KUYRUK.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
            if d.get("mod") != "zamanla":
                continue
            t = dt.datetime.fromisoformat(d["tarih"])
            t = t if t.tzinfo else t.astimezone()
            if t - ONCE <= simdi <= t + SONRA:
                return f.parent.name
        except Exception:
            continue
    return None


def main():
    simdi = dt.datetime.now().astimezone()
    p = pencerede(simdi)
    try:
        son = float(P.DAMGA.read_text(encoding="utf-8"))
    except Exception:
        son = 0
    if p:
        sonuc = f"ac ({p}) {P.ac()}"
    elif time.time() - son > 1800 and P.ubuntu_calisiyor() and P.ayakta():
        sonuc = f"kapat {P.kapat()}"
    else:
        return
    LOG.open("a", encoding="utf-8").write(f"{simdi:%F %T} {sonuc}\n")


main()
