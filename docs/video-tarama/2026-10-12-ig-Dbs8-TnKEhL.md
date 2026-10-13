# Five plugins and Claude Code stops being the thing you ration.
## Künye
Five plugins and Claude Code stops being the thing you ration. · buildwithai.club · süre: 1:01 · ? · https://www.instagram.com/reel/Dbs8-TnKEhL/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-12-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 38517 tk · claude-haiku-5-5: claude-haiku-5-5 · 52335 tk
## Özet
Instagram reel'i: Claude Code'un limit ve token sorununu çözen beş eklentiyi sırasıyla anlatıyor. OmniRoute 237 sağlayıcıya bağlanır ve limit dolunca otomatik geçer. Claude Mem oturumlar arası hafıza verir. Headroom token tüketimini azaltır. Claude Code Setup resmi Anthropic eklentisidir ve repoda eksik hook, skill ve MCP sunucularını bulur. Task Observer düzeltmelerinizi izleyip diğer skill'leri günceller. Yorumda 'Claude' yazana linkler gönderileceği söyleniyor.
## Bölümler
- 0:00 Giriş: beş eklenti
- 0:05 OmniRoute: 237 sağlayıcı, limit dolunca geçiş
- 0:18 Claude Mem: oturumlar arası hafıza
- 0:30 Headroom: token tasarrufu
- 0:39 Claude Code Setup: repo analizi
- 0:48 Task Observer: düzeltmelerden öğrenme
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| OmniRoute | yok | CLI | github.com/diegosouzapw/OmniRoute | 237 yapay zekâ sağlayıcısına bağlanan, limit dolunca sıradaki modele geçen yönlendirici | 0:05 | Omniroot, which connects you to 237 AI providers, 90 of which are free |
| Claude Mem | yok | plugin | yok | Claude'a tüm oturumlar boyunca hafıza veren eklenti | 0:23 | second plugin is Cloud Mem. It gives Cloud memory across every session. |
| Headroom | yok | plugin | yok | Yalnızca önemli kısımları geçirerek token tüketimini azaltan proxy | 0:32 | third plugin is going to be Headroom, which only passes through the parts that actually matter |
| Claude Code Setup | yok | plugin | yok | Resmi Anthropic eklentisi; kod tabanını tarar, eksik hook, skill ve MCP sunucularını önerir | 0:41 | official Anthropic plugin, which scans your codebase, names the hooks, skills, and MCP servers |
| Task Observer | yok | skill | yok | Çalışma şeklinizi izleyip düzeltmelerinizi yakalayan ve diğer skill'leri yeniden yazan eklenti | 0:48 | Task Observer. It watches how you work, catches every correction you make |
| Claude Code | yok | CLI | yok | Eklentilerin kurulduğu ana yapay zekâ kodlama aracı | 0:32 | Ekranda Claude Code sürüm satırı görünüyor (karede: OCR: 'Claude Code v2.1.98' ve 'Launching Claude Code (API routed through Headroom)') |
| Claude Opus | yok | teknik | yok | Headroom üzerinden çalışan Claude Code oturumunda kullanılan model | 0:32 | Model satırı ekranda görünüyor (karede: OCR: 'Opus 4.6 (1M context) - API Usage Billing') |
| rtk | yok | CLI | yok | Headroom başlatılırken kurulan yardımcı araç | 0:32 | Kurulum satırı ekranda görünüyor (karede: OCR: 'Setting up rtk...') |
| OpenRouter | yok | teknik | yok | OmniRoute'un ücretsiz token bütçesi hesabında geçen sağlayıcı | 0:15 | Ücretsiz token açıklaması ekranda görünüyor (karede: OCR: 'a $10 OpenRouter top-up that unlocks +24M/mo') |
| sqlite-vec | yok | teknik | yok | Claude Mem hafıza aramasında vektör geri çağırma için anılan yapı | 0:28 | Hafıza kaydı ekranda görünüyor (karede: OCR: 'KV too slow for vector recall — moved to sqlite-vec') |
| MCP | yok | teknik | yok | Claude Code Setup'ın önerdiği entegrasyon kategorilerinden biri | 0:41 | names the hooks, skills, and MCP servers you're missing |
| Headroom üzerinden çalışan Claude Code'a kod tabanı analizi yaptırmak | yok | prompt | yok | Headroom kod tabanını derinlemesine incele, sorunları anla; alt ajanlar kullanılabilir. Rakip ve pazar araştırması paralel yürütülsün. | 0:32 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| headroom wrap claude | Claude Code'u API'si Headroom proxy'sinden geçecek şekilde başlatır (karede: OCR: 'headroom wrap claude' ve 'Launching Claude Code (API routed through Headroom)') | 0:32 | kare |
| ANTHROPIC_BASE_URL=http://127.0.0.1:8787 | Claude Code API trafiğini yerel Headroom proxy'sine yönlendirir (karede: OCR: 'ANTHR0PIC_BASE_URL=http://127.0.0.1:8787') | 0:32 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| OmniRoute 237 sağlayıcıya bağlanır, 90'ı ücretsizdir; limit dolunca sıradaki modele geçer | 0:05 | özellik |
| Ücretsiz katmanlar aylık yaklaşık 1,6 milyar token eder | 0:15 | sayısal |
| Claude Mem tüm oturumlar boyunca hafıza sağlar | 0:23 | özellik |
| Headroom aynı cevapları çok daha az tokenla verir | 0:32 | özellik |
| Claude Code Setup resmi Anthropic eklentisidir | 0:41 | özellik |
| Task Observer düzeltmeleri yakalar ve diğer skill'leri yeniden yazar; kurulum sırası: OmniRoute, Claude Mem, Headroom, Claude Code Setup, Task Observer | 0:48 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:05 | OmniRoute | OmniRoute | Omniroot connects you to 237 AI providers |
| konuşma 0:23 | Claude Mem | Claude Mem | second plugin is Cloud Mem |
| konuşma 0:32 | Headroom | Headroom | third plugin is going to be Headroom |
| konuşma 0:41 | Claude Code Setup | Claude Code Setup | fourth one, Claude Code Setup, fixes your repo |
| konuşma 0:48 | Task Observer | Task Observer | fifth is Task Observer |
| kare 0:32 | Claude Code | Claude Code | OCR: Claude Code v2.1.98 |
| kare 0:32 | Claude Opus | Claude Opus | OCR: Opus 4.6 (1M context) |
| kare 0:32 | rtk | rtk | OCR: Setting up rtk... |
| kare 0:15 | OpenRouter | OpenRouter | OCR: $10 OpenRouter top-up |
| kare 0:28 | sqlite-vec | sqlite-vec | OCR: moved to sqlite-vec |
| konuşma 0:41 | MCP sunucuları | MCP | names the hooks, skills, and MCP servers |
| konuşma 0:41 | hook ve skill kavramları | aday değil: genel kavram | hooks, skills, and MCP servers you're missing |
| kare 0:08 | Cursor IDE, OpenAI Codex, GitHub Copilot, GitLab Duo, ClinePass, Devin CLI | aday değil: başka adayın parçası (OmniRoute) | Sağlayıcı tablosu satırları |
| kare 0:09 | Qwen Code, Trae, Windsurf, Zed, Adapta | aday değil: başka adayın parçası (OmniRoute) | Sağlayıcı tablosu satırları |
| kare 0:10 | Gemini Web, Grok Web, HuggingChat, Inner.ai, Kimi Web, Arena | aday değil: başka adayın parçası (OmniRoute) | Web Cookie Providers tablosu |
| kare 0:09 | github.com/diegosouzapw/OmniRoute | OmniRoute | OCR: github.com/diegosouzapw/Omn... |
| kare 0:41 | claude.com/plugins/claude-code-setup | Claude Code Setup | OCR: claude.com/plugins/claude-code-setup |
| kare 0:32 | headroom wrap claude komutu | Headroom | OCR: headroom wrap claude |
| kare 0:32 | ANTHROPIC_BASE_URL yerel proxy | Headroom | OCR: http://127.0.0.1:8787 |
| kare 0:05 | Claude plan kullanım limiti ekranı | Claude Code | OCR: PLAN USAGE LIMITS - MAX |
| açıklama | #claudecode #anthropicclaude #aiplugins #mcpservers #aiguide etiketleri | aday değil: genel kavram | Açıklama sonundaki hashtag satırı |
| açıklama | Instagram reel bağlantısı | aday değil: konu dışı | https://www.instagram.com/reel/Dbs8-TnKEhL/ |
| linkli sayfa | delta.dev ve gpui.rs (zed.dev'e çıkıyor) | aday değil: konu dışı | Paketteki bağlantılı sayfalar listesi |
| yorum | Yorumlar | aday değil: konu dışı | Yorumlar girişsiz alınamadı |
## Kareden okunanlar
- 0:08: Sağlayıcı tablosu: clinepass, codebuddy-cn, codex, cursor, devin-cli, github, gitlab-duo, grok-cli; altyazı 'which'
- 0:09: GitHub'da OmniRoute docs/reference/PROVIDER_REFERENCE.md; qwen, trae, windsurf, zed, zed-hosted satırları; altyazı 'to 237'
- 0:10: Web Cookie sağlayıcıları: gemini-business, gemini-web, grok-web, huggingchat, inner-ai, kimi-web, lmarena; altyazı 'providers,'
## Belirsizlikler
- Dil alanı '?' ve yorumlar girişsiz alınamadı; 'Comment Claude' sonrası gönderilecek linkler bilinmiyor.
- Konuşmada 'Omniroot' ve 'Cloud Mem' geçiyor; ad olarak açıklamadaki OmniRoute ve Claude Mem kullanıldı.
- OmniRoute sağlayıcı tablosundaki Cursor, Codex, Copilot, GitLab Duo, Qwen Code, Trae, Windsurf, Zed, Gemini Web, Grok Web, HuggingChat, Kimi Web, Arena yalnız listede görünüyor, kullanılmıyor.
- Task Observer ve Claude Mem için kurulum komutu gösterilmedi.
- Paketteki delta.dev ve gpui.rs bağlantılı sayfaları zed.dev'e çıkıyor; videoda anılmıyor.
- 0:12-0:14 'out of tokens' ekranları ve 0:52-0:55 görev listesi muhtemelen illüstrasyon animasyonu; gerçek kullanım olduğu doğrulanamadı.
- Ek kare yalnız 0:08, 0:09, 0:10 için vardı; diğer ekran bilgileri OCR'a dayanıyor.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/Dbs8-TnKEhL/ | açıklama | açıklama | hayır |
| github.com/diegosouzapw/OmniRoute | 0:09 | ekran | evet |
| solo.trae.ai | 0:09 | ekran | hayır |
| zed.dev | 0:09 | ekran | hayır |
| Adapta.org | 0:09 | ekran | hayır |
| Inner.ai | 0:10 | ekran | hayır |
| arena.ai | 0:10 | ekran | hayır |
| http://127.0.0.1:8787 | 0:32 | ekran | hayır |
| claude.com/plugins/claude-code-setup | 0:41 | ekran | evet |
| github.com/diegosouzapw/Omn... | 0:09 | ekran | evet |
| https://delta.dev | açıklama | açıklama | hayır |
| https://gpui.rs | açıklama | açıklama | hayır |
| https://zed.dev (sayfa) | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Claude Code plan kullanım limiti ekranı gösterilir — araçlar: Claude Code
- 2. adım — OmniRoute sağlayıcı referansı incelenir (237 sağlayıcı, 90'ı ücretsiz) — araçlar: OmniRoute, GitHub
- 3. adım — Limit dolunca modelin otomatik değiştirilmesi ve aylık ~1,6 milyar ücretsiz token gösterilir — araçlar: OmniRoute, OpenRouter
- 4. adım — Claude Mem ile oturumlar arası hafıza ve arama gösterilir — araçlar: Claude Mem, sqlite-vec
- 5. adım — Headroom proxy'si ile Claude Code başlatılır — araçlar: Headroom, Claude Code, rtk
- 6. adım — Headroom kod tabanını incelemek için alt ajanlar paralel çalıştırılır — araçlar: Claude Code, Headroom, Claude Opus
- 7. adım — Token tasarruf göstergesi gösterilir — araçlar: Headroom
- 8. adım — Claude Code Setup eklenti sayfası ve önerileri gösterilir — araçlar: Claude Code Setup, MCP
- 9. adım — Task Observer'ın görev ve düzeltme izlemesi gösterilir — araçlar: Task Observer
- 10. adım — İzleyiciden linkler için yorum yazması istenir — araçlar: Instagram
## Promptlar
- Headroom üzerinden çalışan Claude Code'a kod tabanı analizi yaptırmak — Headroom kod tabanını derinlemesine incele, sorunları anla; alt ajanlar kullanılabilir. Rakip ve pazar araştırması paralel yürütülsün.
ikinci göz KAPALI: --ikinci-goz yok
