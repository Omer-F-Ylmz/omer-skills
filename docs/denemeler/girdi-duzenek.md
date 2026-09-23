# Deneme: girdi-duzenek

20a canlı küçük doğrulama: düzenek çalışıyor mu, soğuk/sıcak farkı görünüyor mu. Karar anlamlı değil (1 görev).

## Hipotez
aynı görevde doğrudan ve Headroom kolu eşit sayıda, karışık sırayla koşar; sıcak koşu soğuktan ucuzdur.

## Metrik
kol başına girdi token · soğuk $ · sıcak $.

## Bütçe
`video dene girdi-duzenek --gorevler okuma --tavan 4 --istek-tavan 6`: 1 görev × 2 kol × 2 koşu = 4 claude -p.

## Başarı eşiği
girdi token −%5

## Görevler
- 4-log-zincir

## Kollar
- dogrudan: temel · env ANTHROPIC_BASE_URL=https://api.anthropic.com
- headroom: env ANTHROPIC_BASE_URL=http://127.0.0.1:6767
