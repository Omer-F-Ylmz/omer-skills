# 32 Tricks to Level Up Claude Code in 16 Mins
## Künye
32 Tricks to Level Up Claude Code in 16 Mins · Nate Herk | AI Automation · süre: 16:15 · en-orig · https://youtu.be/jqoFP9QapXI
motor: parti 2026-09-30-uzun-7 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (6)
## Özet
Nate Herk, Claude Code için 32 ipucunu başlangıç, orta ve ileri seviye olarak anlatıyor. Başlangıç: /init, status line, sesli giriş, küçük bağlam, /context, /compact ve /clear, plan modu, soru sorturma, kendini kontrol eden to-do listeleri. Orta seviye: alt ajanlar, özel skill'ler, Haiku kullanımı, CLAUDE.md bakımı ve yönlendirme, erken durdurma, /rewind, hook bildirimleri, ekran görüntüsü döngüsü, Chrome DevTools, site klonlama. İleri seviye: git worktree, MCP yerine API, /loop, VPS, uzaktan kontrol, BigQuery ile SQL'siz analiz, ultrathink, izin yönetimi, agent teams ve Context7 MCP.
## Bölümler
- 0:00 Giriş
- 0:14 Başlangıç ipuçları
- 4:53 Orta seviye ipuçları
- 10:29 İleri seviye ipuçları
- 15:53 Son düşünceler
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| /init | yok | ipucu | yok | Mevcut projeyi tarayıp mimari, kurallar ve önemli dosyaları içeren CLAUDE.md üretir. | 0:14 | Kare: terminalde claude, /init ve 'Scanning project...' görünüyor; anlatımda da aynı. (karede: Terminalde '$ claude', '> /init', 'Scanning project...' ve altyazı 'Works for new projects too'.) |
| Status line (/statusline) | yok | ipucu | yok | Terminalin altında model, bağlam yüzdesi, maliyet gösteren script oluşturur. | 0:44 | Type slash status line and tell Cloudcode what you want to see. |
| /voice | yok | ipucu | yok | Yerel sesli komut; henüz herkese açılmadı. Alternatif olarak her yerde dikte uygulaması (Glaido) öneriliyor. | 1:14 | Cloudcode just shipped a native slash voice command |
| /context | yok | ipucu | yok | Token tüketimini (sistem istemi, dosyalar, MCP) yüzdelerle gösterir. | 1:14 | do slash context, you'll see exactly what's eating your tokens |
| /compact ve /clear | yok | ipucu | yok | Bağlam ~%60'a gelince kısıtlı tutarak sıkıştır; görev değişince temizle. | 2:16 | when your context hits around 60%, then type slash compact |
| Plan modu (Shift+Tab) | yok | ipucu | yok | Kod yazmadan önce araştırır, soru sorar ve plan çıkarır. | 2:16 | you can hit shift tab to cycle between modes |
| Ask user question ile %95 emin olma | yok | prompt | yok | Claude'a %95 emin olana kadar soru sordurur. | 3:16 | Kare: plan modunda Claude seçenekler sunuyor, kullanıcı istemi görünüyor. (karede: Kullanıcı istemi: 'I want to build a real-time notification system for our app. Before you start coding, ask me questions until you're 95% confident...'; altta 'Plan mode'.) |
| Doğrulama adımlı to-do listesi | yok | iş akışı | yok | To-do'lara ekran görüntüsü ve DevTools kontrolü ekleyerek kendi kendini doğrulatır. | 4:18 | Don't move on to your next to-do until you're 95% confident |
| Alt ajanlar | yok | teknik | yok | İzole bağlamlı paralel ajanlar; ana oturum temiz kalır. | 4:53 | Cloud will spin up isolated sub-agents that each have their own context window. |
| Özel skill'ler (.claude/skills) | yok | skill | yok | techdebt, codereview gibi yeniden kullanılabilir iş akışları; GitHub ile paylaşılabilir. | 4:53 | create reusable prompt files in your .cloud/skills directory |
| Alt ajanlarda Haiku | yok | teknik | yok | Basit/yoğun okuma işlerinde ucuz model, ana ajan Opus. | 5:54 | when you have simple tasks or processing a large amount of data, then use Haiku |
| CLAUDE.md bakımı ve yönlendirme | yok | ipucu | yok | 150-200 satırda tut, detayları ayrı dosyalara yönlendir. | 6:54 | I like to keep it between 150 and 200 lines max. |
| /rewind | yok | ipucu | yok | Konuşmayı önceki noktaya geri alır. | 7:57 | just try using slash rewind and Cloud will roll back |
| /hooks bildirimi | yok | ipucu | yok | Oturum bitince ses bildirimi. | 7:57 | if you type slash hooks, you can set up a notification hook |
| Ekran görüntüsü döngüsü | yok | iş akışı | yok | Tasarla, ekran görüntüsü al, düzelt; V1 öncesi ~3 tur. | 8:59 | it does like three passes of building and screenshots before it even gives me V1 |
| Chrome DevTools | yok | MCP | yok | Tarayıcıyı açıp uygulama işlevselliğini test eder. | 8:59 | Hack number 21 is to use Chrome DevTools. |
| Git worktree | yok | CLI | yok | Her özellik için izole dal/çalışma alanıyla paralel oturumlar. | 10:29 | You just type in Claude dash work tree and then that feature name. |
| /loop | yok | ipucu | yok | Tekrarlayan görevleri oturumda çalıştırır; 3 gün sınırı. | 11:29 | these actual loops will only last for 3 days |
| VPS ile sürekli açık oturum | yok | iş akışı | yok | Uzak sunucuda çalıştır, SSH/Telegram ile eriş. | 12:30 | run Claude code on a remote server, it'll stay running even when your laptop is closed |
| Remote control | yok | ipucu | yok | Yerel oturumu telefondan veya tarayıcıdan yönetme. | 12:30 | control local sessions from your phone or any browser |
| BigQuery bq CLI ile SQL'siz analiz | yok | CLI | yok | Doğal dille sorgu, Claude SQL üretip çalıştırır. | 12:30 | connect CLI tools like BigQuery's BQ tool to Claude code |
| ultrathink | yok | prompt | yok | Zor problemler için maksimum düşünme bütçesi (~32.000 token). | 13:31 | allocates the maximum thinking budget of around 32,000 tokens |
| İzin yönetimi (allow/deny) | yok | teknik | yok | Güvenli komutlara izin, yıkıcı olanlara yasak; deny önceliklidir. | 13:31 | anything in the deny list is going to take priority over anything in the allow list |
| Agent teams | yok | teknik | yok | Birbirleriyle konuşan, ortak görev listesi olan ajanlar. | 14:32 | they share a task list, they can communicate with each other |
| Context7 MCP | yok | MCP | yok | Güncel, sürüme özel kütüphane dokümantasyonunu bağlama enjekte eder. | 14:32 | install the Context 7 MCP server and then whenever you need information on current documentation |
| Claude'a netleştirici sorular sordurmak | yok | prompt | yok | Continuously ask me questions until you're 95% confident that you understand exactly what I need | 3:16 | kaynak: altyazı |
| Kodlamadan önce soru sordurma örneği | yok | prompt | yok | I want to build a real-time notification system for our app. Before you start coding, ask me questions until you're 95% confident you understand exactly what I need. Don't make any assumptions. | 3:47 | kaynak: kare |
| Seçili bilgileri koruyarak sıkıştırma | yok | prompt | yok | /compact but keep all of the API integration decisions and database schema | 2:16 | kaynak: altyazı |
| Çıktıya itiraz edip daha iyisini istemek | yok | prompt | yok | Scrap that. Do a more elegant version. | 7:57 | kaynak: altyazı |
## Açıklama bağlantıları
- https://get.glaido.com/nate — Glaido sesli dikte uygulaması (sponsor/ortaklık bağlantısı) · aday: evet (/voice) · Videoda 'voice tate anywhere' aracı olarak işaret ediliyor.
- https://podcast.nateherk.com/apply — Podcast başvuru sayfası · aday: hayır · Araç değil, konuk başvurusu.
- https://www.hostinger.com/vps/claude-code-hosting — Hostinger VPS barındırma sayfası · aday: evet (VPS ile sürekli açık oturum) · VPS ile sürekli açık oturum ipucuyla ilgili.
- https://www.instagram.com/nateherk/ — Instagram profili · aday: hayır · Sosyal medya, araç değil.
- https://www.linkedin.com/in/nateherkelman/ — LinkedIn profili · aday: hayır · Sosyal medya, araç değil.
- https://www.skool.com/ai-automation-society-plus/about?el=32-hacks&hcategory=youtube-videos&utm_campaign=ais-plus — Ücretli Skool topluluğu · aday: hayır · Ücretli topluluk, içerik erişilemez. · erişilemez: ücretli topluluk
- https://www.skool.com/ai-automation-society/about?el=32-hacks&hcategory=youtube-videos&utm_campaign=free-group — Ücretsiz Skool topluluğu; PDF rehber burada · aday: hayır · Giriş gerektiren topluluk; PDF rehbere erişilemedi. · erişilemez: giriş gerekli
- https://x.com/nateherk — X profili · aday: hayır · Sosyal medya, araç değil.
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bağlam yaklaşık %60'a gelince /compact kullanılmalı. | 2:16 | sayısal |
| CLAUDE.md 150-200 satırı geçmemeli; her konuşmaya yüklenir. | 6:54 | sayısal |
| ultrathink yaklaşık 32.000 token düşünme bütçesi ayırır. | 13:31 | sayısal |
| /loop döngüleri 3 gün sürer. | 11:29 | sayısal |
| MCP sunucuları tüm araç tanımlarını bağlama yükler; token kıtsa doğrudan API daha iyi olabilir. | 11:29 | karşılaştırma |
| İzin listesi + deny listesi, dangerously skip permissions ile aynı hız ve özerkliği daha güvenli sağlar. | 13:31 | karşılaştırma |
| Agent teams daha pahalı ve uzun sürer ama daha tutarlı çıktı verir. | 14:32 | karşılaştırma |
## Kareden okunanlar
- 4:35 (kare 6, görsel sırası): Kare Beginner/Intermediate/Advanced/Power User ilerleme çubuğu, Beginner seçili; RØDE mikrofon.
- görsel: /init terminali: '$ claude', '> /init', 'Scanning project...', 'Works for new projects too'.
- görsel: odaklı istem: 'The login function in src/routes/auth.ts returns a 401 even with valid credentials... Fix the token validation on line 42.' (focused-prompt.txt, yeşil onay).
- görsel: boş Claude Code paneli: 'Use Claude Code in the terminal to configure MCP servers', 'Bypass permissions', 'CLAUDE.md'.
- görsel: plan modu oturumu: ls -la komutu, prompt.txt okuma, iki seçenekli soru ve %95 emin olma istemi; 'Plan mode'.
- görsel: boş kuyruk: Yalnızca 'Queue another message...' giriş alanı.
## Belirsizlikler
- Kareler 6 görsel; zaman damgaları (0:07, 0:44, 1:45, 2:46, 3:47, 4:35) ile eşleşmesi tahmini. Yalnızca 0:07 ve 4:35 kareleri, sırayla ilk ve son görsel varsayıldı.
- 'Hack 28' iki kez numaralanıyor (SQL'siz analitik ve ultrathink); Context7 altyazıda 'up to eight' olarak geçiyor, muhtemelen 'up-to-date'.
- Altyazı 'Cloud' yazıyor ama Claude kastediliyor; 'cloud.md' CLAUDE.md demektir.
- /voice, remote control ve agent teams'in kullanılabilirliği videoya göre; güncel durum doğrulanmadı.
- Kurulum komutları: videoda açık kurulum komutu söylenmedi; Context7 için 'one command to install' deniyor ama komut gösterilmedi.
## Atlanan segment oranı
0/19 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
