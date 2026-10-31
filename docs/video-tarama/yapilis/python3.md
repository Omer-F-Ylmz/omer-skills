# python3

- tür: arac · durum: KURULU-KANITSIZ · videolar: 7XhX8P0ebEU,Dbi13BDlDDQ,DdKcLiJgczB,DdSwfSNgFiJ,DdeiU6Nuh2y,DdlyT_dIiT7,DeL14cPOqin,DeR4IFRTKIu,Deaz4Kzgi3T,DenIklFh8TC,DfBbQs6jKUJ
- bizde: kurulu-tara.json PATH:C:\Users\pc\AppData\Local\Programs\Python\Python312

## Özellikler
- python3 komutuyla betik çalıştırma
- --workers parametresiyle paralel üretim
- Var olan dosyaları atlayarak tekrar çalıştırmayı güvenli kılma
- Telegram chat id bulma betiği (telegram_oku.py --chat-id-bul)

## Videoda yapılış
Komut: python3 generate.py --workers 6. API batch ile 6 slayt paralel üretiliyor; mevcut dosyalar atlanıyor; caption.txt ve PNG'ler klasöre düşüyor (çıktı: 'Done: 6 ok, 0 fail'). Ajan takımında Bash izni python3 bin/tweet_cek.py* ile veriliyor.

## Bizdeki karşılık ve fark
BIZDE: kurulu-tara.json PATH: C:\Users\pc\AppData\Local\Programs\Python\Python312. Hafıza notuna göre python3.exe elle kopyalanmış bir shim; videodaki python3 komutu buna bağlı.

## Al
Paralel üretimde --workers ve idempotent çalışma (var olanı atla) desenini kullanmak.

## At
Windows'ta python3 komutu hazır gelmiyor; elle kopya shim'e bağımlılık var (BIZDE notu).
