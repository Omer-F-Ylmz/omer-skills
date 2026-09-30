# Firecrawl
ad: Firecrawl
tur: plugin
video: ZSvcxjNZdxk
repo: firecrawl/firecrawl-claude-plugin
lisans: bilinmiyor
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
telemetri: bilinmiyor. README'de telemetri beyanı yok. Her istek Firecrawl bulut API'sine gider; hedef URL'ler ve sorgular sunucuya iletilir, hesap ve kredi takibi yapılır. SkillSpector --no-llm taraması eklenti repo'sunda HIGH/CRITICAL 0 buldu. CLI kaynak kodunu incelemedim.
yildiz: bilinmiyor
alt_tur: araç
kullanim_kosullari: bilinmiyor
ucretsiz_katman: Arama sonuçlarına göre ayda 1000 kredi + 1000 arama kredisi, kart gerekmez (eski kaynaklarda tek seferlik 500). Ücretli planlar: Hobby $19/ay, Standard $99, Growth $399, Scale $749. Scrape, crawl ve map sayfa/çağrı başına 1 kredi; JSON çıktısı +4 kredi.
veri_gizliligi: Kazınan URL'ler ve sorgular Firecrawl bulutuna gider. Politika ayrıntısı bilinmiyor. Self-host ile veri kendi altyapında kalır.
bizde_karsilik: Claude Code'un yerleşik WebFetch ve WebSearch araçları kısmen karşılıyor. Crawl, anti-bot ve bulut tarayıcı karşılığı bizde yok.
skillspector: SkillSpector --no-llm: HIGH/CRITICAL 0 (firecrawl-claude-plugin)
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Claude Code için resmi Firecrawl eklentisi. Firecrawl CLI'yi (firecrawl-cli) skill olarak ekler. Claude web sayfalarını aranabilir, kazınabilir, taranabilir ve haritalanabilir hâle getirir; çıktı temiz markdown veya yapılandırılmış veridir.
## Mekanizma
Eklenti kendi başına işlem yapmaz. .claude-plugin/plugin.json ile skills/ altındaki skill'leri yükler: firecrawl-search, scrape, crawl, map, interact, agent, download, monitor, parse, developer-index, research-index ve alexandria. Skill'ler Claude'a `firecrawl ...` CLI komutlarını nasıl çalıştıracağını öğretir. CLI, Firecrawl bulut API'sine (veya FIRECRAWL_API_URL ile self-host örneğe) istek atar. JS render, anti-bot ve proxy rotasyonu sunucu tarafında yapılır. Sonuçlar proje içindeki `.firecrawl/` dizinine dosya olarak yazılır. Ayrıca bulutta tarayıcı oturumu açıp Playwright kodu çalıştırma desteği var. Bir de commands/skill-gen.md komutu var; içeriğini incelemedim.
## Kanıt
- Skill dosyası ve CLI ile kurulur → doğrulandı · README: eklenti CLI'yi skill olarak ekler; `npm install -g firecrawl-cli` ve `/plugin` ile kurulum anlatılıyor; skills/ dizini ağaçta var.
- Ücretsiz kredi kotası var → doğrulandı · README 'Get your free API key' diyor. Arama sonuçlarına göre Free plan ayda 1000 kredi (eski kaynaklarda tek seferlik 500). Ben sınamadım.
- Claude'un yerleşik web erişiminden daha iyi ölçekli crawl/scrape → sınanamadı · README crawl, map, anti-bot ve proxy rotasyonu özelliklerini sayıyor. Karşılaştırmalı ölçüm yapmadım.
- Token tasarrufu sağlar → sınanamadı · Dosyaya yazma mekanizması README'de var. Nicel tasarruf bağımsız olarak ölçülmedi.
- güvenlik ön taraması: SkillSpector --no-llm HIGH/CRITICAL 0
## Kurulum
- Claude Code içinde `/plugin` çalıştır, 'firecrawl' ara ve kur
- npm install -g firecrawl-cli
- firecrawl login --browser (veya FIRECRAWL_API_KEY ortam değişkeni)
- firecrawl --status ile kimlik, eşzamanlılık ve kalan krediyi doğrula
- İsteğe bağlı: `npx -y firecrawl-cli@latest init -y --browser` tek komutla CLI, giriş ve skill kurulumunu yapar; `firecrawl setup mcp` MCP sunucusunu ekler
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude'un yerleşik web erişiminden daha güçlü: JS ağırlıklı ve bot korumalı sitelerde çalışır, tüm siteyi crawl eder, URL haritası çıkarır ve arama sonuçlarını kazır. Bağlam dosya tabanlı tutulur. Self-host seçeneği var. Ücretsiz kota ile denenebilir.
## Maliyet/risk
Bulut API'ye bağımlılık var. API anahtarı gerekir. Kredi tükenince kota sınırına takılırsın. Kazınan URL'ler ve sorgular üçüncü tarafa gider, gizli veya iç URL'lerde dikkat gerekir. `firecrawl setup defaults` Claude'un yerleşik web fetch/search'ünü kapatır. Bu değişikliği bilerek yapmalısın. Kazıdığın sayfalardaki içerik prompt injection taşıyabilir. Lisansı doğrulayamadım.
## Tasarruf
Token aracı sayılır. Sayfalar `.firecrawl/` altına dosya olarak yazılır, bağlama ham HTML girmez. Claude dosyanın yalnızca gerekli kısmını okur (grep, head vb.). Çıktı temiz markdown olduğu için ham HTML'e göre çok daha küçüktür. Üçüncü taraf bir yazıda %80 düşüş iddia ediliyor; ben ölçmedim.
## Üretilebilir
hedef_tur: skill
tarif: 'Dosyaya yaz, bağlamı temiz tut' deseni kendi skill'imize alınabilir. Skill şunları söyler: web içeriğini önce `.cache/web/<slug>.md` dosyasına indir (curl veya bir scrape CLI'si + markdown dönüştürücü), sonra yalnızca grep/head ile gereken kısmı oku. Anti-bot, JS render ve ölçekli crawl için Firecrawl API'si ya da self-host örneği gerekir. Bunu tek başına yapmak pahalıdır. Bu yüzden skill'i `firecrawl` CLI'ye ince bir sarmalayıcı olarak yazmak daha mantıklı.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Web arama (web/news/image kaynakları) ve isteğe bağlı sonuç kazıma, zaman filtresi (--tbs)
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
### Tek sayfayı JS render ederek temiz markdown'a kazıma
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
### Sitedeki tüm URL'leri haritalama (map) ve tüm siteyi crawl etme
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
### Bulut tarayıcı oturumu açıp uzaktan Playwright kodu çalıştırma
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
### Çıktıyı .firecrawl/ dizinine dosya olarak yazıp bağlamı temiz tutma
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
### Self-host desteği (FIRECRAWL_API_URL)
kaynak: https://github.com/firecrawl/firecrawl-claude-plugin
### CLI ile ek skill aileleri (core/build/workflows), MCP kurulumu ve varsayılan web sağlayıcısı yapma (setup defaults)
kaynak: https://github.com/firecrawl/cli
## Destek
- ZSvcxjNZdxk · 8:38 · Claude'un yerleşik web erişiminden daha iyi ölçekli crawl/scrape; skill dosyası ve CLI ile kurulur, ücretsiz kredi kotası var. · kanıt: Fire Crawl allows your AI agent to crawl and scrape the web
