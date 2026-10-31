# Redis

- tür: arac · durum: KURULU-KANITSIZ · videolar: DZ3PUfYlK6z,DalKFHjswU_,DbG0BN2Kpdi,DbVGcvfgUsD,DcDfnzsM2wL,DcI8a69AEJq,DcNGpmXOR42,DcOhWbqm3vK,DdSwfSNgFiJ,DdWfVfbErk3,De3y3DGEyXD,De9L9avinkn,Deau8oUO4i1,Dej2rGAPu5O,DekwK6fFX74
- bizde: kurulu-tara.json pip

## Özellikler
- OpenWA (WhatsApp API ağ geçidi) önbellek katmanı olarak Memory veya Redis seçeneği sunuyor
- Veritabanı (SQLite/PostgreSQL), depolama (Local/S3) ve önbellek katmanları yapılandırmayla değiştirilebiliyor; uygulama kodu değişmiyor
- Videoda bellek içi kayıt yerine kalıcı checkpointer (metinde 'redis checkpointer' geçiyor, kısmen bozuk) kullanıp yeniden başlatmalarda hafızanın korunması anlatılıyor

## Videoda yapılış
OpenWA'da önbellek, veritabanı ve depolama sürücüleri yapılandırma (config) ile seçiliyor. Agent tarafında InMemorySaver yerine kalıcı checkpointer ile hafıza kalıcı hale getiriliyor.

## Bizdeki karşılık ve fark
kurulu-tara.json pip

## Al
Önbellek katmanını (Memory/Redis) ve veritabanını koda dokunmadan yapılandırmayla değiştirme; kalıcı checkpointer ile yeniden başlatmada hafıza koruma

## At
-
