# Anlamsal puan doğrulaması (VİDEO-AKIL-1b-2a DEVAM-1)

Model: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (~0,22 GB, fastembed). Eşikler (çapraz-video çiftlerinin %99'u): is_akisi 0.55, promptlar 0.527, site_ui 0.715, ogrenimler 0.514
Çiftler tur-1 yalın raporlarından; 'eşleşen' = eşiği geçip bire-bir atanan (kosinüse göre eşit aralıklı 8), 'eşik altı' = eşleşmeyen altın maddenin en yakın satırı, eşiğin hemen altındaki en yüksek 8.

## is_akisi (eşik 0.55)

### Eşleşen

- 0.558 · altın: ~20. dakikada token/süre kontrolü (Opus 19.4k, Sonnet 27.1k): Opus önce inceleyip test ediyor, Sonnet doğrudan kuruyor; iskelet Vite + TypeScript + Three.js + GSAP + Lenis, font Inter Tight (Neue Montreal ticari), port 5173 dolu → 5174 · rapor: 5. adım — Sonnet 5.5 ve Opus 5.5 ile 3D web sitesi oluşturma ve performans karşılaştırması yapma — araçlar: Sonnet 5.5, Opus 5.5, Cursor
- 0.570 · altın: Referans görsel yapıştırılır ve başka bilgi vermeden 'Design this website' yazılır · rapor: 3. adım — Yapay zekaya temel web sitesi tasarımı ürettirilir — araçlar: Claude Opus 5.5
- 0.592 · altın: Pinterest'te yalnız üç bölümü görünen bir ajans sitesi referansı seçilip görsel kopyalanır · rapor: 1. adım — Pinterest'ten referans tasarım görseli seçilir — araçlar: Pinterest
- 0.647 · altın: Tasarım düz HTML/CSS/JS'e kodlatılır: index.html, css/styles.css, js/main.js, assets/images, README.md; ZIP indirme sunulur · rapor: 6. adım — Kodlar HTML, CSS ve JavaScript formatında dışarı aktarılır — araçlar: JavaScript, CSS, HTML
- 0.683 · altın: Effort'u High seç, adil karşılaştırma için ajan çalıştırma; Opus 5.5 ve Sonnet 5.5 oturumlarını gönder · rapor: 2. adım — Opus 5.5 ve Sonnet 5.5 ile projeyi sıfırdan kodlamak — araçlar: Claude Opus 5.5, Claude Sonnet 5.5
- 0.711 · altın: bezier curve oluştur, arabayı eğriyi takip edecek şekilde bağla · rapor: 4. adım — Bezier eğrisi kullanarak arabanın rotasını belirlemek ve sahneyi render almak — araçlar: Blender
- 0.785 · altın: Topview'da MCP & Skill sayfasından Claude için MCP URL'sini kopyala; Claude'da Add custom connector → ad 'Topview' + MCP server URL → Connect · rapor: 2. adım — Topview MCP bağlayıcısını Claude'a entegre et — araçlar: Topview, Claude, MCP
- 0.879 · altın: Videoyu GPT Astra'ya ver; önceki videodaki site promptunu emlak sitesine uyarlayıp 4 skill ile sahne sahne site yaptır · rapor: 4. adım — Üretilen videoyu GPT Astra'ya aktararak web sitesini oluştur — araçlar: GPT Astra

### Eşik altı

- 0.673 · altın: Claude istemi Design paneline taşır; artboard ekler, referanstan fotoğraf kırpar, Archivo/Instrument Sans seçer, Artifact olarak kurar · rapor: 2. adım — Claude Opus 5.5 tasarım moduna geçilerek referans görsel yapay zekaya aktarılır — araçlar: Claude Opus 5.5, Claude Design
- 0.659 · altın: Generate Model bölümüne geç, araba görselini yükle (AI Model v3.1) · rapor: 2. adım — Tripo AI kullanarak araba görselinden veya metinden 3D model üretmek ve düzenlemek — araçlar: Tripo AI, Nano Banana
- 0.628 · altın: Karar: tokenlar neredeyse eşit; zor yazılım işinde Opus, gündelik işte (PDF, sunum) Sonnet · rapor: 2. adım — Opus 5.5 ve Sonnet 5.5 ile projeyi sıfırdan kodlamak — araçlar: Claude Opus 5.5, Claude Sonnet 5.5
- 0.620 · altın: Hero için önceden ChatGPT'de üretilmiş yılan portresi görseli girişte gösterilir · rapor: 5. adım — Gemini veya ChatGPT ile alternatif hero görseli üretilip tasarıma entegre edilir — araçlar: Gemini, ChatGPT, Claude Opus 5.5
- 0.609 · altın: ~10-15 dk sonra bitiş: Opus 'Tessel'i localhost:5174'te, Sonnet 'Murmur'u localhost:5391'de (socket probe) çalıştırıyor; npm run build geçiyor; Opus proje notlarını hafızaya kaydediyor, Sonnet Dala ile yan yana karşılaştırıyor · rapor: 2. adım — Opus 5.5 ve Sonnet 5.5 ile projeyi sıfırdan kodlamak — araçlar: Claude Opus 5.5, Claude Sonnet 5.5
- 0.595 · altın: multi-view görseller üret, bunlardan 3D modeli oluştur · rapor: 2. adım — Tripo AI kullanarak araba görselinden veya metinden 3D model üretmek ve düzenlemek — araçlar: Tripo AI, Nano Banana
- 0.583 · altın: Dosyalar çalıştırılmadan önce parallax, appear ve etkileşim animasyonları ekletilir · rapor: 7. adım — Paralaks ve etkileşim animasyonları eklenerek site canlıya alınır — araçlar: Paralaks efekti, JavaScript
- 0.583 · altın: Beğenilmeyen son bölüm için aynı stilde testimonial + yeni footer istenir · rapor: 4. adım — Testimonial ve footer gibi eksik bölümler eklettirilir — araçlar: Claude Opus 5.5

## promptlar (eşik 0.527)

### Eşleşen

- 0.592 · altın: Boş projede sıfırdan Awwwards seviyesi site kur; Dala'yı canlı tarayıcıda baştan sona incele, renk/akış/geçiş dilini koru, test et, boş portta çalıştır. · rapor: Boş bir projeden sıfırlayarak Awwwards seviyesinde interaktif bir web sitesi inşa etmek. — Build a complete Awwwards-level interactive website from scratch inside this empty project.
- 0.664 · altın: Yüklediği yılan portresi görselini hero görselinin yerine koymasını istiyor. · rapor: Hero alanındaki görseli yeni üretilen alternatif görselle değiştirmek. — replace the hero image with the image that I provided over here
- 0.667 · altın: Girişi 3-4 sn'ye indir, camdan geçince aynı oturma odası kalsın, yeni merdiven icat etme, oda temposu yavaş, tek kesintisiz çekim; revize edip üret. · rapor: ChatGPT yardımıyla video girişini kısaltmak ve iç mekan tutarlılığını korumak. — Make the entrance faster. Do not spend 5 seconds outside. Enter the house in about 3-4 seconds. The most important rule: when crossing the glass/opening, the interior must remain the same living room.
- 0.674 · altın: Göz videosu, 3D gözlük modelleri ve 10 görselle scroll anlatımlı lüks site; yaratıcı yön modelde, skill'leri uygula, siyah boşluksuz geçiş, tarayıcıda doğrula. · rapor: VEIL markası için lüks, eksiksiz ve görsel açıdan olağanüstü bir web sitesi tasarlamak ve inşa etmek. — Design and build a complete, visually exceptional website for VEIL, a global, ultra-premium eyewear brand, using the supplied eye video, actual 3D eyewear models, and all 10 product images already included in this project.
- 0.682 · altın: Promptu onaylayıp home-project.png görseliyle üretimi başlatma mesajı. · rapor: Topview MCP ve Seedance 2.5 kullanarak kesintisiz lüks villa uçuş videosu üretmek. — Use the Topview connector. Reference image: home-project.png in the project folder. Do not ask me anything. Write the prompt yourself, then generate immediately. MODEL SETTINGS - Seedance 2.5, image_to_video, first frame = home-project.png - 25 seconds, 720p (Seedance 2.5 does not accept 1080 on Topview), 1 output - Default board GOAL A 25-second, 16:9, seamless cinematic villa fly-through for a luxury real estate website. One continuous smooth shot. No cuts, no scene changes, no dissolve, no crossfade, no jump, no reset, no teleport. The camera moves as one uninterrupted path.
- 0.780 · altın: Pinterest ekran görüntüsünü Design moduna yapıştırıp başka bilgi vermeden yalnızca bu siteyi tasarlamasını istiyor. · rapor: Pinterest'ten alınan referans görselin stilini kopyalayarak temel web sitesi tasarımı oluşturmak. — design this website

### Eşik altı

- 0.544 · altın: Claude'a Topview connector'ı kullan, görseli analiz et, Seedance 2.5 için 25 sn kesintisiz villa fly-through promptu yaz; oda sırası, negatifler, üretmeden onaya göster. · rapor: Topview MCP ve Seedance 2.5 kullanarak kesintisiz lüks villa uçuş videosu üretmek. — Use the Topview connector. Reference image: home-project.png in the project folder. Do not ask me anything. Write the prompt yourself, then generate immediately. MODEL SETTINGS - Seedance 2.5, image_to_video, first frame = home-project.png - 25 seconds, 720p (Seedance 2.5 does not accept 1080 on Topview), 1 output - Default board GOAL A 25-second, 16:9, seamless cinematic villa fly-through for a luxury real estate website. One continuous smooth shot. No cuts, no scene changes, no dissolve, no crossfade, no jump, no reset, no teleport. The camera moves as one uninterrupted path.
- 0.459 · altın: Villa kimliği, saniye saniye kamera yolu, hareket stili, görsel kalite ve uzun HARD NEGATIVES listesi içeren 25 sn image-to-video promptu. · rapor: Topview MCP ve Seedance 2.5 kullanarak kesintisiz lüks villa uçuş videosu üretmek. — Use the Topview connector. Reference image: home-project.png in the project folder. Do not ask me anything. Write the prompt yourself, then generate immediately. MODEL SETTINGS - Seedance 2.5, image_to_video, first frame = home-project.png - 25 seconds, 720p (Seedance 2.5 does not accept 1080 on Topview), 1 output - Default board GOAL A 25-second, 16:9, seamless cinematic villa fly-through for a luxury real estate website. One continuous smooth shot. No cuts, no scene changes, no dissolve, no crossfade, no jump, no reset, no teleport. The camera moves as one uninterrupted path.
- 0.453 · altın: Aynı stilde, sitenin parçası gibi duran iki bölüm istiyor: testimonial ve mevcut footer'ın yerine yenisi. · rapor: Pinterest'ten alınan referans görselin stilini kopyalayarak temel web sitesi tasarımı oluşturmak. — design this website
- 0.451 · altın: Gözlüğü daha büyük göstermesini isteyen revizyon; ölçekle birlikte kamera açısı, yazı yerleşimi ve sahne geçişleri de uyarlanmalı. · rapor: Yapay zekanın görsel yön konusunda kullanıcıya sormadan kendi yaratıcı kararlarını alıp uygulaması. — Make confident creative decisions and implement them without asking me to choose a visual direction.
- 0.442 · altın: Tasarımın en basit diller olan JavaScript, CSS ve HTML ile kodlanmasını istiyor. · rapor: Pinterest'ten alınan referans görselin stilini kopyalayarak temel web sitesi tasarımı oluşturmak. — design this website
- 0.439 · altın: Siteye parallax, beliren (appear) efekt ve bazı etkileşimler eklenmesini istiyor. · rapor: Pinterest'ten alınan referans görselin stilini kopyalayarak temel web sitesi tasarımı oluşturmak. — design this website
- 0.430 · altın: ChatGPT'den Pinterest görselindeki arka plandaki yazıları silip görseli tamamen boş, video üretimine hazır hale getirmesini istiyor. · rapor: Topview MCP ve Seedance 2.5 kullanarak kesintisiz lüks villa uçuş videosu üretmek. — Use the Topview connector. Reference image: home-project.png in the project folder. Do not ask me anything. Write the prompt yourself, then generate immediately. MODEL SETTINGS - Seedance 2.5, image_to_video, first frame = home-project.png - 25 seconds, 720p (Seedance 2.5 does not accept 1080 on Topview), 1 output - Default board GOAL A 25-second, 16:9, seamless cinematic villa fly-through for a luxury real estate website. One continuous smooth shot. No cuts, no scene changes, no dissolve, no crossfade, no jump, no reset, no teleport. The camera moves as one uninterrupted path.
- 0.401 · altın: Dört kurulu skill ile pear.no'nun scroll hissinden esinlenen ama kopyalamayan Awwwards seviyesi lüks villa sitesi; scrollcraft ile pinned sekans, scroll'a bağlı video. · rapor: GPT Astra'ya lüks emlak sitesi ve Awwwards kalitesinde arayüz üretmesini söylemek. — This is not a generic landing page. The result must feel like a high-end, Awwwards-level digital experience for a company selling ultra-premium. Use these 4 installed skills in this project...

## site_ui (eşik 0.715)

### Eşleşen

- 0.784 · altın: Scroll'a bağlı video ilerletme (oda oda kesintisiz gezinti) · rapor: Kesintisiz scroll animasyonlu oda geçişleri
- 0.878 · altın: Scroll'a bağlı parçacıkların farklı 3D modellere dönüşmesi (Engram) · rapor: Scroll ile tetiklenen 3D parçacık animasyonu

### Eşik altı

- 0.714 · altın: Mobil uyarlama ve hafif 3D model · rapor: Parçalanan 3D model animasyonu
- 0.707 · altın: 3D model materyallerinin yeniden kurulumu · rapor: Parçalanan 3D model animasyonu
- 0.696 · altın: İtalik editoryal tipografi karışımı · rapor: Italic editorial typography
- 0.683 · altın: Editoryal kompozisyon: farklı boyutta görseller ve font karşıtlığı · rapor: Anıtsal editoryal tipografi ve lüks marka kompozisyonu
- 0.676 · altın: Scroll ile tünelin içinden geçiş · rapor: Scroll ile tetiklenen 3D parçacık animasyonu
- 0.668 · altın: Scroll-scrubbed karakter bazlı metin açılışı + loader/boot orkestrasyonu · rapor: Scroll-scrubbed per-character text-reveal
- 0.656 · altın: Parçacıkların içine giriş + fiziksel geçiş animasyonu (Opus) · rapor: 3D Tünel geçiş efekti
- 0.640 · altın: Tam genişlik hero görseli ve kenar karartma · rapor: Paralaks görseller ve fare imleç etkileşimi

## ogrenimler (eşik 0.514)

### Eşleşen

- 0.525 · altın: Kamera hareketini drone/gimbal gibi fiziksel tarif et · rapor: 5. adım — Referans mimari görseli analizi ve Seedance 2.5 için kesintisiz kamera hareketi içeren detaylı prompt oluşturma — araçlar: Seedance 2.5
- 0.535 · altın: Başlangıç karesine dönüş (return shot) · rapor: kareler: görsel girdi (6)
- 0.564 · altın: 3D modeli ~5 MB'a optimize et · rapor: 8:48: glasses-website-project, All 10 images are integrated, The 3D models load
- 0.596 · altın: Dala referanslı Awwwards site promptu · rapor: Boş bir projeden sıfırlayarak Awwwards seviyesinde interaktif bir web sitesi inşa etmek. — Build a complete Awwwards-level interactive website from scratch inside this empty project.
- 0.612 · altın: Fiziksel geçiş animasyonu · rapor: | 3D Tünel geçiş efekti | Kullanıcı aşağı kaydırdıkça tünel içerisinden geçiş hissi veren WebGL animasyonu. (karede: Web sitesinde tünel benzeri derinlikli 3D geçiş ekranı yer alıyor.) | 7:10 | altyazı |
- 0.660 · altın: Scroll ile tetiklenen parçacık morph'u · rapor: | Scroll ile tetiklenen 3D parçacık animasyonu | Sayfa kaydırıldıkça hareket eden ve farklı modeller oluşturan parçacık sistemi. | 0:00 | altyazı |
- 0.715 · altın: Scroll'a bağlı video (scrub) · rapor: | Scroll-driven video scrubbing | Kullanıcı sayfayı aşağı kaydırdıkça göz videosunun ilerlemesi veya geri sarılması. (karede: Sayfayı kaydırdıkça gözün içine girilmesi ve 3D gözlüğün ortaya çıkması.) | 0:00 | altyazı |
- 0.824 · altın: Scroll-scrubbed karakter bazlı metin açılışı · rapor: | Scroll-scrubbed per-character text-reveal | Sayfa kaydırıldıkça karakter bazlı metin belirme animasyonu. (karede: Ekran metninde 'text-reveal system (scroll-scrubbed per-character)' ifadesi geçiyor.) | 3:31 | kare |

### Eşik altı

- 0.641 · altın: DOM bölümlerine bağlı keyframe scroll koreografisi · rapor: | Scroll-scrubbed per-character text-reveal | Sayfa kaydırıldıkça karakter bazlı metin belirme animasyonu. (karede: Ekran metninde 'text-reveal system (scroll-scrubbed per-character)' ifadesi geçiyor.) | 3:31 | kare |
- 0.609 · altın: Scroll ile slider · rapor: | Scroll-scrubbed per-character text-reveal | Sayfa kaydırıldıkça karakter bazlı metin belirme animasyonu. (karede: Ekran metninde 'text-reveal system (scroll-scrubbed per-character)' ifadesi geçiyor.) | 3:31 | kare |
- 0.536 · altın: Scroll ile tünel geçişi · rapor: | 3D Tünel geçiş efekti | Kullanıcı aşağı kaydırdıkça tünel içerisinden geçiş hissi veren WebGL animasyonu. (karede: Web sitesinde tünel benzeri derinlikli 3D geçiş ekranı yer alıyor.) | 7:10 | altyazı |
- 0.516 · altın: Scroll hızına tepki · rapor: | Scroll ile tetiklenen 3D parçacık animasyonu | Sayfa kaydırıldıkça hareket eden ve farklı modeller oluşturan parçacık sistemi. | 0:00 | altyazı |
- 0.499 · altın: Parçacık hover efekti · rapor: | Scroll ile tetiklenen 3D parçacık animasyonu | Sayfa kaydırıldıkça hareket eden ve farklı modeller oluşturan parçacık sistemi. | 0:00 | altyazı |
- 0.487 · altın: Prosedürel şekil/nokta üreteçleri · rapor: kareler: görsel girdi (6)
- 0.461 · altın: Kare başına CPU + draw-call ölçümü · rapor: | kare | Cursor editörü | Cursor | Kodlama işlemleri Cursor üzerinden yürütülüyor. |
- 0.456 · altın: Semi-implicit entegrasyon + substepping · rapor: |---|---|---|
