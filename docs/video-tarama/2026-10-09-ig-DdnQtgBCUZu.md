# StemKit splits any YouTube song into vocals, drums, bass, guitar, and piano trac
## Künye
StemKit splits any YouTube song into vocals, drums, bass, guitar, and piano trac · gittrend.io · süre: 0:29 · ? · https://www.instagram.com/reel/DdnQtgBCUZu/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-20 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 16286 tk · claude-haiku-5-5: claude-haiku-5-5 · 57830 tk
## Özet
gittrend.io'dan 29 saniyelik reel: StemKit, herhangi bir YouTube şarkısını vokal, davul, bas, gitar ve piyano kanallarına ayıran ücretsiz, yerel çalışan bir masaüstü uygulaması. Şarkı aranır ya da bağlantı yapıştırılır, her enstrüman kendi kaydırıcısında çıkar. Karaoke, acapella, davul+bas ön ayarları ve WAV dışa aktarma var. Moises gibi ücretli bulut ayırıcılara alternatif olarak sunuluyor. Ekranda GitHub README sayfası (kurulum, derleme, mimari, gizlilik) kaydırılıyor.
## Bölümler
- 0:00 StemKit tanıtımı ve GitHub README
- 0:08 İndirme ve kurulum seçenekleri
- 0:15 Geliştirme ve derleme komutları
- 0:19 GitHub Actions ve macOS imzalama
- 0:24 Nasıl çalışır: mimari ve notlar
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| StemKit | yok | CLI | https://github.com/danielravina/stemkit | YouTube şarkılarını vokal, davul, bas, gitar, piyano kanallarına ayıran yerel masaüstü uygulaması | 0:00 | StemKit is a free app that splits any YouTube song into separate instrument tracks. |
| Moises | yok | teknik | yok | Ücretli bulut tabanlı ayırıcı; StemKit'in alternatif olarak anıldığı servis | 0:00 | A free alternative to paid cloud splitters like Moises. |
| yt-dlp | yok | CLI | yok | YouTube sesini indirmek için kullanılan araç (JS runtime ile) | 0:25 | YouTube URL → yt-dlp (+JS runtime) → bundled ffmpeg → mel-band (karede: kanıttan) YouTube URL → yt-dlp (+JS runtime) → bundled ffmpeg → mel-band |
| ffmpeg | yok | CLI | yok | Uygulamayla paketlenen ses/video işleme aracı | 0:09 | ffmpeg is bundled — nothing else to install. (karede: kanıttan) ffmpeg is bundled — nothing else to install. |
| Mel-Band Roformer | yok | teknik | yok | Stüdyo kalitesinde vokal ayırma modeli (isteğe bağlı) | 0:10 | Studio-quality vocals (Mel-Band Roformer): +913 MB (karede: kanıttan) Studio-quality vocals (Mel-Band Roformer): +913 MB |
| htdemucs_ft | yok | teknik | yok | İnce ayarlı demucs ayırma modeli (isteğe bağlı) | 0:10 | Fine-tuned demucs (htdemucs_ft): ~320 MB, up to 4× slower (karede: kanıttan) Fine-tuned demucs (htdemucs_ft): ~320 MB, up to 4× slower |
| Demucs | yok | teknik | yok | Varsayılan ayırma motoru (davul/bas/diğer) | 0:26 | demucs htdemu... (drums/bass/other, shift...) (karede: kanıttan) demucs htdemu... (drums/bass/other, shift...) |
| Electron | yok | teknik | yok | Uygulamanın masaüstü çatısı (renderer, IPC) | 0:27 | Electron renderer IPC events (karede: kanıttan) Electron renderer IPC events |
| Web Audio | yok | teknik | yok | Kanalların tarayıcıda çalınması; ana saat ses | 0:27 | video iframe (muted) + Web Audio stem playback · master clock (karede: kanıttan) video iframe (muted) + Web Audio stem playback · master clock |
| Python | yok | teknik | yok | Ayırma ortamı için özel Python (python-build-standalone) kurulur | 0:09 | First launch creates a private Python environment (karede: kanıttan) First launch creates a private Python environment |
| Node.js | yok | teknik | yok | Kaynaktan derleme için gerekli, 20+ | 0:14 | Node.js 20+ only for building from source (karede: kanıttan) Node.js 20+ only for building from source |
| npm | yok | CLI | yok | Bağımlılık kurma ve geliştirme/derleme betikleri | 0:15 | npm install · npm run dev (karede: kanıttan) npm install · npm run dev |
| GitHub Actions | yok | iş akışı | yok | Sürüm derlemelerini üretir; tag v* ile taslak release | 0:19 | Releases are built by GitHub Actions: push a tag v* (karede: kanıttan) Releases are built by GitHub Actions: push a tag v* |
| GitHub | yok | teknik | https://github.com/danielravina/stemkit | Repo ve README'nin barındığı servis | 0:00 | GitHub - danielravina/stemkit sekme başlığı (karede: kanıttan) GitHub - danielravina/stemkit sekme başlığı |
| Cloudflare Worker | yok | teknik | yok | Anonim kurulum sayacı için istek alan uç (stemkit-stats) | 0:29 | to a Cloudflare Worker ( stemkit-stats. danielravina. workers (karede: kanıttan) to a Cloudflare Worker ( stemkit-stats. danielravina. workers |
| PowerShell | yok | CLI | yok | Windows için fetch-ffmpeg.ps1 betiği | 0:17 | powershell scripts/fetch-ffmpeg.ps1 # windows (one time) (karede: kanıttan) powershell scripts/fetch-ffmpeg.ps1 # windows (one time) |
| gittrend.io | yok | teknik | yok | Videoyu yayınlayan GitHub trend hesabı/sitesi (filigran) | 0:00 | Sağ altta gittrend.io rozeti (karede: kanıttan) Sağ altta gittrend.io rozeti |
| nvm | yok | CLI | yok | Node sürüm yöneticisi; betikler uygun Node sürümüyle yeniden başlar (nvm-windows dahil) | 0:16 | Scripts auto-relaunch with a suitable one (nvm / nvm- (karede: Ekran metni: 'Wrong Node version? Scripts auto-relaunch ... (nvm / nvm-windows)' (OCR)) |
| YouTube | yok | teknik | yok | Uygulamanın arayıp şarkı sesini indirdiği kaynak platform | 0:00 | splits any YouTube song into separate instrument tracks |
| Keychain Access | yok | teknik | yok | macOS sertifika yöneticisi; Developer ID sertifikasını .p12 olarak dışa aktarma | 0:21 | Keychain Access - My Certificates - right-click Developer ID (karede: Ekran metni: '1. Keychain Access - My Certificates - ... Export - .p12' (OCR)) |
| Apple Developer ID | yok | teknik | yok | macOS imzalama sertifikası; CI'da base64 olarak repo secret'a eklenir | 0:20 | macOS builds are Developer-ID-signed when the certificate is avai · kanıt: kare (karede: Ekran metni: 'macOS builds are Developer-ID-signed when the certificate is available' (OCR)) |
| Apple Notary Service | yok | teknik | yok | Apple notarizasyon servisi; Apple Developer üyeliği gerektirir (isteğe bağlı) | 0:23 | Requires an active Apple Developer membership — Apple's notary · kanıt: kare (karede: Ekran metni: 'Requires an active Apple Developer membership — Apple's notary service' (OCR)) |
| pbcopy | yok | CLI | yok | macOS: çıktıyı panoya kopyalar; sertifikayı base64 olarak kopyalamak için | 0:22 | pbcopy (karede: Ekran metni: 'pbcopy' satırı (OCR; tam komut görünmüyor)) |
| xattr | yok | CLI | yok | Karantina özniteliğini kaldırır; imzasız macOS uygulamasını açmak için | 0:12 | Open Anyway (or xattr -cr /Applications/StemKit.app ) (karede: macOS kurulum notunda 'Open Anyway (or xattr -cr /Applications/StemKit.app)' metni) |
| FUSE | yok | teknik | yok | AppImage çalıştırmak için gereken dosya sistemi arayüzü | 0:18 | .AppImage needs FUSE (karede: Ekran metni: '.AppImage needs FUSE. In-app self-update works on the AppImage' (OCR)) |
| dpkg | yok | CLI | yok | Linux'ta .deb paketi üretmek için host gereksinimi | 0:18 | building the .deb needs dpkg + fakeroot on the host (karede: Ekran metni: 'building the .deb needs dpkg + fakeroot on the host' (OCR)) |
| fakeroot | yok | CLI | yok | Linux'ta .deb paketi üretirken root yetkisi taklit eder | 0:18 | building the .deb needs dpkg + fakeroot on the host (karede: Ekran metni: 'building the .deb needs dpkg + fakeroot on the host' (OCR)) |
| CUDA | yok | teknik | yok | NVIDIA GPU hızlandırma; ayırma işlemi için | 0:09 | GPUs (CUDA), AMD GPUs or CPU (karede: Requirements bölümünde 'NVIDIA GPUs (CUDA)' (OCR)) |
| ROCm | yok | teknik | yok | AMD GPU hızlandırma (Linux, deneysel) | 0:13 | AMD via ROCm on Linux (karede: Requirements bölümünde 'AMD via ROCm on Linux' (OCR)) |
| MPS | yok | teknik | yok | Apple Silicon üzerinde GPU hızlandırma (Metal Performance Shaders) | 0:07 | separation runs on Apple Silicon (MPS) (karede: Özellik listesinde 'separation runs on Apple Silicon (MPS)' (ekli kare 2)) |
## Açıklama bağlantıları
- gittrend.io — Tanıtım sitesi; açıklamada 'More like this →' ile verilen bağlantı · aday: hayır · Trend listesi tanıtımı; izleyicinin kullanacağı bir araç ya da servis değil · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npm install | Bağımlılıkları kurar (kaynaktan geliştirme) (karede: (karede OCR) GitHub - danielravina/stem × + github.com/danielravina/stemkit#readme Install © C * : ← → MIT license : Security README Export any stem (or all) as WAV ● Fully offline after setup — separation runs on) | 0:15 | kare |
| npm run dev | Geliştirme modunda uygulamayı başlatır (karede: (karede OCR) GitHub - danielravina/stem × + github.com/danielravina/stemkit#readme Install © C * : ← → MIT license : Security README Export any stem (or all) as WAV ● Fully offline after setup — separation runs on) | 0:15 | kare |
| bash scripts/fetch-ffmpeg.sh | macOS/Linux için ffmpeg ve kütüphaneleri indirir (karede: (karede OCR) GitHub - danielravina/stem × + Install github.com/danielravina/stemkit#readme © C * : ← → Security MIT license : README Windows: Stemkit-Setup-x.y.z.exe (installer) or portable .zip Linux (x64): Stemk) | 0:17 | kare |
| powershell scripts/fetch-ffmpeg.ps1 | Windows için ffmpeg indirir (bir kez) (karede: (karede OCR) GitHub - danielravina/stem × + Install github.com/danielravina/stemkit#readme © C * : ← → Security MIT license : README Windows: Stemkit-Setup-x.y.z.exe (installer) or portable .zip Linux (x64): Stemk) | 0:17 | kare |
| npm run dist:linux | Linux AppImage + deb (x64) derler (karede: (karede OCR) GitHub - danielravina/stem × + Install github.com/danielravina/stemkit#readme © C * : ← → Security MIT license : README Windows: Stemkit-Setup-x.y.z.exe (installer) or portable .zip Linux (x64): Stemk) | 0:17 | kare |
| npm run dist:win | Windows NSIS + zip derler (karede: (karede OCR) GitHub - danielravina/stem × + Install github.com/danielravina/stemkit#readme © C * : ← → Security MIT license : README Windows: Stemkit-Setup-x.y.z.exe (installer) or portable .zip Linux (x64): Stemk) | 0:17 | kare |
| npm run dist:all | Eşleşen işletim sisteminde tüm hedefleri derler (karede: (karede OCR) GitHub - danielravina/steml × + Install % github.com/danielravina/stemkit#readme © C * : ← → : Security README MIT license engine (~2 GB) — one time. fmpeg is bundled — nothing else to install. its ow) | 0:18 | kare |
| xattr -cr /Applications/StemKit.app | macOS Gatekeeper karantinasını kaldırır (karede: (karede OCR) GitHub - danielravina/stem × + github.com/danielravina/stemkit#readme Install © C * : ← → Security MIT license : README 016+4 Features ●Built-in YouTube search, or paste a link Choose your instruments) | 0:12 | kare |
| pbcopy | Sertifika çıktısını (base64) panoya kopyalar; tam komut ekranda görünmüyor (karede: Ekran metni: 'pbcopy' satırı (OCR)) | 0:22 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| StemKit ücretsiz, yerel çalışır; hesap ve yükleme yok | 0:00 | özellik |
| Moises gibi ücretli bulut ayırıcılara ücretsiz alternatif | 0:00 | karşılaştırma |
| İlk açılışta ayırma motoru yaklaşık 2 GB indirilir | 0:09 | sayısal |
| Karaoke, acapella, davul+bas ön ayarları ve WAV dışa aktarma | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | StemKit | StemKit | StemKit is a free app that splits any YouTube song |
| konuşma 0:00 | YouTube | aday değil: genel kavram | search for a song or paste a link |
| konuşma 0:00 | Moises | Moises | paid cloud splitters like Moises |
| konuşma 0:00 | Vokal/davul/bas/gitar/piyano kanalları | aday değil: başka adayın parçası (StemKit) | vocals, drums, bass, guitar, and piano |
| konuşma 0:00 | Karaoke/acapella ön ayarları | aday değil: başka adayın parçası (StemKit) | one-click presets for karaoke, acapella |
| kare 0:00 | gittrend.io | gittrend.io | Sağ alt rozet gittrend.io |
| kare 0:00 | GitHub README | GitHub | github.com/danielravina/stemkit#readme |
| kare 0:00 | MIT license | aday değil: genel kavram | README sekmesi MIT license |
| kare 0:09 | Python | Python | private Python environment |
| kare 0:09 | ffmpeg | ffmpeg | ffmpeg is bundled |
| kare 0:07 | Apple Silicon MPS / CUDA / ROCm | aday değil: genel kavram | separation runs on Apple Silicon (MPS), NVIDIA GPUs (CUDA) |
| kare 0:10 | htdemucs_ft | htdemucs_ft | Fine-tuned demucs (htdemucs_ft) |
| kare 0:10 | Mel-Band Roformer | Mel-Band Roformer | Studio-quality vocals (Mel-Band Roformer) |
| kare 0:12 | xattr -cr | aday değil: başka adayın parçası (StemKit) | xattr -cr /Applications/StemKit.app |
| kare 0:14 | Node.js | Node.js | Node.js 20+ only for building from source |
| kare 0:15 | npm | npm | npm install, npm run dev |
| kare 0:17 | PowerShell | PowerShell | powershell scripts/fetch-ffmpeg.ps1 |
| kare 0:19 | GitHub Actions | GitHub Actions | Releases are built by GitHub Actions |
| kare 0:25 | yt-dlp | yt-dlp | YouTube URL → yt-dlp (+JS runtime) |
| kare 0:26 | demucs | Demucs | demucs htdemu... |
| kare 0:27 | Electron | Electron | Electron renderer IPC events |
| kare 0:27 | Web Audio | Web Audio | Web Audio stem playback |
| kare 0:29 | Cloudflare Worker | Cloudflare Worker | to a Cloudflare Worker |
| kare 0:23 | Apple Developer / notarization | aday değil: genel kavram | Requires an active Apple Developer membership |
| açıklama | Etiketler (#opensource, #karaoke vb.) | aday değil: konu dışı | #opensource #github #karaoke |
## Kareden okunanlar
- 0:00: GitHub README: StemKit, MIT license, 'platform macOS / Windows / Linux', özellik listesi ve uygulama ekran görüntüsü; 'Everything runs locally — no accounts, no API keys'
- 0:07: Features listesi: yerleşik YouTube arama, tek tık ön ayarlar (All, Karaoke, Acapella, Drums + Bass), WAV dışa aktarma, MPS/CUDA/ROCm/CPU
- 0:12: Download bölümü: macOS dmg, Windows exe/zip, Linux AppImage/deb; htdemucs_ft ve Mel-Band Roformer seçenekleri; macOS Open Anyway notu
## Belirsizlikler
- Yorumlar girişsiz alınamadı; 'Stem' yorumuna repo linki gönderileceği söyleniyor.
- Dil bilgisi belirsiz; altyazı İngilizce.
- Sözlük eşleşmeleri Instrument Serif, Linear, Claude, Claude Sonnet ekranda doğrulanamadı; aday yapılmadı.
- OCR'daki bazı metinler bozuk (ör. demucs satırı), ayrıntılar tahmini.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/danielravina/stemkit#readme | 0:00 | ekran | evet |
| https://gittrend.io | 0:00 | ekran | hayır |
| https://gittrend.io | açıklama | açıklama | hayır |
| stemkit-stats.danielravina.workers (OCR ile kısmi okundu) | 0:29 | ekran | hayır |
## İş akışı
- 1. adım — YouTube'da şarkı arama veya bağlantı yapıştırma — araçlar: StemKit, YouTube
- 2. adım — Şarkının sesini indirme ve paketlenmiş ffmpeg ile işleme — araçlar: yt-dlp, ffmpeg
- 3. adım — Enstrüman seçimi: vokal, davul, bas, gitar, piano ya da hazır ön ayarlar — araçlar: StemKit
- 4. adım — Ayırma motorunu seçme: htdemucs_ft ya da Mel-Band Roformer — araçlar: Demucs, Mel-Band Roformer
- 5. adım — GPU/CPU hızlandırma seçimi: MPS, CUDA, ROCm ya da CPU — araçlar: MPS, CUDA, ROCm
- 6. adım — İlk açılış: özel Python ortamı ve ayırma motorunu indirme — araçlar: Python, python-build-standalone
- 7. adım — Ayrılmış parçaları oynatma ve karıştırma (video iframe + ses saati) — araçlar: Electron, Web Audio API
- 8. adım — Stem'leri WAV olarak dışa aktarma — araçlar: StemKit
- 9. adım — Geliştirici kurulumu: bağımlılıkları kurma ve geliştirme modunu başlatma — araçlar: Node.js, npm, nvm
- 10. adım — ffmpeg'i platforma göre hazırlama (bir kez) — araçlar: fetch-ffmpeg.sh, fetch-ffmpeg.ps1, ffmpeg
- 11. adım — Yükleyici paketlerini üretme (Linux, Windows, hepsi) — araçlar: npm, dpkg, fakeroot
- 12. adım — macOS imzalama: sertifikayı Keychain Access ile .p12 olarak dışa aktarma — araçlar: Keychain Access, Apple Developer ID
- 13. adım — Sertifikayı base64 yapıp panoya kopyalama ve repo secret olarak ekleme — araçlar: pbcopy, GitHub Actions
- 14. adım — İsteğe bağlı notarizasyon ayarı (APPLE_* değişkenleri) — araçlar: Apple Notary Service, GitHub Actions
- 15. adım — GitHub Actions ile sürüm yayını: v* tag push ve Draft Release — araçlar: GitHub Actions, GitHub
- 16. adım — macOS'ta imzasız uygulamayı açma: xattr ile karantina kaldırma — araçlar: xattr
- 17. adım — Uygulama ilk açılışta anonim kurulum isteği gönderir — araçlar: Cloudflare Workers
## Promptlar
- yok
