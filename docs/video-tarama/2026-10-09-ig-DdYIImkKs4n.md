# Yorumlara “FABLE” yaz, sızdırılan sistem komutunu göndereyim.
## Künye
Yorumlara “FABLE” yaz, sızdırılan sistem komutunu göndereyim. · theakselege · süre: 0:21 · ? · https://www.instagram.com/reel/DdYIImkKs4n/ · platform: instagram · tür: reel · yorum: girişsiz alınamıyor · şema 2
motor: parti 2026-10-09-short-29 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (3)
claude-sonnet-5-5: claude-sonnet-5-5 · 15656 tk · claude-haiku-5-5: claude-haiku-5-5 · 102995 tk
## Özet
Kısa reel: Anthropic'in Claude Fable 5 sistem komutunun GitHub'da (asgeirtj/system_prompts_leaks) sızdırıldığı söyleniyor. Anlatıcıya göre komut tek satırla herhangi bir modele (Opus, Sonnet, Haiku) enjekte edilip Fable gibi davranması sağlanabiliyor. Gerçek kurulum satırı gösterilmiyor; yorumlara 'FABLE' yazana komut gönderileceği söyleniyor. Arka planda Claude Code oturumları, 3B deniz feneri modelleme ve GitHub sayfası görülüyor.
## Bölümler
- 0:00 Fable 5 sistem komutunun sızdırıldığı duyurusu
- 0:04 Modele enjekte etme ve Claude Code örnek ekranları
- 0:12 GitHub'daki sızdırılmış claude-fable-5.md dosyası
- 0:15 Model seçimi (Haiku, Sonnet) ve yorum çağrısı
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Fable 5 | yok | prompt | https://github.com/asgeirtj/system_prompts_leaks | Sızdırıldığı söylenen Fable 5 sistem komutu; başka modele enjekte edilerek Fable davranışı alınıyor. | 0:12 | GitHub'da claude-fable-5.md dosyası ve 'System:' metni görünüyor. (karede: kanıttan) GitHub'da claude-fable-5.md dosyası ve 'System:' metni görünüyor. |
| system_prompts_leaks | yok | plugin | https://github.com/asgeirtj/system_prompts_leaks | Sistem komutlarının toplandığı GitHub deposu (asgeirtj); Fable 5 komutu burada. | 0:12 | asgeirtj / system_prompts_leaks, Anthropic / claude-fable-5.md yolu. (karede: kanıttan) asgeirtj / system_prompts_leaks, Anthropic / claude-fable-5.md yolu. |
| Claude Code | yok | CLI | yok | Terminalde performans denetimi ve kod işlerinde gösterilen Anthropic CLI aracı. | 0:01 | Ekran metni 'Claude Code' ve 'Opus (1M context)' başlığı. (karede: kanıttan) Ekran metni 'Claude Code' ve 'Opus (1M context)' başlığı. |
| Opus 4.8 | yok | teknik | yok | Claude Code içinde seçili görünen model; enjeksiyon için kullanılabilir model. | 0:04 | Ekranda 'Opus 4.8' yazıyor; açıklamada Opus geçiyor. |
| Claude Sonnet | yok | teknik | yok | Sistem komutunun takılabileceği daha ucuz model seçeneği. | 0:15 | Ekran metni 'Sonnet'; açıklamada Opus, Sonnet, Haiku sayılıyor. (karede: kanıttan) Ekran metni 'Sonnet'; açıklamada Opus, Sonnet, Haiku sayılıyor. |
| Claude Haiku | yok | teknik | yok | Sistem komutunun takılabileceği en ucuz model seçeneği. | 0:15 | Ekran metni 'Haiku'. (karede: kanıttan) Ekran metni 'Haiku'. |
| PostgreSQL | yok | CLI | yok | Claude Code oturumunda EXPLAIN ANALYZE için psql ile sorgu analizi yapılıyor. | 0:02 | Bash(psql -c 'EXPLAIN ANALYZE SELECT * FROM events WHERE ..') satırı. · kanıt: kare (karede: Bash(psql -c 'EXPLAIN ANALYZE SELECT * FROM events WHERE ..') satırı.) |
| k6 | yok | CLI | yok | Claude Code oturumunda yük testi için çalıştırılan araç. | 0:02 | Bash(k6 run launch-lo...) satırı ve http_req_duration çıktısı. (karede: kanıttan) Bash(k6 run launch-lo...) satırı ve http_req_duration çıktısı. |
| Claude Fable 5 Mythos 5 duyurusu | yok | ipucu | yok | Anthropic'in Fable 5 ve Mythos 5 modellerini anlatan haber sayfası; sistem komutunda anılıyor. | 0:13 | Metinde anthropic.com/news/claude-fable-5-mythos-5 adresi geçiyor. · kanıt: kare (karede: Metinde anthropic.com/news/claude-fable-5-mythos-5 adresi geçiyor.) |
| Claude Opus | yok | teknik | yok | Claude Code model seçicisinde görünen Opus modeli; 'Opus 4.8' yazısı da okunuyor. | 0:01 | Opus (1M context) (karede: Claude Code üst bilgisinde OCR ile okunan 'Opus (1M context)' yazısı) |
| Claude Mythos 5 | yok | teknik | yok | Sistem komutu metninde Claude Fable 5 ile aynı temel modeli paylaştığı söylenen model. | 0:12 | Claude Fable 5 and Claude Mythos 5 share the same underlying model. (karede: GitHub önizlemesindeki sistem komutu metninde 'share the same underlying model' cümlesi) |
| GitHub | yok | teknik | yok | Sistem komutu deposunun görüntülendiği kod barındırma sitesi. | 0:12 | Code · Issues · Pull requests · Discussions sekmeleri · kanıt: kare (karede: GitHub depo sayfasında Code, Issues, Pull requests ve Discussions sekmeleri) |
| psql | yok | CLI | yok | PostgreSQL komut satırı istemcisi; EXPLAIN ANALYZE sorgusu çalıştırmak için kullanılıyor. | 0:02 | Bash(psql -c 'EXPLAIN ANALYZE SELECT * FROM events WHERE ..') (karede: Terminalde 'Bash(psql -c EXPLAIN ANALYZE …)' satırı ve altında 'Seq Scan on events' çıktısı) |
| BZBECAD | yok | teknik | yok | Ekranda 3B model düzenleme arayüzü olarak görünüyor; ad OCR ile tam okunamadı. | 0:06 | Desktop Lighthouse · kanıt: kare (karede: Üst bardaki 'BZBECAD' başlığı, ortada 'Desktop Lighthouse' 3B fener önizlemesi, altta 'EDITING MODEL.PY' kod paneli) |
| Fable 5 sistem komutunu başka modele enjekte etmek | yok | prompt | yok | Sızdırıldığı söylenen Claude Fable 5 sistem komutu: Claude'un davranışı, ürün bilgisi, reklamsız politikası ve istem yazma önerilerini tanımlıyor; modele enjekte edilince Fable gibi davranması sağlanıyor. | 0:12 | kaynak: kare |
## Açıklama bağlantıları
- https://stripe.com — Stripe web sitesi; Anthropic sayfasında müşteri logosu olarak geçiyor. · aday: hayır · Referans sayfası; videoda kullanılmıyor. · sınıf: diğer
- https://www.hebbia.com — Hebbia web sitesi; Anthropic sayfasında müşteri olarak geçiyor. · aday: hayır · Referans sayfası; videoda kullanılmıyor. · sınıf: diğer
- https://www.imc.com — IMC web sitesi; Anthropic sayfasında müşteri olarak geçiyor. · aday: hayır · Referans sayfası; videoda kullanılmıyor. · sınıf: diğer
- https://www.dynotx.com — DynoTx web sitesi; Anthropic sayfasında müşteri olarak geçiyor. · aday: hayır · Referans sayfası; videoda kullanılmıyor. · sınıf: diğer
- https://platform.claude.com/docs/en/about-claude/models/overview — Claude model genel bakış belgesi. · aday: hayır · Referans belge; videoda kullanılan bir araç değil. · sınıf: diğer
- https://www.anthropic.com/news/claude-fable-5-mythos-5 — Anthropic'in Fable 5 ve Mythos 5 duyuru sayfası. · aday: hayır · Referans haber sayfası; kullanılabilir bir araç değil. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| psql -c 'EXPLAIN ANALYZE SELECT * FROM events WHERE ..' | PostgreSQL'de sorgunun çalışma planını ve gerçek süresini gösterir. (karede: Terminalde 'Bash(psql -c EXPLAIN ANALYZE …)' satırı ve 'Seq Scan on events' çıktısı) | 0:02 | kare |
| k6 run launch-… | k6 ile launch senaryosunu çalıştırıp yük ve p95 süresini ölçer. (karede: Terminalde 'Bash(k6 run launch-…' satırı ve 'p95 is over the 400ms' çıktısı) | 0:02 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Fable 5'in tüm sistem komutu sızdırıldı. | 0:00 | özellik |
| Komut tek satır kodla herhangi bir modele enjekte edilip kullanılabiliyor. | 0:00 | özellik |
| Opus, Sonnet veya Haiku ile çalışıyor; daha ucuz modelle aynı davranış alınıyor. | açıklama | karşılaştırma |
| Dosya 3826 satır, 183 KB boyutunda. | 0:12 | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| ekran 0:00 | Claude Fable 5 sistem komutu | Claude Fable 5 | Altyazı: Fable 5'in tüm sistem komutu sızdırıldı. |
| ekran 0:12 | asgeirtj/system_prompts_leaks deposu | system_prompts_leaks | GitHub sayfası kareden okunuyor. |
| ekran 0:01 | Claude Code | Claude Code | OCR: Claude Code başlığı. |
| ekran 0:04 | Opus 4.8 | Opus 4.8 | OCR: Opus 4.8. |
| ekran 0:15 | Sonnet | Claude Sonnet | OCR: Sonnet. |
| ekran 0:15 | Haiku | Claude Haiku | OCR: Haiku. |
| ekran 0:02 | psql EXPLAIN ANALYZE | PostgreSQL | Bash(psql -c 'EXPLAIN ANALYZE ...'). |
| ekran 0:02 | k6 run | k6 | Bash(k6 run launch-lo...). |
| ekran 0:13 | Anthropic Fable 5 haber sayfası | Claude Fable 5 Mythos 5 duyurusu | URL ekranda. |
| ekran 0:06 | 3B deniz feneri modelleme arayüzü | aday değil: konu dışı | Arka plan görseli; araç adı okunmuyor. |
| ekran 0:14 | docs.claude.com prompt yazma belgeleri | aday değil: konu dışı | Sistem komutu metni içinde geçen bağlantı. |
| bağlantılı sayfa | Stripe, Hebbia, IMC, DynoTx | aday değil: konu dışı | Anthropic duyuru sayfasındaki müşteri bağlantıları; videoda kullanılmıyor. |
| yorum | Yorumlar | aday değil: konu dışı | Girişsiz alınamıyor. |
## Kareden okunanlar
- 0:02: Claude Code terminali: perf-audit, EXPLAIN ANALYZE, k6 çıktısı, 'sızdırıldı' altyazısı.
- 0:06: 3B deniz feneri (lighthouse) modelleme arayüzü ve 'EDITING MODEL.PY' kod paneli.
- 0:12: GitHub asgeirtj/system_prompts_leaks, Anthropic/claude-fable-5.md, 'System:' önizlemesi.
## Belirsizlikler
- Tek satırlık kurulum komutu videoda gösterilmiyor ve söylenmiyor; yorumlara 'FABLE' yazana gönderileceği belirtiliyor.
- Sızıntının gerçekliği doğrulanamadı; GitHub deposundaki içeriğe dayanıyor.
- Yorumlar girişsiz alınamadı.
- Arka plan terminal ve 3B deniz feneri ekranlarının konuyla ilişkisi belirsiz (muhtemelen genel Claude Code görselleri).
- OCR'da geçen Next.js, Stripe, TypeScript ve Inter karelerde doğrulanamadı; video bağlamında kullanılmıyor.
- Anthropic haber sayfasında bağlı Stripe, Hebbia, IMC, DynoTx müşteri siteleri videoda kullanılmıyor.
- Ekrandaki URL'ler OCR hatalı; düzeltilmiş hâlleri tahmindir.
## Atlanan segment oranı
0/1 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://www.anthropic.com/news/claude-fable-5-mythos-5 | 0:13 | ekran | hayır |
| https://docs.claude.com/en/docs/build-with-claude/prompt-engineering | 0:14 | ekran | hayır |
| https://www.anthropic.com/news/claude-is-a-space-to-think | 0:14 | ekran | hayır |
| https://github.com/asgeirtj/system_prompts_leaks | 0:12 | ekran | evet |
| https://docs.claude.com/en/docs/build-with-ciaude/prompt- | 0:14 | ekran | hayır |
| https://www.anthropic.com/hews/claude-is-a-space-to- | 0:14 | ekran | hayır |
| https://stripe.com | açıklama | açıklama | hayır |
| https://www.hebbia.com | açıklama | açıklama | hayır |
| https://www.imc.com | açıklama | açıklama | hayır |
| https://www.dynotx.com | açıklama | açıklama | hayır |
| https://platform.claude.com/docs/en/about-claude/models/overview | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Sızdırılan Fable 5 sistem komutunu GitHub deposunda bulma — araçlar: system_prompts_leaks, GitHub
- 2. adım — Komutu seçilen bir modele tek satırla enjekte etme — araçlar: Claude Fable 5, Claude Code
- 3. adım — Model seçimi: Opus, Sonnet veya Haiku — araçlar: Opus 4.8, Claude Sonnet, Claude Haiku
- 4. adım — Kendi projede deneme — araçlar: Claude Code
## Promptlar
- Fable 5 sistem komutunu başka modele enjekte etmek — Sızdırıldığı söylenen Claude Fable 5 sistem komutu: Claude'un davranışı, ürün bilgisi, reklamsız politikası ve istem yazma önerilerini tanımlıyor; modele enjekte edilince Fable gibi davranması sağlanıyor.
ikinci göz KAPALI: --ikinci-goz yok
