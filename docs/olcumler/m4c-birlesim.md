# M4c — birleşim simülasyonu (2026-09-30)

Yeni tarama yok. Veri: m3b-1 = `.kos/m3b` sonnet · m3b-2 = `.kos/m4b/m3b2` sonnet · luna-m3b = `.kos/m3b` luna kolu (M3b'nin tam luna taraması; kare-luna değil).
Betik `tools/video/olcum_m4c.py`, çıktı `.kos/m4c/sonuc.json`. Tekilleştirme: B kalemi A'yla `anahtarlar` kesişiyorsa ya da A'nın yakaladığı altın kaleme eşleşiyorsa kopya.
Doğrulama: M3b Jev k3 hükmü (+`k3_duzelt`), kare kalemde görsel yargıç. Yeni görsel yargıç 4 çağrı / $0,030 (tavan 6 / $0,2), yeni Jev 0 (tavan 100).
Sağlama: betiğin m3b-1 tek satırı M4b tablosuyla aynı (71/79 · 130/160 · 5/127).

Ölçüt: yüksek ≥%90 · genel ≥%75 · dayanmayan ≤%5. Gürültü (M4b, m3b iki koşu): yüksek 1,3 · genel 5,0 · dayanmayan 1,5 puan.

| kol | yüksek | genel | dayanmayan | $ (koşu + doğrulama) | sonnet çağrı | ölçüt |
|---|---|---|---|---|---|---|
| m3b-1 (tek, referans) | %90 (71/79) | %81 (130/160) | %4 (5/127) | 0,860 | 8 | yüksek KALDI (89,9) |
| (i) m3b-1 ∪ m3b-2 | %95 (75/79) | %86 (137/160) | %7 (12/171) | 1,677 | 17 | dayanmayan KALDI |
| (ii) m3b-1 ∪ luna-m3b | %92 (73/79) | %82 (132/160) | %6 (11/179) | 0,902 | 8 (+6 luna) | dayanmayan KALDI |
| (iii) m3b-1 ∪ luna-m3b doğrulamalı | %92 (73/79) | %82 (132/160) | %3 (5/173) | 0,932 | 8 (+6 luna, +görsel) | GEÇTİ |
| (iv) m3b-1 ∪ m3b-2 doğrulamalı | %95 (75/79) | %86 (137/160) | %3 (5/164) | 1,677+ | 17 | GEÇTİ |

Kural 21 (m3b-1'e göre):
- (iii): maliyet +%8 ($0,860→0,932); yüksek +2,5 · genel +1,2 puan · dayanmayan −1,0 puan. Sonnet (Max kotası) çağrısı değişmez.
- (iv): maliyet +%95, yüksek +5,1 · genel +4,4 puan. Kalite artışı (iii)'ün iki katı, maliyet ~12 katı.
- Doğrulamasız (i)/(ii): ekler dayanmayanı ölçüt üstüne taşıyor; önerilmez.

Gürültü payı: (iii) yüksek marjı 2,4 puan (> 1,3), dayanmayan marjı 2,1 puan (> 1,5); genel marjı 7,5 puan (> 5,0). Üç ölçüt de gürültü dışında geçiyor. Yine de yüksekte kazanç yalnız 2 kalem; M5'te ikinci koşuyla teyit edilmeli.

## Önerilen tasarım
**(iii) m3b-1 + luna-m3b, luna'nın yalnız kendisinde olan kalemleri Jev/görsel doğrulamadan geçerse eklenir.** Üç ölçütü geçen en ucuz kol bu. Sonnet çağrısı artmıyor; luna koşusu (6 çağrı, $0,043) ve doğrulama ($0,03) ekleniyor. Motora uygulama M5'te.
