# 9 NEW Claude Mods that can truly change how you work
## Künye
9 NEW Claude Mods that can truly change how you work · Jay E | RoboNuggets · süre: 12:47 · en-orig · https://youtu.be/lDrAZ1wAyVs · şema 2
motor: parti 2026-10-10-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 60700 tk · claude-haiku-5-5: claude-haiku-5-5 · 112483 tk
## Özet
Jay (RoboNuggets), Anthropic'in Claude Code'a getirdiği 'mods' özelliğini anlatıyor: Claude Code içinde çalışan, arayüzü ve davranışı değiştiren küçük eklentiler. Skill ve MCP bağlayıcılarından farkı açıklanıyor, ardından dokuz mod tanıtılıyor: Savvy Progress, Claude Skins, You Should Know, File Tree, Cache Tax, Blast Radius, Reflect, Terminal Browser ve Replay Theater. Sonda kendi modunu yapma adımları (claude update, plugin-authoring skill'i, hot reload, plugin olarak kaydetme) ve maliyet bilgisi veriliyor.
## Bölümler
- 0:00 Giriş
- 0:39 Mod nedir
- 2:02 Mod 1: Savvy Progress
- 3:02 Bir mod nasıl çalışır
- 3:57 Mod 2: Claude Skins
- 4:34 Mod 3: You Should Know
- 6:05 Mod 4: File Tree
- 7:04 Mod 5: Cache Tax
- 8:15 Mod 6: Blast Radius
- 9:04 Mod 7: Reflect
- 9:39 Mod 8: Terminal Browser
- 10:09 Mod 9: Replay Theater
- 10:43 Kendi modunu yap
- 11:56 Kapanış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Modların çalıştığı Anthropic'in kodlama ajanı; terminal ve masaüstü kod sekmesi | 0:00 | Cloud Code can become almost any tool that you need. |
| Claude mods | yok | plugin | yok | Claude Code arayüzünü ve davranışını değiştiren küçük eklentiler; olayları izler, değiştirir veya kendisi işler | 0:39 | a mod is just a small add-on that basically changes how cloud code looks |
| Savvy Progress | yok | plugin | https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-progress | Prompt üstünde ilerleme çubuğu ve alt ajanlar için canlı panel (model, ilerleme, maliyet) | 2:02 | Number one is Savvy Progress. |
| Claude Skins | yok | plugin | https://github.com/hellosverre/claude-skins | Claude Code çıktısını yeniden temalandırır; araç ikonları, renkler, yedi tema | 3:57 | Number two is Claude skins. |
| You Should Know | yok | plugin | yok | İkinci bir ajanla Claude çıktısını okuyup önemli noktaları açılır uyarıyla öne çıkarır | 4:34 | Number three is you should know. |
| File Tree | yok | plugin | https://github.com/data-goblin/claude-code-filetree | Sağda dosya paneli; Claude'un okuduğu/düzenlediği dosyaları gösterir, token harcamaz | 6:05 | Number four is File Tree. |
| Cache Tax | yok | plugin | https://github.com/karanb192/cache-tax | Prompt cache soğuduğunda mesajı durdurup maliyet tahmini gösterir; /keepwarm ile cache'i sıcak tutar | 7:04 | Number five is cash tax. |
| Blast Radius | yok | plugin | https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/blast-radius | Riskli silme komutlarından önce silinecek dosyaları gösterip onay ister | 8:15 | Number six is blast radius. |
| Reflect | yok | plugin | https://github.com/BayramAnnakov/claude-reflect | Düzeltici geri bildirimi CLAUDE.md'ye kalıcı kural olarak kaydetmeyi önerir | 9:04 | Number seven is reflect. |
| Terminal Browser | yok | plugin | https://github.com/zenbu-labs/terminal-browser | Terminalde sohbetin yanında gerçek tarayıcı açar; PR ve web sayfaları incelenir | 9:39 | Number eight is the terminal browser. |
| Replay Theater | yok | plugin | https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/replay-theater | Tur sonunda Claude'un yaptığı dosya düzenlemelerini adım adım yeniden oynatır | 10:09 | Replay Theater. Now, this last one is another of Entropic's own sample mods |
| plugin-authoring | yok | skill | yok | Claude Code'un yerleşik skill'i; mod yazmayı bilir ve mod oluşturur | 10:43 | It's called plug-in authoring. |
| Hot reloading | yok | teknik | yok | Mod inşa edildiği anda oturumda görünmesi için oturumu yeniden yükleme | 10:43 | turn on hot reloading for this session |
| Prompt cache | yok | teknik | yok | Konuşma boyunca tutulan kısa süreli önbellek; soğuyunca tüm konuşma yeniden okunur | 7:04 | if you don't know what the prompt cache is |
| Opus 5.5 | yok | CLI | yok | Ekranda görünen, Claude Code oturumlarında kullanılan ana model | 0:06 | Alt çubukta Opus 5.5 Extra high görünüyor. (karede: kanıttan) Alt çubukta Opus 5.5 Extra high görünüyor. |
| Kling 3.0 | yok | MCP | yok | Video üretimi için model; You Should Know demosunda maliyet uyarısı | 4:42 | I set up the cold brew video with Kling 3.0 (karede: kanıttan) I set up the cold brew video with Kling 3.0 |
| Kie AI | yok | CLI | yok | Kling'i çalıştıran sağlayıcı; klip başı yaklaşık 90 kredi | 4:42 | through Kie AI, about 90 credits per clip (karede: kanıttan) through Kie AI, about 90 credits per clip |
| Claude desktop app | yok | CLI | yok | Kod sekmesinde modların çalıştığı masaüstü uygulaması | 0:39 | in the code tab of the desktop app · kanıt: yok |
| /plugin | yok | CLI | yok | Modları içeren pluginleri kurmak için Claude Code komutu | 0:40 | Mods ship inside plugins, so you install them with /plugin (karede: kanıttan) Mods ship inside plugins, so you install them with /plugin |
| RoboNuggets community | yok | iş akışı | yok | Jay'in Skool topluluğu (sponsor/kendi reklamı) | 5:24 | Powered by skool (karede: kanıttan) Powered by skool |
| Claude Sonnet 5.5 | yok | teknik | yok | Kare 9:54'te model etiketi olarak görünen Claude modeli. | 9:54 | Sonnet 5.5 · kanıt: kare (karede: Ekranda 'Sonnet 5.5' model etiketi görünüyor; yanında yeniden adlandırma sonucu metni var.) |
| Claude Fable | yok | teknik | yok | Konuşmada ve ekranda geçen Claude model adı; 'Fable 5.1 with high effort' olarak terminalde görünür. | 8:15 | even Opus or Fable would wipe out someone's entire project |
| npm | yok | CLI | yok | Node paket yöneticisi; Claude 'npm install dayjs' ve 'npm test' komutlarını çalıştırdı. | 8:54 | Ran 2 shell commands $ npm install dayjs (karede: Sohbette 'Ran 2 shell commands $ npm install dayjs' ve 'I installed dayjs with npm' yazıyor.) |
| pnpm | yok | CLI | yok | Bu projede kullanılması kuralı kaydedilen paket yöneticisi; 'pnpm test --filter hub' komutu da çalıştırılıyor. | 9:06 | Use pnpm instead of npm for package management in this project. (karede: 'Save this as a rule?' kartında 'Use pnpm instead of npm for package management in this project.' yazıyor.) |
| Git | yok | CLI | yok | Claude 'git commit -am' ile iki dosyayı commit etti; dosyalar commit sonrası yeşile döner. | 6:16 | $ git commit -am 'Raise MAX_RETRIES to 3' (karede: Sohbette '$ git commit -am "Raise MAX_RETRIES to 3"' ve 'Claude committed 2 files' yazıyor.) |
| Modları PDF rehberinden kişiye göre seçtirmek | yok | prompt | yok | Ekli 9 Claude Mods PDF rehberini oku, kurulumumu kontrol et ve hangi modların bana uyduğunu söyle. | 1:46 | kaynak: kare |
| Kendi modunu oluşturma | yok | prompt | yok | Claude Code için bir mod yap: ürettiğin her dosya ve sayfayı sohbet kutusunun üstünde küçük baloncuk olarak göster. | 10:48 | kaynak: kare |
| Claude Skins için özel tema üretmek | yok | prompt | yok | Bu renk paletinden bir skin yap. | 4:18 | kaynak: kare |
## Açıklama bağlantıları
- https://www.skool.com/robonuggets-free/classroom/750914f0?md=a2e607329db2457f83744f817b9d8610 — Ücretsiz 9 Claude Mods PDF rehberi (Skool) · aday: hayır · Kanal kendi rehber/topluluk içeriği; izleyicinin kullanacağı araç değil · sınıf: diğer · erişilemez: Skool topluluğu, giriş gerekli
- https://www.skool.com/robonuggets — RoboNuggets ücretli topluluğu · aday: hayır · Kanalın kendi topluluk reklamı · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- https://www.getrubric.app/ — Rubric uygulaması · aday: hayır · Videoda kullanılmıyor/anlatılmıyor · sınıf: diğer
- https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-progress — Savvy Progress modu deposu · aday: evet (Savvy Progress) · Videoda anlatılan mod 1 · sınıf: diğer
- https://github.com/hellosverre/claude-skins — Claude Skins deposu · aday: evet (Claude Skins) · Videoda anlatılan mod 2 · sınıf: diğer
- https://github.com/data-goblin/claude-code-filetree — File Tree modu deposu · aday: evet (File Tree) · Videoda anlatılan mod 4 · sınıf: diğer
- https://github.com/karanb192/cache-tax — Cache Tax modu deposu · aday: evet (Cache Tax) · Videoda anlatılan mod 5 · sınıf: diğer
- https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/blast-radius — Blast Radius modu · aday: evet (Blast Radius) · Videoda anlatılan mod 6 · sınıf: diğer
- https://github.com/BayramAnnakov/claude-reflect — Reflect modu deposu · aday: evet (Reflect) · Videoda anlatılan mod 7 · sınıf: diğer
- https://github.com/zenbu-labs/terminal-browser — Terminal Browser deposu · aday: evet (Terminal Browser) · Videoda anlatılan mod 8 · sınıf: diğer
- https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/replay-theater — Replay Theater modu · aday: evet (Replay Theater) · Videoda anlatılan mod 9 · sınıf: diğer
- https://blotato.com/?ref=robonuggets — Blotato · aday: hayır · Yönlendirme parametreli ortak araç; videoda kullanılmıyor · sınıf: affiliate
- https://n8n.partnerlinks.io/o3jqtj032c02 — n8n ortaklık bağlantısı · aday: hayır · Videoda kullanılmıyor, affiliate reklam · sınıf: affiliate
- https://www.make.com/en/register?pc=robonuggets — Make kayıt bağlantısı · aday: hayır · Videoda kullanılmıyor, affiliate · sınıf: affiliate
- https://try.elevenlabs.io/m5mn2jkv5rzk — ElevenLabs · aday: hayır · Videoda kullanılmıyor, affiliate · sınıf: affiliate
- https://www.apify.com?fpr=sffv1 — Apify · aday: hayır · Videoda kullanılmıyor, affiliate · sınıf: affiliate
- https://www.youtube.com/@RoboNuggets — Kanal sayfası · aday: hayır · Sosyal profil · sınıf: diğer
- https://www.instagram.com/robonuggets — Instagram · aday: hayır · Sosyal profil · sınıf: diğer
- https://www.tiktok.com/@robonuggets — TikTok · aday: hayır · Sosyal profil · sınıf: diğer
- https://www.twitter.com/robonuggets — Twitter · aday: hayır · Sosyal profil · sınıf: diğer
- https://www.linkedin.com/in/j-enri/ — LinkedIn · aday: hayır · Sosyal profil · sınıf: diğer
- https://robolabs.so — RoboLabs ajans sitesi · aday: hayır · Jay'in ajans/referans sitesi · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| İlerleme çubuğu (progress bar) | Prompt üstünde görev ilerleme çubuğu | 2:02 | altyazı |
| Yan panel (side panel) ve kart düzeni (card layout) | Sağ yan panelde alt-ajan kartları ve maliyet özeti (karede: Sağda 'Agents' paneli; 'Launch kit' başlığı altında Cost, Tokens ve Time kartları ve her alt-ajan için renkli ilerleme çubukları var.) | 2:36 | kare |
| Titreşim animasyonu (shimmer animation) ve durum etiketleri | Okunan dosyanın panelde titreşerek vurgulanması (karede: Sağda 'Files: weather-app' paneli; 'Claude is reading client.test.js' ve 'Claude touched 1 file' kartları görünüyor.) | 6:04 | kare |
| Tema kaplaması (theming with CSS custom properties) | Tema seçici ile araç satırlarının yeniden renklendirilmesi (karede: 'Pick one to recolour tool rows, cards and rings.' yazısı ve Noir, Tokyo Night, Dracula, Catppuccin tema kartları görünüyor.) | 4:08 | kare |
| Modal onay penceresi (modal confirmation dialog) | Riskli silme öncesi onay penceresi (karede: 'Delete 9 files' ve 'Cancel' düğmeleri ve 'Held by Blast Radius' etiketi görünüyor.) | 8:12 | kare |
| Ayrılmış panel (docked pane) ve iç içe görünüm | Terminalin yanında açılan gömülü tarayıcı paneli (karede: Claude Code terminalinin yanında açılan 'terminal-browser://start' paneli; PR, çalışan sunucu ve son belgeler listesi var.) | 9:30 | kare |
| Adım adım gezinme (step-through navigation) ve düzenleme listesi | Düzenlemeleri adım adım gösteren oynatma kartı (karede: 'Replay Theater: 4 edits ready to replay' kartı ve 'Replay edits' düğmesi görünüyor.) | 10:08 | kare |
| Kabarcık düzeni (bubble / floating indicator) | Modun yeni dosyaları balon/liste olarak göstermesi (karede: Yan panelde '3 artifacts, newest first' listesi ve 'ARTIFACT RING' başlığı var.) | 11:06 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /plugin enable cc-plugin-you-should-know@builtin | Yerleşik You Should Know pluginini etkinleştirir (karede: Tweet görselinde 'Enable it with: /plugin enable cc-plugin-you-should-know@builtin') | 4:32 | kare |
| claude update | Claude Code'u en son sürüme günceller (karede: Ekran metni 'just type claude update'; güncelleme penceresi görünüyor) | 10:36 | kare |
| /keepwarm | Cache Tax ile prompt cache'i sıcak tutar (karede: '/keepwarm Keep the prompt cache warm: bare for 6h, a window such as 90m, always, off') | 7:42 | kare |
| /replay | Replay Theater ile düzenlemeleri adım adım oynatır (karede: 'Replay edits or type /replay') | 10:18 | kare |
| /browser | Terminal Browser'ı sohbetin yanında açar (karede: Terminalde '/browser terminal-browser: Opened terminal-browser') | 9:30 | kare |
| /savvy-flow:savvy-flow | Savvy Progress ile çoklu ajan lansman kiti akışını başlatır (karede: Sohbette '/savvy-flow:savvy-flow Build the launch kit for our new cold brew') | 2:08 | kare |
| rm -rf build | Blast Radius'un engellediği riskli silme komutu (karede: 'rm -rf build will delete 9 files · 286 KB') | 8:10 | kare |
| npm install dayjs | dayjs paketini npm ile kurar (Reflect demosu) (karede: 'Ran 2 shell commands $ npm install dayjs') | 8:58 | kare |
| /plugin install skins@hellosverre-mods | Claude Skins temalarını kurar. (Komut küçük kare metninden okundu; belirsizlikler bölümüne bakın.) (karede: Tema ekranının altında '/plugin install skins@hellosverre-mods' yazısı görünüyor.) | 3:58 | kare |
| /savvy-flow:savvy-flow Build the launch kit for our new cold brew: research competitor launches, ... | Savvy Progress planını başlatır; görevi dört adıma böler ve üç alt-ajan başlatır. (karede: Sohbette '/savvy-flow:savvy-flow Build the launch kit for our new cold brew: research' komutu yazıyor.) | 2:08 | kare |
| /clear | Terminal oturumundaki konuşmayı temizler. (karede: Terminalde '/clear' komutu yazılı.) | 9:34 | kare |
| npm test | Projenin test paketini çalıştırır. (karede: Sohbette 'Running 1 shell command... $ npm test' yazıyor.) | 1:28 | kare |
| pnpm test -filter hub | pnpm ile hub uygulamasının testlerini çalıştırır. (Ekran metni 'pnpm test -filter hub' olarak okundu; '--filter' olabilir.) (karede: Sohbette 'Bash pnpm test -filter hub' yazıyor.) | 3:54 | kare |
| git commit -am "Raise MAX_RETRIES to 3" | İzlenen değişiklikleri mesajla birlikte commit eder. (karede: Sohbette '$ git commit -am "Raise MAX_RETRIES to 3"' ve 'Claude committed 2 files' yazıyor.) | 6:16 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Mods 1 Ekim'de çıktı; güncel Claude Code'da açık, terminalde ve masaüstü kod sekmesinde çalışıyor, VS Code'da henüz yok. | 0:39 | özellik |
| Mod için Claude Code sürümü 2.1.287 veya daha yeni olmalı. | 10:43 | sayısal |
| Skill işi nasıl yapacağını anlatır, bağlayıcı uygulamaya bağlar; mod ise Claude Code'un içinde çalışıp onu değiştirir. | 0:39 | karşılaştırma |
| Mod üç şey yapabilir: olayı izler, değiştirir veya kendisi işler; Savvy Progress üçünü de kullanır. | 3:02 | özellik |
| You Should Know ikinci bir ajan çalıştırdığı için token kullanımını artırabilir; çoğu mod deterministik koddur. | 5:14 | karşılaştırma |
| Cache yaklaşık bir saatte soğur; soğuyunca sonraki mesaj tüm konuşmayı yeniden okutur. | 7:04 | sayısal |
| Cache Tax kartı soğuk cache'te gönderme maliyetini 0,52 $, sıcak turu 0,03 $ gösteriyor. | 7:22 | sayısal |
| Modlar varsayılan olarak ek ücret yok; ücretli plan gerekir, arka planda model çağıran modlar kullanım hakkından düşer. | 11:30 | özellik |
| Claude'un yazdığı mod geçicidir; kalıcı olması için plugin olarak kaydedip kurmasını istemek gerekir. | 10:43 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Anthropic (Entropic) | aday değil: genel kavram | Entropic just shipped one of the biggest Cloud Code updates |
| konuşma 0:00 | Claude Code | Claude Code | Cloud Code can become almost any tool |
| konuşma 0:39 | Mods | Claude mods | a mod is just a small add-on |
| konuşma 0:39 | Skills | aday değil: genel kavram | a skill basically just tells Claude how to do a job |
| konuşma 0:39 | MCP connectors | aday değil: genel kavram | a connector just plugs Claude into another application |
| konuşma 0:39 | VS Code uzantısı | aday değil: konu dışı | doesn't seem to be available yet in the VS Code extension |
| konuşma 2:02 | Savvy Progress | Savvy Progress | Number one is Savvy Progress. |
| konuşma 2:02 | Alt ajanlar | aday değil: genel kavram | sub agents are basically these helper claws |
| konuşma 3:02 | Olay (event) sistemi | Claude mods | a little signal called an event |
| konuşma 3:02 | Yerleşik mod skill'i | plugin-authoring | built-in skill now for building them |
| konuşma 3:57 | Claude Skins | Claude Skins | Number two is Claude skins. |
| kare 3:54 | Noir, Tokyo Night, Dracula, Catppuccin, Sunset temaları | Claude Skins | Skins paneli kartları |
| konuşma 4:34 | You Should Know | You Should Know | Number three is you should know. |
| konuşma 4:34 | Kling | Kling 3.0 | generate a video with a model like Cling |
| konuşma 4:34 | Kie AI | Kie AI | if I ran it through key AI |
| konuşma 5:34 | RoboNuggets topluluğu / Claude Living Masterclass | aday değil: sponsor/reklam | RoboNuggets community |
| konuşma 6:05 | File Tree | File Tree | Number four is File Tree. |
| konuşma 6:05 | Git commit | aday değil: başka adayın parçası (File Tree) | when the change is committed... it turns green |
| konuşma 7:04 | Cash Tax | Cache Tax | Number five is cash tax. |
| konuşma 7:04 | Prompt cache | Prompt cache | what the prompt cache is |
| konuşma 7:04 | /keepwarm | Cache Tax | you can type /keepwarm |
| konuşma 8:15 | Blast Radius | Blast Radius | Number six is blast radius. |
| konuşma 8:15 | Opus ve Fable modelleri | aday değil: konu dışı | even Opus or Fable would wipe out someone's entire project |
| konuşma 9:04 | Reflect | Reflect | Number seven is reflect. |
| konuşma 9:04 | RLHF | aday değil: genel kavram | bit like reinforcement learning from human feedback |
| konuşma 9:04 | CLAUDE.md | Reflect | permanent rule in your claw.md file |
| konuşma 9:39 | Terminal Browser | Terminal Browser | Number eight is the terminal browser. |
| konuşma 9:39 | GitHub pull request | aday değil: başka adayın parçası (Terminal Browser) | it can also open GitHub pull requests |
| konuşma 10:09 | Replay Theater | Replay Theater | Number nine is Replay Theater. |
| konuşma 10:43 | claude update | Claude Code | you can just type cloud update |
| konuşma 10:43 | plugin authoring skill | plugin-authoring | It's called plug-in authoring. |
| konuşma 10:43 | Hot reloading | Hot reloading | turn on hot reloading for this session |
| konuşma 11:56 | OpenAI | aday değil: konu dışı | I hope OpenAI follows suit |
| kare 0:06 | Opus 5.5 | Opus 5.5 | Alt çubuk 'Opus 5.5 Extra high' |
| kare 0:28 | Dünya haritası/Skool topluluk haritası | aday değil: sponsor/reklam | RoboNuggets topluluk haritası |
| kare 0:30 | UTS Master of Data Science | aday değil: konu dışı | University of Technology Sydney |
| kare 0:32 | RoboLabs sitesi | aday değil: sponsor/reklam | ROBOLABS Services Process Solutions |
| kare 0:40 | @ClaudeDevs tweeti | Claude mods | You can now mod Claude Code |
| kare 1:24 | npm test | aday değil: başka adayın parçası (File Tree) | Running 1 shell command $ npm test |
| kare 3:54 | pnpm | aday değil: başka adayın parçası (Claude Skins) | Bash pnpm test -filter hub |
| kare 6:00 | claude-code-filetree demo | File Tree | data-goblin/claude-code-filetree |
| kare 9:30 | zenbu-labs/terminal-browser PR #113 | Terminal Browser | github.com/zenbu-labs/terminal-browser/pull/113 |
| kare 9:54 | Sonnet 5.5 | aday değil: konu dışı | Replay Theater tweet görseli içinde model adı |
| açıklama | n8n, Make, ElevenLabs, Apify, Blotato | aday değil: sponsor/reklam | Açıklamada AI Partner Tools affiliate bağlantıları |
| açıklama | getrubric.app | aday değil: konu dışı | Videoda geçmiyor |
| açıklama | Kanal sosyal profilleri | aday değil: konu dışı | YouTube, Instagram, TikTok, Twitter, LinkedIn |
| açıklama | You Should Know yerleşik kurulumu | You Should Know | /plugin enable cc-plugin-you-should-know@builtin |
| yorum | DeepSeek harness, Agent Zero, Codex, ChatGPT | aday değil: konu dışı | İzleyici yorumları karşılaştırma yapıyor |
| yorum | Claudixum | aday değil: konu dışı | Bot spam yorumları |
## Kareden okunanlar
- 0:40: @ClaudeDevs tweeti: 'You can now mod Claude Code' – davranışı değiştir, arayüzü özelleştir, kendi özelliklerini ekle; pluginlerle gelir, /plugin ile kurulur.
- 4:32: Komut: /plugin enable cc-plugin-you-should-know@builtin; 'Built by Anthropic'
- 7:22: Cache Tax kartı: 'Your message is on hold', 0,52 $ ve 0,03 $; Pay and send / Start fresh
- 8:12: Blast Radius: 'Delete 9 files' ve 'Cancel' düğmeleri; rm -rf build 9 dosya
- 9:06: Reflect: 'Save this as a rule?' - pnpm kuralı, CLAUDE.md'ye kaydet
- 9:30: Terminal Browser: /browser komutu, Claude Code v2.1.274, PR #113 GitHub sayfası
- 10:18: Replay Theater: '3 edits ready to replay', Replay edits düğmesi
## Belirsizlikler
- Açıklama bağlantılarındaki 'sinif' alanı şemada yok; affiliate/sponsor ayrımı neden alanında belirtildi.
- Savvy Progress deposu claude-kit içinde; ekranda komut adı 'savvy-flow' geçiyor, ad ilişkisi kesin değil.
- Ekranda Opus 5.5, Fable 5.1 ve Sonnet 5.5 model adları görünüyor; yalnız Opus 5.5 ana model olarak aday yapıldı.
- Mod 6'da konuşmada 'Opus veya Fable' geçiyor; ayrı araç olarak anlatılmadı.
- Sözlük eşleşmelerindeki (Matter.js, GSAP, Lottie vb.) çoğu bulanık eşleşme ve videoda kullanılmıyor.
- Videonun 5:24-5:46 aralığı Skool topluluk reklamı; araçlar RoboNuggets dışında kullanılmıyor.
- Ücretli plan şartı konuşmada geçiyor ama fiyat verilmiyor.
- Sürüm numarası 2.1.287 konuşmada; ekranda Claude Code v2.1.274 görünüyor, tutarsızlık olabilir.
## Atlanan segment oranı
0/18 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| skool.com/robonuggets | 5:24 | ekran | hayır |
| https://taxrebates.ai | 5:46 | ekran | hayır |
| github.com/zenbu-labs/terminal-browser/pull/113 | 9:30 | ekran | evet |
| https://www.skool.com/robonuggets-free/classroom/750914f0?md=a2e607329db2457f83744f817b9d8610 | açıklama | yorum | hayır |
| https://github.com/JohnnyVizz/claude-kit/tree/main/plugins/savvy-progress | açıklama | açıklama | evet |
| https://github.com/hellosverre/claude-skins | açıklama | açıklama | evet |
| https://github.com/data-goblin/claude-code-filetree | açıklama | açıklama | evet |
| https://github.com/karanb192/cache-tax | açıklama | açıklama | evet |
| https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/blast-radius | açıklama | açıklama | evet |
| https://github.com/BayramAnnakov/claude-reflect | açıklama | açıklama | evet |
| https://github.com/zenbu-labs/terminal-browser | açıklama | açıklama | evet |
| https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/replay-theater | açıklama | açıklama | evet |
| https://robolabs.so | 0:34 | ekran | hayır |
## İş akışı
- 1. adım — Claude Code'u en son sürüme güncelle (claude update veya masaüstü güncelleme penceresi) — araçlar: Claude Code, Claude desktop app
- 2. adım — PDF mod rehberini Claude Code'a gönderip kuruluma hangi modların uyduğunu sor — araçlar: Claude Code, Opus 5.5
- 3. adım — Savvy Progress ile çoklu ajanlı lansman kiti görevini başlat; ilerleme çubuğu ve ajan panelini izle — araçlar: Savvy Progress, Claude Code
- 4. adım — Claude Skins ile temaları dene, paletten Sunset skin'i üret — araçlar: Claude Skins
- 5. adım — You Should Know ile Kling video isteğinde maliyet uyarısını göster — araçlar: You Should Know, Kling 3.0, Kie AI
- 6. adım — File Tree ile Claude'un okuduğu/düzenlediği dosyaları canlı izle — araçlar: File Tree
- 7. adım — Cache Tax ile soğuk cache mesajını tut, maliyeti gör, /keepwarm ile sıcak tut — araçlar: Cache Tax
- 8. adım — Blast Radius ile rm -rf build komutunu durdur ve iptal et — araçlar: Blast Radius
- 9. adım — Reflect ile 'pnpm kullan' düzeltmesini CLAUDE.md'ye kural olarak kaydet — araçlar: Reflect
- 10. adım — Terminal Browser ile PR sayfasını terminal yanında aç — araçlar: Terminal Browser
- 11. adım — Replay Theater ile yeniden adlandırma ve makale düzenlemelerini tekrar oynat — araçlar: Replay Theater
- 12. adım — Kendi modunu yap: tarif et, plugin-authoring skill'i inşa etsin, hot reload aç — araçlar: plugin-authoring, Hot reloading, Claude Code
- 13. adım — Beğenilen modu plugin olarak kaydet ve kur — araçlar: /plugin, Claude Code
## Promptlar
- Modları PDF rehberinden kişiye göre seçtirmek — Ekli 9 Claude Mods PDF rehberini oku, kurulumumu kontrol et ve hangi modların bana uyduğunu söyle.
- Kendi modunu oluşturma — Claude Code için bir mod yap: ürettiğin her dosya ve sayfayı sohbet kutusunun üstünde küçük baloncuk olarak göster.
- Claude Skins için özel tema üretmek — Bu renk paletinden bir skin yap.
ikinci göz KAPALI: --ikinci-goz yok
