# Haiku

- tür: varlik · durum: KAYITSIZ · videolar: DYmbDrUjBdU,DZ-ZlbQFZy2,DbRGB9QsGtb,DdYIImkKs4n,Ddi0-0Cm1fd,DdjUihCs77b,DdrI2l7H5Gz,DdzDB3Jq6K9,De6BzO3kWQn,Def1nTHD0aW,DefOjSZgifD,DeirdCDkzZZ,DerloxxvzYJ,Gg35_iQWx7g,JNM_rxqtlvY
- bizde: yok

## Özellikler
- Sınıflandırmada (intent, sentiment gibi kategoriler) Sonnet ile aynı etiketleri verir; alıntı dörtte bir sürede bittiğini söylüyor
- Alan çıkarmada (fiş, e-posta) model boyutu önemsiz; maliyet Sonnet'in kesri
- Model kimliği haiku-4-5; girdi fiyatı 1M token başına $0.80 (slayt)
- Yönlendirme (routing), ilk geçiş özetleri ve toplu soru-cevap için kullanılıyor
- Goal/Outcomes döngüsünde bağımsız denetçi (hakem) model olarak kullanılıyor

## Videoda yapılış
Ucuz geçiş önce Haiku ile çalıştırılır, yanıt belirsizse Sonnet'e yükseltilir. Goal/Outcomes döngüsünde Haiku ayrı bir hakem subagent olarak rubriği değerlendirir; kriter karşılanmazsa tur yeniden başlar, max_iterations ile sınırlanır.

## Bizdeki karşılık ve fark
yok

## Al
Ucuz-önce, belirsizde yükselt yönlendirmesi; işi denetleyen bağımsız hakem olarak Haiku

## At
-
