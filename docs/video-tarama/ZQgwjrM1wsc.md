# Kodu Claude yazsın, testi TestSprite yapsın
kanal: Burhan KOCABIYIK · süre: 6 dk · altyazı: otomatik tr
ana iddia: TestSprite CLI'ı API anahtarıyla Claude Code'a bağlayınca ajan her değişiklikten sonra uygulamayı (sayfalar, linkler) otomatik test ediyor, elle test ve token/zaman kaybı bitiyor.
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| TestSprite/testsprite-cli (TestSprite) | YENİ | ADAY | bulut AI test: CLI + API anahtarıyla Claude Code'a bağlanır; sayfa/dil/link kontrolü, dashboard + hata chat'i, otomatik tekrar test; kalite kanıtı yok ("fena değil"); açıklama linki referanslı (?via=burhan-k) |
| "bitti" sonrası otomatik doğrulama, her değişiklikten sonra tüm uygulamayı yeniden test | ZATEN VAR | ELENDİ | CLAUDE.md hedef-güdümlü ("kanıtsız bitti yok") + superpowers:verification-before-completion / test-driven-development |
| eklenen sayfada link kontrolü (tüm linkler çalışıyor mu) | YENİ | BİLGİ | TestSprite testi sayfaya girip linkleri tek tek deniyor; SKILL.md Bölüm 4/9 ve audit.mjs link denetlemiyor |
| doğrulama katmanı varken kalite eşitse ucuz modele geç | YENİ | BİLGİ | Claude Code ile Kimi aynı sonucu veriyorsa Kimi "çok daha ucuz" (yalnız iddia, karşılaştırma gösterilmedi); CLAUDE.md'de model seçimi kuralı yok |
| diğer: Kimi (Moonshot AI), microsoft/vscode? (terminal) | YENİ | ELENDİ | Kimi'yi Claude Code'a bağlama yöntemi/ölçüm yok, ayrı sağlayıcı; VS Code yalnız terminal açmak için, kalem değil |
## ölçütler (YENİ)
- TestSprite/testsprite-cli: bakım=pushed 2026-09-14, 3205★, arşiv değil · çift=kısmi: superpowers:verification-before-completion (yöntem) + claude-in-chrome (yerleşik tarayıcı); bulutta kalıcı test suite/dashboard karşılığı yok · izin=TestSprite hesabı + API anahtarı (kredi bazlı, ücretsiz kredi var), Node 20.19+, global npm (ya da npx), localhost testi için TestSprite tüneli (uygulama buluta açılır), setup repoya skill dosyası yazar (README) · context=kurulan projede skill açıklaması her oturum; MCP şeması yok · kurulum: `npm install -g @testsprite/testsprite-cli` + `testsprite setup` (README; global istemezsen `npx @testsprite/testsprite-cli`)
- link kontrolü: bakım=— (teknik, repo yok) · çift=örtüşme yok (audit.mjs link denetlemiyor) · izin=yok · context=SKILL.md'ye 1 satır (yalnız skill yüklenince) · kurulum: —
- ucuz modele geç: bakım=— (teknik, repo yok) · çift=örtüşme yok · izin=yok · context=CLAUDE.md'ye 1 satır (her oturum) · kurulum: —
- diğer: bakım=Kimi bilinmiyor; microsoft/vscode pushed 2026-09-15, 192560★, arşiv değil · çift=örtüşme yok · izin=Kimi ayrı sağlayıcı API hesabı; VS Code yerel editör · context=kurulmadıkça yok · kurulum: —
## hedefler (BİLGİ)
- yeni/değişen sayfadaki tüm linkler (iç + dış) çalışıyor mu denetlenir, kırık link 0 → frontend-craft Bölüm 4 (kabul kriterleri)
- test/doğrulama döngüsü olan işte aynı görevi ucuz modelle de koştur, sonuç eşitse ucuz modeli kullan → CLAUDE.md (CONTEXT DİSİPLİNİ: model seçimi)
---
## ek: test/güvenlik
- sorun: Protipal yeni sürümünde Claude "yaptım, bitirdim" diyor ama açınca çalışmıyor; defalarca "şurasını yapamamışsın" prompt'u; yeni özellik eskiyi bozuyor (Claude Code, Codex)
- araç: TestSprite (testsprite.com) + TestSprite CLI (github.com/TestSprite/testsprite-cli, açıklamada) — her değişiklikten sonra uygulamanın tamamını otomatik test eden sistem
- yöntem: kurulumun iki yolu — CLI'ı sisteme kurmak ve TestSprite panelinden API anahtarı almak; komut siteden (en üstteki kod) kopyalanıp terminale yapıştırılıyor, komut metni altyazıda yok
- yöntem: kurulum Claude açılmadan boş terminalde (Visual Studio? → Terminal → yeni terminal); sonra CLI seçeneği seçiliyor; "lokalde de çalıştırabilirsiniz" deniyor
- ayar: TestSprite paneli → API anahtarı → yeni anahtar → proje adı ("Cloud left flow") → anahtar kopyalanıp Claude Code'a prompt içinde düz metin veriliyor (gizleme/ortam değişkeni önerisi yok)
- komut (prompt): leftflow.ai'ye şirketlerin veri toplaması için neler yapabileceği ve çözümlerin yazılı olduğu yeni sayfa ekle; "sayfayı bitirdikten sonra TestSprite CLI ile test et" + "TestSprite API key" ile anahtar
- yöntem: ajan sayfayı ekleyip testleri TestSprite'a koyuyor ("TestSprite tarafına koydum"); dashboard'da proje ve takip edilecek sistemler listeleniyor
- yöntem: test kapsamı örneği — data sayfası, İngilizce sürüm, Türkçe sürüm, leftflow içindeki diğer sayfalar
- yöntem: link kontrolü — test ajanı sayfaya girip linklerin çalışıp çalışmadığına bakıyor; nasıl kontrol ettiği dashboard'da izlenebiliyor
- yöntem: dashboard'da neler yapıldı/takip edildi/düzeltildi görünüyor; hata için chat ("neden bu problem var, nasıl düzeltirim")
- yöntem: testler bittikten sonra sürekli tekrar ettiriliyor (otomatik tekrar test), aşama aşama ilerliyor
- model değiştirme: Claude Code'un daha iyi olduğu işte Claude Code, aynı sonucu verdiği işte daha ucuz Kimi; "bunun takibinin yapılabileceği bir sistem kurulmuş" (hangi sistem olduğu belirtilmedi)
- iddia: benzer uygulamalar var (ad verilmedi); konuşmacı yakın zamanda denemiş, "gayet güzel, fena değil" — nitel, ölçüm yok
- sayı: tek satır CLI kurulumu — yalnız iddia (açıklamada; komut metni altyazıda yok)
- sayı: 2 kurulum yolu (CLI + API anahtarı) — gösterildi (demo anlatımı)
- sayı: başlangıçta ücretsiz kredi, "gayet yeterli" — yalnız iddia (miktar verilmedi)
- sayı: elle test döngüsü "iki adım ileri, bir adım geri"; otomatik test token ve "ciddi vakit" tasarrufu — yalnız iddia, ölçüm yok
- sayı: Kimi aynı sonuçta "çok daha ucuz" — yalnız iddia, fiyat/karşılaştırma gösterilmedi
