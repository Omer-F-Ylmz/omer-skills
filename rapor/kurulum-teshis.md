---
type: summary
status: complete
tags: [kurulum, teshis, skill-kur-4]
relatedTo: [kurulum_d2, kurulum_d3]
---
KURULUM-TESHIS (7 Kas 14:10) — kurulum yapilmadi.
KOK NEDEN 1: "coz yeniden islenecek: 41" kapsam suzgeci olmadan tum coz-4 uzerinden sayiliyor; kapsamda yalniz 6. 5'inin coz kaynak sutunu bos (kaynak[:3] suzgecine takilir), 1'i (geo-crawlers) npm -g EJSONPARSE (package.json'da NUL bayt) -> tek HATA satiri.
KOK NEDEN 2: 244 kalem KAPI-GECTI'de takili. kurulum_d2 bitenler() "KAPI-GECTI disi herhangi bir satiri olan = bitti" sayiyor (eski HATA/YOLU-YOK/BULUNAMADI-2 satirlari var); yeniden listesi yalniz son satira bakiyor (o KAPI-GECTI) -> kur fazina hic girmiyorlar.
Kapsam 353 kalem: KAPI-GECTI 244 (eski: BULUNAMADI-2 131, HATA 73, YOLU-YOK 36, YANLIS 4), KURULDU 49, ZATEN 37, GUV-RED 11, KUR-DOGRULANMADI 6, diger 6.
Betik tools/kurulum_omer.ps1 (256 kalem; yalniz klon/registry kanitli): SKILL kopya 46 (79 skill klasoru), NPM -g 20, UV tool 17; elle ayrilan 173 -> tmp/kurulum_ayir.tsv: klon yok/silinmis 38, TOPLU skill reposu (>30 SKILL.md) 29, win release asset var ama exe dogrulanamadi 20, kurulum yolu yok 86. Kaynak klonlama yok.
BULUNAMADI-2 (kapsamda 134): en sik neden "kapsam: islenmedi" — coz DOGRULANDI ama kaynak sutunu bos; kaynak cozulmeden yol cikarilamaz.
-Deneme kosusu (kurulumsuz): SKILL DENEME 79 + ZATEN 210 (klasor adi zaten skills/ altinda), NPM 20, UV 17, hata 0.
NOT: sonuc dosyasi rapor/kurulum-omer-sonuc.tsv simdi -Deneme satirlari iceriyor; gercek kosudan once silmeyin, ustune eklenir (durum DENEME ayirt eder).
OMER KOMUTLARI:
1) powershell -NoProfile -ExecutionPolicy Bypass -File tools\kurulum_omer.ps1 -Deneme
2) powershell -NoProfile -ExecutionPolicy Bypass -File tools\kurulum_omer.ps1
Guvenlik kategorisine dokunulmadi; commit/push yok.
