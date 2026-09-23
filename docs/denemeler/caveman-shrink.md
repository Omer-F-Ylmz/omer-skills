# Deneme: caveman-shrink

video ? · 15 · 20a: düzenek hazır, koşulmaz (caveman kurulumu ONAY bekler)

## Hipotez
okuma ağırlıklı görevlerde komut çıktısını caveman shrink RTK'dan ≥%15 daha az girdi tokenıyla modele verir, sinyal kaybı yok (görev başarısı düşmez).

## Metrik
girdi token · sıcak koşu $ (karar) · soğuk $ (bilgi) · görev başarısı (beklenen: test adı · alan değerleri · hatalı değişiklik · hata zinciri) · Jev kalite.

## Bütçe
`video dene caveman-shrink --gorevler okuma --tavan 16 --istek-tavan 20`: 4 görev × 2 kol × 2 koşu = 16 claude -p, Jev ≤20.

## Geri alma
npm rm -g @caveman-ai/cli; RTK ayarı değişmez.

## Başarı eşiği
girdi token −%15 (RTK'ya göre) ve kalite kapısı (18).

## Kollar
- rtk: temel · env ANTHROPIC_BASE_URL=https://api.anthropic.com
- shrink: env ANTHROPIC_BASE_URL=https://api.anthropic.com CAVEMAN_SHRINK=1 · önek caveman shrink --

## Varsayım
RTK kolu mevcut hook düzeniyle (claude -p kullanıcı hook'larını yükler). `caveman shrink -- <argv>` ve CAVEMAN_SHRINK sözdizimi doğrulanmadı; kurulumdan sonra `caveman shrink --help` ile kesinleşir. Shrink kolunda RTK hook'u da çalışıyorsa iki sıkıştırıcı üst üste biner: o durumda kol "RTK+shrink" diye raporlanır.
