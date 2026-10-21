"""Ücretsiz görü hakemi: her PNG'ye aynı soru, iki aile; JSON {puan, sivi_mi, plastik_gorunen}; aileler ayrışırsa AYRIŞTI.
python gorsel_hakem.py <png...> --soru "<metin>"   (çıktı: PNG başına 1 satır; ayrışan görseli Desktop kendisi inceler)"""
import base64
import io
import json
import os
import re
import subprocess
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
BICIM_KIYAS = """İlk görsel REFERANS, ikinci görsel ADAY. Soru: {soru}
Yalnız tek satır JSON ver: {{"kalite_farki": 1-10 tam sayı (10 = aday referansla aynı/üstün kalitede, 1 = çok geride)}}"""
LOGO = ("ozgunluk", "akilda_kalicilik", "kucuk_okunurluk", "havali")  # --sema logo; sıvı/plastik alanları yok
FARK = 2  # puan farkı bu eşiğe ulaşırsa ya da bool'lar ayrışırsa AYRIŞTI
ZAMAN = 60  # istek başı sn


def veri_url(yol):
    im = Image.open(yol).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def tam(v):  # sayı dışı puan (metin, bool, ondalık) yanıt sayılmaz
    if type(v) is not int:
        raise ValueError(f"sayı değil: {v!r}")
    return v


def ayikla(y, logo=False, kiyas=False):
    m = re.search(r"\{.*?\}", y, re.S)
    if not m:
        raise ValueError("JSON yok")
    j = json.loads(m.group(0))
    if kiyas:
        return {"kalite_farki": tam(j["kalite_farki"])}
    if logo:
        return {k: tam(j[k]) for k in LOGO}
    return {"puan": tam(j["puan"]), "sivi_mi": bool(j["sivi_mi"]), "plastik_gorunen": bool(j["plastik_gorunen"])}


def aile_dene(aile, icerik, ref, logo):  # ilk çalışan aday kazanır; hiçbiri olmazsa kararsız (puan yok)
    for e in ADAY[aile]:
        try:
            return {"durum": "gecerli", "model": h.ad(e), **ayikla(h._istek(e, icerik, 4000 if ref else 400, ZAMAN), logo, bool(ref))}
        except (h.Hata, OSError, ValueError, KeyError, TypeError) as x:
            son = {"durum": "kararsiz", "model": h.ad(e), "sebep": f"{type(x).__name__}: {str(x)[:80]}"}
    return son


def haiku_gorsel(icerik):  # claude -p (abonelik), görüntü blokları stream-json ile; ANTHROPIC_API_KEY yok sayılır (ucretsiz_havuz._haiku ile aynı)
    blok = [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": c["image_url"]["url"].split(",", 1)[1]}}
            if c["type"] == "image_url" else {"type": "text", "text": c["text"]} for c in icerik]
    msg = json.dumps({"type": "user", "message": {"role": "user", "content": blok}}, ensure_ascii=False)
    env = {k: v for k, v in os.environ.items() if not k.startswith("ANTHROPIC_API_KEY")}
    h.DIZIN.mkdir(parents=True, exist_ok=True)
    p = subprocess.run(["claude", "-p", "--model", "claude-haiku-5-5", "--input-format", "stream-json", "--output-format", "stream-json", "--verbose",
                        "--max-turns", "1", "--tools", "", "--setting-sources", ""], input=msg, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=ZAMAN, creationflags=h.NW, cwd=h.DIZIN, env=env)
    j = next((x for x in map(json.loads, p.stdout.splitlines()) if x.get("type") == "result"), {"is_error": True, "result": p.stderr})
    if j.get("is_error") or not (j.get("result") or "").strip():
        raise h.Hata(0, "haiku " + str(j.get("result"))[:80])
    return j["result"].strip()


def gecerli_say(sonuc):
    return sum(v["durum"] == "gecerli" for v in sonuc.values())


def sor(png, soru, logo=False, ref=None):
    bicim = BICIM_KIYAS if ref else BICIM_LOGO if logo else BICIM
    icerik = [{"type": "text", "text": bicim.format(soru=soru)}]
    icerik += [{"type": "image_url", "image_url": {"url": veri_url(p)}} for p in ([ref] if ref else []) + [png]]
    sonuc, deneme = {}, 0
    for aile in ADAY:
        for _ in range(2):  # kararsız aile bir kez yeniden denenir, sonra sıradaki aileye geçilir
            if deneme == 4 or gecerli_say(sonuc) >= CIFT:  # en fazla 4 deneme
                break
            deneme += 1
            sonuc[aile] = aile_dene(aile, icerik, ref, logo)
            if sonuc[aile]["durum"] == "gecerli":
                break
    if gecerli_say(sonuc) < CIFT:  # iki aile toplanamadıysa Haiku görü tek oy
        try:
            sonuc["haiku"] = {"durum": "gecerli", "model": "haiku/claude-haiku-5-5", **ayikla(haiku_gorsel(icerik), logo, bool(ref))}
        except (h.Hata, OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as x:
            sonuc["haiku"] = {"durum": "kararsiz", "model": "haiku/claude-haiku-5-5", "sebep": f"{type(x).__name__}: {str(x)[:80]}"}
    return sonuc


def main():
    a = sys.argv[1:]
    soru = "Görsel gerçekçi bir sıvı (kahve/süt) gösteriyor mu, plastik/yapay mı görünüyor?"
    if "--soru" in a:
        i = a.index("--soru")
        soru = a[i + 1]
        del a[i:i + 2]
    ref = None
    if "--ref" in a:  # kıyas: --ref <referans.png>; PNG'ler aday, çıktı kalite_farki 1-10
        i = a.index("--ref")
        ref = a[i + 1]
        del a[i:i + 2]
        if "--soru" not in sys.argv:
            soru = "Aday, referansın görsel kalitesine (malzeme, ışık, derinlik, atmosfer) kıyasla kaç puan?"
    logo = "--sema" in a and a[a.index("--sema") + 1] == "logo"
    if logo:
        i = a.index("--sema")
        del a[i:i + 2]
        if "--soru" not in sys.argv:
            soru = "Bu logo özgünlük, akılda kalıcılık, 64px'te okunurluk ve 'havalı' olma açısından kaç puan?"
    for png in a:
        s = sor(png, soru, logo, ref)
        v = [d for d in s.values() if d["durum"] == "gecerli"]
        if not v:
            print(f"{Path(png).name} HAKEM YOK (görü uçlarının hiçbiri yanıtlamadı)")
            continue
        if len(v) < 2:
            durum = "TEK-AİLE"
        elif ref:
            durum = "AYRIŞTI" if abs(v[0]["kalite_farki"] - v[1]["kalite_farki"]) >= FARK else "UZLAŞTI"
            durum += f" ORT={sum(x['kalite_farki'] for x in v) / len(v):.1f}"
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
