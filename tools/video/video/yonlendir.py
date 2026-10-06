"""F1: model yönlendirme — adım başı sağlayıcı/model (durum.json "yonlendirme": {adim: {saglayici, model}}); tanımsız adım bugünkü taşıyıcı + d["model"]."""
import base64
import functools
import hashlib
import json
import re
import time
from pathlib import Path

from . import ikinci_goz as ig

OMNI_URL = "http://localhost:20128"  # omni-auth SKILL.md:54-58 (OMNIROUTE_URL varsayılanı)
OMNI_YOL = "/v1/chat/completions"  # omni-inference SKILL.md:283; F1-KURULUM-2 canlı çağrı 200 (5 Eki) — kesin
# F1 eki (Ömer, 5 Eki): model → {"girdi": $/1M, "cikti": $/1M, "kaynak": "<url · tarih>"}; boş başlar, değer tahmin edilmez (F1-KURULUM'da sağlayıcı sayfasından)
_OR = "https://openrouter.ai/api/v1/models · 2026-10-05"  # F1-KURULUM-2: json_schema destekli en ucuz 5 ücretli model; anahtar = OmniRoute model id
_OR6 = "https://openrouter.ai/api/v1/models · 2026-10-06"
CIKTI_TAVAN = 32768  # F3-ELEME: O57 kaçak üretim (max_tokens yok → 131072, ~600 s)
FIYAT = {
    "openrouter/mistralai/mistral-nemo": {"girdi": 0.019, "cikti": 0.03, "kaynak": _OR},  # görselsiz (input_modalities: text) → tarama A/B'ye uygun değil
    "openrouter/inclusionai/ling-3.0-flash-vl": {"girdi": 0.021, "cikti": 0.0616, "kaynak": _OR},
    "openrouter/sao10k/l3-lunaris-8b": {"girdi": 0.04, "cikti": 0.05, "kaynak": _OR},  # görselsiz (input_modalities: text) → tarama A/B'ye uygun değil
    "openrouter/openai/gpt-oss-20b": {"girdi": 0.018, "cikti": 0.09, "kaynak": _OR},  # görselsiz (input_modalities: text) → tarama A/B'ye uygun değil
    # F3-MODEL-2: tek uç Nex AGI (bf16) 0.025/0.1 — canlı usage.cost 0.0043029 = (11440×0.025 + 40169×0.1)/1e6
    "openrouter/nex-agi/nex-n2.5-mini": {"girdi": 0.025, "cikti": 0.1,
                                         "kaynak": "https://openrouter.ai/api/v1/models/nex-agi/nex-n2.5-mini/endpoints + usage.cost (Nex AGI) · 2026-10-05"},
    "openrouter/google/gemma-3-4b-it": {"girdi": 0.05, "cikti": 0.1, "kaynak": _OR},  # F3-HAZIRLIK-2: pricing.prompt/completion token başı × 1e6
    # F3-ELEME: görselli + structured_outputs, sabit kimlik, tahmini çağrı (15k girdi + 6k çıktı) ≤ $0.02; gorsel = pricing.image $/kare
    "openrouter/openai/gpt-6-luna": {"girdi": 0.1, "cikti": 0.5, "kaynak": _OR6},
    "openrouter/cohere/command-a-plus": {"girdi": 0.3, "cikti": 1.5, "kaynak": _OR6},
    "openrouter/qwen/qwen3.7-plus": {"girdi": 0.32, "cikti": 1.28, "kaynak": _OR6},
    "openrouter/mistralai/mistral-large-2512": {"girdi": 0.5, "cikti": 1.5, "kaynak": _OR6},
    "openrouter/google/gemini-3.5-flash-lite": {"girdi": 0.3, "cikti": 2.5, "gorsel": 3e-7, "kaynak": _OR6},
}
MALIYET_BASLIK = "x-omniroute-response-cost"  # openapi.yaml:1173-1176 (USD, 10 ondalık; "0.0000000000" = ücretsiz ya da fiyatsız)


def _usd(model, u, basliklar, kare=0):
    """Yanıt başlığı > 0 ise o; değilse usage × FIYAT (+ kare × gorsel); model FIYAT'ta yoksa None (0 değil — maliyet bilinmiyor).
    prompt_tokens önbellekten okunanı zaten içerir (cached_tokens alt kümesi) → ayrıca eklenmez."""
    try:
        if (m := float(next((v for k, v in basliklar.items() if k.lower() == MALIYET_BASLIK), 0))) > 0:
            return m
    except ValueError:
        pass
    f = FIYAT.get(model)
    return (u.get("prompt_tokens", 0) * f["girdi"] + u.get("completion_tokens", 0) * f["cikti"]) / 1e6 + kare * f.get("gorsel", 0) if f else None


def omni_cagir(model, env, gonder=None, timeout=600, govde_ek=None):
    """hafif.cagir imzasında OmniRoute (OpenAI biçimi) adaptörü → {form, usage, usd, sure, hata}; anahtar yalnız env OMNIROUTE_KEY, hiçbir çıktıya yazılmaz.
    govde_ek istek gövdesine eklenir (F3-ELEME: reasoning); usage.reasoning yalnız yanıtta reasoning token > 0 ise."""
    anahtar = env.get("OMNIROUTE_KEY") or ""
    gonder = gonder or functools.partial(ig._post, basliklar=True, timeout=timeout)

    def cagir(sistem, metin, sema, kareler=(), **_):
        from . import cli  # döngüsel içe aktarma yok
        t0 = time.monotonic()

        def hata(neden, usd=0.0):
            neden = f"ölçülemedi: {neden}"[:200]
            return {"form": None, "usage": {}, "usd": usd, "sure": round(time.monotonic() - t0, 1),
                    "hata": neden.replace(anahtar, "***") if anahtar else neden}
        ekler = [{"type": "image_url", "image_url": {"url": f"data:image/{'png' if str(k).endswith('.png') else 'jpeg'};base64,"
                  + base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
        govde = {"model": model, "max_tokens": CIKTI_TAVAN, "response_format": {"type": "json_schema", "json_schema": {"name": "form", "strict": False, "schema": sema}},
                 "messages": [{"role": "system", "content": sistem},
                              {"role": "user", "content": [{"type": "text", "text": cli._temizle(metin, env)}, *ekler]}], **(govde_ek or {})}
        # Vision Bridge (visionBridge.ts:188) yalnız bizim isteğimizde kapalı: ling'i görselsiz sayıp kareleri 10'a kırpıyordu
        bas = {"Content-Type": "application/json", "x-omniroute-disabled-guardrails": "vision-bridge", **({"Authorization": f"Bearer {anahtar}"} if anahtar else {})}
        try:
            durum, y, *ek = gonder(env.get("OMNIROUTE_URL", OMNI_URL).rstrip("/") + OMNI_YOL, govde, bas)
        except OSError as e:  # sunucu yok / zaman aşımı → adım düşmez, sebep hata alanında
            return hata(f"{type(e).__name__}: {e}", None if isinstance(e, TimeoutError) else 0.0)  # zaman aşımı: upstream faturalamış olabilir
        if durum != 200:
            return hata(f"HTTP {durum} " + json.dumps(y.get("error") or "", ensure_ascii=False))
        u, sec0 = y.get("usage") or {}, (y.get("choices") or [{}])[0]
        ic, kesik = sec0.get("message", {}).get("content") or "", sec0.get("finish_reason") == "length"
        try:
            form = None if kesik else json.loads(ic[ic.find("{"): ic.rfind("}") + 1])
        except ValueError:
            form = None
        akil = (u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
        return {"form": form, "usage": {"input_tokens": u.get("prompt_tokens", 0), "output_tokens": u.get("completion_tokens", 0),
                                        **({"reasoning": akil} if akil else {})},
                "usd": _usd(model, u, ek[0] if ek else {}, len(kareler)), "sure": round(time.monotonic() - t0, 1),
                "hata": f"çıktı tavanı (max_tokens {CIKTI_TAVAN})" if kesik else None if form is not None else "form JSON değil"}
    return cagir


SAGLAYICI = {"omniroute": omni_cagir}
OMNI_MODELLER = "/api/v1/models"  # openapi.yaml:1681 (GET, BearerAuth; data[].id — Model şeması :9091), ücretsiz


def omni_yokla(model, env, getir=ig._post, gorsel=False):
    """F3 ön kontrol (model çağrısından önce): None = sunucu var, kimlik geçer, model listede (gorsel=True: kayıtta capabilities.vision
    ya da input_modalities'te image); değilse hata metni (anahtar yazılmaz)."""
    anahtar = env.get("OMNIROUTE_KEY") or ""
    bas = {"Authorization": f"Bearer {anahtar}"} if anahtar else {}
    try:
        durum, y = getir(env.get("OMNIROUTE_URL", OMNI_URL).rstrip("/") + OMNI_MODELLER, None, bas)[:2]
    except OSError as e:
        neden = f"OmniRoute yok: {type(e).__name__}: {e}"
        return neden.replace(anahtar, "***") if anahtar else neden
    if durum == 401:
        return "OmniRoute 401: kimlik reddedildi (OMNIROUTE_KEY eksik ya da geçersiz)"
    if durum != 200:
        return f"OmniRoute HTTP {durum}"
    kayit = {m.get("id"): m for m in y.get("data") or []}
    if model not in kayit:
        return f"model yok: {model} (listede {len(kayit)} model)"
    k = kayit[model]
    if gorsel and not ((k.get("capabilities") or {}).get("vision") is True or "image" in (k.get("input_modalities") or [])):
        return f"model görsel girdi desteklemiyor: {model}"
    return None


def sec(d, adim, cagir, env, araclar=()):
    """→ (taşıyıcı, model): adım ayarda yoksa ya da araç kullanıyorsa (OmniRoute'a gitmez) verilen taşıyıcı ve d["model"] (bugünkü davranış birebir)."""
    s = None if araclar else (d.get("yonlendirme") or {}).get(adim)
    return (SAGLAYICI[s["saglayici"]](s["model"], env), s["model"]) if s else (cagir, d["model"])


def _a_onbellek(dizin, tas, model, g, i):
    """F3-ELEME: A kolu yanıtı diskte; anahtar = sha256(sistem, metin, şema, kare içerikleri) + model + tekrar sırası. Hatalı yanıt yazılmaz."""
    h = hashlib.sha256()
    for p in (g[0], g[1], json.dumps(g[2], sort_keys=True, ensure_ascii=False)):
        h.update(p.encode() + b"\0")
    for k in g[3] if len(g) > 3 else ():
        h.update(Path(k).read_bytes() + b"\0")
    y = Path(dizin) / f"{h.hexdigest()}-{re.sub(r'[^\w.-]', '_', model)}-{i}.json"
    if y.is_file():
        return json.loads(y.read_text(encoding="utf-8"))
    r = tas(*g[:3], **({"kareler": g[3]} if len(g) > 3 else {}), model=model)
    if not r.get("hata"):
        y.parent.mkdir(parents=True, exist_ok=True)
        y.write_text(json.dumps(r, ensure_ascii=False), encoding="utf-8")
    return r


def ab(d, adim, girdiler, kol_b, cagir, env, puanla, *, basari=None, tekrar=2, tavan, araclar=(), onbellek=None):
    """F2: aynı girdiler (sistem, metin, şema[, kareler]) iki kolda — A = sec(d, adim) bugünkü, B = kol_b; puanla(metinler) kör (GÖREV+YANIT,
    model adı yok); başarı = hata yok + hattın form doğrulaması (parti._denet); gürültü = A tekrar farkı; karar kur.karar (A1 tablosu). usd None kol → SOR;
    tavan < 2×tekrar×girdi → TAVAN, çağrı yok. yonlendirme yalnız AL'de {adim: kol_b}."""
    if araclar:  # araçlı adım OmniRoute'a gitmez (sec) → B kolu kurulamaz; A-A karşılaştırması yapılmaz, çağrı 0
        return {"karar": f"DUR (araç kullanıyor: {adim})", "yonlendirme": None}
    n = 2 * tekrar * len(girdiler)
    if n > tavan:
        return {"karar": f"TAVAN {n} > {tavan}", "yonlendirme": None}
    from . import parti as pt  # parti yonlendir'i içe aktarır; döngü yok
    basari = basari or (lambda y, sema: float(not y.get("hata") and not pt._denet(y.get("form"), sema, "form")))
    kollar = {"a": sec(d, adim, cagir, env), "b": sec({**d, "yonlendirme": {adim: kol_b}}, adim, cagir, env)}
    s, bilinmeyen, yanit = {ad: {"model": m, "ilk_hata": None} for ad, (_, m) in kollar.items()}, [], {}
    gizli = [v for v in (env.get("OMNIROUTE_KEY"), env.get("OPENROUTER_API_KEY")) if v]
    for ad in ("b", "a"):  # önce çağrılar, B önce (nex ~182 s/çağrı): bütün çağrıları hatalı kolda takas da puanla da yok, A çağrılmaz
        tas, model = kollar[ad]
        yanit[ad] = [[_a_onbellek(onbellek, tas, model, g, i) if ad == "a" and onbellek else
                      tas(*g[:3], **({"kareler": g[3]} if len(g) > 3 else {}), model=model) for i in range(tekrar)] for g in girdiler]
        ilk = next((y["hata"] for yg in yanit[ad] for y in yg if y.get("hata")), None)
        for v in gizli:
            ilk = ilk and ilk.replace(v, "***")
        s[ad]["ilk_hata"] = ilk
        if all(y.get("hata") for yg in yanit[ad] for y in yg):
            return {**s, "karar": f"DUR (kol yanıt vermedi: {ad} — {ilk[:120]})", "yonlendirme": None}
    for ad, ys in sorted(yanit.items()):  # puanlama sırası a, b (bugünkü gibi)
        model = s[ad]["model"]
        puan = puanla([f"GÖREV: {g[1]}\nYANIT: {json.dumps(y.get('form'), ensure_ascii=False)}"
                       for g, yg in zip(girdiler, ys) for y in yg])
        puan = [puan[i * tekrar:(i + 1) * tekrar] for i in range(len(girdiler))]
        hepsi = [y for yg in ys for y in yg]
        if any(y.get("usd") is None for y in hepsi):
            bilinmeyen.append(model)
        s[ad] |= {"kalite": sum(map(sum, puan)) / len(hepsi),
                 "gorev": [sum(basari(y, g[2]) for y in yg) / tekrar for g, yg in zip(girdiler, ys)],
                 "girdi": sum((y.get("usage") or {}).get("input_tokens", 0) for y in hepsi),
                 "cikti": sum((y.get("usage") or {}).get("output_tokens", 0) for y in hepsi),
                 "maliyet": sum(y.get("usd") or 0 for y in hepsi), "puan": puan}
        s[ad]["basari"] = sum(s[ad]["gorev"]) / len(girdiler)
    if bilinmeyen:
        return {**s, "karar": f"SOR (maliyet bilinmiyor: {', '.join(bilinmeyen)})", "yonlendirme": None}
    from . import kur
    gurultu = max(max(p) - min(p) for p in s["a"]["puan"])
    k = kur.karar(s["a"], s["b"], None, gurultu, list(zip(s["a"]["gorev"], s["b"]["gorev"])))
    return {**s, "karar": k, "yonlendirme": {adim: kol_b} if k.startswith("AL") else None}


def _tahmin(m, kare):
    """F3-ELEME: aday ilk çağrısının ön tahmini — O58 bandı 15k girdi + 6k çıktı (+ kare × gorsel)."""
    f = FIYAT[m]
    return (15000 * f["girdi"] + 6000 * f["cikti"]) / 1e6 + kare * f.get("gorsel", 0)


def eleme(g, adaylar, a_tas, a_model, env, puanla, *, onbellek, destek=None, b_kur=omni_cagir, yokla=omni_yokla,
          zaman=240, en_fazla=5, tavan_cagri=10, tavan_usd=0.15):
    """F3-ELEME adım 4: tek girdi g (sistem, metin, şema, kareler), adaylar tek koşuda. Ön kontrol (kol sabit · FIYAT · yokla) geçmeyen
    çağrı 0. Aday başı çağrı 1; şema geçerse 2. Sıradaki çağrı B tavanını (çağrı · $; tahmin = adayın son usd'si, yoksa _tahmin) aşacaksa
    yapılmaz → "tavan". usd None (zaman aşımı) harcamaya tahminle girer. supported_parameters'ta reasoning varsa effort minimal istenir.
    Geçen B yoksa A çağrılmaz; A (2 tekrar) _a_onbellek'ten. Puanlama tek puanla çağrısı (A, sonra adaylar; kör). Karar kur.karar
    (çağrı başı ortalamalarla); öneri = AL'ler içinde en yüksek kalite, eşitlikte ucuz."""
    from . import kur, parti as pt
    if len(adaylar) > en_fazla:
        return {"satirlar": [], "oneri": f"TAVAN aday {len(adaylar)} > {en_fazla}", "a_usd": 0.0, "b_usd": 0.0}
    kare = len(g[3]) if len(g) > 3 else 0
    ek = {"kareler": g[3]} if len(g) > 3 else {}
    gecer = lambda y: not y.get("hata") and not pt._denet(y.get("form"), g[2], "form")
    durum, b_usd, cagri = {}, 0.0, 0
    for m in adaylar:
        neden = ("kol sabit değil" if m.startswith("~") or "/~" in m or ":free" in m or "openrouter/free" in m
                 else "fiyat yok" if m not in FIYAT else yokla(m, env, gorsel=bool(kare)))
        x = durum[m] = {"neden": neden, "y": [], "akil": "reasoning" in (destek or {}).get(m, ())}
        if neden:
            continue
        tas = b_kur(m, env, timeout=zaman, govde_ek={"reasoning": {"effort": "minimal"}} if x["akil"] else None)
        while len(x["y"]) < 2 and (not x["y"] or gecer(x["y"][-1])):
            tahmin = (x["y"][-1].get("usd") if x["y"] else None) or _tahmin(m, kare)
            if cagri >= tavan_cagri or b_usd + tahmin > tavan_usd:
                x["tavan"] = True
                break
            y = tas(*g[:3], **ek, model=m)
            cagri, b_usd = cagri + 1, b_usd + (tahmin if y.get("usd") is None else y["usd"])
            x["y"].append(y)
    gecen = {m: [y for y in x["y"] if gecer(y)] for m, x in durum.items()}
    gecen = {m: v for m, v in gecen.items() if v}
    a_usd, ozet, karar = 0.0, {}, {}

    def a_say(*a, **k):
        nonlocal a_usd
        r = a_tas(*a, **k)
        a_usd += r.get("usd") or 0
        return r

    def ozetle(ys, p):
        n = len(ys)
        return {"kalite": sum(p) / len(p), "basari": sum(map(gecer, ys)) / n, "gorev": [sum(map(gecer, ys)) / n],
                "girdi": sum((y.get("usage") or {}).get("input_tokens", 0) for y in ys) / n,
                "cikti": sum((y.get("usage") or {}).get("output_tokens", 0) for y in ys) / n, "maliyet": sum(y.get("usd") or 0 for y in ys) / n}
    oneri = "öneri: yok (geçen aday yok)"
    if gecen:
        ya = [_a_onbellek(onbellek, a_say, a_model, g, i) for i in range(2)]
        if all(y.get("hata") for y in ya):
            oneri = f"öneri: yok (DUR: A yanıt vermedi — {ya[0]['hata'][:120]})"
        else:
            puan = iter(puanla([f"GÖREV: {g[1]}\nYANIT: {json.dumps(y.get('form'), ensure_ascii=False)}"
                                for y in ya + [y for v in gecen.values() for y in v]]))
            pa = [next(puan) for _ in ya]
            sa = ozetle(ya, pa)
            for m, v in gecen.items():
                ozet[m] = ozetle(durum[m]["y"], [next(puan) for _ in v])
                karar[m] = ("SOR (maliyet bilinmiyor)" if any(y.get("usd") is None for y in durum[m]["y"]) else
                            kur.karar(sa, ozet[m], None, max(pa) - min(pa), [(sa["gorev"][0], ozet[m]["gorev"][0])]))
            al = [(ozet[m]["kalite"], -ozet[m]["maliyet"], m) for m, k in karar.items() if k.startswith("AL")]
            oneri = (f"öneri: {max(al)[2]} (kalite {max(al)[0]:.2f} · ${-max(al)[1]:.4f}/çağrı)" if al else
                     "öneri: yok (AL aday yok)")
    gizli = [v for v in (env.get("OMNIROUTE_KEY"), env.get("OPENROUTER_API_KEY")) if v]
    satirlar = []
    for m, x in durum.items():
        ys = x["y"]
        if not ys:
            satirlar.append(f"{m} · hata: {x['neden'] or 'tavan'} · çağrı 0")
            continue
        ilk = next(((y.get("hata") or "şema geçmedi") for y in ys if not gecer(y)), None)
        for v in gizli:
            ilk = ilk and ilk.replace(v, "***")
        t = lambda k: sum((y.get("usage") or {}).get(k, 0) for y in ys)
        usd = [y.get("usd") for y in ys]
        p = [f"{m}", f"hata: {ilk[:120]}" if ilk else "geçti", f"token {t('input_tokens')}/{t('output_tokens')}/{t('reasoning')}",
             "süre " + "+".join(str(y.get("sure")) for y in ys) + " s", "$/çağrı " + ("?" if None in usd else f"{sum(usd) / len(usd):.4f}"),
             *([f"kalite {ozet[m]['kalite']:.2f} · başarı {ozet[m]['basari']:.2f}"] if m in ozet else []), karar.get(m, "ELENDİ")]
        if x["akil"] and t("reasoning") > 0:
            p.append("reasoning parametresi etkisiz")
        if x.get("tavan"):
            p.append("tavan")
        satirlar.append(" · ".join(p))
    return {"satirlar": satirlar, "oneri": oneri, "a_usd": a_usd, "b_usd": b_usd}
