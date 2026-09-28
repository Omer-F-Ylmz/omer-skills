# Parti B brief — 2026-09-28 (Desktop ikinci görüş girdisi)

Kaynak: `video brief` × 3 tarama raporu + katman raporu (docs/kurulumlar/2026-09-28-uygula.md, son koşu = Koşu 5: araştırılan 3 aday). T0 adayların kararları tarama brief'lerinin Departman bölümünde.

## brief: 2026-09-28-2n84xa99FRY.md
### Adaylar
- Codex skill paylaşımı (codex.md) · skill · Codex fleet + imagegen skill'lerini tek dosyada birleştirip herkese açık yayınlamak (0:51)
- Serai (hub) · plugin · Farklı AI modellerini tek panelde birleştirip ortak hafıza/skill/onay katmanı sağlayan özel altyapı (1:57)
- caffeinate · CLI · macOS'ta bilgisayarın 12+ saat uyumasını/kapanmasını engelleyip agent'ların gece boyu çalışmasını sağlar (7:03)
- Çoklu-ajan commit review pipeline · iş akışı · 100+ commit'i 10 paralel agent'a böldürüp raporlarını 3. bir agent'a konsolide ettirerek haftalık review'ı bir günde bitirme (12:07)
- Sub-agent ile token tasarrufu · teknik · Alt agent büyük context'i (132bin token) okuyup ana modele sadece özet (~1,5bin token) döndürerek ana context'i büyütmeden bilgi taşıma (14:33)
- GitHub kullanımı (repo/commit takibi) · ipucu · Agent'ların 400bin+ satırlık codebase'i baştan okumak yerine son commit'lerden değişikliği takip edebilmesi için repo şart; private tutulabilir (21:46)
- Gemini multimodal embedding · teknik · Metin/ses/video/görseli aynı vektör uzayında (tek "dil" gibi) embed ederek RAG kalitesini artırma (11:04)
- Context7 (MCP) · MCP · Kullanılan SDK/API/kütüphane hakkında güncel dokümantasyon çekme; bu görevde gerekmediği için kapatılmış (5:00)
- /model, /effort (Claude Code) · CLI · Oturumda kullanılacak modeli (Fable 5/Opus 4.8) ve düşünme seviyesini (low/medium/high) ayarlama (4:29)
- WebFetch ile skill entegrasyonu · iş akışı · İzleyicinin kendi agent'ına "şu URL'yi aç, skili oku, kendi sistemine entegre et" dedirterek kurulum yaptırması (2:58)
- curl ile herkese açık skill dosyası servis etme · ipucu · `curl -s https://avenox.lol/codex.md` ile agent'ların/CLI araçlarının auth gerektirmeden ham markdown skill dosyasını çekmesi (13:39)
- Backlog sistemi · iş akışı · %80-90 tamamlanan ama bitirilmemiş işleri not alıp sonra dönmek için ayrı bir liste tutma (55:23)
- Skor/iskelet tabanlı ilerleme ölçümü ("scaler" test) · teknik · Klasik pass/fail test yerine her commit'i bir sayısal skora (yön gösteren) bağlayıp sistemin gerçekten iyileşip iyileşmediğini ölçme (41:58)
- Dürüstlük mühendisliği (drift/not-implemented deklarasyonu) · teknik · Agent'ın eksik/yapılmamış kısımları gizlemek yerine açıkça "not implemented" olarak işaretlemesini zorlayan custom guard (28:43)
- /go (Codex) · CLI · Verilen görev tamamen bitene kadar agent'ın durmasını engelleyen komut (34:52)
### Departman
- kural-iş-takibi-alan-bazlı-commit-gerekçe-notu → surec-git-yayin · KUR
- codex-skill/codex-exec-genel → surec-ajan-arac · ÖĞREN
- codex-skill/imagegen → surec-ajan-arac · RED
- codex-skill/fleet-parallel → surec-ajan-arac · ZATEN VAR
- codex-skill/multi-image-referans-zinciri → surec-ajan-arac · ÖĞREN
- serai-hub → surec-ajan-arac · ÖĞREN
- caffeinate → surec-ajan-arac · ÖĞREN
- sub-agent-ile-token-tasarrufu → verimlilik · ÖĞREN
### İddialar
- Codebase ~400-450 bin satır (20:45 · sayısal)
- Sub-agent kullanımı bir araştırmayı 132.000 token'dan ~1.500 token'a düşürüyor (14:33 · sayısal)
- Fable haftalık kullanım limiti, toplam haftalık limitin yarısı kadar ayrı bir kota (14:10 · özellik)
- Codebase'te 457 (sonra 450 olarak da anılan) test dosyası var, davranış assert eden testler (pass/fail değil) (29:43 · özellik)
- Fable'ın codebase review verdisi 10 üzerinden 8.5-9 (A eksi) (32:50 · sayısal)
- 6,5 haftada 1856 commit atıldığı belirtiliyor (46:34 · sayısal)
- Vibe-coding ile yapılan kodda "teknik borç olmama ihtimali sıfır" (44:31 · öneri)
- Kurs satan içerik üreticilerinin çoğu içeriği "damıtarak" satıyor, kalitesi düşük (49:10 · özellik)
- Bir işlem/analiz için normalde saatler sürecek review süreci çoklu-agent pipeline ile bir günde bitiyor (12:07 · karşılaştırma)
- Kendi "LQ" skorunu negatiften pozitife çevirmenin marketing materyali olacağı öneriliyor (51:10 · öneri)
### Site/UI
- yok (raporda site/UI tekniği yok)
### Prompt anatomisi
- yok (bu videonun prompt adayı yok)
### Linkler
- https://youtu.be/2n84xa99FRY
- https://avenox.lol/codex.md
- https://github.com/avenoxai/serai
- https://avenox.lol/codex.md`

## brief: 2026-09-28-XemheY_aM1g.md
### Adaylar
- MiniMax M3 modeli · teknik · Opus yerine kullanılan ucuz, 1M context, görsel+kod destekli model (1:58)
- MiniMax API anahtarı oluşturma + bakiye yükleme · iş akışı · Console > Access'ten anahtar üretme, kullanmadan önce bakiyeye ödeme koyma (3:05)
- `claude /mm` komutu (claude-mm kurulumu) · CLI · Claude Code terminalinde MiniMax modelini başlatan alias (4:13)
- Aynı anda iki terminalde iki model (Opus + MiniMax) · iş akışı · Ayrı terminal pencerelerinde `claude` (Opus) ve `claude /mm` (MiniMax) paralel çalıştırılır (4:47)
- Ekran görüntüsünden şablon/e-posta üretme testi · iş akışı · Ekran görüntüleri modele yapıştırılıp "100 email şablonu oluştur" gibi görev verilir (6:12)
- Görselden arayüz/kod üretme testi · iş akışı · Bir UI görseli verilip benzer arayüz + backend + test kodu üretimi istenir (10:47)
- Token/kullanım takibi (Balance/API Usage paneli) · ipucu · Harcanan token ve maliyeti panelden izleyip modelin fiilen çalıştığını doğrulama (5:48)
- Ajan sistemlerinde ucuz/tekrarlayan-iş modeli seçme (Open Router, Hermes örneği) · ipucu · Sürekli tekrar eden agent görevlerinde pahalı flagship yerine ucuz modelle token maliyeti düşürülür (8:07)
- Yüksek context limitli model seçme · ipucu · Büyük kod tabanı/veri okutulacaksa yüksek context'li model tercih edilmeli, düşük context'te eksik analiz riski var (7:14)
- MiniMax indirim kodu (%12 ek indirim) · ipucu · Mevcut %50 indirime ek %12 indirim alınabiliyor (11:34)
- GOAT oto-mod görev listesiyle ajan çalıştırma · iş akışı · Otomatik modda sırayla görev (sosyal medya stratejisi, carousel, müşteri bul, outreach) çalıştıran ajan yapısı (0:00)
### Departman
- claude-mm/minimax-m3-backend-degisimi → surec-ajan-arac · RED
- minimax-api-anahtarı-oluşturma-bakiye-yü → diger · KUR
- aynı-anda-iki-terminalde-iki-model-opus- → surec-ajan-arac · ÖĞREN
- ekran-görüntüsünden-şablon-e-posta-üretm → belge · ÖĞREN
- görselden-arayüz-kod-üretme-testi → frontend · KUR
- token-kullanım-takibi-balance-api-usage- → verimlilik · KUR
- yüksek-context-limitli-model-seçme → verimlilik · KUR
- minimax-indirim-kodu-12-ek-indirim → diger · ÖĞREN
### İddialar
- MiniMax 1M token ~30 cent (%50 indirimli) (1:58 · sayısal)
- MiniMax token maliyeti Opus'a göre 5-6x düşük (8:07 · karşılaştırma)
- Bu testte gerçek harcama ~5 cent, Opus'ta tahminen ~200 cent olurdu (9:08 · sayısal)
- MiniMax context limiti 1 milyon token, Opus'a benzer (5:48 · özellik)
- MiniMax hem görsel hem kod okuyup üretebiliyor, çoğu ucuz model bunu yapamıyor (8:07 · özellik)
- Mevcut %50 indirime ek %12 indirim kodu önerisi (11:34 · öneri)
### Site/UI
- sohbet + görev paneli iki sütun yerleşimi (GOAT arayüzü, sol chat/sağ gelen kutusu-görevler) · tahmin: özel React uygulaması (GOAT), ekranda ad görünmüyor · bizde: yok
- liste + detay iki panelli grid (MiniMax'ten üretilen örnek arayüz önizlemesi) · tahmin: MiniMax'in ürettiği HTML/CSS, araç adı ekranda/açıklamada geçmiyor · bizde: yok
- tek CTA'lı kısa e-posta şablon düzeni (komut satırı ≤7 kelime, gövde 3-7 cümle) · tahmin: düz markdown şablon, framework yok · bizde: yok
### Prompt anatomisi
- yok (bu videonun prompt adayı yok)
### Linkler
- https://youtu.be/XemheY_aM1g
- https://platform.minimax.io
- https://platform.minimax.io/subscribe/coding-plan?code=H4FJUSY607&source=link

## brief: 2026-09-28-4cE9t4rE0-0.md
### Adaylar
- ChatLLM (Abacus AI) · iş akışı · Görsel, video ve kod üretimini tek platformda birleştiren AI ajan aracı (1:14)
- Çoklu-model erişimi (100+ model) · teknik · Tek arayüzden GPT-5.5, Claude Sonnet 4.6/Opus 4.8, Gemini 3.1 Pro, DeepSeek v4 gibi modellere erişim (1:45)
- RouteLLM · teknik · Prompt'a göre en uygun modeli otomatik seçer (3:16)
- Agent modu · teknik · Kod/proje bazlı işler için chat'ten ayrı çalışma modu (2:16)
- Performans seviyesi seçimi (xHigh/High/Auto/Low) · ipucu · Zor görevlerde (site inşası gibi) yüksek performans modu seçmek sonucu iyileştiriyor (1:08)
- Agent Swarms · teknik · Birden fazla ajanı paralel çalıştırma özelliği (1:08)
- Capability eklentileri (Excel/Figma/Mockup/PDF vb.) · plugin · Göreve özel önceden tanımlı yetenek modülleri ekleme (3:16)
- Hazır proje şablonları galerisi · iş akışı · Stripe entegre site, LinkedIn outreach ajanı gibi hazır şablonlarla başlama (2:46)
- Video üretiminde ilk/son sahne belirleme · ipucu · Video modelleri iki uç kare (başlangıç+bitiş) verilerek aradaki hareketi üretiyor (5:52)
- Kling AI v3 · teknik · ChatLLM'in otomatik yönlendirdiği video üretim modeli (9:41)
- Detaylı video prompt'u (sahne/kamera/ışık tarifi) · ipucu · Sahneler arası hareketi, ışığı ve atmosferi cümle cümle tarif etmek video kalitesini artırıyor (5:52)
- Scroll'a bağlı video scrub · teknik · Scroll ilerledikçe arka plan videosunun ileri/geri sarılması (7:22)
- Site build prompt'u (renk/font/scroll/teknoloji) · prompt · Sitenin sıfırdan üretilmesi için hazırlanmış detaylı prompt (7:22)
- MCP Server Configuration · MCP · ChatLLM hesap ayarlarında MCP sunucu bağlantısı yapılandırma sayfası (12:53)
- Domain bağlama / Abacus subdomain ile yayınlama · iş akışı · Kendi domain ya da Abacus'un ".abacusai.app" subdomain'i ile tek tıkla yayınlama (11:07)
### Departman
- 4ce9-yat-sitesi-promptu/scroll-scrub-hero-video → frontend · UYARLA
- chatllm-abacus-ai → surec-ajan-arac · ÖĞREN
- agent-modu → surec-ajan-arac · ÖĞREN
- performans-seviyesi-seçimi-xhigh-high-au → surec-ajan-arac · ÖĞREN
- agent-swarms → surec-ajan-arac · ÖĞREN
- capability-eklentileri-excel-figma-mocku → surec-ajan-arac · ÖĞREN
- hazır-proje-şablonları-galerisi → surec-ajan-arac · ÖĞREN
- video-üretiminde-ilk-son-sahne-belirleme → arastirma-ogrenme · ÖĞREN
### İddialar
- ChatLLM aboneliği aylık 10 dolar (1:14 · sayısal)
- Video yaklaşık 1 dakikada, 8 saniyelik olarak üretildi (6:52 · sayısal)
- Anlatımda "20.000 kredi üzerinden 7.000 kredi harcandı" deniyor, profil ekranında Used 7.201/20.000, Remaining 12.899 gösteriliyor (12:22 · sayısal)
- "100+ Top AI Models Including SeeDance 2.0 and GPT Image 2.0" (1:45 · özellik)
- Krediler token değildir; bazı LLM'lerde 10K kredi 70.000K tokene kadar karşılık gelebilir (12:53 · özellik)
- Normalde Claude ile yapılan projelerde görseller ayrı ayrı başka AI araçlarıyla üretiliyordu, burada ChatLLM hepsini kendisi üretti (10:11 · karşılaştırma)
- Bu scroll+video tekniğini birçok firma kullanıyor, tasarım çok premium/lüks görünüyor (13:24 · öneri)
- Video üretimi 2.089 kredi, web sitesi üretimi 2.836 kredi harcadı (9:41 · sayısal)
### Site/UI
- Scroll'a bağlı video scrub animasyonu · tahmin: GSAP (ScrollTrigger) · bizde: yok
- Yumuşak/anchor kaydırma ile navbar geçişi · tahmin: GSAP ScrollToPlugin · bizde: yok
- Renk/tipografi sistemi (deep navy/ivory, Cormorant Garamond + Inter) · tahmin: Google Fonts (Cormorant Garamond, Inter) · bizde: yok
- Sabit navbar renk geçişi (transparent → ivory) · GSAP · bizde: yok
- Minimal footer + geniş whitespace grid · tahmin: CSS (grid/flex) · bizde: yok
### Prompt anatomisi
- AI üretimi kısa videoyu hero'ya scroll-scrub olarak yerleştir · 7:22 · şablon: hareket
- Aynı prompt akışını ürün türü değiştirerek tekrar kullan (yat/kahve/uçak) · 7:22 · şablon: yok
### Linkler
- https://youtu.be/4cE9t4rE0-0
- https://chatllm.abacus.ai/yzd

## brief: 2026-09-28-uygula.md
### Özellik kararları
- codex-skill/codex-exec-genel → ÖĞREN — K1: araştırma yarım, DENE verilmez (hipotez: ağır çok-dosyalı analiz Claude oturumu yerine ayrı Codex aboneliğine devredilince Claude bağlamı/tokenı büyümez · metrik: token (devredilen görev başına Claude tarafında tüketilen token) · butce: 3 görev, gerçek repo üstünde · geri_alma: skill dosyasını sil · esik: devredilen görevde Claude token tüketimi devretmeyen eşdeğerine göre ≥%30 düşmeli)
- codex-skill/imagegen → RED — güvenlik: skill "ALWAYS EXECUTES, never just describes" diyor ve fallback yolu ayrı bir API anahtarı + ayrı faturalama gerektiriyor; onay kapısı yok (kaynak: bu aday dosyasının İzinler bölümü).
- codex-skill/fleet-parallel → ZATEN VAR — zaten var: Claude Code'un kendi `run_in_background` Bash mekanizması + bu projenin `video toplu`/alt-ajan paralel dispatch deseni aynı fikri zaten karşılıyor.
- codex-skill/multi-image-referans-zinciri → ÖĞREN — niş bir CLI kullanım ipucu; bilgi kartına değer ama kurulacak bir mekanizma değil.
- claude-mm/minimax-m3-backend-degisimi → RED — lisans: yok (aday dosyasındaki bulgu, license-gate kuralı) · güvenlik: --bare OAuth bypass + veri 3. taraf (MiniMax) sunucusuna gidiyor, API anahtarı düz metin
- 4ce9-yat-sitesi-promptu/scroll-scrub-hero-video → UYARLA — zaten var: yok (kataloğumuzda scroll-scrub hero şablonu yok); aracı kurmadan fikir: mevcut site-build pipeline'ına GSAP ScrollTrigger tabanlı hero-video şablonu eklenebilir
### Departman
- codex-skill → surec-ajan-arac (1.00)
- claude-mm → surec-ajan-arac (1.00)
- 4ce9-yat-sitesi-promptu → frontend (1.00)
### İddialar
- Avenox, Codex fleet + imagegen skill'lerini tek dosyada birleştirip herkese açık yayınladı (0:51) → doğru (github.com/avenoxai/avenoxskills skills/codex-fleet/SKILL.md)
- Skill curl ile auth'suz çekiliyor (13:39) → doğru (on.md kaynak alanı (https://avenox.lol/codex.md, herhangi bir auth başlığı olmadan `video getir` ile erişildi))
- Opus'a göre 5x ucuz → abartılı (https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/)
- 1M token ~0.30$ → doğru (https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/)
- Aynı akışla sınırsız/kolayca kahve, uçak vb. başka site üretilebilir → abartılı (https://www.kdnuggets.com/2026/08/abacus/honest-abacus-ai-review)
- Scroll ile video sürüklenince site "çok premium" görünüyor → doğru (https://developer.chrome.com/docs/css-ui/scroll-driven-animations)
### Linkler
- https://avenox.lol/codex.md`
- https://avenox.lol/codex.md,
- https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/
- https://www.kdnuggets.com/2026/08/abacus/honest-abacus-ai-review
- https://developer.chrome.com/docs/css-ui/scroll-driven-animations
