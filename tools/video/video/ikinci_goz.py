"""MOTOR-M5: ikinci göz — Sonnet formu geçtikten sonra aynı paketle luna (OpenRouter); luna'ya özgü kalem yalnız doğrulanırsa rapora girer.
Metin kalemi: URL'leri paket.md'de → dayanıyor, kalan Jev (kesit: segmentler ±60 sn + açıklama bölümünün tamamı).
Kare kalemi: görsel yargıç (hafif Sonnet, en yakın ≤8 kare, video başına tek çağrı). Doğrulanamayan rapor ekinde, panele girmez."""
import base64
import copy
import json
import re
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from . import hafif
from . import tarama as tr

LUNA = "openai/gpt-6-luna-pro"
AD = {"adaylar": "ad", "site_ui": "teknik", "promptlar": "amac", "iddialar": "iddia", "kurulum_komutlar": "komut", "kareden_okunanlar": "kare"}
ETIKET = {"adaylar": "ne", "site_ui": "ne", "promptlar": "metin", "iddialar": "iddia", "kurulum_komutlar": "ne_yapar", "kareden_okunanlar": "okunan"}
EK = "Doğrulanamadı (ikinci göz)"
URL = r"https?://[^\s|)`\"'<>]+"
Q = {"dayanir": {"type": "noul", "instructions": "`kaynak` video altyazısı/açıklamasından bir kesit. `kalem` motorun çıkardığı bilgi. "
                 "Kaynak bu bilgiyi açıkça içeriyor ya da destekliyor mu? Kaynakta olmayan ayrıntı eklenmişse hayır."}}
SISTEM_G = ("Görsel yargıçsın. Ekli kareler bir videodan. Numaralı her kalem için bu bilgi bu karelerde görülüyor mu karar ver: "
            "evet (karede açıkça görülüyor), hayır (karelerde yok ya da çelişiyor), okunamıyor (ilgili kare var ama çözünürlük/bulanıklık yüzünden okunamıyor).")
SEMA_G = {"type": "object", "required": ["kararlar"], "additionalProperties": False, "properties": {"kararlar": {"type": "array", "items": {
    "type": "object", "required": ["no", "karar"], "additionalProperties": False,
    "properties": {"no": {"type": "integer"}, "karar": {"type": "string", "enum": ["evet", "hayır", "okunamıyor"]}}}}}}
KARAR = {"evet": "dayanıyor", "hayır": "dayanmıyor", "okunamıyor": "okunamıyor"}


def url_norm(u):
    u = re.sub(r"^https?://", "", u.strip().lower().rstrip(".,;"))
    return re.split(r"[?#]", re.sub(r"^www\.", "", u))[0].rstrip("/")


def anahtarlar(metin, ad):
    k = {n} if len(n := tr.normal(re.sub(r"\(.*?\)", "", ad))) >= 3 else set()
    k |= {url_norm(u) for u in re.findall(URL, metin)}
    k |= {f"github.com/{r.lower()}" for r in re.findall(r"\(([\w.-]+/[\w.-]+)\)", metin)}
    return k | {n for x in re.findall(r"`([^`]+)`", metin) if len(n := tr.normal(x)) >= 3}


def _post(url, govde, bas, basliklar=False):
    r = urllib.request.Request(url, json.dumps(govde).encode(), bas)
    try:
        with urllib.request.urlopen(r, timeout=600) as y:
            return (y.status, json.loads(y.read())) + ((dict(y.headers.items()),) if basliklar else ())  # F1 eki: OmniRoute maliyet başlığı
    except urllib.error.HTTPError as e:
        try:  # F1: hata gövdesi (ör. 400 invalid_model) sebep olarak korunur
            return e.code, json.loads(e.read())
        except ValueError:
            return e.code, {}


def or_cagir(model, env, gonder=_post, uyku=time.sleep):
    """hafif.cagir imzasında OpenRouter adaptörü → {form, usage, usd, sure, hata}; 429'da ≤2 tekrar, sonra ölçülemedi."""
    def cagir(sistem, metin, sema, kareler=(), model_=None, butce=0.5, timeout=600, env_=None, **_):
        from . import cli  # döngüsel içe aktarma yok
        t0 = time.monotonic()
        ekler = [{"type": "image_url", "image_url": {"url": f"data:image/{'png' if str(k).endswith('.png') else 'jpeg'};base64,"
                  + base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
        govde = {"model": model, "usage": {"include": True},
                 "response_format": {"type": "json_schema", "json_schema": {"name": "form", "strict": False, "schema": sema}},
                 "messages": [{"role": "system", "content": sistem},
                              {"role": "user", "content": [{"type": "text", "text": cli._temizle(metin, env)}, *ekler]}]}
        bas = {"Authorization": f"Bearer {env.get('OPENROUTER_API_KEY', '')}", "Content-Type": "application/json"}
        for i in range(3):
            durum, y = gonder(cli.OR_URL, govde, bas)
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


def _ks(x):
    z = re.search(r"(\d+):(\d{2})", str(x or ""))
    return int(z[1]) * 60 + int(z[2]) if z else None


def _duz(k):
    return " · ".join(str(x) for x in k.values() if x not in (None, ""))


def kalemler(f):
    return [(b, k, anahtarlar(_duz(k), str(k.get(a) or ""))) for b, a in AD.items() for k in (f.get(b) or []) if isinstance(k, dict)]


def ozgu(fs, fl):
    """M4c kuralı: luna kalemi, anahtarları Sonnet kalemlerinin anahtar birleşimiyle kesişmiyorsa özgü."""
    s = set().union(*(k for _, _, k in kalemler(fs)))
    return [(b, k) for b, k, a in kalemler(fl) if not a & s]


def kesit(k, metin):
    """Jev kaynağı: kalem zamanı ±60 sn segmentleri (zamansızsa sözcük örtüşmesi en iyi 2) + açıklama bölümünün TAMAMI (kesme yok)."""
    seg = [s for s in tr.bolum(metin, "Segmentler").splitlines() if s.startswith("[")]
    if (z := _ks(k.get("kanit_zamani"))) is not None:
        sec = [s for s in seg if (t := _ks(s)) is not None and abs(t - z) <= 60]
    else:
        w = set(re.findall(r"\w{3,}", _duz(k).casefold()))
        sec = sorted(seg, key=lambda s: -len(w & set(re.findall(r"\w{3,}", s.casefold()))))[:2]
    return "\n".join(sec) + "\n" + tr.bolum(metin, "Açıklama bağlantıları")


def _satir(adim, v, **k):
    return {"zaman": datetime.now().isoformat(timespec="seconds"), "adim": adim, "videolar": [v], "girdi": 0, "onb_okuma": 0,
            "onb_yazma": 0, "cikti": 0, "usd": 0.0, **k}


def gorsel(kal, p, yargic, env, butce=.05):
    """Kare kalemleri → ([karar], çağrı sonucu | None); kare yoksa çağrı yok."""
    kz = [(k, t) for k, t in zip(p["kareler"], p.get("kare_zaman") or []) if Path(k).is_file()]
    zs = [_ks(k.get("kanit_zamani")) for _, k in kal]
    sec = {min(kz, key=lambda x: abs((x[1] or 0) - z))[0] for z in zs if z is not None} if kz else set()
    sec = sorted(sec | ({k for k, _ in kz} if None in zs else set()))[:8]
    if not sec:
        return ["kare yok"] * len(kal), None
    y = yargic(SISTEM_G, "Kalemler:\n" + "\n".join(f"{i + 1}. [{b}] {_duz(k)}" for i, (b, k) in enumerate(kal)), SEMA_G,
               kareler=sec, model=hafif.MODEL, butce=butce, env=env)
    k = {x.get("no"): x.get("karar") for x in ((y.get("form") or {}).get("kararlar") or []) if isinstance(x, dict)}
    return [KARAR.get(k.get(i + 1), "ölçülemedi") for i in range(len(kal))], y


def uygula(v, f, p, luna, jev, yargic, env, kalan, denet, yaz):
    """luna(butce) → çağrı sonucu; kalan: parti tavanından kalan {or_usd, jev, yargic}; denet(form) → hata listesi; yaz(defter satırı).
    → (form, ek {eklenen, dogrulanamadi, not, usd})."""
    ek = {"eklenen": [], "dogrulanamadi": [], "not": [], "usd": 0.0}
    if kalan["or_usd"] <= 0:
        ek["not"].append("ikinci göz: tavan (OpenRouter $) — luna çağrılmadı, Sonnet sonucu")
        return f, ek
    fl, hata = None, None
    for _ in range(2):  # video başına ≤2 luna çağrısı
        if kalan["or_usd"] - ek["usd"] <= 0:
            break
        y = luna(round(kalan["or_usd"] - ek["usd"], 4))
        ek["usd"] += y.get("usd") or 0.0
        fl = next((x for x in (y.get("form") or {}).get("videolar") or [] if isinstance(x, dict) and x.get("id") == v), None) if not y.get("hata") else None
        hata = y.get("hata") or (None if fl else "formda video yok")
        u = y.get("usage") or {}
        yaz(_satir("ikinci_goz_luna", v, model=LUNA, girdi=u.get("input_tokens", 0), cikti=u.get("output_tokens", 0), sure=y.get("sure"),
                   usd=y.get("usd") or 0.0, form=f"hata: {hata}" if hata else "gecti"))
        if fl:
            break
    if not fl:
        ek["not"].append(f"ikinci göz: luna hatası ({hata}) — Sonnet sonucu")
        return f, ek
    oz = ozgu(f, fl)
    kare = [(b, k) for b, k in oz if b == "kareden_okunanlar" or k.get("kaynak") == "kare"]
    metin = [x for x in oz if x not in kare]
    karar = {}
    pu = {url_norm(x) for x in re.findall(URL, p["metin"])}
    for i, (b, k) in enumerate(metin):
        if (u := {url_norm(x) for x in re.findall(URL, _duz(k))}) and u <= pu:
            karar[("m", i)] = "dayanıyor"
    sor = [i for i in range(len(metin)) if ("m", i) not in karar]
    for i in sor[max(0, kalan["jev"]):]:
        karar[("m", i)] = "Jev tavanı"
    if sor := sor[:max(0, kalan["jev"])]:
        try:
            r = jev([f"kalem:\n[{metin[i][0]}] {_duz(metin[i][1])[:400]}\n\nkaynak:\n{kesit(metin[i][1], p['metin'])}" for i in sor], Q)
        except Exception as e:  # Jev kesintisi: kalem doğrulanamadı, video düşmez
            r, ek["not"] = [None] * len(sor), [*ek["not"], f"ikinci göz: Jev hatası ({e})"[:200]]
        yaz(_satir("ikinci_goz_jev", v, model="jev", durum=len(sor)))
        for i, x in zip(sor, r):
            s = ((x or {}).get("dayanir") or {}).get("noul")
            karar[("m", i)] = "ölçülemedi" if s is None else "dayanıyor" if s >= .5 else "dayanmıyor"
    if kare and kalan["yargic"] > 0:
        et, y = gorsel(kare, p, yargic, env)
        if y is not None:
            u = y.get("usage") or {}
            yaz(_satir("ikinci_goz_yargic", v, model=hafif.MODEL, girdi=u.get("input_tokens", 0), cikti=u.get("output_tokens", 0),
                       sure=y.get("sure"), usd=y.get("usd") or 0.0, form=f"hata: {y['hata']}" if y.get("hata") else "gecti"))
        karar.update({("k", i): x for i, x in enumerate(et)})
    else:
        karar.update({("k", i): "yargıç tavanı" for i in range(len(kare))})
    f = copy.deepcopy(f)
    for anah, (b, k) in [*((("m", i), x) for i, x in enumerate(metin)), *((("k", i), x) for i, x in enumerate(kare))]:
        if (x := karar[anah]) != "dayanıyor":
            ek["dogrulanamadi"].append([b, _duz(k), x])
            continue
        k = dict(k)
        k[ETIKET[b]] = f"{k.get(ETIKET[b]) or ''} (ikinci göz)".strip()
        deneme = copy.deepcopy(f)
        deneme.setdefault(b, []).append(k)
        if h := denet(deneme):
            ek["dogrulanamadi"].append([b, _duz(k), f"denetim: {h[0]}"[:160]])
            continue
        f = deneme
        ek["eklenen"].append([b, _duz(k)])
    return f, ek


def ozet(ek):
    return {"eklenen": len(ek.get("eklenen", [])), "dogrulanamadi": len(ek.get("dogrulanamadi", [])), "usd": round(ek.get("usd", 0.0), 5)}


def ek_md(ek):
    """Rapor sonuna: not satırları + özet + doğrulanamayanlar (düz madde, 'aday: evet' yok → panel/ayikla almaz)."""
    L = list(ek.get("not", []))
    if ek.get("eklenen") or ek.get("dogrulanamadi"):
        L.append(f"ikinci göz: luna · eklenen {len(ek['eklenen'])} · doğrulanamadı {len(ek['dogrulanamadi'])} · ${ek['usd']:.4f}")
    if ek.get("dogrulanamadi"):
        L += [f"## {EK}", *[f"- [{b}] {re.sub(r'\s+', ' ', m)} — {s}" for b, m, s in ek["dogrulanamadi"]]]
    return "\n".join(L) + "\n" if L else ""
