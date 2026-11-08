# DISK-SIL-1 (YARIM — kanca engeli)
C: boş: başlangıç 108,23 GB; 183,29 GB (HF silmesinden sonra). Not: ~70 GB artış uv'den değil; uv önbelleği hâlâ 71,94 GB (başka süreç boşalttı, kaynağı ölçülemedi).

## 1 uv önbelleği
`uv cache clean` kilit zaman aşımı (300 sn); arka işte UV_LOCK_TIMEOUT=1200 ile yeniden denendi (bpwea6htw), "Cache is currently in-use" bekliyor. Süreç öldürülmedi. Sonuç: DEVAM, henüz silinmedi.

## 2 C:\AI\indirilen
42,7 GB'ın büyük kısmı git klonları (>50 MB arşiv/ağırlık dosyası YOK, üst düzeyde dosya YOK).
| kalem | karar |
|---|---|
| invoiceninja__invoiceninja.part 0,05 · NousResearch__hermes-agent.part 0,07 · ToolJet__ToolJet.part 0,78 · twentyhq__twenty.part 0,15 · _deneme_twenty.part 0,48 | (c) yarım indirme → silinecekti; Remove-Item PreToolUse kancası (block-destructive.ps1) "DUR: kullanıcı onayı gerek" ile ENGELLEDİ; atlatılmadı. ~1,53 GB bekliyor |
| diğer klonlar (video-izle-kur-1 3,97 · ToolJet 2,42 · Infisical 2,35 · remotion 1,26 · MassGen 1,14 …) | a/b/c'ye uymuyor → silinmedi |

## 3 Hugging Face
Silindi (`hf cache rm`, kullanan hat yok: repoda referans 0): ResembleAI/chatterbox 3,2 GB · tts-hub/XTTS-v2 1,9 GB = 5,1 GB.
Tutulan (27,6 GB, hepsi ≤1 gün erişim + hat kullanımı): Hunyuan3D-2 9,9 · Hunyuan3D-2mini 7,6 · faster-whisper large-v3 3,1/turbo 1,6/medium 1,5/small 0,49/tiny 0,08/tiny.en 0,08 · laya 2,4 · Kokoro-82M 0,33 · kompress-v2-base 0,27 · siglip 0,10 · MiniLM-onnx 0,09 · technique-router 0,03 · ModernBERT 0,002 · Xenova/gpt-4 0,004 · Qwen-7B ~0.
