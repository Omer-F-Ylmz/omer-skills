# Deneme: ucuz-tarayici

## Hipotez
video-tarayici (sonnet) çıktısı, ucuz kollarla aynı kalitede alınabilir; alınırsa kuyruğun (83 video) en büyük maliyet kalemi düşer. Kaynak fikir: L9c49WVG_ho (mekanik iş ucuz modele, yargı Claude'da).

## Metrik
kol başına token ve $ · rapor-denetle (tarama.denetle) · aday recall (sonnet adaylarına göre; ad eşleşmesi, kalan için Jev eslesme ≥0.6) · Site/UI ve prompt bölümü dolu mu · İDDİALAR sayısı.

## Kollar
- sonnet: video-tarayici alt ajanı (varsayılan; çıktısı resmi tarama, docs/video-tarama/2026-09-29-<id>.md)
- haiku: .claude/agents/video-tarayici-haiku.md (model: haiku) — ÖLÇÜLMEDİ: tanım oturum ortasında yüklenmedi (Agent type not found); oturum yenilenince `video tara <id> --kol haiku`
- openrouter:qwen/qwen3.8-27b:free — ücretsiz; görsel destekli, bağlam 262k, /models listesinde görsel+128k üstü ücretsizler içinde en güncel genel amaçlı (stealth/önizleme ve içerik-güvenlik modelleri elendi)
- openrouter:openai/gpt-6-luna-pro — ucuz güçlü; görsel destekli, bağlam 1.05M, $0.10/$0.50 /M (ucuz ve görsel listesinde güçlü sınıfın en ucuzu)

## Görevler
- Yunu27g7sLw (Parti E, 1b-2 sıra 14, uzun, 5 kare)
- _X_Seo1u9LM (Parti E, 1b-2 sıra 15, uzun, 6 kare)
- L9c49WVG_ho (kuyruk short, 1 kare)
- enFgYQvI1dM (kuyruk short, 2 kare)

## Tavan
alt ajan 8 (sonnet 4 + haiku 4) · OpenRouter 8 çağrı ve 1 dolar · Jev 80 · claude -p 0 · web 2. Kullanılan: sonnet 4 · haiku 0 · OpenRouter 8 tara çağrısı (10 HTTP: qwen 2×429 tekrar) · Jev 27 · claude -p 0 · web 0 (/models API 1).

## Karar ölçütü
takas tablosu (omer-kurallar 21, kur.takas): kalite düşüşü = max(1 − recall, denetim başarısızlık oranı; koşmayan video başarısız sayılır); tasarruf = aynı videolarda sonnet'e göre $ düşüşü (sonnet $ = alt ajan toplam token × girdi fiyatı, alt sınır). Kol başına AL/SOR/RED; tek eşik yok. İki OpenRouter kolu da görsel destekli, kareler gönderildi (short ≤3, uzun ≤6) → recall bölünmedi.

## Sonuç
| kol | video | token (girdi+çıktı) | $ | denetim | recall | Site/UI dolu | prompt dolu | İDDİALAR | karar |
|---|---|---|---|---|---|---|---|---|---|
| sonnet | Yunu27g7sLw | 38213 | $0.0764 | GEÇTİ | 1.00 (temel, 12 aday) | True | None | 8 | resmi |
| sonnet | _X_Seo1u9LM | 41748 | $0.0835 | GEÇTİ | 1.00 (temel, 10 aday) | True | None | 6 | resmi |
| sonnet | L9c49WVG_ho | 20649 | $0.0413 | GEÇTİ | 1.00 (temel, 9 aday) | None | None | 5 | resmi |
| sonnet | enFgYQvI1dM | 24106 | $0.0482 | GEÇTİ | 1.00 (temel, 5 aday) | None | None | 8 | resmi |
| openrouter:openai/gpt-6-luna-pro | Yunu27g7sLw | 23893+9146 | $0.0066 | 2 hata | 0.75 (9/12) | True | None | 15 | |
| openrouter:openai/gpt-6-luna-pro | _X_Seo1u9LM | 28409+11867 | $0.0082 | 10 hata | 0.60 (6/10) | True | None | 14 | |
| openrouter:openai/gpt-6-luna-pro | L9c49WVG_ho | 9728+5098 | $0.0034 | GEÇTİ | 0.89 (8/9) | None | None | 6 | |
| openrouter:openai/gpt-6-luna-pro | enFgYQvI1dM | 11385+5914 | $0.0040 | GEÇTİ | 0.60 (3/5) | None | None | 12 | |
| openrouter:qwen/qwen3.8-27b:free | Yunu27g7sLw | 5361+10010 | $0.0000 | 2 hata | 0.67 (8/12) | True | None | 10 | |
| openrouter:qwen/qwen3.8-27b:free | _X_Seo1u9LM | - | - | koşmadı (429) | - | - | - | - | - |
| openrouter:qwen/qwen3.8-27b:free | L9c49WVG_ho | 2598+2728 | $0.0000 | 8 hata | 0.00 (0/9) | None | None | 0 | |
| openrouter:qwen/qwen3.8-27b:free | enFgYQvI1dM | - | - | koşmadı (429) | - | - | - | - | - |
| **openrouter:openai/gpt-6-luna-pro** | toplam | | | başarısız 0.50 | 0.72 | | | | **SOR** — tasarruf 91.1 · düşüş 50.0 · düşüş >%20 & tasarruf ≥%50 |
| **openrouter:qwen/qwen3.8-27b:free** | toplam | | | başarısız 1.00 | 0.38 | | | | **SOR** — tasarruf 100.0 · düşüş 100.0 · düşüş >%20 & tasarruf ≥%50 |

Varsayılan tarayıcı DEĞİŞMEDİ (sonnet).
