# Claude Code ile Meta Reklamlarını Analiz Et: Kazanan Reklamı Bul
## Künye
Claude Code ile Meta Reklamlarını Analiz Et: Kazanan Reklamı Bul · Burhan KOCABIYIK · süre: 19:00 · tr-orig · https://youtu.be/Xv9GJZSMCPU · şema 2
motor: parti 2026-10-09-short-9 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (59)
kareler: girdi ≤40000 jeton için 60→59
claude-sonnet-5-5: claude-sonnet-5-5 · 66480 tk · claude-haiku-5-5: claude-haiku-5-5 · 113205 tk
## Özet
Burhan Kocabıyık, Claude Code'u Meta Reklam Kütüphanesi verisiyle ve kendi reklam hesabıyla birleştirerek hangi reklamların tuttuğunu bulmayı gösteriyor. Uzun süre aktif olan ve çok varyasyonu olan reklam tutmuş sayılıyor. Veriyi Apify (facebook-ads-scraper) ve Firecrawl ile çekiyor, Claude Code'u VS Code terminalinde çalıştırıyor, Photoroom reklamlarını HTML rapora döküyor. Kazanan reklamın varyasyonlarını yapay zekâyla üretmeyi anlatıyor. Meta hesabını Marketing API/MCP ya da Composio ile bağlıyor. Son bölümde reklamı durmuş işletmelere hizmet satma yöntemini ve Leads Finder ile lead çıkarmayı gösteriyor.
## Bölümler
- 0:00 Giriş
- 1:25 Tutan Reklam Nasıl Anlaşılır
- 2:47 Örnek: Halı Yıkama Reklamları
- 4:04 Firecrawl Kurulumu
- 5:54 Apify Kurulumu
- 6:48 Claude Code Kurulumu
- 8:39 Maliyet ve Reklam Analizi
- 10:42 Kazanan Reklamın Varyasyonları
- 12:11 Meta Hesabını Claude'a Bağlama
- 14:53 Reklamı Durmuş Şirketlere Satış
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Analizi yapan ve komutları çalıştıran ana yapay zekâ aracı; VS Code terminalinde çalışıyor. | 7:20 | Terminalde 'claude' yazılıp Claude Code başlatılıyor. (karede: Terminalde 'arspar@Mac business1 % claude' ve Claude Code V2.1.287 başlığı görünüyor.) |
| Meta Ads Library | yok | iş akışı | yok | Herkese açık reklam kütüphanesi; aktiflik ve süreye bakarak kazanan reklam bulunuyor. | 0:36 | Meta panelinde bütün reklamlar herkese açık, reklam ne kadar açık kaldığına bakılıyor. |
| Apify | yok | iş akışı | yok | Reklam verisini kütüphaneden çeken scraper platformu; API token ile Claude'a bağlanıyor. | 5:44 | Apify Store'da 'ads' araması ve API & Integrations sayfası gösteriliyor. (karede: console.apify.com/store-search?search=ads sayfası; sol menüde Apify Store, Actors, Integrations.) |
| apify/facebook-ads-scraper | yok | iş akışı | yok | Meta reklamlarını çeken resmi Apify actor'ü; Photoroom için limit 5 ile kullanıldı. | 8:14 | Actor sayfasında Facebook Ads Library Scraper, from $5.00 / 1,000 ads yazıyor. (karede: Facebook Ads Library Scraper, apify/facebook-ads-scraper, fiyat 'from $5.00 / 1,000 ads'.) |
| Firecrawl | yok | MCP | yok | Web ve reklam verisi toplayan servis; MCP ile anahtarsız kurulabiliyor. | 4:04 | Kullandığım bir sistem var, ismi Firecrawl; API anahtarıyla kuruluyor. |
| Composio | yok | MCP | yok | Meta Reklamlar'ı Claude'a bağlayan platform; MCP URL ve API anahtarı ile. | 12:30 | Composio Connect Agents sayfasında Claude Code, MCP URL ve CLI kurulumu var. (karede: dashboard.composio.dev Connect Agents: Claude Code, MCP URL connect.composio.dev/mcp, 'Use Composio via CLI'.) |
| Visual Studio Code | yok | iş akışı | yok | Claude Code'u terminalinde çalıştırdığı editör; eklenti yerine terminal öneriliyor. | 6:24 | VS Code karşılama ekranı ve terminal görünüyor. (karede: Visual Studio Code 'Editing evolved' karşılama ekranı, Recent listesi.) |
| Meta Marketing API | yok | MCP | yok | Kendi reklam hesabını bağlamak ve kampanya kurmak için yöntem 1; MCP ile Claude'a bağlanır. | 12:11 | Pazarlama API'ını alıyorsunuz... MCP ile cloud birbirine bağlıyor. · kanıt: yok |
| Leads Finder | yok | iş akışı | yok | Apify actor'ü; web sitesinden şirket, çalışan ve e-posta bilgisi çıkarıyor. | 17:00 | Leads Finder $1.5/1k leads with Emails actor sayfası gösteriliyor. · kanıt: kare (karede: Apify'da '✨Leads Finder - $1.5/1k leads with Emails [Apollo Alternative]', code_crafter/leads-finder.) |
| Photoroom | yok | iş akışı | yok | Analiz örneği olarak reklamları çekilen uygulama. | 7:52 | Photoroom uygulamasının reklamlarını 5 tane çek. |
| Opus 5.5 | yok | iş akışı | yok | Claude Code'un çalıştığı model. | 7:22 | Başlıkta 'Opus 5.5 with high effort · Claude Max' yazıyor (OCR). (karede: Kare listesinde 7:22 yok; en yakın kare 7:12/7:28, OCR metninden okundu.) |
| Higgsfield | yok | MCP | yok | Varyasyon üretim planında geçen görsel/video üretim MCP'si. | 0:54 | Akış kartlarında 'üretim plan. → Higgsfield' yazıyor (OCR). (karede: 0:54 karesi: 5 bölümlük yol haritası slaytı; Higgsfield OCR'dan okundu.) |
| ElevenLabs | yok | teknik | yok | Gösterilen örnek raporda karakter zaman damgası için anılıyor. | 9:08 | OCR: ElevenLabs'in karakter zaman damgalarından üretildi. (karede: 9:08 karesi: sahne dizimi içeren HTML sayfa.) |
| Meta Reklam Kütüphanesi | yok | teknik | yok | Meta'nın herkese açık reklam arama sayfası; ülke, aktif durum, platform ve tarih filtreleriyle reklam arar. | 2:36 | facebook.com/ads/library: ülke Türkiye, 'halı yıkama', ~1.600 sonuç, filtre 'Aktif' (karede: Meta Reklam Kütüphanesi arama sonuçları; 'Aktif Durum: Aktif Reklamlar' filtresi ve ~1.600 sonuç yazısı.) |
| Google Ads Scraper | yok | teknik | yok | Google Ads Transparency Center'daki reklamları çeken Apify actor'ü (silva95gustavo/google-ads-scraper). | 5:50 | Extract up to 400 ads per minute along with text, image and video ads (karede: Apify Store aramasında 'Google Ads Scraper' kartı; 4.9 puan ve açıklama metni görünüyor.) |
| Meta Ads MCP | yok | MCP | yok | Meta reklam hesabına Claude üzerinden erişen MCP; Composio'da 'Facebook ads' custom connector olarak eklenir; işlemler onay ister. | 13:34 | custom connector 'Facebook ads' + Meta'nun MCP adresi; izinler 'needs approval' (karede: Slayt: 'Kampanyayı kur' ve 'CEVAPLARI' bölümü; 'Meta Ads MCP' adresi ve 'needs approval' izin notu yazılı (OCR).) |
| chrome-devtools | yok | MCP | yok | Claude Code'un Chrome'u kontrol edip hazırlanan HTML sayfasının ekran görüntüsünü alması için çağırdığı araç. | 10:44 | Calling chrome-devtools… · kanıt: kare (karede: Claude Code terminalinde 'Calling chrome-devtools…' ve 'Sayfanın doğru göründüğünü kontrol etmek için tarayıcıda açıp ekran görüntüsü alıyorum' satırları.) |
| Facebook Marketplace | yok | teknik | yok | Yerel işletmelere hizmet teklifi göndermek için kullanılan ilan ve mesajlaşma kanalı. | 14:53 | Facebook Marketplace'ten DM olarak atabilirsiniz. |
| Apify bağlantısını test etme | yok | prompt | yok | Apify ile reklam verisi çekeceğiz, çalışıyor mu kontrol et; Photoroom uygulamasının 5 reklamını çek. | 7:52 | kaynak: kare |
| Meta hesabı verisiyle reklam analizi | yok | prompt | yok | Tüm reklamlarıma bak, hangileri tutmuş/tutmamış; rakipleri analiz et, tutabilecek içerikleri nedenleriyle çıkar, benzerlerini üret. | 13:12 | kaynak: altyazı |
| Durmuş reklam veren müşteri adayı bulma | yok | prompt | yok | Reklam vermiş ama şimdi vermeyen, en az 20 çalışanlı e-ticaret şirketlerini bul, reklamlarına bak, e-postalarını bul; Apify kullan. | 16:54 | kaynak: altyazı |
## Açıklama bağlantıları
- https://skool.com/doa/about — Yazarın Skool topluluğu · aday: hayır · Topluluk sayfası; erişilemez. · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- https://skool.com/doa-zero/about — Skool topluluğu, araç linkleri · aday: hayır · Topluluk sayfası; erişilemez. · sınıf: diğer · erişilemez: ücretli topluluk, giriş gerekli
- https://youtu.be/cnnDG0pPkTk — Önerilen ilgili video · aday: hayır · İzleme önerisi, araç değil. · sınıf: diğer
- https://youtu.be/AkYbv-5Ro_A — Önerilen ilgili video · aday: hayır · İzleme önerisi, araç değil. · sınıf: diğer
- https://youtu.be/N4s51kudOhQ — Önerilen ilgili video · aday: hayır · İzleme önerisi, araç değil. · sınıf: diğer
- https://youtu.be/F0PIbAXhujs — Önerilen ilgili video · aday: hayır · İzleme önerisi, araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl -fsSL https://claude.ai/install.sh / bash | Claude Code yükleyicisini indirip çalıştırır. (karede: Claude Code Docs sayfasında 'Install Claude Code' altında bu komut görünüyor.) | 7:36 | kare |
| claude | Claude Code'u terminalde başlatır. (karede: Terminalde 'arspar@Mac ~ % claude' ve güvenlik sorusu görünüyor.) | 6:52 | kare |
| curl -fsSL https://composio.dev/install / sh | Composio CLI'ı kurar. (karede: Composio Connect Agents sayfasında 'Use Composio via CLI' kutusunda komut görünüyor.) | 13:04 | kare |
| /plugin | Kullanılmayan eklentileri devre dışı bırakma ipucu olarak ekranda anılıyor. (karede: Terminalde 'Tip: You have 2 plugins you haven't used lately. Disable them with /plugin'.) | 11:34 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| 1000 reklam çekmek 5 dolar tutuyor. | 8:39 | sayısal |
| Uzun süre aktif ve çok varyasyonlu reklam tutmuş reklamdır; aktif olmayan kısa ömürlüdür. | 1:25 | öneri |
| Yazar, 20+ yazılımla yaklaşık 400.000 Euro gelir elde ettiklerini söylüyor. | açıklama | sayısal |
| Claude Code'u VS Code eklentisi yerine terminalde kullanmak öneriliyor. | 6:48 | öneri |
| Apify'da bir ücretsiz paket veriliyor; Apify için topluluğa indirim var, başka partnerlik yok. | 5:54 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Code | Claude Code | Cloud kode ve meta panelini birleştirdiğinizde |
| konuşma 1:25 | Meta Reklam Kütüphanesi | Meta Ads Library | Aktif ve uzun süredir yayında reklam |
| konuşma 4:04 | Firecrawl | Firecrawl | Kullandığım bir sistem var, Firecrawl |
| konuşma 5:54 | Apify | Apify | Apify kullanıyorum, indirimimiz var |
| kare 8:14 | apify/facebook-ads-scraper | apify/facebook-ads-scraper | Facebook Ads Library Scraper sayfası |
| kare 6:24 | Visual Studio Code | Visual Studio Code | VS Code karşılama ekranı |
| konuşma 12:11 | Composio | Composio | Kompozy platformu, Meta reklamlar |
| konuşma 12:11 | Meta Marketing API | Meta Marketing API | Pazarlama API'ını alıyorsunuz |
| kare 17:00 | Leads Finder | Leads Finder | Apify Leads Finder actor sayfası |
| konuşma 7:52 | Photoroom | Photoroom | Photoroom uygulamasının reklamları çekiliyor |
| kare 7:22 (OCR) | Opus 5.5 | Opus 5.5 | Opus 5.5 with high effort · Claude Max |
| ekran 0:54 | Higgsfield | Higgsfield | üretim plan. → Higgsfield |
| ekran 9:08 | ElevenLabs | ElevenLabs | ElevenLabs karakter zaman damgaları |
| konuşma 2:47 | ChatGPT | aday değil: konu dışı | Görselleri chat piti ile değiştirdim |
| ekran 0:08 | Codex | aday değil: konu dışı | Kurulum panelinde menü öğesi |
| ekran 12:30 | Notion, Slack, Linear, Perplexity, Discord | aday değil: konu dışı | Composio uygulama listesinde menü öğeleri |
| ekran 12:48 | GitHub, Grok, Cursor | aday değil: konu dışı | Composio listesinde görünen öğeler |
| ekran 7:28 | Supabase, Claude Design, Claude Desktop | aday değil: konu dışı | Google arama önerileri ve kısayollar |
| açıklama | skool.com/doa/about ve doa-zero | aday değil: konu dışı | Topluluk sayfası |
| açıklama | YouTube önerilen videolar (4 adet) | aday değil: konu dışı | İzleme önerisi bağlantıları |
| yorum | Hermes Agent, Opencode | aday değil: konu dışı | İzleyici soruları |
| konuşma 15:53 | Facebook Marketplace DM | aday değil: genel kavram | Marketplace'ten DM atabilirsiniz |
## Kareden okunanlar
- 0:08: 'YENİ VERİ' başlığı; Claude/Codex kurulum paneli ve 'ANALİZ SONUCU – ÖNE ÇIKAN: REKLAM B' grafiği.
- 5:44: Apify Store 'ads' araması, sol menüde Actors, Runs, Integrations.
- 7:36: Claude Code Docs kurulum komutu: curl -fsSL https://claude.ai/install.sh / bash.
- 8:14: Facebook Ads Library Scraper, apify/facebook-ads-scraper, from $5.00 / 1,000 ads.
- 12:58: Composio General: Enhanced Control BETA; Claude Code, Codex, Cursor destekli.
- 17:00: Leads Finder actor: 'Users on the free Apify plan can fetch up to 100 leads per run.'
## Belirsizlikler
- Ekranda görünen Apify API token değeri yazılmadı; ayrıca yeni anahtar üretilip eskisinin silineceği söyleniyor.
- Videoda gösterilen çoğu slayt başka bir video ve 'Sam Piliero' içeriğine atıf yapıyor; bunlar aday olarak alınmadı.
- Altyazıda 'Epify' ve 'Firecroll' olarak yazılan adlar Apify ve Firecrawl olarak düzeltildi.
- Opus 5.5 ve Claude Max yalnızca OCR'dan okundu, kare listesinde tam zamanı yok.
- Yorumdaki Hermes Agent ve Opencode sadece izleyici sorusu, videoda kullanılmadı.
- Menüde görünen Supabase, Claude Design vb. kullanılmadı; adaylara alınmadı.
## Atlanan segment oranı
0/24 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| facebook.com/ads/library | 2:36 | ekran | evet |
| firecrawl.dev | 3:36 | ekran | evet |
| docs.firecrawl.dev/mcp-server | 3:38 | ekran | evet |
| console.apify.com/store-search?search=ads | 5:44 | ekran | evet |
| console.apify.com/settings/integrations | 6:08 | ekran | evet |
| code.claude.com/docs/en/terminal-guide | 7:34 | ekran | evet |
| https://claude.ai/install.sh | 7:36 | ekran | evet |
| console.apify.com/actors/JJghSZmShuco4j9gJ/info/readme?build=latest | 8:14 | ekran | evet |
| composio.dev | 12:24 | ekran | evet |
| https://connect.composio.dev/mcp | 12:48 | ekran | evet |
| https://composio.dev/install | 13:04 | ekran | evet |
| developers.facebook.com/docs/marketing-apis | 13:34 | ekran | evet |
| console.apify.com/actors/loSHqwTR9YGhzccez?addFromActorld=loSHqwTR9YGhzccez | 16:48 | ekran | evet |
| https://skool.com/doa-zero/about | açıklama | yorum | hayır |
| https://skool.com/doa/about | açıklama | açıklama | hayır |
| https://youtu.be/cnnDG0pPkTk | açıklama | açıklama | hayır |
| https://youtu.be/AkYbv-5Ro_A | açıklama | açıklama | hayır |
| https://youtu.be/N4s51kudOhQ | açıklama | açıklama | hayır |
| https://youtu.be/F0PIbAXhujs | açıklama | açıklama | hayır |
| https://itunes.apple.com | 0:12 | ekran | hayır |
| https://www.pazaramatatil.com | 2:48 | ekran | hayır |
| https://github.com/firecrawl/firecrawl | 3:48 | ekran | evet |
| https://api.apify.com/v2/users/me | 8:00 | ekran | evet |
| https://photoroom.com | 10:48 | ekran | hayır |
| https://dashboard.composio.dev/dda/-/connect/apps | 12:38 | ekran | evet |
| https://chatgpt.com | 12:58 | ekran | hayır |
| https://console.apify.com/store | 16:44 | ekran | evet |
| https://gmail.com | 17:00 | ekran | hayır |
## İş akışı
- yok
## Promptlar
- Apify bağlantısını test etme — Apify ile reklam verisi çekeceğiz, çalışıyor mu kontrol et; Photoroom uygulamasının 5 reklamını çek.
- Meta hesabı verisiyle reklam analizi — Tüm reklamlarıma bak, hangileri tutmuş/tutmamış; rakipleri analiz et, tutabilecek içerikleri nedenleriyle çıkar, benzerlerini üret.
- Durmuş reklam veren müşteri adayı bulma — Reklam vermiş ama şimdi vermeyen, en az 20 çalışanlı e-ticaret şirketlerini bul, reklamlarına bak, e-postalarını bul; Apify kullan.
ikinci göz KAPALI: --ikinci-goz yok
