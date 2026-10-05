"""F1: model yönlendirme — adım başı sağlayıcı/model (durum.json "yonlendirme": {adim: {saglayici, model}}); tanımsız adım bugünkü taşıyıcı + d["model"]."""
import base64
import functools
import json
import time
from pathlib import Path

from . import ikinci_goz as ig

OMNI_URL = "http://localhost:20128"  # omni-auth SKILL.md:54-58 (OMNIROUTE_URL varsayılanı)
OMNI_YOL = "/v1/chat/completions"  # omni-inference SKILL.md:283; F1-KURULUM-2 canlı çağrı 200 (5 Eki) — kesin
# F1 eki (Ömer, 5 Eki): model → {"girdi": $/1M, "cikti": $/1M, "kaynak": "<url · tarih>"}; boş başlar, değer tahmin edilmez (F1-KURULUM'da sağlayıcı sayfasından)
_OR = "https://openrouter.ai/api/v1/models · 2026-10-05"  # F1-KURULUM-2: json_schema destekli en ucuz 5 ücretli model; anahtar = OmniRoute model id
FIYAT = {
    "openrouter/mistralai/mistral-nemo": {"girdi": 0.019, "cikti": 0.03, "kaynak": _OR},
    "openrouter/inclusionai/ling-3.0-flash-vl": {"girdi": 0.021, "cikti": 0.0616, "kaynak": _OR},
    "openrouter/sao10k/l3-lunaris-8b": {"girdi": 0.04, "cikti": 0.05, "kaynak": _OR},
    "openrouter/openai/gpt-oss-20b": {"girdi": 0.018, "cikti": 0.09, "kaynak": _OR},
    "openrouter/nex-agi/nex-n2.5-mini": {"girdi": 0.025, "cikti": 0.1, "kaynak": _OR},
}
MALIYET_BASLIK = "x-omniroute-response-cost"  # openapi.yaml:1173-1176 (USD, 10 ondalık; "0.0000000000" = ücretsiz ya da fiyatsız)


def _usd(model, u, basliklar):
    """Yanıt başlığı > 0 ise o; değilse usage × FIYAT; model FIYAT'ta yoksa None (0 değil — maliyet bilinmiyor)."""
    try:
        if (m := float(next((v for k, v in basliklar.items() if k.lower() == MALIYET_BASLIK), 0))) > 0:
            return m
    except ValueError:
        pass
    f = FIYAT.get(model)
    return (u.get("prompt_tokens", 0) * f["girdi"] + u.get("completion_tokens", 0) * f["cikti"]) / 1e6 if f else None


def omni_cagir(model, env, gonder=functools.partial(ig._post, basliklar=True)):
    """hafif.cagir imzasında OmniRoute (OpenAI biçimi) adaptörü → {form, usage, usd, sure, hata}; anahtar yalnız env OMNIROUTE_KEY, hiçbir çıktıya yazılmaz."""
    anahtar = env.get("OMNIROUTE_KEY") or ""

    def cagir(sistem, metin, sema, kareler=(), **_):
        from . import cli  # döngüsel içe aktarma yok
        t0 = time.monotonic()

        def hata(neden):
            neden = f"ölçülemedi: {neden}"[:200]
            return {"form": None, "usage": {}, "usd": 0.0, "sure": round(time.monotonic() - t0, 1),
                    "hata": neden.replace(anahtar, "***") if anahtar else neden}
        ekler = [{"type": "image_url", "image_url": {"url": f"data:image/{'png' if str(k).endswith('.png') else 'jpeg'};base64,"
                  + base64.b64encode(Path(k).read_bytes()).decode()}} for k in kareler]
        govde = {"model": model, "response_format": {"type": "json_schema", "json_schema": {"name": "form", "strict": False, "schema": sema}},
                 "messages": [{"role": "system", "content": sistem},
                              {"role": "user", "content": [{"type": "text", "text": cli._temizle(metin, env)}, *ekler]}]}
        bas = {"Content-Type": "application/json", **({"Authorization": f"Bearer {anahtar}"} if anahtar else {})}
        try:
            durum, y, *ek = gonder(env.get("OMNIROUTE_URL", OMNI_URL).rstrip("/") + OMNI_YOL, govde, bas)
        except OSError as e:  # sunucu yok / zaman aşımı → adım düşmez, sebep hata alanında
            return hata(f"{type(e).__name__}: {e}")
        if durum != 200:
            return hata(f"HTTP {durum} " + json.dumps(y.get("error") or "", ensure_ascii=False))
        u, ic = y.get("usage") or {}, (y.get("choices") or [{}])[0].get("message", {}).get("content") or ""
        try:
            form = json.loads(ic[ic.find("{"): ic.rfind("}") + 1])
        except ValueError:
            form = None
        return {"form": form, "usage": {"input_tokens": u.get("prompt_tokens", 0), "output_tokens": u.get("completion_tokens", 0)},
                "usd": _usd(model, u, ek[0] if ek else {}), "sure": round(time.monotonic() - t0, 1), "hata": None if form is not None else "form JSON değil"}
    return cagir


SAGLAYICI = {"omniroute": omni_cagir}
OMNI_MODELLER = "/api/v1/models"  # openapi.yaml:1681 (GET, BearerAuth; data[].id — Model şeması :9091), ücretsiz


def omni_yokla(model, env, getir=ig._post):
    """F3 ön kontrol (model çağrısından önce): None = sunucu var, kimlik geçer, model listede; değilse hata metni (anahtar yazılmaz)."""
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
    ids = [m.get("id") for m in y.get("data") or []]
    return None if model in ids else f"model yok: {model} (listede {len(ids)} model)"


def sec(d, adim, cagir, env):
    """→ (taşıyıcı, model): adım ayarda yoksa verilen taşıyıcı ve d["model"] (bugünkü davranış birebir)."""
    s = (d.get("yonlendirme") or {}).get(adim)
    return (SAGLAYICI[s["saglayici"]](s["model"], env), s["model"]) if s else (cagir, d["model"])


def ab(d, adim, girdiler, kol_b, cagir, env, puanla, *, basari=None, tekrar=2, tavan):
    """F2: aynı girdiler (sistem, metin, şema) iki kolda — A = sec(d, adim) bugünkü, B = kol_b; puanla(metinler) kör (GÖREV+YANIT,
    model adı yok); başarı = hata yok + hattın form doğrulaması (parti._denet); gürültü = A tekrar farkı; karar kur.karar (A1 tablosu). usd None kol → SOR;
    tavan < 2×tekrar×girdi → TAVAN, çağrı yok. yonlendirme yalnız AL'de {adim: kol_b}."""
    n = 2 * tekrar * len(girdiler)
    if n > tavan:
        return {"karar": f"TAVAN {n} > {tavan}", "yonlendirme": None}
    from . import parti as pt  # parti yonlendir'i içe aktarır; döngü yok
    basari = basari or (lambda y, sema: float(not y.get("hata") and not pt._denet(y.get("form"), sema, "form")))
    kollar = {"a": sec(d, adim, cagir, env), "b": sec({**d, "yonlendirme": {adim: kol_b}}, adim, cagir, env)}
    s, bilinmeyen = {}, []
    for ad, (tas, model) in kollar.items():
        ys = [[tas(si, m, sema, model=model) for _ in range(tekrar)] for si, m, sema in girdiler]
        puan = puanla([f"GÖREV: {m}\nYANIT: {json.dumps(y.get('form'), ensure_ascii=False)}"
                       for (_, m, _), yg in zip(girdiler, ys) for y in yg])
        puan = [puan[i * tekrar:(i + 1) * tekrar] for i in range(len(girdiler))]
        hepsi = [y for yg in ys for y in yg]
        if any(y.get("usd") is None for y in hepsi):
            bilinmeyen.append(model)
        s[ad] = {"model": model, "kalite": sum(map(sum, puan)) / len(hepsi),
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
