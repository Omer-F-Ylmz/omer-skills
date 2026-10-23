---
name: unlimited-ocr
description: "Baidu Unlimited-OCR (3B, MIT): uzun PDF/çok sayfalı belge ve ekran görüntüsünü Markdown'a çevirir. Yerel GPU'da koşar (CC'de doğrudan, Desktop'ta cc-kopru ile); claude.ai sandbox'ında koşmaz."
---

# unlimited-ocr — uzun belge / ekran görüntüsü OCR (yerel GPU)

Model: `baidu/Unlimited-OCR` (MIT). Ortam `C:\AI\unlimited-ocr` (.venv + model). Servis yok: her çağrıda yüklenir, bitince GPU boşalır.
Gerekir: NVIDIA GPU ≥ ~8 GB boş VRAM. claude.ai sandbox'ında (GPU/ağ/model yok) koşmaz.

## Kullanım

```text
python tools/uocr.py belge.pdf --cikti belge.md        # PDF → infer_multi (sayfalar arası bağlam), --dpi 200 varsayılan
python tools/uocr.py kare1.jpg kare2.jpg               # her görsel ayrı infer, "## ad" başlıklı Markdown
python tools/uocr.py s1.png s2.png s3.png --cok        # tüm görseller tek çok-sayfa çağrısı
```

stderr'de `uocr: {"yukle_s":…, "infer_s":…, "tepe_vram_mb":…}`. Çıktı stdout'a ya da `--cikti` dosyasına.

## Desktop (cc-kopru)

```
komut(arac="python", args=["tools/uocr.py", "C:/Projeler/<proje>/belge.pdf", "--cikti", "C:/Projeler/<proje>/belge.md"], cwd="C:/Projeler/omer-skills")
```

Çıktı 8 KB'i aşarsa `--cikti` ver, dosyayı Read ile dar aralıkta oku.

## Ne zaman

- Uzun/çok sütunlu PDF, tablo, formül, taranmış belge → Unlimited-OCR.
- Videodan düz ekran yazısı/altyazı (çok sayıda kare) → `tools/video_derin.py` (RapidOCR) hızlıdır; A/B sonucu için `docs/kurulumlar/unlimited-ocr.md`.
- Doğuştan metinli (born-digital) PDF → `markitdown` / PyMuPDF yeter, OCR gerekmez.
