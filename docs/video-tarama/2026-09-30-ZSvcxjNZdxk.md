# I Tried 100+ Claude Code Skills. These 6 Are The Best.
## Künye
I Tried 100+ Claude Code Skills. These 6 Are The Best. · Tech With Tim · süre: 19:19 · en-CA · https://youtu.be/ZSvcxjNZdxk
motor: parti 2026-09-30-uzun-6 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (8)
## Özet
Tech With Tim, Claude Code için en faydalı bulduğu 6 skill/araç'ı kurulum ve demolarla gösteriyor: gstack (Garry Tan'in 23 skill'lik yazılım geliştirme paketi), Hostinger MCP (terminalden VPS/site yayınlama, 118 araç), Firecrawl (ölçekli web crawl/scrape), Humanizer (AI metnini insansılaştırma), Composio (araçları tek yerden, isteğe bağlı keşifle bağlama) ve VibeSec (güvenlik denetimi skill'i). Kurulumların çoğu, repo/site talimatını Claude Code'a yapıştırıp 'bunu ekle' demekle yapılıyor.
## Bölümler
- 0:00 Genel bakış
- 0:16 1 - gstack
- 3:37 2 - Hostinger MCP
- 8:38 3 - Firecrawl
- 11:37 4 - Humanizer
- 12:48 5 - Composio
- 17:01 6 - VibeSec
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| gstack | yok | skill | https://github.com/garrytan/gstack | Garry Tan'in 23 skill'lik paketi; Claude Code'u sanal mühendislik ekibine çevirir (office-hours, plan-ceo-review, review, QA vb.). | 0:16 | this is a full repo called G stack which comes from Gary Tan... 23 different skills |
| Hostinger MCP + agent skills | yok | MCP | https://github.com/hostinger/api-mcp-server | Claude Code'dan VPS kurma, domain, DNS, site deploy; 118 araç sunar. Hostinger hesabı ve API token gerekir. | 5:40 | hosting our MCP is connected with 118 different tools |
| Firecrawl | yok | plugin | https://github.com/firecrawl/firecrawl-claude-plugin | Claude'un yerleşik web erişiminden daha iyi ölçekli crawl/scrape; skill dosyası ve CLI ile kurulur, ücretsiz kredi kotası var. | 8:38 | Fire Crawl allows your AI agent to crawl and scrape the web |
| Humanizer | yok | skill | https://github.com/blader/humanizer | Claude çıktısını daha insansı yapar; AI kalıplarını ve m-dash'i temizler. /humanizer ile kullanılır. | 11:37 | just make the output that Claude code gives you sound more like a human |
| Composio | yok | MCP | yok | Tüm uygulama bağlantılarını tek yerde tutar; Claude araçları isteğe bağlı keşfeder, token tasarrufu sağlar, makineler arası taşınır. | 12:48 | it can actually bloat the context quite quickly in Claude |
| VibeSec | yok | skill | https://github.com/BehiSecc/VibeSec-Skill | Kod tabanında güvenlik açıklarını denetler; build öncesi kurulursa Claude'a güvenli kod yazmayı öğretir. | 17:01 | stop vibe coding vulnerabilities into production |
| Claude Code auto mode | yok | ipucu | yok | Kurulum sırasında izin istemlerini Claude'un otomatik halletmesi için auto mode açıldı. | 1:18 | I also put auto mode on just so it can do everything itself |
| gstack /office-hours komutunu denemek için örnek proje tanımı. | yok | prompt | yok | hey I would like to build an internal accounting software for my YouTube business where I'm tracking invoices, expenses and the financial health | 2:20 | kaynak: altyazı |
| Hostinger API sayfasındaki MCP config'ini Claude Code'a eklemek. | yok | prompt | yok | add this MCP server to my configuration | 5:40 | kaynak: altyazı |
| Hostinger MCP ile site oluşturup yayınlama demosu. | yok | prompt | yok | can you create a super simple website that just says, hi, my name is Tim, and deploy that | 7:45 | kaynak: altyazı |
| Firecrawl ile ölçekli crawl demosu (/firecrawl ile). | yok | prompt | yok | go to the wiki company's directory and crawl every AI startup page and then extract the following | 9:39 | kaynak: altyazı |
| Composio CLI ile Gmail aracını test etmek. | yok | prompt | yok | grab my three most recent emails, but don't expose any sensitive data and give me a summary | 15:53 | kaynak: altyazı |
## Açıklama bağlantıları
- https://github.com/BehiSecc/VibeSec-Skill — VibeSec skill reposu · aday: evet (VibeSec) · Videoda 6. skill olarak gösteriliyor.
- https://github.com/blader/humanizer — Humanizer skill reposu · aday: evet (Humanizer) · Videoda 4. skill olarak gösteriliyor.
- https://github.com/firecrawl/firecrawl-claude-plugin — Firecrawl Claude plugin reposu · aday: evet (Firecrawl) · Videoda 3. araç olarak gösteriliyor.
- https://github.com/garrytan/gstack — gstack reposu · aday: evet (gstack) · Videoda 1. skill paketi.
- https://ref.wisprflow.ai/techwithtim — Wispr Flow referans bağlantısı (sponsor/ref) · aday: hayır · Videoda anlatılan skill değil, reklam/ref bağlantısı; sesli dikte aracı videonun konusu dışında.
- https://www.hostinger.com/techwithtim — Hostinger ortaklık bağlantısı · aday: evet (Hostinger MCP + agent skills) · Hostinger MCP için gereken hesap/plan bağlantısı; aday Hostinger MCP'ye bağlı (ortaklık linki).
- https://www.hostinger.com/techwithtim10 — Hostinger indirim bağlantısı · aday: hayır · Aynı ortaklık hizmetinin indirim varyantı; ayrı bir araç değil.
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| claude | Terminalde Claude Code'u başlatır. | 1:18 | altyazı |
| /office-hours | gstack'in ürün fikri sorgulama skill'ini çalıştırır. | 2:20 | altyazı |
| /plan-ceo-review, /plan-eng-review, /review, /qa | gstack'in plan, inceleme ve QA komutları (gösterilmedi, sadece anıldı). | 2:20 | altyazı |
| /new | Yeni oturum başlatır; MCP/skill yenilemek için. | 6:43 | altyazı |
| /mcp | MCP sunucularının bağlantı durumunu listeler. | 6:43 | altyazı |
| nvm install v24 && nvm use v24 | Hostinger MCP için gereken Node.js 24'ü kurar (README'de görünüyor). (karede: README'de 'nvm install v24' ve 'nvm use v24' komut kutusu) | 4:07 | kare |
| /firecrawl | Firecrawl skill'ini çağırır. | 9:39 | altyazı |
| /humanizer | Humanizer skill'iyle metni insansılaştırır. | 11:37 | altyazı |
| /vibe skill (VibeSec) | Kod tabanını güvenlik açıklarına karşı denetler; tam komut adı net değil. | 17:01 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| gstack 23 skill içerir; Y Combinator CEO'su Garry Tan'dan. | 0:16 | sayısal |
| Hostinger business planı aylık yaklaşık 4 dolardan başlar, 50 siteye kadar, ücretsiz domain; 'techwithtim' kodu 12+ ay planlarda ek %10 indirim. | 3:37 | sayısal |
| Hostinger MCP 118 araçla bağlandı. | 6:43 | sayısal |
| Firecrawl, yerleşik Claude web özelliklerinden daha hızlı ve ölçekli; demoda 300+ sayfa, ~10 dk, 312 kredi kullandı, 822 kaldı. | 10:41 | sayısal |
| Composio ücretsiz katmanda ayda yaklaşık 20.000 tool çağrısı sunar (konuşmacı emin değil). | 14:52 | sayısal |
| Composio araçları isteğe bağlı keşfettiği için yüzlerce aracı bağlamda tutmaktan daha token verimli ve doğru. | 13:49 | karşılaştırma |
| VibeSec build başlamadan önce kurulmalı; denetimde deploy edilmiş uygulamada çok sayıda açık bulundu. | 18:03 | öneri |
## Kareden okunanlar
- 0:08: Görsel verilmedi; yalnız konuşmacı ve 'FULL TUTORIAL' yazısı görülen kare (sıra 1).
- 0:47: gstack README: 'Twenty-three specialists and eight power tools', MIT lisansı; 'Tech leads and staff engineers' vurgulu.
- 1:49: Terminalde Claude Code v2.1.143, Opus 4.7 (1M context); auto mode bilgisi ve '[Pasted text #1]'.
- 2:52: Siyah ekran, alt kısımda sesli dikte göstergesi ve 'add gstack to the current project so teammates get it' metni.
- 3:30: github.com/garrytan/gstack skill tablosu: /office-hours, /plan-ceo-review, /plan-eng-review, /review, /investigate vb.
- 4:07: hostinger/api-mcp-server README: Node.js v24 gerekli, nvm install v24, nvm use v24.
- 5:09: Hostinger Business plan: 48 ay, $3.59/ay, ücretsiz domain, TECHWITHTIM kuponu -%10, toplam $191.33.
- 6:12: Hostinger API token sayfası: 'claudecode' (Never expires) token'ı, 'Copy your token' uyarısı (değer maskeli).
## Belirsizlikler
- Kare listesinde 8 zaman damgası var; ilk kare (0:08) ekli görsellerde ayrı değil gibi, eşleme kayması olabilir; kare okumaları bu yüzden yaklaşık.
- Altyazıda 'hosting or' gibi ifadeler Hostinger'ın yanlış transkripsiyonu sanılıyor.
- VibeSec komut adı ('vibe skill') transkripsiyondan net değil.
- Firecrawl ve Composio'nun tam kurulum komutları gösterilmedi/okunamadı (skill dosyası ve kopyalanan prompt yapıştırıldı).
- Composio kota ve fiyat bilgisi konuşmacının tahmini ('I think', 'or something').
- Wispr Flow bağlantısı videoda anlatılmıyor; sadece kare 2:52'deki dikte göstergesi ile ilişkili olabilir.
## Atlanan segment oranı
0/23 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
