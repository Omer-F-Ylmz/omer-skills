# GitHub MCP server
ad: GitHub MCP server
tur: MCP
video: uuUo7gWuH9w
repo: github/github-mcp-server
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/github/github-mcp-server
telemetri: Yerel ikilide telemetri olup olmadığı bu incelemede doğrulanamadı: kaynak kodu okunmadı, yalnızca README ve dizin ağacı görüldü. Ağaçta pkg/observability ve internal/profiler var, ama ne topladıkları bilinmiyor. Uzak sunucu GitHub/Copilot altyapısında çalıştığı için istekler GitHub tarafından işlenir.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
GitHub'ın resmi MCP sunucusu. Yapay zekâ araçlarının GitHub'a doğal dille erişmesini sağlar: depo ve kod okuma, issue/PR yönetimi, GitHub Actions çalıştırmalarını izleme, güvenlik bulguları ve Dependabot uyarıları, tartışmalar, bildirimler.
## Mekanizma
İki kipte çalışır. (1) Uzak sunucu: GitHub'ın barındırdığı https://api.githubcopilot.com/mcp/ adresine HTTP MCP olarak bağlanılır. Kimlik doğrulama OAuth ya da `Authorization: Bearer <PAT>` başlığıyla yapılır. (2) Yerel sunucu: Go ile yazılmış `github-mcp-server` ikilisi ya da Docker imajı yerelde çalışır. MCP araçları GitHub REST ve GraphQL API çağrılarına çevrilir. Araçlar toolset'ler halinde gruplanır. Toolset belirtilmezse varsayılan toolset'ler açılır. Repo ayrıca şunları içerir: insiders kipi, salt okunur ve scope filtreleme, lockdown (pkg/lockdown), girdi temizleme (pkg/sanitize), GitHub App kimlik doğrulaması ve politika/yönetişim belgeleri. Claude Code için `claude mcp add` ile eklenir. Videoda PAT ile bu yol kullanılıyor.
## Kanıt
- Resmi GitHub plugini çalışmıyor; alternatif olarak MCP sunucusu PAT ile claude mcp add üzerinden ekleniyor (video). → sınanamadı · Videonun iddiası. Plugin durumu bu incelemede denenmedi. README'de PAT ile uzak sunucu yapılandırması ve Claude kurulum rehberi (docs/installation-guides/install-claude.md) var, yani PAT yolu destekleniyor.
- Sunucu repo yönetimi sağlıyor. → doğrulandı · README kullanım alanları: depo ve kod gezinme, issue/PR yönetimi, Actions izleme, güvenlik bulguları.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- Yalnızca gereken yetkilerle bir GitHub PAT oluştur. Değeri sohbete ya da repoya yazma; ortam değişkeninde tut.
- Uzak sunucu (Claude Code): claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer $GITHUB_PAT"
- Yerel alternatif: Docker imajıyla ya da `github-mcp-server stdio` ikilisiyle çalıştır. GITHUB_PERSONAL_ACCESS_TOKEN ortam değişkeni gerekir. Ayrıntı: docs/installation-guides/install-claude.md
- Gerekirse toolset'leri kısıtla (başlık ya da bayrakla) ve salt okunur kipi aç.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Videodaki resmi GitHub plugini bozuk olduğu için güvenilir bir yol sunar. Ajan, `gh` CLI'a ya da elle API çağrısına gerek kalmadan repo, issue, PR ve CI işlerini yapabilir.
## Maliyet/risk
PAT geniş yetkiliyse ajan yazma, silme ve PR açma gibi işlemler yapabilir. Halka açık issue/PR içeriği prompt injection kaynağı olabilir. Bu yüzden lockdown kipi ve salt okunur kip var. Çok araç, bağlamı şişirir. Yerel `gh` CLI çoğu işi aynı şekilde yapabilir. Tarama raporu yok: SkillSpector koşmadı. Yıldız sayısı ve son commit doğrulanmadı.
## Tasarruf
Token tasarrufu aracı değil. Tersine, çok sayıda araç tanımı bağlamı şişirir. Toolset seçimi, salt okunur kip ve pkg/tooldiscovery ile bu yük azaltılabilir.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Uzak (GitHub barındırmalı) ve yerel sunucu seçeneği; OAuth ya da PAT ile kimlik doğrulama
kaynak: https://github.com/github/github-mcp-server
### Toolset yapılandırması ile araç alt kümesi seçimi
kaynak: https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md
### Politika ve yönetişim ile scope filtreleme belgeleri
kaynak: https://github.com/github/github-mcp-server/blob/main/docs/policies-and-governance.md
### Claude Code dahil birçok istemci için kurulum rehberleri
kaynak: https://github.com/github/github-mcp-server/blob/main/docs/installation-guides/install-claude.md
## Destek
- uuUo7gWuH9w · 5:06 · Resmi GitHub plugini bozuk olduğundan GitHub'ın MCP sunucusu PAT ile claude mcp add üzerinden eklenir; repo yönetimi sağlar. · kanıt: Resmi GitHub plugini çalışmıyor; alternatif olarak varsayılan MCP sunucusu kuruluyor.
