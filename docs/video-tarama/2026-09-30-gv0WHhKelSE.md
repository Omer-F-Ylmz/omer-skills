# Claude Code best practices | Code w/ Claude
## Künye
Claude Code best practices | Code w/ Claude · Anthropic · süre: 25:53 · en · https://youtu.be/gv0WHhKelSE
motor: parti 2026-09-30-uzun-3 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (6)
## Özet
Anthropic'ten Cal Rueb, Code w/ Claude konferansında Claude Code'un ne olduğunu, nasıl çalıştığını (araçlar + döngüde çalışan saf ajan, indeksleme yok, agentic search), kullanım alanlarını (keşif, tasarım, geliştirme, dağıtım, destek/ölçek) ve en iyi pratikleri anlatıyor: CLAUDE.md, izin yönetimi, CLI/MCP entegrasyonu, bağlam yönetimi (/clear, /compact), plan ve to-do, test odaklı 'akıllı vibe coding', ekran görüntüsü, çoklu Claude, Escape/çift Escape, headless otomasyon. Canlı demoda /model, /config, Claude 4'ün araç çağrıları arasında düşünmesi ('think hard'), VS Code/JetBrains entegrasyonları ve GitHub changelog takibi gösteriliyor. Soru-cevapta birden çok CLAUDE.md, talimatlara uyum ve çoklu ajan durum paylaşımı (paylaşılan markdown dosyası) ele alınıyor.
## Bölümler
- 0:00 Giriş ve konuşmacının hikâyesi
- 3:02 Claude Code zihinsel modeli
- 3:47 Claude Code nasıl çalışır
- 4:51 Kod tabanını anlama (agentic search)
- 6:14 Kullanım: keşif
- 7:04 Kullanım: tasarım
- 7:42 Kullanım: geliştirme
- 8:32 Kullanım: dağıtım
- 9:25 Kullanım: destek ve ölçek
- 10:20 En iyi pratik: CLAUDE.md
- 11:13 En iyi pratik: izinler
- 12:38 En iyi pratik: entegrasyon
- 14:05 En iyi pratik: bağlam yönetimi
- 14:44 Etkili iş akışları
- 16:03 Akıllı vibe coding
- 16:54 İleri teknikler
- 18:08 Headless otomasyon
- 18:56 Canlı demo ve soru-cevap
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| CLAUDE.md | yok | ipucu | yok | Çalışma dizinindeki CLAUDE.md oturum başında prompt'a eklenir; test çalıştırma, proje yapısı, stil rehberi gibi bilgileri oturumlar ve ekip arasında paylaşır. Projeye, ev dizinine konabilir. | 10:20 | CLAUDE.md dosyası çalışma dizininde varsa prompt'a 'plopped into context' olarak eklenir. |
| Auto-accept modu (Shift+Tab) | yok | ipucu | yok | Shift+Tab ile Claude onay istemeden çalışır; ayrıca ayarlarda belirli bash komutları (örn. npm run test) kalıcı onaylanabilir. | 12:38 | autoaccept mode where if you're working with cloud code and you press shift tab |
| CLI araçları tercih et (gh) yerine MCP | yok | ipucu | yok | İyi bilinen, belgelenmiş CLI aracı (GitHub gh) varsa MCP sunucusu yerine CLI kurmayı öneriyor. | 13:43 | I would recommend using the CLI tool. |
| /clear ve /compact | yok | ipucu | yok | Bağlam dolmaya başlayınca /clear ile sıfırla (CLAUDE.md kalır) veya /compact ile özetleyip yeni oturumu tohumla. | 14:05 | You can run slashcle and just start over ... or you can run slash compact |
| Önce plan iste + to-do listesi | yok | iş akışı | yok | Hata düzeltmeden önce Claude'dan araştırıp plan çıkarmasını iste; to-do listesini izle, yanlışsa Escape ile müdahale et. | 14:44 | Can you search around, figure out what's causing it, and tell me a plan |
| Akıllı vibe coding (TDD, lint, sık commit) | yok | iş akışı | yok | Küçük değişiklikler, testleri çalıştırma, TypeScript/lint kontrolü ve düzenli commit ile geri dönüş noktaları oluşturma. | 16:03 | test-driven development, small changes, run the tests, check the TypeScript and the linting |
| Ekran görüntüsü / mock ile yönlendirme | yok | teknik | yok | Görseli yapıştırıp veya mock.png dosyasını göstererek Claude'a site yaptırma ve hata ayıklama. | 16:03 | look at this mock.png and then build the website for me |
| Çoklu Claude paralel çalıştırma | yok | iş akışı | yok | tmux veya farklı sekmelerde aynı anda birden çok Claude Code çalıştırıp orkestre etme; bazıları dört tane çalıştırıyor. | 16:54 | people at Anthropic and a few customers that run four clouds at the same time |
| Escape ve çift Escape | yok | ipucu | yok | Escape çalışan ajanı durdurur; iki kez basmak konuşmada geri atlamayı sağlar. | 17:56 | if you press escape twice, you can actually jump back in your conversation |
| Headless / SDK ve GitHub Actions | yok | iş akışı | yok | Claude Code'u programatik kullanma: CI/CD ve GitHub Actions içine ajan yerleştirme. | 18:08 | how can we use Claude programmatically. We have that in GitHub actions. |
| /model ve /config | yok | ipucu | yok | Çalışılan modeli görme ve Sonnet/Opus arasında geçiş. | 18:56 | you can do slashmodel. You can see what model you're running on. |
| 'think hard' genişletilmiş düşünme | yok | prompt | yok | Claude 4 araç çağrıları arasında düşünebilir; prompt'a 'think hard' eklemek düşünmeyi tetikler. | 19:58 | throw a think hard in there |
| VS Code ve JetBrains entegrasyonları | yok | plugin | yok | IDE entegrasyonu Claude'un hangi dosyada olduğunuzu bilmesini sağlar. | 20:30 | new great integrations with VS Code and Jet Brains |
| CLAUDE.md içinde @ ile dosya referansı | yok | teknik | yok | CLAUDE.md içinden @ işaretiyle başka dosyalar içe aktarılabilir. | 22:08 | in your cloud MD you can start referencing other files ... with an at sign |
| Ajanlar arası durum için paylaşılan markdown dosyası | yok | iş akışı | yok | Çoklu ajan iletişimi için ticket.md gibi dosyaya not yazdırıp diğer Claude'a okutma. | 24:15 | write stuff in like ticket.md for another developer |
| Claude'u yazmadan önce düşünce ortağı olarak kullanıp seçenek çıkarttırmak (özetlenmiş ifade). | yok | prompt | yok | I'm thinking about implementing this feature, can you search around and figure out how we would do it and report back with two or three options. Don't start writing any files yet. | 7:04 | kaynak: altyazı |
| Düzeltmeden önce plan almak (özetlenmiş ifade). | yok | prompt | yok | I have this bug. Can you search around, figure out what's causing it, and tell me a plan how we're going to fix it? | 14:44 | kaynak: altyazı |
| Genişletilmiş düşünmeyi demo etmek. | yok | prompt | yok | Can you figure out what's in this project? (think hard) | 19:58 | kaynak: altyazı |
| Kod tabanı keşfi ve git geçmişi özeti (özetlenmiş ifade). | yok | prompt | yok | Look at this file and the git history and tell me a story about how this code has changed over the past couple weeks. | 7:04 | kaynak: altyazı |
## Açıklama bağlantıları
- yok
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Sunum slaytı: 'How Claude Code works' kart/tablo düzeni | Krem arka planlı slaytta solda başlık ve kod simgesi, sağda başlık+açıklama çiftlerinden oluşan kartlar (Powerful actions, Codebase awareness, Transparency, Security); kartlar adım adım eklenir. (karede: Krem zemin, solda 'How Claude Code works' başlığı ve </> pencere simgesi; sağda gri etiket + açık kutuda açıklama satırları. Sonraki karede Transparency ve Security kartları eklenmiş.) | 4:49 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /model | Çalışılan modeli gösterir ve Sonnet/Opus arasında geçiş sağlar. | 18:56 | altyazı |
| /config | Ayarlardan model vb. değiştirme. | 18:56 | altyazı |
| /clear | Bağlamı temizler, CLAUDE.md hariç baştan başlar. | 14:05 | altyazı |
| /compact | Konuşmayı özetleyip yeni oturumu özetle başlatır. | 14:05 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Code kod tabanını indekslemez/embed etmez; glob, grep, find ile agentic search yapar. | 4:51 | özellik |
| Claude Code sorguları aracı sunucu olmadan doğrudan Anthropic modellerine gider; Bedrock ve Vertex AI desteklenir. | 6:04 | özellik |
| Modellerin bağlam penceresi 200.000 token. | 14:05 | sayısal |
| İyi bilinen CLI aracı ile MCP sunucusu arasında seçim varsa CLI önerilir. | 13:43 | öneri |
| Claude 4 ile araç çağrıları arasında düşünme mümkün; önceki modellerde değildi. | 18:56 | karşılaştırma |
| Claude 4, talimatlara (CLAUDE.md) daha iyi uyuyor ve gereksiz yorum bırakma sorunu büyük ölçüde azaldı. | 23:09 | karşılaştırma |
| Bazı kişiler aynı anda dört Claude çalıştırıyor; konuşmacı ikiyi çalıştırabiliyor. | 16:54 | sayısal |
## Kareden okunanlar
- 1 (0:32): Konuşmacı kürsüde, kürsüde 'AI' logosu.
- 2 (1:35): Slayt: 'Claude Code best practices', Cal Rueb, Member of Technical Staff, Anthropic; Code w/ Claude logosu.
- 3 (2:33): Konuşmacı yakın plan, slayt yok.
- 4 (4:17): Konuşmacı yakın plan, kürsüde AI logosu.
- 5 (4:49): Slayt 'How Claude Code works': Powerful actions & integrations ve Codebase awareness kartları (dosya düzenleme, CLI/MCP, commit; agentic arama).
- 6 (6:04): Aynı slayt, ek Transparency (kademeli izin sistemi) ve Security (aracı sunucu yok; Anthropic API, Bedrock, Vertex AI) kartları.
## Belirsizlikler
- Video yalnız konuşma; kurulum/terminal komutu gösterilmedi, sadece slash komutları anıldı.
- Aday prompt'lar konuşmacının sözlü anlatımından özetlendi, birebir gösterilmiş prompt değil.
- Konuşmada 'cloud code' olarak geçen yazımlar altyazı hatası; Claude Code olarak yorumlandı.
- 'coup' adlı iç araç altyazıda geçiyor, gerçek adı belirsiz.
- VS Code/JetBrains demosunun ekran görüntüsü verilmediği için 20:30 zamanı yaklaşıktır.
## Atlanan segment oranı
0/32 (paket tam okuma, motor)
ikinci göz KAPALI: --ikinci-goz yok
