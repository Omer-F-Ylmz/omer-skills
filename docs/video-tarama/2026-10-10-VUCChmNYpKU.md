# Claude Knowledge Base + Scheduled Loop = Game Changer
## Künye
Claude Knowledge Base + Scheduled Loop = Game Changer · Eric Tech · süre: 17:32 · en-orig · https://youtu.be/VUCChmNYpKU · şema 2
motor: parti 2026-10-10-short-14 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 58280 tk · claude-haiku-5-5: claude-haiku-5-5 · 102862 tk
## Özet
Eric Tech, Karpathy'nin raw/wiki yapısından esinlenerek Claude Code ile kendini geliştiren bir ikinci beyin (bilgi tabanı) kurmayı dört adımda anlatıyor. Adımlar: klasör yapısı (raw, wiki, CLAUDE.md), ingest skill'i, veri kaynakları (Google Takeout, oturum geçmişi, MCP/connector'lar) ve Cowork'te zamanlanmış görevle çalışan kendini geliştiren skill. Videoda Virlo sponsor tanıtımı (MCP ile içerik araştırması) yer alıyor. Önemli ders: zamanlamadan önce skill elle denenip çalıştığı doğrulanmalı.
## Bölümler
- 0:00 Giriş
- 1:14 Adım 1 - Bilgi tabanı klasörü
- 3:43 Adım 2 - Ingest skill'i
- 4:59 Adım 3 - Veri kaynakları
- 9:47 Özet - İkinci beyin
- 10:03 Döngü (zamanlama)
- 12:29 Kendini geliştiren skill
- 15:21 Özet
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Ana yapay zekâ aracı; bilgi tabanıyla etkileşim, skill oluşturma ve oturum analizi için kullanılıyor. | 6:20 | Terminalde Claude Code v2.1.195 görülüyor. (karede: kanıttan) Terminalde Claude Code v2.1.195 görülüyor. |
| Claude Opus 4.8 | yok | teknik | yok | Claude Code oturumlarında çalışan model. | 6:20 | Terminalde Opus 4.8 (1M context) with high effort yazıyor. · kanıt: kare (karede: Terminalde Opus 4.8 (1M context) with high effort yazıyor.) |
| Claude | yok | teknik | yok | Sohbet, Cowork ve zamanlanmış görev arayüzü. | 7:26 | Claude uygulaması 'Coffee and Claude time?' ekranı. (karede: kanıttan) Claude uygulaması 'Coffee and Claude time?' ekranı. |
| Claude Cowork | yok | iş akışı | yok | Zamanlanmış görev (cron) oluşturmak için kullanılıyor. | 11:40 | Cowork sekmesinde 'Scheduled tasks' sayfası. (karede: kanıttan) Cowork sekmesinde 'Scheduled tasks' sayfası. |
| Codex | yok | CLI | yok | Geçmiş oturumları analiz etmek için kullanılıyor. | 6:56 | Codex'te 'Audit agent session history' sonuçları görülüyor. (karede: kanıttan) Codex'te 'Audit agent session history' sonuçları görülüyor. |
| Karpathy LLM Knowledge Bases | yok | teknik | yok | raw/ ve wiki/ yapısı üzerine kurulu LLM bilgi tabanı kavramı. | 1:20 | X'te Andrej Karpathy'nin 'LLM Knowledge Bases' gönderisi. · kanıt: kare (karede: X'te Andrej Karpathy'nin 'LLM Knowledge Bases' gönderisi.) |
| CLAUDE.md | yok | teknik | yok | Ajanın bilgi tabanıyla nasıl etkileşeceğini belirleyen ana talimat dosyası. | 1:12 | KnowledgeBase/ ağacında CLAUDE.md satırı. (karede: kanıttan) KnowledgeBase/ ağacında CLAUDE.md satırı. |
| ingest | yok | skill | yok | Dosyayı raw/'a kopyalayıp wiki'yi güncelleyen proje-yerel skill. | 4:24 | Prompt: 'Create a project-local skill called ingest at .claude/skills/ingest/SKILL.md'. (karede: kanıttan) Prompt: 'Create a project-local skill called ingest at .claude/skills/ingest/SKILL.md'. |
| Google Takeout | yok | CLI | yok | Google hesabı verisini dışa aktarıp bilgi tabanına almak için kaynak. | 5:24 | Google Takeout sayfası, 61 of 61 selected. (karede: kanıttan) Google Takeout sayfası, 61 of 61 selected. |
| Oturum geçmişi | yok | teknik | yok | Claude Code/Codex geçmiş oturumlarından tekrarlayan kalıpları çıkarma. | 6:28 | /resume ile 'Resume session (1 of 49)' listesi. · kanıt: kare (karede: /resume ile 'Resume session (1 of 49)' listesi.) |
| MCP | yok | MCP | yok | Üçüncü taraf araçlardan veri çekmek için connector/MCP bağlantıları. | 7:36 | Connectors sayfasında Firecrawl custom MCP URL'si. (karede: kanıttan) Connectors sayfasında Firecrawl custom MCP URL'si. |
| Firecrawl | yok | MCP | yok | Claude'a bağlı özel connector. | 7:36 | Customize > Connectors listesinde Firecrawl CUSTOM. (karede: kanıttan) Customize > Connectors listesinde Firecrawl CUSTOM. |
| Higgsfield | yok | MCP | yok | Claude'a bağlı özel connector. | 7:34 | Connectors menüsünde Higgsfield açık. (karede: kanıttan) Connectors menüsünde Higgsfield açık. |
| Gmail | yok | MCP | yok | Claude connector'ı olarak e-posta verisi kaynağı. | 7:34 | Connectors listesinde Gmail açık. (karede: kanıttan) Connectors listesinde Gmail açık. |
| Google Calendar | yok | MCP | yok | Claude connector'ı. | 7:34 | Connectors listesinde Google Calendar açık. (karede: kanıttan) Connectors listesinde Google Calendar açık. |
| n8n email | yok | MCP | yok | Claude'a bağlı özel connector. | 7:34 | Connectors menüsünde n8n email açık. (karede: kanıttan) Connectors menüsünde n8n email açık. |
| postiz | yok | MCP | yok | Claude connector menüsünde açık duran connector. | 7:34 | Menüde postiz anahtarı açık. (karede: kanıttan) Menüde postiz anahtarı açık. |
| GitHub Integration | yok | MCP | yok | Connector listesinde yüklü GitHub bağlantısı. | 7:36 | Connectors listesinde GitHub Integration. (karede: kanıttan) Connectors listesinde GitHub Integration. |
| Slack | yok | MCP | yok | Konuşmada anılan connector örneği. | 7:00 | There's Slack, there's the monday.com, and so many more. |
| Microsoft 365 | yok | MCP | yok | Dizinde gösterilen connector. | 7:38 | Directory'de Microsoft 365 kartı. (karede: kanıttan) Directory'de Microsoft 365 kartı. |
| Notion | yok | MCP | yok | Connector örneği olarak anıldı. | 7:00 | Slack, Microsoft 365, there's Gmail, Notions. |
| monday.com | yok | MCP | yok | Dizinde gösterilen ve söylenen connector. | 7:42 | Directory'de monday.com Interactive kartı. (karede: kanıttan) Directory'de monday.com Interactive kartı. |
| Virlo | yok | MCP | yok | Sosyal veri/trend analizi API'si ve MCP'si; Claude'a özel connector olarak eklendi (sponsor). | 8:34 | Add custom connector penceresinde ad Virlo, URL dev.virlo.ai/api/mcp/mcp. (karede: kanıttan) Add custom connector penceresinde ad Virlo, URL dev.virlo.ai/api/mcp/mcp. |
| Excalidraw | yok | teknik | yok | Klasör yapısı ve adım diyagramlarını çizmek için kullanıldı. | 1:12 | Excalidraw+ ve Excalidraw+ düğmesi görünüyor. (karede: kanıttan) Excalidraw+ ve Excalidraw+ düğmesi görünüyor. |
| Obsidian | yok | CLI | yok | Wiki'yi açıp gezmek için anılan not aracı. | 15:21 | Either we can use it to index it or using Obsidian here to open it. |
| Hermes Agent | yok | CLI | yok | Kullanılabilecek alternatif ajan olarak anıldı. | 9:47 | This could be a Hermes agent, or you could just talk to your Claude. |
| Skool | yok | teknik | yok | Eric'in topluluk platformu; promptlar orada paylaşılıyor. | 1:00 | EricTech Skool topluluk sayfası ve Classroom. (karede: kanıttan) EricTech Skool topluluk sayfası ve Classroom. |
| cron job | yok | teknik | yok | Skill'i belirli aralıklarla çalıştıran zamanlanmış görev. | 11:40 | Scheduled tasks sayfası, Frequency alanı. (karede: kanıttan) Scheduled tasks sayfası, Frequency alanı. |
| /resume | yok | ipucu | yok | Geçmiş Claude Code oturumlarını listeler. | 6:28 | Terminalde /resume ve 'Resume session (1 of 49)'. (karede: kanıttan) Terminalde /resume ve 'Resume session (1 of 49)'. |
| self-improving knowledge base | yok | skill | yok | Bilgi tabanını gözden geçiren, bulguları üç kovaya ayıran skill. | 12:29 | Creating a project local skill called improving system. |
| Gemini | yok | teknik | yok | Google'ın yapay zekâ ürünü; kullanıcının günlük verilerini (dışa aktarım) kaynak olarak anılıyor. | 4:59 | either you're using other AI tools like Gemini or Google accounts |
| Supabase | yok | teknik | yok | Veritabanı/backend servisi; oturum analizi çıktısında tekrarlayan iş olarak geçiyor. | 6:56 | Oturum analizi çıktısında 'Supabase row updates' tekrar eden iş akışı olarak yazıyor. (karede: Codex çıktısında 'Repeats: public gate URL vs real delivery URL, Supabase row updates' satırı.) |
| improving system | yok | skill | yok | Bilgi tabanını, oturum geçmişini ve bağlı veri skill'lerini tarayıp değişiklikleri otomatik/onaylı/belirsiz olarak ayıran kendini geliştirme skill'i. | 12:29 | creating a project local skill called improving system |
| Bilgi tabanı klasör yapısını kurmak | yok | prompt | yok | Bilgi tabanı klasörünü kur: mevcut dizini tara, dosyaları taşımadan önce onay iste, raw/ ve wiki/ oluştur. | 3:26 | kaynak: kare |
| Ingest skill'i oluşturmak | yok | prompt | yok | Proje-yerel ingest skill'i oluştur: dosyayı raw/'a kopyala, wiki'yi güncelle; raw'ı koru, çakışmada sor. | 4:24 | kaynak: kare |
| Oturum geçmişinden kalıp çıkarmak | yok | prompt | yok | Geçmiş Claude Code ve Codex oturumlarını tara, tekrarlayan kalıpları göster, körü körüne içe aktarma. | 6:00 | kaynak: kare |
| Virlo ile içerik araştırması | yok | prompt | yok | Virlo ile son 60 günde yapay zekâ araçları nişinde en iyi video fikirlerini hook, açı, platform ve görüntülenmeyle bul. | 8:02 | kaynak: altyazı |
| Kendini geliştiren bilgi tabanı skill'i | yok | prompt | yok | Kendini geliştiren skill: sistemi gözden geçir, veriyi yenile, bulguları otomatik uygula/onay gerekli/bağlam gerekli olarak ayır. | 13:29 | kaynak: kare |
## Açıklama bağlantıları
- https://dev.virlo.ai?el=eric — Virlo geliştirici sitesi (sponsor) · aday: evet (Virlo) · Videoda kullanılan servis; MCP ile Claude'a bağlandı. · sınıf: affiliate
- https://youtu.be/v8rCHym0lXE — Tanıtılan başka video · aday: hayır · Araç değil, video bağlantısı. · sınıf: diğer
- https://youtu.be/Y2rpFa43jTo — Obsidian ile Claude Code kurulum videosu · aday: hayır · Videoya bağlantı; araç değil. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Kahraman bölümü, ızgara kartları ve kod önizlemesi (hero, card grid, code block) | Virlo sayfasında başlık, API örneği ve yedi uç nokta ailesi kartları (karede: Virlo sitesinde 'Seven endpoint families' başlığı altında Orbit, Comet, Satellite, Tracking kartları ve koyu tema.) | 8:22 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /resume | Geçmiş Claude Code oturumlarını listeleyip devam ettirir. (karede: Terminalde /resume yazılı, 'Resume session (1 of 49)' listesi.) | 6:28 | kare |
| /mcp | MCP sunucusu kimlik doğrulaması için çalıştırılır. (karede: '1 MCP server needs authentication · run /mcp' uyarısı.) | 6:20 | kare |
| /schedule | Mevcut görevde zamanlanmış görev kurar. (karede: Scheduled tasks ekranında Type /schedule ifadesi.) | 11:40 | kare |
| /super-board | GitHub Project tabanlı otonom pipeline komutu; onboard, lint, status, run, stop alt komutlarını içerir. (karede: Komut öneri listesinde '/super-board' ve açıklaması.) | 6:24 | kare |
| /context-save | Git durumunu, alınan kararları ve kalan işi kaydeder; sonraki oturumda devam edilebilir. (karede: Komut öneri listesinde '/context-save' ve 'Save working context' açıklaması.) | 6:24 | kare |
| brew upgrade claude-code | Claude Code'u Homebrew ile güncelle (ekrandaki güncelleme uyarısında geçiyor). (karede: Terminalde 'Update available! Run: brew upgrade claude-code' satırı.) | 1:02 | kare |
| curl https://api.virlo.ai/v1/orbit -H "Authorization: Bearer <token>" -d '{...}' | Virlo Orbit uç noktasına niş araması gönderir; token değeri gizlendi. (karede: Virlo sayfasında curl örneği; Authorization satırında token kısaltılmış.) | 8:20 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Bilgi tabanı zamanlanmış görevle kendini geliştirebilir. | 0:00 | özellik |
| Cron'a koymadan önce skill elle denenip çalıştığı doğrulanmalı. | 11:03 | öneri |
| Oturum analizinde 2.370 JSONL dosyası tarandı, 2.323 oturum kullanılabilir bulundu. | 6:56 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Andrej Karpathy | Karpathy LLM Knowledge Bases | Karpathy'nin bilgi tabanı konsepti anlatılıyor. |
| kare 1:12 | Excalidraw | Excalidraw | Diyagram Excalidraw'da çiziliyor. |
| konuşma 3:43 | Codex | Codex | Oturum analizi Codex'te gösteriliyor. |
| kare 5:24 | Google Takeout | Google Takeout | Dışa aktarma sayfası gösterildi. |
| kare 7:36 | Firecrawl | Firecrawl | Connector olarak gösterildi. |
| kare 7:34 | Higgsfield | Higgsfield | Connector menüsünde. |
| kare 7:34 | Sentry | aday değil: konu dışı | Yalnızca menüde görünüyor, kullanılmıyor. |
| kare 7:34 | postiz | postiz | Connector menüsünde açık. |
| kare 7:40 | Figma | aday değil: konu dışı | Yalnızca dizin listesinde. |
| konuşma 7:00 | Slack | Slack | Connector örneği olarak söylendi. |
| konuşma 7:00 | Notion | Notion | Connector örneği olarak söylendi. |
| kare 7:42 | monday.com | monday.com | Dizinde gösterildi ve söylendi. |
| kare 8:34 | Virlo | Virlo | Custom connector olarak eklendi. |
| kare 0:32 | n8n | aday değil: konu dışı | Tanıtım klibi. |
| kare 1:00 | Ollama | aday değil: konu dışı | Önceki videonun küçük resmi. |
| açıklama | bookzero.ai | aday değil: konu dışı | Yalnızca açıklamada reklam metni. |
| açıklama | skool.com/erictech | Skool | Topluluk bağlantısı. |
| yorum | Obsidian | Obsidian | Sahip yorumunda ve özette anılıyor. |
| konuşma 9:47 | Hermes Agent | Hermes Agent | Alternatif ajan olarak anıldı. |
| konuşma 11:40 | cron job | cron job | Zamanlama için anlatıldı. |
## Kareden okunanlar
- 1:12: KnowledgeBase/ ağacı: CLAUDE.md, raw/, wiki/, assets/.
- 6:20: Claude Code v2.1.195, Opus 4.8 (1M context).
- 6:56: Codex ekranı: 2,370 JSONL dosyası tarandı, 2,323 oturum.
- 8:34: Add custom connector: Virlo, dev.virlo.ai/api/mcp/mcp.
- 12:16: Create scheduled task: Name, Description, Frequency Manual.
## Belirsizlikler
- Videoda anılan 'Claude 70 file' ifadesi altyazı hatası, CLAUDE.md olarak yorumlandı.
- 'Viralo/Verlo' yazımı altyazıda farklı; ekranda Virlo.
- Açıklama bağlantısı Virlo'da ?el=eric parametresi var ama konuşmada 'shoutout' deniyor; açık sponsor ifadesi yok, bu yüzden affiliate seçildi.
- Skool topluluğu, monday.com gibi menü öğeleri aday olarak mı sayılacağı kesin değil.
- Ekranda görünen Stripe, n8n, Canva, Ollama gibi öğeler tanıtım/montaj klipleri; kullanım değil.
## Atlanan segment oranı
0/21 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| skool.com/erictech | 0:28 | ekran | hayır |
| monday.com | 7:00 | ses | evet |
| https://mcp.firecrawl.dev/fc-6f7e142c474045b497ae7e19f373effc/v2/mcp | 7:36 | ekran | evet |
| https://api.virlo.ai/v1/orbit | 8:20 | ekran | evet |
| dev.virlo.ai/docs/tracking | 8:24 | ekran | evet |
| dev.virlo.ai/docs/comet | 8:28 | ekran | evet |
| dev.virlo.ai/docs/sounds | 8:30 | ekran | evet |
| dev.virlo.ai/docs/trends | 8:32 | ekran | evet |
| https://dev.virlo.ai/api/mcp/mcp | 8:34 | ekran | evet |
| https://dev.virlo.ai?el=eric | açıklama | açıklama | evet |
| https://youtu.be/v8rCHym0lXE | açıklama | açıklama | hayır |
| https://youtu.be/Y2rpFa43jTo | açıklama | yorum | hayır |
| bookzero.ai | açıklama | açıklama | hayır |
| https://mcp.firecrawl.dev/[anahtar gizlendi]/v2/mcp | 7:36 | ekran | hayır |
| https://api.virlo.ai/v1 | 8:16 | ekran | evet |
| https://api.virlo.ai/v1/orbit (OCR: vl/orbit) | 8:25 | ekran | evet |
| https://dev.virlo.ai/api/mcp/mcpl (OCR; muhtemelen mcp) | 8:36 | ekran | hayır |
| https://dev.virlo.ai/docs/hooks | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/playground | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/agents | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/satellite | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/hashtags | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/webhooks | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/mcp | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/ai-agents | açıklama | açıklama | hayır |
| https://dev.virlo.ai/docs/quickstart | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Karpathy'nin LLM bilgi tabanı gönderisinden raw/wiki kavramını tanıtmak — araçlar: Karpathy LLM Knowledge Bases
- 2. adım — Excalidraw'da klasör yapısını çizmek (CLAUDE.md, raw, wiki, assets) — araçlar: Excalidraw, CLAUDE.md
- 3. adım — Klasör kurulum promptunu Claude Code'a vermek — araçlar: Claude Code
- 4. adım — Ingest skill'ini oluşturmak — araçlar: Claude Code, ingest
- 5. adım — Google Takeout ile Google verisini dışa aktarmak — araçlar: Google Takeout
- 6. adım — Geçmiş oturumları /resume ile görüp Codex'te analiz ettirmek — araçlar: Claude Code, Codex, /resume
- 7. adım — Connector'ları (Firecrawl, Gmail vb.) incelemek — araçlar: Claude, MCP, Firecrawl
- 8. adım — Virlo'yu Claude'a özel connector olarak eklemek — araçlar: Virlo, MCP, Claude
- 9. adım — Virlo ile yüksek performanslı içerik fikirlerini sorgulamak — araçlar: Virlo, Claude
- 10. adım — Kendini geliştiren skill'i oluşturup elle test etmek — araçlar: Claude Code, self-improving knowledge base
- 11. adım — Cowork'te zamanlanmış görev oluşturup kaydetmek — araçlar: Claude Cowork, cron job
## Promptlar
- Bilgi tabanı klasör yapısını kurmak — Bilgi tabanı klasörünü kur: mevcut dizini tara, dosyaları taşımadan önce onay iste, raw/ ve wiki/ oluştur.
- Ingest skill'i oluşturmak — Proje-yerel ingest skill'i oluştur: dosyayı raw/'a kopyala, wiki'yi güncelle; raw'ı koru, çakışmada sor.
- Oturum geçmişinden kalıp çıkarmak — Geçmiş Claude Code ve Codex oturumlarını tara, tekrarlayan kalıpları göster, körü körüne içe aktarma.
- Virlo ile içerik araştırması — Virlo ile son 60 günde yapay zekâ araçları nişinde en iyi video fikirlerini hook, açı, platform ve görüntülenmeyle bul.
- Kendini geliştiren bilgi tabanı skill'i — Kendini geliştiren skill: sistemi gözden geçir, veriyi yenile, bulguları otomatik uygula/onay gerekli/bağlam gerekli olarak ayır.
ikinci göz KAPALI: --ikinci-goz yok
