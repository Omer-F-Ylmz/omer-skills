# Claude Sonnet 5.5 vs Opus 5.5: Aynı PRD ile 3D Oyun Yaptırdım
## Künye
Claude Sonnet 5.5 vs Opus 5.5: Aynı PRD ile 3D Oyun Yaptırdım · Emrullah Yaprak | AI & Automation · süre: 32:46 · ? · https://youtu.be/gKRrT6biuag · şema 2
motor: parti 2026-10-09-short-11 · claude-sonnet-5-5 · hafif claude -p
kareler: görsel girdi (60)
altyazı yok: kare-yalnız
claude-sonnet-5-5: claude-sonnet-5-5 · 60707 tk · claude-haiku-5-5: claude-haiku-5-5 · 88095 tk
## Özet
Emrullah Yaprak, Claude Sonnet 5.5 ile Opus 5.5'i aynı PRD (66 kullanıcı hikayesi, 53 kabul kriteri) ve tek bir /goal komutuyla Claude Code'da 'Kargola' adlı 3B depo simülasyonu yaptırarak karşılaştırıyor. Oyunlar yan yana incelenir, 6 alanda 60 puanla değerlendirilir. Opus 5.5 59/60 (yaklaşık 2 sa 40 dk), Sonnet 5.5 55/60 (yaklaşık 3 sa 22 dk) alır. Etikette 2 kat olan fiyat farkı gerçek maliyette yaklaşık 1,1 kat çıkar; cache okuma fiyatı iki modelde aynıdır.
## Bölümler
- 0:00 Giriş: Sonnet 5.5 vs Opus 5.5 ile 3D Oyun Testi
- 0:24 Kargola Oyunu Nasıl Çalışıyor?
- 1:54 Sonnet 5.5 Yenilikleri ve Opus 5.5 ile Fiyat Karşılaştırması
- 3:38 Test Yöntemi: PRD, 53 Kabul Kriteri ve /goal Komutu
- 9:20 Sonnet 5.5'in Yaptığı 3D Oyun İnceleme
- 14:49 Opus 5.5'in Yaptığı 3D Oyun İnceleme
- 19:25 Sonnet 5.5 ve Opus 5.5 Değerlendirme
- 20:35 Opus 5.5 Otomasyon İnceleme
- 22:32 Sonnet 5.5 Otomasyon İnceleme
- 26:00 Puanlama & Değerlendirme
- 30:38 Puanlama, Maliyet ve Sonuç: Hangisi Kazandı?
## Adaylar
| ad | sözlük | tür | link | ne işe yarar | zaman | kanıt |
|---|---|---|---|---|---|---|
| Claude Sonnet 5.5 | yok | teknik | yok | Test edilen ucuz model; Opus 5.5'in yarı fiyatı (2 $/10 $). | 2:00 | Slayt: Sonnet 5.5'te ne yeni? Fiyat 2 $ / 10 $, CursorBench 55,5. (karede: kanıttan) Slayt: Sonnet 5.5'te ne yeni? Fiyat 2 $ / 10 $, CursorBench 55,5. |
| Claude Opus 5.5 | yok | teknik | yok | Karşılaştırılan üst model (4 $/20 $); 59/60 puan aldı. | 2:36 | Kâğıt üstünde tablo: Opus 5.5 fiyat 4 $ / 20 $. (karede: kanıttan) Kâğıt üstünde tablo: Opus 5.5 fiyat 4 $ / 20 $. |
| Claude Code | yok | CLI | yok | Her iki modelin oyunu yazdığı ortam; aynı sürüm, extra efor. | 6:06 | Slayt: Aynı Claude Code sürümü, efor extra, boş klasör. (karede: kanıttan) Slayt: Aynı Claude Code sürümü, efor extra, boş klasör. |
| /goal | yok | ipucu | yok | Hedef sağlanana kadar çalışan Claude Code komutu; hakem her turda kontrol eder. | 6:48 | Slayt: /goal bitene kadar çalış, hedef verilir, hakem bakar. (karede: kanıttan) Slayt: /goal bitene kadar çalış, hedef verilir, hakem bakar. |
| prd-yaz | yok | skill | https://github.com/eyaprak/skills | Kullanıcıyı sorgulayıp PRD yazan skill. | 4:20 | Slayt: prd-yaz skill'i önce beni sorguladı. (karede: kanıttan) Slayt: prd-yaz skill'i önce beni sorguladı. |
| Three.js | yok | teknik | yok | Oyunun 3B grafik kütüphanesi. | 4:20 | Karar tablosunda: Three.js + Vite + TypeScript. (karede: kanıttan) Karar tablosunda: Three.js + Vite + TypeScript. |
| Vite | yok | CLI | yok | Geliştirme sunucusu ve derleme aracı. | 9:12 | Terminalde VITE v8.3.1 ready ve npm run dev çıktısı. (karede: kanıttan) Terminalde VITE v8.3.1 ready ve npm run dev çıktısı. |
| TypeScript | yok | teknik | yok | Oyunun yazıldığı dil. | 4:20 | Karar tablosunda: Three.js + Vite + TypeScript. (karede: kanıttan) Karar tablosunda: Three.js + Vite + TypeScript. |
| npm | yok | CLI | yok | npm run dev ile oyunlar çalıştırıldı. | 9:12 | Terminalde npm run dev komutu ve npm warn çıktısı. (karede: kanıttan) Terminalde npm run dev komutu ve npm warn çıktısı. |
| Kargola | yok | teknik | yok | Test için yaptırılan 3B depo simülasyonu oyunu (üretilen çıktı). | 0:24 | Başlangıç ekranı: Kargola, Devam et / Yeni oyun. (karede: kanıttan) Başlangıç ekranı: Kargola, Devam et / Yeni oyun. |
| VS Code | yok | teknik | yok | PRD'nin önizlemesi ve terminal için kullanılan editör. | 7:24 | Preview prd.md sekmeleri ve alt terminal paneli. · kanıt: kare (karede: Preview prd.md sekmeleri ve alt terminal paneli.) |
| Claude masaüstü uygulaması | yok | teknik | yok | Sonnet/Opus oturumlarının çalıştığı Claude Code arayüzü. | 8:08 | Ekran: What's up next, Emrullah? ve proje listesi; model Opus 5.5 Extra. · kanıt: kare (karede: Ekran: What's up next, Emrullah? ve proje listesi; model Opus 5.5 Extra.) |
| Chrome | yok | teknik | yok | Oyunların localhost'ta açıldığı tarayıcı. | 9:20 | localhost:5173 adres çubuğu, iki Kargola sekmesi. · kanıt: kare (karede: localhost:5173 adres çubuğu, iki Kargola sekmesi.) |
| Artificial Analysis | yok | teknik | yok | Karşılaştırma tablosunda genel puan kaynağı. | 2:36 | Kaynak: ... artificialanalysis.ai; genel puan 56 / 58. (karede: kanıttan) Kaynak: ... artificialanalysis.ai; genel puan 56 / 58. |
| PowerShell | yok | CLI | yok | Komutların çalıştırıldığı Windows kabuğu. | 9:12 | powershell terminal sekmesi (karede: VS Code terminal panelinde 'powershell' sekmesi.) |
| Her iki modele verilen tek /goal hedefi | yok | prompt | yok | prd.md'deki Kargola oyununu bu klasörde sıfırdan geliştir; iş, kabul kriterlerinin tamamı kanıtla sağlanıp teslim raporu yazılınca biter. Görsel kalite en az oyun mantığı kadar önemli. | 6:48 | kaynak: kare |
| Tek prompt ile PRD sözleşmesi karşıtlığı | yok | prompt | yok | Basit tek prompt örneği: bana bir kargo oyunu yap (PRD yaklaşımıyla karşılaştırma). | 3:36 | kaynak: kare |
## Açıklama bağlantıları
- https://youtu.be/pywfao8gZyo — Başka bir YouTube videosu · aday: hayır · İzleyicinin kullanacağı araç değil, video bağlantısı. · sınıf: diğer
- https://youtu.be/EFqVVIDCyMs — Başka bir YouTube videosu · aday: hayır · Araç değil, video bağlantısı. · sınıf: diğer
- https://github.com/eyaprak/skills — Yazarın skill deposu (prd-yaz) · aday: evet (prd-yaz) · İzleyicinin kullanabileceği skill deposu; prd-yaz videoda kullanıldı. · sınıf: diğer
- https://code.claude.com/docs/en/goal — /goal komutu dokümanı · aday: evet (/goal) · Videoda kullanılan /goal komutunun resmi dokümanı. · sınıf: diğer
- https://n8nkursu.com/destek/gKRrT6biuag?utm_source=youtube&utm_medium=description&utm_content=gKRrT6biuag — Kaynak dosyaları için kahve destek sayfası · aday: hayır · Destek/ürün sayfası, araç değil; utm parametresi var ama yönlendirme/indirim kodu yok. · sınıf: diğer · erişilemez: ücretli destek sayfası, içeriğe erişilemedi
## Site/UI teknikleri
| teknik | ne işe yarar | zaman | kaynak |
|---|---|---|---|
| Sol sipariş paneli, durum rozetli kartlar (sidebar order list, status badges) | Siparişlerin durum renkleri ve kalan süre ile listelendiği panel (karede: Sol panel: Siparişler, kartlarda RAMPADA/TOPLANIYOR rozetleri ve saat) | 0:30 | kare |
| Üst durum çubuğu (HUD top bar) | Kasa, memnuniyet yıldızı, gün/saat, hız düğmeleri 1x/2x/4x, açık sipariş sayısı, kargo sayaçları (karede: Üstte KASA, MEMNUNİYET, OYUN SAATİ, hız düğmeleri, AÇIK SİPARİŞ) | 0:30 | kare |
| Açılış menüsü (modal / start screen) | Kargola logolu Devam et / Yeni oyun ekranı, arkada kuş bakışı depo (karede: Kargola logosu, sarı Devam et ve Yeni oyun düğmeleri) | 0:22 | kare |
| Alt işlem paneli (bottom action panel) | Kutu boyu seçimi ve Bantla / Etiket bas / Banda koy adımları (karede: Alt panel: Küçük, Orta, Büyük kutu; 1 Bantla, 2 Etiket bas, 3 Banda koy) | 0:52 | kare |
| Gün sonu rapor penceresi (modal dialog, stat cards) | Gönderilen, geciken, kaçırılan, gelen sipariş ve ciro kartları (karede: Gün 1 sonu raporu: Gönderilen 2, Geciken 5, Günün cirosu 1.020 ₺) | 1:22 | kare |
| Depo yönetimi sekmeli penceresi (tabbed modal) | Otomasyon sekmesinde satın alma kartları (karede: Depo yönetimi: Stok ve tedarik / Otomasyon; Satın al düğmeleri) | 1:24 | kare |
| Bildirim bildirimleri (toast notifications) | Yeni sipariş ve gecikme uyarıları üstte kısa mesaj olarak (karede: Üstte Yeni sipariş K-1-07, K-1-04 siparişi gecikti, Martı Kargo 1 paketi aldı) | 1:08 | kare |
| Dünya içi etiketler ve üzerine gelince ipucu (3D labels, tooltip) | Raflarda ürün adı/adet etiketleri ve hover ipuçları (karede: Raf etiketi Masa lambası ve tooltip Rafta 6/20 - tıkla: çalışan alsın) | 0:50 | kare |
| Kuş bakışı ve serbest kamera (orbit camera) | Sağ tuşla döndürme, WASD kaydırma, tekerlekle yakınlaştırma (karede: Sonnet oyununda alt köşede Sağ tuş / Q E döndür, WASD kaydır yazısı) | 9:20 | kare |
| Gün-gece döngüsü ve gölgeli aydınlatma (lighting, shadows) | Sonnet oyununda gölge ve ışık efektleri (karede: Sonnet 5.5 oyunu: raflara düşen gölgeler, gün göstergesi) | 9:36 | kare |
| Ayarlar penceresi (settings modal, toggle) | Ses efektleri anahtarı, kayıt bilgisi ve oyunu sıfırla (karede: Ayarlar: Ses efektleri anahtarı, Kayıt, Oyunu sıfırla) | 22:28 | kare |
| Sen yokken özeti (offline progress modal) | Oyun kapalıyken geçen süre özeti (karede: Sen yokken...: Gelen sipariş 8, Kazanılan para 1.370 ₺) | 20:34 | kare |
| Puanlama tablosu uygulaması (scoring dashboard) | Geçti/Kısmen/Kaldı seçimli iki sütunlu puan sayfası (karede: Kargola: Opus 5.5 ve Sonnet 5.5, Geçti/Kısmen/Kaldı düğmeleri) | 26:10 | kare |
## Kurulum/komutlar
| komut | ne yapar | zaman | kaynak |
|---|---|---|---|
| /goal prd.md dosyasındaki Kargola oyununu bu klasörde sıfırdan geliştir ... | Claude Code'da hedef sağlanana kadar otonom çalıştırır (karede: (karede OCR) – — · SPACE - F tam ekran - R tekrar 13 / 18 IGOAL /goal: bitene kadar çal Hayır: “devam et" Model çaliır Hakem bakar: “hedef sağlandi mi?" Evet: i biter × Hedef verilir KOMUT /goal prd.md dosyasindak) | 6:48 | kare |
| /prd-yaz | prd-yaz skill'ini çağırır; PRD için sorular sorar (karede: (karede OCR) 6 / 18 — — · SPACE · F tam ekran - R tekrar PRD-YAZ prd-yaz skill'i önce beni sorguladi SORU KARARIM Three.js + Vite + TypeScript Hangi teknoloji? Oyun kapaliyken zaman işlesin mi? Evet, gerçek süre,) | 4:20 | kare |
| npm run dev | Vite geliştirme sunucusunu başlatır (karede: (karede OCR) File Edit Selection File Edit Selection 08 □ kargola-opus □ X kargola-sonnet × × ← * Preview prd.md × Preview prd.md × * PRD: Kargola (tarayicida oynanan 3D sipariş paketleme ve PRD: Kargola (tarayici) | 9:12 | kare |
| npm run dev -- --port 5174 | Sunucuyu 5174 portunda başlatır (ekranda npm uyarısı gösteriyor) (karede: (karede OCR) File Edit Selection File Edit Selection 08 □ kargola-opus □ X kargola-sonnet × × ← * Preview prd.md × Preview prd.md × * PRD: Kargola (tarayicida oynanan 3D sipariş paketleme ve PRD: Kargola (tarayici) | 9:12 | kare |
| vite 5174 | Vite'ı 5174 portunda başlatır; 5173 meşgul olduğu için port değişir. (karede: Terminalde '> vite 5174' ve 'Port 5173 is in use, trying another one...' çıktısı.) | 9:12 | kare |
| npm run dev --port 5174 (tam sözdizimi belirsiz) | Vite'ı belirli bir portta açmayı denemek; npm bu parametreyi 'Unknown cli config' uyarısıyla tanımadı. (karede: Terminalde 'npm warn Unknown cli config "--port"' uyarısı.) | 9:12 | kare |
| /goal prd.md dosyasındaki Kargola oyununu bu klasörde sıfırdan geliştir. İş, PRD'deki kabul kriterlerinin tamamı kanıtıyla sağlandığında ve teslim raporu yazıldığında biter. Görsel kalite standardı en az oyun mantığı kadar önemlidir. | Claude Code'da hedef koşusunu başlatır; hakem 'hedef sağlandı mı?' diye kontrol eder, sağlanmazsa model devam eder. (karede: Slayt: '/goal prd.md dosyasındaki Kargola oyununu...' komut kutusu.) | 6:48 | kare |
## İddialar
| iddia | zaman | tür |
|---|---|---|
| Sonnet 5.5 fiyatı 2 $ / 10 $, Opus 5.5 4 $ / 20 $; cache okuma ikisinde de 0,20 $. | 3:12 | sayısal |
| Sonnet 5.5 CursorBench 55,5, OSWorld 80,1, GDPval 1844; %30'dan fazla hızlı. | 2:02 | sayısal |
| Opus 5.5 60 üzerinden 59, Sonnet 5.5 55 puan aldı. | 30:20 | karşılaştırma |
| Etiket fiyat farkı 2 kat, gerçek maliyet farkı yaklaşık 1,1 kat. | 30:56 | karşılaştırma |
| Sonnet koşusu 3 sa 22 dk, 441 API çağrısı, 217,1 M token; standart API karşılığı yaklaşık 61,2 $. | 8:48 | sayısal |
| Max değil extra efor seçildi; max hem çok uzun sürüyor hem hataya daha açık. | 6:06 | öneri |
| Opus 5.5 yaklaşık 2 sa 40 dk, Sonnet 5.5 yaklaşık 3 sa 22 dk sürdü. | açıklama | sayısal |
## İz
| kaynak | ne | bağlandığı | kanıt |
|---|---|---|---|
| kare 0:04 | Anthropic | aday değil: konu dışı | Rozet: ANTHROPIC, yeni bir model duyurdu. |
| kare 0:04 | Claude Sonnet 5.5 | Claude Sonnet 5.5 | Sonnet 5.5 vs Opus 5.5 başlığı. |
| kare 0:04 | Claude Opus 5.5 | Claude Opus 5.5 | Opus 5.5'in yarı fiyatına. |
| kare 0:24 | Kargola oyunu | Kargola | Başlangıç ekranı Kargola. |
| kare 2:00 | CursorBench 4.0 | aday değil: genel kavram | Benchmark satırı. |
| kare 2:00 | OSWorld 2.1 | aday değil: genel kavram | Benchmark satırı. |
| kare 2:00 | GDPval | aday değil: genel kavram | Benchmark satırı. |
| kare 2:36 | Terminal-Bench 4.0 | aday değil: genel kavram | Benchmark satırı. |
| kare 2:36 | artificialanalysis.ai | Artificial Analysis | Kaynak satırı ve genel puan. |
| kare 3:12 | Cache fiyatı | aday değil: genel kavram | Tekrar okuma (cache) 0,20 $. |
| kare 4:20 | prd-yaz | prd-yaz | prd-yaz skill'i önce beni sorguladı. |
| kare 4:20 | Three.js | Three.js | Karar tablosu. |
| kare 4:20 | Vite | Vite | Karar tablosu. |
| kare 4:20 | TypeScript | TypeScript | Karar tablosu. |
| kare 6:06 | Claude Code | Claude Code | Aynı Claude Code sürümü. |
| kare 6:48 | /goal | /goal | Slayt /goal komutu. |
| kare 7:24 | VS Code | VS Code | Preview prd.md, File Edit Selection. |
| kare 8:08 | Claude masaüstü uygulaması | Claude masaüstü uygulaması | What's up next, Emrullah? |
| kare 8:12 | Skill menüsü (code-review, context-mode, claude-api, excalidraw vb.) | aday değil: konu dışı | Yalnız menüde listeleniyor, kullanılmadı. |
| kare 9:12 | npm | npm | npm run dev. |
| kare 9:12 | PowerShell | aday değil: başka adayın parçası (npm) | Terminal sekmesi. |
| kare 9:20 | Chrome tarayıcı | Chrome | localhost:5173 sekmeleri. |
| kare 9:20 | browser-use yer imi | aday değil: konu dışı | Yalnız yer imi çubuğunda. |
| açıklama | github.com/eyaprak/skills | prd-yaz | Faydalı linkler. |
| açıklama | code.claude.com/docs/en/goal | /goal | Faydalı linkler. |
| açıklama | youtu.be/pywfao8gZyo ve EFqVVIDCyMs | aday değil: konu dışı | Başka video bağlantıları. |
| açıklama | n8nkursu.com destek bağlantısı | aday değil: sponsor/reklam | Kahve destek sayfası, utm parametreli. |
| yorum | Descript | aday değil: konu dışı | Sözlük eşleşmesi, videoda kullanılmadı. |
| yorum | Yazarın sonnet worker + opus planlama önerisi | aday değil: genel kavram | Sahip yorumu. |
| linkli sayfa | code.claude.com dokümanları (hooks, permission modes vb.) | aday değil: konu dışı | /goal sayfasından çıkan bağlantılar. |
| linkli sayfa | metr.org, imaginefrontier.com | aday değil: konu dışı | Opus 5.5 sayfasındaki bağlantılar. |
## Kareden okunanlar
- 0:04: Anthropic yeni bir model duyurdu: Sonnet 5.5 vs Opus 5.5, Opus 5.5'in yarı fiyatına.
- 2:36: Tablo: Sonnet 5.5 Terminal-Bench 70,6; Opus 66,4; Artificial Analysis 56 / 58.
- 8:48: Sonnet raporu: 3 sa 22 dk, 441 API çağrısı, 217,1 M token, çıktı 905.628.
- 30:56: Opus 59/60, Sonnet 55/60; etiket 2 kat, gerçek 1,1 kat; dolar başına puan 0,9.
## Belirsizlikler
- Altyazı yok; konuşma içeriği yalnız kare, OCR ve açıklamadan çıkarıldı.
- Opus'un tam maliyet rakamı kısmen okunabildi (TL karşılığı 3.262,91 / 2.999,29 ₺ görünüyor).
- OCR'da geçen Ollama, Llama, Next.js, Cursor, iTerm, Go yalnız gürültü/menü olabilir; videoda kullanıldığı doğrulanamadı.
- Ekran listesinde görünen code-review, context-mode, claude-api, excalidraw-diagram-generator, typesafe skill'leri yalnız menüde; kullanılmadı.
- Tarayıcı yer imlerindeki browser-use yalnız yer imi; kullanıldığı görülmedi.
- Yorumda geçen Descript videoda kullanılmış görünmüyor.
- Sonnet 5.5'in Opus 5.5 olarak adlandırılan çıkış tarihleri slaytta var; doğrulanmadı.
## Atlanan segment oranı
0/0 (paket tam okuma, motor)
## URL'ler
| url | zaman | kaynak | aday |
|---|---|---|---|
| anthropic.com/claude-sonnet-5-5 | 2:02 | ekran | hayır |
| anthropic.com/claude-opus-5-5 | 2:36 | ekran | hayır |
| artificialanalysis.ai | 2:36 | ekran | evet |
| http://localhost:5175/ | 9:12 | ekran | hayır |
| http://localhost:5174/ | 9:12 | ekran | hayır |
| https://youtu.be/pywfao8gZyo | açıklama | açıklama | hayır |
| https://youtu.be/EFqVVIDCyMs | açıklama | açıklama | hayır |
| https://github.com/eyaprak/skills | açıklama | açıklama | evet |
| https://code.claude.com/docs/en/goal | açıklama | açıklama | evet |
| https://n8nkursu.com/destek/gKRrT6biuag?utm_source=youtube&utm_medium=description&utm_content=gKRrT6biuag | açıklama | yorum | hayır |
| platform.claude.com | 9:06 | ekran | hayır |
## İş akışı
- 1. adım — Sonnet 5.5 ve Opus 5.5'in yeniliklerini, fiyat ve cache farkını slaytlarla karşılaştırma — araçlar: Claude Sonnet 5.5, Claude Opus 5.5, Artificial Analysis
- 2. adım — PRD'yi prd-yaz skill'iyle, sorulara verilen kararlarla yazdırma — araçlar: prd-yaz, Claude Code
- 3. adım — PRD'yi (66 hikaye, 53 kabul kriteri) editörde inceleme — araçlar: VS Code
- 4. adım — Aynı koşulları ayarlama: aynı sürüm, extra efor, boş klasör — araçlar: Claude Code
- 5. adım — Her iki modelde aynı /goal komutunu verip müdahalesiz çalıştırma — araçlar: /goal, Claude Sonnet 5.5, Claude Opus 5.5
- 6. adım — Sonnet koşusunun maliyet raporunu okuma — araçlar: Claude Code
- 7. adım — İki projeyi npm run dev ile başlatma — araçlar: npm, Vite
- 8. adım — Sonnet'in oyununu tarayıcıda inceleme (sipariş, paketleme, kamyon) — araçlar: Chrome, Three.js
- 9. adım — Opus'un oyununu tarayıcıda inceleme — araçlar: Chrome, Three.js
- 10. adım — Sen yokken, F5 sonrası kayıt ve hız testi — araçlar: Chrome
- 11. adım — Robot ve otomasyon sistemlerini iki oyunda test etme — araçlar: Chrome
- 12. adım — 6 alan, 60 puanlık tabloyla puanlama — araçlar: Puanlama uygulaması
- 13. adım — Gerçek API maliyetini hesaplayıp sonucu açıklama — araçlar: Claude Code
## Promptlar
- Her iki modele verilen tek /goal hedefi — prd.md'deki Kargola oyununu bu klasörde sıfırdan geliştir; iş, kabul kriterlerinin tamamı kanıtla sağlanıp teslim raporu yazılınca biter. Görsel kalite en az oyun mantığı kadar önemli.
- Tek prompt ile PRD sözleşmesi karşıtlığı — Basit tek prompt örneği: bana bir kargo oyunu yap (PRD yaklaşımıyla karşılaştırma).
