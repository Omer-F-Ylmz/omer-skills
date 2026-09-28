# lumen-sitesi-promptu
ad: lumen-sitesi-promptu
tur: prompt
video: iYwCzKy6W40
etiket: yeniden:parti-c
repo: yok
lisans: yok
son_commit: yok
arsiv: yok
kaynak: yok
telemetri: yok
arastirma: yarım: araştırıcı 12 tur tavanında dosya yazmadan durdu (45.5k token · 12 çağrı); alanları ana ajan on.md'deki altyazıdan (5:04) yazdı, dış kaynak doğrulaması yok
## Ne
Kurulabilir araç değil: Sketchfab GLB modeliyle React Three Fiber (Three.js) 3D kamera landing sayfası ürettiren site yapım promptu; video açıklamasında paylaşıldığı söyleniyor, metni altyazıdan anlatım olarak okunuyor.
## Kanıt
iYwCzKy6W40 5:04 (docs/video-tarama/2026-09-28-iYwCzKy6W40.md · .kos/iYwCzKy6W40/lumen-sitesi-promptu/on.md): anlatıcı promptun teknik, dosya formatı, kritik, sahne/ışık/kamera ve font kısımlarını sırayla gösteriyor.
## Kurulum
- yok (prompt; kurulacak paket yok)
## İzinler
- yok
## Duman testi
- yok
## Geri alma
- yok
## Köprü izni
- yok
## Önerilen katman
UYARLA (şablonda olmayan bölümler frontend-promptlar kütüphanesine)
## Telemetri kapatma
- yok
## Prompt anatomisi
bolumler: teknik (stack) · dosya formatı · kritik/atlama yasağı · sahne-ışık-kamera · font (stil, boyut px)
hareket: modern animasyon; 3D modelin animasyon pozisyonları elle ayarlanmış, "atlama/değiştirme" diye sabitlenmiş
teknoloji: React Three Fiber (Three.js) adıyla; "güzel site yap" yerine stack adlandırılıyor
dosya: bileşenlere ayrılmış dosya yapısı prompt'ta tarif ediliyor, projeler arası sabit tutuluyor
config: sahne kurulumu + ışık (üstten vuran parlama) + kamera konumu açıkça isteniyor; konumlar sayısal verilmiş (değerler altyazıda yok)
asset: Sketchfab'den indirilen GLB model
kabul: doğrulanamadı (altyazıda kabul ölçütü yok; "%90 benzer" iddiası ölçülmedi)
### Kalıplar
- 3D modeli stack adıyla ver: model + R3F/Three.js birlikte · 5:04 · teknik: React Three Fiber · şablon: teknoloji
- Dosya yapısını bileşen bileşen yaz, projeler arası aynı kalsın · 5:04 · teknik: bileşen ayrımı · şablon: dosya
- Elle ayarlanmış pozisyonları "atlama, değiştirme" diye kilitle · 5:04 · teknik: kritik blok · şablon: yok
- 3D'de sahne, ışık ve kamera ayarını ayrı ayrı iste · 5:04 · teknik: Three.js scene/light/camera · şablon: config
- Font stilini ve piksel boyutlarını prompt'ta belirt · 5:04 · teknik: tipografi tokenları · şablon: yok
## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Prompt kopyalanıp yapıştırılırsa sitenin %90 benzeri çıkar (5:04) | - | doğrulanamadı | yalnız anlatım; claude -p 0, koşulmadı | - |
## Bizde durum
- kurulum: yok (katalog ve settings'te yok)
- jev skill (Act): anthropic-skills:creative-coding 0.91
