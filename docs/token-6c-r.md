# TOKEN-6c-R: recap ölçümü

Salt okuma dalgası (2026-10-03 19:20). Ayar, hook ve Headroom değiştirilmedi; claude -p 0. Veri `olcum/token-6c-r.json`, betik scratchpad'de (`k6cr.py`). Kırılma mantığı `token_olc.ttl_sim` ile aynı (yalnız etkileşimli · ana); sınıflama H2 yöntemiyle yapıldı (PERF satırı, cr+cw birebir, +03, ±2 sn).

## Pencereler
- R, recap kapalı: 10-03 18:49:58 → 19:2x. 4–60 dk bandında n=1. Kapı (<30 çift) beklendiği gibi kapalı, R karşılaştırması yapılmadı.
- (b), recap açık, log tam: 10-01 04:03 → 10-03 17:33:58 (bakT6c CreationTime).
- (a), 14 gün: yalnız bilgi için. 10-01 04:03'ten (log başlangıcı) önceki kırılmaların PERF karşılığı yok, kanıtsız sayıldı.

## (b) 4–60 dk sınıf tablosu
n=108 çift, 41 kırılma. 41'in hepsi Headroom dönüşümü (read_maturation / kompress_background). Diğer sınıflar 0: oturum eylemi, tool_search_deferral, araç listesi, diğer, kanıtsız. "Diğer" oranı tool_search_deferral dahil de hariç de %0. Ağırlıklı maliyet ve $ json'da.

## Doğrudan recap testi: 4–60 dk çiftleri, aralarında away_summary var/yok

| pencere | bant | away var | away yok |
|---|---|---|---|
| (b) | 4–60 | 33/43 %76.7 | 8/65 %12.3 |
| (b) | 4–10 | 13/18 %72.2 | 4/55 %7.3 |
| (b) | 10–60 | 20/25 %80.0 | 4/10 %40.0 |
| (b) | 4–60, Headroom hariç | 0/10 | 0/57 |
| (a) | 4–60 | 60/85 %70.6 | 32/207 %15.5 |
| (a) | 4–10 | 19/34 %55.9 | 7/144 %4.9 |

4–10 dk alt bandı boşta kalma süresini sabit tutuyor ve fark orada da yaklaşık 10 kat. Fark yalnız uzun boşluktan gelmiyor.

## Hüküm
- Kural: iki grupta da n ≥ 10 ve fark ≥ 2 kat → **recap kırıyor. Recap kapalı kalır, deneme biter.** (b): 43 / 65, %76.7 / %12.3.
- Mekanizma: recap'li kırılmaların hepsi Headroom etiketli. Headroom hariç tutulunca kırılma 0/10. Yani away_summary önbelleği tek başına kırmıyor; kırılma Headroom'un tam yeniden yazmasıyla geliyor (H2: `frozen_message_count == 0` iken kompress_background fast pass). Aday zincir (kanıtsız): away_summary mesaj dizisini değiştiriyor → Headroom'un sıkı önceki-tur kontrolü (`_strict_previous_turn_frozen_count`, anthropic.py:1509-1513) eşleşmeyi bulamıyor → donmuş sayı 0 → tüm mesajlar yeniden yazılıyor. TOKEN-6f'nin ilk doğrulama noktası bu olmalı.
- Ek kolonlar: frozen_message_count log vermiyor (PERF satırında alan yok). Pencere boyunca runtime-env satırı: 10-03 19:11:37 GET, H2 kapanışındaki 404 denemesi. (b) penceresinde 0. Son POST 18:27:07'de (6d deney kapanışı), pencere dışında.
- Recap'i yeniden açmak yalnız TOKEN-6f Headroom tarafını düzeltirse gündeme gelir. O zaman aynı test yeniden koşulur.
