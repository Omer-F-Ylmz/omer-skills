# VIDEO-HIZ-4 TUR 4 — TUR BITTI (hız 400 kapısı geçmedi; toplu koşu YOK, push yok)
- Ölçüm (40 shorts, 39/40 json): es 3 nefes 0,33 = 368/sa (TUR 3); es 4 = 326/sa, RAM tepe %88; es 3 nefes 0,12 = 343/sa, RAM %86. GPU tepe hepsinde %100 (1 sn örnek), VRAM %60.
- Sonuç: es artırmak ve GPU nefesini kısmak hız vermiyor (ölçüm gürültüsü ±%7); tavan bu makinede ~330–370/sa. Darboğaz: OCR+ASR GPU kilidinde sıralı (aşama toplamı ocr 1156 · asr 1033 · asr_gpu 415 · indir 281 sn).
- Varsayılan değişmedi (es 3). Kod değişikliği yok. 400 için gereken: OCR'yi kareden azaltma (yazı ön sınıflandırıcı) — recall riski, ölçülmedi.

# VIDEO-HIZ-4 TUR 3 — TUR BITTI (hız 400 kapısı geçmedi: 368/sa; toplu koşu YOK, push yok)
- (1) KÖK NEDEN (kanıtlı): boş-ASR + link kaçağı. `-S lang` ile yt-dlp HLS (m3u8) video 229 + 251-7 sesi seçti, mkv birleştirme "unknown timestamp" ile düştü; indir() yalnız-video `v.f229.mp4`'i aldı → ses yok → asr "yok". Düzeltme: format `[protocol^=http]` (HLS dışı) + indir() `v.f<id>` parçalarını seçmez. 6/6 boş-ASR video yeniden koşuldu, hepsi segmentli.
- Link/komut kalan tek kaçak (TixdV5DP7oc): KOMUT_RE `claude\s+.+` düz cümleyi ("Claude just killed…") komut sayıyordu. `claude` yalnız alt komut/bayrakla (mcp, plugin, code, doctor, update, config, install, agents, login, -, /) eşleşir. Sonuç: link/komut 37/37 (%100).
- (2) RAM: es 3 (TUR 2: es 6) → RAM tepe %84 (≤%89 ✓), VRAM tepe %60. Hız 40 shorts 372 sn, 9,8 sn/link = 368 video/sa (TUR 2: 239). 38/40 json (eQKZsCL_4DQ, zcoUIECwS_s yok: ref2'de de hatalıydı). Kapı 400 geçmedi; es 4 denenmedi.
- (3) GPU: tepe hâlâ %100 (1 sn örnek), işçi içi %75 kısma EKLENMEDİ (yapılmadı) — (b) çözülmedi.
- (4) ASR (ref2, N=37): ort 0,935, ≥0,96 18/37 (önce 14/38), ≥0,90 32/37. Kalan fark gerçek ASR değişkenliği (konuşma dili Türkçe "yakıyoruz/yükülüyoruz", atlanan 8 kelimelik parça; "7000" vs "7 bin" gibi yazım), normalizasyon uygulanmadı, metrik gevşetilmedi.
- OCR sabit geri çağırım 37/37 ≥0,98 (ham 0,947); kapı ≥%96 ✓.
- Sapma: Roast Room, envanter_tara, GPU kısma, es 4 ve uzun video ölçümü 40 tur bütçesi nedeniyle yapılmadı. Sonraki: es 4 + RAM tepe, GPU işçi içi kısma, ASR tutarsızlığı için tekrar-koşu varyansı.
