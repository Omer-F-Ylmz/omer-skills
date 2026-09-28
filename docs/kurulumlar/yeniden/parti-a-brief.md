# Parti A brief — 2026-09-28 (Desktop ikinci görüş girdisi)

Kaynak: `video brief` × 4 tarama raporu + katman raporu (docs/kurulumlar/2026-09-28-uygula.md). 24a K7 ile yeniden üretildi; katman bölümü son koşudan (24a-kapanış).

## brief: 2026-09-28-NyNScAc2u_o.md
### Adaylar
- GSAP · teknik · Kartların dönüşü ve hover geçişlerindeki yumuşak animasyonu sağlıyor (2:37)
- Vanilla JavaScript ile framework'süz tek sayfa · teknik · Kütüphane bağımlılığı olmadan tek sayfalık 3D sitenin kurulması (2:37)
- Claude ile prompt'tan proje üretme · iş akışı · Uzun, ayrıntılı prompt'u yapıştırıp Claude'a projeyi sıfırdan kurdurma (7:45)
- Dosya yapısını prompt'ta 4-5 kez tekrarlama · ipucu · AI'ın halüsinasyon yapmadan index.html/styles.css/script.js yapısını doğru kurmasını sağlıyor (4:42)
- Görselleri public/ klasörüne koyup AI'a aldırma · ipucu · AI'ın görselleri doğrudan projeye dahil edip rastgele/dengeli dağıtmasını sağlıyor (4:42)
- Renk paleti ve font ailesini prompt başında sabitleme · ipucu · AI'ın rastgele font/renk seçmesini engelleyip marka kimliğine sadık kalmasını sağlıyor (5:44)
- 3D perspective detayını prompt'ta açıkça belirtme · ipucu · Kartların doğru açı/incelik ile sahneye yerleşmesini sağlayan kritik prompt detayı (5:44)
- "Tasarımı değiştirme, aynen üret" talimatı · ipucu · AI'ın kendi yorumunu katmadan tarif edilen tasarıma birebir sadık kalmasını sağlıyor (2:37)
- Prompt'u yayınlamadan önce 5-10 kez test etme · iş akışı · Aynı prompt'un tutarlı/aynı çıktı vermesini garanti altına almak için tekrarlı deneme (9:11)
- Awwwards'tan ilham/analiz alma · ipucu · Ödüllü sitelerin tasarımını inceleyip kendi projesine referans yapma (1:03)
- 3D galeri build prompt'u · prompt · CLOU'dan ilhamla 3D dairesel galeri sitesini uçtan uca tarif eden prompt (6:14)
### Departman
- 3d-perspective-detayını-prompt-ta-açıkça → frontend · KUR
- görselleri-public-klasörüne-koyup-ai-a-a → frontend · KUR
- renk-paleti-ve-font-ailesini-prompt-başı → frontend · KUR
- nyns-3d-galeri-promptu/3d-dairesel-ring-galeri → frontend · ZATEN VAR
- nyns-3d-galeri-promptu/scroll-mouse-parallax-rotasyon → frontend · UYARLA
### İddialar
- Bu kalitede profesyonel bir 3D site 50.000-100.000 dolar aralığında (1:03 · sayısal)
- CLOU sitesi Awwwards'ta 2022'de Site of the Day seçildi, puan 7,62/10 (1:34 · sayısal)
- Galeri 136 görsel kullanıyor, tekrar eden havuzdan rastgele/dengeli dağıtılıyor (4:42 · sayısal)
- Prompt hazırlığı yaklaşık 2 gün sürüyor, her prompt 5-10 kez test ediliyor (9:11 · sayısal)
- Böyle siteler eskiden 2-3 haftada yapılırdı, AI ile artık çok daha hızlı (9:11 · karşılaştırma)
- Dosya yapısı talimatı halüsinasyonu önlemek için prompt içinde 4-5 kez tekrarlanıyor (4:42 · öneri)
### Site/UI
- 3D dairesel (ring) galeri kart dizilimi, transform-style:preserve-3d · tahmin: vanilla CSS 3D transform + GSAP · bizde: yok
- Scroll'a bağlı saat yönü/ters yönü dönüş · tahmin: GSAP · bizde: yok
- Hover'da kart yumuşak kayma/uzaklaşma geçişi · tahmin: GSAP · bizde: yok
- Mouse Y eksenine bağlı galeri parallax hareketi · tahmin: GSAP + JS mousemove · bizde: yok
- Dönerek açılan yükleme ekranı (loader→intro akışı) · tahmin: GSAP timeline · bizde: yok
- Masaüstü/mobil için tek kod tabanında ayrı davranış (breakpoint) · tahmin: CSS media query / JS breakpoint · bizde: yok
### Prompt anatomisi
- "Tasarımı değiştirme, birebir üret" talimatı · 3:37 · şablon: kabul
- Dosya yapısını 4-5 kez tekrarlama (halüsinasyon önleme) · 4:42 · şablon: dosya
- Görselleri public/'a koy, AI otomatik alsın · 4:42 · şablon: asset
- Renk paleti ve fontu prompt başında sabitleme · 5:44 · şablon: config
- 3D perspective'i sayısal olarak belirtme (PERSPECTIVE 1600) · 5:44 · şablon: config
- Fisher-Yates shuffle ile görselleri kartlara dengeli dağıtma · 4:42 · şablon: asset
- Tüm sayısal sabitleri EXACT CONSTANTS altında toplama · 6:14 · şablon: config
### Linkler
- https://youtu.be/NyNScAc2u_o
- https://www.awwwards.com/sites/clou

## brief: 2026-09-28-Gg35_iQWx7g.md
### Adaylar
- Claude Code · iş akışı · Terminalde çalışan ana araç; paralel çoklu terminal ile farklı işleri takip ettirme (0:00)
- Skills (yetenekler) · teknik · Claude'a hazır sistem promptu ekleyerek belirli bir işte daha iyi çalışmasını sağlama (2:24)
- skills.sh · teknik · 1 milyondan fazla hazır yetenek barındıran pazar yeri (2:54)
- frontend-design (skill) · skill · Jenerik olmayan, üretim kalitesinde frontend arayüz tasarımı üretir (2:54)
- npx skills add <repo> --skill <ad> · CLI · anthropics/skills reposundan tek komutla belirli bir yeteneği kurma (2:54)
- Codex · teknik · Claude Code'a alternatif olarak anılan başka bir kod ajanı (4:04)
- Antigravity · teknik · Claude Code'a alternatif olarak anılan bir araç (4:04)
- MiMo V2.5 (Xiaomi) · teknik · Opus'a göre ~11 kat ucuz, basit işlerde (ör. email yazma) benzer sonuç veren model (4:04)
- Fable (model adı) · teknik · Anılan bir model adı, Opus/Sonnet ile birlikte /model listesinde geçiyor (ASR şüpheli) (4:04)
- OpenRouter · teknik · Farklı modellerin token kullanımı/fiyatına göre sıralamasını gösteren platform (9:08)
- Hermes (ajan) · iş akışı · Kendi kendini geliştiren, sürekli çalışan otonom yapay zeka ajanı; reklam işlerinde kullanılıyor (4:45)
- MCP · MCP · Email, CRM, ERP gibi uygulamaları Claude'a bağlayan protokol (6:19)
- Email MCP entegrasyonu · iş akışı · Gelen kutusunu kategorize edip geçmiş yanıtlara bakarak otomatik cevap taslağı üretme (6:19)
- Şirket verisini (CRM/ERP) bağlama · iş akışı · Reklam/satış/CRM/ERP verisini bağlayıp haftalık analiz ve öneri ürettirme (7:19)
- /loop · CLI · Bir hedefi sürekli otomasyon mantığında tekrar ettirme (9:26)
### Departman
- kural-claude-code-btw-loop-goal-resume-plugin → surec-ajan-arac · RED
- paralel-terminal-ile-çoklu-görev-takibi → surec-ajan-arac · KUR
- plugin-ile-model-listesine-model-ekleme → surec-ajan-arac · ÖĞREN
- projeyi-sürekli-github-a-yükleme → surec-git-yayin · KUR
- skills-cli/skill-kurma → surec-ajan-arac · ZATEN VAR
- skills-cli/gecici-kullan → surec-ajan-arac · ZATEN VAR
### İddialar
- Xiaomi'nin modeli (MiMo V2.5) Opus'tan yaklaşık 11 kat daha ucuz (4:04 · sayısal)
- Kodlamada Opus çok daha iyiyken email yazımında ucuz model (MiMo V2.5) benzer sonuç veriyor (4:04 · karşılaştırma)
- frontend-design skill'i 721.0K kurulum ve 165.1K GitHub yıldızı almış (2:54 · sayısal)
- OpenRouter sıralamasında Claude Sonnet 5 ~559B token, Claude Opus 4.8 ~391B token kullanılmış (9:08 · sayısal)
- Hermes tarzı ajanlar çok fazla token tükettiği için (ucuz modelle çalıştırılmadıkça) nadiren görülüyor (8:51 · özellik)
- MCP ile saatler sürecek bir iş 15 dakikada yapılabiliyor (6:19 · öneri)
- Aynı anda ~16 terminal ile paralel iş yürütülüyor (0:00 · sayısal)
### Site/UI
- Estetik yön seçimi (brütalist/maksimalist/retro-fütüristik/lüks/organik) sonra uygulama · tahmin: frontend-design skill (anthropics/skills), kütüphane belirtilmemiş · bizde: yok
- Tipografi, renk (CSS variables), motion tasarımı, mekansal kompozisyon temel tasarım sütunları olarak vurgulanıyor · tahmin: frontend-design skill, HTML/CSS/JS/React/Vue çıktısı (ekranda yazılı) · bizde: yok
### Prompt anatomisi
- yok (bu videonun prompt adayı yok)
### Linkler
- https://youtu.be/Gg35_iQWx7g
- https://skills.sh
- https://github.com/anthropics/skills
- https://openrouter.ai

## brief: 2026-09-28-JNM_rxqtlvY.md
### Adaylar
- Caveman · skill · Claude'a kısa, süssüz konuşma talimatı verip çıktı token'ını düşürür (2:08)
- claude-usage (phuryn) · CLI · Yerel session loglarını okuyup token kullanımını gösteren ücretsiz dashboard/JSON API (4:13)
- Düzeltme yerine Edit/Regenerate · ipucu · Yanlış cevaba "onu kastetmedim" gibi düzeltme mesajı atmak yerine mesajı düzenleyip yeniden üretmek bağlamı şişirmez (2:08)
- 15-20 mesajda yeni sohbete geç · iş akışı · Sohbet uzadıkça her mesaj geçmişi yeniden okuduğundan belirli aralıkla yeni sohbet açmak token'ı düşürür (2:52)
- Soruları tek mesajda topla · ipucu · Ayrı ayrı sorular yerine tüm soruları tek mesajda sormak bağlam yüklemesini azaltır, cevabı netleştirir (3:26)
- session.jsonl'den token ölçümü · ipucu · Oturum loglarındaki input_tokens/output_tokens/cache_read alanlarından gerçek token tüketimini görmek (4:13)
- Sık kullanılan dosyaları projeye yükle · iş akışı · Tekrar kullanılan dosyaları (ör. PDF) her seferinde yapıştırmak yerine projeye eklemek tekrarlayan tokeni azaltır (5:15)
- Memory/User Settings'i bir kez kur · ipucu · Rol, iletişim tarzı ve tercihleri her sohbette tekrar yazmak yerine bir kez hafızaya kaydetmek (5:48)
- Kullanılmayan özellikleri kapat · ipucu · Web search, connectors, tools/research, extended thinking açık kaldığında kullanılmasa da arka planda token yakar (6:29)
- Basit işler için Haiku'ya geç · ipucu · Basit görevlerde daha küçük/ucuz modele geçmek token maliyetini düşürür (7:03)
- İşi gün içine yay / sabah erken ping · iş akışı · 5 saatlik kullanım penceresini sabah erken saatte küçük bir mesajla başlatıp günü 2-3 seansa bölmek limiti verimli kullandırır (7:46)
- Yoğun olmayan saatlerde çalış · ipucu · Yoğun saatlerde (hafta içi TR saatiyle öğleden sonra 3'ten akşam 10'a kadar) free modellerde limit daha hızlı tükeniyor, bu saatler dışında çalışmak avantajlı (8:38)
- Overage (limit aşımı) açık tut · ipucu · Güvenlik için limit aşımı özelliğini açık bırakmak kritik anda çalışmanın kesilmesini önler (9:18)
### Departman
- 15-20-mesajda-yeni-sohbete-geç → verimlilik · KUR
- düzeltme-yerine-edit-regenerate → verimlilik · KUR
- soruları-tek-mesajda-topla → verimlilik · KUR
- claude-usage/terminal-ozet → verimlilik · KUR
- claude-usage/web-dashboard → frontend · ÖĞREN
- claude-usage/vscode-entegrasyonu → verimlilik · ZATEN VAR
### İddialar
- 10. mesaj ~5000 token, 30. mesajdaki tek mesaj tam 232.000 token tutuyor (1:00 · sayısal)
- Tokenların %98,5'i eski sohbeti tekrar okumaya, %1,5'i yeni cevabı üretmeye gidiyor (1:00 · sayısal)
- Caveman kullananlar %65'e varan tasarruf sağlamış (2:01 · sayısal)
- Arayüzdeki kullanım çubuğu sadece "%63 kullanıldı" gösteriyor, gerçek token sayısını göstermiyor (4:13 · özellik)
- 26 Mart 2026'dan itibaren yoğun saatlerde (hafta içi TR saatiyle öğleden sonra 3'ten akşam 10'a kadar) free modellerde 5 saatlik limit daha hızlı tükeniyor (8:38 · özellik)
- Haftalık limit değişmiyor, sadece limitin gün içinde nasıl tükendiği değişiyor (8:38 · karşılaştırma)
### Site/UI
- yok (raporda site/UI tekniği yok)
### Prompt anatomisi
- yok (bu videonun prompt adayı yok)
### Linkler
- https://youtu.be/JNM_rxqtlvY
- https://github.com/JuliusBrussee/caveman
- https://github.com/phuryn/claude-usage

## brief: 2026-09-28-jGJ09wdTGDI.md
### Adaylar
- Claude Design · teknik · Prompt ile tam web sitesi tasarımı + React kodu üretme aracı (4:18)
- Adobe Firefly · teknik · İlk+son kareden video üretme (tanıtım videosu) (0:38)
- Veo 3.1 · teknik · Firefly içinde kullanılan video üretim modeli (0:38)
- İlk kare + son kare arası video üretimi · iş akışı · İki görsel verip aradaki 8 sn videoyu AI'a ürettirme (1:39)
- Prompt'u İngilizce yazma · ipucu · AI görsel/video üretiminde İngilizce promptun daha iyi sonuç verdiği gözlemi (1:39)
- Web sitesi yapım promptu (Claude Design'a verilen) · prompt · Saat markası için tam site üretme promptu, ekranda gösteriliyor (3:15)
- Doğal dille düzenleme komutu verme · iş akışı · Üretilen siteyi tek Türkçe cümleyle revize etme ("yazıyı kaldır", "butonları köşeye al") (5:36)
- Üretilen kodu Claude Code'a aktarma · iş akışı · Claude Design çıktısını taşıyıp Claude Code'da düzenleme/optimize önerisi (7:49)
- Component bazlı dosya yapısı · teknik · Üretilen sitenin React component'lere bölünmüş kaynak kodu (7:18)
- Design System / UI kit paneli · teknik · Üretilen sitenin tasarım token'larını ve bileşen kütüphanesini inceleme (9:23)
- Lucide (ikon seti) · teknik · Design System'de kullanılan ikon kütüphanesi (9:23)
- Chrome DevTools cihaz araç çubuğu ile responsive test · ipucu · Farklı cihaz boyutlarında (iPad Mini, iPhone X) sitenin görünümünü kontrol etme (11:24)
- Sayfa performans testi · teknik · Üretilen sitenin performansını ölçüp Claude Design'ın zayıf yanını tespit etme (12:00)
- Rakip/ilham site incelemesi (Rolex.com) · ipucu · Tasarım kalitesini gerçek premium marka siteleriyle kıyaslama (13:26)
- Hostinger (sponsor) · teknik · Video sponsoru; hosting indirim linki (0:00)
### Departman
- chrome-devtools-cihaz-araç-çubuğu-ile-re → test-qa · KUR
- design-system-ui-kit-paneli → frontend · ÖĞREN
- prompt-u-i-ngilizce-yazma → frontend · ÖĞREN
- jgj0-claude-design-promptu/tek-prompt-e-ticaret-sitesi → frontend · UYARLA
- jgj0-claude-design-promptu/dogal-dille-iteratif-revizyon → frontend · ZATEN VAR
- jgj0-claude-design-promptu/ciktiyi-claude-code-a-tasiyip-optimize-etme → frontend · DENE
### İddialar
- Adobe Firefly ile iki kare arasında 8 saniyelik video üretiliyor (1:39 · sayısal)
- İngilizce prompt yazınca AI'nin ürettiği sonuç daha iyi oluyor (1:39 · öneri)
- Claude Design ilk üretimde web sitesi tüm cihazlara uyumlu değildi (5:36 · özellik)
- Claude Design çıktısını Claude Code'a aktarmak daha sağlıklı sonuç veriyor (7:49 · öneri)
- Bu tasarımı yazılımcıların manuel yapması çok zaman alırdı, Claude Design hızlı ve iyi yapmış (7:49 · karşılaştırma)
- iPhone X boyutunda menü ikonları sıkışıyor (10:54 · özellik)
- Üretilen sitenin performans skoru %71 (12:00 · sayısal)
- Claude Design tasarımda güçlü ama performans/teknik tarafta zayıf (12:00 · karşılaştırma)
- Kanal sahibi bundan sonraki web sitesi işlerine Claude Design ile devam edeceğini söylüyor (13:39 · öneri)
### Site/UI
- Prompt'tan tam site (React component'ler) üretimi · tahmin: Claude Design · bizde: yok
- Component bazlı dosya mimarisi (Nav.jsx, ProductCard.jsx, Primitives.jsx...) · tahmin: React · bizde: yok
- Tasarım token sistemi (spacing, corner radii, elevation, renk paleti) · tahmin: design tokens deseni · bizde: yok
- İkonografi kütüphanesi · Lucide 1.25 · bizde: yok
- Tipografi: display + UI + mono font üçlüsü (Cormorant Garamond + Inter + JetBrains Mono) · tahmin: web font servisi · bizde: yok
- Renk paleti tokenlaştırma (obsidian/emerald/champagne-gold) · tahmin: Claude Design (colors_and_type.css) · bizde: yok
### Prompt anatomisi
- E-ticaret sitesi yap, videoyu arka plana full yerleştir · 3:15 · şablon: asset
- Kendi ürettiğim ürün görsellerini ver, bunları kullan de · 3:15 · şablon: asset
- Premium, dark temalı, Shop Now CTA'li site iste · 3:15 · şablon: config
- Ortadaki yazıyı kaldır, butonları köşeye al tek cümle · 5:36 · şablon: hareket
- Bu web siteyi responsive yap tek cümle · 5:36 · şablon: kabul
### Linkler
- https://youtu.be/jGJ09wdTGDI
- https://hostinger.com/YILDIZDIKME10

## brief: 2026-09-28-uygula.md
### Özellik kararları
- claude-usage/terminal-ozet → KUR — gerçek kullanımı gösteriyor, kurulumu geri alınabilir, ek risk yok.
- claude-usage/web-dashboard → DENE — hipotez: URL-durum + localStorage kalıcı panel deseni kendi iç panolarımızda tekrar filtre kurma turunu azaltır · metrik: aynı görünüme dönmek için gereken tıklama/istek sayısı · bütçe: 1 iç araç, ≤2 saat · geri_alma: deseni uygulamazsak mevcut sunucu-taraflı görünüm kalır · eşik: tıklama sayısı %30 düşerse benimse.
- claude-usage/vscode-entegrasyonu → ZATEN VAR — zaten var: terminal-ozet + web-dashboard aynı veriyi IDE bağımlılığı olmadan karşılıyor.
- skills-cli/skill-kurma → KUR — MIT, Snyk audit'li, mevcut katalogda benzer tek-komut skill kurucu yok.
- skills-cli/gecici-kullan → KUR — aynı artefakt, ek risk yok; kurulum öncesi inceleme için doğrudan kullanılabilir.
- nyns-3d-galeri-promptu/3d-dairesel-ring-galeri → ZATEN VAR — zaten var: docs/kurulumlar/bekleyen/teknik-3d-dairesel-ring-galeri-kart-dizilimi-transform-style-preserve-3d.md (aynı video, onaysız bekliyor)
- nyns-3d-galeri-promptu/scroll-mouse-parallax-rotasyon → UYARLA — fikir: scroll/mouse olaylarını tek ortak açı fonksiyonuna (angleOf) bağlamak · hedef: departman-frontend prompt şablonu notu · kod yazılmaz
- jgj0-claude-design-promptu/tek-prompt-e-ticaret-sitesi → UYARLA — kurulacak araç değil; fikir (asset+sıfat kısıtlı tek prompt kalıbı) kendi frontend-craft akışımıza aktarılabilir, kod yazılmaz.
- jgj0-claude-design-promptu/dogal-dille-iteratif-revizyon → ZATEN VAR — zaten var: commit 3321f38 (BIRLESTIR K15 -> omer-kurallar:10 iterasyon cümlesi) bu kalıbı zaten kataloglamış.
- jgj0-claude-design-promptu/ciktiyi-claude-code-a-tasiyip-optimize-etme → DENE — hipotez: tasarım-öncelikli çıktının performans açığı Claude Code'a aktarılıp optimize edilince ölçülebilir kapanır · metrik: Lighthouse performans skoru · bütçe: 1 örnek site, ≤30 dk oturum · geri_alma: iyileşme yoksa bırak · eşik: ≥85 Lighthouse.
### Departman
- claude-usage → verimlilik (0.71)
- skills-cli → surec-ajan-arac (1.00)
- nyns-3d-galeri-promptu → frontend (0.98)
- jgj0-claude-design-promptu → frontend (0.99)
### İddialar
- "logları okuyan bir dashboard/JSON API" → doğru (README (dashboard.py `/api/data`) + cli.py yorumları)
- session.jsonl'den input_tokens/output_tokens/cache_read okunuyor → doğru (scanner.py alan adları (on.md envanteri))
- araç veri göndermiyor / telemetri yok → doğru (ToolHunter incelemesi + pyproject.toml `dependencies = []`)
- npx skills add ile anthropics/skills gibi repolardan tek komutla skill kurulur → doğru (README.md (vercel-labs/skills))
- CLOU 2022'de Awwwards Site of the Day, puan 7,62/10 → doğru (awwwards.com/sites/clou)
- Tam profesyonel site fiyatı 50.000-100.000 dolar → doğrulanamadı (yok)
- Prompt hazırlığı ~2 gün sürüyor, 5-10 kez test ediliyor → doğrulanamadı (yok)
- Tek promptla birkaç dakikada tüm stil/renk paleti/taslak çıkar (3:15-4:18) → doğru (Claude Design ürün sayfası (claude.com/product/design))
- Performans zayıf, sadece optimizasyon eksik, tasarım güçlü (12:00) → doğru (agence-scroll.com 2026 Guide)
- İngilizce prompt yazmak AI'dan daha iyi sonuç verir (1:39) → doğrulanamadı (-)
### Linkler
- yok
## Desktop görüşü (28 Eyl)
- Brief hatası (g): dört video brief'inin Özellik/Departman/İddia bölümleri boş — `video brief` tarama raporlarının bölüm adlarını tanımıyor. Gg35 ve JNM'deki "KUR 4"leri bu yüzden değerlendiremedim.
- skills-cli KUR × 2 → bence ZATEN VAR (işlevsel eşdeğer): envanterde skill keşfet/kur işini yapan skill-ui-cli ve cli-skill-collector var. Ad eşleşmesi işlevsel eşdeğerleri yakalamıyor (h). Rastgele repodan skill kurmak ayrıca izin kapsamı riski taşır; kurulum yok.
- claude-usage/terminal-ozet KUR → katılıyorum (MIT, bağımlılık yok, telemetri yok; proje/oturum bazında geçmiş token dökümü statusline ve headroom perf'in vermediği şey). Ömer ONAY'ıyla 14b yolundan kurulur.
- claude-usage/web-dashboard DENE → ÖĞREN: tıklama sayısı `video dene` ile ölçülemez; URL-durum + localStorage deseni bilgi kartı olarak frontend'e.
- jgj0/ciktiyi-claude-code-a-tasiyip-optimize-etme DENE: katılıyorum; site kalite ölçümü (KURULUM-24) gelince koşulur.
- "İngilizce prompt daha iyi" → dış kaynak yok ama iç ölçümümüz var (İNGİLİZCE-AB, 17 Eyl; global CLAUDE.md bu yüzden İngilizce). Bilgi kartı olmadığı için hat bulamadı; kart açılmalı.
- Araştırıcı: taze adayda gerçek maliyet 35–82k; asıl kayıp tur tavanında raporsuz kalmak (2/4). İlk turda iskelet, en geç 9. turda kapanış + prompt metni on.md'de olmalı.

## Düzeltme (24e-1 K1)
Dosya adları ASCII'ye taşındı (eski → yeni):
- 15-20-mesajda-yeni-sohbete-geç → 15-20-mesajda-yeni-sohbete-gec
- 3d-perspective-detayını-prompt-ta-açıkça → 3d-perspective-detayini-prompt-ta-acikca
- chrome-devtools-cihaz-araç-çubuğu-ile-re → chrome-devtools-cihaz-arac-cubugu-ile-re
- düzeltme-yerine-edit-regenerate → duzeltme-yerine-edit-regenerate
- görselleri-public-klasörüne-koyup-ai-a-a → gorselleri-public-klasorune-koyup-ai-a-a
- paralel-terminal-ile-çoklu-görev-takibi → paralel-terminal-ile-coklu-gorev-takibi
- projeyi-sürekli-github-a-yükleme → projeyi-surekli-github-a-yukleme
- renk-paleti-ve-font-ailesini-prompt-başı → renk-paleti-ve-font-ailesini-prompt-basi
- soruları-tek-mesajda-topla → sorulari-tek-mesajda-topla
