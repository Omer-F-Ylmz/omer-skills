"""TOKEN-6cR-H2: 6c-R recap testi (ttl_sim kırılma mantığı, k6cr yöntemi) + h2a_kayit ile kırılma sınıflaması. Salt okuma.
Sınıf: d TTL aşımı · a recap (away arada, Headroom öneki değişti) · b Headroom dönüşümü (CC öneki aynı, sıkıştırılmış önek değişti)
· c system/tools (sıkıştırılmış önek aynı, ara < TTL) · e sınıflanamayan (sebebiyle) · kayit_yok / bosluk ayrı.
Çalıştır: python tools/h2_sinif.py --pencere AD BAS BIT ... --h2a BAS BIT [--kayit-yok BAS BIT ...] [--cikti yol]
(zamanlar yerel "YYYY-MM-DD HH:MM:SS", BIT "simdi" olabilir)"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import token_olc as T  # noqa: E402

HARIC = ("Kendi-oyun-modlarim",)
BANT = (240, 3600)
SINIF = ("a", "b", "c", "d", "e", "kayit_yok", "bosluk")
HEADROOM = ("read_maturation", "kompress_background")


def istekler(kok, gun=14, simdi=None, haric=HARIC):
    """etk·ana istekleri; kırılma b ve ek maliyet k6cr ile birebir. away = önceki istekten beri away_summary satırı."""
    sinir, r = (simdi or time.time()) - gun * 86400, []
    for yol in sorted(Path(kok).rglob("*.jsonl")):
        if yol.stat().st_mtime < sinir or any(h in str(yol) for h in haric):
            continue
        onceki, gonder, olay, aw, gorulen = None, None, False, False, set()
        with yol.open(encoding="utf-8", errors="replace") as f:
            for s in f:
                try:
                    o = json.loads(s)
                except ValueError:
                    continue
                if not isinstance(o, dict):
                    continue
                ts, tur, ek = T.zaman(o.get("timestamp")), o.get("type"), o.get("attachment")
                if ts is not None and ts < sinir:
                    continue
                if tur == "user" and ts is not None:
                    gonder = ts
                elif tur == "system" and o.get("subtype") == "compact_boundary":
                    olay = True
                m = o.get("message") if isinstance(o.get("message"), dict) else {}
                u = m.get("usage") if tur == "assistant" else None
                if not isinstance(u, dict) or m.get("id") in gorulen:
                    if tur != "assistant" and "away_summary" in (o.get("subtype"), ek.get("type") if isinstance(ek, dict) else None):
                        aw = True
                    continue
                if T.kaynak(o, yol) != "etkilesimli" or T.ajan_turu(o, yol) != "ana":
                    break
                gorulen.add(m.get("id"))
                p = T.parcala(u)
                yazma, an, me = p["cache_5m"] + p["cache_1h"], gonder if gonder is not None else ts, (m.get("model"), o.get("effort"))
                ara = an - onceki["an"] if onceki and an is not None and onceki["an"] is not None else None
                b = min(yazma, max(0, onceki["onbellek"] - p["cache_okuma"])) if onceki else 0
                x = {"oturum": yol.stem, "an": an, "ts": ts, "ara": ara, "b": b, "away": aw, "cr": p["cache_okuma"], "cw": yazma,
                     "ttl": None, "olay": False, "onceki": None, "ek_w": 0, "ek_usd": 0}
                if onceki:
                    f_ = T.FIYAT.get(max((k for k in T.FIYAT if (m.get("model") or "").removeprefix("claude-").startswith(k)),
                                         key=len, default="opus-5-5"))
                    wy, py = (T.AGIRLIK["cache_1h"], f_[3]) if onceki["ttl"] == 3600 else (T.AGIRLIK["cache_5m"], f_[2])
                    x.update(ttl=onceki["ttl"], olay=olay or me != onceki["me"], onceki=(onceki["cr"], onceki["cw"], onceki["ts"]),
                             ek_w=b * (wy - T.AGIRLIK["cache_okuma"]), ek_usd=b * (py - f_[1]) / 1e6)
                r.append(x)
                ttl = 3600 if p["cache_1h"] else 300 if p["cache_5m"] else onceki["ttl"] if onceki else 3600
                onceki = {"an": an, "onbellek": p["cache_okuma"] + yazma, "ttl": ttl, "me": me, "cr": x["cr"], "cw": yazma, "ts": ts}
                olay, aw = False, False
    return r


def _grup(x):
    return {"n": len(x), "kirik": sum(1 for c in x if c["b"]), "oran_%": round(100 * sum(1 for c in x if c["b"]) / len(x), 1) if x else None,
            "token": sum(c["b"] for c in x), "ek_w": sum(c["ek_w"] for c in x), "ek_usd": round(sum(c["ek_usd"] for c in x), 2)}


def recap(ist, bas, bit):
    p = [c for c in ist if c["an"] is not None and bas <= c["an"] < bit]
    cift = [c for c in p if c["ara"] is not None]
    bant = [c for c in cift if BANT[0] <= c["ara"] < BANT[1]]
    return {"oturum": len({c["oturum"] for c in p}), "istek": len(p), "tum_ciftler": _grup(cift),
            "away_var": _grup([c for c in bant if c["away"]]), "away_yok": _grup([c for c in bant if not c["away"]])}


def h2a_oku(yol):
    kayit, bosluk, gorulen = [], [], set()
    for s in Path(yol).read_text(encoding="utf-8").splitlines():
        o = json.loads(s)
        if "bosluk" in o:
            bosluk.append(time.mktime(time.strptime(o["bosluk"], "%Y-%m-%dT%H:%M:%S")))
        elif "request_id" in o and o["request_id"] not in gorulen:
            gorulen.add(o["request_id"])
            kayit.append(o)
    return kayit, bosluk


def _fark(a, b):
    """a'nın b'de bozulduğu ilk indeks; a b'nin öneki ise len(a)."""
    return next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))


def sinifla(ist, kayit, bosluk, kayit_yok, bas, bit, tolerans=120):
    idx = {}
    for k in kayit:
        idx.setdefault((k["cache_read_tokens"], k["cache_write_tokens"]), []).append((T.zaman(k["ts"]), k))

    def bul(cr, cw, ts):
        a = [(abs(t - ts), k) for t, k in idx.get((cr, cw), []) if t is not None and ts is not None and abs(t - ts) <= tolerans]
        return min(a, key=lambda x: x[0])[1] if a else None

    s = {k: [] for k in SINIF}
    sebep, etiket = Counter(), 0
    for c in ist:
        if not c["b"] or c["an"] is None or not bas <= c["an"] < bit:
            continue
        h, hp = bul(c["cr"], c["cw"], c["ts"]), bul(*c["onceki"])
        if h is None and any(a <= c["ts"] < z for a, z in kayit_yok):
            k = "kayit_yok"
        elif h is None and any(t - 120 < c["ts"] <= t for t in bosluk):  # ponytail: bosluk satırı önceki ~2 yoklamayı kapsar sayılır
            k = "bosluk"
        elif c["ara"] is not None and c["ara"] >= c["ttl"]:
            k = "d"
        elif c["olay"]:
            k, _ = "e", sebep.update(["oturum_eylemi"])
        elif h is None or hp is None:
            k, _ = "e", sebep.update(["eslesmedi"])
        elif not hp["compressed_messages"] or not h["compressed_messages"]:
            k, _ = "e", sebep.update(["mesaj_yok"])
        elif (ic := _fark(hp["compressed_messages"], h["compressed_messages"])) == len(hp["compressed_messages"]):
            k = "c"
        elif ic < _fark(hp["request_messages"], h["request_messages"]):  # CC öneki sonda kayar (cache_control); Headroom daha önce bozduysa onundur
            k = "a" if c["away"] else "b"
            etiket += k == "b" and any(x in str(h["transforms_applied"]) for x in HEADROOM)
        else:
            k, _ = "e", sebep.update(["cc_onek"])
        s[k].append(c)
    return {"sinif": {k: {"adet": len(v), "token": sum(c["b"] for c in v), "ek_w": sum(c["ek_w"] for c in v),
                          "ek_usd": round(sum(c["ek_usd"] for c in v), 2)} for k, v in s.items()},
            "e_sebep": dict(sebep), "sicak_headroom_etiketli": etiket}


def main(a):
    yerel = lambda x: time.time() if x == "simdi" else time.mktime(time.strptime(x, "%Y-%m-%d %H:%M:%S"))  # noqa: E731
    ciftler = lambda ad: [(a[i + 1], yerel(a[i + 2]), yerel(a[i + 3])) if ad == "--pencere" else (yerel(a[i + 1]), yerel(a[i + 2]))  # noqa: E731
                          for i, x in enumerate(a) if x == ad]
    if "--pencere" not in a:
        print(__doc__)
        return 2
    ist = istekler(Path.home() / ".claude" / "projects")
    r = {"pencere": {ad: recap(ist, b, z) for ad, b, z in ciftler("--pencere")}}
    if "--h2a" in a:
        (b, z), = ciftler("--h2a")
        r["h2a"] = sinifla(ist, *h2a_oku(Path.home() / ".headroom" / "h2a_kayit.jsonl"), ciftler("--kayit-yok"), b, z)
    if "--cikti" in a:
        Path(a[a.index("--cikti") + 1]).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
