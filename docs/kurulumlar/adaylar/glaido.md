# glaido
ad: glaido
tur: uygulama
video: 3XIGcM7VICc
repo: yok
lisans: yok
son_commit: yok
arsiv: hayır
kaynak: yok

## Ne
Masaüstünde (macOS + Windows 11) her uygulamada çalışan sesle-yazma (dikte) aracı. Kısayol tuşuna basılı tutup konuşunca, düzenlenmiş metni aktif uygulamaya yazıyor. Kapalı kaynak, ticari SaaS/masaüstü uygulama — "The voice layer for every app".

## Kanıt
- `gh search repos glaido` → glaido adında resmi bir kod deposu yok; dönen 3 sonuç (sstroemer/glaidos, ItsssssJack/glaido-deck, daveebbelaar/glaido-skills) ilgisiz/üçüncü taraf projeler.
- Verilen link `https://get.glaido.com/nate` bir affiliate/referral bağlantısı: 302 ile `https://app.glaido.com/signup?ref=GLAIDO44063&dub_id=...` adresine yönleniyor (ref= parametresi affiliate izi).
- Resmi site glaido.com: kapalı kaynak, GitHub/kaynak kod linki verilmiyor. Fiyatlandırma: Basic ücretsiz (haftada 2.000 kelime), Pro 17 $/ay (yıllık faturalı), Enterprise özel fiyat.
- docs.glaido.com ana sayfası: kurulum adımları, izin listesi, kaldırma talimatı, lisans bilgisi hiçbiri yayınlanmamış.

## Kurulum
Belirsiz. Resmi dokümantasyonda adım adım kurulum yok; "Try Glaido Free" → app.glaido.com/signup üzerinden kayıt/indirme akışına yönlendiriyor. Doğrudan indirme linki, checksum veya paket yöneticisi (brew/winget) bilgisi yok.

## İzinler
Sayfalarda açıkça listelenmiyor. Ürünün çalışma şekli (global kısayol, mikrofonla dikte, aktif uygulamaya metin yazma) mikrofon ve muhtemelen erişilebilirlik/klavye enjeksiyonu izni gerektirdiğini düşündürüyor — bu bir çıkarım, doğrulanmadı.

## Duman testi
Yapılamadı: kapalı kaynak, indirilebilir paket/kod yok; kurulum koşulmadı (talimat gereği).

## Geri alma
Belirtilmemiş; resmi kaynaklarda uninstall talimatı yok.

## Köprü izni
yok — kurulacak yürütülebilir kod/CLI yok, köprüye bağlanacak salt-okur alt komut söz konusu değil.

## Önerilen katman
RED — lisans yok (kapalı kaynak, GitHub deposu yok), kurulum/kaldırma/izin bilgisi doğrulanamıyor; verilen link affiliate/referral bağlantısı, resmi kaynak değil.
