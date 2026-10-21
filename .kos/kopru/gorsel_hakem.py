"""Ücretsiz görü hakemi: her PNG'ye aynı soru, iki aile; JSON {puan, sivi_mi, plastik_gorunen}; aileler ayrışırsa AYRIŞTI.
python gorsel_hakem.py <png...> --soru "<metin>"   (çıktı: PNG başına 1 satır; ayrışan görseli Desktop kendisi inceler)"""
import base64
import io
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import ucretsiz_havuz as h  # noqa: E402
from PIL import Image  # noqa: E402

# aile → görü yetenekli adaylar (ilk çalışan kazanır); havuz ENT'i görü türü taşımadığı için burada ayrı
ADAY = {"google": [h.E("gemini", "gemini-3.1-flash-lite", "google", None, 10, 200_000, 200, 900_000, ()),
                   h.E("gemini", "gemini-3.6-flash", "google", None, 5, 200_000, 100, 900_000, ())],
        "meta": [h.E("nvidia", "meta/llama-3.2-11b-vision-instruct", "meta", None, 30, 100_000, 1000, 100_000, ()),
                 h.E("nvidia", "meta/llama-3.2-90b-vision-instruct", "meta", None, 30, 100_000, 1000, 100_000, ())],
        "nvidia": [h.E("openrouter", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "nvidia", "openrouter", 18, 10**6, 900, 100_000, ()),
                   h.E("openrouter", "nvidia/nemotron-3.5-super-vl:free", "nvidia", "openrouter", 18, 10**6, 900, 100_000, ())]}
CIFT = 2
BICIM = """Bu görseli değerlendir. Soru: {soru}
Yalnız tek satır JSON ver: {{"puan": 0-10 tam sayı, "sivi_mi": true/false, "plastik_gorunen": true/false}}"""
BICIM_LOGO = """Bu bir kişisel logo (monogram). Soru: {soru}
Yalnız tek satır JSON ver: {{"ozgunluk": 1-10, "akilda_kalicilik": 1-10, "kucuk_okunurluk": 1-10, "havali": 1-10}}"""
LOGO = ("ozgunluk", "akilda_kalicilik", "kucuk_okunurluk", "havali")  # --sema logo; sıvı/plastik alanları yok
FARK = 2  # puan farkı bu eşiğe ulaşırsa ya da bool'lar ayrışırsa AYRIŞTI


def veri_url(yol):
    im = Image.open(yol).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def ayikla(y, logo=False):
    m = re.search(r"\{.*?\}", y, re.S)
    if not m:
        raise ValueError("JSON yok")
    j = json.loads(m.group(0))
    if logo:
        return {k: int(j[k]) for k in LOGO}
    return {"puan": int(j["puan"]), "sivi_mi": bool(j["sivi_mi"]), "plastik_gorunen": bool(j["plastik_gorunen"])}


def sor(png, soru, logo=False):
    icerik = [{"type": "text", "text": (BICIM_LOGO if logo else BICIM).format(soru=soru)}, {"type": "image_url", "image_url": {"url": veri_url(png)}}]
    sonuc = {}
    for _ in range(2):  # geçici 503/zaman aşımı için ikinci tur (yalnız eksik aileler)
        for aile, adaylar in ADAY.items():
            if len(sonuc) >= CIFT:
                break
            for e in [] if aile in sonuc else adaylar:
                try:
                    sonuc[aile] = {"model": h.ad(e), **ayikla(h._istek(e, icerik, 400, 60), logo)}
                    break
                except (h.Hata, OSError, ValueError, KeyError, TypeError):
                    continue
    return sonuc


def main():
    a = sys.argv[1:]
    soru = "Görsel gerçekçi bir sıvı (kahve/süt) gösteriyor mu, plastik/yapay mı görünüyor?"
    if "--soru" in a:
        i = a.index("--soru")
        soru = a[i + 1]
        del a[i:i + 2]
    logo = "--sema" in a and a[a.index("--sema") + 1] == "logo"
    if logo:
        i = a.index("--sema")
        del a[i:i + 2]
        if "--soru" not in sys.argv:
            soru = "Bu logo özgünlük, akılda kalıcılık, 64px'te okunurluk ve 'havalı' olma açısından kaç puan?"
    for png in a:
        s = sor(png, soru, logo)
        if not s:
            print(f"{Path(png).name} HAKEM YOK (görü uçlarının hiçbiri yanıtlamadı)")
            continue
        v = list(s.values())
        if len(v) < 2:
            durum = "TEK-AİLE"
        elif logo:
            durum = "AYRIŞTI" if any(abs(v[0][k] - v[1][k]) >= FARK for k in LOGO) else "UZLAŞTI"
        elif abs(v[0]["puan"] - v[1]["puan"]) >= FARK or any(v[0][k] != v[1][k] for k in ("sivi_mi", "plastik_gorunen")):
            durum = "AYRIŞTI"
        else:
            durum = "UZLAŞTI"
        if logo:
            ort = sum(x[k] for x in v for k in LOGO) / (len(v) * len(LOGO))
            durum += f" ORT={ort:.2f}"
        print(f"{Path(png).name} {durum} " + json.dumps({k: {x: y for x, y in d.items() if x != "model"} for k, d in s.items()}, ensure_ascii=False)
              + " " + ",".join(d["model"] for d in s.values()))


main()
