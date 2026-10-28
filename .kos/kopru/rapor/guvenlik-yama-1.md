# GUVENLIK-YAMA-1 (28 Eki 2026)
Kaynaklar: php.net releases JSON, nodejs.org/dist/index.json, winget show. Tarifteki sürümler doğrulandı.
| paket | eski → yeni | kaynak | durum |
|---|---|---|---|
| PHP 8.5 | 8.5.12 → 8.5.12 (zaten yamalı; 8.4.27/8.3.36 de güncel) | php.net | yapıldı (önceden) |
| Node 24 LTS (Program Files) | 24.22.1 → 24.22.1 (24.x son) | nodejs.org dist | yapıldı (önceden) |
| Corretto 17 | 17.0.21 → 17.0.21 (winget güncel; Temurin 17 yalnız 17.0.20) | winget show | yapıldı (önceden) |
| Corretto 21 | 21.0.13 → 21.0.13 | winget show | yapıldı (önceden) |
| Node 24.19.0 (winget user portable kopya) | eski, PATH'te 2. sırada | winget | Ömer'de |
Not: tarifteki "26.12.0/22.23.3" güncel değil; şimdi 26.12.1, 22.23.4 (LTS çizgisi 24 kaldı).
Doğrulama: node v24.22.1 · npm.cmd 11.19.1 · claude 2.1.311 · php 8.5.12 · java 21.0.13. RAM %74, C: 254 GB boş.
Yönetici gerektiren adım yok → guvenlik_yama_yonetici.ps1 yazılmadı.
Ömer'de: winget upgrade --scope user eski 24.19.0 kopyasında "remove_all: Access is denied" (kopya kullanımda); node'lar kapalıyken tekrar `winget upgrade OpenJS.NodeJS.LTS --scope user` ya da klasörü elle sil (silme yetkisi bende yok). Kalan savunmasız kopya: o klasör.
Reel/video_derin adımı bu oturumda yapılmadı (resmî kaynak kazanır; sürümler zaten resmî kaynakla eşleşiyor).
