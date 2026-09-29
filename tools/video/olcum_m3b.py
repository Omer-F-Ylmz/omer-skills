"""MOTOR-M3b ölçüm: beş altın set videosu güncel motorla (izole rapor dizini) yeniden taranır, altın kalemlerle eşlenir.

Kullanım (tools/video'da): uv run python olcum_m3b.py [tara|esle|rapor|hepsi]
Her adım .kos/m3b/<adim>.json'a yazar; tamamlanan parti/adım yeniden koşuda atlanır. Motor koduna dokunmaz:
ucuz kollar hafif.cagir yerine OpenRouter adaptörüyle aynı parti hattından (girdi + form + rapor_md) geçer.
"""
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from video import akil, cli, hafif, kur
from video import parti as pt
from video import tarama as tr

REPO = Path(__file__).resolve().parents[2]
KOS = REPO / ".kos" / "m3b"
CACHE = Path(os.environ.get("VIDEO_CACHE") or cli.KOK)
ONEM = ("yüksek", "orta", "düşük")
ATLA_ALTIN = {"Kaynaklar", "Emin olunmayanlar"}
ATLA_RAPOR = {"Künye", "Özet", "Bölümler", "Belirsizlikler", "Atlanan segment oranı"}
VIDEOLAR = {"L9c49WVG_ho": (0.6, "ücretsiz API anahtarı"), "kHtOSJRUkLs": (19.8, "yapılandırma/prompt token tasarrufu"),
            "g89FJiNAlEs": (15.1, "4 repo token tasarrufu"), "86HM0RUWhCk": (27.9, "site/UI uçtan uca + prompt anatomisi"),
            "JfmAm3sxCSc": (10.9, "site/UI 3D website")}
GRUPLAR = [["L9c49WVG_ho"], ["kHtOSJRUkLs", "g89FJiNAlEs", "86HM0RUWhCk"], ["JfmAm3sxCSc"]]
# kol → (OpenRouter modeli | None=motorun kendisi, grup başına (hafif çağrı tavanı, $ tavanı)); sonnet Σ 8 / $1,0 · ucuz Σ $0,25+$0,25
KOLLAR = {"sonnet": (None, [(2, .15), (4, .55), (2, .30)]),
          "luna": ("openai/gpt-6-luna-pro", [(2, .04), (4, .13), (2, .08)]),
          "qwen": ("qwen/qwen3.8-27b:free", [(2, .04), (4, .13), (2, .08)])}
JEV_TAVAN = 300
OR_URL = cli.OR_URL
ZAMAN = re.compile(r"\b(\d{1,2}):(\d{2})(?::(\d{2}))?\b")


def sn(metin):
    if not (z := ZAMAN.search(metin or "")):
        return None
    a, b, c_ = int(z[1]), int(z[2]), z[3]
    return a * 3600 + b * 60 + int(c_) if c_ else a * 60 + b


def url_norm(u):
    u = re.sub(r"^https?://", "", u.strip().lower().rstrip(".,;"))
    return re.split(r"[?#]", re.sub(r"^www\.", "", u))[0].rstrip("/")


def anahtarlar(metin, ad):
    k = {n} if len(n := tr.normal(re.sub(r"\(.*?\)", "", ad))) >= 3 else set()
    k |= {url_norm(u) for u in re.findall(r"https?://[^\s|)`\"'<>]+", metin)}
    k |= {f"github.com/{r.lower()}" for r in re.findall(r"\(([\w.-]+/[\w.-]+)\)", metin)}
    return k | {n for x in re.findall(r"`([^`]+)`", metin) if len(n := tr.normal(x)) >= 3}


def altin_oku(md):
    """## Kategori altında `N. …` / `- …` satırları; Kaynaklar ve Emin olunmayanlar ölçüme girmez."""
    kat, out = None, []
    for s in md.splitlines():
        if h := re.match(r"##\s+(.+?)(?:\s+\(\d+\))?\s*$", s):
            kat = h[1]
        elif kat and kat not in ATLA_ALTIN and (m := re.match(r"\s*(?:\d+\.|-)\s+(.+)", s)) and not m[1].lower().startswith("yok"):
            p = [x.strip() for x in m[1].split(" · ")]
            out.append({"kat": kat, "metin": m[1], "ad": p[0], "onem": next((o for o in ONEM if p[-1].startswith(o)), None),
                        "zaman": sn(m[1])})
    return out


def motor_kalemleri(md):
    """Rapor bölümlerindeki tablo satırları ve maddeler (başlık/ayraç, Künye/Özet/Bölümler/Belirsizlikler hariç)."""
    bolum, bas, out = None, False, []
    for s in md.splitlines():
        if h := re.match(r"##\s+(.+?)\s*$", s):
            bolum, bas = h[1], False
        elif not bolum or bolum in ATLA_RAPOR:
            continue
        elif s.lstrip().startswith("|"):
            h = [x.strip() for x in re.split(r"(?<!\\)\|", s.strip().strip("|"))]
            if not bas or all(re.fullmatch(r":?-+:?", x) for x in h):
                bas = True
                continue
            out.append({"bolum": bolum, "ad": h[0], "metin": " · ".join(h), "zaman": sn(" ".join(h[1:]))})
        elif (m := re.match(r"\s*-\s+(.+)", s)) and not re.match(r"(yok|EKSİK)\b", m[1]):
            out.append({"bolum": bolum, "ad": m[1].strip(), "metin": m[1].strip(), "zaman": sn(m[1])})
    return out


def det_esle(altin, motor):
    mk = [anahtarlar(m["metin"], m["ad"]) for m in motor]
    return {i: j for i, a in enumerate(altin) if (ak := anahtarlar(a["metin"], a["ad"]))
            for j in [next((j for j, k in enumerate(mk) if ak & k), None)] if j is not None}


def _sozcuk(m):
    return set(re.findall(r"\w{3,}", m.casefold()))


def adaylar_sec(a, motor, k=5):
    w = _sozcuk(a["metin"])
    p = sorted(((len(w & (x := _sozcuk(m["metin"]))) / (len(w | x) or 1), j) for j, m in enumerate(motor)), reverse=True)
    return [j for s, j in p[:k] if s > 0]


def jev_sinirla(k2, k3, tavan):
    """Öncelik: K2 (tüm kollar tek durumda) → K3 kol sırasıyla; aşan 'ölçülemedi'."""
    k2, kalan, out, dus = k2[:tavan], tavan - min(len(k2), tavan), {}, {}
    for kol, x in k3.items():
        out[kol], dus[kol] = x[:kalan], max(0, len(x) - kalan)
        kalan -= len(out[kol])
    return k2, out, dus


def metrik(altin, eslesen):
    say = lambda xs: (sum(i in eslesen for i in xs), len(xs))
    kir = {}
    for i, a in enumerate(altin):
        kir.setdefault((a["kat"], a["onem"] or "belirtilmemiş"), []).append(i)
    return {"yuksek": say([i for i, a in enumerate(altin) if a["onem"] == "yüksek"]), "genel": say(range(len(altin))),
            "kirilim": {k: say(v) for k, v in kir.items()}}


def oran(t):
    return t[0] / t[1] if t[1] else 0.0


def olcut(m, dayanmayan):
    return {"yuksek": not m["yuksek"][1] or oran(m["yuksek"]) >= .9, "genel": not m["genel"][1] or oran(m["genel"]) >= .75,
            "dayanmayan": oran(dayanmayan) <= .05}


def sebep(a, paket):
    """Kaçırılan altın kalem: (a) kaynak motora gitmedi · (b) formda yeri yok · (c) model atladı. (d) ayrıca: panel düşürdü."""
    if a["kat"] == "Kurulum/komutlar":
        return "b"
    t, m = a["zaman"], a["metin"]
    if re.search(r"\baçıklama\b", m):
        u = {url_norm(x) for x in re.findall(r"https?://[^\s|)`\"'<>]+", m)}
        return "a" if u - {url_norm(x) for x in re.findall(r"https?://[^\s|)`\"'<>]+", paket)} else "c"
    if t is None:
        return "c"
    if re.search(r"\bkare\b", m) and "altyazı" not in m:  # ponytail: kare zamanı paket satırındaki ilk zamandan; zamansız kare satırı sayılmaz
        kz = [z for s in paket.splitlines() if re.search(r"\.(jpg|png)", s) and (z := sn(s)) is not None]
        return "c" if any(abs(z - t) <= 30 for z in kz) else "a"
    bas = [sn(x) for x in re.findall(r"^\[(\d+:\d\d(?::\d\d)?)\]", paket, re.M)]
    return "c" if any(b <= t <= b + 75 for b in bas) else "a"


def secim(v):
    if v is None:
        return "0"
    x = v.get("choice", v) if isinstance(v, dict) else v
    return str(max(x, key=x.get) if isinstance(x, dict) else x)


def _post(url, govde, bas):
    r = urllib.request.Request(url, json.dumps(govde).encode(), bas)
    try:
        with urllib.request.urlopen(r, timeout=600) as y:
            return y.status, json.loads(y.read())
    except urllib.error.HTTPError as e:
        return e.code, {}


def or_cagir(model, env, gonder=_post, uyku=time.sleep):
    """hafif.cagir imzasında OpenRouter adaptörü → {form, usage, usd, sure, hata}; 429'da ≤2 tekrar, sonra ölçülemedi."""
    def cagir(sistem, metin, sema, kareler=(), model_=None, butce=0.5, timeout=600, env_=None, **_):
        t0 = time.monotonic()
        ekler = [{"type": "image_url", "image_url": {"url": f"data:image/{'png' if str(k).endswith('.png') else 'jpeg'};base64,"
                  + base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
        govde = {"model": model, "usage": {"include": True},
                 "response_format": {"type": "json_schema", "json_schema": {"name": "form", "strict": False, "schema": sema}},
                 "messages": [{"role": "system", "content": sistem},
                              {"role": "user", "content": [{"type": "text", "text": cli._temizle(metin, env)}, *ekler]}]}
        bas = {"Authorization": f"Bearer {env.get('OPENROUTER_API_KEY', '')}", "Content-Type": "application/json"}
        for i in range(3):
            durum, y = gonder(OR_URL, govde, bas)
            if durum != 429 or i == 2:
                break
            uyku(20 * (i + 1))
        sure = round(time.monotonic() - t0, 1)
        if durum != 200:
            return {"form": None, "usage": {}, "usd": 0.0, "sure": sure, "hata": f"ölçülemedi: HTTP {durum}"}
        u, ic = y.get("usage") or {}, (y.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        try:
            form = json.loads(ic[ic.find("{"): ic.rfind("}") + 1])
        except ValueError:
            form = None
        return {"form": form, "usage": {"input_tokens": u.get("prompt_tokens", 0), "output_tokens": u.get("completion_tokens", 0)},
                "usd": u.get("cost") or 0.0, "sure": sure, "hata": None if form is not None else "form JSON değil"}
    return cagir


# ---------------------------------------------------------------- canlı adımlar

def _oku(ad):
    return json.loads(y.read_text(encoding="utf-8")) if (y := KOS / f"{ad}.json").is_file() else {}


def _yaz(ad, d):
    KOS.mkdir(parents=True, exist_ok=True)
    (KOS / f"{ad}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def tara():
    d = _oku("tara")
    for kol, (model, tavan) in KOLLAR.items():
        tdir = KOS / kol / "rapor"
        env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(tdir), "PYTHONIOENCODING": "utf-8"}
        for gi, (vids, (n, usd)) in enumerate(zip(GRUPLAR, tavan)):
            if (anah := f"{kol}-{gi}") in d:
                continue
            (q := KOS / kol / f"kuyruk-{gi}.md").parent.mkdir(parents=True, exist_ok=True)
            q.write_text("### Sıra 1\n| id | dk | ad | not | durum |\n|---|---|---|---|---|\n"
                         + "".join(f"| {v} | {VIDEOLAR[v][0]} | {v} | {VIDEOLAR[v][1]} | bekliyor |\n" for v in vids), encoding="utf-8")
            once, asil = set((REPO / ".kos").iterdir()), hafif.cagir
            hafif.cagir = or_cagir(model, env) if model else asil
            try:
                rc = cli.main(["parti", "baslat", str(q), "--tarih", f"m3b-{kol}", "--cagri-tavan", str(n), "--usd-tavan", str(usd)], env=env)
                pdir = next(iter(set((REPO / ".kos").iterdir()) - once))
                if any(s["tarama"]["durum"] == "bekliyor" for s in json.loads((pdir / "durum.json").read_text(encoding="utf-8"))["videolar"].values()):
                    rc = cli.main(["parti", "devam", pdir.name], env=env)
            finally:
                hafif.cagir = asil
            durum = json.loads((pdir / "durum.json").read_text(encoding="utf-8"))
            cagri, dolar, jeton = pt._defter(pdir)
            d[anah] = {"pid": pdir.name, "rc": rc, "cagri": cagri, "usd": dolar, "jeton": jeton,
                       "videolar": {v: s["tarama"]["durum"] for v, s in durum["videolar"].items()}}
            _yaz("tara", d)
            print(f"tara {anah}: {d[anah]}")
    return d


def onar():
    """Motorun kuyruk akışındaki gibi form_red bir kez yeniden (parti.py:422); yalnız sonnet, kalan Σ tavan (8 çağrı / $1,0) içinde."""
    d = _oku("tara")
    env = {**os.environ, "VIDEO_TARAMA_DIZIN": str(KOS / "sonnet" / "rapor"), "PYTHONIOENCODING": "utf-8"}
    for anah, x in d.items():
        kalan = (8 - sum(y["cagri"] for k, y in d.items() if k.startswith("sonnet-")), 1.0 - sum(y["usd"] for k, y in d.items() if k.startswith("sonnet-")))
        if not anah.startswith("sonnet-") or "form_red" not in x["videolar"].values() or kalan[0] < 1:
            continue
        pdir = REPO / ".kos" / x["pid"]
        cli.main(["parti", "devam", x["pid"], "--form-red-yeniden", "--cagri-ek", "1", "--usd-ek", f"{kalan[1] - .005:.3f}"], env=env)
        durum = json.loads((pdir / "durum.json").read_text(encoding="utf-8"))
        x["cagri"], x["usd"], x["jeton"] = pt._defter(pdir)
        x["videolar"] = {v: s["tarama"]["durum"] for v, s in durum["videolar"].items()}
        _yaz("tara", d)
        print(f"onar {anah}: {x}")


def k3_duzelt(m, karar, paket):
    """Jev 'dayanmıyor' sonrası deterministik düzeltme: URL paket.md girdisinde varsa dayanıyor; karede okunmuşsa metinle doğrulanamaz."""
    if karar != "dayanmıyor":
        return karar
    u = {url_norm(x) for x in re.findall(r"https?://[^\s|)`\"'<>]+", m["metin"])}
    if u and u <= {url_norm(x) for x in re.findall(r"https?://[^\s|)`\"'<>]+", paket)}:
        return "dayanıyor"
    return "kare-doğrulanamadı" if "karede" in m["metin"] or "Kare" in m["bolum"] else karar


def _pencere(vid, m, paket):
    seg = [json.loads(s) for s in (CACHE / vid / "segmentler.jsonl").read_text(encoding="utf-8").splitlines() if s.strip()]
    if m["zaman"] is not None:
        sec = [s for s in seg if s["bas"] <= m["zaman"] + 60 and s["son"] >= m["zaman"] - 60]
    else:
        w = _sozcuk(m["metin"])
        sec = sorted(seg, key=lambda s: -len(w & _sozcuk(s["metin"])))[:2]
    return (tr.bolum(paket, "Açıklama bağlantıları")[:1200] + "\n" + "\n".join(s["metin"] for s in sec))[:3500]


def _metin(s):
    """Jev state düz metin ister (cekirdek.redakte); alanlar `ad:` başlıklı bloklar, sorular bunlara backtick'le atıf yapar."""
    return "\n\n".join(f"{k}:\n{v}" for k, v in s.items())


def esle():
    from jev import cekirdek as c
    env = dict(os.environ)
    veri = {}
    for vid in VIDEOLAR:
        altin = altin_oku((REPO / "docs" / "olcumler" / "altin" / f"{vid}.md").read_text(encoding="utf-8"))
        paket = (CACHE / vid / "paket.md").read_text(encoding="utf-8")
        kol_v = {}
        for kol in KOLLAR:
            r = sorted((KOS / kol / "rapor").glob(f"*-{vid}.md"))
            md = r[-1].read_text(encoding="utf-8") if r else None
            motor = motor_kalemleri(md) if md else None
            panel = set()
            if md:
                for a in akil.birlestir([(vid, md)], REPO)[0].values():
                    panel |= {tr.normal(x) for x in [a["ad"], *a["adlar"]]}
            kol_v[kol] = {"rapor": r[-1].name if r else None, "motor": motor, "panel": sorted(panel),
                          "det": {str(i): j for i, j in det_esle(altin, motor).items()} if motor else {}}
        veri[vid] = {"altin": altin, "kollar": kol_v, "paket_var": True}
    # K2: det eşleşmeyen altın kalem başına tek durum; her kol için ayrı choice sorusu
    k2 = []
    for vid, v in veri.items():
        for i, a in enumerate(v["altin"]):
            st, bos = {"altin": f"[{a['kat']}] {a['metin']}"}, True
            for kol, kv in v["kollar"].items():
                js = [] if kv["motor"] is None or str(i) in kv["det"] else adaylar_sec(a, kv["motor"])
                kv.setdefault("aday", {})[str(i)] = js
                st[f"adaylar_{kol}"] = "\n".join(f"{n + 1}. [{kv['motor'][j]['bolum']}] {kv['motor'][j]['metin'][:300]}" for n, j in enumerate(js)) or "(yok)"
                bos &= not js
            if not bos:
                k2.append(((vid, i), st))
    k2s, _, _ = jev_sinirla(k2, {}, JEV_TAVAN)
    kr = {"0": "hiçbiri aynı bilgiyi vermiyor", **{str(n): f"{n}. aday" for n in range(1, 6)}}
    q = {kol: {"type": "choice", "criteria": kr, "instructions":
               f"`altin` altın set kalemi. `adaylar_{kol}` motor kalemlerinden hangisi AYNI bilgiyi karşılıyor (aynı araç/link/komut/teknik/"
               "kural/prompt/kare bilgisi)? Kategori ya da bölüm farkı engel değil. Yalnız benzer konu yetmez. Liste '(yok)' ya da hiçbiri → 0."}
         for kol in KOLLAR}
    t = c.Tasiyici(env=env, en_fazla=len(c.parcala([s for _, s in k2s])) + 1, istek_tavan=len(k2s) + 10)
    cev = t.yargila([_metin(s) for _, s in k2s], q) if k2s else []
    for ((vid, i), _), r in zip(k2s, cev):
        for kol, kv in veri[vid]["kollar"].items():
            n = int(secim((r or {}).get(kol)) or 0) if kv["aday"].get(str(i)) else 0
            if 0 < n <= len(kv["aday"][str(i)]):
                kv.setdefault("jev", {})[str(i)] = kv["aday"][str(i)][n - 1]
    # K3: hiçbir altın kaleme eşleşmeyen motor kalemleri → kaynakta var mı
    k3 = {}
    for kol in KOLLAR:
        for vid, v in veri.items():
            kv = v["kollar"][kol]
            if kv["motor"] is None:
                continue
            esli = set(kv["det"].values()) | set(kv.get("jev", {}).values())
            paket = (CACHE / vid / "paket.md").read_text(encoding="utf-8")
            k3.setdefault(kol, []).extend(((vid, j), {"kalem": f"[{m['bolum']}] {m['metin'][:400]}", "kaynak": _pencere(vid, m, paket)})
                                          for j, m in enumerate(kv["motor"]) if j not in esli)
    _, k3s, dus = jev_sinirla([], k3, JEV_TAVAN - len(k2s))
    q3 = {"dayanir": {"type": "noul", "instructions": "`kaynak` video altyazısı/açıklamasından bir kesit. `kalem` motorun çıkardığı bilgi. "
                      "Kaynak bu bilgiyi açıkça içeriyor ya da destekliyor mu? Kaynakta olmayan ayrıntı eklenmişse hayır."}}
    for kol, xs in k3s.items():
        if not xs:
            continue
        t = c.Tasiyici(env=env, en_fazla=len(c.parcala([s for _, s in xs])) + 1, istek_tavan=len(xs) + 10)
        for ((vid, j), _), r in zip(xs, t.yargila([_metin(s) for _, s in xs], q3)):
            p = ((r or {}).get("dayanir") or {}).get("noul")
            m = veri[vid]["kollar"][kol]["motor"][j]
            veri[vid]["kollar"][kol].setdefault("k3", {})[str(j)] = (
                "ölçülemedi" if p is None else "dayanıyor" if p >= .5 else "kare-doğrulanamadı" if "Kare" in m["bolum"] else "dayanmıyor")
    _yaz("esle", {"veri": veri, "jev": {"k2": len(k2s), "k2_istenen": len(k2), "k3": {k: len(x) for k, x in k3s.items()}, "k3_dusen": dus}})
    print(f"esle: jev K2 {len(k2s)}/{len(k2)} · K3 {sum(len(x) for x in k3s.values())} · düşen {dus}")


def _pct(t):
    return f"%{100 * oran(t):.0f} ({t[0]}/{t[1]})"


def rapor():
    e, ta = _oku("esle"), _oku("tara")
    veri, ozet = e["veri"], {}
    for kol in KOLLAR:
        tum, esl, say3, seb, ornek, d_say = [], set(), {"dayanıyor": 0, "dayanmıyor": 0, "kare-doğrulanamadı": 0, "ölçülemedi": 0}, {}, {}, 0
        for vid, v in veri.items():
            kv = v["kollar"][kol]
            if kv["motor"] is None:  # tarama hata/bitmedi → bu kolda video ölçülemedi, metriğe girmez
                continue
            eslesen ={int(i) for i in kv["det"]} | {int(i) for i in kv.get("jev", {})}
            paket = (CACHE / vid / "paket.md").read_text(encoding="utf-8")
            for i, a in enumerate(v["altin"]):
                tum.append({**a, "vid": vid})
                if i in eslesen:
                    esl.add(len(tum) - 1)
                    j = kv["det"].get(str(i), kv.get("jev", {}).get(str(i)))
                    m = kv["motor"][j]
                    d_say += m["bolum"] == "Adaylar" and tr.normal(m["ad"]) not in set(kv["panel"])
                elif a["onem"] in ("yüksek", "orta"):
                    s = sebep(a, paket)
                    seb[s] = seb.get(s, 0) + 1
                    ornek.setdefault(s, f"{vid} · {a['metin'][:90]}")
            for j, x in list(kv.get("k3", {}).items()):
                kv["k3"][j] = x = k3_duzelt(kv["motor"][int(j)], x, paket)
                say3[x] += 1
        n_motor = sum(len(v["kollar"][kol]["motor"] or []) for v in veri.values())
        m = metrik(tum, esl)
        alt, ust = (say3["dayanmıyor"], n_motor), (say3["dayanmıyor"] + say3["kare-doğrulanamadı"] + say3["ölçülemedi"], n_motor)
        grup = [x for k, x in ta.items() if k.startswith(kol + "-")]
        ozet[kol] = {"m": m, "tum": tum, "esl": esl, "alt": alt, "ust": ust, "say3": say3, "seb": seb, "ornek": ornek, "d": d_say,
                     "n_motor": n_motor, "usd": sum(x["usd"] for x in grup), "jeton": sum(x["jeton"] for x in grup),
                     "cagri": sum(x["cagri"] for x in grup), "ol_alt": olcut(m, alt), "ol_ust": olcut(m, ust)}
    s0 = ozet["sonnet"]
    gk = lambda b: "GEÇTİ" if b else "KALDI"
    L = ["# M3b — altın set ölçümü (güncel motor)", "",
         "| kol | yüksek-önem | genel | dayanmayan (alt–üst) | motor kalem | hafif çağrı | jeton | $ |", "|---|---|---|---|---|---|---|---|"]
    L += [f"| {k} | {_pct(z['m']['yuksek'])} | {_pct(z['m']['genel'])} | {_pct(z['alt'])} – {_pct(z['ust'])} | {z['n_motor']} | {z['cagri']} | {z['jeton']} | {z['usd']:.4f} |"
          for k, z in ozet.items()]
    L += ["", "## Ölçütler (önceden sabit; sonnet = güncel motor)",
          f"- yüksek-önem ≥%90: {gk(s0['ol_alt']['yuksek'])} ({_pct(s0['m']['yuksek'])})",
          f"- tüm kalemler ≥%75: {gk(s0['ol_alt']['genel'])} ({_pct(s0['m']['genel'])})",
          f"- dayanmayan ≤%5: alt sınır {gk(s0['ol_alt']['dayanmayan'])} ({_pct(s0['alt'])}) · üst sınır (kare-doğrulanamadı + ölçülemedi dahil) {gk(s0['ol_ust']['dayanmayan'])} ({_pct(s0['ust'])})",
          f"- sonuç: motor {'MÜKEMMEL' if all(s0['ol_alt'].values()) and all(s0['ol_ust'].values()) else 'mükemmel DEĞİL → kaçırma sebepleri M4 düzeltme listesine'}",
          "", "## Kategori × önem yakalama (sonnet)", "| kategori | önem | yakalama |", "|---|---|---|"]
    L += [f"| {k[0]} | {k[1]} | {_pct(t)} |" for k, t in sorted(s0["m"]["kirilim"].items())]
    L += ["", "## Video yakalama", "| video | " + " | ".join(KOLLAR) + " |", "|---|" + "---|" * len(KOLLAR)]
    for vid in veri:
        L.append(f"| {vid} | " + " | ".join(_pct(metrik([a for a in z["tum"] if a["vid"] == vid],
                                                      {n - min(i for i, a in enumerate(z["tum"]) if a["vid"] == vid) for n in z["esl"] if z["tum"][n]["vid"] == vid})["genel"])
                                            for z in ozet.values()) + " |")
    ad = {"a": "kaynak motora gitmedi (segment/kare/link girdide yok)", "b": "formda alan/kategori yok", "c": "model atladı (girdide + formda yeri vardı)"}
    L += ["", "## Kaçırma sebepleri (kaçırılan yüksek/orta kalem, sonnet)"]
    L += [f"- ({k}) {ad[k]}: {n} · örn. {s0['ornek'][k]}" for k, n in sorted(s0["seb"].items(), key=lambda x: -x[1])]
    L += [f"- (d) sonraki aşama düşürdü (rapor adayı panel birleşiminde yok): {s0['d']}"]
    L += ["", "## Ucuz kollar (kural 21 takası: kur.takas)", "| kol | yakalama düşüşü | tasarruf ($) | ölçütler | öneri |", "|---|---|---|---|---|"]
    for k in ("luna", "qwen"):
        z = ozet[k]
        if not z["n_motor"]:
            L.append(f"| {k} | ölçülemedi | — | — | ölçülemedi |")
            continue
        hata = 100 * sum(v["kollar"][k]["motor"] is None for v in veri.values()) / len(veri)  # 2a kuralı: düşüş = max(yakalama düşüşü, hata oranı)
        dus = max(0.0, 100 * (oran(s0["m"]["genel"]) - oran(z["m"]["genel"])) / (oran(s0["m"]["genel"]) or 1), hata)
        tas = 100 * (1 - z["usd"] / s0["usd"]) if s0["usd"] else 0.0
        ok = all(z["ol_alt"].values())
        L.append(f"| {k} | %{dus:.0f} | %{tas:.0f} | {'GEÇTİ' if ok else 'KALDI'} | {' — '.join(kur.takas(tas, dus, ok))} |")
    L += ["", "## Altın sete ek aday listesi (K3 'dayanıyor'; altın set ölçüm sırasında değiştirilmedi)"]
    for kol in KOLLAR:
        for vid, v in veri.items():
            kv = v["kollar"][kol]
            L += [f"- {kol} · {vid} · [{kv['motor'][int(j)]['bolum']}] {kv['motor'][int(j)]['metin'][:140]}" for j, x in kv.get("k3", {}).items() if x == "dayanıyor"]
    L += ["", "## Dayanmayan kalemler (sonnet)"]
    for vid, v in veri.items():
        kv = v["kollar"]["sonnet"]
        L += [f"- {vid} · [{kv['motor'][int(j)]['bolum']}] {kv['motor'][int(j)]['metin'][:140]}" for j, x in kv.get("k3", {}).items() if x == "dayanmıyor"]
    L += ["", f"Jev: K2 {e['jev']['k2']}/{e['jev']['k2_istenen']} durum · K3 {e['jev']['k3']} · tavan dışı (ölçülemedi) {e['jev']['k3_dusen']} · tavan {JEV_TAVAN}.",
          "Tarama sonucu (video başına): " + " · ".join(f"{k} {vid} {d}" for k in KOLLAR for x in ta.values() if x["pid"].startswith(f"m3b-{k}-")
                                                         for vid, d in x["videolar"].items()),
          "Ölçülemedi (tarama hata/bitmedi, metriğe girmez): " + (" · ".join(f"{k} {vid}" for k in KOLLAR for vid, v in veri.items() if v["kollar"][k]["motor"] is None) or "yok"),
          "Not: sonnet m3b-sonnet-uzun 86HM0RUWhCk ilk koşuda tavanla form_red; motorun kuyruk akışındaki gibi bir kez --form-red-yeniden (+1 çağrı) → tamam.",
          "Tarama: " + " · ".join(f"{k} {x['pid']} {x['videolar']}" for k, x in ta.items()), "Eşleme tabloları: docs/olcumler/m3b-esleme/<id>.md"]
    (REPO / "docs" / "olcumler" / "m3b-altin-olcum.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (ed := REPO / "docs" / "olcumler" / "m3b-esleme").mkdir(exist_ok=True)
    for vid, v in veri.items():
        E = [f"# M3b eşleme — {vid}", "", "Hücre: det|jev · [motor bölümü] motor satırı (kanıt). Bölüm ≠ altın kategori ise kategori farkı notudur.", "",
             "| # | kategori | önem | altın kalem | " + " | ".join(KOLLAR) + " |", "|---|---|---|---|" + "---|" * len(KOLLAR)]
        for i, a in enumerate(v["altin"]):
            h = []
            for kol, kv in v["kollar"].items():
                j, y = (kv["det"][str(i)], "det") if str(i) in kv["det"] else (kv.get("jev", {}).get(str(i)), "jev")
                h.append("—" if j is None else f"{y} · [{kv['motor'][j]['bolum']}] {kv['motor'][j]['metin'][:90]}".replace("|", "\\|"))
            E.append(f"| {i + 1} | {a['kat']} | {a['onem'] or '-'} | {a['metin'][:110].replace('|', chr(92) + '|')} | " + " | ".join(h) + " |")
        (ed / f"{vid}.md").write_text("\n".join(E) + "\n", encoding="utf-8")
    print("rapor: docs/olcumler/m3b-altin-olcum.md")
    for k, z in ozet.items():
        print(f"{k}: yüksek {_pct(z['m']['yuksek'])} · genel {_pct(z['m']['genel'])} · dayanmayan {_pct(z['alt'])}–{_pct(z['ust'])} · sebep {z['seb']} · d {z['d']} · ${z['usd']:.4f}")


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)  # arka plan koşusunda log boş kalmasın (cli.main çıktısı dahil)
    sys.path.insert(0, str(REPO / "tools" / "jev"))
    adim = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    for ad, f in (("tara", tara), ("onar", onar), ("esle", esle), ("rapor", rapor)):
        if adim in (ad, "hepsi"):
            f()
