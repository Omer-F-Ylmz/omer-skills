"""Ücretsiz havuz sağlayıcı durum tablosu (HAVUZ-TAMIR-1). Kotadan şüphelenmeden önce ÖNCE bunu çalıştır.

    python tools/kota_yokla.py            sağlayıcı başına 1 canlı istek
    python tools/kota_yokla.py --n 10     sağlayıcı başına 10 istek (başarı/süre)
    python tools/kota_yokla.py --sadece groq,mistral

Yalnız tablo basar; anahtar hiçbir çıktıya yazılmaz. Havuz durumuna (durum.json) dokunmaz, yalnız okur.
Karar kuralı: 429 = kota/hız (Retry-After/başlıktan süre) · 402 = bütçe bitti (kalıcı, sıfırlanma tarihine kadar) ·
401/403 = anahtar/izin · 404/410 = MODEL değişmeli (kota DEĞİL) · 5xx/zaman aşımı = geçici.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import ucretsiz_havuz as H  # noqa: E402

# sağlayıcı → yoklama modeli (canlı ölçüm 29 Eki); uç ve anahtar H.SAG'den
MODEL = {"groq": "openai/gpt-oss-20b", "openrouter": "openrouter/free", "mistral": "ministral-14b-latest",
         "nvidia": "openai/gpt-oss-20b", "sambanova": "gpt-oss-120b", "github": "openai/gpt-4.1-mini",
         "ollama": "gpt-oss:20b", "cloudflare": "@cf/openai/gpt-oss-20b", "gemini": "gemini-flash-lite-latest",
         "omniroute": "cc-ucuz-free"}
# Sıfırlanma (belge/ölçüm): mistral 402 = API bütçesi, console.mistral.ai faturalama; ollama = aylık kota, ollama.com/settings/usage
NOT = {"mistral": "402 budget exhausted: otomatik sıfırlanmaz, Mistral konsolunda bütçe/limit yenilenmeli",
       "ollama": "Free usage limit: aylık pencere, ayın başında sıfırlanır (ollama.com/settings/usage)"}


def sinif(kod, govde):
    if kod == 200:
        return "ÇALIŞIYOR"
    if kod == 429:
        return "GEÇİCİ-429 (hız/kota; başlığa bak)"
    if kod == 402:
        return "DOLU-402 (bütçe bitti)"
    if kod in (401, 403):
        return "ANAHTAR/İZİN"
    if kod in (404, 410):
        return "MODEL-DEĞİŞTİR (kota değil)"
    if kod == 400:
        return "İSTEK-400 (model/parametre)"
    return "GEÇİCİ/AĞ"


def yokla(prov):
    url, kaynak = H._url(prov), H.SAG[prov][1]
    key = H._anahtar(kaynak)
    if not url or not key:
        return (0, 0.0, "ANAHTAR YOK", "", "")
    g = {"model": MODEL[prov], "messages": [{"role": "user", "content": "1+1? tek kelime"}], "max_tokens": 300}
    if prov in H.DUSUNME and "gemma" not in MODEL[prov]:
        g["reasoning_effort"] = "low"
    q = urllib.request.Request(url, json.dumps(g).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8", "Authorization": "Bearer " + key})
    t = time.time()
    try:
        with urllib.request.urlopen(q, timeout=40) as r:
            j = json.load(r)
            hd = r.headers
            ok = bool(((j.get("choices") or [{}])[0].get("message", {}).get("content") or "").strip())
            return (200 if ok else 502, time.time() - t, "ÇALIŞIYOR" if ok else "BOŞ-YANIT", baslik(hd), "")
    except urllib.error.HTTPError as e:
        b = H._gizle(e.read()[:160].decode("utf-8", "replace")).replace("\n", " ")
        return (e.code, time.time() - t, sinif(e.code, b), baslik(e.headers), b)
    except Exception as e:  # noqa: BLE001
        return (599, time.time() - t, "GEÇİCİ/AĞ", "", H._gizle(str(e))[:80])


def baslik(h):
    ra = h.get("retry-after")
    kalan = [f"{k}={v}" for k, v in h.items() if "ratelimit" in k.lower() and ("remaining" in k.lower() or "reset" in k.lower())]
    return ("retry-after=" + ra + " " if ra else "") + " ".join(kalan[:3])


def havuz_durum():
    d = H._durum(); now = time.time()
    return {k: int(v - now) for k, v in d.get("soguma", {}).items() if v > now}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--sadece", default="")
    a = ap.parse_args()
    sec = [p for p in MODEL if not a.sadece or p in a.sadece.split(",")]
    print(f"{'saglayici':<11}{'model':<30}{'ok/n':<7}{'sn(ort)':<9}{'son-http':<9}durum · başlık/gövde")
    for p in sec:
        r = [yokla(p) for _ in range(a.n)]
        ok = sum(1 for x in r if x[0] == 200)
        son = r[-1]
        ort = sum(x[1] for x in r) / len(r)
        print(f"{p:<11}{MODEL[p][:29]:<30}{ok}/{a.n:<5}{ort:<9.1f}{son[0]:<9}{son[2]} {son[3]} {son[4][:90]}")
        if p in NOT and son[0] != 200:
            print(f"{'':<11}↳ {NOT[p]}")
    soguma = havuz_durum()
    print(f"havuz soğumada ({len(soguma)}): " + (", ".join(f"{k}:{v // 60}dk" for k, v in sorted(soguma.items())) or "yok"))


if __name__ == "__main__":
    main()
