"""BEYIN-KAYIT-1: ajan-sira işinin sonucunu Obsidian kasasına tarihli blok olarak yazar (Claude yok).
Kullanım:
  python tools/beyin_kayit.py <ajan-sira-adı>              ajan-sira sonucunu Obsidian'a özetler
  python tools/beyin_kayit.py olay <tur> <metin> [--hata]  2. beyne tek olay satırı (.kos/kopru/beyin-olay.jsonl); tur: ilerleme|hata|ders|maliyet
  (kalıcı ders: python tools/beyin.py kaydet <proje> "<metin>" --etiket ders|basari|karar)
Özet: ucretsiz_havuz (ücretsiz) → düşerse yerel Ollama. Aynı ad ikinci kez yazılmaz. Hata vermez, atlar."""
import hashlib
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
OLLAMA_MODEL = "qwen3.5:9b"  # 22 Eki: 4b disk temizliğinde silindi
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
             "options": {"num_ctx": 8192, "num_predict": 400},
             "keep_alive": 0}  # 22 Eki Ömer: llama-server (≈3.7 GB) yanıttan hemen sonra kapansın, RAM'de kalmasın
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


def kaydet(p, metin, etiket="ders"):
    """`beyin kaydet`: metni olduğu gibi 40-projeler/<p>.md'ye tarihli blok yazar; aynı metin 2. kez yazılmaz."""
    metin = metin.strip()
    if not metin:
        return "atla: metin boş"
    marker = f"<!-- beyin-kaydet:{hashlib.sha1(metin.encode('utf-8')).hexdigest()[:12]} -->"
    dosya = PROJELER / f"{p}.md"
    if dosya.exists() and marker in dosya.read_text(encoding="utf-8"):
        return f"zaten yazıldı: {p}"
    blok_yaz(dosya, etiket, marker, metin.splitlines(), f"# {p}\n")
    return f"yazıldı: {etiket} → {dosya.name}"


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


def cli(argv):
    if not argv or argv[0] in ("-h", "--help"):
        return "Kullanım" + __doc__.split("Kullanım", 1)[1].split("Özet:")[0].rstrip()
    if argv[0] == "olay" and len(argv) >= 3:
        sys.path.insert(0, str(KOK / "tools"))
        import beyin_dusun
        beyin_dusun.olay(argv[1], "claude", argv[2], hata="--hata" in argv[3:])
        return f"olay yazıldı: {argv[1]}"
    return main(argv[0])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print(cli(sys.argv[1:]))
