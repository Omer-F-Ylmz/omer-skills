# Firecrawl CLI ve skill
ad: Firecrawl CLI ve skill
tur: CLI
video: OFyECKgWXo8
repo: firecrawl/cli
lisans: ISC
son_commit: bilinmiyor (npm sürümü 1.25.0)
arsiv: bilinmiyor
kaynak: https://github.com/firecrawl/cli
telemetri: Bilinmiyor. README'nin okunan kısmında telemetri anlatılmıyor. Ancak işlem bulut API'si üzerinden yapıldığı için istenen URL'ler ve sorgular Firecrawl sunucularına gider. Kurulum betiğini çalıştırmadan önce kaynağını incelemek gerekir.
yildiz: 642
alt_tur: araç
skillspector: bilinmiyor
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Firecrawl web API'sinin komut satırı aracı. Web sayfalarını ajanların okuyabileceği temiz çıktıya çevirir. Komutlar: scrape, crawl, map, search, interact, agent, parse, download. Makale arama indeksi de var (PubMed, arXiv vb.). Claude Code, Codex, Cursor gibi ajanlara skill ve MCP kurar.
## Mekanizma
CLI, resmi `firecrawl` Node SDK'sı (4.40.0) üzerinden Firecrawl bulut API'sine istek atar. Sayfayı işleyip markdown ya da yapılandırılmış veri döndürür. `init` veya `setup` komutları skill dosyalarını (skills/firecrawl-scrape, -search, -crawl, -map, -interact vb.) algılanan ajan editörlerine kopyalar. Skill'ler ajana CLI'yi ne zaman ve nasıl çağıracağını öğretir. `setup defaults` ajanın yerleşik web fetch/search araçlarını kapatıp web işini Firecrawl'a yönlendirir. Çalışması için API anahtarı ve giriş gerekir; scraping bulutta yapılır.
## Kanıt
- Komutlar scrape, crawl, map ve search → doğrulandı · README ilk satırı ve skills/ dizini: firecrawl-scrape, -crawl, -map, -search. Ek olarak interact, agent, parse, download, monitor da var.
- Tek satırlık kurulum skill'i de içeriyor → doğrulandı · README: `npx -y firecrawl-cli@latest init -y --browser` CLI'yi kurar, giriş yaptırır ve skill'leri algılanan editörlere ekler.
- Web search aracından üstündür → sınanamadı · Yalnız videodaki görüş. Kendim karşılaştırmadım. Video sayfası getirildiğinde yalnız başlık geldi, transkript gelmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- npm install -g firecrawl-cli (Node >=22)
- npx -y firecrawl-cli@latest init -y --browser (CLI, giriş ve skill'lerin tek satırlık kurulumu)
- firecrawl setup core / build / workflows (skill aileleri)
- firecrawl setup mcp (MCP sunucusunu editörlere ekler)
- firecrawl init --agent claude-code (yalnız tek ajana kurulum)
- İsteğe bağlı: curl -fsSL https://firecrawl.dev/install.sh / bash
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanlara güvenilir web scraping, arama ve site haritalama yeteneği verir. JS ile render edilen ve korumalı sayfaları da alabilir. Tek komutla birçok ajana skill kurar. Video, web search aracından üstün bulunduğunu söylüyor.
## Maliyet/risk
Bulut servisine bağımlı: API anahtarı gerekir, kullanım kredi ile sınırlı ve ücretli olabilir. Fiyat ve ücretsiz katman doğrulanmadı. `setup defaults` ajanın yerleşik web araçlarını devre dışı bırakır, bunu bilerek kullanmak gerekir. Sayfa içeriği ajana doğrudan girdiği için prompt injection riski var. `curl / bash` kurulum yolu riskli. Skill'ler global kurulur ve tüm ajanlara yayılır.
## Tasarruf
Token tasarrufu hedefli ama sayısal ölçüm yok. Sayfalar ham HTML yerine temiz markdown olarak döner, bu bağlamı küçültür. Ajan tarayıcı açıp sayfayı ayrıştırmaya uğraşmaz. Somut bir oran bulamadım.
## Üretilebilir
hedef_tur: skill
tarif: Firecrawl CLI'yi olduğu gibi kullanmak daha mantıklı. Kendi skill'imiz için: SKILL.md içinde `firecrawl scrape <url> --format markdown` ve `firecrawl search` çağrılarını, hangi durumda kullanılacağını ve çıktıyı dosyaya yazıp yalnız gereken kısmı okuma kuralını yaz. Bulut bağımlılığı istemezsek Playwright ve readability/turndown ile yerel bir scrape CLI'si yazılabilir, ama JS ve bot korumasında Firecrawl kadar güçlü olmaz.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### scrape/crawl/map/search/interact/agent komutları ve ajan dostu temiz çıktı
kaynak: https://github.com/firecrawl/cli
### Tek komutla 8 ajana (Claude Code, Codex, Cursor, Windsurf vb.) skill ve MCP kurulumu
kaynak: https://github.com/firecrawl/cli
### setup defaults ile yerleşik web araçlarını Firecrawl'a yönlendirme
kaynak: https://github.com/firecrawl/cli
### Araştırma makalesi indeksi araması (PubMed, bioRxiv, medRxiv, arXiv)
kaynak: https://github.com/firecrawl/cli/blob/main/package.json
## Destek
- OFyECKgWXo8 · 14:39 · Yapay zekâ ajanlarına uygun çıktı veren web scraping aracı. Komutları scrape, crawl, map ve search. · kanıt: Tek satırlık kurulum skill'i de içeriyor; web search aracından üstün bulunuyor.
