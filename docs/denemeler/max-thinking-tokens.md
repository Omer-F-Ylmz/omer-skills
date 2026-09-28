# Deneme: max-thinking-tokens

video v-vRYtvWDYs · 15 · bu dalgada koşulmaz (14b)

## Hipotez
MAX_THINKING_TOKENS üst sınırı düşünme tokenını (dolayısıyla $'ı) azaltır; 6 sabit görevde (docs/denemeler/gorevler/) kalite kapısı düşmez.

## Metrik
görev başına sıcak koşu $ ve çıktı token + kalite kapısı (beklenen:) geçen görev sayısı; A: varsayılan · B: env MAX_THINKING_TOKENS sınırlı (değer TOKEN-DENEME-2'de seçilir).

## Bütçe
claude -p en fazla 24 (6 görev × 2 kol × 2, --tavan 24); bu dalgada 0.

## Geri alma
settings.json env'den MAX_THINKING_TOKENS silinir (bu dalgada eklenmedi).

## Başarı eşiği
sıcak koşu $ ≥%20 düşüş VE kalite kapısı düşüşsüz (18); değilse RED(token)/RED(kalite).

## Not
Ömer kararı 28 Eyl (KURULUM-24e-1-KAPANIŞ): DENE — token; kural değil ayar. Bu dalgada koşulmaz; TOKEN-DENEME-2'de ölçülecek. Aday: docs/kurulumlar/bekleyen/kural-max-thinking-tokens-ayari.md
