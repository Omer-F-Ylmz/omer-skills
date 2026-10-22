# VERİM-HEDEF-1 (22 Eki) — taban, yönlendirme tablosu, eğri
Ölçüm: `python tools/verim_pano.py` (usage.db; $ claude-usage ile birebir doğrulandı: sonnet 3/15, haiku 1/5, opus 5/25 $/M; önbellek okuma 0.1x, yazma 1.25x).

## Taban (7 gün, 16–22 Eki)
- Claude $662 / 11.7k tur: 20 Eki $434 · 21 Eki $119 · 22 Eki $110 (öğlene dek).
- $ dağılımı: önbellek yazma+okuma %59 · çıktı %24 · girdi %17. Ana oturum %75, alt ajan %25.
- Model $: sonnet %72 · opus %21 · haiku %6.
- Ücretsiz havuz bugün 437 çağrı = çağrıların %13.7'si (Claude 2.7k tur); $ payı ~0.
- Haftalık limit %: CLI vermiyor ($ vekil). Kalite: hakem/Desktop KABUL-RED kaydı yoktu → `verim_pano.py kalite` ile beslenir.

## Yönlendirme (önce yerel/ücretsiz → haiku → sonnet → opus)
| Adım türü | Basamak | Gerekçe |
|---|---|---|
| log/doküman özeti, keşif, OCR, transkript | ücretsiz (ucuz_alt / ucretsiz_havuz / yerel whisper) | çıktı kısa, doğrulaması ucuz |
| görsel hakem, sınıflama, etiket | ücretsiz (iki aile) | gorsel_hakem zaten çift aile |
| test koşusu, format | suite-kosucu (haiku) / yerel | karar yok |
| kod yazma, düzenleme | sonnet | hata maliyeti yüksek; A/B'siz ücretsize kayma yok |
| plan, mimari, son birleştirme | sonnet → opus yalnız zorsa | |

Kapı: `verim_pano.py kalite <tür> ok|red`; son 5 kayıtta ≥%40 RED (en az 3 kayıt) → tür bir basamak yukarı (`merdiven`), pencere sıfırlanır.

## Eğri (dürüst)
- %50: ana oturum bağlamını kısaltmak (önbellek $ %59: /clear dalga başı, /compact, okuma/keşif alt işe) + alt ajan işlerinin (%25) ücretsize kayması. Mümkün.
- %80: yalnız keşif/özet/hakem ağırlıklı işlerde. Kod yazma ağırlıklı işte kalite riski; A/B olmadan kayma yok.
- "5–6 saat ≈ %1": haftalık limit tavanı ölçülemiyor; bugünkü ~$13–20/saat ile doğrulanamaz. Şimdilik $/saat eğrisi izlenir.
- A/B (5 iş, ücretsiz vs sonnet, hakem puanı) BU TURDA KOŞULMADI; sonraki adım.
