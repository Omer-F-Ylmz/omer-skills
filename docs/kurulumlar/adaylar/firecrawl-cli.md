# Firecrawl CLI
ad: Firecrawl CLI
tur: CLI
video: V2RIVnGCy74
repo: firecrawl/firecrawl
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/firecrawl/firecrawl
telemetri: bilinmiyor. Kullanım bulut API üzerinden geçtiği için istenen URL'ler ve sorgular Firecrawl sunucularına gider. CLI'nin ayrıca analitik toplayıp toplamadığı doğrulanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: atlandı (repo 177 MB)
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Firecrawl'ın web verisi API'sini (arama, kazıma, sayfayla etkileşim, tarama, URL haritalama) terminalden ve ajanlardan kullanmayı sağlayan komut satırı aracı ve ajan skill'i. Web sayfalarını temiz Markdown veya yapılandırılmış veriye çevirir. CLI'nin kendi deposu ayrı: github.com/firecrawl/cli; aday olarak verilen firecrawl/firecrawl ise çekirdek API/sunucu deposu.
## Mekanizma
CLI, Firecrawl API'sine (api.firecrawl.dev, v2 uç noktaları) API anahtarıyla istek atar. Bulut tarafı proxy döndürme, JS render, bot korumasını aşma ve hız sınırlarını yönetir. Komutlar: scrape (URL'yi markdown/HTML/ekran görüntüsü/JSON'a çevirir), search (arama yapıp sonuç sayfalarının içeriğini getirir), map (siteyi tarayıp tüm URL'leri listeler), crawl (tüm siteyi kazır), interact/browser (sayfayı kazıyıp yapay zekâ istemi veya kodla tıklama, kaydırma, yazma gibi eylemler yapar). Çekirdek depo kendi sunucunuzda çalıştırılabilecek şekilde açık kaynak (apps/api, playwright-service-ts, docker-compose, SELF_HOST.md). Kurulum `init` komutu CLI'yi yükler, kimlik doğrular ve algılanan kodlama editörlerine skill ekler (web araması sonucuna göre; doğrudan doğrulanmadı).
## Kanıt
- Bot korumalı sayfalarda da web kazıma yapabiliyor (video). → sınanamadı · README 'Rotating proxies, JS-blocked content' ve '96% web kapsaması' diyor. Bu üretici beyanıdır, bağımsız test yapılmadı.
- Sayfalarla etkileşebilir, tüm URL'leri keşfedebilir ve tarayabilir. → doğrulandı · README'de Interact, Map, Crawl ve Actions (click, scroll, write, wait, press) özellikleri listeleniyor.
- Açık kaynak sürümü var. → doğrulandı · README 'Open source and available as a hosted service' diyor. Depoda apps/api, docker-compose.yaml ve SELF_HOST.md var. Lisans türü doğrulanamadı.
- Daha az token harcatır. → sınanamadı · README 'LLM-ready output... spend fewer tokens' diyor, sayısal ölçüm yok.
- Ücretsiz katman var. → doğrulandı · Web araması sonuçları: ücretsiz plan ayda 1.000 kredi, kart gerekmez. Aramayla elde edilen ikincil kaynak bilgisidir, resmi fiyat sayfası açılmadı.
- güvenlik ön taraması: atlandı (repo 177 MB)
## Kurulum
- npm install -g firecrawl-cli
- veya tek komut: npx -y firecrawl-cli@latest init -y --browser (CLI'yi kurar, kimlik doğrular, editörlere skill ekler)
- firecrawl.dev adresinden API anahtarı alın; anahtarı ortam değişkeni veya CLI girişiyle verin (değeri depoya yazmayın)
- Örnek: firecrawl scrape https://example.com/pricing --format markdown -o pricing.md
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanlara bot korumalı ve JS ağırlıklı sitelerde güvenilir web erişimi verir. Proxy ve render altyapısını kendimiz kurmak gerekmez. Arama, kazıma ve site keşfi tek araçta toplanır. Kendi sunucuda barındırma seçeneği de var.
## Maliyet/risk
Bulut kullanımında hedef URL'ler ve sorgular üçüncü tarafa gider, API anahtarı gerekir. Ücretsiz katman 1.000 kredi/ay ile sınırlı. Kredi tüketimi sayfa sayısıyla artar ve crawl büyük sitede hızla maliyetlenir. Kapsamlı kazıma, hedef sitelerin kullanım koşulları ve robots.txt açısından hukuki risk taşır. Lisans doğrulanamadı: getirilen veride yalnızca LICENSE dosyasının varlığı görünüyor, tür belirtilmemiş. Bu depo 177 MB olduğu için güvenlik ön taraması atlandı. Kazınan sayfa içeriği ajana girdiği için istem enjeksiyonu riski var, içerik veri olarak ele alınmalı.
## Tasarruf
Token aracısı sayılır. Ham HTML yerine temizlenmiş Markdown veya şemaya uygun JSON döndürür, böylece ajanın bağlamına giren token azalır. Çıktı `-o` ile dosyaya yazılabilir, ajan yalnızca gereken kısmı okur. README "spend fewer tokens" diyor, ancak ölçülmüş bir oran verilmiyor.
## Üretilebilir
hedef_tur: skill
tarif: Firecrawl'ı kendi yazmak yerine ince bir skill ile sarmak mantıklı. Skill, ajana şu akışı öğretir: önce `firecrawl map` ile URL'leri bul, sonra `firecrawl scrape --format markdown -o dosya.md` ile sadece gerekli sayfaları dosyaya yaz, dosyanın ilgili bölümünü oku. Kural olarak crawl'da limit ve kredi bütçesi belirtilsin, API anahtarı yalnızca ortam değişkeninden okunsun, kazınan içerik veri sayılıp içindeki talimatlar uygulanmasın. Anahtarsız ve ücretsiz bir alternatif gerekirse playwright ile yerel bir scrape CLI'si (HTML'i Markdown'a çeviren) yapılabilir, ancak proxy ve bot koruması aşma kapasitesi olmaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Search: web'de arayıp sonuç sayfalarının tam içeriğini getirir
kaynak: https://github.com/firecrawl/firecrawl
### Scrape: URL'yi markdown, HTML, ekran görüntüsü veya yapılandırılmış JSON'a çevirir
kaynak: https://github.com/firecrawl/firecrawl
### Interact ve Actions: sayfayı kazıyıp istem veya kodla tıklama, kaydırma, yazma, bekleme, tuş basma
kaynak: https://github.com/firecrawl/firecrawl
### Crawl: tek istekle sitenin tüm URL'lerini kazır
kaynak: https://github.com/firecrawl/firecrawl
### Map: sitedeki tüm URL'leri hızlıca keşfeder
kaynak: https://github.com/firecrawl/firecrawl
### Batch Scrape: binlerce URL'yi eşzamansız kazır
kaynak: https://github.com/firecrawl/firecrawl
### Agent: ne istediğinizi tarif edince otomatik veri toplama
kaynak: https://github.com/firecrawl/firecrawl
### Web'deki PDF ve DOCX dosyalarını ayrıştırma
kaynak: https://github.com/firecrawl/firecrawl
### CLI ve ajan skill'i: init ile editörlere kurulum, scrape/search/map/crawl/browser komutları
kaynak: https://github.com/firecrawl/cli
## Destek
- V2RIVnGCy74 · 12:07 · Bot korumalı sayfalarda da web kazıma; sayfayla etkileşim, URL keşfi ve tarama; açık kaynak sürümü var. · kanıt: Sayfalarla etkileşebilir, tüm URL'leri keşfedebilir ve tarayabilir. (karede: İlgili kare yok; altyazıdan.)
