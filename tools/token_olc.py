"""TOKEN-0 K1: Claude Code oturum jsonl'lerinden ağırlıklı token ölçümü.

Birim: girdi×1 + cache okuma×0.1 + cache yazma (5m×1.25, 1h×2) + çıktı×5.
Çıktıda yalnız sayı ve ad bulunur; içerik metni asla yazılmaz.

Kullanım: python tools/token_olc.py olc [--gun 14] [--kok <projects>] [--cikti olcum/token-0.json]
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
ALANLAR = ("istek", *AGIRLIK, "agirlikli")
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


def tara(kok, gun=14, simdi=None, en_buyuk=20):
    sinir = (simdi or time.time()) - gun * 86400
    kok = Path(kok)
    r = {"pencere_gun": gun, "dosya": 0, "bozuk_satir": 0, "usage_eksik": 0, "kirilimsiz_cache": 0,
         "gorsel": 0, "gorsel_token": 0}
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
              "tur": 0, "son_ctx": 0, "agirlikli": 0, "gorsel": 0, "gorsel_token": 0}
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
                    p, a = parcala(u), agirlikli(u)
                    k = (o.get("cwd") or "?", kaynak(o, yol), ajan_turu(o, yol), m.get("model") or "?")
                    g = grup[k]
                    g["istek"] += 1
                    g["agirlikli"] += a
                    for alan, v in p.items():
                        g[alan] += v
                    if ts is not None:
                        gunluk[time.strftime("%Y-%m-%d", time.gmtime(ts))][k[1]] += a
                    ctx = p["girdi"] + p["cache_okuma"] + p["cache_5m"] + p["cache_1h"]
                    if ot["taban"] is None:
                        ot.update(taban=ctx, proje=k[0], kaynak=k[1], ajan=k[2], model=k[3])
                    ot["tur"] += 1
                    ot["son_ctx"] = ctx
                    ot["agirlikli"] += a
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
         f" · görsel {r['gorsel']} ({r['gorsel_token']} tok)",
         "", "kaynak · ajan | ağırlıklı M | pay | girdi · okuma · yazma5m · yazma1h · çıktı (ağırlıklı pay)"]
    for (k, a), v in _topla(r, lambda x: (x["kaynak"], x["ajan"])):
        sat = [x for x in r["satirlar"] if (x["kaynak"], x["ajan"]) == (k, a)]
        kat = " · ".join(f"%{100 * AGIRLIK[c] * sum(x[c] for x in sat) / (v or 1):.0f}" for c in AGIRLIK)
        s.append(f"{k} · {a} | {v / 1e6:.2f} | %{100 * v / top:.1f} | {kat}")
    s += ["", "model | ağırlıklı M | pay"]
    s += [f"{m} | {v / 1e6:.2f} | %{100 * v / top:.1f}" for m, v in _topla(r, lambda x: x["model"])]
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

    r = tara(deger("--kok", Path.home() / ".claude" / "projects"), int(deger("--gun", 14)))
    cikti = deger("--cikti", None)
    if cikti:
        Path(cikti).parent.mkdir(parents=True, exist_ok=True)
        Path(cikti).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(tablo(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
