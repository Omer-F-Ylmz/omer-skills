# vphone-cli boots a virtual iPhone on your Mac, so you can test iOS apps without 
## Künye
vphone-cli boots a virtual iPhone on your Mac, so you can test iOS apps without  · gittrend.io · süre: 0:29 · ? · https://www.instagram.com/reel/DdXZOxTihxj/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-29 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 50651 tk · claude-haiku-5-5: claude-haiku-5-5 · 38119 tk
## Özet
vphone-cli, Apple'ın Virtualization.framework'ünü ve PCC araştırma VM altyapısını kullanarak Mac üzerinde sanal iPhone başlatan açık kaynak bir araçtır. Tek komutla yazılım indirilir, yama uygulanır ve VM başlar; ekran (VNC) veya SSH ile bağlanılır. Ücretli Corellium'a ücretsiz alternatiftir; bir varyant jailbreak ile gelir ve güvenlik araştırmacıları içindir. Video GitHub README'sini kaydırarak gösterir.
## Bölümler
- 0:00 Giriş: Mac'te sanal iPhone ve README
- 0:07 Kurulum ve gereksinimler
- 0:10 Hızlı başlangıç: vm create
- 0:12 VM yönetim komutları
- 0:20 Firmware varyantları ve jailbreak
- 0:23 Bağlanma ve dosya konumları
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| vphone-cli | yok | CLI | https://github.com/Lakr233/vphone-cli | Mac üzerinde sanal iPhone oluşturup başlatan komut satırı aracı | 0:00 | Vphone CLI does it. One command downloads the iPhone software |
| Virtualization.framework | yok | teknik | yok | Apple'ın sanallaştırma çatısı; sanal iPhone'u başlatmak için kullanılır | 0:00 | README: Boot a virtual iPhone via Apple's Virtualization.framework (karede: README başlığı altında açıklama cümlesi Virtualization.framework'ü anıyor) |
| PCC research VM | yok | teknik | yok | VM'in dayandığı Private Cloud Compute araştırma sanal makine altyapısı | 0:00 | README: using PCC research VM infrastructure (karede: README ilk cümlesi: using PCC research VM infrastructure) |
| Corellium | yok | teknik | yok | Aynı iş için ücretli araç; vphone-cli ücretsiz alternatif olarak anılır | 0:00 | free alternative to Corellium, the paid tool for the same job |
| GitHub | yok | teknik | https://github.com/Lakr233/vphone-cli | Deponun README'sinin gösterildiği servis | 0:00 | Tarayıcıda github.com/Lakr233/vphone-cli#readme sayfası (karede: Tarayıcı sekmesi 'GitHub - Lakr233/vphone-cli', adres çubuğunda github.com/Lakr233/vphone-cli#readme) |
| Homebrew | yok | CLI | yok | Bağımlılıkları ve vphone-cli'yi kuran paket yöneticisi | 0:00 | brew install python@3.13 aria2 wget gnu-tar openssl@3 ldid-procursus · kanıt: kare (karede: Kare altında Dependencies bölümünde brew install ... komut satırı) |
| Xcode | yok | CLI | yok | iOS SDK ile misafir daemon'u çapraz derlemek için gereken geliştirme ortamı | 0:00 | Xcode + iOS SDK (cross-compiles the guest daemon) (karede: Host listesinde Xcode + iOS SDK (cross-compiles the guest daemon) maddesi) |
| SSH | yok | CLI | yok | VM'e terminalden bağlanma yöntemi | 0:27 | ssh -p 22222 mobile@<vm-ip> (karede: Running & Connecting: SSH (jailbreak): ssh -p 22222 mobile@<vm-ip>) |
| VNC | yok | teknik | yok | VM ekranına bağlanma yöntemi | 0:27 | vnc://<vm-ip>:5901 · kanıt: kare (karede: Running & Connecting: VNC: vnc://<vm-ip>:5901) |
| Sileo | yok | teknik | yok | jb varyantında kurulan jailbreak paket yöneticisi | 0:27 | + full jailbreak (Sileo, TrollStore auto-install on first boot) (karede: Varyant tablosunda jb satırı notu: Sileo, TrollStore auto-install) |
| TrollStore | yok | teknik | yok | jb varyantında ilk açılışta kurulan uygulama yükleyici | 0:27 | + full jailbreak (Sileo, TrollStore auto-install on first boot) (karede: Varyant tablosunda jb satırı notu: Sileo, TrollStore auto-install) |
| neofetch | yok | CLI | yok | Sanal iPhone terminalinde çalıştırılan sistem bilgisi aracı | 0:00 | Terminalde neofetch çıktısı (karede: README görselinde sağdaki terminal penceresi neofetch çıktısı) |
| ldid-procursus | yok | CLI | yok | İkili imzalama aracı; bağımlılık olarak kurulur | 0:00 | brew install python@3.13 aria2 wget gnu-tar openssl@3 ldid-procursus (karede: Dependencies altında brew install satırı ldid-procursus ile bitiyor) |
| Python | yok | teknik | yok | Araç için otomatik oluşturulan Python ortamı ve bağımlılık | 0:00 | python@3.13 kurulumu; ~/.vphone/venv/ Python ortamı (karede: brew install satırında python@3.13) |
| aria2 | yok | CLI | yok | Firmware indirmek için bağımlılık olarak kurulan indirici | 0:00 | brew install python@3.13 aria2 wget ... (karede: brew install satırında aria2) |
| wget | yok | CLI | yok | Bağımlılık olarak kurulan indirme aracı | 0:00 | brew install python@3.13 aria2 wget ... (karede: brew install satırında wget) |
| gnu-tar | yok | CLI | yok | Bağımlılık olarak kurulan arşiv aracı | 0:00 | brew install ... gnu-tar openssl@3 ... (karede: brew install satırında gnu-tar) |
| OpenSSL | yok | CLI | yok | Bağımlılık olarak kurulan kriptografi kütüphanesi (openssl@3) | 0:00 | brew install ... openssl@3 ldid-procursus (karede: brew install satırında openssl@3) |
| Git | yok | CLI | yok | Depoyu alt modüllerle klonlamak için kullanılır | 0:19 | git clone --recurse-submodules https://github.com/Lakr233/vphone-cli (karede: 0:19 karesinde Quick Start üstü kesik git clone satırı; tam hali OCR'da 0:08) |
| Apple Silicon | yok | teknik | yok | Gerekli ana makine donanımı | 0:00 | Host: Apple Silicon, macOS 15+ (Sequoia) (karede: Prerequisites > Host listesinde Apple Silicon maddesi) |
| APFS | yok | teknik | yok | Hızlı VM klonlama ve seal-volume artefaktları için dosya sistemi | 0:19 | fast APFS clone, fresh (karede: Komut yorumları ve ~/.vphone/tools/ satırında APFS seal-volume ifadesi) |
| SIP/AMFI gevşetme | yok | teknik | yok | Özel PV=3 yetkileri için imzasız ikili ile gereken SIP/AMFI ayarını gevşetme ön koşulu. | 0:00 | SIP/AMFI relaxation to allow private PV=3 entitlements · kanıt: kare (karede: Prerequisites listesinde bağlantılı madde) |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| brew install zqxwce/tap/vphone-cli | vphone-cli'yi Homebrew tap'inden kurar (karede: Gönderilen karelerde yok; yalnız OCR ekran metninde 0:07) | 0:07 | kare |
| git clone --recurse-submodules https://github.com/Lakr233/vphone-cli | Depoyu alt modüllerle klonlar (karede: Gönderilen karelerde yok; OCR ekran metninde 0:08, 0:19 karesinde kısmen) | 0:08 | kare |
| brew install python@3.13 aria2 wget gnu-tar openssl@3 ldid-procursus | Gerekli bağımlılıkları kurar (karede: 0:00 karesinde Dependencies altında brew install satırı) | 0:00 | kare |
| ./scripts/setup_tools.sh | Araç zinciri alt modüllerini ve araçları kurar (karede: Gönderilen karelerde yok; yalnız OCR ekran metninde 0:09) | 0:09 | kare |
| ./scripts/build.sh | vphone-cli'yi derler, imzalar ve paketler (karede: Gönderilen karelerde yok; yalnız OCR ekran metninde 0:09) | 0:09 | kare |
| vphone-cli --help | Yardım çıktısını gösterir (karede: Gönderilen karelerde yok; yalnız OCR ekran metninde 0:09) | 0:09 | kare |
| vphone-cli vm create myphone -V jb | Jailbreak varyantlı VM'i uçtan uca oluşturur (karede: 0:19 karesinde vphone-cli vm create myphone -V jb # -V / --variant) | 0:19 | kare |
| vphone-cli vm launch myphone | Oluşturulan VM'i başlatır (karede: 0:19 karesinde vphone-cli vm launch myphone) | 0:19 | kare |
| vphone-cli vm list | VM'leri listeler (karede: 0:19 karesinde vm list # list VMs) | 0:19 | kare |
| vphone-cli vm info myphone | VM bilgisini gösterir (karede: 0:19 karesinde vm info myphone) | 0:19 | kare |
| vphone-cli vm new myphone | Boş VM paketi oluşturur (karede: 0:19 karesinde vm new myphone) | 0:19 | kare |
| vphone-cli vm config myphone --cpu 8 --memory 8192 | VM'e CPU ve bellek ayarlar (karede: 0:19 karesinde vm config myphone --cpu 8 --memory 8192) | 0:19 | kare |
| vphone-cli vm clone myphone myphone-2 | VM'i hızlı APFS klonuyla kopyalar (karede: 0:19 karesinde vm clone myphone myphone-2) | 0:19 | kare |
| vphone-cli vm export myphone --out myphone.tzst | VM'i arşive aktarır (karede: 0:19 karesinde vm export myphone --out myphone.tzst) | 0:19 | kare |
| vphone-cli vm import myphone.tzst --name restored | Arşivden VM içe aktarır (karede: 0:19 karesinde vm import myphone.tzst --name restored) | 0:19 | kare |
| vphone-cli vm rename myphone iphone16 | VM'i yeniden adlandırır (karede: 0:19 karesinde vm rename myphone iphone16) | 0:19 | kare |
| vphone-cli vm delete iphone16 | VM'i siler (karede: 0:19 karesinde vm delete iphone16) | 0:19 | kare |
| vphone-cli fw prepare myphone --iphone-version 26.1 | Firmware'i indirir ve hazırlar (karede: 0:19 karesinde fw prepare myphone --iphone-version 26.1) | 0:19 | kare |
| vphone-cli fw patch myphone --variant jb | Firmware'e jb varyantı yamalarını uygular (karede: 0:19 karesinde fw patch myphone --variant jb) | 0:19 | kare |
| vphone-cli vm launch myphone --dfu & | VM'i DFU modunda arka planda başlatır (karede: 0:19 karesinde vm launch myphone --dfu &) | 0:19 | kare |
| vphone-cli restore myphone --get-shsh | SHSH blobları alır (karede: 0:19 karesinde restore myphone --get-shsh) | 0:19 | kare |
| vphone-cli restore myphone | DFU restore uygular (karede: 0:19 karesinde restore myphone) | 0:19 | kare |
| vphone-cli cfw install myphone --variant jb | Özel firmware'i (CFW) kurar (karede: Gönderilen karelerde yok; 0:19 karesinde kısmen (cfw ...), tam hali OCR 0:17) | 0:17 | kare |
| vphone-cli vm stop myphone | VM'i durdurur (karede: 0:19 karesinde stop myphone satırı kısmen görünür; tam hali OCR 0:17) | 0:17 | kare |
| ssh -p 22222 mobile@<vm-ip> | Jailbreak VM'ine SSH ile bağlanır (karede: 0:27 karesinde SSH (jailbreak): ssh -p 22222 mobile@<vm-ip>) | 0:27 | kare |
| cd build/vphone-cli.app/Contents/Macos/ | Derlenen uygulamanın ikili dizinine geçer. (karede: Terminalde cd build/vphone-cli.app/Contents/Macos/ komutu (OCR bozuk olabilir)) | 0:09 | kare |
| ssh -p 2222 root@<vm-ip> | Normal/dev SSH bağlantısı kurar (port okunuşu belirsiz, bkz. belirsizlikler). (karede: Running & Connecting bölümünde SSH (regular/dev) satırı) | 0:24 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Tek komutla iPhone yazılımı indirilir, kurulur ve VM başlatılır | 0:00 | özellik |
| Corellium'a ücretsiz alternatiftir | 0:00 | karşılaştırma |
| Bir modda jailbreak önceden kurulu gelir | 0:00 | özellik |
| Beş yama varyantı var: less 4, regular 42, dev 53, jb 113, exp 141 yama | 0:27 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | vphone-cli | vphone-cli | Vphone CLI does it. |
| kare 0:00 | Virtualization.framework | Virtualization.framework | README ilk satırı |
| kare 0:00 | PCC research VM | PCC research VM | README ilk satırı |
| altyazı 0:00 | Corellium | Corellium | free alternative to Corellium |
| kare 0:00 | GitHub | GitHub | Tarayıcıda GitHub README |
| kare 0:00 | Homebrew | Homebrew | brew install komutu |
| kare 0:19 | Git | Git | git clone --recurse-submodules |
| kare 0:00 | Xcode + iOS SDK | Xcode | Xcode + iOS SDK gereksinimi |
| kare 0:00 | python@3.13 | Python | brew install python@3.13 |
| kare 0:00 | aria2 | aria2 | brew install komutu |
| kare 0:00 | wget | wget | brew install komutu |
| kare 0:00 | gnu-tar | gnu-tar | brew install komutu |
| kare 0:00 | openssl@3 | OpenSSL | brew install komutu |
| kare 0:00 | ldid-procursus | ldid-procursus | brew install komutu |
| kare 0:00 | Apple Silicon | Apple Silicon | Host gereksinimi |
| kare 0:00 | macOS 15+ (Sequoia) | aday değil: genel kavram | Yalnız işletim sistemi gereksinimi olarak geçiyor |
| kare 0:00 | SIP/AMFI relaxation | aday değil: genel kavram | Güvenlik ayarı gereksinimi |
| kare 0:00 | neofetch | neofetch | Sanal iPhone terminalinde neofetch |
| kare 0:27 | SSH | SSH | ssh -p 22222 mobile@<vm-ip> |
| kare 0:27 | VNC | VNC | vnc://<vm-ip>:5901 |
| kare 0:27 | Sileo | Sileo | jb varyant notu |
| kare 0:27 | TrollStore | TrollStore | jb varyant notu |
| kare 0:19 | APFS | APFS | fast APFS clone |
| kare 0:00 | MIT license | aday değil: genel kavram | README sekmesi, lisans |
| kare 0:00 | Calendar, FaceTime, Weather uygulamaları | aday değil: konu dışı | Sanal iPhone ana ekranındaki simgeler |
| açıklama | gittrend.io | aday değil: sponsor/reklam | Kanalın kendi tanıtımı: More like this → gittrend.io |
| kare 0:19 | build.sh ve setup_tools.sh | aday değil: başka adayın parçası (vphone-cli) | Depo içi betikler |
| kare 0:19 | fw prepare / fw patch / restore / cfw install | aday değil: başka adayın parçası (vphone-cli) | vphone-cli alt komutları |
| kare 0:27 | ~/.vphone/ dizinleri | aday değil: başka adayın parçası (vphone-cli) | Konum tablosu |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:00: GitHub Lakr233/vphone-cli README: başlık, sanal iPhone ekran görüntüsü, neofetch terminali, gereksinimler (Apple Silicon, macOS 15+, Xcode + iOS SDK, SIP/AMFI gevşetme)
- 0:19: Hızlı başlangıç ve komutlar: vm create myphone -V jb, vm launch, vm list/info/new/config/clone/export/import/rename/delete; manuel build adımları fw prepare, fw patch, restore
- 0:27: Firmware varyant tablosu (less, regular, dev, jb, exp), SSH/VNC bağlantı bilgileri, ~/.vphone/ konum tablosu
## Belirsizlikler
- OCR bazı komutları bozuk okudu (ör. vphone-cl1); komutlar kareler ve bağlamla düzeltildi.
- Sözlük eşleşmelerindeki Bun, Claude, Claude Sonnet videoda gerçekte geçmiyor; OCR gürültüsü sayıldı.
- Ekranda görünen Calendar, FaceTime, Weather gibi sanal iPhone uygulamaları yalnız arayüzde görünüyor, kullanılmıyor.
- Videodaki ana yapay zekâ aracı belirsiz; yorumlar girişsiz alınamadı.
- Komutların hangi sırayla çalıştırıldığı videoda gösterilmiyor; README'den okunuyor.
- Yalnız OCR'da görünen komutların bir kısmı gönderilen 3 karede yok; kaynak 'kare' ekran metnine dayanır.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| github.com/Lakr233/vphone-cli#readme | 0:00 | ekran | evet |
| https://github.com/Lakr233/vphone-cli | 0:08 | ekran | evet |
| gittrend.io | açıklama | açıklama | hayır |
| vnc://<vm-ip>:5901 | 0:27 | ekran | hayır |
## İş akışı
- 1. adım — Gereksinimleri kontrol et: Apple Silicon, macOS 15+, Xcode + iOS SDK — araçlar: Xcode, macOS
- 2. adım — SIP/AMFI ayarını gevşet (özel PV=3 yetkileri için) — araçlar: SIP/AMFI gevşetme
- 3. adım — Homebrew ile vphone-cli'yi kur — araçlar: Homebrew, vphone-cli
- 4. adım — Repoyu alt modüllerle klonla — araçlar: Git
- 5. adım — Bağımlılıkları brew ile kur — araçlar: Homebrew, Python 3.13, aria2, wget, gnu-tar, openssl@3, ldid-procursus
- 6. adım — Uygulamayı derle ve imzala — araçlar: build.sh
- 7. adım — Toolchain alt modüllerini kur ve derle — araçlar: setup_tools.sh
- 8. adım — Derlenen uygulama dizinine geçip yardım komutunu kontrol et — araçlar: vphone-cli --help
- 9. adım — Tek komutla VM oluştur (-V jb): indirme, yama, DFU restore, CFW, ilk açılış — araçlar: vphone-cli
- 10. adım — VM'i başlat ve listele/incele — araçlar: vphone-cli vm launch, vphone-cli vm list, vphone-cli vm info
- 11. adım — Adım adım manuel kurulum: VM oluştur, firmware hazırla, yama uygula, restore et, CFW kur — araçlar: vphone-cli vm new, vphone-cli fw prepare, vphone-cli fw patch, vphone-cli restore, vphone-cli cfw install
- 12. adım — VM'i DFU modunda başlat — araçlar: vphone-cli vm launch --dfu
- 13. adım — VM'i yapılandır (CPU ve bellek) — araçlar: vphone-cli vm config
- 14. adım — VM'i klonla, dışa aktar, içe aktar, yeniden adlandır veya sil — araçlar: vphone-cli vm clone, vphone-cli vm export, vphone-cli vm import, vphone-cli vm rename, vphone-cli vm delete
- 15. adım — VM'e SSH ile bağlan (jailbreak: mobile, regular/dev: root) — araçlar: ssh
- 16. adım — VM ekranına VNC ile bağlan (vnc://<vm-ip>:5901) — araçlar: VNC
- 17. adım — VM'i durdur — araçlar: vphone-cli vm stop
- 18. adım — Dosya konumlarını kontrol et (~/.vphone/ altında VMs, ipsws, tools, debs, venv) — araçlar: vphone-cli
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
