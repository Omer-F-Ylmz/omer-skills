# OmniRoute

- tür: arac · durum: KURULU-KANITSIZ · videolar: Da8ZthUPK98,DaSs65mMrHk,Dae05TSAK1l,Dapjs58z0P0,Db1J34usxwh,DbIrCksJiqq,DbIt9AjK7-U,DbQx7UrM7Ud,Db_GVNhOnQF,Dbs8-TnKEhL,Dc7G9Pxu_1O,DcDgvucqG5K,DcMpM8_S1U3,Dcw20sWpLgs,DdBs5ZLJDoh,DdUELmKktcr,DdUf3qJOvTO,DdUk0Lrx0rw,DdZmPY4u-xd,Ddb1UVZIakr,DdcBCJRRQFT,DdeLN4ujZGN,DdjgNfBtToS,DdlurQHG2Mm,Ddqym0VAqzU,Ddrki7GugWV,DdtRDoSCll-,Ddw5QLjIlLp,DeCfWoGMIET,DeHbBTZjx5O,DeHz9pjRytv,DeIGeHSDeGQ,DeMrKekk7RU,DeNy
- bizde: docs/envanter/envanter.tsv; yontem:.kos\kopru\kaynak-dizin\dizin.tsv; arac:.kos\kopru\kaynak-dizin\dizin.tsv; npm -g:docs\katalog\yetenek.tsv

## Özellikler
- Claude Code gibi araçları 200+ AI sağlayıcısına bağlar (nick_saraev, theopenstack)
- Claude kotası dolunca otomatik olarak bir sonraki modele geçer
- Ücretsiz katmanları birleştirir; videoda ayda 'up to 1.6 billion' ücretsiz token iddiası var
- İstemleri (prompt) modele gitmeden sıkıştırır; 'up to 90%' token tasarrufu iddiası (nick_saraev)
- theopenstack örneğinde aynı landing page istemi için '75% fewer tokens' sonucu gösteriliyor

## Videoda yapılış
Tek npm install, tek API bağlantısı ve kullanılan araca bir satır yapıştırma (theopenstack: 'one npm install, one API connection, one line pasted into yo...' — metin kesik).

## Bizdeki karşılık ve fark
Durum KURULU-KANITSIZ: docs/envanter/envanter.tsv, .kos\kopru\kaynak-dizin\dizin.tsv (yöntem ve araç), docs\katalog\yetenek.tsv (npm -g) kayıtlı. Fark: kurulu olduğu yazılıyor ama alıntıda kanıt yok; bizde yönlendirme ve sıkıştırma çalışması doğrulanmamış.

## Al
Kota dolunca model değişimiyle kesintisiz çalışma fikri. Prompt sıkıştırmanın token tüketimini düşürmesi.

## At
1.6 milyar token ve %90 tasarruf rakamları alıntıda doğrulanmamış. 'Aynı çıktı kalitesi' iddiası kanıtsız. Çok sayıda üçüncü taraf sağlayıcıya veri akışı olur.
