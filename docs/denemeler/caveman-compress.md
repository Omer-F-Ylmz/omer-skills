# Deneme: caveman-compress

video ? · 15 · 20a: düzenek hazır, koşulmaz (caveman kurulumu ONAY bekler)

## Hipotez
Divisima CLAUDE.md ≥%30 küçülür, hiçbir kural kaybolmaz.

## Metrik
token önce/sonra (c.token) ve kural korunumu: kaynaktaki her `- ` maddesi (şu an 94) için Jev score (≥1.5 korunmuş).

## Bütçe
`video dene caveman-compress --istek-tavan 120`: claude -p 0, Jev ≤120 (94 madde, uzun state bölünürse fazlası; tavan ağa çıkmadan denetlenir).

## Geri alma
Yok: hedef dosyaya asla yazılmaz. Komut yalnız docs/denemeler/.kos/caveman-compress/CLAUDE.md KOPYASINDA koşar; kaynak bayt değişirse `dene` özgün baytı geri yazar ve RED verir.

## Başarı eşiği
token −%30 ve korunmayan kural 0.

## Kaynak
C:/Users/pc/Desktop/smart/Divisima.Solution/CLAUDE.md

## Komut
caveman compress {kopya}

## Varsayım
`caveman compress <dosya>` yerinde sıkıştırır varsayımı; `.original` gibi yedek dosyayı kopya dizinine yazar. Kurulumdan sonra `caveman compress --help` ile doğrulanır.
