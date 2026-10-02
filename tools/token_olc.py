"""TOKEN-0 K1: Claude Code oturum jsonl'lerinden ağırlıklı token ölçümü.

Birim: girdi×1 + cache okuma×0.1 + cache yazma (5m×1.25, 1h×2) + çıktı×5.
TOKEN-1b: gerçek $ sütunu (FIYAT) · olcum/motor-usage.jsonl ayrı "motor" kaynak satırı.
Çıktıda yalnız sayı ve ad bulunur; içerik metni asla yazılmaz.

Kullanım: python tools/token_olc.py olc [--gun 14] [--kok <projects>] [--motor olcum/motor-usage.jsonl] [--cikti olcum/token-0.json]
"""
import base64
import heapq
import json
import struct
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

AGIRLIK = {"girdi": 1, "cache_okuma": 0.1, "cache_5m": 1.25, "cache_1h": 2, "cikti": 5}
ALANLAR = ("istek", *AGIRLIK, "agirlikli", "usd")
# $/MTok: girdi · cache okuma · yazma 5m · yazma 1h · çıktı. Kaynak: platform.claude.com/docs/en/about-claude/pricing
# "Model pricing" (2 Eki 2026). Opus 5.5 okuma 0.05× (dipnot 2); Sonnet 5 $2/$10 artık standart (dipnot 3).
FIYAT = {"opus-5-5": (4, 0.20, 5, 8, 20), "opus-5": (5, 0.50, 6.25, 10, 25), "sonnet-5-5": (2, 0.20, 2.50, 4, 10),
         "sonnet-5": (2, 0.20, 2.50, 4, 10), "haiku-4-5": (1, 0.10, 1.25, 2, 5)}
OBSERVER = "claude-mem-observer"
PNG = b"\x89PNG\r\n\x1a\n"


def parcala(u):
    cc = u.get("cache_creation")
    if cc:
        m5, h1 = cc.get("ephemeral_5m_input_tokens") or 0, cc.get("ephemeral_1h_input_tokens") or 0
    else:
        m5, h1 = u.get("cache_creation_input_tokens") or 0, 0  # kırılım yok → 5m
    return {"girdi": u.get("input_tokens") or 0, "cache_okuma": u.get("cache_read_input_tokens") or 0,
            "cache_5m": m5, "cache_1h": h1, "cikti": u.get("output_tokens") or 0}


def agirlikli(u):
    return sum(AGIRLIK[k] * v for k, v in parcala(u).items())


def usd(u, model):
    """Gerçek $ (FIYAT, en uzun model öneki); fiyatı bilinmeyen model (<synthetic> vb.) → None."""
    m = (model or "").removeprefix("claude-")
    k = max((x for x in FIYAT if m == x or m.startswith(x + "-")), key=len, default=None)
    return None if k is None else sum(f * v for f, v in zip(FIYAT[k], parcala(u).values())) / 1e6


def _ekle(r, g, u, model):
    a, d = agirlikli(u), usd(u, model)
    r["fiyatsiz_istek"] += d is None
    g["istek"] += 1
    g["agirlikli"] += a
    g["usd"] += d or 0
    for alan, v in parcala(u).items():
        g[alan] += v
    return a, d or 0


def ajan_turu(satir, yol):
    if satir.get("isSidechain") or satir.get("agentId") or "subagents" in Path(yol).parts:
        return "subagent"
    return "ana"


def kaynak(satir, yol):
    if any(OBSERVER in p for p in Path(yol).parts):
        return "observer"
    e = satir.get("entrypoint") or "cli"
    return {"cli": "etkilesimli", "sdk-cli": "claude-p"}.get(e, e)


def gorsel_token(src):
    try:
        b = base64.b64decode((src.get("data") or "")[:32])
        if b[:8] == PNG:
            w, h = struct.unpack(">II", b[16:24])
            olcek = min(1, 1568 / max(w, h), (1_150_000 / (w * h)) ** 0.5)
            return round(w * h * olcek * olcek / 750)
    except (ValueError, struct.error, ZeroDivisionError):
        pass
    return 1600  # ponytail: PNG dışı (JPEG vb.) üst sınırla sayılır; boyut ayrıştırma gerekirse eklenir


def zaman(ts):
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except (ValueError, AttributeError):
        return None


def tara(kok, gun=14, simdi=None, en_buyuk=20, motor=None):
    sinir = (simdi or time.time()) - gun * 86400
    kok = Path(kok)
    r = {"pencere_gun": gun, "dosya": 0, "bozuk_satir": 0, "usage_eksik": 0, "kirilimsiz_cache": 0,
         "gorsel": 0, "gorsel_token": 0, "fiyatsiz_istek": 0}
    grup = defaultdict(lambda: dict.fromkeys(ALANLAR, 0))
    gunluk = defaultdict(lambda: defaultdict(float))
    arac = defaultdict(lambda: {"adet": 0, "token": 0})
    ekler = defaultdict(lambda: {"adet": 0, "karakter": 0})
    sonuclar, oturumlar, gorulen = [], [], set()
    for yol in sorted(kok.rglob("*.jsonl")) if kok.is_dir() else []:
        if yol.stat().st_mtime < sinir:
            continue
        r["dosya"] += 1
        ad = str(yol.relative_to(kok))
        ot = {"oturum": ad, "proje": None, "kaynak": None, "ajan": None, "model": None, "taban": None,
              "tur": 0, "son_ctx": 0, "agirlikli": 0, "usd": 0, "gorsel": 0, "gorsel_token": 0}
        adlar = {}
        with yol.open(encoding="utf-8", errors="replace") as f:
            for s in f:
                try:
                    o = json.loads(s)
                except ValueError:
                    r["bozuk_satir"] += 1
                    continue
                if not isinstance(o, dict):
                    r["bozuk_satir"] += 1
                    continue
                ts = zaman(o.get("timestamp"))
                if ts is not None and ts < sinir:
                    continue
                m = o.get("message") if isinstance(o.get("message"), dict) else {}
                icerik = m.get("content") if isinstance(m.get("content"), list) else []
                tur = o.get("type")
                if tur == "assistant":
                    for b in icerik:
                        if isinstance(b, dict) and b.get("type") == "tool_use":
                            adlar[b.get("id")] = b.get("name")
                    u = m.get("usage")
                    if not u:
                        r["usage_eksik"] += 1
                        continue
                    if m.get("id") in gorulen:
                        continue
                    gorulen.add(m.get("id"))
                    if u.get("cache_creation_input_tokens") and not u.get("cache_creation"):
                        r["kirilimsiz_cache"] += 1
                    p = parcala(u)
                    k = (o.get("cwd") or "?", kaynak(o, yol), ajan_turu(o, yol), m.get("model") or "?")
                    a, d = _ekle(r, grup[k], u, k[3])
                    if ts is not None:
                        gunluk[time.strftime("%Y-%m-%d", time.gmtime(ts))][k[1]] += a
                    ctx = p["girdi"] + p["cache_okuma"] + p["cache_5m"] + p["cache_1h"]
                    if ot["taban"] is None:
                        ot.update(taban=ctx, proje=k[0], kaynak=k[1], ajan=k[2], model=k[3])
                    ot["tur"] += 1
                    ot["son_ctx"] = ctx
                    ot["agirlikli"] += a
                    ot["usd"] += d
                elif tur == "user":
                    for b in icerik:
                        if not isinstance(b, dict):
                            continue
                        parcalar = [b]
                        if b.get("type") == "tool_result":
                            c = b.get("content")
                            parcalar = c if isinstance(c, list) else [{"type": "text", "text": c or ""}]
                            n = round(sum(len(x.get("text") or "") for x in parcalar
                                          if isinstance(x, dict) and x.get("type") == "text") / 4)
                            isim = adlar.get(b.get("tool_use_id")) or "?"
                            arac[isim]["adet"] += 1
                            arac[isim]["token"] += n
                            sonuclar.append((n, isim, ad))
                        for x in parcalar:
                            if isinstance(x, dict) and x.get("type") == "image":
                                gt = gorsel_token(x.get("source") or {})
                                ot["gorsel"] += 1
                                ot["gorsel_token"] += gt
                elif tur == "attachment":
                    ek = o.get("attachment") if isinstance(o.get("attachment"), dict) else {}
                    e = ekler[ek.get("type") or "?"]
                    e["adet"] += 1
                    e["karakter"] += len(json.dumps(ek, ensure_ascii=False))
        r["gorsel"] += ot["gorsel"]
        r["gorsel_token"] += ot["gorsel_token"]
        if ot["tur"]:
            oturumlar.append(ot)
    # hafif.py motoru --no-session-persistence ile koşar → jsonl yok; usage sayıları ayrı dosyada
    for s in Path(motor).read_text(encoding="utf-8", errors="replace").splitlines() if motor and Path(motor).is_file() else []:
        try:
            o = json.loads(s)
        except ValueError:
            o = None
        if not isinstance(o, dict) or not isinstance(o.get("usage"), dict):
            r["bozuk_satir"] += 1
            continue
        if (o.get("ts") or 0) < sinir:
            continue
        k = ("motor", "motor", "ana", o.get("model") or "?")
        a, _ = _ekle(r, grup[k], o["usage"], k[3])
        gunluk[time.strftime("%Y-%m-%d", time.gmtime(o["ts"]))]["motor"] += a
    r["satirlar"] = sorted(({"proje": k[0], "kaynak": k[1], "ajan": k[2], "model": k[3], **v}
                            for k, v in grup.items()), key=lambda x: -x["agirlikli"])
    r["toplam"] = {k: sum(x[k] for x in r["satirlar"]) for k in ALANLAR}
    r["gunluk"] = {g: dict(v) for g, v in sorted(gunluk.items())}
    r["oturumlar"] = sorted(oturumlar, key=lambda x: -x["agirlikli"])
    r["en_buyuk_arac"] = [{"arac": i, "token": n, "oturum": o} for n, i, o in heapq.nlargest(en_buyuk, sonuclar)]
    r["araclar"] = dict(sorted(arac.items(), key=lambda kv: -kv[1]["token"]))
    r["ekler"] = dict(sorted(ekler.items(), key=lambda kv: -kv[1]["karakter"]))
    return r


def _topla(r, anahtar):
    d = defaultdict(float)
    for x in r["satirlar"]:
        d[anahtar(x)] += x["agirlikli"]
    return sorted(d.items(), key=lambda kv: -kv[1])


def tablo(r):
    t = r["toplam"]
    top = t["agirlikli"] or 1
    s = [f"{r['pencere_gun']} gün · {r['dosya']} dosya · {t['istek']} istek · ağırlıklı {t['agirlikli'] / 1e6:.2f} M"
         f" · bozuk {r['bozuk_satir']} · usage yok {r['usage_eksik']} · kırılımsız {r['kirilimsiz_cache']}"
         f" · görsel {r['gorsel']} ({r['gorsel_token']} tok) · $ {t['usd']:.2f} (fiyatsız istek {r['fiyatsiz_istek']})",
         "", "kaynak · ajan | ağırlıklı M | pay | $ | girdi · okuma · yazma5m · yazma1h · çıktı (ağırlıklı pay)"]
    for (k, a), v in _topla(r, lambda x: (x["kaynak"], x["ajan"])):
        sat = [x for x in r["satirlar"] if (x["kaynak"], x["ajan"]) == (k, a)]
        kat = " · ".join(f"%{100 * AGIRLIK[c] * sum(x[c] for x in sat) / (v or 1):.0f}" for c in AGIRLIK)
        s.append(f"{k} · {a} | {v / 1e6:.2f} | %{100 * v / top:.1f} | {sum(x['usd'] for x in sat):.2f} | {kat}")
    s += ["", "model | ağırlıklı M | pay | $"]
    s += [f"{m} | {v / 1e6:.2f} | %{100 * v / top:.1f} | {sum(x['usd'] for x in r['satirlar'] if x['model'] == m):.2f}"
          for m, v in _topla(r, lambda x: x["model"])]
    s += ["", "proje (ilk 10) | ağırlıklı M | pay"]
    s += [f"{p} | {v / 1e6:.2f} | %{100 * v / top:.1f}" for p, v in _topla(r, lambda x: x["proje"])[:10]]
    s += ["", "araç (toplam sonuç token, ilk 10) | adet | token"]
    s += [f"{i} | {v['adet']} | {v['token']}" for i, v in list(r["araclar"].items())[:10]]
    s += ["", "ek türü (ilk 10) | adet | karakter"]
    s += [f"{i} | {v['adet']} | {v['karakter']}" for i, v in list(r["ekler"].items())[:10]]
    return "\n".join(s)


def main(a):
    if not a or a[0] != "olc":
        print(__doc__)
        return 2

    def deger(ad, vars):
        return a[a.index(ad) + 1] if ad in a else vars

    r = tara(deger("--kok", Path.home() / ".claude" / "projects"), int(deger("--gun", 14)),
             motor=deger("--motor", Path(__file__).resolve().parents[1] / "olcum" / "motor-usage.jsonl"))
    cikti = deger("--cikti", None)
    if cikti:
        Path(cikti).parent.mkdir(parents=True, exist_ok=True)
        Path(cikti).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(tablo(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
