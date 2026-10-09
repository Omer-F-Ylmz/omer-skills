# MVT (Mobile Verification Toolkit) helps with conducting forensics of mobile devi
## Künye
MVT (Mobile Verification Toolkit) helps with conducting forensics of mobile devi · git.radar · süre: 0:59 · ? · https://www.instagram.com/reel/DdjEKF4jDso/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-16 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 31492 tk · claude-haiku-5-5: claude-haiku-5-5 · 29504 tk
## Özet
git.radar reel'i, Amnesty International Security Lab'in geliştirdiği Mobile Verification Toolkit (MVT) GitHub projesini tanıtıyor. Araç, mobil cihazlardaki sistem dosyalarında casus yazılım izlerini (IOC) tarar. Uzmanlar ve araştırmacılar içindir, kişisel sorun giderme için değildir. Video README, kurulum ve kullanım bölümlerini gösteriyor.
## Bölümler
- 0:00 Giriş: Telefonun izleniyor mu?
- 0:14 Aracın işlevi: dijital dedektif ve sistem dosyalarındaki izler
- 0:38 Metal dedektörü benzetmesi, kurulum ve kullanım ekranı
- 0:45 Uzmanlar için tasarım, kişisel kullanım uyarısı, GitHub yönlendirmesi
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| MVT | yok | CLI | https://github.com/mvt-project/mvt | Mobil cihazlarda casus yazılım izlerini adli analizle arayan Mobile Verification Toolkit | 0:00 | README başlığı: Mobile Verification Toolkit; mvt-project/mvt (karede: kanıttan) README başlığı: Mobile Verification Toolkit; mvt-project/mvt |
| GitHub | yok | teknik | yok | Projenin barındırıldığı ve gösterildiği kod platformu | 0:00 | Kare mvt-project/mvt depo sayfasını gösteriyor (karede: kanıttan) Kare mvt-project/mvt depo sayfasını gösteriyor |
| uv | yok | CLI | yok | MVT'yi komut satırı aracı olarak kuran Python paket yöneticisi | 0:38 | Kare: uv tool install mvt komutu (karede: kanıttan) Kare: uv tool install mvt komutu |
| PyPI | yok | teknik | yok | MVT'nin kurulabildiği Python paket dizini | 0:38 | Kare: MVT can be installed from sources or from PyPI (karede: kanıttan) Kare: MVT can be installed from sources or from PyPI |
| pip3 | yok | CLI | yok | MVT'yi PyPI'den kuran Python paket aracı | 0:38 | Kare: pip3 install mvt · kanıt: kare (karede: Kare: pip3 install mvt) |
| mvt-ios | yok | CLI | yok | iOS cihaz edinimlerini analiz eden MVT komutu | 0:38 | Kare: MVT provides three commands: mvt-ios and mvt-android (karede: kanıttan) Kare: MVT provides three commands: mvt-ios and mvt-android |
| mvt-android | yok | CLI | yok | Android cihaz edinimlerini analiz eden MVT komutu | 0:38 | Kare: mvt-ios and mvt-android analyse acquisitions (karede: kanıttan) Kare: mvt-ios and mvt-android analyse acquisitions |
| Python | yok | teknik | yok | MVT'nin yazıldığı programlama dili | açıklama | Açıklamada: Python |
| Indicators of Compromise | yok | teknik | yok | Bilinen casus yazılım kampanyalarının izlerini eşleştiren genel göstergeler (IOC) | 0:14 | Kare: MVT supports using public indicators of compromise (IOCs) (karede: kanıttan) Kare: MVT supports using public indicators of compromise (IOCs) |
| pip | yok | CLI | yok | Python paket yöneticisi; MVT'yi pip3 install mvt komutuyla kurmak için gösterilir. | 0:38 | README'de 'pip3 install mvt' kod kutusu (karede: Installation bölümünde ilk kod kutusunda 'pip3 install mvt' yazısı) |
| curl | yok | CLI | yok | URL'den dosya indiren komut satırı aracı; uv'nin kurulum betiğini indirmek için kullanılır. | 0:38 | README'de 'curl -LsSf https://astral.sh/uv/install.sh / sh' komutu (karede: Installation bölümünde 'curl -LsSf https://astral.sh/uv/install.sh / sh' kod kutusu) |
## Açıklama bağlantıları
- https://github.com/mvt-project/mvt — MVT GitHub deposu · aday: evet (MVT) · Videoda anlatılan araç MVT'nin resmi deposu; izleyici kullanabilir · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pip3 install mvt | MVT'yi PyPI'den pip ile kurar (karede: Kurulum bölümünde pip3 install mvt kod bloğu) | 0:38 | kare |
| curl -LsSf https://astral.sh/uv/install.sh / sh | uv paket yöneticisini kurar (karede: Kod bloğunda curl -LsSf https://astral.sh/uv/install.sh / sh) | 0:38 | kare |
| uv tool install mvt | MVT'yi uv ile komut satırı aracı olarak kurar (karede: Kod bloğunda uv tool install mvt) | 0:38 | kare |
| mvt-ios --verbose check-backup ... | iOS yedek kontrolünü hata ayıklama çıktısıyla çalıştırma örneği; --verbose seçeneği komut adının önüne yazılır. (karede: Usage bölümünde 'mvt-ios --verbose check-backup ...' örneği) | 0:38 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Projenin GitHub'da 13.348 yıldızı var | 0:00 | sayısal |
| Araç sistem dosyalarındaki casus yazılım izlerini otomatik tarar | 0:14 | özellik |
| Kişisel sorun giderme için kullanılmamalı, uzmanlara yöneliktir | 0:45 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | GitHub | GitHub | Altyazı: powerful tool on GitHub with 13,348 stars |
| konuşma 0:00 | Mobile Verification Toolkit | MVT | Altyazı: It's called the Mobile Verification Toolkit |
| konuşma 0:14 | Casus yazılım izleri (IOC) | Indicators of Compromise | Altyazı: tiny, invisible breadcrumbs in the system files |
| konuşma 0:38 | Metal dedektörü benzetmesi | aday değil: genel kavram | Altyazı: Think of it like using a metal detector |
| kare 0:38 | pip3 install mvt | pip3 | Kurulum kod bloğu |
| kare 0:38 | PyPI | PyPI | MVT can be installed from sources or from PyPI |
| kare 0:38 | uv | uv | uv tool install mvt |
| kare 0:38 | astral.sh/uv/install.sh | uv | curl -LsSf https://astral.sh/uv/install.sh / sh |
| kare 0:38 | mvt-ios | mvt-ios | MVT provides three commands: mvt-ios |
| kare 0:38 | mvt-android | mvt-android | mvt-ios and mvt-android analyse acquisitions |
| kare 0:00 | Amnesty International Security Lab | aday değil: başka adayın parçası (MVT) | README: developed and released by Amnesty International Security Lab |
| kare 0:00 | Pegasus Project | aday değil: başka adayın parçası (MVT) | README: in the context of the Pegasus Project |
| kare 0:14 | Access Now Digital Security | aday değil: başka adayın parçası (MVT) | README: forensic partnership with Access Now |
| açıklama | Python | Python | Açıklamada: 🔵 Python |
| açıklama | https://github.com/mvt-project/mvt | MVT | Açıklama bağlantısı |
| açıklama | Hashtag'ler (#opensource, #coding vb.) | aday değil: konu dışı | Açıklamadaki etiketler |
| yorum | Yorumlar | aday değil: konu dışı | Yorumlar girişsiz alınamadı |
## Kareden okunanlar
- 0:00: mvt-project/mvt README: Mobile Verification Toolkit, pypi v2026.9.7, docs ve tests passing, downloads 508k, v3 dalı uyarısı
- 0:14: Not ve Indicators of Compromise bölümü; araç son kullanıcı öz değerlendirmesi için değil
- 0:38: Kurulum: pip3 install mvt, curl ile uv kurulumu, uv tool install mvt; kullanım: mvt-ios, mvt-android, mvt
## Belirsizlikler
- Yorumlar girişsiz alınamadı.
- OCR sözlük eşleşmeleri (Suno, Three.js, Inter, Outfit) videoda kullanılmıyor, yanlış eşleşme sayıldı.
- Pegasus Project, Amnesty International Security Lab ve Access Now yalnızca README metninde geçiyor, araç olarak kullanılmıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/mvt-project/mvt | açıklama | açıklama | evet |
| https://astral.sh/uv/install.sh | 0:23 | ekran | evet |
## İş akışı
- 1. adım — GitHub'daki MVT deposu ve README ekranı gösteriliyor — araçlar: GitHub, MVT
- 2. adım — Aracın amacı ve casus yazılım izi tarama mantığı anlatılıyor — araçlar: MVT, Indicators of Compromise
- 3. adım — Kullanım uyarısı ve IOC bölümü gösteriliyor — araçlar: MVT
- 4. adım — Kurulum seçenekleri gösteriliyor — araçlar: pip3, PyPI, uv
- 5. adım — Kullanım komutları gösteriliyor — araçlar: mvt-ios, mvt-android
- 6. adım — Uzman aracı olduğu belirtilip GitHub sayfasına yönlendiriliyor — araçlar: GitHub
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
