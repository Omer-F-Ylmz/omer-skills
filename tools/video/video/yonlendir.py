"""F1: model yönlendirme — adım başı sağlayıcı/model (durum.json "yonlendirme": {adim: {saglayici, model}}); tanımsız adım bugünkü taşıyıcı + d["model"]."""
import base64
import bisect
import functools
import hashlib
import json
import random
import re
import subprocess
import tempfile
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
    # F3-V7a: onbellek = pricing.input_cache_read $/1M (aynı GET, 2026-10-06)
    "openrouter/google/gemini-3.5-flash-lite": {"girdi": 0.3, "cikti": 2.5, "gorsel": 3e-7, "onbellek": 0.03, "kaynak": _OR6},
    # F3-VARYANT REF: aynı aile bir üst (flash; image + structured_outputs + reasoning). 3.5-flash 1.5/9 → ~40k+3k çağrı ~$0.085 > $0.05;
    # 3.8-flash 0.75/3.75 → ~$0.04
    "openrouter/google/gemini-3.8-flash": {"girdi": 0.75, "cikti": 3.75, "gorsel": 7.5e-7, "onbellek": 0.075, "kaynak": "https://openrouter.ai/api/v1/models · 2026-10-06"},
}
MALIYET_BASLIK = "x-omniroute-response-cost"  # openapi.yaml:1173-1176 (USD, 10 ondalık; "0.0000000000" = ücretsiz ya da fiyatsız)


def _usd(model, u, basliklar, kare=0):
    """Yanıt başlığı > 0 ise o; değilse usage × FIYAT (+ kare × gorsel); model FIYAT'ta yoksa None (0 değil — maliyet bilinmiyor).
    prompt_tokens önbellekten okunanı zaten içerir (cached_tokens alt kümesi) → ayrıca eklenmez; F3-V7a: o kısım onbellek fiyatıyla (yoksa girdi)."""
    try:
        if (m := float(next((v for k, v in basliklar.items() if k.lower() == MALIYET_BASLIK), 0))) > 0:
            return m
    except ValueError:
        pass
    if not (f := FIYAT.get(model)):
        return None
    c = (u.get("prompt_tokens_details") or {}).get("cached_tokens") or 0
    return ((u.get("prompt_tokens", 0) - c) * f["girdi"] + c * f.get("onbellek", f["girdi"])
            + u.get("completion_tokens", 0) * f["cikti"]) / 1e6 + kare * f.get("gorsel", 0)


def omni_cagir(model, env, gonder=None, timeout=600, govde_ek=None, uyku=time.sleep):
    """hafif.cagir imzasında OmniRoute (OpenAI biçimi) adaptörü → {form, usage, usd, sure, hata}; anahtar yalnız env OMNIROUTE_KEY, hiçbir çıktıya yazılmaz.
    govde_ek istek gövdesine eklenir (F3-ELEME: reasoning); usage.reasoning yalnız yanıtta reasoning token > 0 ise."""
    anahtar = env.get("OMNIROUTE_KEY") or ""
    gonder = gonder or functools.partial(ig._post, basliklar=True, timeout=timeout)

    def cagir(sistem, metin, sema, kareler=(), **_):
        from . import cli  # döngüsel içe aktarma yok
        t0 = time.monotonic()

        def hata(neden, usd=0.0):
            neden = f"ölçülemedi: {neden}"[:200]
            return {"form": None, "usage": {}, "usd": usd, "sure": round(time.monotonic() - t0, 1), "yeniden": n,
                    "hata": neden.replace(anahtar, "***") if anahtar else neden}
        ekler = [{"type": "image_url", "image_url": {"url": f"data:image/{'png' if str(k).endswith('.png') else 'jpeg'};base64,"
                  + base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
        govde = {"model": model, "max_tokens": CIKTI_TAVAN, "response_format": {"type": "json_schema", "json_schema": {"name": "form", "strict": False, "schema": sema}},
                 "messages": [{"role": "system", "content": sistem},
                              {"role": "user", "content": [{"type": "text", "text": cli._temizle(metin, env)}, *ekler]}], **(govde_ek or {})}
        # Vision Bridge (visionBridge.ts:188) yalnız bizim isteğimizde kapalı: ling'i görselsiz sayıp kareleri 10'a kırpıyordu
        bas = {"Content-Type": "application/json", "x-omniroute-disabled-guardrails": "vision-bridge", **({"Authorization": f"Bearer {anahtar}"} if anahtar else {})}
        n = 0
        while True:  # F3-V5b: kabul reddi (503 chat_admission_busy, upstream'e gitmez) ≤ 3 kez yeniden
            try:
                durum, y, *ek = gonder(env.get("OMNIROUTE_URL", OMNI_URL).rstrip("/") + OMNI_YOL, govde, bas)
            except OSError as e:  # sunucu yok / zaman aşımı → adım düşmez, sebep hata alanında
                return hata(f"{type(e).__name__}: {e}", None if isinstance(e, TimeoutError) else 0.0)  # zaman aşımı: upstream faturalamış olabilir
            ra = next((v for a, v in (ek[0] if ek else {}).items() if a.lower() == "retry-after"), None)
            if durum not in (429, 503) or n == 3 or not (ra or re.search("admission|Retry", json.dumps(y))):
                break
            n += 1
            try:
                bekle = min(float(ra), 15)
            except (TypeError, ValueError):
                bekle = 2 ** n + random.uniform(0, 0.5)
            uyku(bekle)
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
                                        **({"reasoning": akil} if akil else {}),  # F3-V7a: cached yalnız sağlayıcı bildirdiyse
                                        **({"cached": c} if (c := (u.get("prompt_tokens_details") or {}).get("cached_tokens")) is not None else {})},
                "usd": _usd(model, u, ek[0] if ek else {}, len(kareler)), "sure": round(time.monotonic() - t0, 1), "yeniden": n,
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
                 "girdi": sum(_girdi(y.get("usage") or {}) for y in hepsi),
                 "cikti": sum((y.get("usage") or {}).get("output_tokens", 0) for y in hepsi),
                 "maliyet": sum(y.get("usd") or 0 for y in hepsi), "puan": puan}
        s[ad]["basari"] = sum(s[ad]["gorev"]) / len(girdiler)
    if bilinmeyen:
        return {**s, "karar": f"SOR (maliyet bilinmiyor: {', '.join(bilinmeyen)})", "yonlendirme": None}
    from . import kur
    gurultu = max(max(p) - min(p) for p in s["a"]["puan"])
    k = kur.karar(s["a"], s["b"], None, gurultu, list(zip(s["a"]["gorev"], s["b"]["gorev"])))
    return {**s, "karar": k, "yonlendirme": {adim: kol_b} if k.startswith("AL") else None}


VARYANT = {"V0": "temel (bugünkü)", "V1": "tek örnek: sistem mesajına başka bir videonun Claude tarama formu",
           "V3": "akıl yürütme düşük (reasoning effort low; supported_parameters'ta yoksa çağrı 0)",
           "V4": "düşük çözünürlük: kareler aynı, uzun kenar 512 px (yalnız istek gövdesinde; dosyalar değişmez)",
           "V2": "V0 + EKSİKSİZLİK KURALI + DEĞERLENDİR LİSTESİ (paket metninden mekanik ön çıkarım; model çağrısı yok)",
           "V21": "V2 + örnek form (ELEME_ORNEK21; test videosundan olamaz)",
           "V5": "V21 sistemi + bolumle(k=3): parçalar paralel, formlar birlestir ile tek yanıt",
           "V54": "V5, k=4",
           "V6": "V54 + ELEME_ORNEK6 (6 liste dolu) · sabit sistem öneki · yük dengeli bolumle · bolumler paketten · son geçiş (özet + eksik)",
           "V63": "V6, k=3"}
PARCA = {"V5": 3, "V54": 4, "V6": 4, "V63": 3}  # F3-V5: parça sayısı (tavanlar parça çağrısını sayar)
SON = ("V6", "V63")  # F3-V6: parça + son geçiş (çağrı k + 1)
DEGERLENDIR = "DEĞERLENDİR LİSTESİ (paket metninden mekanik çıkarım):\n"
PARCA_BOLUM = "bolumler: boş bırak ([]); bölümler paketten doldurulur."
PARCA_LINK = "aciklama_baglantilari: boş bırak ([]); bağlantılar yalnız 1. parçada istenir."
SON_LISTE = ("adaylar", "iddialar", "kurulum_komutlar", "promptlar", "site_ui")
SON_SISTEM = ("Bir videonun paket metni (konuşma + ekran metni) ve parça parça çıkarılmış formun anahtar satırları verilir. ozet: tüm videoyu "
              "kapsayan tek bütünlüklü özet. ek_* listelerine yalnız anahtar satırlarda OLMAYAN öğeleri yaz (öğe biçimi ana formdakiyle aynı); "
              "emin değilsen belirsizlikler'e yaz.")
PARALEL_TAVAN = 1  # F3-V5b: OmniRoute OMNIROUTE_CHAT_MAX_HEAVY_IN_FLIGHT varsayılanı (büyük gövde > 256 KiB); fazlası 503 chat_admission_busy
ORNEK_BASLIK = "\n\nÖRNEK ÇIKTI (başka bir videonun onaylı formu; yalnız biçim ve ayrıntı düzeyi için, içeriğini kopyalama):\n"


EKSIKSIZLIK = ("EKSİKSİZLİK KURALI: Videoda adı geçen, ekranda görünen ya da anlatılan HER araç, kütüphane, servis, model, skill, teknik, "
               "yöntem ve kavram adaylar[]'da AYRI öğedir; birleştirme, özetleme, sayı sınırı yok. Emin değilsen ekle ve belirsizlikler[]'e yaz. "
               "Ekrandaki her anlamlı metin (komut, prompt, ayar, başlık, kod) kareden_okunanlar[]'a kare numarasıyla ayrı öğe. Ekranda görünen "
               "ya da söylenen her prompt promptlar[]'a kelimesi kelimesine. Her kurulum komutu kurulum_komutlar[]'a birebir. Her iddiada "
               "aday_adi doldur. Kısa yazma; her öğede kanıt ve zaman ver. DEĞERLENDİR LİSTESİ'ndeki her öğeyi ya forma ekle ya da neden "
               "eklemediğini belirsizlikler[]'e tek satırla yaz.")
ON_TAVAN = 1500  # F3-V2: DEĞERLENDİR LİSTESİ token tavanı (~4 karakter/token)
_KOMUT = re.compile(r"\b(?:npm|npx|pip3?|uvx?|brew|winget|git clone|claude (?:mcp|plugin|skills?))\s[^\n,;`]{1,100}")


def on_cikarim(metin):
    """F3-V2 mekanik ön çıkarım (model çağrısı yok): url · GitHub owner/repo · kurulum komutu · `kod` · kare OCR satırı (paket
    "## Ekran metni (OCR)", [m:ss] ile; gürültü paket yazılırken süzülür) · büyük harfle başlayan ad (cümle başı değil). Tekil,
    öncelik bu sırayla, ON_TAVAN'da kesilir."""
    kare, ocr, ad = [], False, []
    for s in metin.splitlines():
        if s.startswith(("#", "===")):
            ocr = s.startswith("## Ekran metni (OCR)")
            continue
        if ocr and re.match(r"\[[\d:]+\] ", s):
            kare.append(s.strip())
        for c in re.split(r"(?<=[.!?:])\s+", re.sub(r"^\[[\d:]+\]\s*|https?://\S+", " ", s).strip()):
            ad += [w for w in (x.rstrip(".-+") for x in re.findall(r"\w[\w.+-]*", c)[1:]) if len(w) >= 3 and w[0].isupper()]
    oge = ([f"url: {u.rstrip('.,;:')}" for u in re.findall(r"https?://[^\s<>\"'`)\]]+", metin)]
           + [f"repo: {r.strip('.')}" for r in re.findall(r"github\.com/([\w.-]+/[\w.-]+)", metin)]
           + [f"komut: {k.strip(' .')}" for k in _KOMUT.findall(metin)] + [f"kod: {k}" for k in re.findall(r"`([^`\n]{2,80})`", metin)]
           + [f"kare: {k}" for k in kare] + [f"ad: {w}" for w in ad])
    out, n = [], 0
    for x in dict.fromkeys(oge):
        n += len(x) + 1
        if n > ON_TAVAN * 4:
            break
        out.append(x)
    return "\n".join(out)


def ornek_sec(yollar, haric=("b2QkhmQ0sT0",)):
    """F3-V2 V21 örneği: OLCUM listelerinin hepsi dolu en kısa Claude video formu (haric id'ler dışında); yoksa None."""
    uy = []
    for y in map(Path, yollar):
        t = y.read_text(encoding="utf-8")
        if y.stem not in haric and all(json.loads(t).get(x) for x in ("adaylar", "promptlar", "kurulum_komutlar", "kareden_okunanlar")):  # F3-ÖLÇÜM-4: örnek değişmez
            uy.append((len(t), str(y), y))
    return min(uy)[2] if uy else None


def ornek_sec6(yollar, haric=("b2QkhmQ0sT0",)):
    """F3-V6 örneği: OLCUM'un 6 listesi dolu en kısa Claude video formu; yoksa en çok listesi dolu olan. → (yol, eksik listeler) ya da (None, [])."""
    uy = []
    for y in map(Path, yollar):
        t = y.read_text(encoding="utf-8")
        if y.stem not in haric:
            eksik = [x for x in OLCUM if not json.loads(t).get(x)]
            uy.append((len(eksik), len(t), str(y), y, eksik))
    return min(uy)[3:] if uy else (None, [])


def _girdi(u):
    """A (Claude) girdisinin çoğu önbellekte → input + cache_read + cache_creation (OpenAI biçiminde yalnız input_tokens var)."""
    return sum(u.get(k, 0) for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))


def _kucult(kareler, dizin):
    """F3-VARYANT V4: uzun kenar 512 px (küçük kare büyütülmez) → dizin/<ad>; asıl dosyalar değişmez."""
    Path(dizin).mkdir(parents=True, exist_ok=True)
    cik = [Path(dizin) / Path(k).name for k in kareler]
    for k, y in zip(kareler, cik):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(k), "-vf",
                        "scale='min(512,iw)':'min(512,ih)':force_original_aspect_ratio=decrease", str(y)], check=True, timeout=60)
    return cik


def _olc(x, yol, o, bos):
    if isinstance(x, dict):
        for k, v in x.items():
            _olc(v, f"{yol}.{k}" if yol else k, o, bos)
        return
    bos[0] += x is None or x == "" or x == []
    o[yol] = o.get(yol, 0) + (len(x) if isinstance(x, (str, list)) else x is not None)
    for v in x if isinstance(x, list) else ():
        _olc(v, yol + "[]", o, bos)


def _sema_yol(s, yol=""):
    for k, v in (s.get("properties") or {}).items():
        p = f"{yol}.{k}" if yol else k
        yield p
        yield from _sema_yol(v.get("items") or {}, p + "[]") if "items" in v else _sema_yol(v, p)


def alan_farki(a_formlar, b_formlar, sema):
    """F3-VARYANT: alan alan A'ya göre — ölçü: metin uzunluğu · liste uzunluğu · var 1 (form başı ortalama, liste öğeleri toplanır);
    boş alan (None/""/[]) sayısı, şemada olup B yanıtında olmayan yollar; fark = |A−B| / max(A, B, 1). → {ozet, satirlar (md tablo)}."""
    def ort(formlar):
        o, bos = {}, [0]
        for f in formlar:
            _olc(f, "", o, bos)
        n = max(len(formlar), 1)
        return {k: v / n for k, v in o.items()}, bos[0] / n
    a, ba = ort(a_formlar)
    b, bb = ort(b_formlar)
    sira = sorted(((abs(a.get(y, 0) - b.get(y, 0)) / max(a.get(y, 0), b.get(y, 0), 1), abs(a.get(y, 0) - b.get(y, 0)), y)
                   for y in set(a) | set(b)), key=lambda t: (-t[0], -t[1], t[2]))
    eksik = sorted(set(_sema_yol(sema)) - set(b))
    return {"ozet": f"boş alan A {ba:.1f} → B {bb:.1f} · şemada yok: {', '.join(eksik) or 'yok'} · en çok fark: "
                    + ", ".join(f"{y} {a.get(y, 0):.1f}→{b.get(y, 0):.1f}" for _, _, y in sira[:5]),
            "satirlar": [f"| {y} | {a.get(y, 0):.1f} | {b.get(y, 0):.1f} | {f * 100:.0f} |" for f, _, y in sira]}


OLCUM = {"adaylar": ("ad", 0.40), "site_ui": ("ne teknik", 0.15), "promptlar": ("metin", 0.15), "iddialar": ("iddia", 0.10),
         "kurulum_komutlar": ("komut", 0.10), "kareden_okunanlar": ("okunan", 0.10)}  # F3-ÖLÇÜM-4: site_ui anahtarı ne + teknik
DAYANAK = {"dayanaklı": "konuşmada var", "doğrulanamadı": "yalnız kare", "dayanaksız": "dayanaksız"}


def _n(s):
    from .tarama import normal
    return normal(s or "")


def _kelime(s):
    return {w for w in map(_n, (s or "").split()) if w}


def _k(o, k):
    """F3-ÖLÇÜM-4: öğe anahtarı — boşlukla ayrılmış alanlar birleşir (site_ui: ne + teknik)."""
    return " ".join(str(o.get(p) or "") for p in k.split()).strip()


ANLAM_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"  # F3-ÖLÇÜM-4: fastembed ONNX-Q, Apache-2.0, ~225 MB
ANLAM_ESIK = 0.6  # kalibrasyon: test_f3_kare _AYNI ≥ eşik · _FARKLI < eşik
ANLAMSAL = True
ANLAM_LISTE = ("adaylar", "iddialar", "site_ui", "promptlar", "kareden_okunanlar")
DAYANAK_ESIK = 0.37  # F3-V7a: cümle dayanağı (TR iddia ↔ EN pencere); kalibrasyon test_f3_v5 _IDDIA: aynı ≥ 0.396 · ilgisiz ≤ 0.343
DAYANAK_LISTE = ("iddialar", "site_ui", "promptlar")  # kısa ad/terim (adaylar, kareden_okunanlar) ANLAM_ESIK'te kalır
_VEK = {}


@functools.cache
def _model():
    """F3-ÖLÇÜM-4: yerel çok dilli embedding (ilk kullanımda indirilir, .video-cache/emb); yüklenemezse None → bugünkü kurallar."""
    try:
        from fastembed import TextEmbedding
        from .cli import KOK
    except Exception:
        return None
    for yerel in (True, False):  # önce önbellek (ağsız), yoksa tek indirme
        try:
            return TextEmbedding(ANLAM_MODEL, cache_dir=str(Path(KOK) / "emb"), local_files_only=yerel)
        except Exception:
            pass
    return None


def _acik():
    return ANLAMSAL and _model() is not None


def _vek(ms):
    import numpy as np
    yeni = [m for m in dict.fromkeys(ms) if m not in _VEK]
    for m, v in zip(yeni, _model().embed(yeni) if yeni else ()):
        _VEK[m] = v / (np.linalg.norm(v) or 1)
    return np.array([_VEK[m] for m in ms])


def _benzerlik(a, b):
    """F3-ÖLÇÜM-4: kosinüs benzerliği (anlamsal kapalıysa 0)."""
    if not (_acik() and a and b):
        return 0.0
    x = _vek([a, b])
    return float(x[0] @ x[1])


@functools.lru_cache(maxsize=4)
def _pencereler(metin):
    """F3-ÖLÇÜM-4: paket metni (konuşma + OCR) ~3 cümlelik örtüşmeli pencereler (adım 2) → vektör matrisi."""
    c = [s for s in re.split(r"(?<=[.!?])\s+|\n+", metin) if s.strip()]
    return _vek([" ".join(c[i:i + 3]) for i in range(0, max(len(c) - 2, 1), 2)]) if c else None


def eslesir(liste, a, b):
    """F3-ÖLÇÜM v2 (plan O61): iki anahtar aynı öğe mi — adaylar tr.normal karşılıklı içerme ya da kelime Jaccard ≥ 0.6 ·
    kurulum_komutlar boşluk normalize içerme · aciklama_baglantilari birebir · promptlar/kareden_okunanlar kelime örtüşmesi
    (ortak / kısa olanın kelimesi) ≥ 0.5. Eleme'den bağımsız (B hattı süzgeci). F3-ÖLÇÜM-4: ANLAM_LISTE'de ya da anlamsal
    benzerlik ≥ ANLAM_ESIK."""
    if liste in ANLAM_LISTE and _benzerlik(a, b) >= ANLAM_ESIK:
        return True
    if liste == "adaylar":
        na, nb, ka, kb = _n(a), _n(b), _kelime(a), _kelime(b)
        return bool(na and nb and (na in nb or nb in na)) or bool(ka | kb) and len(ka & kb) / len(ka | kb) >= 0.6
    if liste == "kurulum_komutlar":
        na, nb = " ".join((a or "").split()), " ".join((b or "").split())
        return bool(na and nb) and (na in nb or nb in na)
    if liste == "aciklama_baglantilari":
        return bool(a) and a == b
    ka, kb = _kelime(a), _kelime(b)
    return bool(ka and kb) and len(ka & kb) / min(len(ka), len(kb)) >= 0.5


DURAK = {"ile", "veya", "icin", "için", "gibi", "ama", "ancak", "the", "and", "for", "with", "from", "into", "via", "but"}  # F3-V2 bağlaç


def _ayirt(s):
    """F3-V2: parantez içi atılır; ayırt edici kelimeler (≥ 3 harf, DURAK dışı)."""
    return [w for w in re.findall(r"\w+", re.sub(r"\([^)]*\)", " ", s).casefold()) if len(w) >= 3 and w not in DURAK]


def dayanak(liste, oge, metin):
    """F3-ÖLÇÜM v2: anahtar paket metninde (konuşma + açıklama + bölümler + kare OCR) → dayanaklı (adaylar tr.normal içerme ·
    komut boşluk normalize içerme · metin/okunan kelimelerinin ≥ yarısı); değil ama kaynak kare / karede_gorulen dolu /
    kareden_okunanlar → doğrulanamadı (cezasız); ikisi de değil → dayanaksız."""
    k = _k(oge, OLCUM[liste][0])
    if liste == "adaylar":
        w, m = _ayirt(k), {x[:5] for x in re.findall(r"\w+", metin.casefold())}  # F3-V2: ya da kelimelerin ≥ yarısı 5 harf önekle
        var = bool(_n(k)) and _n(k) in _n(metin) or bool(w) and 2 * sum(x[:5] in m for x in w) >= len(w)
    elif liste == "kurulum_komutlar":
        var = bool(k.split()) and " ".join(k.split()) in " ".join(metin.split())
    else:
        w = _kelime(k)
        var = bool(w) and len(w & _kelime(metin)) / len(w) >= 0.5
    if not var and liste in ANLAM_LISTE and k and _acik() and (p := _pencereler(metin)) is not None:
        var = float((p @ _vek([k])[0]).max()) >= (DAYANAK_ESIK if liste in DAYANAK_LISTE else ANLAM_ESIK)  # F3-ÖLÇÜM-4: anlamsal dayanak (en yakın pencere)
    return ("dayanaklı" if var else "doğrulanamadı" if liste == "kareden_okunanlar" or oge.get("kaynak") == "kare"
            or (oge.get("karede_gorulen") or "").strip() else "dayanaksız")


def _ogeler(form, x):
    """F3-ÖLÇÜM-3: gerçek formda listeler videolar[] altında — öğeye video id'si (_v) eklenir; eşleşme ve D aynı video içinde."""
    return [{**o, "_v": v.get("id")} for v in (form or {}).get("videolar") or () if isinstance(v, dict)
            for o in v.get(x) or () if isinstance(o, dict)]


def _dolu(x):
    """F3-ÖLÇÜM-3 boş ölçüm korkuluğu: formun herhangi bir derinliğinde dolu bir OLCUM listesi var mı."""
    if isinstance(x, dict):
        return any(k in OLCUM and v or _dolu(v) for k, v in x.items())
    return isinstance(x, list) and any(map(_dolu, x))


def referans(a_formlar, formlar, metin):
    """F3-ÖLÇÜM v2: D = A formlarının tüm öğeleri ∪ formlar'ın dayanaklı öğeleri (liste başı, aynı video içinde eslesir ile tekil;
    B > A mümkün)."""
    d = {x: [] for x in OLCUM}
    if _acik():  # F3-ÖLÇÜM-4: tüm anahtarlar tek toplu embedding
        _vek([_k(o, k) for f in (*a_formlar, *formlar) for x, (k, _) in OLCUM.items() for o in _ogeler(f, x) if _k(o, k)])
    for f, a_mi in [(f, True) for f in a_formlar] + [(f, False) for f in formlar]:
        for x, (k, _) in OLCUM.items():
            for o in _ogeler(f, x):
                if _k(o, k) and (a_mi or dayanak(x, o, metin) == "dayanaklı") and \
                        not any(r["_v"] == o["_v"] and eslesir(x, _k(o, k), _k(r, k)) for r in d[x]):
                    d[x].append(o)
    return d


def olc_v2(form, d, metin):
    """F3-ÖLÇÜM v2 form başı: liste başı n · kapsam (D'den bulunan / |D|; D boşsa None) · doğruluk (dayanaklı / dayanaklı +
    dayanaksız; payda 0 → 1) · doğrulanamadı · bulunan (D sırası) + url sayısı (skora girmez); kapsam/doğruluk/F1 OLCUM
    ağırlıklı, yalnız D'si dolu listeler (ağırlık oranla); D hiç yoksa 1 (görev = şema başarısı)."""
    r, top = {"liste": {}, "url": len(_ogeler(form, "aciklama_baglantilari"))}, {"kapsam": 0.0, "dogruluk": 0.0, "f1": 0.0}
    wt = sum(a for x, (_, a) in OLCUM.items() if d[x])
    for x, (k, a) in OLCUM.items():
        os_ = [o for o in _ogeler(form, x) if _k(o, k)]
        ds = [dayanak(x, o, metin) for o in os_]
        iyi, kotu = ds.count("dayanaklı"), ds.count("dayanaksız")
        bul = [i for i, y in enumerate(d[x]) if any(y["_v"] == o["_v"] and eslesir(x, _k(y, k), _k(o, k)) for o in os_)]
        kp, dg = len(bul) / len(d[x]) if d[x] else None, iyi / (iyi + kotu) if iyi + kotu else 1.0
        r["liste"][x] = {"n": len(os_), "kapsam": kp, "dogruluk": dg, "dogrulanamadi": ds.count("doğrulanamadı"), "bulunan": bul,
                        "dayanaksiz": [_k(o, k) for o, z in zip(os_, ds) if z == "dayanaksız"],
                        "fazla": [(_k(o, k), z) for o, z in zip(os_, ds)  # F3-ÖLÇÜM-4: D'de karşılığı yok
                                  if not any(y["_v"] == o["_v"] and eslesir(x, _k(y, k), _k(o, k)) for y in d[x])]}
        if d[x]:
            for t, v in (("kapsam", kp), ("dogruluk", dg), ("f1", 2 * kp * dg / (kp + dg) if kp + dg else 0.0)):
                top[t] += a / wt * v
    return {**r, **(top if wt else dict.fromkeys(top, 1.0))}


def _ort(v, k):
    return sum(x[k] for x in v) / len(v) if v else 0.0


def _yuzde(v):
    return " · ".join(f"{e} %{_ort(v, k) * 100:.0f}" for e, k in (("kapsam", "kapsam"), ("doğruluk", "dogruluk"), ("F1", "f1")))


def olcum_satirlari(a, b, d, metin):
    """F3-ÖLÇÜM v2 rapor (a, b: olc_v2 form sonuçları): satır · liste başı A/B sayı, kapsam, doğruluk, doğrulanamadı · url sayısı ·
    B'nin hiçbir yanıtında bulunmayan ilk 5 D öğesi (konuşmada var / yalnız kare / dayanaksız)."""
    o = lambda v, x, t: sum(r["liste"][x][t] or 0 for r in v) / max(len(v), 1)  # noqa: E731
    s = [f"{_yuzde(b)} (A: {_yuzde(a)})"]
    s += [f"{x}: A {o(a, x, 'n'):.1f} · B {o(b, x, 'n'):.1f} · kapsam " + (f"%{o(b, x, 'kapsam') * 100:.0f}" if d[x] else "—")
          + f" · doğruluk %{o(b, x, 'dogruluk') * 100:.0f} · doğrulanamadı {o(b, x, 'dogrulanamadi'):.1f}" for x in OLCUM]
    s.append(f"aciklama_baglantilari (skora girmez): A {_ort(a, 'url'):.1f} · B {_ort(b, 'url'):.1f}")
    s.append(f"anlamsal: açık (eşik {ANLAM_ESIK})" if _acik() else "anlamsal: kapalı")  # F3-ÖLÇÜM-4
    ab = [{(x, i) for x in OLCUM for i in r["liste"][x]["bulunan"]} for r in a[:2]]
    s.append("A1↔A2 kapsam: " + (f"%{len(ab[0] & ab[1]) / len(ab[0] | ab[1]) * 100:.0f}" if len(ab) == 2 and ab[0] | ab[1] else "—"))
    kac = [(x, y) for x in OLCUM for i, y in enumerate(d[x]) if not any(i in r["liste"][x]["bulunan"] for r in b)]
    z = list(dict.fromkeys(y for r in a for x in OLCUM for y in r["liste"][x]["dayanaksiz"]))  # F3-V2: kalibrasyon görünsün
    fz = list(dict.fromkeys((y, e) for r in b for x in OLCUM for y, e in r["liste"][x]["fazla"]))
    s.append("B fazlası: " + (", ".join(f"{y[:80]} ({DAYANAK[e]})" for y, e in fz[:5]) or "yok"))
    s.append("A dayanaksız: " + (", ".join(y[:80] for y in z[:5]) or "yok"))
    s.append("kaçırılan: " + (", ".join(f"{_k(y, OLCUM[x][0])[:80]} ({DAYANAK[dayanak(x, y, metin)]})" for x, y in kac[:5]) or "yok"))
    return s


def _sn(s):
    return functools.reduce(lambda a, x: a * 60 + int(x), s.split(":"), 0)


def _bolumler(paket):
    """F3-V6: paketin ## Chapter satırları → şemanın bolumler biçimi [{"zaman", "baslik"}] ("yok" → [])."""
    b = paket.split("\n## Segmentler\n", 1)[0].split("\n## Chapter\n", 1)[-1].split("\n## ", 1)[0]
    return [{"zaman": z[1], "baslik": z[2].strip()} for z in re.finditer(r"^(\d+(?::\d+)+) (.+)$", b, re.M)]


def bolumle(paket, k, yuk=False):
    """F3-V5: paket süresi k eşit parçaya, sınırlar en yakın bölüm (## Chapter) başlangıcına. Her parça = aralık notu + "## Segmentler"
    öncesi (başlık · bölümler · açıklama bağlantıları; hepsinde) + aralıktaki konuşma/OCR/kare satırları; damgasız satır ilk parçada.
    F3-V6 yuk=True: sınırlar yükü (metin/4 + kare × 1000 token) eşitleyen bölüm başına (bölüm kalmadıysa satır zamanına); konuşması
    ve karesi olmayan parça oluşursa k bir düşer."""
    from .metin import ss
    ust, govde = (paket.split("\n## Segmentler\n", 1) + [""])[:2]
    govde = "## Segmentler\n" + govde if govde else ""
    bas = sorted({_sn(b["zaman"]) for b in _bolumler(ust)})
    zaman = lambda s: re.match(r"\[(\d+(?::\d+)+)\]", s) or re.search(r" · (\d+(?::\d+)+)$", s)
    sure = int(z[1]) if (z := re.search(r"sure_sn (\d+)", ust)) else max([_sn(z[1]) for s in govde.splitlines() if (z := zaman(s))] or [0]) + 1
    sat, bolum = [], ""  # (satır, sn | None, yük, konuşma/kare mi)
    for s in govde.splitlines():
        bolum = s if s.startswith("## ") else bolum
        z = None if s.startswith("## ") else zaman(s)
        sat.append((s, _sn(z[1]) if z else None, len(s) / 4 + 1000 * (bool(z) and bolum == "## Kareler"),
                    bool(z) and bolum in ("## Segmentler", "## Kareler")))
    yk = lambda t: sum(y for _, z, y, _ in sat if (z or 0) < t)
    while True:
        sinir = [0]
        for i in range(1, k):
            c = [b for b in bas if b > sinir[-1]]
            if yuk:
                c = c or sorted({z for _, z, _, _ in sat if z and z > sinir[-1]})
                sinir.append(min(c, key=lambda b: abs(yk(b) - yk(sure + 1) * i / k)) if c else sinir[-1] + 1)
            else:
                sinir.append(min(c, key=lambda b: abs(b - sure * i / k)) if c else max(round(sure * i / k), sinir[-1] + 1))
        parca = [[f"Bu çağrı videonun {ss(a)}–{ss(b)} aralığı; yalnız bu aralıktaki öğeleri yaz.", ust]
                 for a, b in zip(sinir, sinir[1:] + [max(sure, sinir[-1])])]
        dolu = [False] * k
        for s, z, _, ic in sat:
            if s.startswith("## "):
                for p in parca:
                    p.append(s)
            else:
                j = max(bisect.bisect_right(sinir, z) - 1, 0) if z is not None else 0
                parca[j].append(s)
                dolu[j] |= ic
        if not yuk or k == 1 or all(dolu):
            return ["\n".join(p) for p in parca]
        k -= 1


ANAHTAR = {**{x: a for x, (a, _) in OLCUM.items()}, "iz": "ne"}  # F3-V5: birlestir tekilleştirme anahtarı


def birlestir(formlar, bolumler=None):
    """F3-V5: parça formları (zaman sırasıyla) → tek form. videolar[] aynı id'de birleşir · ozet sırayla birleşim · bolumler ve
    aciklama_baglantilari ilk dolu parçadan bir kez · ANAHTAR listeleri eslesir ile tekil · diğer listeler birebir tekil · gerisi ilk parça.
    F3-V6: bolumler verilirse (paketten) parçalarınkinin yerine o yazılır."""
    if formlar and all(isinstance(f.get("videolar"), list) for f in formlar):
        ids = dict.fromkeys(v.get("id") for f in formlar for v in f["videolar"])
        return {"videolar": [birlestir([v for f in formlar for v in f["videolar"] if v.get("id") == i], bolumler) for i in ids]}
    if bolumler is not None:
        return {**birlestir(formlar), "bolumler": bolumler}
    out = {}
    for x in dict.fromkeys(a for f in formlar for a in f):
        d = [f[x] for f in formlar if x in f]
        if x == "ozet":
            out[x] = " ".join(s for s in d if s)
        elif x in ("bolumler", "aciklama_baglantilari"):
            out[x] = next((s for s in d if s), d[0])
        elif isinstance(d[0], list):
            tut = []
            for o in (o for s in d for o in s):
                a = _k(o, ANAHTAR[x]) if x in ANAHTAR and isinstance(o, dict) else o
                if not any(eslesir(x, a, b) if x in ANAHTAR else a == b for b, _ in tut):
                    tut.append((a, o))
            out[x] = [o for _, o in tut]
        else:
            out[x] = d[0]
    return out


def son_gecis(tas, g, form, m):
    """F3-V6: birleşimden sonra tek görselsiz çağrı (paket başlığı + konuşma + OCR + birleşik listelerin anahtar satırları) → ozet ve
    belirsizlikler yazılır, ek_* öğeleri birlestir (eslesir) ile tekil eklenir. → (yanıt, hata | None); hatada form değişmez."""
    from . import parti as pt
    ust, govde = (g[1].split("\n## Segmentler\n", 1) + [""])[:2]
    v = form["videolar"][0]
    sat = [f"- {x}: {_k(o, ANAHTAR[x])}" for x in SON_LISTE for o in v.get(x) or [] if isinstance(o, dict)]
    s = g[2]["properties"]["videolar"]["items"]["properties"]
    sema = pt._o(ozet=s["ozet"], belirsizlikler=s["belirsizlikler"], **{f"ek_{x}": s[x] for x in SON_LISTE})
    konusma = govde.split("\n## Kareler\n", 1)[0]  # konuşma + OCR; kare yolları yok (görselsiz)
    r = tas(SON_SISTEM, f"{ust}\n## Segmentler\n{konusma}\n\n## Birleşik form (anahtar satırlar)\n" + "\n".join(sat or ["yok"]), sema, model=m)
    if r.get("hata") or pt._denet(r.get("form"), sema, "son"):
        return r, r.get("hata") or "şema"
    f = r["form"]
    form["videolar"][0] = {**birlestir([v, {"id": v.get("id"), **{x: f[f"ek_{x}"] for x in SON_LISTE}, "belirsizlikler": f["belirsizlikler"]}]),
                           "ozet": f["ozet"] or v.get("ozet")}
    return r, None


def _parcali(tas, sis, g, k, ek, m, v6=False):
    """F3-V5: bolumle(g[1], k) parçaları paralel (≤ PARALEL_TAVAN, fazlası kuyrukta) → birlestir. usd/usage/yeniden toplam, sure duvar saati; parça hatasında birleşim yok.
    F3-V6 (v6): yük dengeli bolumle · parçaya özel talimat + DEĞERLENDİR listesi kullanıcı mesajının başında · bolumler paketten · son_gecis."""
    from concurrent.futures import ThreadPoolExecutor
    parca = bolumle(g[1], k, yuk=v6)
    msg = (lambda i, p: "\n".join([PARCA_BOLUM, *[PARCA_LINK] * (i > 0)]) + f"\n\n{DEGERLENDIR}{on_cikarim(p)}\n\n{p}") if v6 else (lambda i, p: p)
    kar = lambda p: {"kareler": [x for x in ek["kareler"] if f"{Path(x).name} · " in p]} if "kareler" in ek else {}
    t0 = time.monotonic()
    with ThreadPoolExecutor(min(len(parca), PARALEL_TAVAN)) as h:
        ys = list(h.map(lambda ip: tas(sis(ip[1]), msg(*ip), g[2], **kar(ip[1]), model=m), enumerate(parca)))
    hata = next((f"parça {i}: {y['hata']}" for i, y in enumerate(ys, 1) if y.get("hata")), None)
    form, son = None if hata else birlestir([y.get("form") or {} for y in ys], _bolumler(g[1]) if v6 else None), None
    if v6 and form and form.get("videolar"):
        r, son = son_gecis(tas, g, form, m)
        ys.append(r)
    us, ks = [y.get("usd") for y in ys], dict.fromkeys(a for y in ys for a in (y.get("usage") or {}))
    y = {"usage": {a: sum((y.get("usage") or {}).get(a, 0) for y in ys) for a in ks},
         "usd": None if None in us else sum(us), "sure": round(time.monotonic() - t0, 1),
         "yeniden": sum(y.get("yeniden", 0) for y in ys)}
    return {"form": form, **y, "hata": hata, **({"k_not": f"k {k}→{len(parca)}"} if len(parca) != k else {}), **({"son_hata": son} if son else {})}


def _yaz(y, d):
    y.parent.mkdir(parents=True, exist_ok=True)
    y.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def _tahmin(m, kare):
    """F3-ELEME: aday ilk çağrısının ön tahmini — O58 bandı 15k girdi + 6k çıktı (+ kare × gorsel)."""
    f = FIYAT[m]
    return (15000 * f["girdi"] + 6000 * f["cikti"]) / 1e6 + kare * f.get("gorsel", 0)


JEV_TAVAN = 12  # F3-ÖLÇÜM: puanlama isteği üst sınırı (A 2 + aday 5 × 2); koşu 2 TavanHata ile sonuçsuz kaldı


def eleme(g, adaylar, a_tas, a_model, env, puanla, *, onbellek, destek=None, b_kur=omni_cagir, yokla=omni_yokla,
          zaman=240, en_fazla=5, tavan_cagri=10, tavan_usd=0.15, ornek=None, ornek21=None, kucult=_kucult, kayit=None, yeniden=None, ornek6=None):
    """F3-ELEME adım 4: tek girdi g (sistem, metin, şema, kareler), adaylar tek koşuda. Ön kontrol (kol sabit · varyant · FIYAT · yokla)
    geçmeyen çağrı 0. Aday başı çağrı 1; şema geçerse 2. Sıradaki çağrı B tavanını (çağrı · $; tahmin = adayın son usd'si, yoksa _tahmin)
    aşacaksa yapılmaz → "tavan". usd None (zaman aşımı) harcamaya tahminle girer. supported_parameters'ta reasoning varsa effort minimal.
    F3-VARYANT: aday "model" ya da "model@varyant" (VARYANT): V1 sistem + ornek formu (test videosundan olamaz) · V3 effort low ·
    V4 kareler kucult ile 512 px · F3-V2: V2 EKSIKSIZLIK + DEĞERLENDİR LİSTESİ (on_cikarim) · V21 V2 + ornek21. Geçen B yoksa A çağrılmaz; A (2 tekrar) _a_onbellek'ten. Puanlama tek puanla çağrısı (A, sonra adaylar;
    kör; öğe sayı ya da {"score", ...}). Karar kur.karar (çağrı başı ortalamalarla); öneri = AL'ler içinde en yüksek kalite, eşitlikte ucuz.
    kayit: her yanıt + Jev puanı kayit/<aday>/<i>.json (A: kayit/A). rapor: aday başı alan_farki (A'ya göre)."""
    from . import kur, parti as pt
    if len(adaylar) > en_fazla:
        return {"satirlar": [], "oneri": f"TAVAN aday {len(adaylar)} > {en_fazla}", "a_usd": 0.0, "b_usd": 0.0, "rapor": {}}
    kare = len(g[3]) if len(g) > 3 else 0
    ek = {"kareler": g[3]} if len(g) > 3 else {}
    gecer = lambda y: not y.get("hata") and not pt._denet(y.get("form"), g[2], "form")
    sk = lambda p: p["score"] if isinstance(p, dict) else p
    dosya = lambda ad: re.sub(r"[^\w.@-]", "_", ad)
    durum, b_usd, cagri = {}, 0.0, 0
    for ad in adaylar:
        m, _, v = ad.partition("@")
        v, akil = v or "V0", "reasoning" in (destek or {}).get(m, ())
        if yeniden:  # F3-ÖLÇÜM: B çağrısı 0, kayıttaki yanıtlar · F3-ÖLÇÜM-3: kayıttaki Jev puanı tekrar kullanılır
            ks = [json.loads(f.read_text(encoding="utf-8")) for f in sorted((Path(yeniden) / dosya(ad)).glob("*.json"))]
            durum[ad] = {"neden": None if ks else "kayıt yok", "y": [r["yanit"] for r in ks], "p": [r.get("puan") for r in ks], "akil": akil}
            continue
        orn = {"V1": ornek, "V21": ornek21, "V5": ornek21, "V54": ornek21, "V6": ornek6, "V63": ornek6}.get(v)
        neden = ("kol sabit değil" if m.startswith("~") or "/~" in m or ":free" in m or "openrouter/free" in m
                 else f"bilinmeyen varyant: {v}" if v not in VARYANT
                 else f"{v} örneği yok" if v in ("V1", "V21", *PARCA) and not (orn and Path(orn).is_file())
                 else f"{v} örneği test videosundan ({Path(orn).stem})" if orn and f"=== VIDEO {Path(orn).stem} ===" in g[1]
                 else "V3: reasoning desteklenmiyor" if v == "V3" and not akil
                 else "fiyat yok" if m not in FIYAT else yokla(m, env, gorsel=bool(kare)))
        durum[ad] = {"neden": neden, "y": [], "akil": akil, "m": m, "v": v}
    acik = [x for x in durum.values() if not x["neden"]]
    ap = [json.loads(f.read_text(encoding="utf-8")).get("puan") if (f := Path(yeniden) / "A" / f"{i}.json").is_file() else None
          for i in range(2)] if yeniden else [None, None]
    # Jev: A 2 + çağrılabilecek en fazla B yanıtı · yeniden: yalnız kayıtta puanı olmayanlar
    gerek = sum(p is None for p in ap) + sum(sum(p is None for p in x["p"]) if yeniden else 2 for x in acik)
    if gerek > JEV_TAVAN:
        for x in acik:
            x.update(neden="TAVAN jev", y=[])
    for ad, x in [] if yeniden else durum.items():
        if x["neden"]:
            continue
        m, v, akil = x["m"], x["v"], x["akil"]
        n, b = PARCA.get(v, 1), "V21" if v in PARCA else v  # F3-V5: V5/V54 = V21 sistemi, liste parçaya süzülür
        nc = n + (v in SON)  # F3-V6: son geçiş çağrısı da tavana sayılır
        sis = (lambda t, s=g[0] + f"\n\n{EKSIKSIZLIK}" + ORNEK_BASLIK + Path(ornek6).read_text(encoding="utf-8"): s) if v in SON else \
            lambda t, b=b: (g[0] + (f"\n\n{EKSIKSIZLIK}\n\n{DEGERLENDIR}{on_cikarim(t)}" if b in ("V2", "V21") else "")
                            + (ORNEK_BASLIK + Path(ornek if b == "V1" else ornek21).read_text(encoding="utf-8") if b in ("V1", "V21") else ""))
        ek_v = {"kareler": kucult(g[3], (Path(kayit) if kayit else Path(tempfile.mkdtemp(prefix="eleme-"))) / dosya(ad) / "kare")} \
            if v == "V4" and kare else ek
        tas = b_kur(m, env, timeout=zaman, govde_ek={"reasoning": {"effort": "low" if v == "V3" else "minimal"}} if akil else None)
        while len(x["y"]) < 2 and (not x["y"] or gecer(x["y"][-1])):
            tahmin = (x["y"][-1].get("usd") if x["y"] else None) or _tahmin(m, kare) * nc
            if cagri + nc > tavan_cagri or b_usd + tahmin > tavan_usd:
                x["tavan"] = True
                break
            y = _parcali(tas, sis, g, n, ek_v, m, v6=v in SON) if n > 1 else tas(sis(g[1]), g[1], g[2], **ek_v, model=m)
            cagri, b_usd = cagri + nc, b_usd + (tahmin if y.get("usd") is None else y["usd"])
            x["y"].append(y)
            if kayit:  # puanlamadan önce diske (koşu 2: Jev hatasında 6 yanıt kayboldu)
                _yaz(Path(kayit) / dosya(ad) / f"{len(x['y']) - 1}.json", {"yanit": y, "puan": None})
    gecen = {ad: [y for y in x["y"] if gecer(y)] for ad, x in durum.items()}
    gecen = {ad: v for ad, v in gecen.items() if v}
    a_usd, ozet, karar, rapor, ya, pa, pb = 0.0, {}, {}, {}, [], [], {}

    def a_say(*a, **k):
        nonlocal a_usd
        r = a_tas(*a, **k)
        a_usd += r.get("usd") or 0
        return r

    def ozetle(ys, p):
        n = len(ys)
        v2 = [olc_v2(y["form"], d, g[1]) for y in ys if gecer(y)]  # F3-ÖLÇÜM: görev = şema geçti × ağırlıklı F1
        return {"kalite": sum(p) / len(p), "basari": sum(map(gecer, ys)) / n, "gorev": [sum(x["f1"] for x in v2) / n],
                "girdi": sum(_girdi(y.get("usage") or {}) for y in ys) / n,
                "cikti": sum((y.get("usage") or {}).get("output_tokens", 0) for y in ys) / n, "maliyet": sum(y.get("usd") or 0 for y in ys) / n,
                "v2": v2}
    oneri = "öneri: yok (geçen aday yok)"
    if gecen:
        ya = [_a_onbellek(onbellek, a_say, a_model, g, i) for i in range(2)]
        if all(y.get("hata") for y in ya):
            oneri = f"öneri: yok (DUR: A yanıt vermedi — {ya[0]['hata'][:120]})"
        else:
            kp = {ad: [p for y, p in zip(durum[ad]["y"], durum[ad].get("p") or [None] * len(durum[ad]["y"])) if gecer(y)]
                  for ad in gecen}
            jev = {ad: sum(p is None for p in v) for ad, v in kp.items()}
            eski = ap + [p for v in kp.values() for p in v]
            ms = [f"GÖREV: {g[1]}\nYANIT: {json.dumps(y.get('form'), ensure_ascii=False)}" for y in ya + [y for v in gecen.values() for y in v]]
            yeni = iter(puanla([s for s, p in zip(ms, eski) if p is None]) if None in eski else ())
            puan = iter([next(yeni) if p is None else p for p in eski])
            pa = [next(puan) for _ in ya]
            d = referans([y["form"] for y in ya if gecer(y)], [y["form"] for v in gecen.values() for y in v], g[1])
            bos = not any(d.values()) and any(_dolu(y.get("form")) for y in ya)  # F3-ÖLÇÜM-3: veri var, ölçüm görmüyor
            sa = ozetle(ya, list(map(sk, pa)))
            for ad, v in gecen.items():
                pb[ad] = [next(puan) for _ in v]
                ozet[ad] = ozetle(durum[ad]["y"], list(map(sk, pb[ad])))
                karar[ad] = ("DUR (ölçüm boş)" if bos else "SOR (maliyet bilinmiyor)" if any(y.get("usd") is None for y in durum[ad]["y"]) else
                             kur.karar(*({**o, "basari": o["gorev"][0]} for o in (sa, ozet[ad])), None,  # F3-V2: başarı = görev skoru
                                       max(map(sk, pa)) - min(map(sk, pa)), [(sa["gorev"][0], ozet[ad]["gorev"][0])]))
                rapor[ad] = {**alan_farki([y["form"] for y in ya if y.get("form")], [y["form"] for y in v], g[2]),
                             "olcum": ["ÖLÇÜM BOŞ"] if bos else olcum_satirlari(sa["v2"], ozet[ad]["v2"], d, g[1])}
            al = [(ozet[m]["kalite"], -ozet[m]["maliyet"], m) for m, k in karar.items() if k.startswith("AL")]
            oneri = (f"öneri: {max(al)[2]} (kalite {max(al)[0]:.2f} · ${-max(al)[1]:.4f}/çağrı)" if al else
                     "öneri: yok (AL aday yok)")
    if kayit:
        for i, y in enumerate(ya):
            _yaz(Path(kayit) / "A" / f"{i}.json", {"yanit": y, "puan": pa[i] if i < len(pa) else None})
        for ad, x in durum.items():
            it = iter(pb.get(ad, ()))
            for i, y in enumerate(x["y"]):
                _yaz(Path(kayit) / dosya(ad) / f"{i}.json", {"yanit": y, "puan": next(it, None) if gecer(y) else None})
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
             *([f"önbellek %{100 * t('cached') / t('input_tokens'):.0f}"] if t("input_tokens") and any("cached" in (y.get("usage") or {}) for y in ys) else []),
             "süre " + "+".join(str(y.get("sure")) for y in ys) + " s", "$/çağrı " + ("?" if None in usd else f"{sum(usd) / len(usd):.4f}"),
             *([f"yeniden {yn}"] if (yn := sum(y.get("yeniden", 0) for y in ys)) else []),
             *dict.fromkeys(y["k_not"] for y in ys if y.get("k_not")), *(["son geçiş: hata"] if any(y.get("son_hata") for y in ys) else []),
             *([f"kalite {ozet[m]['kalite']:.2f} · şema {ozet[m]['basari']:.2f}"] if m in ozet else []), karar.get(m, "ELENDİ"),
             *([rapor[m]["olcum"][0]] if m in ozet else []),
             *([f"Jev {jev[m]}" if jev[m] else "Jev 0 (kayıttan)"] if yeniden and m in ozet else [])]
        if x["akil"] and max((y.get("usage") or {}).get("reasoning", 0) for y in ys) > 1000:  # F3-VARYANT: küçük iz gürültü sayılır
            p.append("reasoning parametresi etkisiz")
        if x.get("tavan"):
            p.append("tavan")
        satirlar.append(" · ".join(p))
    return {"satirlar": satirlar, "oneri": oneri, "a_usd": a_usd, "b_usd": b_usd, "rapor": rapor, "jev_istek": gerek}
