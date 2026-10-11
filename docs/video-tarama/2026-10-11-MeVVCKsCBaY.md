# Claude Skills Nedir? Bir Kez Öğret, Hep Kullan
## Künye
Claude Skills Nedir? Bir Kez Öğret, Hep Kullan · Berko · süre: 16:53 · tr-orig · https://youtu.be/MeVVCKsCBaY · şema 2
motor: parti 2026-10-11-uzun-2 · claude-sonnet-5-5 · hafif claude -p
kareler: yok
kare yok: yt-dlp rc=1: ERROR: unable to download video data: HTTP Error 403: Forbidden
claude-sonnet-5-5: claude-sonnet-5-5 · 31302 tk · claude-haiku-5-5: claude-haiku-5-5 · 58648 tk
## Özet
Berko, tekrar eden uzun prompt'ları Claude Skills'e dönüştürmeyi anlatıyor. Haftalık özet örneğiyle SKILL.md yapısını (name ve description front matter'ı), Claude'un skill'i description üzerinden nasıl seçtiğini ve bağlamın nasıl yönetildiğini açıklıyor. Skill'in Claude'a yazdırılmasını öneriyor. Warp, Herdr, Skill Creator, Superpowers, Matt Pocock ve Karpathy skill'lerini gösteriyor, çıktıya bakıp skill'i yinelemeyi (iterasyon) anlatıyor. Zincirleme çalışan 'genel analiz' skill'ini örnekliyor ve ilk skill için 5 adım veriyor. Kare görseli alınamadığı için (indirme 403) her şey altyazı ve açıklamaya dayanıyor.
## Bölümler
- 0:00 Skill nedir? Haftalık özet örneği
- 1:06 Tekrar eden işi neden skill yapmalı?
- 1:42 SKILL.md'nin içi
- 3:02 Claude hangi skill'i seçer?
- 3:45 Skill'ler bağlamı nasıl kullanır?
- 5:29 İlk skill'i oluştur ve test et
- 6:39 Warp ve Herdr
- 8:13 Skill Creator ile skill oluşturma
- 10:31 Superpowers ve herkese açık skill örnekleri
- 13:53 Sonuca bakıp skill'i iyileştirme
- 14:31 Skill zinciri: genel analiz
- 16:13 İlk skill için beş adım
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Skills | yok | skill | yok | Tekrar eden işleri SKILL.md dosyasına yazıp description eşleşmesiyle otomatik çalıştıran Claude özelliği | 0:00 | Skill nedir, nasıl kullanılır, nasıl oluşturulur anlatılıyor; haftalık özet skill'i örnek. |
| SKILL.md | yok | teknik | yok | Başında name ve description front matter'ı olan, talimatları içeren Markdown dosyası | 1:42 | Skill'in içinde ne var? Dediğim gibi bir MD file, Markdown dosyası. |
| Claude Code | yok | CLI | yok | Skill'lerin gerçek ortamda denendiği ve haftalık limit uyarısına takılınan ajan aracı | 6:29 | Açıklamada gerçek Claude Code denemesinde haftalık limite takıldığı yazıyor; deneme 6:29'da başlıyor. |
| Claude | yok | CLI | yok | Skill'leri seçip çalıştıran ana yapay zekâ modeli/ajanı | 0:00 | Burada cloud olur, Codex olur; modellerin çoğu skill biliyor. |
| Codex | yok | CLI | yok | Skill destekleyen alternatif yapay zekâ aracı olarak anıldı | 0:00 | Cloud olur, Codex olur, farklı depsepsek gibi modeller de olur. |
| DeepSeek | yok | CLI | yok | Skill destekleyen alternatif model olarak anıldı (altyazıda 'depsepsek') | 0:00 | Farklı depsepsek gibi modeller de olur; onları da kullanabilirsiniz. · kanıt: yok |
| Warp | yok | CLI | yok | Konuşmacının terminal olarak kullandığı uygulama | 6:39 | Ben burada terminal olarak warp kullanıyorum; bu warp'ın sitesi. |
| Herdr | yok | CLI | https://github.com/herdrdev/herdr | Birden fazla ajan oturumunu yöneten, terminal kapansa da arka planda çalışan ve sesli bildirim veren araç | 6:39 | Warp'ın içinde herder kullanıyorum; birden fazla agent'ı görüntülemenizi sağlıyor. |
| Whisper | yok | CLI | yok | Sesli komutla prompt vermek için kullanılan konuşma tanıma aracı | 8:13 | Ben bu arada sesli komut olarak whisper kullanıyorum. |
| Skill Creator | yok | skill | yok | Claude'un yerleşik, skill üretmek ve mevcut skill'leri düzenlemek için kullanılan skill'i/eklentisi | 8:13 | Skill creator skillini kullanabilirsiniz; Claude'un kendi plugin built-in skill'lerinden biri. |
| Superpowers | yok | plugin | https://github.com/obra/superpowers | Brainstorming, plan ve alt ajan akışı sunan skill/eklenti paketi | 10:31 | Super powers benim çok sevdiğim skill'lerden biri; repo gösteriliyor. |
| Brainstorming | yok | skill | yok | İşi netleştirip plan ve spec dosyaları çıkaran Superpowers skill'i | 10:31 | Brainstorming skili size bir işi netleştiriyor, sonra planlamasını yazıyor. |
| Visual Companion | yok | skill | yok | Tasarım seçeneklerini (A/B/C) yerel sunucuda gösteren Superpowers özelliği | 11:32 | Tasarımı lokal server olarak kaldırıp A, B, C seçeneği gösteriyor. |
| Sub-agent | yok | teknik | yok | Planı alt ajanlarla yürütme seçeneği; daha çok token harcar | 11:32 | Ben genellikle sub agent'ı tercih ediyorum; biraz daha fazla token tüketiyor. |
| Matt Pocock Skills | yok | skill | https://github.com/mattpocock/skills | Gereksizleri çıkarıp mühendislik bakışıyla ilerleyen herkese açık skill deposu (Skills for Real Engineers) | 11:32 | Medpok'un bir skill var; gerçek mühendislik açısıyla dosyalara bakıyor. |
| Karpathy Guidelines | yok | skill | https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md | Kodlamadan önce düşün, basitleştir, cerrahi değişiklik yap ve hedefe göre doğrula ilkelerini içeren skill | 12:33 | Kodlamadan önce düşün, basite indirge; sadece gereken dosyalara dokun. |
| CLAUDE.md | yok | teknik | yok | Talimatların her oturumda bağlama yüklendiği proje dosyası; skill'lerle karşılaştırıldı | 3:45 | Bir cloud MD dosyamız varsa ve 20 skill varsa description'lar kontekste tutulur. |
| /skills | yok | ipucu | yok | Mevcut skill'leri listeleyip açıp kapatmaya ve aramaya yarayan menü | 9:14 | Slash skills deyince var olan skillerinizi görebiliyorsunuz; aktive edip kapatabiliyorsunuz. |
| Eklenti marketplace'i | yok | plugin | yok | Eklentileri aratıp yüklemeye ve etkinleştirip kapatmaya yarayan Claude Code menüsü | 10:17 | Marketplace olarak taratabiliyorsunuz; financial services built-in skill'ler gibi. · kanıt: yok |
| YouTube eklentisi | yok | plugin | yok | YouTube videosu izletmek için kullanılan eklenti (adı verilmedi) | 13:33 | YouTube videosunu izletmek için bir plugin kullanıyorum. · kanıt: yok |
| genel analiz | yok | skill | yok | Konuşmacının slash ile çağırdığı, alt skill'leri zincirleyen finans analiz skill'i | 14:31 | Genel analiz yap dediğimde tek skill çağırıyorum; arka planda birden fazla skill çalışıyor. |
| yatırım tartışma | yok | skill | yok | Alt ajanlarla çalışan, 0-10 arası puan veren zincirdeki skill | 15:32 | Yatırım tartışma diye bir skillim var; en son 0 ile 10 arasında puan veriyor. |
| platform rapor | yok | skill | yok | Analiz sonucunu platform raporuna yazan zincir skill'i | 15:32 | Platform rapor skili ile platform raporuna yazıyor. |
| Telegram | yok | iş akışı | yok | Portföy sesli brifinginin gönderildiği kanal | 15:32 | Portföyün çıktısını bana Telegram'dan sesli bir şekilde atıyor. |
| Yahoo Finance | yok | iş akışı | yok | Finans haberlerinin çekildiği site | 14:31 | Finans için Yahoo Finance'e gidiyor, Bloomberg'e gidiyor. |
| Bloomberg | yok | iş akışı | yok | Finans haberlerinin çekildiği site | 14:31 | Yahoo Finance'e gidiyor, Bloomberg'e gidiyor; haberleri özetletiyor. |
| Twitter | yok | iş akışı | yok | Takip edilen hesapların özetinin toplandığı kaynak | 14:31 | Twitter'da takip ettiğim kanalların özetlerini topluyor. |
| YouTube | yok | iş akışı | yok | Takip edilen kanalların transkriptlerinin çekilip özetlendiği kaynak | 14:31 | İlk YouTube'u tarıyor, her kanalın transkriptini çekiyor. |
| graf | yok | skill | yok | Dosya düzenini tutan ve notlara göre token tasarrufu sağlayan araç; tam adı belirsiz. | 9:14 | graf kullanıyorum |
| Cursor | yok | teknik | yok | Superpowers'ın plugin olarak sunulduğu IDE. | 10:31 | Cursor için, Codex için vesaire |
| Hermes Agent | yok | teknik | yok | Superpowers'ın plugin olarak sunulduğu agent aracı. | 10:31 | PHP için Hermes agent'ta da yine |
| Tekrar eden prompt'un neden skill'e dönüştürülmesi gerektiğini göstermek | yok | prompt | yok | Pazartesi'den itibaren her gün aynı prompt'u yazma örneği: notlar klasöründeki bu haftanın notlarını oku. | 1:06 | kaynak: altyazı |
| Skill Creator ile haftalık özet skill'i üretmek | yok | prompt | yok | Skill Creator'ı kullanarak haftalık özet skill'i oluştur. 'Bu hafta ne yaptım' denince klasörü tara, dosyaları incele, özetle ve aktar. Sesli (Whisper) verildi. | 8:13 | kaynak: altyazı |
| Açıklamadaki haftalık özet skill'ini oluşturma prompt'u | yok | prompt | yok | Haftalik-ozet skill'i .claude/skills altında oluşturulsun. notlar/ klasöründeki bu haftanın dosyalarını okusun; sorunlar, kararlar, açık işler başlıklarında toplasın. Her maddeye kaynak dosya adı, açık işe son tarih (yoksa belirtilsin) eklensin. Çıktı ozetler/YYYY-MM-DD.md dosyasına yazılsın. Tetikleyici: 'bu hafta ne yaptım' veya 'haftalık özet'. Kural: notlarda olmayan bir şeyi uydurmasın. | açıklama | kaynak: açıklama |
| İzleyicinin kendi tekrar eden işi için başlangıç prompt'u (sabit yorum) | yok | prompt | yok | Genel şablon: [skill-adı] adlı skill oluştur; [dosya/bilgiler] ile [işi] yapsın; sık söylenen cümleyle çalışsın; çıktı biçim/konumu belirtilsin; yasaklara uysun. SKILL.md'yi yazıp yeni oturumda dene; tetiklenmezse description'ı, sonuç eksikse talimatları düzelt. | açıklama | kaynak: açıklama |
| Description'ın tetiklemedeki önemini göstermek | yok | prompt | yok | Skill'i test etmek için 'bu hafta ne yaptım' ve 'haftalık özet' denir; description anlamsız yazılırsa skill tetiklenmez, düzeltilince tekrar çalışır. | 5:29 | kaynak: altyazı |
| Skill'i çıktıya bakarak yinelemeyle iyileştirmek | yok | prompt | yok | Çıktıya bakıp skill'i güncelle: yeni sorunları en üste al, her açık işe son tarih ekle ve bunu skill'e yaz. | 13:53 | kaynak: altyazı |
## Açıklama bağlantıları
- https://code.claude.com/docs/en/skills — Claude Skills resmi rehberi · aday: evet (Claude Code) · Alan adı videoda kullanılan Claude Code aracını adlandırıyor; resmi dokümantasyon. · sınıf: diğer
- https://www.warp.dev/download — Warp indirme sayfası · aday: evet (Warp) · Videoda terminal olarak kullanılan Warp'ın indirme sayfası. · sınıf: diğer
- https://herdr.dev/ — Herdr ana sayfası · aday: evet (Herdr) · Videoda kullanılıp gösterilen Herdr aracının sitesi. · sınıf: diğer
- https://github.com/obra/superpowers — Superpowers deposu · aday: evet (Superpowers) · Videoda repo açılıp anlatılan Superpowers eklentisi. · sınıf: diğer
- https://github.com/mattpocock/skills — Matt Pocock skill deposu · aday: evet (Matt Pocock Skills) · Videoda örnek olarak anlatılan, izleyicinin kullanabileceği skill deposu. · sınıf: diğer
- https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md — Karpathy Guidelines SKILL.md dosyası · aday: evet (Karpathy Guidelines) · Videoda açılıp içeriği gösterilen skill dosyası. · sınıf: diğer
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| herdr | Herdr'ı açar; çalışan agent oturumlarını listeler ve yönetir. | 6:39 | altyazı |
| Ctrl+B ve Q | Herdr görünümünü kapatır; agent arka planda çalışmaya devam eder. | 8:13 | altyazı |
| /skills | Mevcut skill'leri listeler; etkinleştirme ve kapatma buradan yapılır. | 9:14 | altyazı |
| /fatura tablo | Fatura tablo skill'ini elle çağırır. | 2:43 | altyazı |
| /genel analiz | Zincirleme genel analiz skill'ini tetikler; alt skill'leri sırayla çalıştırır. | 14:31 | altyazı |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Claude yalnızca skill'lerin description alanını bağlamda tutar; talimatlar skill çağrılınca yüklenir, diğer skill'ler yer kaplamaz. | 3:45 | özellik |
| Skill seçimi yalnızca description alanıyla eşleşerek yapılır; SKILL.md gövdesine bakılmaz. | 1:42 | özellik |
| Anthropic skill'leri 500 satırın altında tutmayı tavsiye ediyor. | 4:45 | öneri |
| Skill'ler doğal dille ya da /skill-adı ile elle çağrılabilir. | 3:02 | özellik |
| Proje özelinde skill'i proje içinde tutmak, genel (kullanıcı düzeyi) skill'e göre bağlam karışmasını önler. | 2:43 | öneri |
| Herdr, terminal kapansa bile ajanları arka planda çalıştırır ve iş bitince sesli bildirim verir. | 6:39 | özellik |
| Sub-agent yürütmesi normale göre biraz daha fazla token tüketir. | 11:32 | karşılaştırma |
| Matt Pocock skill deposunun yaklaşık 270.000 yıldızı var. | 11:32 | sayısal |
| Karpathy skill deposu yaklaşık 215.000 yıldız almış. | 11:32 | sayısal |
| Açık bırakılan tüm eklentiler bağlamda yer kaplar; gerektiğinde etkinleştirip kapatmak gerekir. | 13:33 | öneri |
| İlk sürüm mükemmel olmaz; çıktıya bakıp skill'i düzeltip yinelemek en iyi sonucu verir. | 13:53 | öneri |
| İlk etapta skill'i kendiniz yazmak yerine Claude'a tarif edip yazdırın. | 5:29 | öneri |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| konuşma 0:00 | Claude Skills | Claude Skills | Videonun konusu: skill nedir ve nasıl oluşturulur. |
| konuşma 0:00 | Deniz kahve dükkanı simülasyonu | aday değil: konu dışı | Haftalık özet örneği için kurgulanan karakter. |
| konuşma 0:00 | Claude | Claude | Skill'i çalıştıran ana model olarak anıldı. |
| konuşma 0:00 | Codex | Codex | Skill destekleyen alternatif olarak anıldı. |
| konuşma 0:00 | DeepSeek (depsepsek) | DeepSeek | Alternatif model olarak anıldı. |
| konuşma 0:00 | haftalık özet skill'i | aday değil: başka adayın parçası (Claude Skills) | Örnek skill, Claude Skills anlatımının parçası. |
| konuşma 1:42 | SKILL.md ve front matter | SKILL.md | name ve description alanları anlatıldı. |
| konuşma 1:42 | Markdown | aday değil: genel kavram | Dosya biçimi olarak anıldı. |
| konuşma 2:43 | Proje düzeyi ve tilda ile genel skill konumu | aday değil: başka adayın parçası (Claude Skills) | Skill'lerin nerede tutulduğu anlatıldı. |
| konuşma 3:02 | Slash ile skill çağırma | Claude Skills | Slash fatura-tablo ile elle çağırma örneği. |
| konuşma 3:45 | CLAUDE.md | CLAUDE.md | Skill'lerle bağlam kullanımı karşılaştırıldı. |
| konuşma 4:45 | Anthropic | aday değil: konu dışı | 500 satır tavsiyesini veren şirket olarak anıldı. |
| konuşma 6:39 | Warp | Warp | Terminal olarak kullanılıyor. |
| konuşma 6:39 | Herdr | Herdr | Warp içinde ajan yönetimi için kullanılıyor. |
| konuşma 8:13 | Skill Creator | Skill Creator | Yerleşik skill ile haftalık özet skill'i oluşturuldu. |
| konuşma 8:13 | Whisper | Whisper | Sesli komut için kullanılıyor. |
| konuşma 9:14 | /skills menüsü | /skills | Mevcut skill'ler listelenip açılıp kapatılıyor. |
| konuşma 9:14 | Brainstorming | Brainstorming | Uzun işlerde sık kullanılan skill. |
| konuşma 9:14 | graf | aday değil: konu dışı | Adı belirsiz; dosya düzeni ve token tasarrufu için kullanıldığı söylendi, belirsizliklerde. |
| konuşma 10:17 | Plugin marketplace ve financial services eklentisi | Eklenti marketplace'i | Marketplace'te aranıp görüntülendi. |
| konuşma 10:31 | Superpowers | Superpowers | Repo gösterildi, iş akışı anlatıldı. |
| konuşma 10:31 | Cursor ve Hermes Agent | aday değil: konu dışı | Superpowers'ın desteklediği araçlar olarak sayıldı. |
| konuşma 11:32 | Sub-agent | Sub-agent | Plan yürütme yöntemi olarak seçiliyor. |
| konuşma 11:32 | Visual Companion | Visual Companion | Tasarım seçeneklerini yerel sunucuda gösteriyor. |
| konuşma 11:32 | Matt Pocock skill'i | Matt Pocock Skills | Altyazıda 'Medpok'; 270.000 yıldız. |
| konuşma 11:32 | Karpathy skill'i | Karpathy Guidelines | SKILL.md içeriği gösterildi. |
| konuşma 13:33 | YouTube izletme eklentisi | YouTube eklentisi | Yüklü eklentiler arasında gösterildi. |
| konuşma 14:31 | genel analiz skill zinciri | genel analiz | Tek slash komutuyla çok skill çalışıyor. |
| konuşma 14:31 | YouTube | YouTube | Kanal transkriptleri çekiliyor. |
| konuşma 14:31 | Twitter | Twitter | Hesap özetleri toplanıyor. |
| konuşma 14:31 | Yahoo Finance | Yahoo Finance | Haber özetleri için gidiliyor. |
| konuşma 14:31 | Bloomberg | Bloomberg | Haber özetleri için gidiliyor. |
| konuşma 15:32 | yatırım tartışma skill'i | yatırım tartışma | Alt ajanlarla 0-10 puan veriyor. |
| konuşma 15:32 | platform rapor skill'i | platform rapor | Sonucu platform raporuna yazıyor. |
| konuşma 15:32 | Telegram | Telegram | Sesli brifing buradan gönderiliyor. |
| açıklama | code.claude.com/docs/en/skills | Claude Code | Resmi skill rehberi bağlantısı. |
| açıklama | warp.dev/download | Warp | Warp indirme bağlantısı. |
| açıklama | herdr.dev | Herdr | Herdr sitesi bağlantısı. |
| açıklama | github.com/obra/superpowers | Superpowers | Superpowers deposu. |
| açıklama | github.com/mattpocock/skills | Matt Pocock Skills | Skill deposu bağlantısı. |
| açıklama | karpathy-guidelines SKILL.md | Karpathy Guidelines | Videoda açılan dosya bağlantısı. |
| açıklama | GitHub | aday değil: konu dışı | Yalnızca depoların barındırıldığı platform; repolar videoda gösterildi. |
| açıklama | haftalik-ozet SKILL.md örneği | aday değil: başka adayın parçası (SKILL.md) | Açıklamadaki örnek dosya içeriği. |
| yorum | Sabit yorum başlangıç prompt şablonu | aday değil: konu dışı | İzleyici için şablon; promptlar bölümünde yer aldı. |
| linkli sayfa agentskills.io | Agent Skills standardı sitesi | aday değil: konu dışı | Videoda anılmıyor; yalnızca docs sayfasındaki bağlantı. |
| linkli sayfa herdr.dev/docs | Herdr dokümantasyonu | Herdr | Herdr sitesinin alt sayfaları. |
| linkli sayfa github.com/herdrdev/herdr | Herdr GitHub deposu | Herdr | Herdr sayfasından bağlanan depo. |
## Kareden okunanlar
- yok
## Belirsizlikler
- Kare görseli yok (indirme 403); ekran içeriği doğrulanamadı, tüm kanıtlar altyazı ve açıklamadan.
- Altyazıda 'graf' geçiyor (9:14); büyük olasılıkla bir bilgi grafı/not aracı ama adı kesin değil, aday yapılmadı.
- 'Matt Pocock' altyazıda 'Medpok', 'Andrej Karpathy' 'Andrev Carpet' diye bozuk; açıklama bağlantılarıyla eşleştirildi.
- Sözlük eşleşmeleri (Matter.js, context7, skill-ui, taste-skill, CapCut, plugin-dev, Skills CLI, Inter, iTerm, Descript) bulanık eşleşme; videoda bu araçların kullanıldığına dair kanıt yok, aday yapılmadı.
- 'fatura tablo' (3:02) ve 'yarın hava nasıl olacak' yalnızca varsayımsal örnek; aday değil.
- Kullanılan YouTube eklentisinin adı söylenmedi.
- Yorumlardaki ve ekranda gösterilen exact sürüm/limit değerleri doğrulanamadı; 270.000 ve 215.000 yıldız sayıları konuşmadan alındı.
- Kurulum komutları: herdr, Ctrl+B Q ve slash komutların yazımı sesten çıkarıldı, birebir yazım emin değil.
## Atlanan segment oranı
0/23 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| https://code.claude.com/docs/en/skills | açıklama | açıklama | hayır |
| https://www.warp.dev/download | açıklama | açıklama | evet |
| https://herdr.dev/ | açıklama | açıklama | evet |
| https://github.com/obra/superpowers | açıklama | açıklama | evet |
| https://github.com/mattpocock/skills | açıklama | açıklama | evet |
| https://github.com/multica-ai/andrej-karpathy-skills/blob/main/skills/karpathy-guidelines/SKILL.md | açıklama | açıklama | evet |
| https://code.claude.com/docs/llms.txt | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/commands | açıklama | açıklama | hayır |
| https://agentskills.io | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/workflows | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/settings-reference#disablebundledskills | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/commands#all-commands | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/setup#configure-release-channel | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/hooks | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/memory#my-claude-md-is-too-large | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/permissions#permission-modes | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/permissions | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/memory#audit-your-instruction-files | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/settings-reference#includegitinstructions | açıklama | açıklama | hayır |
| https://platform.claude.com/docs/en/api/overview | açıklama | açıklama | hayır |
| https://platform.claude.com/docs/en/managed-agents/overview | açıklama | açıklama | hayır |
| https://platform.claude.com/docs/en/build-with-claude/preserved-thinking | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/managed-settings#delivery-mechanisms | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/plugins/overview | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/plugins/loading#plugins-shared-through-a-repository | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/permissions#move-the-session-to-another-directory | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/worktrees | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/worktrees#what-worktrees-share-with-the-main-checkout | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/agent-sdk/typescript#options | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/agent-sdk/python#claudeagentoptions | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/settings-reference#strictpluginonlycustomization | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/headless#start-faster-with-bare-mode | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/cli-reference#cli-flags | açıklama | açıklama | hayır |
| https://code.claude.com/docs/en/permissions#additional-directories-grant-file-access-not-configuration | açıklama | açıklama | hayır |
| https://herdr.dev/docs | açıklama | açıklama | evet |
| https://github.com/herdrdev/herdr | açıklama | açıklama | evet |
| https://github.com/herdrdev/herdr/releases | açıklama | açıklama | evet |
| https://herdr.dev/docs/agents | açıklama | açıklama | hayır |
| https://herdr.dev/docs/session-state | açıklama | açıklama | hayır |
| https://herdr.dev/docs/agent-automation | açıklama | açıklama | hayır |
| https://herdr.dev/docs/integrations | açıklama | açıklama | hayır |
| https://herdr.dev/docs/connecting-machines | açıklama | açıklama | hayır |
| https://herdr.dev/docs/windows-beta | açıklama | açıklama | hayır |
## İş akışı
- 1. adım — Tekrar eden işi belirle: bu hafta notlarından haftalık özet çıkarma — araçlar: Claude Code
- 2. adım — SKILL.md'yi yaz: name ve description ile talimatları ve yasakları tarif et — araçlar: Claude Code, Markdown
- 3. adım — Skill'i proje içinde .claude/skills altına yerleştir — araçlar: Claude Code
- 4. adım — Terminali aç ve Herdr ile agent oturumunu başlat — araçlar: Warp, Herdr
- 5. adım — Skill Creator ile sesli komutla yeni haftalık özet skill'i oluştur — araçlar: Skill Creator, Whisper, Claude Code
- 6. adım — Herdr'dan Ctrl+B ve Q ile ayrıl; agent arka planda çalışmaya devam etsin — araçlar: Herdr
- 7. adım — /skills ile mevcut skill'leri listele ve etkinleştir/kapat — araçlar: Claude Code
- 8. adım — Superpowers plugin'ini marketplace'ten ara ve kur — araçlar: Superpowers, Claude Code
- 9. adım — Brainstorming ile işi netleştir, spec ve plan dosyalarını oluştur — araçlar: Superpowers, Brainstorming
- 10. adım — Visual Companion ile tasarım seçeneklerini yerel sunucuda gösterip seç — araçlar: Superpowers
- 11. adım — Karpathy Guidelines SKILL.md dosyasını incele: kodlamadan önce düşün, basitleştir — araçlar: Karpathy Guidelines
- 12. adım — Yeni bir oturumda skill'i örnek girdilerle test et (fatura tablo, hava durumu) — araçlar: Claude Code
- 13. adım — Çıktıya göre skill'i güncelle: açık işlere son tarih ekle, eski talimatları temizle — araçlar: Claude Code
- 14. adım — Zincirleme genel analiz skill'ini çalıştır; YouTube, Twitter, Yahoo Finance, Bloomberg taramaları — araçlar: Claude Code, YouTube, Twitter, Yahoo Finance, Bloomberg
- 15. adım — Sonucu Telegram'a sesli briefing olarak gönder — araçlar: Telegram
## Promptlar
- Tekrar eden prompt'un neden skill'e dönüştürülmesi gerektiğini göstermek — Pazartesi'den itibaren her gün aynı prompt'u yazma örneği: notlar klasöründeki bu haftanın notlarını oku.
- Skill Creator ile haftalık özet skill'i üretmek — Skill Creator'ı kullanarak haftalık özet skill'i oluştur. 'Bu hafta ne yaptım' denince klasörü tara, dosyaları incele, özetle ve aktar. Sesli (Whisper) verildi.
- Açıklamadaki haftalık özet skill'ini oluşturma prompt'u — Haftalik-ozet skill'i .claude/skills altında oluşturulsun. notlar/ klasöründeki bu haftanın dosyalarını okusun; sorunlar, kararlar, açık işler başlıklarında toplasın. Her maddeye kaynak dosya adı, açık işe son tarih (yoksa belirtilsin) eklensin. Çıktı ozetler/YYYY-MM-DD.md dosyasına yazılsın. Tetikleyici: 'bu hafta ne yaptım' veya 'haftalık özet'. Kural: notlarda olmayan bir şeyi uydurmasın.
- İzleyicinin kendi tekrar eden işi için başlangıç prompt'u (sabit yorum) — Genel şablon: [skill-adı] adlı skill oluştur; [dosya/bilgiler] ile [işi] yapsın; sık söylenen cümleyle çalışsın; çıktı biçim/konumu belirtilsin; yasaklara uysun. SKILL.md'yi yazıp yeni oturumda dene; tetiklenmezse description'ı, sonuç eksikse talimatları düzelt.
- Description'ın tetiklemedeki önemini göstermek — Skill'i test etmek için 'bu hafta ne yaptım' ve 'haftalık özet' denir; description anlamsız yazılırsa skill tetiklenmez, düzeltilince tekrar çalışır.
- Skill'i çıktıya bakarak yinelemeyle iyileştirmek — Çıktıya bakıp skill'i güncelle: yeni sorunları en üste al, her açık işe son tarih ekle ve bunu skill'e yaz.
ikinci göz KAPALI: --ikinci-goz yok
