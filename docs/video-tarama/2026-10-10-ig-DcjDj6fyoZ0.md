# Comment “DATA” and I’ll drop you the link to use it.
## Künye
Comment “DATA” and I’ll drop you the link to use it. · jackroberts___ · süre: 0:24 · ? · https://www.instagram.com/reel/DcjDj6fyoZ0/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-10-short-8 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 26585 tk · claude-haiku-5-5: claude-haiku-5-5 · 37694 tk
## Özet
Kısa reel: Scrapling adlı açık kaynak Python scraping kütüphanesi tanıtılıyor. İddiaya göre 700 kat daha hızlı, Cloudflare gibi bot korumalarını gerçek tarayıcı gibi görünerek geçiyor ve site değişince kendini onarıyor. Claude Code veya Codex'e bağlanıp canlı veri çekmek için kullanılabiliyor. Ekranda curl2fetcher, quotes.toscrape.com örneği, GitHub deposu ve Cloudflare MCP bağlayıcısı görülüyor. Video 'DATA' yorumuna link vaadiyle bitiyor.
## Bölümler
- 0:00 700 kat hız iddiası ve Scrapling tanıtımı
- 0:07 Site değişince klasik scraper'ların bozulması
- 0:11 Cloudflare Workflows ve ajan döngüsü görselleri
- 0:15 Cloudflare MCP bağlayıcısı ve Claude/Codex ile kullanım
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Scrapling | yok | teknik | yok | Açık kaynak Python scraping kütüphanesi; gerçek tarayıcı parmak izi taklidi ve kendini onaran seçiciler | 0:01 | Ekranda 'Scrapling', 'OPEN SOURCE', 'PYTHON' yazıyor; açıklamada Scrapling heals itself (karede: Kare 0:01: terminalde curl2fetcher kodu ve '700X' yazısı) |
| Claude Code | yok | CLI | yok | Scrapling'in bağlanabileceği kodlama ajanı | 0:00 | Just plug it into CloudCode or Codex |
| Codex | yok | CLI | yok | Scrapling'in bağlanabileceği diğer kodlama ajanı | 0:17 | Altyazıda 'Codex' görünüyor (karede: Kare 0:17: altyazı 'Codex', Claude izin penceresi (List Workers)) |
| Cloudflare | yok | teknik | yok | Bot koruma hizmeti; Scrapling'in geçtiği iddia edilen engel | 0:00 | walks straight past Cloudflare and any other service provider |
| Cloudflare Developer Platform | yok | MCP | yok | Claude'a Workers, KV, R2, D1 araçları sağlayan bağlayıcı | 0:15 | Connector URL bindings.mcp.cloudflare.com ve araç listesi · kanıt: kare (karede: Kare 0:15: 'Developer Platform', kv_namespaces_list, r2_bucket_get, d1_database_query etiketleri, Connector URL) |
| Cloudflare Workflows | yok | teknik | yok | Yeniden denemeli çok adımlı yürütme deseni | 0:11 | Ekran metni: Cloudflare Workflows, multi-step execution with retries |
| curl2fetcher | yok | teknik | yok | curl komutunu Scrapling fetcher'a çeviren işlev | 0:01 | curl2fetcher"""curl 'https://... komutu (karede: Kare 0:01: curl2fetcher ve -H başlıkları içeren terminal) |
| quotes.toscrape.com | yok | teknik | yok | Scraping demosunda kullanılan örnek site | 0:02 | Ekran günlüğü: Fetched (200) GET https://quotes.toscrape.com/ |
| GitHub | yok | teknik | yok | Scrapling deposunun gösterildiği servis | 0:04 | Ekran metni: 3 Branches, D4Vinci v0.4.14, agent-skill · kanıt: yok |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| curl 'https://quotes.toscrape.com/' -H 'accept-language: en-US,en;q=0.9' -H 'user-agent: Mozilla/5.0 ...' (başlıklar kırpılmış) | Tarayıcıdan kopyalanan isteği cURL olarak gösterir; hedef quotes.toscrape.com. (karede: Terminalde 'curl2fetcher"""curl 'https://quotes.toscrape.com/' \' ile başlayan çok satırlı -H başlıkları) | 0:01 | kare |
| curl2fetcher("""curl 'https://quotes.toscrape.com/' ...""") | cURL isteğini Scrapling fetcher çağrısına dönüştürür. (karede: Terminal satırında 'curl2fetcher"""curl 'https://quotes.toscrape.com/' ...' ifadesi) | 0:01 | kare |
| view(page) | Çekilen sayfayı tarayıcıda görüntüler. (karede: Terminalde pre çıktısının altında 'view(page)' satırı) | 0:01 | kare |
| page.css('.quote') | Sayfadaki .quote sınıflı alıntı öğelerini CSS seçiciyle seçer. (karede: 0:02 ekran metni (OCR), kare görseli gönderilmedi: page.css('.quote')) | 0:02 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Scrapling kullandığınız scraper'dan 700 kat daha hızlı | 0:00 | sayısal |
| Cloudflare ve diğer sağlayıcıların bot korumasını geçiyor | 0:00 | özellik |
| Site değişince kendini onarıyor, veriyi yine bulur | açıklama | özellik |
| Claude Code veya Codex'e takılıp canlı veri çeker | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı 0:00 | Scrapling | Scrapling | OCR: Scrapling, OPEN SOURCE, PYTHON |
| ekran 0:00 | Python | aday değil: başka adayın parçası (Scrapling) | OCR: PYTHON |
| altyazı 0:00 | Claude Code | Claude Code | plug it into CloudCode or Codex |
| altyazı 0:00 | Codex | Codex | or Codex |
| altyazı 0:00 | Cloudflare | Cloudflare | walks straight past Cloudflare |
| kare 0:01 | curl2fetcher | curl2fetcher | curl2fetcher"""curl 'https: |
| ekran 0:02 | quotes.toscrape.com | quotes.toscrape.com | Fetched (200) GET https://quotes.toscrape.com/ |
| ekran 0:04 | GitHub deposu | GitHub | 3 Branches, D4Vinci v0.4.14 |
| ekran 0:04 | agent-skill | aday değil: başka adayın parçası (Scrapling) | depo klasörü agent-skill |
| ekran 0:11 | Cloudflare Workflows | Cloudflare Workflows | Cloudflare Workflows, Durable apps |
| ekran 0:15 | Cloudflare Developer Platform MCP | Cloudflare Developer Platform | Connector URL bindings.mcp.cloudflare.com |
| ekran 0:15 | Anthropic | aday değil: konu dışı | Anthropic does not control which tools |
| ekran 0:17 | Claude izin penceresi | aday değil: başka adayın parçası (Claude Code) | Claude wants to use List Workers |
| açıklama | Hashtag'ler #cloudflare #claudecode #codex | aday değil: başka adayın parçası (Cloudflare) | #scrapling #webscraping #cloudflare #claudecode #codex |
| açıklama | Web scraping | aday değil: genel kavram | #webscraping |
## Kareden okunanlar
- 0:01: Terminalde curl2fetcher ve curl -H başlıkları; '700X' ve '700 times' yazıları
- 0:15: Cloudflare Developer Platform bağlayıcısı, araç etiketleri (kv_namespaces_list, r2_bucket_get, d1_database_query), Connector URL bindings.mcp.cloudflare.com
- 0:17: Claude 'List Workers' izin penceresi: Always allow, Deny, Allow once; altyazı 'Codex'
## Belirsizlikler
- Dil belirtilmemiş; altyazı İngilizce.
- Yorumlar girişsiz alınamadı; 'DATA' ile gelecek link görülemedi.
- Cloudflare MCP görüntüleri Scrapling ile ilgisi belirsiz stok/b-roll olabilir.
- Kare listesinde 0:07 ve 0:11 kareleri gönderilmedi; yalnız OCR ile okundu.
- Scrapling'in Claude Code'a nasıl bağlandığı gösterilmedi.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://quotes.toscrape.com/ | 0:02 | ekran | hayır |
| https://bindings.mcp.cloudflare.com | 0:15 | ekran | evet |
| bindings.mcp.cloudflare.com/mcp | 0:16 | ekran | evet |
## İş akışı
- 1. adım — Konuşmacı Scrapling'i tanıtır ve Claude Code ya da Codex'e takılıp agent'ların canlı veri çekebileceğini anlatır (anlatım, ekranda kurulum yok) — araçlar: Claude Code, Codex, Scrapling
- 2. adım — Tarayıcıdan alınan cURL isteğini curl2fetcher ile Scrapling fetcher çağrısına dönüştürme — araçlar: curl2fetcher, Scrapling
- 3. adım — Çekilen sayfayı view(page) ile görüntüleme — araçlar: Scrapling
- 4. adım — quotes.toscrape.com adresine istek atılır; 200 yanıtı alınır — araçlar: Scrapling
- 5. adım — page.css('.quote') ile alıntı öğelerini CSS seçiciyle çekme — araçlar: Scrapling
- 6. adım — Oturumun kaydedilmesi (Saving session...completed) — araçlar: Scrapling
- 7. adım — Site değişimi demosu: taşınan div ve yeniden adlandırılan class ile seçicinin kırılması (anlatım, kendini onarma iddiası) — araçlar: Scrapling
- 8. adım — 403 CAPTCHA duvarı ve bot kontrolü gösterimi (anlatım, bypass iddiası) — araçlar: yok
- 9. adım — Cloudflare Workflows başlığı ve kullanım alanlarının gösterimi (yalnız ekran) — araçlar: Cloudflare Workflows
- 10. adım — Agent döngüsü (plan → tool call → reason → repeat) açıklaması — araçlar: yok
- 11. adım — Cloudflare Developer Platform sayfasını açma ve Connector URL'yi (bindings.mcp.cloudflare.com) gösterme — araçlar: Cloudflare Developer Platform
- 12. adım — Claude arayüzünde araçların yüklenmesi (Loading tools) — araçlar: Cloudflare Developer Platform, Claude arayüzü
- 13. adım — List Workers aracı için izin verme (Allow once / Always allow) — araçlar: Cloudflare Developer Platform, Claude arayüzü
- 14. adım — List Workers çağrısının çalışması (Working) ve canlı veri çekme gösterimi — araçlar: Cloudflare Developer Platform, Claude arayüzü
## Promptlar
- yok
ikinci göz KAPALI: --ikinci-goz yok
