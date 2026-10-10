# Claude Code ile YouTube Videosu Nasıl Yapılır?
## Künye
Claude Code ile YouTube Videosu Nasıl Yapılır? · Berko · süre: 14:00 · tr-KZrcWfPZoKc · https://youtu.be/AYPx7yJmbNg · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 69033 tk · claude-haiku-5-5: claude-haiku-5-5 · 309786 tk
## Özet
Berkay, finans kanalının OpenAI parasını anlatan son videosunu Claude Code ile sekiz mesajla üretme hattını dokuz durakta gösteriyor: kurulum, konu seçimi, araştırma, senaryo, ses, görsel, kurgu/ses tasarımı, kapak ve yayın. Claude Code üç ajanla konu araştırıyor. Codex ikinci göz olarak rakamları doğruluyor ve kapak ile kareleri çiziyor. ElevenLabs ses klonunu, Whisper denetimi, Wan yerel klipleri, Remotion ve FFmpeg kurguyu, CosyVoice dokuz dil dublajını, YouTube Data API yüklemeyi üstleniyor. Bağımsız denetçi ajanlar yanlışları yakalıyor. Videoda 407 araç çağrısı, 11 alt ajan, 6 Codex koşusu ve 3 denetim sayılıyor. Açıklamada başlangıç dosyası ve 7 ipucu var.
## Bölümler
- 0:00 Yapay zekâyla YouTube videosu nasıl yapılır?
- 0:26 Ben kimim, video kimin için
- 0:50 Dokuz durakta bir video
- 1:23 Kurulum: terminal, Claude Code, prompt ve skill'ler
- 3:05 Konu: hangi videoyu yapacağıma nasıl karar veriyorum
- 4:12 Araştırma: her rakamın kaynağı var
- 5:00 Senaryo ve bağımsız denetim
- 6:01 Ses: ElevenLabs ses klonu ve Whisper kontrolü
- 8:10 Görsel: Codex kareleri ve Wan klipleri
- 8:39 Seedance'i neden kullanmadım
- 8:53 Gerçek sayfalar ve başka videolardan ilham
- 9:14 Kodla kurgu: Remotion ve FFmpeg
- 9:57 Ses tasarımı ve dublaj
- 10:48 Kapak ve render denetimi
- 11:18 Yayın: YouTube API ile gizli yükleme
- 12:20 8 prompt, 407 araç çağrısı
- 12:47 Hattın ürettiği videodan bir parça
- 13:39 Kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Claude'un terminalde çalışan hali; dosya okur, yazar, komut çalıştırır. Tüm hattın ana yapay zekâ aracı. | 1:23 | Claude Code, Claude'un terminalde çalışan hali: dosyaları okuyor, yazıyor, komut çalıştırıyor. |
| Opus 5.5 | yok | teknik | yok | Claude Code başlığında görünen model; sunucunun içinde çalıştığı ana model. | 1:30 | Claude Code karşılama kutusunda model adı görünüyor. (karede: kanıttan) Claude Code karşılama kutusunda model adı görünüyor. |
| Skill | yok | skill | https://github.com/berkayburakk/claude-code-youtube-baslangic | Claude'a işin nasıl yapılacağını anlatan, tekrar kullanılan talimat dosyası; video-produce skill'i gösteriliyor. | 2:18 | .claude/skills/ altında video-produce/SKILL.md açık. (karede: kanıttan) .claude/skills/ altında video-produce/SKILL.md açık. |
| CLAUDE.md | yok | teknik | https://github.com/berkayburakk/claude-code-youtube-baslangic | Kanalın kural dosyası: her rakama kaynak, uydurma kanıt yasağı; hatalar kurala ders olarak giriyor. | 2:32 | CLAUDE.md kural dosyası penceresi görünüyor. (karede: kanıttan) CLAUDE.md kural dosyası penceresi görünüyor. |
| Wispr | yok | CLI | yok | Promptları konuşarak yazmak için sesle yazma servisi. | 1:23 | Prompt'larımı çoğunlukla konuşarak yazıyorum, Wispr ile. |
| Codex | yok | CLI | yok | OpenAI'ın kod ajanı; ikinci göz olarak rakam doğrulama, denetim, kare ve kapak çizimi. | 4:12 | Codex, OpenAI'ın kod ajanı; ben onu ikinci göz olarak kullanıyorum. |
| ElevenLabs | yok | CLI | yok | Ses üreten ve klonlayan servis; anlatım, İngilizce ve Türkçe dublaj. | 6:01 | Anlatım benim sesim, ElevenLabs'teki ses klonum. |
| Eleven v4 | yok | teknik | yok | ElevenLabs'in yeni ses modeli; eski modelle dinleyerek kıyaslanıp seçildi. | 6:34 | Model alanında V4 Eleven v4 seçili, kodda model_id eleven_v4. (karede: kanıttan) Model alanında V4 Eleven v4 seçili, kodda model_id eleven_v4. |
| ElevenLabs API | yok | teknik | yok | API anahtarıyla kod üzerinden ses üretimi (text-to-speech with-timestamps). | 6:16 | Developers sayfasında API Keys ve Create Key düğmesi. (karede: kanıttan) Developers sayfasında API Keys ve Create Key düğmesi. |
| Whisper | yok | CLI | https://github.com/openai/whisper | Sesi yazıya çeviren model; üretilen sesi geri dinleyip denetler. | 7:03 | Üretilen sesi bir başka yapay zekâ, Whisper, geri dinliyor. |
| Wan | yok | CLI | https://github.com/Wan-Video/Wan2.2 | Ekran kartında yerel çalışan açık video modeli; karelerden klip üretir. | 8:10 | Kendi bilgisayarımda, ücretsiz bir modelle, Wan ile videoya çeviriyorum. |
| Codex imagegen | yok | teknik | yok | Codex ile sinematik kare ve kapak görseli üretimi, ortak stil referansıyla. | 8:10 | Sinematik kareleri Codex çiziyor; bu videoya özel 18 kare. |
| Remotion | yok | CLI | https://github.com/remotion-dev/remotion | Kodla (React) video yapma aracı; her grafik ve geçiş kod. | 9:14 | Asıl kurgu kodla yapılıyor, Remotion ile. |
| FFmpeg | yok | CLI | yok | Sesleri birleştirme, müziği kısma (sidechain) ve loudnorm ses düzeyi ayarı. | 9:14 | Ses düzeyini ayarlamak gibi işleri de FFmpeg yapıyor. |
| ElevenLabs Music | yok | teknik | yok | Her bölüm için sözsüz müzik parçası üretimi (7 parça). | 9:57 | Müzik de yapay zekâdan, ElevenLabs Music. Her bölüme bir parça. |
| CosyVoice | yok | CLI | https://github.com/FunAudioLLM/CosyVoice | Yerel çalışan açık kaynak ses modeli; sekiz dilde dublaj. | 9:57 | Adı CosyVoice; GitHub'da açık kaynak. |
| YouTube Data API v3 | yok | teknik | yok | Videoyu gizli yüklemek ve başlık/açıklama/bölüm ayarlamak için API. | 11:18 | Google Cloud'da bir proje açıp YouTube Data API'yi etkinleştiriyorsunuz. |
| Google Cloud | yok | teknik | yok | Proje, OAuth istemci kimliği ve JSON kimlik dosyası için konsol. | 10:58 | console.cloud.google.com Credentials, Create credentials menüsü. (karede: kanıttan) console.cloud.google.com Credentials, Create credentials menüsü. |
| YouTube Studio | yok | teknik | yok | Gizli yüklenen videoyu izleme, yapay zekâ beyanı ve görünürlüğü herkese açık yapma; dil/ses parçaları. | 11:18 | studio.youtube.com Video details ve AI use: Yes. (karede: kanıttan) studio.youtube.com Video details ve AI use: Yes. |
| /watch | yok | skill | yok | Bir YouTube videosunu izleyip kare ve konuşma çıkaran komut; ilham için kullanılıyor. | 8:53 | /watch ile videoyu izliyor, karelerini ve konuşmasını çıkarıyor. |
| Seedance | yok | teknik | yok | ByteDance'in kredili bulut video modeli; anlatıldı ama kullanılmadı. | 8:39 | Seedance gibi modellerle video üretmek çok kolay; ama kredisi yüksek. |
| ComfyUI | yok | CLI | yok | Yerel görsel/video üretim sunucusu; Claude akışında arka planda başlatılıyor. | 2:08 | PowerShell(Start ComfyUI server in background) satırı. (karede: kanıttan) PowerShell(Start ComfyUI server in background) satırı. |
| Bağımsız denetçi ajan | yok | iş akışı | yok | İşi yapmamış ajan senaryoyu ve render'ı denetler; yanlış rakamları yakalar. | 5:00 | Senaryo, işi yapmamış bağımsız bir denetçiye gidiyor. · kanıt: yok |
| Alt ajanlar | yok | iş akışı | yok | Konu araştırmasında üç ajan, kurguda sahneleri paralel yazan alt ajanlar. | 3:05 | Claude üç ajanı aynı anda çalıştırdı: gündem, kanıt, şüpheci. |
| WebSearch | yok | teknik | yok | Skill'deki brief adımında gerçek araştırma için kullanılan araç. | 2:18 | Skill listesinde 2. Brief — GERÇEK araştırma yap (WebSearch). (karede: kanıttan) Skill listesinde 2. Brief — GERÇEK araştırma yap (WebSearch). |
| PowerShell | yok | CLI | yok | Windows terminali; kurulum komutu ve Claude'un çağırdığı komutlar. | 1:36 | PowerShell penceresinde irm install.ps1 komutu yazılı. (karede: kanıttan) PowerShell penceresinde irm install.ps1 komutu yazılı. |
| video-produce | yok | skill | https://github.com/berkayburakk/claude-code-youtube-baslangic | Videoyu baştan sona üreten skill: brief, araştırma, plan, senaryo, kontrol döngüsü ve ses adımları. | 2:18 | name: video-produce description: Use when producing a … YouTube video end-to-end (karede: '.claude/skills/video-produce/SKILL.md' başlığı; 'Video Üretim Akışı — Claude Code = Yazar' ve adımlar listeleniyor.) |
| gpt-6.1-so1 | yok | teknik | yok | Codex terminalinde seçili görünen model. Ekranda okunabildiği kadarıyla yazıldı; tam adı belirsiz. | 4:26 | gpt-6.1-so1 medium (karede: Codex terminal ekranı; alt kısımda model satırı görünüyor, metin kısmen okunaklı (gpt-6.1-so1 medium).) |
| Wan2.2 | yok | teknik | https://github.com/Wan-Video/Wan2.2 | Ekran kartında yerel çalışan açık video modeli; Codex kareleri Wan ile klibe çevrildi. | 8:10 | Wan, ekran kartında çalışan açık bir video modeli. |
| Python | yok | teknik | yok | ElevenLabs API çağrılarının ve dublaj scriptlerinin yazıldığı dil. | 6:08 | from elevenlabs.client import ElevenLabs (karede: ElevenLabs Developers sayfasında 'Python' sekmesi altında 'from elevenlabs.client import ElevenLabs' kodu.) |
| Finans videosunun üretim akışını başlatmak | yok | prompt | yok | Video kurgusu için akışın başlatılmasını iste; Anthropic S-1 videosundaki gibi akış sağlam olsun, kanal kurallarına dikkat edilsin. | 2:00 | kaynak: kare |
| Konu seçimi için üç ajanlı araştırma istemek | yok | prompt | yok | Yeni video konuları araştırıp getir; tıklanabilecek, ilgi çekici, çok detaylı olmayan bir konu olsun. | 3:05 | kaynak: altyazı |
| Kredi yenilendiğini Claude'a bildirmek | yok | prompt | yok | ElevenLabs seslendirme kredisini artırdım. | 7:12 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/berkayburakk/claude-code-youtube-baslangic — Başlangıç dosyası: skill, kural dosyası örneği · aday: evet (Skill) · İzleyicinin indirip kullanacağı video üretim skill'i ve CLAUDE.md; videoda anlatılıyor. · sınıf: diğer
- https://code.claude.com/docs/en/quickstart — Claude Code resmi kurulum sayfası · aday: evet (Claude Code) · Claude Code aracının kurulum belgesi; videoda gösteriliyor. · sınıf: diğer
- https://learn.chatgpt.com/docs/codex/cli — Codex CLI sayfası · aday: evet (Codex) · Videoda kullanılan Codex aracı. · sınıf: diğer
- https://elevenlabs.io — ElevenLabs ses servisi · aday: evet (ElevenLabs) · Videoda ses klonu için kullanılan servis. · sınıf: diğer
- https://wisprflow.ai — Wispr Flow sesle yazma aracı · aday: evet (Wispr) · Promptları konuşarak yazmak için kullanılan araç (Wispr). · sınıf: diğer
- https://github.com/openai/whisper — Whisper deposu · aday: evet (Whisper) · Ses denetimi için kullanılan model. · sınıf: diğer
- https://github.com/Wan-Video/Wan2.2 — Wan 2.2 deposu · aday: evet (Wan) · Yerel klip üretimi için kullanılan model. · sınıf: diğer
- https://github.com/remotion-dev/remotion — Remotion deposu · aday: evet (Remotion) · Kodla kurgu aracı. · sınıf: diğer
- https://ffmpeg.org — FFmpeg sitesi · aday: evet (FFmpeg) · Ses birleştirme ve düzey ayarında kullanılan araç. · sınıf: diğer
- https://github.com/FunAudioLLM/CosyVoice — CosyVoice deposu · aday: evet (CosyVoice) · Sekiz dil dublajı için kullanılan yerel model. · sınıf: diğer
- https://developers.google.com/youtube/v3 — YouTube Data API belgesi · aday: evet (YouTube Data API v3) · Yükleme için kullanılan API. · sınıf: diğer
- https://www.youtube.com/watch?v=MeVVCKsCBaY — Önceki video: Claude Skills Nedir? · aday: hayır · Yazarın kendi önceki videosu; referans sayfası, araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| irm https://claude.ai/install.ps1 / iex | Claude Code'u Windows PowerShell'de kurar. (karede: PowerShell penceresinde 'PS youtube-channel> irm https://claude.ai/install.ps1 /' yazılı; sayfada iex'li tam komut.) | 1:36 | kare |
| curl -fsSL https://claude.ai/install.sh / bash | Claude Code'u macOS, Linux ve WSL'de kurar. (karede: Quickstart sayfasında macOS, Linux, WSL başlığı altında bu komut.) | 1:36 | kare |
| curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd | Claude Code'u Windows CMD'de kurar. (karede: Windows CMD başlığı altında curl ... install.cmd && insta... satırı kesik görünüyor.) | 1:36 | kare |
| claude | Claude Code'u başlatır; tarayıcıda Claude hesabıyla giriş açılır. | 1:23 | altyazı |
| claude --version | Kurulu Claude Code sürümünü gösterir. (karede: OCR: 'PS youtube-channel> claude --version' ve 'x.y.z (Claude Code)'; kare görseli yok.) | 1:38 | kare |
| codex | Codex CLI'ı başlatır; ilk açılışta ChatGPT ile giriş yapılır. (karede: Terminalde 'youtube-channel > codex' ve 'Sign in with ChatGPT'.) | 4:26 | kare |
| /watch https://www.youtube.com/watch?v=sLgHqzSe2o0 | Verilen YouTube videosunu izleyip kare ve konuşmayı çıkarır. (karede: OCR satırı '/watch https://www.youtube.com/watch?v=sLgHqzSe2o0'; kare görseli yok.) | 8:40 | kare |
| ffmpeg -f concat -safe 0 -i liste.txt … anlatim.wav | Paragraf seslerini tek anlatım dosyasında birleştirir. (karede: Finans hattı ses penceresinde bu komut vurgulanmış.) | 9:06 | kare |
| loudnorm=I=-14:TP=-1.0:LRA=11 | YouTube ses düzeyine (-14 LUFS) normalleştirir. (karede: 'YouTube ses düzeyi (iki geçiş)' altında loudnorm satırı.) | 9:04 | kare |
| [mu][sc]sidechaincompress=threshold=0.03:ratio=3.5 | Konuşma başlayınca müziği kısar. (karede: muzik_mix.py yorumunun altında sidechaincompress filtresi.) | 9:04 | kare |
| curl -fsSL https://claude.ai/install.cmd -o install.cmd && insta… | Windows CMD için kurulum dosyasını indirip çalıştırır (komutun sonu ekranda kesik). (karede: Docs sayfasında 'Windows CMD:' altında kesik satır görünüyor.) | 1:36 | kare |
| ffmpeg -i input.mp4 output.avi | Bir video dosyasını başka formata dönüştürür (ffmpeg.org sayfasındaki örnek). (karede: ffmpeg.org sayfasında kod kutusunda 'ffmpeg -i input.mp4 output.avi' satırı.) | 9:02 | kare |
| ELEVENLABS_API_KEY=<gizli anahtar> | ElevenLabs anahtarını proje .env dosyasında tutar; değer bu kayıtta yazılmadı ve kimseyle paylaşılmamalı. (karede: '.env · projedeki gizli dosya' ekranında '# ElevenLabs · kimseye gösterilmez' ve maskeli anahtar satırı.) | 6:18 | kare |
| PowerShell: Start ComfyUI server in background | Wan için ComfyUI sunucusunu arka planda başlatır. (karede: Claude Code araç listesinde 'PowerShell(Start ComfyUI server in background)' satırı.) | 2:08 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Video 8 mesajla üretildi; arkasında 407 araç çağrısı, 11 alt ajan, 6 Codex koşusu, 3 denetim vardı. | 12:20 | sayısal |
| Claude ilk akışı 5 dakika 19 saniyede, 9 araçla kurdu. | 2:08 | sayısal |
| Pro ya da Max aboneliği yeterli; ayrı API anahtarı gerekmiyor. | 1:23 | özellik |
| Araştırmada 91 rakam vardı: 56 resmi, 17 haber, 18 kendi hesabı. | 4:12 | sayısal |
| İlk denetimde 3 yanlış, 16 yanıltıcı ifade çıktı; ikinci denetimde sıfır. | 5:00 | sayısal |
| Kararlılık düşük, benzerlik yüksek tutulunca ses daha canlı ve klon daha benzer çıkıyor. | 6:34 | öneri |
| Yeni ElevenLabs modeli eskisinden daha doğal duyuldu. | 7:03 | karşılaştırma |
| Wan ücretsiz ve yerel çalışıyor; Seedance'in kredisi yüksek. | 8:39 | karşılaştırma |
| İlk tam video akış başladıktan 2 saat 18 dakika sonra hazırdı. | 9:14 | sayısal |
| Videoda 189 ses efekti var, hepsi kodla üretildi. | 9:57 | sayısal |
| Render denetiminde ajan 3 kritik hata buldu: vurgulanan rakam söylenenle uyuşmuyordu. | 10:48 | sayısal |
| Test kullanıcısı eklenmezse OAuth yüklemede 403 hatası alınır. | 11:12 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code ile video üretimi | Claude Code | Yapay zekâyla YouTube videosu nasıl yapılır? Baştan sona göstereceğim. |
| konuşma 0:26 | Claude 3.5 Sonnet | aday değil: genel kavram | Yazar yapay zekâ kullanım geçmişini anlatırken geçiyor; videoda kullanılmıyor. |
| kare 1:30 | Opus 5.5 modeli | Opus 5.5 | Claude Code başlığında model adı. |
| kare 1:36 | Kurulum komutları | Claude Code | install.ps1, install.sh, install.cmd. |
| kare 1:36 | PowerShell | PowerShell | PowerShell penceresinde komut. |
| konuşma 1:23 | Wispr ile sesle prompt | Wispr | Prompt'larımı konuşarak yazıyorum, Wispr ile. |
| konuşma 1:23 | Pro/Max aboneliği | aday değil: genel kavram | Abonelik planı, araç değil. |
| konuşma 1:23 | Anthropic S-1 | aday değil: konu dışı | Önceki finans videosunun konusu. |
| kare 2:08 | ComfyUI sunucusu | ComfyUI | PowerShell(Start ComfyUI server in background). |
| kare 2:08 | Remotion kit kopyalama, kit_kopyala.py, op_ses.py | aday değil: başka adayın parçası (Claude Code) | Claude'un yazdığı dosyalar. |
| konuşma 2:25 | Skill | Skill | Skill, Claude'a bir işin nasıl yapılacağını anlatan talimat dosyası. |
| kare 2:18 | video-produce skill'i ve diğer skill klasörleri | Skill | .claude/skills/ listesi. |
| kare 2:18 | WebSearch | WebSearch | Brief adımı WebSearch ile. |
| kare 2:32 | CLAUDE.md kural dosyası | CLAUDE.md | Kanalın kural dosyası. |
| kare 2:44 | uretim-dersleri.md | aday değil: başka adayın parçası (CLAUDE.md) | Hatalardan çıkan kural satırları. |
| kare 2:52 | Claude Skills Nedir? önceki video | aday değil: konu dışı | Yazarın önceki videosu, referans. |
| konuşma 3:05 | Üç ajan: gündem, kanıt, şüpheci | Alt ajanlar | Claude üç ajanı aynı anda çalıştırdı. |
| kare 3:30 | Rakip kanal sayfaları (YouTube, Economy Media) | aday değil: konu dışı | Rakip kanalların gerçek sayfası, analiz verisi. |
| kare 3:26 | Gündem aday konuları | aday değil: konu dışı | Tesla, Bitcoin vb. finans konuları. |
| konuşma 4:12 | Araştırma ajanı ve rakamlar.json | aday değil: başka adayın parçası (Claude Code) | Rakamları kaynakla dosyaya yazıyor. |
| konuşma 4:12 | Codex | Codex | Codex, OpenAI'ın kod ajanı; ikinci göz. |
| kare 4:26 | ChatGPT hesabıyla giriş | aday değil: başka adayın parçası (Codex) | Codex girişi. |
| kare 4:38 | Kullanılmasın listesi | aday değil: başka adayın parçası (Codex) | Doğrulamadan çıkan liste. |
| konuşma 5:00 | Bağımsız denetçi | Bağımsız denetçi ajan | Senaryo bağımsız denetçiye gidiyor. |
| kare 5:24 | RAKAM-DENETIMI.md | aday değil: başka adayın parçası (Bağımsız denetçi ajan) | Denetim çıktısı. |
| konuşma 6:01 | ElevenLabs | ElevenLabs | Anlatım ElevenLabs'teki ses klonum. |
| kare 6:16 | ElevenLabs API anahtarı | ElevenLabs API | API Keys sayfası. |
| kare 6:34 | Eleven v4 | Eleven v4 | Model Eleven v4. |
| konuşma 7:03 | Whisper | Whisper | Whisper geri dinliyor. |
| konuşma 8:10 | Codex kareleri | Codex imagegen | 18 kare. |
| konuşma 8:10 | Wan | Wan | Wan ile videoya çeviriyorum. |
| konuşma 8:39 | Seedance | Seedance | Seedance anlatıldı ama kullanılmadı. |
| kare 8:32 | SoftBank, FT, Amazon 10-Q gerçek sayfaları | aday değil: konu dışı | Videonun finans kaynakları. |
| konuşma 8:53 | /watch | /watch | /watch ile videoyu izliyor. |
| konuşma 9:14 | Remotion | Remotion | Asıl kurgu Remotion ile. |
| konuşma 9:14 | FFmpeg | FFmpeg | Ses işleri FFmpeg. |
| kare 9:04 | loudnorm ve sidechaincompress | aday değil: başka adayın parçası (FFmpeg) | FFmpeg filtreleri. |
| konuşma 9:57 | ElevenLabs Music | ElevenLabs Music | Her bölüme bir parça. |
| konuşma 9:57 | CosyVoice | CosyVoice | Sekiz dil yerel modelle. |
| kare 10:14 | YouTube Studio Languages | YouTube Studio | Ayrı ses parçaları. |
| konuşma 10:48 | Kapak üretimi | aday değil: başka adayın parçası (Codex imagegen) | Codex beş kapak çizdi. |
| konuşma 11:18 | YouTube Data API | YouTube Data API v3 | API etkinleştiriliyor. |
| kare 11:00 | Google Cloud konsolu | Google Cloud | Credentials ekranı. |
| kare 11:32 | AI use beyanı | YouTube Studio | Yes seçili. |
| konuşma 12:20 | Alt ajanlar | Alt ajanlar | 11 alt ajan. |
| açıklama | Başlangıç dosyası deposu | Skill | Skill sade hali ve CLAUDE.md. |
| açıklama | Önceki video bağlantısı | aday değil: konu dışı | Yazarın önceki videosu. |
| açıklama | 7 ipucu | aday değil: genel kavram | İpuçları listesi. |
| linkli sayfa | Claude Code dokümanları | Claude Code | quickstart sayfası. |
| linkli sayfa | Remotion dokümanları, lisans, banger.show | aday değil: başka adayın parçası (Remotion) | remotion.dev alt sayfaları. |
| linkli sayfa | Wispr Flow dokümanları | Wispr | wisprflow.ai alt sayfaları. |
| linkli sayfa | ffmpeg alt siteleri (Sovereign Tech Fund, trac) | aday değil: başka adayın parçası (FFmpeg) | ffmpeg.org alt bağlantıları. |
| linkli sayfa | KSL makalesi | aday değil: konu dışı | OpenAI nakit yakma haberi. |
## Kareden okunanlar
- 0:04: YouTube arama kutusu 'yapay zekâyla youtube videosu nasıl yapılır?' ve altı kutucuk: Claude Code, Voice Clone, Image, Edit, Thumbnail, 9 Languages.
- 1:30: Claude Code karşılama kutusu: Opus 5.5 · ~/youtube-channel; altyazı 'Claude'un terminalde çalışan hali.'
- 1:36: Quickstart sayfasında üç kurulum komutu; PowerShell'de irm install.ps1 yazılıyor.
- 2:08: Akışı kuruyor… (5m 19s · 9 araç); PowerShell ve Write çağrıları, Codex ile 18 kare, ComfyUI sunucusu.
- 2:18: .claude/skills/ listesi (flow-graphic, find-topic, video-produce vb.) ve video-produce SKILL.md adımları.
- 2:44: docs/uretim-dersleri.md satır 308-313: bölüm kartı, iki bağımsız denetçi, Codex kapak, render öncesi kare kontrolü.
- 4:20: Codex doğrulama dosyası: OFFICIAL ve REPORTED etiketleriyle $122B, $852B, $30B, $1.4T.
- 4:26: learn.chatgpt.com Codex CLI sayfası ve terminalde 'codex' ile Sign in with ChatGPT.
- 6:16: ElevenLabs API Keys sayfası, Create Key; anahtar değerleri bulanık.
- 6:34: Model Eleven v4; kodda stability 0.50, similarity_boost 0.75.
- 8:06: Kare Codex'ten klip Wan (yerel) ve github.com/Wan-Video/Wan2.2 sayfası.
- 8:20: seed.bytedance.com Seedance 2.0 sayfası; 'Kredi: Yüksek'.
- 9:04: FFmpeg komutları: concat, sidechaincompress, loudnorm.
- 9:42: ElevenLabs Music 7 sözsüz parça: m0 Açılış … m6 Cevap.
- 10:10: EN, TR ElevenLabs; ES FR DE IT RU JA KO ZH yerel CosyVoice.
- 11:00: Google Cloud Credentials: Create credentials, OAuth client ID.
- 11:32: YouTube Studio AI use: Yes seçili.
## Belirsizlikler
- Karelerde ve OCR'da model adı 'gpt-6.1-sol' ve 'Opus 5.5' okunuyor; OCR bozuk olabilir, ad doğrulanamadı.
- Sözlük eşleşmeleri (Veo, Hermes Agent, Suno, Redis, Descript vb.) yalnızca bulanık eşleşme; videoda kullanıldığına dair kanıt yok.
- Kare listesinde 3:26-3:28 konu kutuları ve açıklamadaki 'VİDEO BÖLÜMLERİ' ile 'VİDEODA KULLANDIĞIM ARAÇLAR' başlıkları boş geldi.
- Yorumlar pakette yok.
- Bağlı sayfalardaki (docs, KSL, remotion.dev) çok sayıda alt bağlantı videoda kullanılmadığından tek tek işlenmedi.
- Kareler 1:37, 3:30 vb. için görsel gelmedi; yalnız OCR'a dayanıldı.
- Wispr'ın ürün adı Wispr Flow olabilir; videoda 'Wispr' söyleniyor, ekranda 'WISPR' görünüyor.
## Atlanan segment oranı
0/22 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/berkayburakk/claude-code-youtube-baslangic | açıklama | açıklama | evet |
| https://code.claude.com/docs/en/quickstart | 1:36 | ekran | evet |
| https://claude.ai/install.sh | 1:36 | ekran | evet |
| https://claude.ai/install.ps1 | 1:36 | ekran | evet |
| https://claude.ai/install.cmd | 1:36 | ekran | evet |
| youtube.com/@ | 3:30 | ekran | hayır |
| https://learn.chatgpt.com/docs/codex/cli | 4:26 | ekran | evet |
| elevenlabs.io/app/voice-lab | 5:52 | ekran | evet |
| https://elevenlabs.io | 5:56 | ekran | evet |
| elevenlabs.io/app/developers | 6:08 | ekran | evet |
| elevenlabs.io/app/developers/api-keys | 6:12 | ekran | evet |
| elevenlabs.io/app/developers/request-log | 6:30 | ekran | evet |
| elevenlabs.io/app/speech-synthesis | 6:34 | ekran | evet |
| https://github.com/Wan-Video/Wan2.2 | 8:06 | ekran | evet |
| seed.bytedance.com/en/seedance2_0 | 8:20 | ekran | evet |
| ft.com | 8:32 | ekran | hayır |
| https://www.youtube.com/watch?v=sLgHqzSe2o0 | 8:40 | ekran | hayır |
| https://github.com/remotion-dev/remotion | 8:48 | ekran | evet |
| remotion.dev | 8:52 | ekran | evet |
| https://ffmpeg.org | 9:02 | ekran | evet |
| https://github.com/FunAudioLLM/CosyVoice | 10:10 | ekran | evet |
| studio.youtube.com | 10:14 | ekran | evet |
| console.cloud.google.com | 10:58 | ekran | evet |
| accounts.google.com | 11:06 | ekran | evet |
| openai.com/index/accelerating-the-next-phase-ai | 12:28 | ekran | hayır |
| ksl.com/article/51625983/openai-expects-to-burn-through-almost-280-billion | 12:54 | ekran | hayır |
| https://wisprflow.ai | açıklama | açıklama | evet |
| https://github.com/openai/whisper | açıklama | açıklama | evet |
| https://developers.google.com/youtube/v3 | açıklama | açıklama | evet |
| https://www.youtube.com/watch?v=MeVVCKsCBaY | açıklama | açıklama | hayır |
| youtube.com/@ (rakip kanal) | 3:30 | ekran | hayır |
| https://seed.bytedance.com/en/seedance2_8 | 8:30 | ekran | evet |
| github.com/Won-Videa/Wan2.2 | 8:31 | ekran | hayır |
| googleapis.com | 10:58 | ekran | hayır |
| googte.com (OCR; büyük olasılıkla google.com) | 11:00 | ekran | hayır |
| https://youtu.be/M_6-AxfKmL8 | 11:18 | ekran | hayır |
| studiatgutube.co (OCR; büyük olasılıkla studio.youtube.com) | 11:32 | ekran | hayır |
## İş akışı
- 1. adım — Terminal açma, Claude Code'u kurma ve Claude hesabıyla giriş yapma — araçlar: PowerShell, Claude Code
- 2. adım — Promptu Wispr Flow ile konuşarak yazma ve kurgu akışını başlatma — araçlar: Wispr Flow, Claude Code
- 3. adım — video-produce skill'i ve CLAUDE.md kural dosyasını klasöre yerleştirme — araçlar: Claude Code, video-produce, CLAUDE.md
- 4. adım — Gündem, kanıt ve şüpheci üç alt ajanla konu araştırması ve konu seçimi — araçlar: Claude Code, WebSearch
- 5. adım — Her rakamı kaynak linkiyle bir dosyaya (rakamlar.json) yazma — araçlar: Claude Code
- 6. adım — Codex ile rakamları bağımsız doğrulama ve 'Kullanılmasın' listesi çıkarma — araçlar: Codex
- 7. adım — Senaryo: iki açılış yazma, sahne ve işaret ekleme, rakamları dosyadan çekme — araçlar: Claude Code
- 8. adım — Senaryoyu bağımsız denetçi ile kontrol etme (1. denetim: 3 yanlış, 16 yanıltıcı; 2. denetim: sıfır) — araçlar: Codex
- 9. adım — ElevenLabs ses klonu ve API anahtarıyla anlatımı üretme (kararlılık 0.50, benzerlik 0.75) — araçlar: ElevenLabs, Python
- 10. adım — Üretilen sesi Whisper ile denetleme; 'debt' hatasını düzeltip paragrafı yeniden üretme — araçlar: Whisper, ElevenLabs
- 11. adım — Codex ile 18 sinematik kare üretme; ComfyUI sunucusunu başlatma — araçlar: Codex, ComfyUI
- 12. adım — Kareleri Wan2.2 ile yerel klibe çevirme — araçlar: ComfyUI, Wan2.2
- 13. adım — Remotion ile kodla kurgu ve sahneleri alt ajanlara yazdırma; kareleri kontrol edip düzeltme — araçlar: Remotion, React, Claude Code
- 14. adım — Anlatım, efekt ve müziği FFmpeg ile birleştirme; müziği konuşma altında kısma ve loudnorm uygulama — araçlar: FFmpeg, ElevenLabs Music
- 15. adım — Dublaj: EN ve TR için ElevenLabs, 8 dil için yerel CosyVoice; rakamları Whisper ile kontrol — araçlar: ElevenLabs, CosyVoice, Whisper
- 16. adım — Kapak: Codex ile 5 kapak çizdirme, logo ve yazı hatalarını eleme, sonuncuyu seçme — araçlar: Codex
- 17. adım — Render sonrası bağımsız ajanla videoyu izletme; vurgulanan rakam hatasını düzeltme ve karede tekrar kontrol — araçlar: Claude Code
- 18. adım — Google Cloud'da proje açma, YouTube Data API v3'ü etkinleştirme, OAuth kimliği oluşturma — araçlar: Google Cloud, YouTube Data API v3
- 19. adım — Claude Code ile videoyu gizli olarak YouTube'a yükleme ve tarayıcıda kanal izni verme — araçlar: Claude Code, YouTube Data API v3
- 20. adım — YouTube Studio'da baştan sona izleme, AI kullanım beyanını Evet işaretleme ve herkese açma — araçlar: YouTube Studio
## Promptlar
- Finans videosunun üretim akışını başlatmak — Video kurgusu için akışın başlatılmasını iste; Anthropic S-1 videosundaki gibi akış sağlam olsun, kanal kurallarına dikkat edilsin.
- Konu seçimi için üç ajanlı araştırma istemek — Yeni video konuları araştırıp getir; tıklanabilecek, ilgi çekici, çok detaylı olmayan bir konu olsun.
- Kredi yenilendiğini Claude'a bildirmek — ElevenLabs seslendirme kredisini artırdım.
ikinci göz KAPALI: --ikinci-goz yok
