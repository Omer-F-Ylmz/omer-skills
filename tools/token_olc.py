"""TOKEN-0 K1: Claude Code oturum jsonl'lerinden ağırlıklı token ölçümü.

Birim: girdi×1 + cache okuma×0.1 + cache yazma (5m×1.25, 1h×2) + çıktı×5.
TOKEN-1b: gerçek $ sütunu (FIYAT) · olcum/motor-usage.jsonl ayrı "motor" kaynak satırı.
Çıktıda yalnız sayı ve ad bulunur; içerik metni asla yazılmaz.

TOKEN-4a: --arac-dokum araç sonucu dökümü (Read/Bash/headroom_retrieve/tur/arşiv/L14; Headroom katsayısıyla düzeltilmiş katkı).

Kullanım: python tools/token_olc.py olc [--gun 14] [--kok <projects>] [--motor olcum/motor-usage.jsonl] [--cikti olcum/token-0.json]
          python tools/token_olc.py olc --arac-dokum [--gun 14] [--kok <projects>] [--arsiv .claude/dalga-arsiv] [--cikti olcum/token-4a.json]
"""
import base64
import heapq
import json
import math
import re
import statistics
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
SIKISTIR = "Condense the tool payload"  # TOKEN-2: claude-mem tek atımlık compress isteği (tools/cmem_yama.py)
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
    son_sik = (0, 0)
    for yol in sorted(kok.rglob("*.jsonl")) if kok.is_dir() else []:
        if yol.stat().st_mtime < sinir:
            continue
        r["dosya"] += 1
        ad = str(yol.relative_to(kok))
        ot = {"oturum": ad, "proje": None, "kaynak": None, "ajan": None, "model": None, "taban": None,
              "tur": 0, "son_ctx": 0, "agirlikli": 0, "usd": 0, "gorsel": 0, "gorsel_token": 0, "cikti": 0}
        adlar, sik = {}, False
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
                    if sik and ts is not None and ts >= son_sik[0]:
                        son_sik = (ts, p["cache_1h"])
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
                    ot["usd"], ot["cikti"] = ot["usd"] + d, ot["cikti"] + parcala(u)["cikti"]
                elif tur == "user":
                    c = m.get("content")
                    ilk = c if isinstance(c, str) else (icerik[0].get("text") or "") if icerik and isinstance(icerik[0], dict) else ""
                    sik = sik or ilk.startswith(SIKISTIR)
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
    r["compress_son_1h"] = son_sik[1]
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
    if r.get("compress_son_1h"):
        s.insert(0, "UYARI: cmem yaması yok → python tools/cmem_yama.py (son compress isteğinde 1h yazma)")
    return "\n".join(s)


REHBER = re.compile(r"(^|/)(skills|references)/")  # SINIR (Blender dersi): rehber okuması kısıtlanmaz, ayrı sayılır
ALT_KOMUT = {"git", "gh", "npm", "npx", "uv", "uvx", "dotnet", "graphify", "jev", "docker", "claude", "pip",
             "gitleaks", "cargo", "video", "winget"}
DEGISTIREN = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
KUCUK = 2000  # "küçük" tek Read (token)
# ponytail: dalga = istemin ilk 300 karakterindeki kimlik (TOKEN-4a, KALAN-7); kimliksiz dalga sınırı görülmez
DALGA = re.compile(r"\b(?!UTF-|SHA-|ISO-)[A-Z][A-Z0-9]{2,}-\d+[a-z]?(?:-\d+)?\b")
TUR_KALIP = (re.compile(r"(?i)tur\s*(\d+)\s*/\s*(\d+)"), re.compile(r"(?i)tur tavan\w*\s*\(~?(\d+)\s*>\s*(\d+)\)"))
SATIR_ARALIK = ((0, 100), (100, 300), (300, 500), (500, 1000), (1000, 2000), (2000, None))
ESIKLER = (300, 500, 1000, 2000)


def aile(komut):
    """Bash komut ailesi: cd/set/export, VAR= ve rtk önekleri atlanır; ilk kelime + (python -m modül · betik · alt komut)."""
    for parca in re.split(r"&&|\|\||;|\n", komut or ""):
        w = parca.split()
        while w and "=" in w[0]:
            w.pop(0)
        if w[:1] == ["rtk"]:
            w = w[2:] if w[1:2] == ["proxy"] else w[1:]
        if not w or w[0] in ("cd", "set", "export"):
            continue
        ilk = Path(w[0].strip("\"'")).name.lower().removesuffix(".exe")
        if len(w) > 2 and w[1] == "-m":
            return f"{ilk} -m {w[2]}"
        if len(w) > 1 and re.search(r"\.(py|ps1|js|sh)$", w[1]):
            return f"{ilk} {Path(w[1].strip(chr(34) + chr(39))).name}"
        if len(w) > 1 and ilk in ALT_KOMUT and re.fullmatch(r"[a-z][\w-]*", w[1]):
            return f"{ilk} {w[1]}"
        return ilk
    return "?"


def _satir(toplam, yol):
    if isinstance(toplam, int):
        return toplam
    try:
        with open(yol, "rb") as g:
            return sum(1 for _ in g)
    except (OSError, ValueError):
        return None


def _sayac():
    return {"adet": 0, "token": 0, "katki": 0.0, "katki_duz": 0.0}


def _say(d, n, kt, kd):
    d["adet"] += 1
    d["token"] += n
    d["katki"] += kt
    d["katki_duz"] += kd


def _liste(d, anahtar):
    return sorted(({anahtar: a, **v} for a, v in d.items()), key=lambda x: -x["katki_duz"])


def dokum(kok, gun=14, simdi=None, arsiv=None):
    """TOKEN-4a K1 (--arac-dokum): araç sonucu dökümü. Çıktıda yalnız sayı, dosya yolu ve komut ailesi bulunur.

    katkı = n·(w + 0.1·(R−1)) — n sonuç token'ı (karakter/4), R sonucu taşıyan istek sayısı (compact sınırına dek),
    w yazma katsayısı (oturumda 1h baskınsa 2, değilse 1.25). Düzeltilmiş = katkı·k; k (oturum başına) = Σ(Δctx − çıktı)
    / Σ sonuç token'ı, yalnız arasına yalnız tool_result giren ardışık isteklerde ("temiz adım"): transcript Headroom
    öncesi boyutu, usage sonrasını tutar. Temiz adımı olmayan oturum genel k'yı (Σ/Σ) alır.
    """
    sinir = (simdi or time.time()) - gun * 86400
    kok = Path(kok)
    toplam, gorulen, dosya, kayit = 0.0, set(), 0, []
    oku = {**_sayac(), "aralikli": 0, "rehber": 0}
    uzanti, rv_oku = defaultdict(_sayac), defaultdict(_sayac)
    limitsiz, aralik_n = [], []  # limitsiz: (yol, satır, n, katkı, düz) — rehber dışı, aralıksız Read
    tekrar = defaultdict(lambda: {**_sayac(), "degismeden": 0, "degismeden_katki": 0.0, "degismeden_duz": 0.0,
                                  "ayni_aralik": 0, "ayni_katki": 0.0, "ayni_duz": 0.0})
    bash = defaultdict(lambda: {**_sayac(), "n": [], "nr": [], "ns": [], "rtk": 0, "rtksiz": 0.0, "rtksiz_duz": 0.0,
                                "pipe": 0, "tail": 0})
    rv = {"adet": 0, "onceki": defaultdict(int), "sn": [], "tur": []}
    tur = {"istek": 0, "aracli": 0, "paralel": 0, "arac_sayisi": defaultdict(int)}
    dizi_t = {"dizi": 0, "istek": 0, "kazanc": 0, "kazanc_agirlikli": 0.0}
    uzun = {"oturum": 0, "tek_dalga": 0, "cok_dalga": 0, "bolme_tasarruf": 0.0}
    for yol in sorted(kok.rglob("*.jsonl")) if kok.is_dir() else []:
        if yol.stat().st_mtime < sinir:
            continue
        dosya += 1
        istek, mid_idx, araclar, sonuc, rtkler, dalgalar, adim = [], {}, [], {}, set(), [], []
        sg, dalga, m5, h1, gap_n, kirli = 0, None, 0, 0, 0, False
        with yol.open(encoding="utf-8", errors="replace") as f:
            for s in f:
                try:
                    o = json.loads(s)
                except ValueError:
                    continue
                if not isinstance(o, dict):
                    continue
                ts = zaman(o.get("timestamp"))
                if ts is not None and ts < sinir:
                    continue
                m = o.get("message") if isinstance(o.get("message"), dict) else {}
                icerik = [b for b in m["content"] if isinstance(b, dict)] if isinstance(m.get("content"), list) else []
                tip = o.get("type")
                if tip == "assistant":
                    mid = m.get("id")
                    if mid not in mid_idx:
                        u = m.get("usage") if isinstance(m.get("usage"), dict) else {}
                        p, a = parcala(u), agirlikli(u)
                        m5, h1 = m5 + p["cache_5m"], h1 + p["cache_1h"]
                        if mid not in gorulen:
                            gorulen.add(mid)
                            toplam += a
                        ctx = p["girdi"] + p["cache_okuma"] + p["cache_5m"] + p["cache_1h"]
                        if istek and istek[-1]["sg"] == sg and gap_n and not kirli:
                            adim.append((ctx - istek[-1]["ctx"] - istek[-1]["cikti"], gap_n))
                        gap_n, kirli = 0, False
                        mid_idx[mid] = len(istek)
                        istek.append({"ctx": ctx, "cikti": p["cikti"], "ts": ts, "sg": sg, "a": a, "arac": []})
                    i = mid_idx[mid]
                    for b in icerik:
                        if b.get("type") == "tool_use":
                            g = b.get("input") if isinstance(b.get("input"), dict) else {}
                            istek[i]["arac"].append(b.get("id"))
                            araclar.append((b.get("id"), b.get("name") or "?", g, i))
                elif tip == "user":
                    c = m.get("content")
                    metin = c if isinstance(c, str) else "".join(b.get("text") or "" for b in icerik if b.get("type") == "text")
                    sonuclar = [b for b in icerik if b.get("type") == "tool_result"]
                    kirli = kirli or bool(metin) or any(b.get("type") == "image" for b in icerik)
                    if metin and not sonuclar and not o.get("isMeta"):
                        mm = DALGA.search(metin[:300])
                        if mm and mm.group() != dalga:
                            dalga = mm.group()
                            dalgalar.append(len(istek))
                    for b in sonuclar:
                        c = b.get("content")
                        parcalar = c if isinstance(c, list) else [{"type": "text", "text": c or ""}]
                        n = round(sum(len(x.get("text") or "") for x in parcalar
                                      if isinstance(x, dict) and x.get("type") == "text") / 4)
                        gap_n += n
                        kirli = kirli or any(isinstance(x, dict) and x.get("type") == "image" for x in parcalar)
                        tr = o.get("toolUseResult") if len(sonuclar) == 1 else None
                        fl = tr.get("file") if isinstance(tr, dict) else None
                        sonuc[b.get("tool_use_id")] = (n, len(istek), sg, fl.get("totalLines") if isinstance(fl, dict) else None)
                elif tip == "attachment":
                    ek = o.get("attachment") if isinstance(o.get("attachment"), dict) else {}
                    kirli = kirli or ek.get("type") != "hook_success"  # hook_success stdout bağlama girmez
                    if ek.get("hookEvent") == "PreToolUse" and "Bash" in str(ek.get("hookName")):
                        try:
                            komut = json.loads(ek.get("stdout") or "{}")["hookSpecificOutput"]["updatedInput"]["command"]
                        except (ValueError, KeyError, TypeError):
                            komut = ""
                        if "rtk " in str(komut):
                            rtkler.add(ek.get("toolUseID"))
                elif tip == "system" and o.get("subtype") == "compact_boundary":
                    sg += 1
        if istek:
            kayit.append((yol, istek, araclar, sonuc, rtkler, dalgalar,
                          AGIRLIK["cache_1h"] if h1 > m5 else AGIRLIK["cache_5m"],
                          sum(x[0] for x in adim), sum(x[1] for x in adim), len(adim)))
    py, pd = sum(x[7] for x in kayit), sum(x[8] for x in kayit)
    genel = max(0.0, py / pd) if pd else 1.0
    ks = [max(0.0, x[7] / x[8]) for x in kayit if x[8]]
    for yol, istek, araclar, sonuc, rtkler, dalgalar, w, opay, opayda, _ in kayit:
        k = max(0.0, opay / opayda) if opayda else genel
        son_idx = {q["sg"]: i for i, q in enumerate(istek)}

        def katki(n, i, sg):
            r_ = son_idx.get(sg, -1) - i + 1
            return n * (w + AGIRLIK["cache_okuma"] * (r_ - 1)) if r_ > 0 else 0.0

        okunan, degisen, onceki, tetik = {}, set(), None, set()
        for tid, ad, g, i in araclar:
            n, si, ssg, tsonuc = sonuc.get(tid, (0, None, 0, None))
            kt = katki(n, si, ssg) if si is not None else 0.0
            kd = kt * k
            if ad == "Read":
                ham = str(g.get("file_path") or "")
                anah = ham.replace("\\", "/")
                aralik = any(x in g for x in ("offset", "limit", "pages"))
                rehber = bool(REHBER.search(anah.lower()))
                _say(oku, n, kt, kd)
                oku["aralikli"] += aralik
                oku["rehber"] += rehber
                _say(uzanti[Path(anah).suffix.lower() or "-"], n, kt, kd)
                if not rehber:
                    if aralik:
                        aralik_n.append(n)
                    else:
                        limitsiz.append((anah, _satir(tsonuc, ham), n, kt, kd))
                ar = (g.get("offset"), g.get("limit"), g.get("pages"))
                if anah in okunan:
                    x = tekrar[anah]
                    _say(x, n, kt, kd)
                    if anah not in degisen:
                        x["degismeden"] += 1
                        x["degismeden_katki"] += kt
                        x["degismeden_duz"] += kd
                        if okunan[anah] == ar:
                            x["ayni_aralik"] += 1
                            x["ayni_katki"] += kt
                            x["ayni_duz"] += kd
                okunan[anah] = ar
                degisen.discard(anah)
            elif ad == "Bash":
                kom = str(g.get("command") or "")
                x = bash[aile(kom)]
                _say(x, n, kt, kd)
                x["n"].append(n)
                rt = tid in rtkler or kom.lstrip().startswith("rtk ")
                x["rtk"] += rt
                x["nr" if rt else "ns"].append(n)
                if not rt:
                    x["rtksiz"] += kt
                    x["rtksiz_duz"] += kd
                x["pipe"] += bool(re.search(r"(?<!\|)\|(?!\|)", kom))
                x["tail"] += bool(re.search(r"\|\s*(tail|head)\b", kom))
            elif ad in DEGISTIREN:
                degisen.add(str(g.get("file_path") or g.get("notebook_path") or "").replace("\\", "/"))
            if ad.endswith("headroom_retrieve"):
                rv["adet"] += 1
                if onceki:
                    o_ad, o_i, o_tid, o_kayit = onceki
                    rv["onceki"][o_ad] += 1
                    rv["tur"].append(i - o_i)
                    if None not in (istek[i]["ts"], istek[o_i]["ts"]):
                        rv["sn"].append(istek[i]["ts"] - istek[o_i]["ts"])
                    if o_kayit and o_tid not in tetik:
                        tetik.add(o_tid)
                        _say(rv_oku[o_kayit[0]], *o_kayit[1:])
            else:
                onceki = (ad, i, tid, (anah, n, kt, kd) if ad == "Read" else None)
        adlar = {x[0]: x[1] for x in araclar}
        dizi = 0
        for j, q in enumerate(istek + [None]):
            if q is not None:
                tur["istek"] += 1
                tur["aracli"] += bool(q["arac"])
                tur["paralel"] += len(q["arac"]) > 1
                tur["arac_sayisi"][str(len(q["arac"]))] += 1
                if (len(q["arac"]) == 1 and adlar.get(q["arac"][0]) == "Read"
                        and sonuc.get(q["arac"][0], (KUCUK,))[0] < KUCUK):
                    dizi += 1
                    continue
            if dizi >= 2:
                dizi_t["dizi"] += 1
                dizi_t["istek"] += dizi
                dizi_t["kazanc"] += dizi - 1
                dizi_t["kazanc_agirlikli"] += sum(x["a"] for x in istek[j - dizi + 1:j])
            dizi = 0
        if "subagents" not in yol.parts and max(q["ctx"] for q in istek) > 200_000:
            uzun["oturum"] += 1
            uzun["tek_dalga" if len(dalgalar) <= 1 else "cok_dalga"] += 1
            for j, bas in enumerate(dalgalar[1:], 1):
                bit = dalgalar[j + 1] if j + 1 < len(dalgalar) else len(istek)
                if bas < len(istek):
                    uzun["bolme_tasarruf"] += (AGIRLIK["cache_okuma"] * max(0, istek[bas]["ctx"] - istek[0]["ctx"])
                                               * (bit - bas))
    ars = []
    for f in sorted(Path(arsiv).glob("*.md")) if arsiv and Path(arsiv).is_dir() else []:
        metin = f.read_bytes().decode("utf-8", "replace")
        for kalip in TUR_KALIP:
            ars += [{"dosya": f.name, "gercek": int(a), "tavan": int(b), "oran": round(int(a) / int(b), 2) if int(b) else None}
                    for a, b in kalip.findall(metin)]
    lb = defaultdict(lambda: {**_sayac(), "satir": 0})
    for anah, satir, n, kt, kd in limitsiz:
        if satir and satir > 300:
            _say(lb[anah], n, kt, kd)
            lb[anah]["satir"] = satir
    dag = {}
    for alt, ust in SATIR_ARALIK:
        sec = [x for x in limitsiz if x[1] is not None and x[1] > alt and (ust is None or x[1] <= ust)]
        dag[f">{alt}" if ust is None else f"{alt + 1}-{ust}"] = {
            "adet": len(sec), "katki": sum(x[3] for x in sec), "katki_duz": sum(x[4] for x in sec)}
    m_ar = statistics.median(aralik_n) if aralik_n else 0
    esik = []
    for e in ESIKLER:
        sec = [x for x in limitsiz if x[1] is not None and x[1] > e]
        kes = [max(0.0, 1 - m_ar / x[2]) if x[2] else 0.0 for x in sec]  # ret → aralıklı medyan boyunda yeniden okuma
        esik.append({"esik": e, "adet": len(sec), "katki": sum(x[3] for x in sec), "katki_duz": sum(x[4] for x in sec),
                     "tasarruf": sum(x[3] * c for x, c in zip(sec, kes)),
                     "tasarruf_duz": sum(x[4] * c for x, c in zip(sec, kes))})
    def med(xs):
        return statistics.median(xs) if xs else None
    bl = []
    for a, v in sorted(bash.items(), key=lambda kv: -kv[1]["token"]):
        mr, ms = med(v["nr"]), med(v["ns"])
        # ponytail: rtk oranı rtk'lı/rtk'sız medyan çıktıdan; komut biçimi farkı karışır, A/B koşusu TOKEN-4b'de
        bl.append({"aile": a, **{c: v[c] for c in v if c not in ("n", "nr", "ns")}, "medyan": med(v["n"]),
                   "medyan_rtk": mr, "medyan_rtksiz": ms,
                   "rtk_oran": min(1.0, max(0.0, 1 - mr / ms)) if mr is not None and ms else 0.0})
    tekrar_l, lb_l, rv_l = _liste(tekrar, "dosya"), _liste(lb, "dosya"), _liste(rv_oku, "dosya")

    def oz(kat, ad, xs):
        return {"kategori": kat, "anahtar": ad, **{c: sum(x[c] for x in xs) for c in ("adet", "token", "katki", "katki_duz")}}
    kaynaklar = ([oz("limitsiz>300", "Read >300 satır, aralıksız (rehber dışı)", lb_l),
                  oz("tekrar", "aynı dosyanın tekrar okunması", tekrar_l),
                  oz("retrieve-read", "headroom_retrieve'i tetikleyen Read", rv_l)]
                 + [oz("bash", x["aile"], [x]) for x in bl])
    kaynaklar = sorted((x for x in kaynaklar if x["katki"]), key=lambda x: -x["katki_duz"])[:10]
    for x in kaynaklar:
        x["pay"] = 100 * x["katki_duz"] / (toplam or 1)
    b5 = bl[:5]
    return {
        "pencere_gun": gun, "dosya": dosya, "toplam_agirlikli": toplam,
        "katsayi": {"oturum": len(ks), "medyan": statistics.median(ks) if ks else genel, "genel": genel,
                    "adim": sum(x[9] for x in kayit)},
        "read": {**oku, "uzanti": dict(uzanti), "aralikli_medyan_token": m_ar, "satir_dagilim": dag, "esik": esik},
        "limitsiz_buyuk": lb_l, "tekrar": tekrar_l, "bash": bl,
        "retrieve": {"adet": rv["adet"], "onceki": dict(rv["onceki"]),
                     "sn_medyan": statistics.median(rv["sn"]) if rv["sn"] else None,
                     "tur_medyan": statistics.median(rv["tur"]) if rv["tur"] else None, "read_dosyalar": rv_l},
        "tur": {**tur, "arac_sayisi": dict(tur["arac_sayisi"]), "kucuk_read_dizisi": dizi_t},
        "arsiv": ars, "uzun": uzun, "kaynaklar": kaynaklar,
        "kaldirac_gunluk": {
            "L8a": [{"esik": e["esik"], "ham": e["tasarruf"] / gun, "duz": e["tasarruf_duz"] / gun} for e in esik],
            "L8b": {"ham": sum(x["rtksiz"] * x["rtk_oran"] for x in b5) / gun,
                    "duz": sum(x["rtksiz_duz"] * x["rtk_oran"] for x in b5) / gun},
            "L8b_ust": {"ham": sum(x["rtksiz"] for x in b5) / gun, "duz": sum(x["rtksiz_duz"] for x in b5) / gun},
            "L8c": {"ham": sum(x["ayni_katki"] for x in tekrar_l) / gun, "duz": sum(x["ayni_duz"] for x in tekrar_l) / gun},
            "L8c_ust": {"ham": sum(x["degismeden_katki"] for x in tekrar_l) / gun,
                        "duz": sum(x["degismeden_duz"] for x in tekrar_l) / gun},
            "L7": {"istek": dizi_t["kazanc"] / gun, "agirlikli": dizi_t["kazanc_agirlikli"] / gun},
            "L14": {"agirlikli": uzun["bolme_tasarruf"] / gun}}}


def tablo_dokum(d):
    def mb(x):
        return f"{x / 1e6:.3f}"
    k, r, u, rv, z, kal = d["katsayi"], d["read"], d["tur"], d["retrieve"], d["uzun"], d["kaldirac_gunluk"]
    kd = u["kucuk_read_dizisi"]
    s = [f"{d['pencere_gun']} gün · {d['dosya']} dosya · toplam ağırlıklı {mb(d['toplam_agirlikli'])} M · Headroom k"
         f" medyan {k['medyan']:.2f} · genel {k['genel']:.2f} ({k['oturum']} oturum, {k['adim']} temiz adım)"
         " · katkı ham → düz (×k)",
         "", "en büyük 10 kaynak | kategori | adet | token | ham M | düz M | pay %"]
    s += [f"{x['anahtar']} | {x['kategori']} | {x['adet']} | {x['token']} | {mb(x['katki'])} | {mb(x['katki_duz'])}"
          f" | {x['pay']:.2f}" for x in d["kaynaklar"]]
    s += ["", f"Read {r['adet']} · aralıklı {r['aralikli']} · rehber {r['rehber']} · {r['token']} tok · ham {mb(r['katki'])}"
              f" → düz {mb(r['katki_duz'])} M · aralıklı medyan {r['aralikli_medyan_token']} tok",
          "limitsiz satır dağılımı (rehber dışı) | adet | ham M | düz M"]
    s += [f"{a} | {v['adet']} | {mb(v['katki'])} | {mb(v['katki_duz'])}" for a, v in r["satir_dagilim"].items()]
    s += ["", "limitsiz >300 satır (ilk 10) | adet | satır | ham M | düz M"]
    s += [f"{x['dosya']} | {x['adet']} | {x['satir']} | {mb(x['katki'])} | {mb(x['katki_duz'])}"
          for x in d["limitsiz_buyuk"][:10]]
    s += ["", "Bash ailesi (ilk 5, çıktı) | adet | token | medyan (rtk/rtksız) | rtk | pipe | tail/head | ham M | düz M"]
    s += [f"{x['aile']} | {x['adet']} | {x['token']} | {x['medyan']:.0f} ({x['medyan_rtk']}/{x['medyan_rtksiz']})"
          f" | {x['rtk']} | {x['pipe']} | {x['tail']} | {mb(x['katki'])} | {mb(x['katki_duz'])}" for x in d["bash"][:5]]
    s += ["", "tekrar okuma (ilk 10) | tekrar | değişmeden | aynı aralık | ham M | düz M"]
    s += [f"{x['dosya']} | {x['adet']} | {x['degismeden']} | {x['ayni_aralik']} | {mb(x['katki'])} | {mb(x['katki_duz'])}"
          for x in d["tekrar"][:10]]
    s += ["", f"headroom_retrieve {rv['adet']} · önceki araç {rv['onceki']} · sn medyan {rv['sn_medyan'] or 0:.1f} · tur medyan"
              f" {rv['tur_medyan']}", "tetikleyen Read (ilk 10) | adet | token | ham M | düz M"]
    s += [f"{x['dosya']} | {x['adet']} | {x['token']} | {mb(x['katki'])} | {mb(x['katki_duz'])}"
          for x in rv["read_dosyalar"][:10]]
    s += ["", f"tur: {u['istek']} istek · araçlı {u['aracli']} · paralel {u['paralel']}"
              f" (%{100 * u['paralel'] / (u['aracli'] or 1):.1f}) · araç sayısı {u['arac_sayisi']} · küçük Read dizisi"
              f" {kd['dizi']} ({kd['istek']} istek, kazanç {kd['kazanc']} istek = {mb(kd['kazanc_agirlikli'])} M)",
          "arşiv | gerçek/tavan | oran"]
    s += [f"{x['dosya']} | {x['gercek']}/{x['tavan']} | {x['oran']}" for x in d["arsiv"]]
    s += ["", f">200k oturum {z['oturum']} · tek dalga {z['tek_dalga']} · çok dalga {z['cok_dalga']} · dalga bölme"
              f" tasarrufu {mb(z['bolme_tasarruf'])} M", "", "kaldıraç günlük | ham M | düz M | Headroom örtüşmesi M"]
    s += [f"L8a eşik >{e['esik']} satır | {mb(e['ham'])} | {mb(e['duz'])} | {mb(e['ham'] - e['duz'])}" for e in kal["L8a"]]
    s += [f"{a} | {mb(kal[a]['ham'])} | {mb(kal[a]['duz'])} | {mb(kal[a]['ham'] - kal[a]['duz'])}" for a in ("L8b", "L8b_ust", "L8c", "L8c_ust")]
    s += [f"L7 küçük Read birleştirme | usage {mb(kal['L7']['agirlikli'])} | {kal['L7']['istek']:.1f} istek/gün",
          f"L14 dalga bölme | usage {mb(kal['L14']['agirlikli'])}"]
    return "\n".join(s)


OLCUM = re.compile(r"(?i)^\s*ok\s*$")  # TOKEN-6b K1: ölçüm koşusu ilk istemi (docs/token-6b.md §K1)
GRUPLAR = ("etk·ana omer-skills", "etk·ana diğer", "etk·subagent", "claude-p", "observer")


def grup(x):
    k = x["kaynak"]
    if k in ("observer", "claude-p"):
        return k
    if k == "etkilesimli":
        return "etk·subagent" if x["ajan"] == "subagent" else "etk·ana omer-skills" if "omer-skills" in (x["proje"] or "") else "etk·ana diğer"
    return None


def _ilk_istem(yol):
    with Path(yol).open(encoding="utf-8", errors="replace") as f:
        for s in f:
            try:
                o = json.loads(s)
            except ValueError:
                continue
            if isinstance(o, dict) and o.get("type") == "user" and not o.get("isMeta") and isinstance(o.get("message"), dict):
                c = o["message"].get("content")
                if isinstance(c, list):
                    c = next((b.get("text") or "" for b in c if isinstance(b, dict) and b.get("type") == "text"), "")
                return c if isinstance(c, str) else ""
    return ""


def karsilastir(taban, kok, baslar, simdi=None, az=30):
    """TOKEN-6b K1: taban (olcum/token-0.json) → grup başına dönem başından bugüne normalize metrikler ve Σ pay × düşüş.
    Birincil: observer ağ./gün · claude-p ağ./çağrı · etk ağ./istek. Ölçüm koşuları (OLCUM ilk istemi, alt ajanı üst
    oturumuyla) ayrı sayılır ve karşılaştırmaya girmez; istek < az grup "yetersiz örnek", toplamda 0 sayılır."""
    simdi, bol = simdi or time.time(), (lambda x, y: x / y if y else 0)
    bos = lambda: {"istek": 0, "agirlikli": 0, "usd": 0, "cikti": 0, "taban": [], "cagri": 0}  # noqa: E731
    tb, sayildi = {g: bos() for g in GRUPLAR}, set()
    for x in taban["satirlar"]:
        if grup(x):
            u = {"input_tokens": x["girdi"], "cache_read_input_tokens": x["cache_okuma"], "output_tokens": x["cikti"],
                 "cache_creation": {"ephemeral_5m_input_tokens": x["cache_5m"], "ephemeral_1h_input_tokens": x["cache_1h"]}}
            for alan, v in (("istek", x["istek"]), ("agirlikli", x["agirlikli"]), ("usd", usd(u, x["model"]) or 0), ("cikti", x["cikti"])):
                tb[grup(x)][alan] += v
    for o in taban["oturumlar"]:
        if grup(o) and o["ajan"] == "ana":
            tb[grup(o)]["taban"].append(o["taban"])
            tb[grup(o)]["cagri"] += 1
    top = {k: sum(v[k] for v in tb.values()) or 1 for k in ("agirlikli", "usd")}
    r = {"gruplar": {}, "olcum": {"oturum": 0, "istek": 0, "agirlikli": 0}, "tasarruf": 0, "tasarruf_usd": 0}
    for g in GRUPLAR:
        bas = baslar.get(g, baslar["varsayilan"])
        gun, n = (simdi - bas) / 86400, bos()
        ss = tara(kok, gun, simdi)["oturumlar"]
        olc = {Path(o["oturum"]).stem for o in ss if o["ajan"] == "ana" and OLCUM.search(_ilk_istem(Path(kok) / o["oturum"]))}
        for o in (o for o in ss if grup(o) == g):
            p = Path(o["oturum"])
            if p.stem in olc or (p.parent.name == "subagents" and p.parent.parent.name in olc):
                if o["oturum"] not in sayildi:
                    sayildi.add(o["oturum"])
                    for alan, v in (("oturum", 1), ("istek", o["tur"]), ("agirlikli", o["agirlikli"])):
                        r["olcum"][alan] += v
                continue
            for alan, v in (("istek", o["tur"]), ("agirlikli", o["agirlikli"]), ("usd", o["usd"]), ("cikti", o["cikti"])):
                n[alan] += v
            if o["ajan"] == "ana":
                n["taban"].append(o["taban"])
                n["cagri"] += 1
        bolen = {"observer": lambda v, d: d, "claude-p": lambda v, d: v["cagri"]}.get(g, lambda v, d: v["istek"])
        ikili = lambda f: {"taban": f(tb[g], taban["pencere_gun"]), "simdi": f(n, gun)}  # noqa: E731
        s = {"bas": bas, "istek": n["istek"], "yetersiz": n["istek"] < az, "pay": tb[g]["agirlikli"] / top["agirlikli"],
             "birincil": ikili(lambda v, d: bol(v["agirlikli"], bolen(v, d))),
             "birincil_usd": ikili(lambda v, d: bol(v["usd"], bolen(v, d))),
             "agirlikli_istek": ikili(lambda v, d: bol(v["agirlikli"], v["istek"])),
             "usd_istek": ikili(lambda v, d: bol(v["usd"], v["istek"])),
             "cikti_istek": ikili(lambda v, d: bol(v["cikti"], v["istek"])),
             "ilk_istem": ikili(lambda v, d: bol(sum(v["taban"]), len(v["taban"])))}
        for k, alan, kay in (("tasarruf", "birincil", "agirlikli"), ("tasarruf_usd", "birincil_usd", "usd")):
            b, pay = s[alan], tb[g][kay] / top[kay]
            if b["taban"] and not s["yetersiz"]:
                r[k] += pay * (1 - b["simdi"] / b["taban"])
        r["gruplar"][g] = s
    return r


def tablo_karsilastir(r):
    yz = lambda d: f"{d['taban']:.0f} → {d['simdi']:.0f} ({100 * (d['simdi'] / d['taban'] - 1):+.0f}%)" if d["taban"] else "-"  # noqa: E731
    s = ["grup | dönem başı UTC | istek | pay | birincil ağ. taban → şimdi | birincil $ taban → şimdi | ağ./istek | çıktı/istek | ilk istem"]
    for g, v in r["gruplar"].items():
        u = v["birincil_usd"]
        s.append(f"{g}{' (yetersiz örnek)' if v['yetersiz'] else ''} | {time.strftime('%m-%d %H:%M', time.gmtime(v['bas']))} | {v['istek']}"
                 f" | %{100 * v['pay']:.1f} | {yz(v['birincil'])} | {u['taban']:.4f} → {u['simdi']:.4f} | {yz(v['agirlikli_istek'])}"
                 f" | {yz(v['cikti_istek'])} | {yz(v['ilk_istem'])}")
    o = r["olcum"]
    s += ["", f"ölçüm koşuları (hariç): {o['oturum']} oturum · {o['istek']} istek · ağırlıklı {o['agirlikli'] / 1e6:.2f} M",
          f"toplam tahmini tasarruf = Σ pay × normalize düşüş: ağırlıklı %{100 * r['tasarruf']:.1f} · $ %{100 * r['tasarruf_usd']:.1f}"
          " (yetersiz örnek grupları 0 sayılır)",
          "Çekince: dönem kısa ve çoğu TOKEN dalgalarının kendi oturumları; iş karışımı tabandan farklı."]
    return "\n".join(s)


SEBEPLER = ("compact", "ara>ttl", "model/effort", "arac_listesi", "diger")


def _yuzdelik(x, q):
    return x[min(len(x) - 1, math.ceil(round(q * len(x), 9)) - 1)] if x else None


def ttl_sim(kok, gun=14, simdi=None):
    """TOKEN-6b K2: etk·ana önbellek yazması a (yeni içerik) / b (kırılma sonrası baştan) ve TTL kolları.
    1h = gerçek · 5m = 1h yazma 5m'ye, ara > 300 sn ise okuma 5m yazmaya döner · hibrit = oturum başına ucuz kol (kehanet üst sınırı).
    Ara = istekten önceki son user satırları arası (gönderim anı); TTL okumayla tazelenir."""
    sinir, kok, aralar = (simdi or time.time()) - gun * 86400, Path(kok), []
    r = {"pencere_gun": gun, "oturum": 0, "istek": 0, "yazma": {"a": 0, "b": 0},
         "sebep": {s: {"adet": 0, "token": 0} for s in SEBEPLER},
         "kollar": {k: {"agirlikli": 0, "usd": 0} for k in ("1h", "5m", "hibrit")}}
    for yol in sorted(kok.rglob("*.jsonl")) if kok.is_dir() else []:
        if yol.stat().st_mtime < sinir:
            continue
        kol = {k: {"agirlikli": 0, "usd": 0} for k in ("1h", "5m")}
        onceki, gonder, olay, gorulen = None, None, set(), set()
        with yol.open(encoding="utf-8", errors="replace") as f:
            for s in f:
                try:
                    o = json.loads(s)
                except ValueError:
                    continue
                if not isinstance(o, dict):
                    continue
                ts, tur, ek = zaman(o.get("timestamp")), o.get("type"), o.get("attachment")
                if ts is not None and ts < sinir:
                    continue
                if tur == "user" and ts is not None:
                    gonder = ts
                elif tur == "system" and o.get("subtype") == "compact_boundary":
                    olay.add("compact")
                elif tur == "attachment" and isinstance(ek, dict) and ek.get("type") == "deferred_tools_delta":
                    olay.add("arac_listesi")
                m = o.get("message") if isinstance(o.get("message"), dict) else {}
                u = m.get("usage") if tur == "assistant" else None
                if not isinstance(u, dict) or m.get("id") in gorulen:
                    continue
                if kaynak(o, yol) != "etkilesimli" or ajan_turu(o, yol) != "ana":
                    break
                gorulen.add(m.get("id"))
                p = parcala(u)
                yazma, an, me = p["cache_5m"] + p["cache_1h"], gonder if gonder is not None else ts, (m.get("model"), o.get("effort"))
                ara = an - onceki["an"] if onceki and an is not None and onceki["an"] is not None else None
                b = min(yazma, max(0, onceki["onbellek"] - p["cache_okuma"])) if onceki else 0
                if b:
                    sebep = ("compact" if "compact" in olay else "ara>ttl" if ara is not None and ara > onceki["ttl"]
                             else "model/effort" if me != onceki["me"] else "arac_listesi" if "arac_listesi" in olay else "diger")
                    r["sebep"][sebep]["adet"] += 1
                    r["sebep"][sebep]["token"] += b
                if ara is not None:
                    aralar.append(ara)
                r["yazma"]["a"] += yazma - b
                r["yazma"]["b"] += b
                kayip = p["cache_okuma"] if ara is not None and ara > 300 else 0
                u5 = {"input_tokens": p["girdi"], "cache_read_input_tokens": p["cache_okuma"] - kayip, "output_tokens": p["cikti"],
                      "cache_creation": {"ephemeral_5m_input_tokens": yazma + kayip, "ephemeral_1h_input_tokens": 0}}
                for k, uu in (("1h", u), ("5m", u5)):
                    kol[k]["agirlikli"] += agirlikli(uu)
                    kol[k]["usd"] += usd(uu, m.get("model")) or 0
                ttl = 3600 if p["cache_1h"] else 300 if p["cache_5m"] else onceki["ttl"] if onceki else 3600
                onceki, olay = {"an": an, "onbellek": p["cache_okuma"] + yazma, "ttl": ttl, "me": me}, set()
                r["istek"] += 1
        if onceki:
            r["oturum"] += 1
            ucuz = min(kol.values(), key=lambda x: x["agirlikli"])
            for alan in ("agirlikli", "usd"):
                r["kollar"]["hibrit"][alan] += ucuz[alan]
                for k in kol:
                    r["kollar"][k][alan] += kol[k][alan]
    aralar.sort()
    r["ara"] = {"n": len(aralar), **{f"p{q}": _yuzdelik(aralar, q / 100) for q in (50, 90, 99)},
                "5dk_ustu_pay": sum(x > 300 for x in aralar) / len(aralar) if aralar else 0}
    return r


def tablo_ttl(r):
    y, k1, a = r["yazma"], r["kollar"]["1h"], r["ara"]
    top = (y["a"] + y["b"]) or 1
    s = [f"{r['pencere_gun']} gün · etk·ana {r['oturum']} oturum · {r['istek']} istek · yazma {top / 1e6:.2f} M:"
         f" yeni %{100 * y['a'] / top:.1f} · baştan %{100 * y['b'] / top:.1f}", "", "sebep | adet | token M | baştan payı"]
    s += [f"{k} | {v['adet']} | {v['token'] / 1e6:.2f} | %{100 * v['token'] / (y['b'] or 1):.1f}" for k, v in r["sebep"].items()]
    s += ["", "kol | ağırlıklı M | $ | 1h'e göre"]
    s += [f"{k} | {v['agirlikli'] / 1e6:.2f} | {v['usd']:.2f} | %{100 * (v['agirlikli'] / (k1['agirlikli'] or 1) - 1):+.1f}"
          for k, v in r["kollar"].items()]
    s += ["", f"istek arası (sn): n {a['n']} · p50 {a['p50']} · p90 {a['p90']} · p99 {a['p99']} · >5 dk %{100 * a['5dk_ustu_pay']:.1f}"]
    return "\n".join(s)


def main(a):
    if not a or a[0] != "olc":
        print(__doc__)
        return 2

    def deger(ad, vars):
        return a[a.index(ad) + 1] if ad in a else vars

    kok, gun, repo = deger("--kok", Path.home() / ".claude" / "projects"), int(deger("--gun", 14)), Path(__file__).resolve().parents[1]
    if "--arac-dokum" in a:
        r, yazi = dokum(kok, gun, arsiv=deger("--arsiv", repo / ".claude" / "dalga-arsiv")), tablo_dokum
    elif "--karsilastir" in a:
        baslar = {k: zaman(v) for k, v in (x.split("=", 1) for i, x in enumerate(a) if i and a[i - 1] == "--bas")}
        r = karsilastir(json.loads(Path(deger("--karsilastir", None)).read_text(encoding="utf-8")), kok, baslar)
        yazi = tablo_karsilastir
    elif "--ttl-sim" in a:
        r, yazi = ttl_sim(kok, gun), tablo_ttl
    else:
        r, yazi = tara(kok, gun, motor=deger("--motor", repo / "olcum" / "motor-usage.jsonl")), tablo
    cikti = deger("--cikti", None)
    if cikti:
        Path(cikti).parent.mkdir(parents=True, exist_ok=True)
        Path(cikti).write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    print(yazi(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
