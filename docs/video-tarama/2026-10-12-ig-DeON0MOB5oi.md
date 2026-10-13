# This is how I made my agents native browser use so fast and efficient
## Künye
This is how I made my agents native browser use so fast and efficient · charles.zhengg · süre: 0:36 · ? · https://www.instagram.com/reel/DeON0MOB5oi/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-12-short-2 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 33415 tk · claude-haiku-5-5: claude-haiku-5-5 · 107830 tk
## Özet
Charles Zheng, 'API Anything' adlı açık kaynak depoyu tanıtıyor. Depo, bir sitenin ağ trafiğini tersine mühendislikle çözüp siteyi ajan için API'ye çeviriyor. Böylece LinkedIn, Reddit gibi sitelerde tarayıcı sürmek gerekmiyor. Google Flights karşılaştırmasında tarayıcı ajanı 23 sn, 0,150 $ ve 11 araç çağrısı harcıyor. Anlatıcıya göre süre ve maliyet %50 düşüyor. Kurulum, ajana bir GitHub INSTALL.md bağlantısı verilerek yapılıyor.
## Bölümler
- 0:00 API Anything deposunun tanıtımı
- 0:02 README: siteyi bir kez öğret, sonra API gibi çağır
- 0:03 Ağ trafiği (Network) ve operasyon öğrenme
- 0:11 Claude Code'a kurulum ve tersine mühendislik promptları
- 0:19 Google Flights: tarayıcı ajanı ile api-anything MCP karşılaştırması
- 0:25 Benchmark: yanıt süresi (5 tarih, 5 çalıştırma medyanı)
- 0:33 Profil ve bio bağlantıları
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| API Anything | yok | CLI | github.com/goodnight000/api-anything | Sitenin ağ trafiğini tersine mühendislikle çözüp operasyon olarak kaydeder; ajan siteyi MCP, CLI veya TypeScript ile API gibi çağırır. | 0:00 | This repo can turn any website into an API for your agents (karede: GitHub deposu api-anything; .claude-plugin, bench, docs klasörleri, README, INSTALL.md, AGENTS.md dosyaları) |
| Claude Code | yok | CLI | yok | Kurulum ve tersine mühendislik promptlarının yazıldığı ana yapay zekâ aracı. | 0:10 | Ekran metni 'Claude Code' ve 'Set up API Anything for me' promptu (karede: Gönderilen karelerde (0:00, 0:01, 0:33) Claude Code ekranı yok; yalnız OCR'da 0:10'da görünüyor) |
| Playwright MCP | yok | MCP | yok | Karşılaştırmada tarayıcı ajanının headless Chrome'u sürmek için kullandığı MCP. | 0:19 | OCR: Playwright MCP driving headless Chrome (karede: Gönderilen karelerde yok; yalnız OCR metni) |
| MCP | yok | teknik | yok | API Anything operasyonlarının ajana sunulduğu protokol; karşılaştırmada 'api-anything MCP, no browser'. | 0:02 | OCR: calls that operation with new inputs over MCP, the CLI or TypeScript (karede: Gönderilen karelerde yok; yalnız OCR metni) |
| Google Flights | yok | teknik | yok | Karşılaştırma görevinde SFO-JFK uçuşları için kullanılan site. | 0:19 | Open page google.com/travel/flights?q=Flights from SFO to JFK (karede: Gönderilen karelerde yok; yalnız OCR metni) |
| TypeScript | yok | teknik | yok | API Anything'in dili ve ajanın operasyonları çağırma yollarından biri. | 0:01 | Depo dil çubuğunda TypeScript 93.9% (karede: Kare 0:01: sağda Languages bölümünde TypeScript ve JavaScript çubuğu) |
| JavaScript | yok | teknik | yok | Depoda küçük oranda kullanılan dil. | 0:01 | Depo dil çubuğunda JavaScript 5% (karede: Kare 0:01: Languages bölümünde JavaScript) |
| cstack | yok | skill | github.com/goodnight000/cstack | Anlatıcının profilinde 'My skills' altında gösterilen başka bir depo. | 0:34 | OCR: github.com/goodnight000/cstack (karede: Gönderilen karelerde yok; yalnız OCR metni) |
| Headless Chrome | yok | teknik | yok | Playwright MCP'nin sürdüğü arka planda çalışan Chrome tarayıcısı. | 0:19 | OCR: Playwright MCP driving headless Chrome (karede: kanıttan) OCR: Playwright MCP driving headless Chrome |
| API Anything kurulumu | yok | prompt | yok | Ajana API Anything'i kurmasını söyler ve INSTALL.md GitHub bağlantısını verir. | 0:11 | kaynak: kare |
| LinkedIn API'sini tersine mühendislik | yok | prompt | yok | Ajandan LinkedIn'in API'sini tersine mühendislikle çıkarmasını ister. | 0:13 | kaynak: kare |
## Açıklama bağlantıları
- yok
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| Set up API Anything for me: https://github.com/goodnight000/api-anything/blob/main/INSTALL.md | Claude Code'a API Anything'i INSTALL.md'ye göre kurdurur. (karede: (karede OCR) Claude Code * Set up API Anything for me: https://github. com/goodnight0o0/api-anything/blob/mai to your) | 0:11 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Tarayıcı eylemlerini API çağrısına çevirmek ajanın görev süresini %50, maliyetini %50 azaltır. | 0:00 | sayısal |
| Tarayıcı ajanı Google Flights görevini 23,0 sn, 0,150 $ ve 11 araç çağrısıyla bitirdi. | 0:23 | sayısal |
| Ücretli API'ler yerine herhangi bir siteyi ajan için API'ye çevirmek mümkündür. | 0:00 | özellik |
| Tarayıcı erişimi açık olmalı; en çok tarayıcı kullanan otomatik iş akışlarında işe yarar. | 0:00 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | API Anything deposu | API Anything | This repo can turn any website into an API |
| konuşma 0:00 | LinkedIn | aday değil: genel kavram | LinkedIn veya Reddit için API ödemek gerekmez |
| konuşma 0:00 | Reddit | aday değil: genel kavram | Reddit pazarlama otomasyonu |
| konuşma 0:00 | Tarayıcı erişimi | aday değil: genel kavram | Ajanın tarayıcı erişimi açık olmalı |
| kare 0:00 | .claude-plugin klasörü | API Anything | Depo klasör listesinde .claude-plugin |
| kare 0:01 | TypeScript | TypeScript | Languages: TypeScript |
| kare 0:01 | JavaScript | JavaScript | Languages: JavaScript |
| ekran 0:02 | MCP | MCP | over MCP, the CLI or TypeScript |
| ekran 0:03 | Network paneli (UserByScreenName, main.js vb.) | API Anything | Network 767 requests |
| ekran 0:10 | Claude Code | Claude Code | Claude Code başlığı |
| ekran 0:11 | GitHub INSTALL.md bağlantısı | API Anything | Set up API Anything for me |
| ekran 0:19 | Playwright MCP | Playwright MCP | Playwright MCP driving headless Chrome |
| ekran 0:19 | Google Flights | Google Flights | google.com/travel/flights |
| ekran 0:09 | airbnb | aday değil: genel kavram | Site listesinde airbnb |
| ekran 0:33 | getforth.co | aday değil: konu dışı | Profil bio bağlantısı |
| ekran 0:34 | cstack deposu | cstack | github.com/goodnight000/cstack |
| ekran 0:33 | Instagram profili | aday değil: konu dışı | charles.zhengg profil ekranı |
## Kareden okunanlar
- 0:00: GitHub deposu goodnight000/api-anything (Public); .claude-plugin, bench, docs klasörleri; altyazı 'This repo'.
- 0:01: AGENTS.md, CONTRIBUTING.md, INSTALL.md, LICENSE, README.md, package.json, tsconfig.json; katkıda bulunanlar goodnight000 ve claude; TypeScript ve JavaScript; 'API Anything' başlığı.
- 0:33: Instagram profili charles.zhengg; Charles Zheng, CMU ECE+Robotics, getforth.co, 9 gönderi, 1.071 takipçi, 795 takip; son 30 günde 219,7K görüntülenme.
## Belirsizlikler
- Google Flights karşılaştırma kareleri gönderilmedi; sayılar yalnız OCR'dan.
- Reddit ve LinkedIn yalnız örnek olarak anıldı; araç olarak gösterilmedi.
- Altyazıda 'Make' ve 'agentsby' sözlük eşleşmeleri bulanık; aday yapılmadı.
- Repo adresi OCR'da goodnight000 ve goodnight0o0 olarak farklı okunuyor.
- Yorumlar girişsiz alınamadı.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.instagram.com/reel/DeON0MOB5oi/ | açıklama | açıklama | hayır |
| https://google.com/travel/flights?q=Flights | 0:19 | ekran | evet |
| getforth.co | 0:33 | ekran | hayır |
| github.com/goodnight000/api-anything | 0:34 | ekran | evet |
| github.com/goodnight000/cstack | 0:35 | ekran | evet |
| github.com/goodnight000/api-anything/blob/main/INSTALL.md | 0:11 | ekran | evet |
| https://google.com | 0:19 | ekran | hayır |
## İş akışı
- 1. adım — API Anything deposunu GitHub'da göstermek — araçlar: API Anything, GitHub
- 2. adım — Ajanda tarayıcı erişimini açmak — araçlar: Claude Code
- 3. adım — Kurulum promptunu INSTALL.md bağlantısıyla vermek — araçlar: Claude Code, API Anything
- 4. adım — Ajandan LinkedIn API'sini tersine mühendislikle çıkarmasını istemek — araçlar: Claude Code, API Anything
- 5. adım — Tarayıcı ajanıyla Google Flights aramasını çalıştırmak — araçlar: Playwright MCP, Google Flights
- 6. adım — api-anything MCP ile aynı aramayı tarayıcısız çalıştırmak — araçlar: API Anything, MCP, Google Flights
- 7. adım — Süre, maliyet ve araç çağrısını karşılaştırmak — araçlar: API Anything, Playwright MCP
## Promptlar
- API Anything kurulumu — Ajana API Anything'i kurmasını söyler ve INSTALL.md GitHub bağlantısını verir.
- LinkedIn API'sini tersine mühendislik — Ajandan LinkedIn'in API'sini tersine mühendislikle çıkarmasını ister.
ikinci göz KAPALI: --ikinci-goz yok
