# Unlimited-OCR kurulumu (23 Eki 2026)

- Kaynak: github.com/baidu/Unlimited-OCR (resmi, ★28k) @ 92ad94b (2026-10-12); model `baidu/Unlimited-OCR` HF sha 8249d20. Lisans: **MIT** (repo + model kartı).
- Konum: `C:\AI\unlimited-ocr` (`repo/` klon, `.venv` py3.12 + torch 2.10.0+cu128 + transformers 4.57.1, `model/` 6,4 GB bf16; yinelenen `model.safetensors` ve gif indirilmedi). README torch cu129 der; Windows'ta cu129 tekerleği yok, cu128 kullanıldı (çalışıyor).
- Tarama: gitleaks 0 sızıntı · semgrep p/python + p/security-audit 0 bulgu (`--config auto` metrics kapalıyken çalışmaz). Ağ: `infer.py` yalnız 127.0.0.1:10000 sglang sunucusuna konuşur (SGLang yolu kullanılmıyor); transformers yolu `trust_remote_code` ile `model/` içindeki .py'leri çalıştırır → `uocr.py` `HF_HUB_OFFLINE=1` ile koşar.
- Giriş: `tools/uocr.py` (sarmalayıcı; çağrıda yükle, bitince bırak, sürekli servis yok). Skill: `skills/unlimited-ocr`, zip: `dist/unlimited-ocr.zip` (zip_denetle temiz), CC kurulumu: `python onay/unlimited_ocr_uygula.py uygula`.

## A/B (RTX 4070 Ti 12 GB, GPU başka işlerle paylaşımlı; RapidOCR CPU'da çünkü onnxruntime CUDA sağlayıcısı yok)

| | Unlimited-OCR | RapidOCR (video_derin) |
|---|---|---|
| 20 kare (ig42 orta kareleri) | 1418 sn (≈71 sn/kare) | 116 sn (≈5,8 sn/kare) |
| 14 sayfalık PDF (200 dpi) | 1460 sn | 326 sn |
| PDF kelime kapsama (gömülü metin referansı, 1535 kelime) | **0,960** (fazla kelime 0,025) | 0,938 (fazla 0,053) |
| Tepe VRAM | 9,1–9,6 GB | — |
| Model yükleme | 8–46 sn | ~1,5 sn |

- Kare çıktıları: Unlimited-OCR sözcükleri doğru boşlukla ve belge yapısıyla (Markdown) verir; RapidOCR bitişik jeton üretir (`obsidianreplaced`). Karelerde insan referansı yok → kare doğruluğu sayısal ölçülmedi, yalnız çıktı farkı (ortak 216 / yalnız-rapid 197 / yalnız-uocr 173 anlamlı kelime, çoğu birleşik-jeton farkı).
- Kimlik: dikkat `eager` (flash-attn yok), `no_repeat_ngram` penceresi süreyi artırıyor (gundam: ngram 128 → 90 sn, ngram 0 → 68 sn; tek kare).
- **Karar:** `video_derin`'e eklenmedi, varsayılan değil: 12× yavaş, 9 GB VRAM, kare başına ek doğruluk kanıtı yok. Kullanım yeri: uzun/taranmış PDF, çok sütunlu/tablolu belge (`tools/uocr.py`). Ham çıktılar `.kos/kopru/rapor/uocr-ab/`.
- Tekrarlama: `python tools/uocr_ab.py` (kare + PDF A/B; PDF aşaması uzun, ~30 dk).
