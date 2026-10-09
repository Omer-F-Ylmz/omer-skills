# Claude Limitlerine artık asla takılma
## Künye
Claude Limitlerine artık asla takılma · Doruk Yalçınsoy · süre: 17:15 · tr-orig · https://youtu.be/uu-qQVfncko · şema 2
motor: parti 2026-10-09-uzun-5 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
claude-sonnet-5-5: claude-sonnet-5-5 · 69626 tk · claude-haiku-5-5: claude-haiku-5-5 · 130329 tk
## Özet
Doruk Yalçınsoy, Claude (Claude Code) kullanım limitlerine takılmamak için token kavramını, API ile abonelik farkını (100 dolara 2.500 dolarlık kullanım), session/context mantığını ve 11 taktiği anlatıyor: /compact, rewind, /context, Haiku alt ajan, plan modu, /btw, MD dosyalarını İngilizce yazma, Markdown'a çevirme (docling), kısa CLAUDE.md, .claudeignore ve ajan haritalama.
## Bölümler
- 0:00 Giriş: Claude limitlerini aşmak ve verimlilik
- 0:15 Token nedir? (yapay zekânın kalorisi)
- 1:00 Türkçe kullanımın token maliyetine etkisi
- 1:38 API vs abonelik: 25 kat daha fazla kullanım hakkı
- 3:07 Session ve context kavramı
- 4:47 Taktik 1: Context rot ve /compact
- 7:32 Taktik 2: Rewind ve /context sayacı
- 9:52 Taktik 3: Doğru işe doğru ajan (Haiku)
- 10:55 Taktik 4: Plan modu ve /btw
- 12:42 Taktik 5: MD dosyaları İngilizce ve Markdown dönüşümü
- 14:00 Taktik 6: CLAUDE.md, .claudeignore ve ajan haritalama
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Videonun ana aracı; oturumlar, /compact, rewind, /context ve modlar bunun içinde gösteriliyor. | 7:58 | Yeni oturum ekranında 'Claude Code' başlığı ve Bypass permissions görünüyor. (karede: kanıttan) Yeni oturum ekranında 'Claude Code' başlığı ve Bypass permissions görünüyor. |
| Claude Opus | yok | teknik | yok | Sunucunun/oturumun çalıştığı ana model; 1M token bağlam penceresi. | 4:07 | 1 milyon token... işte opus 4.7de öyle şu anda. |
| Claude Haiku | yok | teknik | yok | Araştırma gibi angarya işler için ucuz alt ajan modeli. | 9:52 | Araştırma gibi işleri Hayku'ya ver HK yapsın... Opus yapmasın. |
| Claude Sonnet | yok | teknik | yok | Kullanım limitleri ekranında ayrı 'Sadece Sonnet' haftalık kotası. | 2:34 | Plan usage limits kartında 'Sadece Sonnet' satırı görünüyor. (karede: kanıttan) Plan usage limits kartında 'Sadece Sonnet' satırı görünüyor. |
| Sub-agent | yok | teknik | yok | Keşif işini ayrı bağlamda yapıp yalnız özet döndüren alt ajan. | 9:52 | Şimdi sub agent konusu var... Haiku ile araştır. |
| /compact | yok | ipucu | yok | Bağlamı özetleyip yeni pencerede devam ettirir; %50-70'te kullanılması öneriliyor. | 5:49 | %50, %60 %70'e doğru toparla. Hoppact yaz. |
| /clear | yok | ipucu | yok | Özeti kopyalayıp temiz sayfayla başlama seçeneği. | 6:50 | Özeti kopyalarız. Clear da yapabiliriz. |
| Rewind | yok | ipucu | yok | Önceki bir mesaja geri dönüp başarısız denemeleri bağlamdan temizler (Esc Esc veya /rewind). | 8:32 | İki kere ESC'ye basarak... slash rewind yazdığım zaman çalıştırabiliyorum. |
| /context | yok | ipucu | yok | Bağlam kullanımını kategori bazında gösterir. | 9:16 | Estimated usage by category tablosu: System prompt, MCP tools, Messages, Free space. (karede: kanıttan) Estimated usage by category tablosu: System prompt, MCP tools, Messages, Free space. |
| Plan modu | yok | ipucu | yok | Düzenlemeden önce kodu inceleyip plan sunan mod. | 10:48 | Modes listesinde 'Plan mode' seçili. (karede: kanıttan) Modes listesinde 'Plan mode' seçili. |
| Bypass permissions | yok | ipucu | yok | Onay gerektirmeyen izin modu; konuşmacı genelde bunu kullanıyor. | 10:55 | Genelde bypass permissions diyoruz. Yani iznemiz ne gerek yok abi. |
| /btw | yok | ipucu | yok | Ana bağlamı kirletmeden yan soru sorma komutu; videoda ortamda mevcut değil çıktı. | 12:02 | '/btw isn't available in this environment.' yanıtı görünüyor. (karede: kanıttan) '/btw isn't available in this environment.' yanıtı görünüyor. |
| docling | yok | CLI | yok | PDF/HTML/DOCX/PPTX dosyalarını temiz Markdown'a çeviren açık kaynak CLI. | 13:00 | 'pip install docling' ve 'docling rapor.pdf --output md' komutları. (karede: kanıttan) 'pip install docling' ve 'docling rapor.pdf --output md' komutları. |
| Markdown | yok | teknik | yok | HTML/PDF/DOCX yerine token tasarrufu için tercih edilen biçim. | 12:42 | HTML olursa %90 fazla... PDF'se %70... docx %33 daha fazla. |
| CLAUDE.md | yok | teknik | yok | Her oturumda yüklenen kural dosyası; kısa tutulmalı, ajan haritası içermeli. | 14:00 | İki tane Cloud MD vardır. Birincisi bilgisayardaki, ikincisi projenin içindeki. |
| .claudeignore | yok | teknik | yok | Büyük klasörleri Claude'un taramasından dışlar. | 15:00 | '.claudeignore ile büyük klasörleri dışla' metni. (karede: kanıttan) '.claudeignore ile büyük klasörleri dışla' metni. |
| Ajan haritalama | yok | teknik | yok | CLAUDE.md'de küçük tablo; görevde yalnız ilgili ajan dosyası yüklenir. | 15:18 | 'CLAUDE.md HARİTASI' kartı: YouTube → agents/youtube/AGENT.md. (karede: kanıttan) 'CLAUDE.md HARİTASI' kartı: YouTube → agents/youtube/AGENT.md. |
| Codex | yok | CLI | yok | Özeti başka modele taşımak için anılan alternatif ajan. | 6:50 | Sağ tarafta Codex var... Gemini'ya veririm. |
| Gemini | yok | teknik | yok | Özetin taşınabileceği başka bir yapay zekâ modeli. | 6:50 | Cemina'ya veririm vesaire. |
| Notion | yok | MCP | yok | /context çıktısında yüklü MCP olarak görünen servis. | 9:14 | mcp__claude_ai_Notion__notion-search vb. MCP araç listesi. (karede: kanıttan) mcp__claude_ai_Notion__notion-search vb. MCP araç listesi. |
| frontend-design | yok | skill | yok | /context skill listesinde Plugin kaynaklı skill. | 9:11 | Skills tablosunda frontend-design, kaynak Plugin, 67 token. (karede: kanıttan) Skills tablosunda frontend-design, kaynak Plugin, 67 token. |
| claude-api | yok | skill | yok | /context skill listesinde yüklü skill. | 9:11 | Skills tablosunda claude-api 189 token. (karede: kanıttan) Skills tablosunda claude-api 189 token. |
| Skool | yok | teknik | yok | Konuşmacının topluluğunun barındığı platform (İş Güç Yapay Zeka). | 16:32 | Classroom sayfası, adres skool.com/is-guc-yapayzeka/classroom. (karede: kanıttan) Classroom sayfası, adres skool.com/is-guc-yapayzeka/classroom. |
| Outfit | yok | teknik | yok | Slayt başlıklarında kullanılan geometrik sans font görünümü; ad doğrulanmadı. | 0:00 | Başlık 'Claude Limitlerini Aş' geometrik sans ile yazılı. · kanıt: kare (karede: Başlık 'Claude Limitlerini Aş' geometrik sans ile yazılı.) |
| pip | yok | CLI | yok | Python paket yöneticisi; Docling'in kurulumu için 'pip install docling' komutunda kullanılıyor. | 13:00 | pip install docling (karede: Ekranda 'pip install docling' komutu yazıyor.) |
| Web Search | yok | teknik | yok | Alt ajanın güncel trend araştırması için kullandığı web arama aracı. | 10:40 | Web search results for query (karede: Agent çıktısında 'Web Search' satırı ve sonuç bağlantıları görünüyor.) |
| Chrome | yok | teknik | yok | Hazırlanan HTML sunumunu açmak için kullanılan tarayıcı. | 7:14 | Açmak için: dosyayı Chrome'da aç. (karede: Sohbet çıktısında 'Açmak için: dosyayı Chrome'da aç' yazıyor; sunum tarayıcıda açık.) |
| Ucuz modelle araştırma yaptırma | yok | prompt | yok | Git ve YouTube ile ilgili bu ayki trendleri alt ajan olarak Haiku ile araştır. | 10:12 | kaynak: kare |
| /btw komutunu deneme | yok | prompt | yok | Yan soru olarak Türkiye'deki trendleri sor (/btw ile). | 12:14 | kaynak: kare |
| Slayt örneği: alt ajan ile bağlamı hafif tutma | yok | prompt | yok | Auth akışını Haiku alt ajanı ile araştır, yalnız özet dön. | 9:46 | kaynak: kare |
## Açıklama bağlantıları
- https://www.skool.com/is-guc-yapayzeka/about — İş Güç Yapay Zeka topluluğu hakkında sayfası · aday: hayır · Konuşmacının kendi topluluk tanıtımı; izleyicinin kullanacağı araç değil. Skool platformu ayrıca aday. · sınıf: diğer
- https://dorukyalcinsoy.com/ — Konuşmacının kişisel sitesi · aday: hayır · Kişisel site/portfolyo, araç değil. · sınıf: diğer
- https://dorukyalcinsoy.com/e-kitap — Ücretsiz Claude Code e-kitabı · aday: hayır · İçerik/e-kitap sayfası, araç değil. · sınıf: diğer
- https://dorukyalcinsoy.com/podcast — Podcast konuk başvurusu · aday: hayır · Tanıtım sayfası, araç değil. · sınıf: diğer
- https://www.instagram.com/dorukyalcinsoy/ — Instagram profili · aday: hayır · Sosyal medya profili. · sınıf: diğer
- https://www.linkedin.com/in/dorukyalcinsoy/ — LinkedIn profili · aday: hayır · Sosyal medya profili. · sınıf: diğer
- https://x.com/dorukyalcinsoy — X profili · aday: hayır · Sosyal medya profili. · sınıf: diğer
- https://www.youtube.com/channel/UCJJrZm2OysRQJj5eWlIoSXQ?sub_confirmation=1 — Kanala abone olma bağlantısı · aday: hayır · Kanal abonelik bağlantısı, araç değil. · sınıf: diğer
- https://www.skool.com/is-guc-yapayzeka — İş Güç Yapay Zeka Skool topluluğu · aday: evet (Skool) · Alan adı Skool platformunu adlandırıyor ve videoda topluluk ekranı gösteriliyor. · sınıf: diğer
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Koyu tema slayt, ızgara/noktalı arka plan, vurgu rengi mercan (Dark theme, dotted background, accent color) | Sunum slaytları koyu zemin, noktalı desen ve Claude mercan vurgusuyla (karede: Siyah zeminde 'Claude Limitlerini Aş' başlığı, 'Claude' mercan renkte, sağda mercan maskot.) | 0:00 | kare |
| Sekme çubuğu (Tab bar) | VS Code tarzı Session 1/2/3 sekmeleri, aktif sekmede mercan üst kenarlık (karede: Session 1 aktif, Session 2 ve 3 soluk, sonda + ikonu.) | 3:06 | kare |
| Doluluk çubuğu (Progress bar) | Kullanım limiti ve mesaj sayısına göre dolan yatay çubuklar (karede: Mesaj 1/30/100/240+ çubukları, sonuncu kırmızı dolu.) | 4:44 | kare |
| Kart ızgarası (Card grid) | İnsan/Ajan karşılaştırma kartları, mod listesi ve ajan haritası kartları (karede: 'Kalori yakar' ve 'Token yakar' iki kart yan yana.) | 0:30 | kare |
| Büyük sayı vurgusu (Big number stat) | $100 → $2.500 ve +75% gibi büyük rakamlar (karede: Gri $100 ve mercan $2.500 büyük yazı.) | 2:28 | kare |
| Giriş animasyonu (Fade-in animation) | Öğeler sırayla belirerek geliyor; kodda anim-d1 sınıfı (karede: h1 class="anim-d1" ve accent span içeren kod satırları.) | 7:52 | kare |
| Monospace font vurgusu (Monospace type) | Etiket ve rakamlarda tek aralıklı yazı (karede: $100 ve $2.500 monospace benzeri kalın rakamlarla.) | 2:28 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /compact | Konuşmayı özetleyip yeni bağlamda devam ettirir (karede: Sohbette '/compact' yazılı ve 'Compacting...' görünüyor.) | 6:30 | kare |
| /clear | Bağlamı sıfırlar, temiz sayfa açar (karede: Handoff slaytında '③ /clear' adımı.) | 6:40 | kare |
| /rewind | Seçilen mesaja geri dönüp konuşmayı ve kodu o noktadan çatallar (Esc Esc ile de açılır) (karede: 'Rewind to...' penceresi, mesaj listesi ve 'Select a message to restore code'.) | 7:58 | kare |
| /context | Bağlam kullanımını kategori bazında gösterir (karede: 'Estimated usage by category' tablosu.) | 9:16 | kare |
| /btw | Ana bağlama dokunmadan yan soru sorar (karede: '/btw isn't available in this environment.' mesajı.) | 12:02 | kare |
| pip install docling | Markdown dönüştürücü docling'i kurar (karede: Slaytta 'pip install docling' kod satırı.) | 13:00 | kare |
| docling rapor.pdf --output md | PDF'i Markdown'a çevirir (karede: Slaytta 'docling rapor.pdf --output md' satırı.) | 13:00 | kare |
| /btw Next.js 15 Server Actions nasıl? | Yan soruyu ana bağlamı kirletmeden yanıtlatır. (karede: Sohbet kutusunda '/btw Next.js 15 Server Actions nasıl?' yazıyor.) | 11:50 | kare |
| /debug | Claude Code'un yerleşik komutu; videoda ne yaptığı açıklanmıyor. (karede: Slash komut listesinde '/debug' yazıyor.) | 3:14 | kare |
| /remote-control | Claude Code'un yerleşik komutu; videoda ne yaptığı açıklanmıyor. (karede: Slash komut listesinde '/remote-control' yazıyor.) | 3:14 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| İnsan bir yılda yaklaşık 10 milyon token/kelime konuşur; konuşmacı bir gecede 9 milyon token yaktı. | 0:15 | sayısal |
| Türkçe kullanım %30-%75, hatta iki kata kadar daha fazla token harcatır. | 1:00 | sayısal |
| 100 dolarlık abonelik yaklaşık 2.500 dolarlık API token hakkı sağlar (25 kat). | 1:38 | karşılaştırma |
| Model bağlam %90 dolulukta verimini yitirir; %50-70'te /compact önerilir. | 5:49 | öneri |
| Slayt: Auto-compact %95'te tetiklenir, manuel /compact ile erken tetiklenmeli. | 5:52 | özellik |
| Slayt: bağlam dolunca doğruluk %92'den %78'e düşer. | 4:44 | sayısal |
| HTML Markdown'a göre ~%90, PDF ~%70, DOCX ~%33 daha fazla token harcatır. | 12:42 | sayısal |
| Alt ajan keşfi Haiku ile yapılınca maliyet $15 → $5, yaklaşık 3 kat ucuz (slayt). | 9:46 | sayısal |
| CLAUDE.md her oturumda yüklenir; konuşmacı 2000 satırı geçmemesini önerir. | 15:00 | öneri |
| Rewind Anthropic'in en büyük önerisidir. | 7:32 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:00 | Claude Limitlerini Aş slaytı | Claude Code | Başlık ve mercan Claude maskotu. |
| konuşma 0:15 | Token kavramı | aday değil: genel kavram | Ajanın kalorisi benzetmesi. |
| konuşma 1:00 | Türkçe token maliyeti | aday değil: genel kavram | Türkçe karakterler token artırır. |
| konuşma 1:38 | API vs abonelik fiyatı | aday değil: genel kavram | 100 dolar karşılığı 2.500 dolarlık token. |
| kare 2:36 | Claude Sonnet kotası | Claude Sonnet | Sadece Sonnet satırı. |
| ekran 2:56 | claude.ai/settings | Claude Code | Kullanım limiti sayfası adresi; Claude ürünü. |
| konuşma 3:07 | Session/oturum | aday değil: genel kavram | Her oturumun ayrı hafızası. |
| konuşma 4:07 | Opus 4.7, 1M token | Claude Opus | Opus 4.7de 1 milyon token. |
| konuşma 4:47 | Context rot | aday değil: genel kavram | Bağlam dolunca hata artar. |
| kare 6:30 | /compact | /compact | Compacting... görünüyor. |
| kare 6:40 | /clear | /clear | Handoff adımı. |
| konuşma 6:50 | Codex | Codex | Sağ tarafta Codex var. |
| konuşma 6:50 | Gemini | Gemini | Cemina'ya veririm. |
| kare 7:58 | Rewind penceresi | Rewind | Rewind to... listesi. |
| kare 9:16 | /context | /context | Estimated usage tablosu. |
| kare 9:14 | Notion MCP araçları | Notion | mcp__claude_ai_Notion__ listesi. |
| kare 9:11 | frontend-design skill | frontend-design | Skills tablosu. |
| kare 9:11 | claude-api skill | claude-api | Skills tablosu. |
| kare 9:11 | update-config, keybindings-help, simplify, loop, schedule, security-review, review, init, self-improve | aday değil: konu dışı | Yalnız /context skill listesinde görünüyor, kullanılmadı. |
| konuşma 9:52 | Haiku alt ajan | Claude Haiku | Haiku ile araştır. |
| konuşma 9:52 | Sub-agent | Sub-agent | Alt ajan araştırma yaptı. |
| kare 10:40 | milx.app trend sayfası | aday değil: konu dışı | Web aramasında çıkan sonuç bağlantısı. |
| kare 10:48 | Plan mode | Plan modu | Modes listesi. |
| konuşma 10:55 | Bypass permissions | Bypass permissions | Genelde bypass diyoruz. |
| kare 12:02 | /btw | /btw | isn't available mesajı. |
| kare 12:00 | gh skill / Agent Skills yayınlama | aday değil: konu dışı | Haiku araştırma çıktısındaki trend maddesi. |
| kare 12:28 | MD dosyaları İngilizce | CLAUDE.md | Türkçe CLAUDE.md 3200 → 2200. |
| kare 13:00 | docling | docling | pip install docling. |
| konuşma 12:42 | Markdown, HTML, PDF, DOCX | Markdown | Format token karşılaştırması. |
| kare 13:44 | .claudeignore | .claudeignore | Büyük klasörleri dışla. |
| kare 15:18 | CLAUDE.md haritası | Ajan haritalama | agents/youtube/AGENT.md. |
| kare 16:32 | Skool topluluğu | Skool | Classroom ekranı. |
| kare 16:32 | AI Model / Openclaw kursu | aday değil: konu dışı | Yalnız Skool kurs kartı başlığında görünüyor. |
| kare 6:28 | Next/Tailwind/Framer/fal/Vercel sunum yığını | aday değil: konu dışı | Önceki oturumda üretilen farklı sunumun slayt listesi. |
| konuşma 0:00 | Cloud (Claude) kullanımı | Claude Code | Cloud limitleri = Claude limitleri. |
| açıklama | n8n, Qwen, ai agent etiketleri | aday değil: konu dışı | Yalnız açıklama etiketlerinde, videoda anlatılmıyor. |
| açıklama | Skool, kişisel site, e-kitap, podcast, sosyal profiller | aday değil: konu dışı | Tanıtım ve sosyal bağlantılar; Skool ayrıca aday. |
| yorum | Ruflo, Cursor, Kimi, MiniMax, VS Code | aday değil: konu dışı | Yalnız izleyici yorumlarında. |
| linkli sayfa | etkinlik.isgucyapayzeka.com | aday değil: konu dışı | Etkinlik tanıtım sayfası. |
## Kareden okunanlar
- 0:00: Slayt: 'Claude Limitlerini Aş', alt başlık 'Aynı işi on kat daha ucuza', 15 taktik · 3 grup · 30 dakika, sağda mercan maskot.
- 1:08: 'Build an AI agent' 4 token/17 karakter; 'Yapay zeka ajanı oluştur' 7 token/24 karakter.
- 1:16: 'Türkçe yazdığın her şey yaklaşık 2 kat pahalı', +75%.
- 2:28: $100 üyelik = $2.500 API; 'Aynı tokeni token başına ödeseydin 25 katı ödüyordun'.
- 2:36: Plan usage limits MAX (5x): 5 saatlik pencere %33, tüm modeller %21, Sadece Sonnet %0.
- 4:44: Context rot = AI bunaması; doğruluk %92 → %78; Mesaj 1: 500, 30: 15.500, 100: 180.000 token.
- 5:52: Auto-compact %95'te tetiklenir; manuel /compact %12-60 arasında.
- 7:24: Anthropic'in #1 önerisi: Esc Esc → rewind.
- 9:16: /context: System prompt 9.9k, MCP tools (deferred) 86.2k, Free space 923.3k (%92.3); Model: claude-opus-4-7[1m].
- 9:46: Sub-agent + Haiku: $15 → $5, 3x ucuz.
- 10:48: Modes: Ask before edits, Edit automatically, Plan mode, Auto mode, Bypass permissions.
- 12:28: Girdiyi Küçült: MD dosyalar İngilizce (3200 → 2200), Markdown dönüşümü, CLAUDE.md disiplini.
- 16:32: Skool 'İş Güç Yapay Zeka' Classroom; kurslar: Buradan Başla, İnşa Et, Satış Yap, AI Model / Openclaw vb.
## Belirsizlikler
- Sözlükte geçen Kling, Next.js, Tailwind CSS, Framer, Framer Motion, Vercel, Hermes Agent, TypeScript, Geist, Veo, OpenClaw, agent-skills yalnız bir ekran metninde veya arka planda geçiyor; videoda kullanıldıkları görülmediği için aday yapılmadı.
- Yorumlardaki Ruflo, Cursor, Kimi, MiniMax, VS Code yalnız yorumda; videoda anlatılmadı.
- Sunum içeriği bir önceki oturumda Claude ile üretilmiş; bu videoda yapılan iş değil, bu yüzden Next.js/Tailwind vb. aday sayılmadı.
- Slayt font adı ekrandan kesin okunamadı; 'Outfit' tahmindir.
- Slayttaki doğruluk %92→%78 ve $15→$5 rakamları konuşmacının slaytı, kaynağı belirtilmemiş.
- Konuşmacı '11 taktik' diyor, bölümlerde 6 başlık var; slaytta 15 taktik yazıyor.
- Altyazıda 'bypass' ve 'cloud' gibi kelimeler otomatik çeviri hataları (Claude kastediliyor).
## Atlanan segment oranı
0/23 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| claude.ai/settings | 2:56 | ekran | hayır |
| dorukyalcinsoy.com/My%20Drive/Agents/agents/youtube/outputs/2026-04-21_presentation_token-ustaligi.h | 8:50 | ekran | hayır |
| dorukyalcinsoy.com/My | 9:10 | ekran | hayır |
| https://milx.app/en/trends/video-conten | 10:40 | ekran | hayır |
| https://www.skool.com/is-guc-yapayzeka/classroom | 16:32 | ekran | evet |
| https://etkinlik.isgucyapayzeka.com | açıklama | açıklama | hayır |
| https://www.skool.com/is-guc-yapayzeka/about | açıklama | açıklama | hayır |
| https://dorukyalcinsoy.com/ | açıklama | açıklama | hayır |
| https://dorukyalcinsoy.com/e-kitap | açıklama | açıklama | hayır |
| https://dorukyalcinsoy.com/podcast | açıklama | açıklama | hayır |
| https://www.instagram.com/dorukyalcinsoy/ | açıklama | açıklama | hayır |
| https://www.linkedin.com/in/dorukyalcinsoy/ | açıklama | açıklama | hayır |
| https://x.com/dorukyalcinsoy | açıklama | açıklama | hayır |
| https://www.youtube.com/channel/UCJJrZm2OysRQJj5eWlIoSXQ?sub_confirmation=1 | açıklama | açıklama | hayır |
| https://www.skool.com/is-guc-yapayzeka | açıklama | açıklama | evet |
| medvi-redesign.dorukyalcinsoy.com | 9:04 | ekran | hayır |
## İş akışı
- 1. adım — Token kavramı ve Türkçe maliyet farkını slaytla anlatma — araçlar: Claude Code
- 2. adım — Plan kullanım limitleri ekranında 5 saatlik ve haftalık kotayı gösterme — araçlar: Claude Code, Claude Sonnet
- 3. adım — Yeni oturum açıp boş bağlamın dolmasını gösterme — araçlar: Claude Code
- 4. adım — Dolu oturumda /compact çalıştırma — araçlar: Claude Code, /compact
- 5. adım — Özet alıp /clear ile temiz oturuma geçmeyi anlatma — araçlar: Claude Code, /clear
- 6. adım — Rewind penceresiyle önceki mesaja geri dönme — araçlar: Claude Code, Rewind
- 7. adım — /context ile bağlam kullanımını denetleme — araçlar: Claude Code, /context
- 8. adım — Haiku alt ajanıyla Git ve YouTube trend araştırması yaptırma — araçlar: Claude Code, Claude Haiku, Sub-agent
- 9. adım — Plan modu ve izin modlarını gösterme — araçlar: Claude Code, Plan modu, Bypass permissions
- 10. adım — /btw ile yan soru deneme — araçlar: Claude Code, /btw
- 11. adım — MD dosyalarını İngilizce yazma ve docling ile Markdown'a çevirmeyi anlatma — araçlar: docling, Markdown
- 12. adım — CLAUDE.md, .claudeignore ve ajan haritasını anlatma — araçlar: CLAUDE.md, .claudeignore
- 13. adım — Skool topluluk sayfasını gösterip kapanış — araçlar: Skool
## Promptlar
- Ucuz modelle araştırma yaptırma — Git ve YouTube ile ilgili bu ayki trendleri alt ajan olarak Haiku ile araştır.
- /btw komutunu deneme — Yan soru olarak Türkiye'deki trendleri sor (/btw ile).
- Slayt örneği: alt ajan ile bağlamı hafif tutma — Auth akışını Haiku alt ajanı ile araştır, yalnız özet dön.
