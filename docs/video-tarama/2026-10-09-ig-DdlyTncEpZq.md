# Plexo is a free download manager that pulls one file through every connection yo
## Künye
Plexo is a free download manager that pulls one file through every connection yo · gittrend.io · süre: 0:32 · ? · https://www.instagram.com/reel/DdlyTncEpZq/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-19 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 15706 tk · claude-haiku-5-5: claude-haiku-5-5 · 39782 tk
## Özet
Plexo, Wi-Fi, kablolu bağlantı ve telefonun USB internetini aynı anda kullanarak tek dosyayı parçalara bölüp paralel indiren ücretsiz, açık kaynaklı (MIT) bir indirme yöneticisidir. Video GitHub README sayfasını ve uygulama demosunu gösterir. Toplam 32 bağlantıya kadar çıkar, hızlı arayüzler daha fazla parça alır, duraklat/devam et dosyayı bozmaz, canlı ızgara parçaların inişini gösterir. IDM gibi ücretli yöneticilere alternatif olarak sunulur.
## Bölümler
- 0:00 Plexo tanıtımı ve README sayfası
- 0:04 Demo: iki ağın birleştirilmesi ve toplam hız
- 0:07 USB tethering ve TetherKit notu
- 0:13 Özellik listesi (work-stealing, resume, ızgara, telemetri)
- 0:22 Nasıl çalışır: HTTP range ve localAddress bağlama
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Plexo | yok | CLI | https://github.com/anmolkapil/plexo | Birden çok ağ arayüzünden aynı dosyayı paralel parçalarla indiren açık kaynaklı indirme yöneticisi (Windows, macOS, Linux) | 0:00 | README başlığı Plexo; A fast download manager for Windows, macOS, and Linux (karede: GitHub sayfası anmolkapil/plexo README, Plexo başlığı ve plexo.mp4 demo videosu) |
| TetherKit | yok | teknik | yok | macOS'ta Android USB tethering için çekirdek eklentisiz kullanıcı alanı RNDIS sürücüsü | 0:07 | install TetherKit — a kext-free, user-space RNDIS driver. (karede: README: To use your Android phone's connection over USB, install TetherKit) |
| HTTP range requests | yok | teknik | yok | Dosyayı bayt dilimleri halinde 206 Partial Content ile çekme tekniği | 0:23 | HTTP range requests (206 Partial Content) (karede: kanıttan) HTTP range requests (206 Partial Content) |
| localAddress | yok | teknik | yok | Node.js'te giden isteği belirli yerel IP/ağ arayüzüne bağlama seçeneği | 0:28 | Multi-interface socket binding via localAddress |
| Node.js | yok | teknik | yok | Plexo'nun ağ bağlama motorunun dayandığı çalışma zamanı | 0:29 | Node.js allows outbound HTTP/HTTPS requests to explicitly bind |
| TypeScript | yok | teknik | yok | Projenin yazıldığı dil (açıklama etiketi) | açıklama | #typescript |
| PowerShell Get-NetAdapter | yok | CLI | yok | Windows'ta ağ adaptörü adlarını tespit etmek için kullanılan komut | 0:14 | queries Windows adapters via PowerShell Get-NetAdapter |
| networksetup | yok | CLI | yok | macOS donanım portlarını okuyan komut | 0:14 | macOS hardware ports via networksetup |
| gittrend.io | yok | iş akışı | yok | Videoyu yayınlayan GitHub trend keşif hesabı/servisi | 0:00 | Köşede gittrend.io rozeti (karede: kanıttan) Köşede gittrend.io rozeti |
| GitHub | yok | iş akışı | yok | Plexo reposunun ve README'sinin barındığı servis | 0:00 | GitHub - anmolkapil/plexo sekmesi (karede: kanıttan) GitHub - anmolkapil/plexo sekmesi |
| HoRNDIS | yok | teknik | yok | Eski macOS RNDIS kernel extension'ı; Apple Silicon'da çalışmayı bıraktığı anlatılıyor | 0:00 | why legacy kernel extensions like HoRNDIS stopped working on Apple Silicon (karede: Alt kısımda 'why legacy kernel extensions like HoRNDIS stopped working on Apple Silicon' cümlesi görünüyor) |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Izgara yerleşimi (Grid layout) | Canlı parça ızgarası: her indirme parçasının durumu renkli kutularla gösterilir (karede: Dosya satırının altında yatay yeşil ve kırmızı parça kutuları görünüyor) | 0:07 | kare |
| Alan grafiği (Area chart) | Canlı toplam hız göstergesi ve alan grafiği (karede: Sağ üstte turuncu alan grafiği ve büyük 'TOTAL SPEED' hız değeri (31.0 MB/s) görünüyor) | 0:07 | kare |
| Kart yerleşimi (Card layout) | Her ağ arayüzü için ayrı kart: Wi-Fi ve USB Tether, hız ve akış sayısıyla (karede: Wi-Fi ve USB Tether kartları, her biri için 'streams' ve hız satırı içeriyor) | 0:04 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Plexo en fazla 32 eşzamanlı bağlantı kullanır (arayüz başına 8) | 0:13 | sayısal |
| Hızlı bağlantılar daha fazla parça alır | 0:00 | özellik |
| Duraklat/devam et dosyayı bozmaz | 0:00 | özellik |
| IDM gibi ücretli indirme yöneticilerine ücretsiz alternatif | 0:00 | karşılaştırma |
| Karede iki ağ birleşik toplam hız 93.6 KB/s ve 31.0 MB/s gösterilir | 0:07 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:00 | Plexo | Plexo | GitHub - anmolkapil/plexo |
| ekran 0:00 | GitHub | GitHub | GitHub sekmesi |
| ekran 0:00 | gittrend.io | gittrend.io | rozet ve açıklama |
| ekran 0:00 | MIT license | aday değil: genel kavram | MIT license sekmesi |
| ekran 0:07 | TetherKit | TetherKit | install TetherKit |
| ekran 0:01 | Ubuntu ISO bağlantısı | aday değil: konu dışı | releases.ubuntu.com demo indirme bağlantısı |
| bağlantılı sayfa | cdimage.ubuntu.com ve releases.ubuntu.com sıralama bağlantıları | aday değil: konu dışı | Ubuntu dizin sayfası |
| konuşma 0:00 | IDM | aday değil: konu dışı | paid download managers like IDM |
| ekran 0:14 | PowerShell Get-NetAdapter | PowerShell Get-NetAdapter | README metni |
| ekran 0:14 | networksetup | networksetup | README metni |
| ekran 0:23 | HTTP range requests | HTTP range requests | README başlığı |
| ekran 0:28 | localAddress | localAddress | README başlığı |
| ekran 0:29 | Node.js | Node.js | README metni |
| açıklama | TypeScript | TypeScript | #typescript |
| ekran 0:19 | İnteraktif ilerleme ızgarası | aday değil: başka adayın parçası (Plexo) | README özellik listesi |
| ekran 0:21 | Açık/koyu tema | aday değil: başka adayın parçası (Plexo) | Light & Dark modes |
| ekran 0:11 | React, v0, Three.js, Linear, Make, Stitch, Inter | aday değil: konu dışı | Sözlük eşleşmeleri OCR gürültüsü |
## Kareden okunanlar
- 0:00: GitHub anmolkapil/plexo README; Wi-Fi, Ethernet, USB-tethered phone listesi; plexo.mp4 demosu; altyazı PLEXO IS A
- 0:04: Demo: TOTAL SPEED 93.6 KB/s, ubuntu-26.04.1-desktop-amd64.iso, Wi-Fi 4 streams, USB Tethering; altyazı ONCE.
- 0:07: Demo: TOTAL SPEED 31.0 MB/s, Wi-Fi ve USB Tethering ilerlemesi; README TetherKit notu; altyazı PULLS THEM
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- OCR'da Ubuntu sürümü 26.84.1 olarak bozuk okundu; kareden ubuntu-26.04.1 görünüyor.
- Sözlük eşleşmeleri (React, v0, Three.js, Linear, Make, Stitch, Inter) OCR gürültüsü olabilir; videoda kullanıldığına dair kanıt yok.
- Repo bağlantısı yorumda DM ile verilecek denmiş, yalnızca ekrandaki github.com/anmolkapil/plexo adresi kullanıldı.
- Kurulum komutu videoda gösterilmedi.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/anmolkapil/plexo#readme | 0:00 | ekran | evet |
| gittrend.io | 0:00 | ekran | hayır |
| https://releases.ubuntu.com/26.04.1/ubuntu-26.04.1-desktop-amd64.iso | 0:03 | ekran | hayır |
| releases.ubuntu.com | 0:24 | ekran | hayır |
| http://cdimage.ubuntu.com | açıklama | açıklama | hayır |
| https://releases.ubuntu.com/26.84.1/ubuntu-26.84.1-desktop-amd64 | 0:01 | ekran | hayır |
| https://releases.ubuntu.com/26.84.1/ubuntu-26.84.1-desktop-amd64.iso | 0:03 | ekran | hayır |
## İş akışı
- 1. adım — GitHub'da Plexo README sayfasını açıp projeyi tanıtma — araçlar: GitHub, Plexo
- 2. adım — Demo uygulamaya Ubuntu ISO bağlantısını yapıştırma — araçlar: Plexo
- 3. adım — Algılanan ağ arayüzlerini (Wi-Fi, USB Tethering) seçme — araçlar: Plexo
- 4. adım — Paralel akış sayısını ayarlayıp indirmeyi başlatma — araçlar: Plexo
- 5. adım — Birleşik toplam hızı ve ağ başına paylaşımı izleme — araçlar: Plexo
- 6. adım — macOS'ta USB tethering için TetherKit notunu gösterme — araçlar: TetherKit
- 7. adım — Özellik listesini ve parça ızgarasını gösterme — araçlar: Plexo
- 8. adım — HTTP range ve localAddress ile çalışma mantığını anlatma — araçlar: HTTP range requests, localAddress, Node.js
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
