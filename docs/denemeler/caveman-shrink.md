# Deneme: caveman-shrink

video ? · 15 · bu dalgada koşulmaz (14b)

## Hipotez
aynı komut çıktılarında RTK'dan ≥%15 daha az token, sinyal kaybı yok.

## Metrik
komut başına çıktı token (RTK'ya karşı A/B) ve sinyal korunumu (hata satırı · test sayısı · yol).

## Bütçe
5 komut çıktısı (pytest · dotnet test · git log · npm test · rg), model yok, $0.

## Geri alma
npm rm -g @caveman-ai/cli; RTK ayarı değişmez.

## Başarı eşiği
token RTK'ya göre −%15 ve kayıp sinyal 0.

