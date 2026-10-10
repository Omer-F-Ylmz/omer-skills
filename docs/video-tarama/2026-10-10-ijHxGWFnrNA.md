# Claude Code ile Mobil Uygulama Geliştirirken Asıl Bilmen Gerekenler
## Künye
Claude Code ile Mobil Uygulama Geliştirirken Asıl Bilmen Gerekenler · Onur Builds · süre: 10:01 · tr · https://youtu.be/ijHxGWFnrNA · şema 2
motor: parti 2026-10-10-short-10 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
tek kol: claude-sonnet-5-5 error_max_budget_usd:  · claude-haiku-5-5: claude-haiku-5-5 · 92107 tk
## Özet
Video, Claude Code ve Claude Opus 5.5 ile bir iOS (SwiftUI) uygulamasının fikirden çalışan ürüne kadar nasıl geliştirileceğini ideBox örneğiyle anlatıyor. Ürün tarifi, MVVM mimarisi, veri ve backend kararları önceden belgelenir. CLAUDE.md giriş kapısı, SwiftUI Engineering skill'i, implement-feature ve swift-review komutları ile docs klasöründeki PRODUCT-SPEC, ARCHITECTURE, DATA-PERSISTENCE, DESIGN-SYSTEM, ANIMATION ve PERFORMANCE dosyaları yapay zekânın kurallara uymasını sağlar. Claude Code bu dosyaları okuyup uygulamayı geliştirir; Xcode'da simülatörde test edilir. Video, kuralların hataları azalttığını ama hatasız kod garanti etmediğini vurgular.
## Bölümler
- 0:00 Fikirden çalışan uygulamaya: bu videoda ne yapacağız
- 0:13 Proje büyüyünce yapay zekayla neler bozulur?
- 0:40 Örnek uygulama: ideBox ve kullandığım araçlar
- 1:08 Fikri planlamak
- 1:20 UI ve UX
- 1:37 MVVM Mimarisi
- 2:11 Veri yapısı kararları
- 2:25 Backend gerekli mi? Lokal veri ve senkronizasyon
- 2:41 API nedir?
- 3:02 Bütün bunları yapay zekaya nasıl vereceğiz?
- 3:08 CLAUDE.md, skill dosyaları ve MCP
- 3:51 Hatasız kod garanti mi?
- 4:04 Proje klasörü: settings.json, skill ve komutlar
- 5:13 Docs: ürün tarifi, performans, mimari, animasyon
- 6:18 Apple'ın Xcode içindeki dokümanları
- 6:52 CLAUDE.md
- 7:14 Geliştirmeyi başlatan komut
- 8:15 Sonuç: uygulamayı test ediyoruz
- 9:38 Bu yapı neden önemli?
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Code | yok | CLI | yok | Terminalde çalışan yapay zekâ kodlama aracı; proje bu araçla geliştiriliyor. | 1:00 | Terminalde 'claude' yazılıp 'Claude Code' çıktısı görünüyor. (karede: Terminal penceresinde '> claude' yazılı; altında 'Claude Code' ve 'model: Opus 5.5 · güncel' satırları.) |
| Claude Opus 5.5 | yok | teknik | yok | Claude Code ile kullanılan model; videoda güncel ve en iyi model olarak tanıtılıyor. | 0:40 | Opus 5.5 modeli şu an güncel. En iyi model o. |
| Xcode | yok | teknik | yok | Apple'ın iOS uygulama geliştirme ortamı; proje açılıp simülatörde çalıştırılıyor. | 8:15 | Şu anda Xcode'u açıp projemize ideBox Open dedim. |
| SwiftUI | yok | teknik | yok | Uygulamanın arayüzünü yazmak için kullanılan Apple UI framework'ü. | 4:32 | SKILL.md içinde 'struct IdeaListView: View' kodu gösteriliyor. (karede: SKILL.md ekranında 'struct IdeaListView: View' ve '@State private var viewModel: IdeaListViewModel' kodu.) |
| Swift | yok | teknik | yok | Uygulamanın programlama dili; skill'de Swift 6 strict concurrency kuralları yer alıyor. | 4:38 | Swift 6 strict concurrency (default MainActor, @ModelActor, @concurrent) yazıyor. (karede: SKILL.md açıklama satırında 'Swift 6 strict concurrency' ifadesi.) |
| SwiftData | yok | teknik | yok | Verilerin cihazda saklandığı kalıcılık katmanı; PRODUCT-SPEC'te yerel veri için geçiyor. | 5:08 | 'all data stays on the device (SwiftData)' ifadesi. (karede: PRODUCT-SPEC.md ilkeler bölümünde 'SwiftData' parantez içinde yazıyor.) |
| Swift Testing | yok | teknik | yok | Testleri yazmak için kullanılan framework; @Test, #expect ve #require kuralları skill'de. | 4:34 | 'Swift Testing' ve '#require' kuralları yazıyor. (karede: SKILL.md test kurallarında '@Test', '#expect', '#require' ve 'Test.cancel()' satırları.) |
| String Catalog | yok | teknik | yok | Çok dilli metinlerin tutulduğu yerelleştirme dosyası (Localizable.xcstrings). | 4:42 | 'String Catalog localization' ifadesi. (karede: SKILL.md satırında 'String Catalog localization and Swift Testing' yazıyor.) |
| Liquid Glass | yok | teknik | yok | Apple'ın iOS 27 cam efekti tasarım dili; tasarım kurallarında kullanılıyor. | 5:32 | 'Liquid Glass can no longer be opted out of' kuralı. (karede: Tasarım dokümanında 'iOS 27 facts: Liquid Glass can no longer be opted out of' satırı.) |
| Instruments | yok | teknik | yok | Apple'ın performans ölçüm aracı; PERFORMANCE.md içinde kontrol listesi var. | 5:24 | '## 6. Instruments Checklist' başlığı. (karede: PERFORMANCE.md'de '6. Instruments Checklist' başlığı ve SwiftUI, Time Profiler satırları.) |
| CLAUDE.md | yok | teknik | yok | Projenin giriş kurallarını içeren dosya; Claude oturum başında okur. | 3:08 | CLAUDE.md dosyası da bu projede nasıl çalışacağını söylüyor olacak. |
| settings.json | yok | teknik | yok | Claude'un bu projede izin sormadan yapabileceği işleri (okuma, yazma, komut) tanımlayan dosya. | 4:04 | Claude'un bu projede neleri izin sormadan yapabileceğini belirliyor. |
| SwiftUI Engineering skill | yok | skill | https://github.com/onuryildriim/idebox-claude-code | Claude'a kıdemli iOS geliştirici gibi Swift/SwiftUI kodu yazdıran skill dosyası. | 4:04 | Skill'de SwiftUI Engineering dediğimiz skill MD dosyamız var. · kanıt: yok |
| /implement-feature | yok | iş akışı | https://github.com/onuryildriim/idebox-claude-code | Yeni bir özelliği önce veri, sonra mantık, sonra ekran, sonra test sırasıyla yaptıran komut. | 4:04 | Implement Feature MD... önce veri, sonra mantık, sonra ekran, sonra test. |
| /swift-review | yok | iş akışı | https://github.com/onuryildriim/idebox-claude-code | Verilen Swift dosyalarını proje kurallarına göre inceleyip dosya ve satır bazlı sorunları ve düzeltmeleri gösteren komut. | 4:04 | swift-review.md dosyamız da buradaki hataları nasıl kontrol etmiş. |
| ideBox Claude Code kiti | yok | iş akışı | https://github.com/onuryildriim/idebox-claude-code | Videodaki CLAUDE.md, skill, komut ve docs dosyalarının ücretsiz indirilebilir paketi. | açıklama | Videoda kullandığım bütün dosyalar ücretsiz. · kanıt: yok |
| Claude Code'a proje geliştirmeyi başlatmak | yok | prompt | yok | iOS 27 ve min SDK iOS 27 olarak ayarlansın; önce tüm MD dosyaları okunsun, sonra proje kurallara uygun şekilde geliştirilmeye başlasın. | 7:14 | kaynak: altyazı |
| Ürün tarifi dosyasını güncellemek | yok | prompt | yok | Proje için PRODUCT-SPEC.md dosyası güncellensin; ürün tarifi projeye göre yeniden yazılsın. | 5:13 | kaynak: altyazı |
| Swift kodunu proje kurallarına göre incelemek (swift-review) | yok | prompt | yok | Verilen dosyalar (yoksa son değişiklikler) CLAUDE.md ve docs/project kurallarına göre incelensin; her sorun dosya, satır, neden ve düzeltme ile raporlansın. | 4:48 | kaynak: kare |
| SwiftUI skill'in rol tanımı | yok | prompt | yok | Claude kıdemli bir iOS geliştirici (8+ yıl) gibi davransın; iOS 27 SDK'da doğru, basit, test edilebilir ve erişilebilir üretim kodu yazsın. | 4:56 | kaynak: kare |
| Yeni özellik geliştirmek (implement-feature) | yok | prompt | yok | Yeni bir özellik önce veri, sonra mantık, sonra ekran, sonra test sırasıyla yapılsın. | 4:04 | kaynak: altyazı |
## Açıklama bağlantıları
- https://github.com/onuryildriim/idebox-claude-code — ideBox proje dosyaları deposu (CLAUDE.md, skill, komut, docs) · aday: evet (ideBox Claude Code kiti) · Videoda kullanılan CLAUDE.md, skill ve komut dosyalarını indirilebilir kıldığı için izleyicinin kullanabileceği bir kaynak. · sınıf: diğer
- https://code.claude.com/docs/en/quickstart — Claude Code resmi kurulum rehberi · aday: hayır · Resmi kurulum sayfası; referans bağlantısı, videoda kullanılan bir araç değil. · sınıf: diğer
- https://academy.claude.com/courses/claude-code-101 — Claude Code 101 ücretsiz başlangıç kursu · aday: hayır · Eğitim kursu referansı; videoda kullanılan bir araç ya da servis değil. · sınıf: diğer
## Site/UI teknikleri
- EKSİK: formda site/UI tekniği yok (kısmi kabul)
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude Code geliştirmede kullanılan ana araç olarak tercih ediliyor. | 0:40 | öneri |
| Claude Opus 5.5 şu an en iyi model olarak tanıtılıyor. | 0:40 | karşılaştırma |
| Kurallar dosyaları hataları azaltır ama yapay zekânın hatasız kod yazacağı garanti edilmez. | 3:51 | öneri |
| Apple'ın Xcode dokümanlarının çoğu modelin bilgisinde olduğu için tüm dokümanlara gerek yok; ihtiyaç duyulanlara referans vermek yeterli. | 6:18 | öneri |
| Proje minimum SDK iOS 27 olarak geliştirildi. | 7:14 | özellik |
| Uygulama Xcode'da iPhone 18 Pro simülatöründe çalıştırılıyor. | 8:15 | özellik |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| altyazı | Geliştirme için Claude Code kullanılacağı söyleniyor | Claude Code | 0:40 'Geliştirme yaparken ben Claude Code kullanacağım.' |
| altyazı | Opus 5.5 modelinin güncel ve en iyi model olduğu söyleniyor | Claude Opus 5.5 | 0:40 'Opus 5.5 modeli şu an güncel. En iyi model o.' |
| altyazı | CLI terminal üzerinden geliştirme anlatılıyor | Claude Code | 0:40 'Ben CLI dediğimiz terminalden geliştirmeye devam edeceğim.' |
| altyazı | Claude masaüstü uygulamasının alternatif olarak anılması | aday değil: genel kavram | 0:40 'Claude masaüstü uygulamasından da geliştirmeye devam edebilirsiniz.' |
| kare | Terminal uygulamasının adı olarak 'iTerm' yazısı | aday değil: genel kavram | 1:00 ekran metni 'iTerm' (sözlük eşleşmesi, belirsiz) |
| kare | Terminalde claude komutu yazılıp Claude Code açılıyor | Claude Code | 1:00 '> claude' ve 'Claude Code · model: Opus 5.5 · güncel' |
| altyazı | Örnek uygulama ideBox | aday değil: konu dışı | 0:40 'ideBox adında şu an geliştireceğimiz bir mobil uygulama' |
| kare | Örnek fikir metni olarak Higgsfield yazılıyor | aday değil: konu dışı | 1:08 ekran metni 'Higgsfield' fikir kutusu örneği |
| altyazı | Fikir örneğinde görüntü modeli olarak Seedance anılıyor | aday değil: konu dışı | 8:15 'seedance 2.5 videosu çek' fikir notu |
| altyazı | MVVM mimarisi açıklanıyor | aday değil: genel kavram | 1:37 'MVVM mimarisi ile çalışacağız' |
| altyazı | Backend ve senkronizasyon kavramları anlatılıyor | aday değil: genel kavram | 2:25 'Backend gerekiyor mu? Lokal veri tabanı yeterli' |
| altyazı | API kavramı anlatılıyor | aday değil: genel kavram | 2:41 'API'de uygulamayla servisin belirli kurallara göre haberleştiği bir arayüz' |
| altyazı | Sözlükte 'Inter' eşleşmesi (2:41) | aday değil: genel kavram | 2:41 'Inter' eşleşmesi belirsiz; konuşmada kullanılmıyor |
| altyazı | CLAUDE.md dosyası ve rolü anlatılıyor | CLAUDE.md | 3:08 'CLAUDE.md dosyası da bu projede nasıl çalışacağını söylüyor olacak.' |
| altyazı | Skill dosyalarının tanımı anlatılıyor | aday değil: genel kavram | 3:08 'Skill dosyaları ne? ... uzmanlıkla alakalı görevlerin tarifleri' |
| altyazı | MCP kavramı anlatılıyor, videoda kullanılmıyor | aday değil: genel kavram | 3:08 'MCP... AI araçlarının dış araçlara bağlanmasını sağlayan bir standart' |
| altyazı | Ses altyazısında 'claude-mem' bulanık eşleşmesi (CLAUDE.md) | aday değil: genel kavram | 3:08 'claudemd' bulanık eşleşme; ayrı araç değil |
| kare | Slaytta 'RIVE' yazısı | aday değil: konu dışı | 3:08 ekran metni 'RIVE' belirsiz; videoda kullanılmıyor |
| altyazı | Ses altyazısında 'claude-api' bulanık eşleşmesi (4:04) | aday değil: genel kavram | 4:04 'claudea' bulanık eşleşme; ayrı araç olduğu doğrulanamadı |
| altyazı | settings.json ile izinlerin tanımlanması | settings.json | 4:04 'settings, JSON'lar ne yapıyor? ... izin sormadan yapabileceğini' |
| altyazı | SwiftUI Engineering skill dosyasının gösterilmesi | SwiftUI Engineering skill | 4:04 'Skill'de SwiftUI Engineering dediğimiz skill MD dosyamız var.' |
| altyazı | Implement Feature komut dosyasının anlatılması | /implement-feature | 4:04 'Implement Feature MD dediğimiz Claude'a yeni bir özelliği...' |
| altyazı | swift-review komut dosyasının anlatılması | /swift-review | 4:04 'swift-review.md dosyamız da buradaki hataları nasıl kontrol etmiş.' |
| kare | settings.local.json içinde WebFetch alan adı izinleri | aday değil: başka adayın parçası (settings.json) | 4:22 'WebFetch(domain:developer.apple.com)' ve diğer alan adları |
| kare | settings.local.json içinde Bash(xcodebuild:*), Bash(xcrun:*) ve Bash(swift:*) izinleri | aday değil: başka adayın parçası (settings.json) | 4:22 izin listesinin ilk satırları |
| kare | Ürün tarifi dosyası PRODUCT-SPEC.md | aday değil: başka adayın parçası (ideBox Claude Code kiti) | 4:28 'PRODUCT-SPEC.md (scope)' ve kare 5:08 |
| kare | ARCHITECTURE, DATA-PERSISTENCE, DESIGN-SYSTEM, ANIMATION ve PERFORMANCE dosyaları | aday değil: başka adayın parçası (ideBox Claude Code kiti) | 4:38 'Models, queries, migrations, repository / DATA-PERSISTENCE.md' ve diğer docs satırları |
| kare | SKILL.md içinde SwiftUI View kodu | SwiftUI | 4:32 'struct IdeaListView: View' |
| kare | Skill test kurallarında Swift Testing geçiyor | Swift Testing | 4:34 '#require, arguments:' ve 'Test.cancel() instead of XCTSkip' |
| kare | Skill'de Swift 6 strict concurrency kuralları | Swift | 4:38 'Swift 6 strict concurrency (default MainActor, @ModelActor, @concurrent)' |
| kare | Skill'de String Catalog localization kuralı | String Catalog | 4:42 'String Catalog localization and Swift Testing' |
| kare | Sözlükte 'Instrument Serif' eşleşmesi (4:38) | aday değil: konu dışı | 4:38 'Instruments' kelimesinin yanlış eşleşmesi |
| kare | Sözlükte 'Framer Motion' ve 'Descript' eşleşmeleri (4:28) | aday değil: konu dışı | 4:28 'motion tokens' ifadesinin yanlış eşleşmesi |
| kare | Sözlükte 'Emotion' eşleşmesi (4:34) | aday değil: konu dışı | 4:34 'motion' ifadesinin yanlış eşleşmesi |
| kare | Sözlükte 'Go' eşleşmesi (4:48) | aday değil: konu dışı | 4:48 yanlış eşleşme; videoda kullanılmıyor |
| kare | Sözlükte 'Next.js' eşleşmesi (5:28) | aday değil: konu dışı | 5:28 yanlış eşleşme; videoda kullanılmıyor |
| kare | Sözlükte 'Linear' eşleşmesi (6:00) | aday değil: konu dışı | 6:00 yanlış eşleşme; videoda kullanılmıyor |
| kare | Foundation Models ve planlanan Spotlight, AlarmKit özellikleri spec'te yer alıyor | aday değil: konu dışı | 5:14 'Foundation Models suggestions · iCloud sync · rich text · reminders' |
| kare | Swift review komutunun prompt metni ekranda | /swift-review | 4:48 'Swift Review: $ARGUMENTS' ve 'Review the given files' |
| kare | SKILL.md rol tanımı ekranda | SwiftUI Engineering skill | 4:56 'You are a senior iOS engineer (8+ years)' |
| kare | Instruments kontrol listesi PERFORMANCE.md içinde | Instruments | 5:24 '## 6. Instruments Checklist' |
| kare | Liquid Glass tasarım kuralları | Liquid Glass | 5:32 'Liquid Glass can no longer be opted out of' |
| kare | Apple'ın hazırladığı framework MD'leri (AdditionalDocumentation) | aday değil: başka adayın parçası (ideBox Claude Code kiti) | 6:00 'Implementing Liquid Glass Design.md' ve diğer Apple MD listesi |
| altyazı | Xcode içindeki Apple dokümanları | aday değil: başka adayın parçası (Xcode) | 6:18 'Apple'ın Xcode içindeki dokümanları' |
| altyazı | StoreKit servisi dokümanı örnek olarak anılıyor | aday değil: genel kavram | 6:18 'StoreKit Updates MD'yi ... referans veriyor'; videoda kullanılmıyor |
| altyazı | README.md dosyası ve referans tablosu | aday değil: başka adayın parçası (ideBox Claude Code kiti) | 6:52 'Readme MD'de buradaki tüm dosyaların ne zaman okuması gerektiği' |
| kare | README'de /implement-feature komut satırı | /implement-feature | 6:40 '+ /implement-feature <description>' |
| kare | Claude Code sürüm ve plan bilgisi ekranda | Claude Code | 7:20 'Claude Code v2.1.291' ve 'Opus 5.5 (1M context)' |
| kare | Claude Max abonelik bilgisi ekranda | aday değil: konu dışı | 7:20 'Opus 5.5 (1M context) · Claude Max' abonelik adı |
| kare | Terminal başlığında caffeinate ibaresi | aday değil: genel kavram | 7:48 'caffeinate - claude' başlığı; komut elle yazılmadı |
| kare | Terminal başlığında sourcekit-lsp ibaresi | aday değil: genel kavram | 8:04 'sourcekit-lsp - claude' başlığı |
| kare | Claude özetinde /config komutu anılıyor | aday değil: başka adayın parçası (Claude Code) | 8:08 '(disable recaps in /config)' metni |
| kare | CloudKit konteyner kimliği ekranda | aday değil: konu dışı | 7:52 'iCloud.com.onuryildirim.ideBox' metni |
| kare | Dosya ağacında AirDrop ve iCloud Drive klasörleri | aday değil: konu dışı | 3:58 Finder kenar çubuğunda AirDrop ve iCloud Drive |
| kare | Dosya aktarımı yöntemi olarak AirDrop geçiyor | aday değil: konu dışı | 3:58 'AirDrop' ekran metni |
| kare | Sözlükte 'Llama' eşleşmesi (7:52) | aday değil: konu dışı | 7:52 ekranda 'Llama' yazısı; videoda araç olarak kullanılmıyor |
| ses | Sözlükte 'fal.ai' bulanık eşleşmesi (7:14) | aday değil: genel kavram | 7:14 'falan' bulanık eşleşme; araç olarak anılmıyor |
| ses | MarkItDown bulanık eşleşmesi (9:15), markdown dışa aktarımı | aday değil: genel kavram | 9:15 'markdown olarak dışarı aktar'; araç adı değil |
| kare | Uygulamanın Markdown olarak dışa aktarma özelliği | aday değil: konu dışı | 9:15 ayarlar ekranında 'Markdown Olarak Dışa Aktar' |
| kare | Xcode simülatörü (iPhone 18 Pro) kullanılıyor | aday değil: başka adayın parçası (Xcode) | 8:15 'Direkt 18 Pro simülatöre run ettim.' |
| açıklama | ideBox proje dosyalarının GitHub deposu | ideBox Claude Code kiti | açıklama 'github.com/onuryildriim/idebox-claude-code' bağlantısı |
| açıklama | Claude Code resmi kurulum rehberi | aday değil: genel kavram | açıklama 'Claude Code'u hiç kurmadıysan resmi kurulum rehberi' |
| açıklama | Claude Code 101 ücretsiz kurs | aday değil: konu dışı | açıklama 'Ücretsiz başlangıç kursu (Claude Code 101)' |
| açıklama | GitHub platformu olarak anılıyor | aday değil: genel kavram | açıklama bağlantısı github.com; GitHub'ın kendisi araç olarak kullanılmıyor |
| yorum | Yorumda Higgsfield reklamları anılıyor | aday değil: sponsor/reklam | yorum 'higgsfield reklamlarıyla dolu dandik videolardan sonra' |
| yorum | Yorumda ChatGPT soruluyor | aday değil: konu dışı | yorum 'Ben chatgpt 20 dolarlık paketi kullanıyorum' |
| yorum | Yorumda Codex karşılaştırması soruluyor | aday değil: konu dışı | yorum 'codex ve claude'ın 20 usd paketleri için hangisi' |
## Kareden okunanlar
- 0:54: Terminalde '> cl' yazısı
- 1:00: '> claude' · 'Claude Code' · 'model: Opus 5.5 · güncel'
- 1:08: 'ideBox · fikir kutusu' ve örnek fikir metni 'Higgsfield'
- 2:00: 'BUNU DEĞİŞTİR · DİĞERLERİ ETKİLENMEZ' ve View, ViewModel, Model kutuları
- 3:08: 'CLAUDE.md · GİRİŞ KAPISI' ve '.claude/docs/' ağacı
- 3:28: CLAUDE.md maddeleri: 'Kodun yapısı', 'Teknolojiler', 'Mimari'
- 4:22: settings.local.json izinleri: WebFetch alan adları, WebSearch, Bash(xcodebuild:*)
- 4:28: PRODUCT-SPEC.md ve 'APIs (iOS 27 SDK). Correct, simple, testable, accessible'
- 4:32: SKILL.md: 'struct IdeaListView: View' ve ViewModel kodu
- 4:48: swift-review: 'Review the given files...' ve 'Swift Review: $ARGUMENTS'
- 5:08: PRODUCT-SPEC: 'Local-first & private... (SwiftData)'
- 5:24: PERFORMANCE.md: '## 6. Instruments Checklist'
- 5:32: Tasarım kuralı: 'Liquid Glass can no longer be opted out of'
- 6:40: README: '+ /implement-feature <description>' ve 'Apple framework references'
- 7:20: 'Claude Code v2.1.291' · 'Opus 5.5 (1M context)' · 'Claude Max'
- 7:48: Terminal başlığı: 'caffeinate - claude'
- 8:08: Claude özeti: '(disable recaps in /config)'
## Belirsizlikler
- Ekranda 'Rive' yazısı (3:08) geçiyor; videoda araç olarak kullanılıp kullanılmadığı belirsiz.
- Ses altyazısında 'claude-mem' (3:08, 'claudemd' bulanık eşleşmesi) ve 'claude-api' (4:04, 'claudea' bulanık eşleşmesi) geçiyor; büyük olasılıkla CLAUDE.md ve Claude Code kastediliyor, ayrı araç olduğu doğrulanamadı.
- Sözlük eşleşmeleri Descript, Framer Motion, Emotion, Instrument Serif, Go, Next.js, Linear, Llama, fal.ai ve MarkItDown büyük olasılıkla yanlış eşleşme (ekrandaki kelime benzerliği veya bulanık ses); videoda araç olarak kullanılmıyor.
- Ekrandaki 'iTerm' (1:00) yazısının terminal uygulamasının adı olup olmadığı net değil.
- Terminal başlıklarında 'caffeinate - claude' (7:48) ve 'sourcekit-lsp' (8:04) görünüyor; bunların elle mi çalıştırıldığı belirsiz.
- 'Opus 5.5' sürüm adı ekranda ve konuşmada geçiyor; resmi sürüm adının doğruluğu bu pakette doğrulanamadı.
- Claude Code kurulumu videoda gösterilmiyor; kurulum adımları açıklama bağlantılarına yönlendiriliyor.
- Gerçek cihaz, iCloud senkronizasyonu ve App Group adımları videoda gösterilmiyor; yalnızca Claude özetinde (8:04–8:08) metin olarak geçiyor.
- Yorumdaki '200 dolarlık paket' ve '20 dolarlık paket' bilgileri fiyat doğrulaması yapılmadan aktarılamaz.
- Açıklama bağlantısındaki idebox-claude-code deposundaki dosyaların videodakiyle birebir aynı olup olmadığı doğrulanamadı.
- EKSİK: rapor (bölüm eksik: ## Site/UI teknikleri)
## Atlanan segment oranı
0/22 (paket tam okuma, motor)
## URL'ler
- yok
## İş akışı
- yok
## Promptlar
- Claude Code'a proje geliştirmeyi başlatmak — iOS 27 ve min SDK iOS 27 olarak ayarlansın; önce tüm MD dosyaları okunsun, sonra proje kurallara uygun şekilde geliştirilmeye başlasın.
- Ürün tarifi dosyasını güncellemek — Proje için PRODUCT-SPEC.md dosyası güncellensin; ürün tarifi projeye göre yeniden yazılsın.
- Swift kodunu proje kurallarına göre incelemek (swift-review) — Verilen dosyalar (yoksa son değişiklikler) CLAUDE.md ve docs/project kurallarına göre incelensin; her sorun dosya, satır, neden ve düzeltme ile raporlansın.
- SwiftUI skill'in rol tanımı — Claude kıdemli bir iOS geliştirici (8+ yıl) gibi davransın; iOS 27 SDK'da doğru, basit, test edilebilir ve erişilebilir üretim kodu yazsın.
- Yeni özellik geliştirmek (implement-feature) — Yeni bir özellik önce veri, sonra mantık, sonra ekran, sonra test sırasıyla yapılsın.
