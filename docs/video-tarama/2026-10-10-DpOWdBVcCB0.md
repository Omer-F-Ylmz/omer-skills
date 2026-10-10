# Tek Bir Prompt ile Profesyonel Youtube Videosu Üretmek: #claude code + #remotion Rehberi
## Künye
Tek Bir Prompt ile Profesyonel Youtube Videosu Üretmek: #claude code + #remotion Rehberi · Burhan KOCABIYIK · süre: 16:53 · tr-orig · https://youtu.be/DpOWdBVcCB0 · şema 2
motor: parti 2026-10-10-short-15 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (58)
kareler: girdi ≤40000 jeton için 60→58
claude-sonnet-5-5: claude-sonnet-5-5 · 66021 tk · claude-haiku-5-5: claude-haiku-5-5 · 101937 tk
## Özet
Burhan Kocabıyık, Claude Code'u VS Code eklentisi olarak kullanıp Remotion ile tek prompttan 1 dakikalık 'İstanbul'un Fethi' videosu üretmeyi gösteriyor. Kurulum: VS Code, Claude Code eklentisi, Node.js, Git ve 'npx skills add remotion-dev/skills'. Ardından plan, soru-cevap (altyazı, çözünürlük), prompt ile düzeltme, YouTube videosundan stil analizi (yt-dlp), maliyet tahmini (2–10 $) ve Kie.ai/fal.ai ile ElevenLabs entegrasyonu anlatılıyor. Dosya paketleri ve krediler ücretli topluluk (Skool DOA) üzerinden sunuluyor.
## Bölümler
- 0:00 Tek Prompt ile Otonom Video Üretme Giriş
- 1:11 Strateji: YouTube Otomasyon Planı ve Doğru Prompt Yazımı
- 1:51 Teknik Altyapı: Dosyaların Önemi ve Topluluk Kaynakları
- 3:37 ReMotion ve Claude Code Entegrasyonu Nasıl Çalışır?
- 4:45 Uygulamalı Kurulum: VS Code ve Extension Ayarları
- 5:41 Adım Adım Terminal Komutları, Node.js ve Git Kurulumu
- 7:05 Örnek Analizi: YouTube Videolarını Klonlama ve Stil Analizi
- 8:46 Maliyet Analizi: 2$ - 10$ Arasında Video Üretmek
- 10:48 Uygulama: İstanbul'un Fethi ve Tarih Kanalı Örneği
- 15:47 Sonuç: Yapay Zeka ile Konuşarak İş Halletme Devri
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Prompttan plan, kod ve video üretimini yürüten ana yapay zekâ kodlama aracı; VS Code eklentisi olarak kullanılıyor. | 5:24 | Menüde 'Claude Code: Open' ve sağ panelde Claude sohbeti görünüyor. (karede: kanıttan) Menüde 'Claude Code: Open' ve sağ panelde Claude sohbeti görünüyor. |
| Remotion | yok | CLI | https://github.com/remotion-dev/remotion | React ile programatik video üreten framework; videonun sahne, geçiş ve animasyonlarını kodluyor. | 3:50 | remotion.dev: 'Make videos programmatically' ve 'npx create-video@latest'. (karede: kanıttan) remotion.dev: 'Make videos programmatically' ve 'npx create-video@latest'. |
| VS Code | yok | CLI | yok | Claude Code eklentisinin kurulduğu editör. | 5:14 | Download Visual Studio Code sayfası gösteriliyor. (karede: kanıttan) Download Visual Studio Code sayfası gösteriliyor. |
| Claude Code eklentisi | yok | plugin | yok | VS Code Extensions bölümünden yüklenen Claude Code uzantısı. | 2:08 | Özet belgede '"Claude Code" extension'ını bul ve yükle' adımı yazıyor. · kanıt: kare (karede: Özet belgede '"Claude Code" extension'ını bul ve yükle' adımı yazıyor.) |
| Remotion skills | yok | skill | yok | remotion-dev/skills paketi; Claude için Remotion best-practices kuralları. | 5:46 | Terminalde 'npx skills add remotion-dev/skills' yazılı. (karede: kanıttan) Terminalde 'npx skills add remotion-dev/skills' yazılı. |
| Skills CLI | yok | CLI | yok | npx skills ile skill ekleyen komut satırı aracı. | 5:46 | 'npx skills add remotion-dev/skills' komutu. (karede: kanıttan) 'npx skills add remotion-dev/skills' komutu. |
| Node.js | yok | CLI | yok | npx/npm için gerekli çalışma ortamı, LTS sürüm indiriliyor. | 5:54 | nodejs.org 'Download Node.js' sayfası, v24.13.1 LTS. (karede: kanıttan) nodejs.org 'Download Node.js' sayfası, v24.13.1 LTS. |
| Git | yok | CLI | yok | Gerekli ön koşul; git-scm.com'dan indiriliyor. | 6:04 | Git for Windows indirme sayfası. (karede: kanıttan) Git for Windows indirme sayfası. |
| nvm | yok | CLI | yok | Node sürüm yöneticisi; Node.js sayfasındaki kurulum seçeneği. | 5:54 | nvm install.sh curl komutu gösteriliyor. (karede: kanıttan) nvm install.sh curl komutu gösteriliyor. |
| Chocolatey | yok | CLI | yok | Windows'ta Node.js kurulum seçeneği. | 5:56 | 'choco install nodejs --version="24.13.1"' komutu. (karede: kanıttan) 'choco install nodejs --version="24.13.1"' komutu. |
| winget | yok | CLI | yok | Windows'ta Git kurulum seçeneği. | 6:04 | 'winget install --id Git.Git -e --source winget'. (karede: kanıttan) 'winget install --id Git.Git -e --source winget'. |
| npm | yok | CLI | yok | Node paket yöneticisi; npm run produce ile üretim betiği çalışıyor. | 8:56 | 'npm run produce' komutu ekranda. (karede: kanıttan) 'npm run produce' komutu ekranda. |
| ElevenLabs | yok | MCP | yok | Türkçe seslendirme (TTS) servisi; API anahtarı .env'e giriliyor. | 8:56 | 'ELEVENLABS_API_KEY=[gizlendi]' ve elevenlabs.io görünüyor. (karede: kanıttan) 'ELEVENLABS_API_KEY=[gizlendi]' ve elevenlabs.io görünüyor. |
| Kie.ai | yok | MCP | yok | AI görsel/video üretim servisi; API anahtarı isteniyor. | 8:56 | Kie.ai anahtarı: kie.ai → Dashboard → API Keys. (karede: kanıttan) Kie.ai anahtarı: kie.ai → Dashboard → API Keys. |
| fal.ai | yok | MCP | yok | Görsel/video üretim API platformu; topluluk kredileri. | 9:24 | fal.ai partnerliği duyuru yazısı ve fal.ai ana sayfası. (karede: kanıttan) fal.ai partnerliği duyuru yazısı ve fal.ai ana sayfası. |
| yt-dlp | yok | CLI | yok | YouTube video meta verisini çekmek için kullanılan araç. | 10:16 | 'python3 -m yt_dlp --dump-json' komutu onay isteği. (karede: kanıttan) 'python3 -m yt_dlp --dump-json' komutu onay isteği. |
| Python | yok | CLI | yok | yt-dlp ve json ayrıştırma betiği için kullanıldı. | 10:16 | 'python3 -m yt_dlp --dump-json' ve python3 -c betiği. (karede: kanıttan) 'python3 -m yt_dlp --dump-json' ve python3 -c betiği. |
| pip | yok | CLI | yok | yt-dlp kurulumu sırasında çıkan pip sürüm bildirimi. | 10:16 | 'A new release of pip is available' notu. (karede: kanıttan) 'A new release of pip is available' notu. |
| Claude Sonnet 4.5 | yok | teknik | yok | Claude Code panelinde seçili model. | 15:00 | Giriş kutusunun altında 'Claude Sonnet 4.5' yazıyor. (karede: kanıttan) Giriş kutusunun altında 'Claude Sonnet 4.5' yazıyor. |
| Antigravity | yok | teknik | yok | Alternatif ajan IDE; Gemini 3 Pro ile Kie.ai/ElevenLabs entegrasyonu yapıldı. | 12:16 | 'Antigravity - Settings' ve görev listesi. (karede: kanıttan) 'Antigravity - Settings' ve görev listesi. |
| Gemini 3 Pro | yok | teknik | yok | Antigravity içindeki model. | 12:20 | Antigravity ayarlarında 'Gemini 3 Pro' yazıyor. (karede: kanıttan) Antigravity ayarlarında 'Gemini 3 Pro' yazıyor. |
| tldraw | yok | iş akışı | yok | Uzun video deneme notlarının tutulduğu beyaz tahta. | 6:16 | tldraw.com sayfasında 'remotion uzun video deneme'. (karede: kanıttan) tldraw.com sayfasında 'remotion uzun video deneme'. |
| Google Docs | yok | iş akışı | yok | Kurulum özeti belgesi. | 2:08 | 'CLAUDE CODE + REMOTION KURULUM ÖZETİ' belgesi. · kanıt: kare (karede: 'CLAUDE CODE + REMOTION KURULUM ÖZETİ' belgesi.) |
| Tailwind CSS | yok | teknik | yok | Remotion projesinde entegre CSS çatısı. | 7:34 | Ekran metni: 'Remotion v4.0.418, Tailwind CSS v4 entegreli'. |
| Remotion Studio | yok | teknik | yok | Videonun önizlendiği yerel studio (localhost:3000). | 8:56 | 'Remotion Studio başarıyla açıldı' mesajı. (karede: kanıttan) 'Remotion Studio başarıyla açıldı' mesajı. |
| Runway | yok | teknik | yok | Plan belgesinde AI video üretimi için önerilen servis (Gen-3). | 6:44 | 'Runway Gen-3 ile 5sn klip' ve maliyet tablosu. (karede: kanıttan) 'Runway Gen-3 ile 5sn klip' ve maliyet tablosu. |
| Visual Studio Code | yok | teknik | yok | Claude Code eklentisinin kurulacağı editör; video projesi burada açılıyor. | 4:45 | VS kodunun indirilmesi |
| PowerShell | yok | CLI | yok | Windows kabuğu; Chocolatey kurulum komutu burada çalıştırılıyor. | 5:56 | powershell -c "irm ... install.ps1/iex" (karede: Node.js sayfasında PowerShell kurulum komutu) |
| Midjourney | yok | teknik | yok | Görsel üretim için prompt hedefi olarak planda anılıyor. | 6:22 | AI Görsel Prompt (Midjourney/DALL-E) (karede: Planda 'AI Görsel Prompt (Midjourney/DALL-E)' başlığı) |
| DALL-E | yok | teknik | yok | Görsel üretim için prompt hedefi olarak planda anılıyor. | 6:22 | AI Görsel Prompt (Midjourney/DALL-E) (karede: Planda 'AI Görsel Prompt (Midjourney/DALL-E)' başlığı) |
| Tek promptla video otomasyon planı | yok | prompt | yok | 1 dakikalık YouTube videosu için tam otomasyon planı: 8-10 sahne, her sahne için AI video, seslendirme, geçişler. Konu verilecek, epik dramatik ton, Türkçe. | 1:11 | kaynak: altyazı |
| İlk sürümü düzeltme | yok | prompt | yok | Yazıları küçült, görseller 5 saniyede bir değişsin. | 8:06 | kaynak: altyazı |
| Stil klonlama | yok | prompt | yok | fern tarzında bana bir video üret, fal ai API anahtarını vereceğim. | 15:00 | kaynak: kare |
| Stil analizi | yok | prompt | yok | Bu videoyu nasıl oluşturabilirim? (YouTube bağlantısıyla) | 8:46 | kaynak: altyazı |
## Açıklama bağlantıları
- https://drive.google.com/drive/folders/1Zg1kjVcxKWLxVcE6xTD4D1y8zGjtvyCI?usp=sharing — Dosya paketi klasörü (Google Drive) · aday: hayır · Yazarın kendi paylaştığı dosya klasörü; araç değil. · sınıf: diğer
- https://drive.google.com/drive/folder — Kesilmiş Drive bağlantısı · aday: hayır · Eksik URL, dosya paylaşımı; araç değil. · sınıf: diğer
- https://www.skool.com/doa — DOA ücretli topluluk · aday: hayır · Topluluk tanıtımı. · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- skool.com/doa/about — DOA topluluğu hakkında sayfa. · aday: hayır · Topluluk tanıtım sayfası; araç değil. · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- skool.com/doa-zero/about — Ücretsiz kaynaklar için Skool sayfası (açıklamada 'tüm kaynaklar %100 ücretsiz'). · aday: hayır · Topluluk kaynak sayfası; araç değil. · sınıf: diğer · erişilemez: giriş gerekli (Skool)
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| npx skills add remotion-dev/skills | Remotion skill paketini Claude Code'a ekler (karede: Terminalde 'npx skills add remotion-dev/skills' yazılı.) | 5:46 | kare |
| npx create-video@latest | Yeni Remotion projesi oluşturur (karede: remotion.dev sayfasında '$ npx create-video@latest'.) | 3:50 | kare |
| npm run produce | Seslendirme ve video üretim betiğini çalıştırır (karede: Claude yanıtında 'npm run produce' görünüyor.) | 8:56 | kare |
| python3 -m yt_dlp --dump-json | YouTube video meta verisini JSON olarak çeker (karede: Bash onay isteğinde komut görünüyor.) | 10:16 | kare |
| curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh / bash | nvm kurar (karede: Node.js sayfasında curl komutu.) | 6:02 | kare |
| choco install nodejs --version="24.13.1" | Windows'ta Node.js kurar (karede: Node.js sayfasında choco komutu.) | 5:56 | kare |
| winget install --id Git.Git -e --source winget | Windows'ta Git kurar (karede: git-scm.com Windows sayfasında winget komutu.) | 6:04 | kare |
| powershell -c "irm https://community.chocolatey.org/install.ps1/iex" | Windows için Chocolatey paket yöneticisini kurar (karede: Node.js sayfasında PowerShell komutu) | 5:56 | kare |
| npm -v | npm sürümünü kontrol eder (beklenen 11.8.0) (karede: 'npm -v # Should print "11.8.0"' satırı) | 5:56 | kare |
| python3 -m yt_dlp --dump-json "<YouTube URL>" | YouTube videosunun başlık, süre, açıklama vb. meta verisini JSON olarak çeker (karede: Terminalde 'python3 -m yt_dlp --dump-json' komutu) | 10:16 | kare |
| which yt-dlp && yt-dlp --dump-json "<YouTube URL>" | yt-dlp kurulu mu kontrol eder ve meta veriyi çeker (karede: Claude Code panelinde 'which yt-dlp' komutu) | 13:22 | kare |
| ELEVENLABS_API_KEY=<anahtar> | ElevenLabs API anahtarını ortam değişkeni olarak tanımlar (değer yazılmadı) (karede: Terminalde 'ELEVENLABS_API_KEY=[gizlendi]' satırı) | 8:56 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bir video 2–10 dolar arası maliyetle üretilebilir; 30 klip görselle ~2,5 $, tam videoyla 8–10 $. | 13:51 | sayısal |
| Videonun tamamı tek prompt ile üretildi. | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Tek promptla üretilen video | Claude Code | Videonun tek promptla üretildiği anlatılıyor. |
| kare 3:50 | Remotion | Remotion | remotion.dev ana sayfası. |
| kare 5:14 | VS Code indirme | VS Code | Download Visual Studio Code. |
| kare 5:56 | Node.js | Node.js | nodejs.org indirme sayfası. |
| kare 6:04 | Git | Git | git-scm Windows sayfası. |
| kare 8:56 | ElevenLabs | ElevenLabs | ELEVENLABS_API_KEY ayarı. |
| kare 10:16 | yt-dlp | yt-dlp | python3 -m yt_dlp komutu. |
| kare 8:46 | fern kanalı | aday değil: konu dışı | Stil örneği olarak aranan YouTube kanalı. |
| kare 8:46 | Incogni reklamı | aday değil: sponsor/reklam | Fern videosunun açıklamasındaki reklam. |
| açıklama | Skool DOA topluluğu | aday değil: konu dışı | Yazarın ücretli topluluğu. |
| kare 12:16 | Antigravity | Antigravity | Antigravity Settings ekranı. |
| kare 3:44 | Replicate, Resend, Rube, n8n | aday değil: konu dışı | Yalnızca tarayıcı öneri listesinde. |
| kare 6:44 | Kling AI, CapCut, DaVinci, Canva, Photoshop, Pika | aday değil: konu dışı | Yalnızca Claude'un maliyet tablosunda geçiyor. |
| kare 7:24 | tldraw | tldraw | Notlar tldraw sayfasında gösteriliyor. |
| kare 2:08 | Google Docs özeti | Google Docs | Kurulum özeti belgesi. |
| yorum | Ollama | aday değil: konu dışı | Yalnızca sözlük eşleşmesi, videoda kullanılmadı. |
## Kareden okunanlar
- 2:08: Google Docs 'CLAUDE CODE + REMOTION KURULUM ÖZETİ': VSCode kur, Claude Code eklentisi, 'npx skills add remotion-dev/skills'.
- 9:24: Skool duyurusu: fal.ai partnerliği, topluluğa özel krediler.
- 15:00: Claude Sonnet 4.5 seçili; 'fern tarzinda...' prompt'u yazılı.
## Belirsizlikler
- Kare verileri bu sohbette görsel olarak doğrulanmadı; kare okumaları OCR ve zaman damgalarına dayanıyor.
- Antigravity ve Gemini 3 Pro'nun kullanımı kısa gösterildi.
- Replicate, Resend, Rube vb. yalnızca tarayıcı önerilerinde göründü, videoda kullanılmadı.
- Runway, Kling, CapCut, DaVinci vb. yalnızca Claude'un maliyet tablosunda geçiyor.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/21 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://code.visualstudio.com/download | 2:08 | ekran | evet |
| https://nodejs.org/en/download | 2:08 | ekran | evet |
| git-scm.com/install/windows | 6:04 | ekran | evet |
| remotion.dev | 3:48 | ekran | evet |
| github.com/remotion-dev/remotion | 3:44 | ekran | evet |
| https://elevenlabs.io | 8:56 | ekran | evet |
| fal.ai | 9:24 | ekran | evet |
| Kie.ai | 8:56 | ekran | evet |
| http://localhost:3000 | 8:56 | ekran | hayır |
| https://www.skool.com/doa | açıklama | açıklama | hayır |
| https://drive.google.com/drive/folders/1Zg1kjVcxKWLxVcE6xTD4D1y8zGjtvyCI?usp=sharing | açıklama | açıklama | hayır |
| skool.com/doa/classroom | 2:12 | ekran | hayır |
| docs.google.com/document/d/1ytl0Noe03ab6X-T_-Jy9kqQOwlT9NLJISyhqfpWiduM/edit | 2:13 | ekran | hayır |
| git-scm.com/install/ | 3:42 | ekran | evet |
| replicate.com | 3:44 | ekran | hayır |
| resend.com/onboarding | 3:44 | ekran | hayır |
| rube.app/chat | 3:44 | ekran | hayır |
| youtube.com/watch?v=7JOruOg3RUw | 3:44 | ekran | hayır |
| n8n.io/workflows/2682-perplexity-research-to-html-ai-powered-content-creation/ | 3:44 | ekran | hayır |
| yscode.dev | 5:14 | ekran | hayır |
| raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | 6:02 | ekran | evet |
| community.chocolatey.org/install.ps1 | 5:56 | ekran | evet |
| Amazon.com | 6:00 | ekran | hayır |
| nodejs.org/dist/v24.13.1/node-v24.13.1.pkg | 6:06 | ekran | evet |
| git-scm.com/book | 6:15 | ekran | hayır |
| tldraw.com/f/1WZ45J1JBmNTGgzZLJHuh | 6:16 | ekran | evet |
| youtube.com | 8:40 | ekran | hayır |
| youtube.com/results?search_query=fern | 8:46 | ekran | hayır |
| incogni.com/ferntv | 8:46 | ekran | hayır |
| localhost:3001 | 9:08 | ekran | hayır |
| skool.com/doa/falai-partnerligimiz-geldi-topluluga-ozel-krediler-ve-startup-program | 9:24 | ekran | hayır |
| www.youtube.com/watch?v=-1DvXSsWKLI | 8:46 | ekran | hayır |
| w-youtube.com/watch?v=-1DvXSsWKLI | 10:52 | ekran | hayır |
| code.vieiaistudio.com/download | 12:48 | ekran | evet |
| localhost:30 (http://localhost:30xx) | 13:22 | ekran | hayır |
| tldraw.com/f/1WZ4 | 15:00 | ekran | evet |
| code.visualstudio.com/downlpad | 15:38 | ekran | evet |
| skool.com/doa-zero/about | açıklama | açıklama | hayır |
| https://drive.google.com/drive/folder | açıklama | yorum | hayır |
## İş akışı
- 1. adım — VS Code indirilip kuruldu — araçlar: VS Code
- 2. adım — Extensions bölümünden Claude Code eklentisi yüklendi — araçlar: VS Code, Claude Code eklentisi
- 3. adım — Node.js LTS ve Git kuruldu — araçlar: Node.js, Git, nvm
- 4. adım — Remotion skill'i terminalden eklendi — araçlar: Skills CLI, Remotion
- 5. adım — Tek prompt ile 1 dakikalık video planı istendi — araçlar: Claude Code
- 6. adım — Altyazı ve çözünürlük soruları yanıtlandı — araçlar: Claude Code
- 7. adım — İlk sürüm üretilip prompt ile düzeltildi — araçlar: Claude Code, Remotion Studio
- 8. adım — API anahtarları ayarlanıp üretim betiği çalıştırıldı — araçlar: Kie.ai, ElevenLabs, npm
- 9. adım — YouTube videosu yt-dlp ile analiz edildi — araçlar: yt-dlp, Python, Claude Code
- 10. adım — Maliyet tahmini alındı — araçlar: Claude Code
- 11. adım — fern tarzında video için fal.ai anahtarı istendi — araçlar: fal.ai, Claude Code
## Promptlar
- Tek promptla video otomasyon planı — 1 dakikalık YouTube videosu için tam otomasyon planı: 8-10 sahne, her sahne için AI video, seslendirme, geçişler. Konu verilecek, epik dramatik ton, Türkçe.
- İlk sürümü düzeltme — Yazıları küçült, görseller 5 saniyede bir değişsin.
- Stil klonlama — fern tarzında bana bir video üret, fal ai API anahtarını vereceğim.
- Stil analizi — Bu videoyu nasıl oluşturabilirim? (YouTube bağlantısıyla)
