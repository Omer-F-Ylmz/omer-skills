"""ORDU-1 d12: 18:55 öncesi/sonrası köprü oturumları — delegasyon, ağırlıklı token, tahmini $.
Kullanım: python tools/olcum/ordu_d12_olc.py [kesim_HH:MM] [gün]"""
import json, sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ordu_onsoz_tara import DIZIN, ONSOZ, tara

# $/Mtok: girdi, çıktı, önbellek-okuma, önbellek-yazma
FIYAT = {"haiku": (1, 5, 0.1, 1.25), "sonnet": (3, 15, 0.3, 3.75), "opus": (5, 25, 0.5, 6.25)}


def maliyet(yol):
    agirlikli, usd, ilk_ts = 0.0, 0.0, None
    gorulen = set()
    for s in yol.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            o = json.loads(s)
        except ValueError:
            continue
        if ilk_ts is None and o.get("timestamp"):
            ilk_ts = datetime.fromisoformat(o["timestamp"].replace("Z", "+00:00")).astimezone()
        m = o.get("message") or {}
        u = m.get("usage")
        if o.get("type") != "assistant" or not u or m.get("id") in gorulen:
            continue
        gorulen.add(m.get("id"))
        f = next((v for k, v in FIYAT.items() if k in str(m.get("model", ""))), FIYAT["sonnet"])
        g, c, cr, cw = (u.get("input_tokens", 0), u.get("output_tokens", 0),
                        u.get("cache_read_input_tokens", 0), u.get("cache_creation_input_tokens", 0))
        usd += (g * f[0] + c * f[1] + cr * f[2] + cw * f[3]) / 1e6
        agirlikli += g + 5 * c + 0.1 * cr + 1.25 * cw
    return ilk_ts, agirlikli, usd


def ozet(ad, r):
    if not r:
        print(ad, "n=0")
        return
    n = len(r)
    d = sum(1 for x in r if x["del"] > 0)
    print(f"{ad} n={n} delegasyonlu={d} ({100*d/n:.0f}%) ort$={sum(x['usd'] for x in r)/n:.2f} "
          f"ort_agirlikli_tok={sum(x['tok'] for x in r)/n/1e3:.0f}k ort_arac={sum(x['arac'] for x in r)/n:.0f}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    hh, mm = (sys.argv[1] if len(sys.argv) > 1 else "18:55").split(":")
    gun = float(sys.argv[2]) if len(sys.argv) > 2 else 2
    simdi = datetime.now().astimezone()
    kesim = simdi.replace(hour=int(hh), minute=int(mm), second=0, microsecond=0)
    esik = simdi - timedelta(days=gun)
    once, sonra = [], []
    for y in sorted(DIZIN.glob("*.jsonl"), key=lambda p: p.stat().st_mtime):
        if datetime.fromtimestamp(y.stat().st_mtime).astimezone() < esik:
            continue
        ilk, ar, ucuz = tara(y)
        if ONSOZ not in ilk:
            continue
        ts, tok, usd = maliyet(y)
        if ts is None:
            continue
        yeni = "ucuz_alt.py --tur ozet" in ilk
        r = {"id": y.name[:8], "ts": ts, "del": ar.get("Agent", 0) + ar.get("Task", 0) + ucuz,
             "tok": tok, "usd": usd, "arac": sum(ar.values()), "yeni": yeni}
        (sonra if ts >= kesim and yeni else once).append(r)
    once = once[-5:] if len(once) > 5 else once
    ozet("ONCE(son5)", once)
    ozet("SONRA", sonra)
    for r in sonra:
        print(" ", r["id"], r["ts"].strftime("%H:%M"), "del", r["del"], f"${r['usd']:.2f}", f"{r['tok']/1e3:.0f}k")


if __name__ == "__main__":
    main()
