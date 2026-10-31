# /compact

- tür: arac · durum: KURULU-KANITSIZ · videolar: 1Jb517FRX7I,Dd-Xxv2H4VH,DdznBJLyoEz,DeRgZlhJngj,DeY_8acEaiy,DelQS4sE2Id,DenHUw1CiQy,DepyR86P1ml,DeudWFqMKON,Gg35_iQWx7g
- bizde: docs/envanter/envanter.tsv

## Özellikler
- Uzun oturumda konuşmayı yoğun bir checkpoint'e çevirir
- Aktif geçmişi en fazla %85 küçültür (videoda 'HISTORY REDUCED 85%')
- Bağlam paneli: 493.5K/1.0M jeton kullanımı ve ~17,200 jetonluk geçmiş gösterilir
- Token tasarrufu için 18 ipucu arasında yer alır

## Videoda yapılış
Uzun oturumda /compact çalıştırılır; 'Analyzing conversation, Creating checkpoint, Compressing history' akışıyla CHECKPOINT oluşur. Ek öneriler: sistem promptunu 200 satır altında tutmak, kısa molalar vermek, dosya referanslarına dikkat etmek ve filtrelemek. Kural dosyası kısa tutulmalı, veri deposu gibi kullanılmamalı.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv'de kayıtlı; kurulu ancak kanıtı doğrulanmamış.

## Al
Uzun oturumda checkpoint alıp bağlamı temizleme; kural dosyasını kısa tutma

## At
Videodaki %80 ve %85 azaltma oranları ölçüm verisiyle desteklenmiyor; yalnızca ekran görüntüsü ve iddia var
