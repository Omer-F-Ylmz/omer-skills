# Jev kalibrasyonu — 2026-09-22

Veri: jev_kalibre.jsonl · n=40 sentetik Türkçe mesaj (12 sınır durum) · model başına 1 batch. Kesinlik: choice `confidence`, noul `max(p, 1-p)`; niyet + acil yargıları birlikte (80 yargı/model).

| model | niyet isabeti | acil Brier | doygunluk (≥0.999) | doygunluk sınır | Act önerisi (≥0.95) | Flag önerisi (≥0.80) | yanıtsız |
|---|---|---|---|---|---|---|---|
| jev-1.13 | 0.95 | 0.089 | 0.29 | 0.21 | 0.6 | 0.49 | 0 |
| jev-latest | 0.95 | 0.089 | 0.29 | 0.21 | 0.65 | 0.51 | 0 |

Varsayılan bantlarla (0.85/0.60) bant başına isabet:

| model | Act n · isabet | Flag n · isabet | Escalate n · isabet |
|---|---|---|---|
| jev-1.13 | 51 · 1.00 | 22 · 0.86 | 7 · 0.43 |
| jev-latest | 50 · 1.00 | 23 · 0.83 | 7 · 0.57 |

**Önerilen model:** jev-1.13 (isabet, sonra Brier; eşitlikte pinli jev-1.13).
**bantlar.json:** act 0.85 · flag 0.60 (taban). 0.60/0.49 önerisi kolay setin yan etkisi, n=40, taban korundu; varsayılan bantlar ölçümle doğrulandı (jev-1.13: Act 51 · 1.00 · Flag 22 · 0.86 · Escalate 7 · 0.43). Ölçüm 80 HTTP istek (2 batch); yeniden koşulmadı.

Not: n=40. Eşikler kaba; güven aralığı geniş. Doygunluk yüksekse kesinlik ayırt edici değildir, bant yerine sınıf/p'ye bakılır.

Etiket düzeltmesi sonrası (13c): #16 iade→ödeme (#23 zaten ödeme); kalibrasyon yeniden koşulmadı, yukarıdaki sayılar eski etiketlerle.
