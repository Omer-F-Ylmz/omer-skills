"""Ücretsiz görü hakemi: her PNG'ye aynı soru, iki aile; JSON {puan, sivi_mi, plastik_gorunen}; aileler ayrışırsa AYRIŞTI.
python gorsel_hakem.py <png...> --soru "<metin>"   (çıktı: PNG başına 1 satır; ayrışan görseli Desktop kendisi inceler)"""
import base64
import hashlib
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

# aile → görü yetenekli adaylar (ilk çalışan kazanır); havuz ENT'i görü türü taşımadığı için burada ayrı.
# HAVUZ-GENİŞ-1 canlı envanter (.kos/kopru/havuz-envanter.tsv, G rolü 200 + doğru renk): gemini · nvidia · groq · openrouter · mistral.
# meta/llama-3.2-11b-vision görüntüyü kabul etti ama "Beyaz" dedi → aday değil.
ADAY = {"google": [h.E("gemini", "gemini-3.5-flash-lite", "google", None, 10, 200_000, 200, 900_000, ()),
                   h.E("gemini", "gemini-3.6-flash", "google", None, 5, 200_000, 100, 900_000, ())],
        "nvidia": [h.E("nvidia", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning", "nvidia", None, 30, 100_000, 1000, 100_000, ()),
                   h.E("openrouter", "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free", "nvidia", "openrouter", 18, 10**6, 900, 100_000, ())],
        "alibaba": [h.E("groq", "qwen/qwen3.8-27b", "alibaba", None, 25, 6000, 800, 4500, ())],
        "minimax": [h.E("openrouter", "minimax/minimax-m3.1-flash:free", "minimax", "openrouter", 18, 10**6, 900, 100_000, ())],
        "mistral": [h.E("mistral", "ministral-8b-latest", "mistral", None, 30, 100_000, 1000, 100_000, ())]}
CIFT = 3  # en az 3 aile aynı görsele oy verir; altı → Haiku tek oy (TEK-AİLE)
ONBELLEK = h.DIZIN / "hakem-onbellek.json"  # aynı görsel + istem → önceki sonuç (yalnız ≥1 geçerli oy olanlar)
BICIM = """Bu görseli değerlendir. Soru: {soru}
Yalnız tek satır JSON ver: {{"puan": 0-10 tam sayı, "sivi_mi": true/false, "plastik_gorunen": true/false}}"""
BICIM_LOGO = """Bu bir kişisel logo (monogram). Soru: {soru}
Yalnız tek satır JSON ver: {{"ozgunluk": 1-10, "akilda_kalicilik": 1-10, "kucuk_okunurluk": 1-10, "havali": 1-10}}"""
BICIM_KIYAS = """İlk görsel REFERANS, ikinci görsel ADAY. Soru: {soru}
Yalnız tek satır JSON ver: {{"kalite_farki": 1-10 tam sayı (10 = aday referansla aynı/üstün kalitede, 1 = çok geride)}}"""
LOGO = ("ozgunluk", "akilda_kalicilik", "kucuk_okunurluk", "havali")  # --sema logo; sıvı/plastik alanları yok
FARK = 2  # puan farkı bu eşiğe ulaşırsa ya da bool'lar ayrışırsa AYRIŞTI
ZAMAN = 60  # istek başı sn
ENT = {h.ad(e): e for l in ADAY.values() for e in l}


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


KALIB = h.DIZIN / "hakem-kalib.json"  # model → {lo, hi}: ankraj görsellerine verdiği ham puanlar (ölçek kalibrasyonu)
VARSAYIM_SORU = "Görsel kalitesi (malzeme, ışık, derinlik, gerçekçilik) kaç puan?"


def ankraj_url(iyi):  # düşük = düz gri; yüksek = ışıklı, gölgeli küre (prosedürel ankraj, repoya bağımlı değil)
    im = Image.new("RGB", (512, 512), (128, 128, 128))
    if iyi:
        px = im.load()
        for y in range(512):
            for x in range(512):
                px[x, y] = (40 + y // 8, 45 + y // 8, 60 + y // 6)
                dx, dy = (x - 256) / 150, (y - 230) / 150
                r2 = dx * dx + dy * dy
                if r2 < 1:
                    l = max(0.0, (-dx * 0.5 - dy * 0.6 + (1 - r2) ** 0.5 * 0.62))
                    px[x, y] = (int(230 * l ** 0.8) + 15, int(120 * l ** 0.8) + 10, int(70 * l ** 0.8) + 8)
                elif abs(dx) < 2.2 and dy > 1.0 and dy < 1.5:
                    px[x, y] = (int(px[x, y][0] * 0.55), int(px[x, y][1] * 0.55), int(px[x, y][2] * 0.55))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def kalib(e):  # model başına bir kez: düz gri (lo) ve ışıklı küre (hi) ham puanı; başarısızsa None
    kay = json.loads(KALIB.read_text(encoding="utf-8")) if KALIB.exists() else {}
    ad = h.ad(e)
    if ad in kay:
        return kay[ad]
    try:
        ham = [ayikla(h._istek(e, [{"type": "text", "text": BICIM.format(soru=VARSAYIM_SORU)}, {"type": "image_url", "image_url": {"url": ankraj_url(i)}}], 400, ZAMAN))["puan"] for i in (False, True)]
    except (h.Hata, OSError, ValueError, KeyError, TypeError):
        return None
    kay[ad] = {"lo": ham[0], "hi": ham[1]}
    h.DIZIN.mkdir(parents=True, exist_ok=True)
    KALIB.write_text(json.dumps(kay), encoding="utf-8")
    return kay[ad]


def norm100(e, puan):  # ham puan → 0-100: ankraj (düz gri → ışıklı küre) aralığı doğrusal eşlenir; ankrajı ayıramayan/ters sıralayan aile None (atlanır)
    k = kalib(e)
    if not k or k["hi"] - k["lo"] < 2:
        return None
    return max(0.0, min(100.0, (puan - k["lo"]) / (k["hi"] - k["lo"]) * 100))


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
    anahtar = hashlib.sha256(json.dumps(icerik, ensure_ascii=False).encode()).hexdigest()
    onb = json.loads(ONBELLEK.read_text(encoding="utf-8")) if ONBELLEK.exists() else {}
    if anahtar in onb:
        return onb[anahtar]
    sonuc, deneme = {}, 0
    for aile in ADAY:
        for _ in range(2):  # kararsız aile bir kez yeniden denenir, sonra sıradaki aileye geçilir
            if deneme == 6 or gecerli_say(sonuc) >= CIFT:  # en fazla 6 deneme
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
    if gecerli_say(sonuc):
        onb[anahtar] = sonuc
        ONBELLEK.write_text(json.dumps(onb, ensure_ascii=False), encoding="utf-8")
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
            kf = [x["kalite_farki"] for x in v]
            durum = "AYRIŞTI" if max(kf) - min(kf) >= FARK else "UZLAŞTI"
            durum += f" ORT={sum(kf) / len(v):.1f}"
        elif logo:
            durum = "AYRIŞTI" if any(max(x[k] for x in v) - min(x[k] for x in v) >= FARK for k in LOGO) else "UZLAŞTI"
        else:
            durum = "AYRIŞTI" if any(len({x[k] for x in v}) > 1 for k in ("sivi_mi", "plastik_gorunen")) else "UZLAŞTI"
            nv = [n for n in (norm100(ENT[x["model"]], x["puan"]) for x in v if x["model"] in ENT) if n is not None]  # haiku ENT'te yok; kalibrasyonsuz aile atlanır
            durum += f" NORM={sum(nv) / len(nv):.0f}/{len(nv)}aile" if len(nv) >= 2 else " NORM=YOK(<2 aile)"
            if len(nv) >= 2 and max(nv) - min(nv) >= 30:  # normalize sonrası da 30+ puan fark → aileler gerçekten ayrışıyor
                durum = "AYRIŞTI" + durum[len(durum.split()[0]):]
        if logo:
            ort = sum(x[k] for x in v for k in LOGO) / (len(v) * len(LOGO))
            durum += f" ORT={ort:.2f}"
        print(f"{Path(png).name} {durum} " + json.dumps({k: {x: y for x, y in d.items() if x != "model"} for k, d in s.items()}, ensure_ascii=False)
              + " " + ",".join(d["model"] for d in s.values()))


main()
