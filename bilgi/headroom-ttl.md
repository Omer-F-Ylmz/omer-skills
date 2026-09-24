---
iddia: Headroom cache_control ttl 1h'yi bayt bayt korur; üst akış yazımı %100 ephemeral_1h. 5–60 dk aralık sonrası kayıpların nedeni TTL değil.
kaynak: kaydedici 400 yakalaması (CC ve 8792 Headroom zinciri), K3 claude -p usage.cache_creation, proxy.log* aralık sınıflaması
guven: yuksek (TTL) · orta (kayıp nedeni ölçülmedi)
dogrulama: docs/olcumler/headroom-gelistir.md
tarih: 2026-09-24
bayatlama: 2026-12-23
etiketler: token, headroom, rtk, olcum
---
Headroom cache_control ttl 1h'yi bayt bayt korur; üst akış yazımı %100 ephemeral_1h. 5–60 dk aralık sonrası kayıpların nedeni TTL değil.
- 3 kırılım (system[1], system[2], messages[1]) iki zincirde de ttl 1h.
- <5 dk read oranı 0.95; 5–60 dk 0.39, 46 aralığın 37'si tam kayıp, 7 isabet (22–55 dk dahil).
- Headroom ayarı gerekmiyor; bekleyen/headroom-ttl.md yazılmadı.
