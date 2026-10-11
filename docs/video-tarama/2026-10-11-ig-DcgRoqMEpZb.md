# Comment 'SEARCH' and I'll send it over.
## Künye
Comment 'SEARCH' and I'll send it over. · nateherkai · süre: 0:27 · ? · https://www.instagram.com/reel/DcgRoqMEpZb/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-11-short · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 17747 tk · claude-haiku-5-5: claude-haiku-5-5 · 40178 tk
## Özet
Nate Herk'in kısa reel'i: Panniantong'un açık kaynak 'agent-reach' GitHub deposu, yapay zekâ ajanına Twitter, Reddit, YouTube, GitHub, LinkedIn, Instagram gibi 13 platforma ücretsiz erişim veriyor. YouTube altyazısı çekme, Reddit arama, Twitter okuma ve bot engelli sitelere erişim anlatılıyor. Ekranda pipx ile kurulum gösteriliyor. Yorumlara 'SEARCH' yazana repo gönderilecek.
## Bölümler
- 0:00 Açık kaynak depo tanıtımı: 13 platforma erişim
- 0:09 pipx ile agent-reach kurulumu
- 0:16 Claude ve ChatGPT'nin zorlandığı yerler, bot engeli
- 0:26 Çağrı: 'search' yorumu yap
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| agent-reach | yok | CLI | https://github.com/Panniantong/agent-reach | Yapay zekâ ajanına 13 platforma (Twitter, Reddit, YouTube, GitHub, LinkedIn, Instagram vb.) ücretsiz erişim veren açık kaynak depo/araç | 0:10 | Terminalde pipx install .../agent-reach/archive/main.zip ve 'installed package agent-reach 0.1.0' (karede: GitHub deposu sayfası (Panniantong/agent_reach) dosya listesiyle; yeni kare gönderilen kareler arasında 0:01 görüntüsü) |
| pipx | yok | CLI | yok | agent-reach'i global kurmak için kullanılan Python uygulama yükleyicisi | 0:09 | OCR: 'pipx install https://github.com/Panniantong/agent-reach/archive/main.zip' (karede: Terminal kare sırasında değil; OCR metni (0:09-0:10) kurulum çıktısını gösteriyor) |
| Claude | yok | teknik | yok | Ajan erişiminde zorlanan örnek model olarak anılıyor | 0:00 | places that Claude and ChatGPT normally struggle with |
| ChatGPT | yok | teknik | yok | Erişimde zorlanan örnek model olarak anılıyor | 0:00 | places that Claude and ChatGPT normally struggle with |
| Claude Code | yok | CLI | yok | Ekranda CronCreate hatırlatıcı ile çalışan ajan arayüzü (VS Code içinde) | 0:02 | OCR: 'ctrl esc to focus or unfocus Claude', 'CronCreate' (karede: Bu zaman için kare gönderilmedi; OCR metnine dayanır) |
| Visual Studio Code | yok | teknik | yok | Claude Code oturumunun çalıştığı editör | 0:02 | OCR: 'remind me at 10:23 am to.. - Herk-2 - Visual Studio Code' (karede: Bu zaman için kare gönderilmedi; OCR metnine dayanır) |
| Codex CLI | yok | CLI | yok | Bot engeli bölümünde gösterilen Codex CLI görevi kaydı | 0:16 | Kare: 'Fix /diff error with special characters in filename', 'Codex CLI', Logs (karede: Üstte Codex CLI görev kaydı (Logs, AGENTS.md, shell komutu), altta konuşmacı ve 'BOT BLOCKED' yazısı) |
| Postman | yok | teknik | yok | Açığa çıkmış API anahtarı arama ekranı gösteriliyor | 0:18 | OCR: 'My Postman', 'Paste key to search', 'postman-api-key-in-collection' (karede: Bu zaman için kare gönderilmedi; OCR metnine dayanır) |
| Voicebox | yok | MCP | yok | Ses klonlama/yazıya dökme için yerel MCP sunucusu ve REST API dokümanı | 0:23 | Kare: 'Voicebox ships a built-in Model Context Protocol server'; claude mcp add voicebox (karede: Üstte curl örnekleri (/generate, /speak, /transcribe, /profiles) ve 'claude mcp add voicebox' komutu, altta konuşmacı ve 'GITHUB REPOS' yazısı) |
| Whisper | yok | teknik | yok | Voicebox transkripsiyon örneğinde model | 0:23 | Kare: -F "model=whisper-turbo" (karede: curl /transcribe örneğinde model=whisper-turbo) |
| yt-dlp | yok | CLI | yok | agent-reach commit mesajlarında YouTube desteği için anılıyor | 0:01 | Kare: 'fix(youtube): align yt-dlp runtime support' (karede: GitHub dosya listesinde commit mesajı fix(youtube): align yt-dlp runtime support) |
| OpenCLI | yok | CLI | yok | xiaohongshu kanalı için OpenCLI durumu çözümleme commit'inde anılıyor | 0:01 | Kare: 'fix(xiaohongshu): resolve OpenCLI status at...' (karede: agent_reach satırında commit mesajı resolve OpenCLI status) |
| Python | yok | teknik | yok | Programlama dili. Terminal çıktısında agent-reach'in Python 3.11.6 ile kurulduğu görülüyor. | 0:10 | installed package agent-reach 0.1.0, installed using Python 3.11.6 (karede: kanıttan) installed package agent-reach 0.1.0, installed using Python 3.11.6 |
| curl | yok | CLI | yok | Terminalden HTTP istekleri gönderen komut satırı aracı. Voicebox uç noktalarını çağırmak için kullanılıyor. | 0:23 | curl -X POST http://127.0.0.1:17493/generate \ (karede: kanıttan) curl -X POST http://127.0.0.1:17493/generate \ |
| Codex CLI'ye bir GitHub issue'sunu çözdürme (bağlam örneği) | yok | prompt | yok | Filename'de özel karakter olunca 'diff' komutunun hata verdiği bir GitHub issue'sunu çözmesi isteniyor. Sorunu yeniden üretmek için geçici bir git reposu ve 'a$b.txt' gibi bir dosya kullanılıyor, Codex CLI'nin bilgi istediği alanlar (sürüm, model, platform, adımlar) doldurulmuş. | 0:16 | kaynak: kare |
| Codex'e sandbox içi test adımlarını yaptırma | yok | prompt | yok | Sandbox içinde ilk komut olarak bir ASCII kedi çıktısı yazdırılması, ardından geçici bir git reposu oluşturulup 'a$b.txt' adlı dosyayla hatanın tekrar üretilmesi isteniyor. | 0:16 | kaynak: kare |
| Kaynaklara dayalı özet/brifing istemi (bağlam) | yok | prompt | yok | Gen AI stratejisi için temel konuları, verilen kaynaklara dayanarak özetleyen bir istem (Google NotebookLM benzeri arayüz). | 0:12 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| pipx install https://github.com/Panniantong/agent-reach/archive/main.zip | agent-reach paketini pipx ile global kurar (karede: Terminal görüntüsü OCR'da okunuyor; bu zaman için kare gönderilmedi) | 0:10 | kare |
| agent-reach install --env=auto | agent-reach kurulumunu ortamı otomatik algılayarak çalıştırır (karede: Bu zaman için kare gönderilmedi; OCR'daki 'agent-reach install' ve '--env=auto' satırlarına dayanır) | 0:10 | kare |
| claude mcp add voicebox --transport http --url http://127.0.0.1:17493/mcp | Voicebox MCP sunucusunu Claude Code'a ekler (karede: Claude Code one-liner altında claude mcp add voicebox, --transport http, --url http://127.0.0.1:17493/mcp) | 0:23 | kare |
| agent-reach install | Kurulu agent-reach'in kurulum adımını çalıştırır (ayrıntı ekranda yok) (karede: (karede OCR) agent-reach - zsh . pipx install https://github.com/Panniantong/agent-reach/archive/main.zip Dounloading archive... Installing agent-reach... installed package agent-reach 0.1.0, installed using Pytho) | 0:10 | kare |
| claude mcp add voicebox --transport http --url http://127.0.0.1:17493/mcp --header "X-Voicebox-Client-Id: …" | Claude Code'a Voicebox MCP sunucusunu HTTP transport ile ekler (header değeri kesik okundu) (karede: Voicebox README'sinde 'Claude Code one-liner:' altındaki komut bloğu; header satırı kesik.) | 0:23 | kare |
| curl -X POST http://127.0.0.1:17493/generate -H "Content-Type: application/json" -d '{"text":"Hello world","profile_id":"abc123","language":"en"}' | Voicebox ile metinden konuşma üretir (karede: '# Generate speech' başlıklı curl bloğu.) | 0:23 | kare |
| curl -X POST http://127.0.0.1:17493/speak -H "Content-Type: application/json" -H "X-Voicebox-Client-Id: my-script" -d '{"text":"Deploy complete.","profile":"Morgan"}' | Verilen ses profiliyle metni seslendirir (karede: '# Agent voice output' başlıklı curl bloğu.) | 0:23 | kare |
| curl -X POST http://127.0.0.1:17493/transcribe -F "audio=@recording.wav" -F "model=whisper-turbo" | Ses dosyasını whisper-turbo modeliyle metne çevirir (karede: '# Transcribe an audio file' başlıklı curl bloğu.) | 0:23 | kare |
| curl http://127.0.0.1:17493/profiles | Kayıtlı ses profillerini listeler (karede: '# List voice profiles' başlıklı curl bloğu.) | 0:23 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Depo 13 farklı platforma ücretsiz erişim sağlıyor | 0:00 | sayısal |
| Claude ve ChatGPT'nin zorlandığı yerlere erişebiliyor, bot engelli siteleri aşabiliyor | 0:00 | karşılaştırma |
| Normalde birden çok API ve ücretli abonelik gerekirken tek ücretsiz araç | 0:00 | karşılaştırma |
| YouTube transkriptlerini çekebilir, Reddit'te arama yapabilir, Twitter okuyabilir | 0:00 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | agent-reach deposu (açık kaynak GitHub repo) | agent-reach | Someone just released an open source GitHub repo |
| konuşma 0:00 | Twitter | aday değil: genel kavram | Twitter, Reddit, YouTube, GitHub, LinkedIn, Instagram |
| konuşma 0:00 | Reddit | aday değil: genel kavram | search Reddit threads |
| konuşma 0:00 | YouTube | aday değil: genel kavram | pull YouTube transcripts |
| konuşma 0:00 | GitHub | aday değil: genel kavram | open source GitHub repo |
| konuşma 0:00 | LinkedIn | aday değil: genel kavram | LinkedIn, Instagram, and more |
| konuşma 0:00 | Instagram | aday değil: genel kavram | LinkedIn, Instagram, and more |
| konuşma 0:00 | Claude | Claude | places that Claude and ChatGPT normally struggle with |
| konuşma 0:00 | ChatGPT | ChatGPT | places that Claude and ChatGPT normally struggle with |
| konuşma 0:00 | API'ler ve ücretli abonelikler | aday değil: genel kavram | you'd need multiple APIs and paid subscriptions |
| konuşma 0:00 | Yorum çağrısı 'search' | aday değil: sponsor/reklam | Just comment, search, and I'll send you the repo. |
| kare 0:01 | agent-reach GitHub sayfası | agent-reach | Panniantong deposu dosya listesi |
| kare 0:01 | yt-dlp commit | yt-dlp | fix(youtube): align yt-dlp runtime support |
| kare 0:01 | OpenCLI commit | OpenCLI | resolve OpenCLI status |
| kare 0:01 | CLAUDE.md, llms.txt, CHANGELOG.md, test.sh dosyaları | aday değil: başka adayın parçası (agent-reach) | Depo dosya listesinde |
| kare 0:01 | GitHub Actions workflows (.github/workflows) | aday değil: başka adayın parçası (agent-reach) | ci: add wheel-build gate |
| kare 0:01 | Facebook/Instagram kanalı | aday değil: başka adayın parçası (agent-reach) | feat(channels): add facebook and instagram |
| kare 0:01 | xiaohongshu kanalı | aday değil: başka adayın parçası (agent-reach) | fix(xiaohongshu) |
| ekran 0:02 | Claude Code / CronCreate | Claude Code | CronCreate, 'Reminder set for 10:23 AM' |
| ekran 0:02 | Visual Studio Code | Visual Studio Code | remind me at 10:23 am to.. - Herk-2 - Visual Studio Code |
| ekran 0:09 | pipx install komutu | pipx | pipx install https://github.com/Panniantong/agent-reach/archive/main.zip |
| ekran 0:10 | Python 3.11.6 | aday değil: genel kavram | installed using Python 3.11.6 |
| ekran 0:10 | zsh terminal | aday değil: genel kavram | agent-reach - zsh |
| ekran 0:12 | Not defteri / briefing doc ekranı | aday değil: konu dışı | Briefing doc, Save to note, Google Cloud AI strategy metni |
| ekran 0:13 | Reddit gönderisi/yorumları (kira) | aday değil: konu dışı | Top 1% Commenter, Reply Award Share |
| kare 0:16 | Codex CLI görevi | Codex CLI | Fix /diff error..., Codex CLI, AGENTS.md |
| ekran 0:18 | Postman API anahtarı arama | Postman | Paste key to search, My Postman |
| ekran 0:19 | Fiyat tablosu (aylık/yıllık krediler) | aday değil: konu dışı | Pay annually - 10% discount, MOST POPULAR |
| kare 0:23 | Voicebox MCP sunucusu | Voicebox | Voicebox ships a built-in Model Context Protocol server |
| kare 0:23 | whisper-turbo modeli | Whisper | model=whisper-turbo |
| kare 0:23 | Cursor, Windsurf, Cline | aday değil: konu dışı | MCP-aware agent listesi; videoda kullanılmıyor, yalnız dokümanda |
| kare 0:23 | claude mcp add voicebox komutu | Voicebox | claude mcp add voicebox --transport http |
| ekran 0:26 | agent-reach commit listesi | agent-reach | Panniantong Merge pull request #530 |
## Kareden okunanlar
- 0:01: GitHub sayfası: Panniantong/agent-reach, 81.4k yıldız, 75 issue, 97 pull request, dosyalar (agent_reach, CLAUDE.md, llms.txt, pyproject.toml, test.sh); üstte 'AN OPEN SOURCE GITHUB REPO'
- 0:16: Codex CLI görevi: 'Fix /diff error with special characters in filename', model o4-mini, loglarda AGENTS.md ve shell komutu; 'BOT BLOCKED' yazısı
- 0:23: Voicebox dokümanı: curl örnekleri 127.0.0.1:17493 ve MCP sunucusu için claude mcp add voicebox komutu; 'GITHUB REPOS' yazısı
## Belirsizlikler
- Yorumlar girişsiz alınamadı; yorumlardaki bağlantılar bilinmiyor.
- Videoda 13 platformun tamamı sayılmıyor; yalnız altısı adlandırılıyor.
- 0:12-0:19 arası (NotebookLM benzeri not defteri, Reddit, Postman, fiyat tablosu) kareler gönderilmediği için yalnız OCR'a dayanıyor; bağlamı belirsiz, aday yapılmadı.
- Ekrandaki 81.4k yıldız ve 'agent-reach 0.1.0' OCR/kare okumasıdır, doğrulanamadı.
- Voicebox ve Codex CLI görüntüleri agent-reach dışı örnek/kurgu olabilir; videoda kullanıldıkları söylenmiyor.
- Kurulum URL'si OCR'da 'archivel' diye bozuk; 'archive/main.zip' olarak varsayıldı.
- EKSİK: rapor (süre dışı zaman: 10:23 > 0:27)
- EKSİK: rapor (süre dışı zaman: 10:23 > 0:27)
- EKSİK: rapor (süre dışı zaman: 10:23 > 0:27)
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://github.com/Panniantong/agent-reach/archivel | 0:09 | ekran | evet |
| https://github.com/Panniantong/agent-reach/archive/main.zip | 0:10 | ekran | evet |
| http://127.0.0.1:17493/mcp | 0:23 | ekran | evet |
| http://127.0.0.1:17493 | 0:23 | ekran | evet |
| http://127.0.0.1:17493/generate | 0:23 | ekran | evet |
| http://127.0.0.1:17493/speak | 0:23 | ekran | evet |
| http://127.0.0.1:17493/transcribe | 0:23 | ekran | evet |
| http://127.0.0.1:17493/profiles | 0:23 | ekran | evet |
## İş akışı
- 1. adım — Açık kaynak agent-reach GitHub deposunu tanıtma — araçlar: GitHub, agent-reach
- 2. adım — Claude Code oturumunda hatırlatıcı (CronCreate) örneği gösterme — araçlar: Claude Code, Visual Studio Code
- 3. adım — Aracı terminalde pipx ile kurma — araçlar: pipx, agent-reach
- 4. adım — Kurulum sihirbazını ortam otomatik algılama ile çalıştırma — araçlar: agent-reach
- 5. adım — Erişim örneklerini gösterme (Reddit, Postman, fiyat sayfası) — araçlar: agent-reach
- 6. adım — Bot engeli konusunu Codex CLI görev kaydıyla örnekleme — araçlar: Codex CLI
- 7. adım — Voicebox MCP kurulum örneğini gösterme — araçlar: Voicebox, Claude Code
- 8. adım — Yorumda 'search' yazana repoyu gönderme çağrısı yapma — araçlar: Instagram
## Promptlar
- Codex CLI'ye bir GitHub issue'sunu çözdürme (bağlam örneği) — Filename'de özel karakter olunca 'diff' komutunun hata verdiği bir GitHub issue'sunu çözmesi isteniyor. Sorunu yeniden üretmek için geçici bir git reposu ve 'a$b.txt' gibi bir dosya kullanılıyor, Codex CLI'nin bilgi istediği alanlar (sürüm, model, platform, adımlar) doldurulmuş.
- Codex'e sandbox içi test adımlarını yaptırma — Sandbox içinde ilk komut olarak bir ASCII kedi çıktısı yazdırılması, ardından geçici bir git reposu oluşturulup 'a$b.txt' adlı dosyayla hatanın tekrar üretilmesi isteniyor.
- Kaynaklara dayalı özet/brifing istemi (bağlam) — Gen AI stratejisi için temel konuları, verilen kaynaklara dayanarak özetleyen bir istem (Google NotebookLM benzeri arayüz).
