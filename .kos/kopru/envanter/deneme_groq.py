"""ENVANTER-KULLAN-1: OmniRoute üstünden en fazla 2 ücretsiz Groq çağrısı (metin combo + Llama 4 Scout görsel)."""
import base64, json, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, r"C:\Projeler\omer-skills\tools")
import ucuz_alt  # anahtar() + iste() — UA düzeltmesi dahil

E = Path(__file__).parent
ocr = (E / "deneme_gorsel.txt").read_text(encoding="utf-8").split("## rapidocr")[1].split("## ollama")[0]
kare = Path(sys.argv[1])
istem = "Yalnız marka/ürün/araç adlarını satır satır yaz, başka bir şey yazma."
denemeler = [
    ("groq llama-3.3-70b (metin, OCR üstü)", {"model": "groq/llama-3.3-70b-versatile", "max_tokens": 300,
                                         "messages": [{"role": "user", "content": istem + "\nOCR:\n" + ocr}]}),
    ("groq llama-4-scout (görsel)", {"model": "groq/meta-llama/llama-4-scout-17b-16e-instruct", "max_tokens": 300,
                                     "messages": [{"role": "user", "content": [
                                         {"type": "text", "text": istem},
                                         {"type": "image_url", "image_url": {"url": "data:image/png;base64," + base64.b64encode(kare.read_bytes()).decode()}}]}]}),
]
sonuc = []
for ad, g in denemeler:
    t = time.time()
    try:
        q = urllib.request.Request(ucuz_alt.URL, json.dumps(g).encode(), {
            "content-type": "application/json", "authorization": f"Bearer {ucuz_alt.anahtar()}",
            "user-agent": "omer-skills-ucuz-alt/1"})  # Groq 403 vermesin diye UA
        d = json.load(urllib.request.urlopen(q, timeout=90))
        s = f"model={d.get('model')} jeton={d.get('usage', {}).get('total_tokens')}\n" + d["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        s = f"HATA {e.code}: {e.read().decode(errors='replace')[:300]}"
    except Exception as e:
        s = f"HATA {type(e).__name__}: {str(e)[:200]}"
    sonuc.append(f"## {ad} ({time.time() - t:.1f}s)\n{s.strip()[:800]}")
(E / "deneme_groq.txt").write_text("\n".join(sonuc) + "\n", encoding="utf-8")
print("\n".join(sonuc))
