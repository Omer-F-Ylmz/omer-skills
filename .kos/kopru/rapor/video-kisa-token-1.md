# VİDEO-KISA-TOKEN-1 — ara rapor d1 (14 Eki ~16:15) — KABUL DEĞİL, ölçüm arka planda
Katalog: kullanılan [video CLI (hafif.cagir, tarama.sozluk_kur/eslestir, instagram.getir, cli._kullanici_env), ig-41 karar-birlesik.tsv, tools/ucuz_alt.py, gh api] · atlanan [plan-kur/katalog_ara (tek alan: video hattı kendi araçları yeterli), alt ajan (kural: 0)]

- M0 taban kaynağı: VİDEO-16 altın short kümesi (ig-DeW7JHrgsXb, ig-DeV9nZPtSsC, ig-DeHMM45NaFt), .kos/v16/{taban-1/2, low-ssb-1/2}.json — yeni claude -p yok. Taban = güncel varsayılan ssb (d9: 64 sn/video, $.087, çıktı 6.7k). `kisa_m4.py m0` video başı ağırlıklı jeton + kategori (metin · kare · sabit · rapor yazımı · araştırma 0) verir.
- M1: tools/video/video/kisa.py — Gemini (gemini-3.5-flash, yedek 2.5-flash; anahtar HKCU'dan, başlıkta) video + paket.md → gemini.json (şema: konusma_ozet, ekran_metni, araclar[{ad,ne_dedi,zaman}], linkler, komutlar, iddialar). Reel mp4 Files API, YouTube URL doğrudan, carousel görseller satır içi + slayt videoları + paket OCR. Duman: ig-DeW7 20.2 sn, 4 araç, `pip install airllm` yakalandı.
- M2: katalog() = ig-41 kararı > kurulu sözlük > bilinmeyen; bilinmeyen → repo_bul (link ya da gh arama, "doğrulanmadı" işaretli) + arastir (gh künye + README özeti ucuz_alt/OmniRoute; repo başı önbellek .kos/kopru/video/kisa/arastirma/).
- M3: oturum() tek claude -p (hafif.cagir, efor low) ≥8 videonun Gemini JSON'u + katalog → rapor araç başı 2 satır.
- Ölçüm: `kisa_m4.py kos` arka planda (8 video: 3 altın + 4 reel + 1 carousel; claude -p 1/4). Günlük .kos/kopru/video/kisa_kos.log.
- Test: tests/test_kisa.py 3/3 yeşil.
- Kalan: M4 puan (kapı), M5 skill + zip → devir/video-kisa-token-1-devam.md.
- d2 (16:45): fallback 2.5-flash emekli (404 'no longer available to new users') → 3.8-flash; hata gövdesi günlükte; kisa.calistir + `video kisa` + SKILL.md bölümü + zip TEMİZ. kos 3. videoda 3.5-flash zaman aşımıyla düştü → devir.

## d5 (14 Eki 18:00): recall artışı, ATLAS sözlüğü + paralel Gemini metin geçişi
- Kaçak analizi (kisa_m4.py kacak): d4 kaçaklarının çoğu pakette yazılı (pip, npm, Browser Use, Featherless, GliFormer, Llama); kalanı kavram ("Katman katman yükleme") ya da ad varyantı ("jev (GliFormer)").
- kisa.sozluk_tara: paket.md n-gram ∩ ATLAS envanter adları; videonun kendi raporundan gelen satır sayılmaz (sızıntı), belge sıklığı %20'yi aşan ad genel kelime sayılır. kisa.metin_gec: yalnız metin üzerinde çalışan Gemini (lite, ~2–7 sn, ücretsiz) adayları süzer, birlestir ile eklenir; izle ile paralel koşar. katalog() ATLAS'ı da tanır (bilinen 153/181).
- DF ≤%1 denemesi geri alındı: lite aday dışındaki sık adları (pip, npm, Llama) bıraktı.
- Ölçüm normalleştiricisi: "X (Y)" / "X, powered by Y" biçiminde çekirdek ad da eşleşir (tüm kollara eşit).

| kol | araç_yak | link_yak | yp/video | ağır_tk/video | sn/video |
|---|---|---|---|---|---|
| taban (1+2 ort.) | 0.850 | 0.584 | 0 | 236 348 | 131.5 |
| low-ssb (1+2 ort.) | 0.641 | 0.179 | 0 | 43 279 | 64.2 |
| yeni d5 | 0.861 | 0.449 | 0 | 10 020 (0.04×) | 32.7 (0.25×) |
| yeni d6 (link_tamamla) | 0.861 | 0.475 (temiz 0.600) | 0 | 10 020 (0.23× low-ssb) | 32.7 (0.51× low-ssb) |

- d6: link kaçakları — DeV9'da 4/4 referansın kendi "ocr bozuk" dediği adresler, DeHMM'de 3 kırpık HF + 3 Claude web aramasıyla bulunmuş repo. Kök: karar dosyasında "KUR" olan Laya bilinen sayılıp araştırılmadığı için repo linki rapora girmiyordu → kisa.link_tamamla (ig-41 link sütunu + videonun kendi linkinden bulunan repo; gh arama tahmini yazılmaz). "link_temiz" = referansın bozuk/kırpık işaretlediği adresler hariç, tüm kollara eşit. Önizleme yeni claude -p'siz (son işlem Claude çıktısına deterministik).
- Ömer 17:38 kapısı (low-ssb'ye göre): araç 0.861 ≥0.80 ✓ · link 0.475 ≥0.179 ✓ · yp 0 ✓ · token 0.23× ✓ · süre 0.51× ✗ (sınır 32.1 sn, aşım 0.6 sn/video; low-ssb-1'e göre 0.485×, low-ssb-2'ye göre 0.535×). Süre kökü: önbellekteki Gemini izleme süresi 17–32 sn (iki flash 503 → lite düşüşü dahil). Eski taban (sonnet+haiku) linkine göre 0.475 < 0.584 — Desktop kararı.
## d12–d13 (14 Eki 21:45, claude -p 0): Claude'suz çıkarım kapısı (Desktop 20:58) — sınama araç 0.944 < 0.95, KAPI GEÇMEDİ (ara)
| kol | altın araç | altın link | sınama araç | sınama link | yp | Claude tk/video | sn/video (8'li) |
|---|---|---|---|---|---|---|---|
| low-ssb (1/2) | 0.5 / 0.333 | 0.268 / 0.418 | – | – | 0 | 47 445 / 39 113 | 67.4 / 61.1 |
| yeni d12a / d12b | 1.0 / 1.0 | 0.85 / 0.85 | 0.944 / 0.944 | 1.0 / 1.0 | 0 | 0 (Claude adımı TOKEN-2'de) | 11.95 / 12.58 |
- Tekrarlar arası oynama yok (temp0+seed+tavan); d13a (DF 0.2 metin geçişi yeniden) yine 0.944. Sınama 6'lıda sn/video 17–20 (8'li partide ≤15 ✓). Flash modelleri günlük kotada (429) → hepsi lite; lite tek başına 1–2 sn, koşudaki ~31 sn metin süresi tavan kuyruğu + 429 sekmeleri.
- 9 kaçak: platform/dil (GitHub, Claude, Go, S3, .TECH — sözlük DF>%20 ile aday dışı) · gerçek (Sales Navigator, agenthubstack.dev — açıklamada; RustFS — OCR'da compose dosya adı) · ref gürültüsü (Bytebase — star-history sayfasının sponsor linki).
- Denenip REDDEDİLEN (kodda yok): (1) DF_TAVAN 1.0 → aday 2× → lite gerçek adları bıraktı, sınama 0.796 · (2) tüm link alan adları → araç: 0.950'ye çıkardı ama OCR bozuk licdn/logo şirketi gürültüsü (DYKS +18, DeV9 +13); yp metriği pakette geçen adı saymadığından metrik oyunu.
- Öneri (TOKEN-2'ye): DF'si yüksek ama ürün olan adlar için ayrı kısa "platform listesi" (GitHub, Claude, Go, S3…) metin geçişine aday değil ayrı satır olarak; açıklama bölümündeki alan adları (yalnız ## Açıklama) araç adayı.
- d7 (18:50): Ömer 18:25 kapısı (araç ≥0.90, link ≥0.584, yp 0, tk ≤0.04×, toplu ≤10 sn/video) için kod hazır (teknikler alanı, kurulum komutu, OCR GitHub başlığı + gh doğrulama, düşük çözünürlük/fps, videolar arası paralel); ölçüm RAM %93 yüzünden koşulmadı → devir d7.
