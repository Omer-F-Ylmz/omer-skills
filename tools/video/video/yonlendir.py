"""F1: model yönlendirme — adım başı sağlayıcı/model (durum.json "yonlendirme": {adim: {saglayici, model}}); tanımsız adım bugünkü taşıyıcı + d["model"]."""
import base64
import functools
import json
import time
from pathlib import Path

from . import ikinci_goz as ig

OMNI_URL = "http://localhost:20128"  # omni-auth SKILL.md:54-58 (OMNIROUTE_URL varsayılanı)
OMNI_YOL = "/v1/chat/completions"  # omni-inference SKILL.md:283; openapi.yaml:1156 /api/v1/… adayı — F1-KURULUM canlı çağrısı kesinleştirir
# F1 eki (Ömer, 5 Eki): model → {"girdi": $/1M, "cikti": $/1M, "kaynak": "<url · tarih>"}; boş başlar, değer tahmin edilmez (F1-KURULUM'da sağlayıcı sayfasından)
FIYAT = {}
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


def sec(d, adim, cagir, env):
    """→ (taşıyıcı, model): adım ayarda yoksa verilen taşıyıcı ve d["model"] (bugünkü davranış birebir)."""
    s = (d.get("yonlendirme") or {}).get(adim)
    return (SAGLAYICI[s["saglayici"]](s["model"], env), s["model"]) if s else (cagir, d["model"])
