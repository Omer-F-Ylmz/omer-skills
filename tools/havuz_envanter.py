"""HAVUZ-GENİŞ-1: canlı envanter. Her sağlayıcının /models listesi + her model için 1 metin ve 1 GÖRSEL deneme
→ .kos/kopru/havuz-envanter.tsv. Roller: G=görsel, K=kod, E=embedding/görüntü-gömme, TR=Türkçe. Anahtar değeri yazılmaz.
Kullanım: python -I tools/havuz_envanter.py   (anahtar yoksa halka 'anahtar yok' ile atlanır)"""
import base64, json, re, struct, sys, time, urllib.error, urllib.request, zlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import ucretsiz_havuz as H  # noqa: E402

KOK = Path(__file__).resolve().parents[1]
CIKTI = KOK / ".kos/kopru/havuz-envanter.tsv"
METIN = "Türkiye'nin başkenti neresidir? Tek cümleyle, Türkçe karakterlerle yanıtla."
GORSEL = "Bu görselin rengi nedir? Tek kelimeyle yanıtla."
# NVIDIA /models listesi (20 Eki 2026 canlı, 83 kimlik): sohbet, kod, görsel, gömme ve güvenlik modelleri birlikte denenir
NVIDIA = """01-ai/yi-large adept/fuyu-8b ai21labs/jamba-1.5-large-instruct aisingapore/sea-lion-7b-instruct bigcode/starcoder2-15b
databricks/dbrx-instruct deepseek-ai/deepseek-coder-6.7b-instruct deepseek-ai/deepseek-v4.1-flash google/codegemma-1.1-7b
google/codegemma-7b google/deplot google/diffusiongemma-26b-a4b-it google/gemma-2b google/gemma-3-12b-it google/gemma-3-4b-it
google/gemma-4-31b-it google/recurrentgemma-2b ibm/granite-3.0-3b-a800m-instruct ibm/granite-3.0-8b-instruct ibm/granite-34b-code-instruct
ibm/granite-8b-code-instruct meta/codellama-70b meta/llama-3.2-11b-vision-instruct meta/llama-3.2-90b-vision-instruct
meta/llama-guard-4-12b meta/llama2-70b meta/muse-glimmer-30b microsoft/kosmos-2 microsoft/phi-3-vision-128k-instruct
microsoft/phi-3.5-moe-instruct mistralai/codestral-22b-instruct-v0.1 mistralai/mistral-7b-instruct-v0.3 mistralai/mistral-large
mistralai/mistral-large-2-instruct mistralai/mixtral-8x22b-v0.1 moonshotai/kimi-k2.6 nv-mistralai/mistral-nemo-12b-instruct
nvidia/ai-synthetic-video-detector nvidia/cosmos-reason2-8b nvidia/embed-qa-4 nvidia/ising-calibration-1.5-31b
nvidia/llama-3.1-nemoguard-8b-content-safety nvidia/llama-3.1-nemoguard-8b-topic-control nvidia/llama-3.1-nemotron-51b-instruct
nvidia/llama-3.1-nemotron-70b-instruct nvidia/llama-3.1-nemotron-safety-guard-8b-v3 nvidia/llama-3.1-nemotron-ultra-253b-v1
nvidia/llama-3.2-nemoretriever-1b-vlm-embed-v1 nvidia/llama-3.2-nv-embedqa-1b-v1 nvidia/llama-nemotron-embed-vl-1b-v2
nvidia/llama3-chatqa-1.5-70b nvidia/mistral-nemo-minitron-8b-8k-instruct nvidia/nemotron-3-embed-1b
nvidia/nemotron-3-nano-omni-30b-a3b-reasoning nvidia/nemotron-3-super-120b-a12b nvidia/nemotron-3-ultra-550b-a55b
nvidia/nemotron-3.5-content-safety nvidia/nemotron-3.5-embed-1b nvidia/nemotron-3.5-embed-8b nvidia/nemotron-3.5-lightning-30b-a3b
nvidia/nemotron-3.5-super-vl-120b-a12b nvidia/nemotron-4-340b-instruct nvidia/nemotron-4-340b-reward nvidia/nemotron-nano-3-30b-a3b
nvidia/nemotron-parse nvidia/nemotron-parse-2.0 nvidia/neva-22b nvidia/nv-embedqa-mistral-7b-v2 nvidia/nvclip
nvidia/riva-translate-4b-instruct nvidia/riva-translate-4b-instruct-v2 nvidia/vila openai/gpt-oss-20b poolside/laguna-xs-2.1
snowflake/arctic-embed-l stepfun-ai/step-5-preview writer/palmyra-creative-122b writer/palmyra-fin-70b-32k writer/palmyra-med-70b
writer/palmyra-med-70b-32k z-ai/glm-5.3 z-ai/glm-5.3-flash zyphra/zamba2-7b-instruct""".split()


def _png(w=32, h=32):
    """Küçük kırmızı PNG (saf Python; Pillow gerekmez)."""
    raw = b"".join(b"\x00" + b"\xff\x00\x00" * w for _ in range(h))

    def parca(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + parca(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + parca(b"IDAT", zlib.compress(raw)) + parca(b"IEND", b""))


GORSEL_URL = "data:image/png;base64," + base64.b64encode(_png()).decode()


def _temiz(s):
    return str(s).replace("\t", " ").replace("\n", " ")[:90]


def _gonder(prov, model, icerik, max_tokens, zaman=90):
    """Tek çağrı → (metin|None, durum_kodu, not, hiz_basliklari). Anahtar değeri çıktıya girmez."""
    url, kaynak = H._url(prov), H.SAG[prov][1]
    if not url or not H._anahtar(kaynak):
        return None, -1, "anahtar yok", ""
    g = {"model": model, "messages": [{"role": "user", "content": icerik}], "max_tokens": max_tokens}
    if prov in H.DUSUNME and "gemma" not in model:
        g["reasoning_effort"] = "low"
    q = urllib.request.Request(url, json.dumps(g).encode(), {"Content-Type": "application/json", "User-Agent": "curl/8",
                                                            "Authorization": "Bearer " + H._anahtar(kaynak)})
    try:
        with urllib.request.urlopen(q, timeout=zaman) as f:
            j, hd = json.load(f), f.headers
    except urllib.error.HTTPError as x:
        return None, x.code, _temiz(H._gizle(x.read()[:200].decode("utf-8", "replace"))), _basliklar(x.headers)
    except (OSError, ValueError) as x:
        return None, 599, type(x).__name__, ""
    if j.get("error"):
        return None, 502, _temiz(H._gizle(str(j["error"])[:90])), _basliklar(hd)
    try:
        y = j["choices"][0]["message"].get("content")
    except (KeyError, IndexError, TypeError):
        return None, 502, "choices yok", _basliklar(hd)
    if not isinstance(y, str) or not y.strip():
        return None, 200, "bos", _basliklar(hd)
    return y.strip(), 200, "", _basliklar(hd)


def _basliklar(hd):
    return ";".join(f"{k}={v}" for k, v in hd.items() if "ratelimit" in k.lower() or "retry" in k.lower())[:120]


def _tara(satir):
    prov, model = satir
    t0 = time.time()
    m, kod, not_, hiz = _gonder(prov, model, METIN, 800)
    sn = round(time.time() - t0, 1)
    tr = "-" if m is None else ("iyi" if "Ankara" in m and re.search(r"[şğıçöü]", m) else "zayıf")
    g_kod, g_m, g_not = _gonder_gorsel(prov, model)
    roller = []
    if g_m and ("kırmız" in g_m.lower() or "red" in g_m.lower()):
        roller.append("G")
    if tr == "iyi":
        roller.append("TR")
    if re.search(r"code|coder|codestral|codegemma|starcoder|codellama", model):
        roller.append("K")
    if re.search(r"embed|retriever|clip", model):
        roller.append("E")
    if m is not None:
        roller.insert(0, "M")
    return [prov, model, kod, sn, tr, g_kod, _temiz(g_m or g_not), ",".join(roller) or "-", hiz, not_ or "-"]


def _gonder_gorsel(prov, model):
    icerik = [{"type": "text", "text": GORSEL}, {"type": "image_url", "image_url": {"url": GORSEL_URL}}]
    m, kod, not_, _ = _gonder(prov, model, icerik, 300)
    return kod, m, not_


def _liste(prov):
    url, kaynak = H._url(prov), H.SAG[prov][1]
    if not url or not H._anahtar(kaynak):
        return "anahtar yok"
    try:
        taban = url.rsplit("/chat/completions", 1)[0]
        # HAVUZ-GENIS-2: cloudflare /ai/v1/models yok (HTTPError) → /ai/models/search ("result"); github'da models.github.ai her yola 200 + gövde "OK" döner (ağ katmanı, 23 Eki doğrulandı)
        u = taban.replace("/ai/v1", "/ai/models/search?per_page=100") if prov == "cloudflare" else taban + "/models"
        r = urllib.request.Request(u, headers={"Authorization": "Bearer " + H._anahtar(kaynak), "User-Agent": "curl/8"})
        ham = urllib.request.urlopen(r, timeout=30).read()
        if ham.strip() == b"OK":
            return "liste:stub-OK"
        j = json.loads(ham)
        return len(j.get("data") or j.get("result") or [])
    except Exception as x:  # noqa: BLE001 - envanter: her hata satır olur
        return f"liste:{type(x).__name__}"


def main():
    isler = [("nvidia", m) for m in NVIDIA] + [(e.prov, e.model) for e in H.ENT if e.prov != "nvidia"]
    isler += [("nvidia", e.model) for e in H.ENT if e.prov == "nvidia" and ("nvidia", e.model) not in isler]
    sayilar = {p: _liste(p) for p in H.SAG}
    with ThreadPoolExecutor(max_workers=4) as ex:
        sonuc = list(ex.map(_tara, isler))
    satir = ["saglayici\tmodel\tmetin_kod\tgecikme_sn\tturkce\tgorsel_kod\tgorsel_yanit\troller\thiz_basliklari\tnot"]
    satir += [f"{p}\t(liste)\t-\t-\t-\t-\t-\t{sayilar[p]}\t-\t-" for p in H.SAG]
    satir += ["\t".join(map(str, s)) for s in sonuc]
    CIKTI.write_text("\n".join(satir) + "\n", encoding="utf-8")
    ozet = {}
    for s in sonuc:
        ozet.setdefault(s[0], [0, 0, 0])
        ozet[s[0]][0] += 1
        ozet[s[0]][1] += s[2] == 200
        ozet[s[0]][2] += "G" in s[7]
    print(f"yazıldı: {CIKTI.name} · denenen {len(sonuc)} model")
    for p, (n, ok, g) in ozet.items():
        print(f"{p}: denendi {n} · metin 200 {ok} · görsel {g} · liste {sayilar.get(p)}")


if __name__ == "__main__":
    main()
