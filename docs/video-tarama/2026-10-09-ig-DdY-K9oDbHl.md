# You built it. Now brag. Turn the project you just created into a short, shareabl
## Künye
You built it. Now brag. Turn the project you just created into a short, shareabl · git.radar · süre: 1:00 · ? · https://www.instagram.com/reel/DdY-K9oDbHl/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-17 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 31952 tk · claude-haiku-5-5: claude-haiku-5-5 · 51103 tk
## Özet
Kısa bir Instagram reel'i: latent-spaces/brag GitHub deposunu tanıtıyor. /brag, projeden tek komutla müzikli, hareketli ve paylaşım metinli kısa bir lansman videosu üreten bir Claude Code skill'i. Videoyu Hyperframes üretiyor. README üzerinden kurulum komutları, kullanım, gereksinimler ve krediler gösteriliyor. Depo 2.364 yıldızlı, Python olarak etiketli.
## Bölümler
- 0:00 Brag tanıtımı ve GitHub README'si
- 0:02 Kurulum: plugin ve skills CLI komutları
- 0:24 Kullanım: /brag, --tone ve --voice
- 0:32 Nasıl çalışır ve gereksinimler
- 0:40 Depo içeriği ve krediler
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| brag | yok | skill | https://github.com/latent-spaces/brag | Projeden tek komutla kısa lansman videosu üreten Claude Code skill'i | 0:00 | README: /brag is a Claude Code skill that turns the project you created (karede: kanıttan) README: /brag is a Claude Code skill that turns the project you created |
| Hyperframes | yok | CLI | yok | Brag'in brief'inden videoyu kuran, zamanlayan ve render eden video aracı | 0:33 | It hands a focused brief to Hyperframes, which builds, times, and renders (karede: kanıttan) It hands a focused brief to Hyperframes, which builds, times, and renders |
| Claude Code | yok | CLI | yok | Skill'in çalıştığı ana yapay zekâ kodlama aracı | 0:00 | A Claude Code skill that turns the project you created (karede: kanıttan) A Claude Code skill that turns the project you created |
| skills CLI | yok | CLI | yok | npx skills add ile skill'i diğer ajanlara kuran komut satırı aracı | 0:06 | npx skills add https://github.com/latent-spaces/brag --skill brag |
| skills.sh | yok | CLI | yok | README'de skill'lere gözatmak için anılan site | 0:07 | (browse on skills.sh) |
| Kokoro | yok | teknik | yok | --voice açıkken Hyperframes üzerinden seslendirme sağlayan model | 0:29 | Narration uses Kokoro through Hyperframes when enabled. |
| FFmpeg | yok | CLI | yok | Gereksinim olarak PATH üzerinde bulunması gereken video aracı | 0:38 | Requirements listesinde: FFmpeg on PATH (karede: kanıttan) Requirements listesinde: FFmpeg on PATH |
| Node.js | yok | teknik | yok | Gereksinim: Node.js 22+ | 0:38 | Requirements listesinde: Node.js 22+ (karede: kanıttan) Requirements listesinde: Node.js 22+ |
| Impeccable | yok | skill | yok | Örnek sahte demo sitelerini üretmekte kullanılan araç | 0:52 | Fake demo sites — built with Impeccable |
| Kenney | yok | teknik | yok | Ses efektleri kaynağı | 0:50 | Credits: Sound effects — Kenney (karede: kanıttan) Credits: Sound effects — Kenney |
| ende.app | yok | teknik | yok | Paketlenmiş müzik kaynağı (Happy Beats / Business Moves) | 0:50 | Credits: Music — ende.app "Happy Beats / Business Moves" (karede: kanıttan) Credits: Music — ende.app "Happy Beats / Business Moves" |
| GitHub Pages | yok | teknik | yok | docs/ klasöründeki lansman sitesini barındırır | 0:44 | docs/ — the launch site (GitHub Pages) |
| Cursor | yok | teknik | yok | Skills CLI ile brag kurulabilen AI kod editörü. | 0:04 | (Cursor, Codex, Copilot, Gemini CLI, opencode, and more) (karede: Metinde '(Cursor, Codex, Copilot, Gemini CLI, opencode, and more)' listesi görünüyor.) |
| Codex CLI | yok | CLI | yok | brag'in desteklendiği ajanlardan; Skills CLI ile kurulur. | 0:04 | (Cursor, Codex, Copilot, Gemini CLI, opencode, and more) (karede: Metinde '(Cursor, Codex, Copilot, Gemini CLI, opencode, and more)' listesi görünüyor.) |
| Copilot | yok | teknik | yok | Skills CLI ile brag kurulabilen ajan (GitHub Copilot). | 0:04 | (Cursor, Codex, Copilot, Gemini CLI, opencode, and more) (karede: Metinde '(Cursor, Codex, Copilot, Gemini CLI, opencode, and more)' listesi görünüyor.) |
| Gemini CLI | yok | CLI | yok | Skills CLI ile brag kurulabilen Google Gemini komut satırı ajanı. | 0:04 | (Cursor, Codex, Copilot, Gemini CLI, opencode, and more) (karede: Metinde '(Cursor, Codex, Copilot, Gemini CLI, opencode, and more)' listesi görünüyor.) |
| opencode | yok | CLI | yok | Skills CLI ile brag kurulabilen ajan; .opencode/skills/brag/ keşif yolunu kullanır. | 0:04 | (Cursor, Codex, Copilot, Gemini CLI, opencode, and more) (karede: Metinde '(Cursor, Codex, Copilot, Gemini CLI, opencode, and more)' listesi görünüyor.) |
| Git | yok | CLI | yok | Windows'ta symlink için git config core.symlinks true ve git clone -c ayarı gerekir. | 0:18 | Windows users: Git requires git config core.symlinks true (karede: Ekran metni (OCR, 0:18): 'Windows users: Git requires git config core.symlinks true'.) |
| Ajana proje için tanıtım videosu ürettirme | yok | prompt | yok | Proje klasöründe ajana 'let's /brag' diyerek brag'i çalıştırmasını ve projeyi tanıtan kısa video üretmesini iste. | 0:24 | kaynak: kare |
| Video tonunu belirleme | yok | prompt | yok | /brag komutuna '--tone' ile 2016 temalı 'sahte Series A lansmanı' tonu vererek videoyu bu tarzda üretmesini iste. | 0:26 | kaynak: kare |
| Seslendirme açma | yok | prompt | yok | Seslendirme varsayılan kapalıdır; açıkça --voice bayrağıyla çalıştırarak anlatım eklemesini iste. | 0:28 | kaynak: kare |
## Açıklama bağlantıları
- https://github.com/latent-spaces/brag.git — brag deposunun git clone adresi · aday: evet (brag) · Videoda anlatılan brag skill'inin deposu; izleyicinin kullanabileceği araç. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /plugin marketplace add latent-spaces/brag | brag marketplace'ini Claude Code'a ekler (karede: Install bölümünde kod bloğunda /plugin marketplace add latent-spaces/brag) | 0:02 | kare |
| /plugin install brag@brag | brag eklentisini kurar (karede: Aynı kod bloğunda /plugin install brag@brag) | 0:02 | kare |
| npx skills add https://github.com/latent-spaces/brag --skill brag | Skill'i skills CLI ile diğer ajanlara kurar | 0:06 | altyazı |
| /brag | Proje klasöründe lansman videosu üretir | 0:24 | altyazı |
| /brag --tone "fake Series A launch from 2016" | Videonun tonunu yönlendirir | 0:26 | altyazı |
| /brag --voice | Seslendirmeyi açar (Kokoro) | 0:28 | altyazı |
| npx hyperframes doctor | Hyperframes CLI kurulumunu kontrol eder (karede: Requirements: Hyperframes CLI — npx hyperframes (check it with npx hyperframes doctor)) | 0:41 | kare |
| git config core.symlinks true | Windows'ta symlink desteğini açar | 0:18 | altyazı |
| npx skills add ... --skill brag -g | -g bayrağı ile skill'i genel olarak kurar (her projede kullanılabilir); bayrak yoksa yalnız mevcut projeye kapsar. (karede: Ekran metni (OCR, 0:07): 'Add -g to install globally (available in every project)'.) | 0:07 | kare |
| git clone -c core.symlinks=true <repo> | Repoyu symlink destekli olarak klonlar. (karede: Ekran metni (OCR, 0:19): 'git clone -c core.symlinks=true' (OCR'da '-true' yazılı).) | 0:19 | kare |
| npx hyperframes | Hyperframes CLI'ını çalıştırır. (karede: Gereksinimler listesinde 'Hyperframes CLI — npx hyperframes' yazıyor.) | 0:41 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Depo 2.364 yıldıza sahip | 0:00 | sayısal |
| Tek komutla müzik, hareket ve paylaşım metni içeren kısa lansman videosu üretir | 0:00 | özellik |
| Seslendirme varsayılan olarak kapalıdır, --voice ile açılır | 0:27 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:00 | GitHub README sayfası | brag | latent-spaces/brag deposu |
| kare 0:00 | Hyperframes | Hyperframes | powered by Hyperframes |
| kare 0:00 | Claude Code | Claude Code | A Claude Code skill |
| konuşma 0:00 | Bragg | brag | This tool called Bragg changes the game |
| açıklama | Python etiketi | aday değil: genel kavram | 🔵 Python |
| açıklama | Hashtag'ler (#github #opensource vb.) | aday değil: genel kavram | #github #opensource #coding |
| açıklama | brag.git bağlantısı | brag | https://github.com/latent-spaces/brag.git |
| ekran 0:06 | npx skills add komutu | skills CLI | npx skills add ... --skill brag |
| ekran 0:07 | skills.sh | skills.sh | browse on skills.sh |
| ekran 0:04 | Cursor, Codex, Copilot, Gemini CLI, opencode | aday değil: konu dışı | Yalnızca uyumlu ajan listesinde geçiyor |
| ekran 0:29 | Kokoro | Kokoro | Narration uses Kokoro through Hyperframes |
| kare 0:50 | FFmpeg ve Node.js 22+ | FFmpeg | Requirements listesi |
| ekran 0:50 | ende.app müzik kredisi | ende.app | Music — ende.app |
| kare 0:50 | Kenney ses efektleri | Kenney | Sound effects — Kenney |
| ekran 0:52 | Impeccable | Impeccable | built with Impeccable |
| ekran 0:44 | GitHub Pages | GitHub Pages | docs/ — the launch site (GitHub Pages) |
| ekran 0:38 | Node.js | Node.js | Node.js 22+ |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamadı |
## Kareden okunanlar
- 0:00: GitHub latent-spaces/brag README; 'You built it. Now brag.' başlığı ve turuncu lansman görseli; Hyperframes ile çalışan Claude Code skill açıklaması
- 0:04: README Install bölümü: /plugin marketplace add latent-spaces/brag ve /plugin install brag@brag; altyazı 'It's like having a professional marketing'
- 0:50: Requirements, What's in this repo ve Credits (ende.app, Kenney); altyazı 'It's basically the difference between showing'
## Belirsizlikler
- Açıklamadaki 'Python' etiketi dışında Python kullanımı videoda gösterilmiyor.
- Sesteki 'Bragg' yazımı depo adı brag ile aynı araç kabul edildi.
- Yorumlar girişsiz alınamadı.
- 'Sözlük eşleşmeleri' (Framer Motion, Matter.js, Stitch, Slack vb.) videoda kullanılmıyor; eşleşmeler yanlış pozitif sayıldı.
- Cursor, Codex, Copilot, Gemini CLI, opencode yalnızca uyumlu ajan listesinde geçiyor, videoda kullanılmıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/latent-spaces/brag.git | açıklama | açıklama | evet |
| https://github.com/latent-spaces/brag | 0:08 | ekran | evet |
| skills.sh | 0:07 | ekran | evet |
| ende.app | 0:50 | ekran | evet |
| https://github.com/iatent-spaces/brag | 0:06 | ekran | evet |
| https://github.com/latent-spaces/brg | 0:11 | ekran | evet |
| https://ithub.com/latent-spaces/brag | 0:13 | ekran | evet |
## İş akışı
- 1. adım — Brag deposunun README'si açılıp tanıtılır — araçlar: GitHub, brag
- 2. adım — Skill, Claude Code'a plugin marketplace ile eklenir ve kurulur — araçlar: Claude Code, brag
- 3. adım — Diğer ajanlar için skills CLI ile kurulum yapılır — araçlar: skills CLI, skills.sh
- 4. adım — Gereksinimler (Node.js 22+, FFmpeg, Hyperframes CLI) kontrol edilir — araçlar: Node.js, FFmpeg, Hyperframes
- 5. adım — Proje klasöründe /brag çalıştırılır, istenirse --tone ve --voice verilir — araçlar: brag, Kokoro
- 6. adım — Hyperframes videoyu kurar, zamanlar ve render eder; brag-output/ klasörü oluşur — araçlar: Hyperframes, FFmpeg
## Promptlar
- Ajana proje için tanıtım videosu ürettirme — Proje klasöründe ajana 'let's /brag' diyerek brag'i çalıştırmasını ve projeyi tanıtan kısa video üretmesini iste.
- Video tonunu belirleme — /brag komutuna '--tone' ile 2016 temalı 'sahte Series A lansmanı' tonu vererek videoyu bu tarzda üretmesini iste.
- Seslendirme açma — Seslendirme varsayılan kapalıdır; açıkça --voice bayrağıyla çalıştırarak anlatım eklemesini iste.
