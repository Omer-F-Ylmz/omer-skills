# Claude Yalan Söylüyor: Uygulamanı Bu Ajanla Test Et
kanal: İsa Nurdoğdu · süre: 9 dk · altyazı: otomatik tr
ana iddia: Claude kendi yazdığı kodu kendisi test ettiği için yalnız iyi senaryoları doğrulayıp "hazır" diyor; çözüm, canlı uygulamayı uçtan uca kıran bağımsız bir test ajanı (TestSprite).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| TestSprite | YENİ | ELENDİ | bulut test ajanı (MCP/CLI); izin ağır: hesap + API anahtarı + kredi, test hesabı bilgisi harici servise; açıklama linki ?via= yönlendirmeli |
| Operiqo | YENİ | ELENDİ | açıklamada tanıtılan hizmet, Live test örnek URL'si; araç değil |
| microsoft/playwright | ÇİFT | ELENDİ | Claude in Chrome aynı canlı tarayıcı testini yapıyor; videoda yalnız anıldı |
| diğer: Claude in Chrome, /mcp, /exit, kanıtsız "hazır" iddiasını reddetme | ZATEN VAR | ELENDİ | Claude Code yerleşik; kural CLAUDE.md Hedef-güdümlü "kanıtsız bitti yok" |
| bağımsız doğrulayıcı: kodu yazan ≠ test eden | YENİ | BİLGİ | canlı uygulamada uçtan uca akış testi, hata raporu kök neden + kanıt (kayıt) ile; mevcut kural yalnız kanıt istiyor |
| uç/negatif senaryo + regresyon testi | YENİ | BİLGİ | geçersiz girdi (telefon formatı, eksik hane), yoğun istek, düzeltme sonrası eski özellik kontrolü |
## ölçütler (YENİ)
- TestSprite: bakım=bilinmiyor (videoda repo yok; gh repos/TestSprite/testsprite-mcp 404) · çift=kısmi: Claude in Chrome (canlı tarayıcı testi) + superpowers:requesting-code-review (ayrı alt-agent) · izin=testsprite.com hesabı, API anahtarı, kredi tabanlı plan (ücretsiz başlangıç), login akışında test hesabı bilgisi, uygulamaya harici servis erişimi · context=MCP tool şemaları her oturum (sayı videoda yok) · kurulum: —
- Operiqo: bakım=bilinmiyor · çift=örtüşme yok · izin=bilinmiyor (videoda anlatılmıyor) · context=— · kurulum: —
- bağımsız doğrulayıcı, uç/negatif senaryo + regresyon: bakım=— (teknik) · çift=kısmi: superpowers:requesting-code-review, verification-before-completion · izin=yok · context=CLAUDE.md kural satırı (her oturum) · kurulum: —
## hedefler (BİLGİ)
- kodu yazan ajan kendi işini doğrulamaz; doğrulama ayrı bağlamda, canlı uygulamada uçtan uca, hata kök neden + kanıtla raporlanır → CLAUDE.md (Hedef-güdümlü)
- test kapsamı mutlu yolla bitmez: geçersiz girdi, yoğun istek, düzeltme sonrası eski özelliklerin regresyon kontrolü → CLAUDE.md (Hedef-güdümlü)
---
## ek: test/güvenlik
- TestSprite: bağımsız "müfettiş" test ajanı; kodu değil canlı uygulamayı test eder (giriş, tıklama, buton, form doldurma, uçtan uca iş akışı)
- TestSprite: arka planda tek değil birden fazla model kullanarak yanlılığı önlediği iddiası (kanıt gösterilmedi)
- TestSprite raporu: fail testte hata açıklaması, kök neden, hatanın yeri (ör. işletme bilgileri kaydındaki API hatası) ve testin ekran kaydı videosu
- TestSprite Create project, seçenek Live: yayındaki URL verilir (örnek operiqo.com); geri bildirim/ajan döngüsü yok, yayına alınmamış localhost projeyi test edemez
- TestSprite Create project, seçenek CLI: terminalde komut çalıştırılır, API anahtarı ister; tüm kodlama ajanları için (Codex, Antigravity, Claude Code); komut metni altyazıda yok
- TestSprite Create project, seçenek MCP: Cursor, Claude Code ve diğer IDE'ler için yükleme seçenekleri; videoda bu yol kullanıldı
- kurulum akışı: panelde API key oluştur (Create) → Claude Code'a "TestSprite MCP kur" promptu + anahtar → /exit → yeniden başlat → /mcp ile bağlı olduğunu doğrula
- CLI komutu terminal açmadan Claude Code'a verilip çalıştırılabilir; Claude Code uygulamasında da aynı prompt geçerli; Antigravity'ye "TestSprite MCP kur" demek de yeterli denir
- test promptu: "TestSprite'ı kullanarak uygulamayı uçtan uca test et" ya da spesifik akış (acente sahibi girişi; tur kartları, işletme ayarları, KPI'lar)
- login gereken akışta test hesabının giriş bilgileri prompta verilir (videoda örnek test hesabı verildi)
- testing configuration: mod, backend, frontend seçenekleri; ayarları ajanın kendisi yapar
- TestSprite paneli: proje sayfasında MCP bağlı / CLI bağlı çalıştırmalar ve sonuçları görüntülenir
- döngü: sonuç Claude Code'a geri bildirim olarak döner, Claude raporu çekip düzeltmeleri yapar; test tek seferlik değil gün gün tekrarlanmalı
- GitHub bağlama: "Connect GitHub" ile GitHub'daki projeler de test edilebilir
- yöntem: kodu yazan ile test eden aynı ajan olmamalı (kendi ödevini denetleme yanlılığı); test etmek ile test kodu yazmak aynı şey değil
- iddia: AI kod ajanları yalnız iyi senaryoları test eder, uç senaryoları (chatbota yoğun aralıklarla mesaj) atlar, koşulları gevşetir (mesai saatleri ekranı boş gösteriliyor)
- iddia: hata düzeltirken dün eklenen özelliği sessizce bozar (regresyon); "araştırmalarla kanıtlanmış" denir, kaynak verilmez
- Claude Chrome'u açıp Playwright ile de test yapabilir; TestSprite farkı ikinci göz olması ve daha az token harcatması (iddia, ölçüm yok)
- Claude "tüm testler yapıldı, yayına alabilirsin" dedi; aynı uygulamada tur kartı ve telefon değiştirme akışlarında hata çıktı (canlı gösterim)
- negatif girdi örnekleri: sabit hane sayılı alana iki haneli değer kabul edilmemeli; geçersiz telefon formatı reddedilmeli
- sayı: uygulama 3 ay geliştirildi, tur kartında yüzlerce PNG var — yalnız iddia
- sayı: net marj 24.000, maliyet 24.000 (0 olmalı), toplam kâr 30.000 mantık hatası — gösterildi
- sayı: tur kartında İleri sonrası 404 hatası — gösterildi (TestSprite kaydında da yakalandı)
- sayı: ücretsiz planda 150 kredi — gösterildi (panelden okundu)
- sayı: TestSprite 7 test belirledi, ilk aşamada 1 pass 1 fail — gösterildi
- sayı: tüm testler sonrası 146 kredi kaldı, yaklaşık 4-5 kredi harcandı — gösterildi (panelden okundu)
- açıklamadaki TestSprite linki yönlendirme parametreli (?via=isa-N)
