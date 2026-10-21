"""BEYIN-KAYIT-1: ajan-sira işinin sonucunu Obsidian kasasına tarihli blok olarak yazar (Claude yok).
Kullanım: python tools/beyin_kayit.py <ajan-sira-adı>
Özet: ucretsiz_havuz (ücretsiz) → düşerse yerel Ollama. Aynı ad ikinci kez yazılmaz. Hata vermez, atlar."""
import json
import sys
import time
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
CIKTI = KOK / ".kos" / "kopru" / "ajan-sira"
KASA = Path(r"C:\Users\pc\Desktop\Obsidian")
PROJELER = KASA / "40-projeler"
KARARLAR = KASA / "10-kararlar" / "Kararlar.md"
PROJE_ANAHTAR = {"kurulum-video": "KURULUM-VIDEO", "telve": "TELVE", "neffex": "NEFFEX", "oktan": "OKTAN", "mucevher": "mücevher"}
OLLAMA = "http://127.0.0.1:11434/api/chat"
OLLAMA_MODEL = "qwen3.5:4b"
ISTEM = ("Aşağıdaki iş sonucunu Türkçe, en fazla 4 satırda özetle. Her satır şu etiketle başlasın: "
         "commit: (hash ya da -), ne bitti: , ★: (kalite/ölçü ya da -), karar: (varsa ya da -). Başka metin yazma.\n\n")


def proje(ad):
    for on, p in PROJE_ANAHTAR.items():
        if ad.startswith(on):
            return p
    return "omer-skills"


def sonuc(ad):
    """claude -p JSON'unun son '{' satırındaki result metni; yoksa ''."""
    for s in reversed((CIKTI / f"{ad}.json").read_text(encoding="utf-8", errors="replace").splitlines()):
        if s.startswith("{"):
            return json.loads(s).get("result") or ""
    return ""


def yerel(istem):
    govde = {"model": OLLAMA_MODEL, "messages": [{"role": "user", "content": istem}], "stream": False, "think": False,
             "options": {"num_ctx": 8192, "num_predict": 400}}
    istek = urllib.request.Request(OLLAMA, json.dumps(govde).encode("utf-8"), {"Content-Type": "application/json"})
    with urllib.request.urlopen(istek, timeout=120) as r:
        return json.loads(r.read())["message"]["content"]


def ozetle(metin):
    """Ücretsiz havuz; düşerse yerel Ollama. Claude/Haiku yok. En fazla 5 satır döner."""
    istem = ISTEM + metin[:12000]
    y = None
    try:
        sys.path.insert(0, str(KOK / "tools"))
        import ucretsiz_havuz as H
        y, _, _ = H.cagir("ozet", istem, max_tokens=600, haiku_tavan=0, etiket="beyin-kayit",
                          dogrula=lambda t: None if t and t.strip() else "bos")
    except Exception:
        y = None
    if not y:
        try:
            y = yerel(istem)
        except (OSError, ValueError, KeyError):
            return []
    return [s.strip() for s in y.splitlines() if s.strip()][:5]


def blok_yaz(dosya, ad, marker, satirlar, baslik):
    dosya.parent.mkdir(parents=True, exist_ok=True)
    yeni = not dosya.exists()
    with open(dosya, "a", encoding="utf-8", newline="\n") as f:
        if yeni:
            f.write(baslik)
        f.write(f"\n## {time.strftime('%Y-%m-%d')} · {ad}\n{marker}\n" + "\n".join(f"- {s}" for s in satirlar) + "\n")


def main(ad):
    marker = f"<!-- beyin-kayit:{ad} -->"
    p = proje(ad)
    not_ = PROJELER / f"{p}.md"
    if not_.exists() and marker in not_.read_text(encoding="utf-8"):
        return f"zaten yazıldı: {ad}"
    try:
        metin = sonuc(ad)
    except (OSError, ValueError) as x:
        return f"atla {ad}: {type(x).__name__}"
    if not metin.strip():
        return f"atla {ad}: sonuç boş"
    satirlar = [s.lstrip("-*• ").strip() for s in ozetle(metin)]
    if not satirlar:
        return f"atla {ad}: özet alınamadı (havuz ve yerel kapalı)"
    blok_yaz(not_, ad, marker, satirlar, f"# {p}\n")
    karar = next((s for s in satirlar if s.lower().startswith("karar:")), "")
    if karar.split(":", 1)[-1].strip() not in ("", "-"):
        blok_yaz(KARARLAR, ad, marker, [karar], "# Kararlar\n")
    return f"yazıldı: {ad} → {not_.name}"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(main(sys.argv[1]))
