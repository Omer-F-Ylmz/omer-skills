# Uyarlama: caveman-oz
arac: talimat
token_tavani: 150
aday: docs/kurulumlar/adaylar/caveman.md
ozellik: skill
kaynak_metin: docs/denemeler/caveman-talimat.md
lisans: MIT

18 K3 · `video uret caveman-oz` → `video dene caveman-oz`; taslak: docs/uyarlamalar/caveman-oz-talimat.md

## Fikir
caveman skill'inin iyi yanı: hitap, dolgu, çekince ve tekrar yok; açıklama kısa ve sonuç önde.

## Kapsam
Yalnız açıklama metni kısalır. Kod, komut, dosya yolu, hata mesajı ve güvenlik uyarısı eksiksiz ve olduğu gibi kalır (caveman-seçici bulgusu; caveman README "ne zaman kullan / atla"). Türkçe yanıtta doğal Türkçe, dilbilgisi bozulmaz. Her yanıta etki ettiği için skill değil talimat.

## Alınmayacaklar
Dil bozma (tanımlık/ek düşürme, parçalı cümle) ve ~1k tokenlık kural dosyası (14b: kural girdisi kısa görevde kazancı yedi, maliyet +%7.7).

## Başarı eşiği
çıktı token −%20 ve toplam maliyet −%0 ya da daha iyi
