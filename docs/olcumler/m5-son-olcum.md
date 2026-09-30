# M5 — son ölçüm (ikinci göz açık, iki taze koşu)

Ölçütler (yüksek ≥%90 · genel ≥%75 · dayanmayan ≤%5) ve altın set değişmedi. Motor: M3b + K1 + ikinci göz (luna; özgü kalem Jev/görsel yargıçla doğrulanırsa).
Paket: .kos/m4b/cache-m3b (M3b-1 ile aynı girdi). Koşular izole: .kos/m5/r1 · .kos/m5/r2, ayrı partiler. Tavan (koşu başına): Sonnet 10 çağrı / $1,03 · luna $0,1 · Jev 150 durum · yargıç 8.

**SONUÇ: DEĞİL — en yakın kalan ölçüt genel ≥%75: ortalama %74.7 (fark -0.3 puan)**

## Koşular
| koşu | yüksek | genel | dayanmayan | Sonnet çağrı | Sonnet $ | luna $ (çağrı) | Jev durum (motor) | yargıç motor/ölçüm | eklenen / doğrulanamadı | durumlar |
|---|---|---|---|---|---|---|---|---|---|---|
| r1 | %86.1 (68/79) | %75.0 (120/160) | %7.5 (16/214) | 8 | 0.899 | 0.0398 (5) | 70 | 5/4 | 66 / 29 | L9c4 tamam · kHtO tamam · g89F tamam · 86HM tamam · JfmA tamam |
| r2 | %88.6 (70/79) | %74.4 (119/160) | %7.4 (15/203) | 11 | 1.089 | 0.0346 (5) | 68 | 3/5 | 64 / 24 | L9c4 tamam · kHtO tamam · g89F tamam · 86HM tamam · JfmA tamam |

Ölçülemeyen motor kalemi (Jev/görsel yargıç tavanı dışı): r1 0/214 (%0.0) · r2 0/203 (%0.0)
Devam (K1): 86HM0RUWhCk ilk ölçümde r1 `hata` (Sonnet parti içi onarım çağrısı kalan parti $'ına kırpıldı, parti.py:351 → error_max_budget_usd) · r2 iki deneme form_red; ikinci gözden değil. `onar` yalnız bu video için hata/form_red'i yeniden taradı (≤3 çağrı / $0,35). Ölçüm tavanları motordan ayrı: Jev 300 durum · görsel yargıç 8/koşu.

## Ortalama ± yarı fark (ölçütlere karşı)
| ölçüt | ortalama | ± | M4b gürültüsü (puan) | sonuç |
|---|---|---|---|---|
| yüksek ≥%90 | %87.3 | 1.3 | 1.3 | KALDI |
| genel ≥%75 | %74.7 | 0.3 | 5.0 | KALDI |
| dayanmayan ≤%5 | %7.4 | 0.0 | 1.5 | KALDI |

## Yan yana
| | yüksek | genel | dayanmayan | $ (koşu) |
|---|---|---|---|---|
| M3b-1 (tek koşu) | %90.0 | %81.0 | %4.0 | 0.860 |
| M4c (iii) simülasyon | %92.0 | %82.0 | %3.0 | 0.932 |
| M5 ortalama | %87.3 | %74.7 | %7.4 | 1.079 |

## Kategori × önem (yakalama)
| kategori | önem | r1 | r2 | ortalama |
|---|---|---|---|---|
| Araç/servis/ürün | yüksek | 16/17 | 15/17 | %91.2 |
| Araç/servis/ürün | orta | 11/13 | 11/13 | %84.6 |
| Araç/servis/ürün | düşük | 2/4 | 2/4 | %50.0 |
| Açıklama bağlantıları | yüksek | 7/7 | 7/7 | %100.0 |
| Açıklama bağlantıları | orta | 3/3 | 3/3 | %100.0 |
| Açıklama bağlantıları | düşük | 1/1 | 1/1 | %100.0 |
| Kareden bilgi | yüksek | 4/5 | 4/5 | %80.0 |
| Kareden bilgi | orta | 8/18 | 8/18 | %44.4 |
| Kareden bilgi | düşük | 6/9 | 5/9 | %61.1 |
| Kural/ipucu/iş akışı | yüksek | 5/9 | 6/9 | %61.1 |
| Kural/ipucu/iş akışı | orta | 7/11 | 6/11 | %59.1 |
| Kural/ipucu/iş akışı | düşük | 1/2 | 1/2 | %50.0 |
| Kurulum/komutlar | yüksek | 8/10 | 9/10 | %85.0 |
| Kurulum/komutlar | orta | 4/6 | 3/6 | %58.3 |
| Kurulum/komutlar | düşük | 2/2 | 2/2 | %100.0 |
| Promptlar | yüksek | 5/6 | 6/6 | %91.7 |
| Teknikler | yüksek | 23/25 | 23/25 | %92.0 |
| Teknikler | orta | 7/12 | 7/12 | %58.3 |

## Maliyet ve Max kotası
- Koşu $ (Sonnet + luna + motor yargıcı): r1 0.996 · r2 1.163 · ortalama 1.079 (M3b-1 0.860)
- İkinci göz video başına ek $ (luna + yargıç, ortalama): 0.0171
- Max kotası payı (Sonnet tarama + motor görsel yargıç çağrısı): r1 13 · r2 14 · ortalama 13.5 (m3b-1 8 → %+69); ölçüm yargıcı ayrıca r1 4 · r2 5

## Kural 21
- ikinci göz: $ 0.860 → 1.079 (%+26) · yüksek -2.7 · genel -6.3 · dayanmayan +3.4 puan (M3b-1'e göre; gürültü yüksek ±1.3 · genel ±5.0 · dayanmayan ±1.5)
