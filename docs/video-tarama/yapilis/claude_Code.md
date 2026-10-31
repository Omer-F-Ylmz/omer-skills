# claude Code

- tür: arac · durum: KURULU-KANITSIZ · videolar: 1Jb517FRX7I,2n84xa99FRY,3XIGcM7VICc,7XhX8P0ebEU,DM331_IByuB,DUS8hMijFGv,DV4V4fCDPsV,DV6W5PTDrkm,DVyqBiejOh8,DW4-DC0IJ-7,DWtKXrODwnm,DWywnl8jeVK,DWzpImJIuci,DX1v6a1hqUf,DX2ubACJYRN,DX3iYGwM6Di,DXb_hOdDRan,DXezZ_KjHTm,DXmM2wLkf92,DXnCpVAuhzZ,DXosDMHDDPh,DXpE4ggiD3x,DXqzDc6j-H_,DXruEuojJLI,DXt9VG5DwNV,DXtiKwCjNHv,DXvgZqaNXvp,DXwGMS_jK_B,DXxQS0AO1Km,DY8EtIPtKLC,DYA1MUFuid-,DYC-x8DogOI,DYEtbbGICX6,DYKR
- bizde: docs/envanter/envanter.tsv

## Özellikler
- Token tüketimini azaltmaya yönelik 18 'token hack' (9 kolay, 5 orta, 4 ileri düzey)
- clear, compact ve stats komutları
- Opus ve Sonnet modellerini hibrit kullanarak maliyet optimizasyonu (metin kesik)
- Birden fazla Claude Code oturumunu aynı anda açma; arka planda birkaç agent ve test çalıştırma
- Model değiştirme (videoda Fable'a geçiş gösteriliyor)

## Videoda yapılış
Video 1: token tasarrufu için clear/compact/stats komutları ve model hibriti anlatılıyor. Video 2: aynı anda iki terminalde Claude Code açılıyor, model Fable'a alınıyor, arka plandaki test ve agent'lar izleniyor. Uzun süren (iki güne yayılan) agent işinin nasıl kurulacağı konuşmada soru olarak kalıyor, cevaplanmıyor.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv'de kayıtlı (durum: KURULU-KANITSIZ). Kayıt satırının içeriği verilen metinde yok, bu yüzden fark çıkarılamadı.

## Al
clear/compact/stats ile bağlamı ve token kullanımını izleme; göreve göre model seçimi

## At
%80 tasarruf iddiası ölçülmemiş. Fable model iddiası metinde doğrulanmıyor. Çok sayıda paralel agent (videoda 6-8) yavaşlamaya yol açıyor.
