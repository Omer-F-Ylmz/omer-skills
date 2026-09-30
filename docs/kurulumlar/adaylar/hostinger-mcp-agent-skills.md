# Hostinger MCP + agent skills
ad: Hostinger MCP + agent skills
tur: MCP
video: ZSvcxjNZdxk
repo: hostinger/api-mcp-server
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/hostinger/api-mcp-server
telemetri: Yerel kodda telemetri olduğuna dair kanıt ön getirmede yok; README tamamı (4729 satır kesildi) okunmadı, bilinmiyor. Bilinen: uzak modda istekler Hostinger'ın mcp.hostinger.com ve auth.hostinger.com sunucularından geçer. Yerelde OAuth tokenları diske yazılır (0600).
yildiz: 156 (web arama sonucu, kesin güncel değil)
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Hostinger'ın resmi MCP sunucusu. Claude Code gibi bir istemciden Hostinger hesabındaki VPS, domain, DNS, hosting, WordPress, e-posta, e-ticaret, faturalama ve Reach işlemlerini yönetmeyi sağlar. Repo ayrıca 7 agent skill içerir: audit-hosting, connect-domain, deploy-to-hosting, headless, maintain-wordpress, migrate-to-hosting, troubleshoot-website.
## Mekanizma
İki kullanım şekli var. (1) Barındırılan uzak sunucu https://mcp.hostinger.com, Streamable HTTP ile bağlanır, OAuth ile yetkilendirilir. Claude Code için: `claude mcp add --transport http hostinger https://mcp.hostinger.com`. (2) Yerel stdio sunucusu, npm paketi @hostinger/mcp (Node 24+). Yerel sunucu HOSTINGER_API_TOKEN ile ya da OAuth 2.0 PKCE ile (dinamik istemci kaydı, yerel geçici port, kimlik bilgileri ~/.config/hostinger-mcp/credentials.json) kimlik doğrular. Güncel README'ye göre her binary aynı üç aracı sunar: arama (search), çalıştırma (execute) ve bir üçüncüsü (adı ön getirmede yok). Tüm operasyonlar (toplam 403) bu araçlar üzerinden aranıp çalıştırılır. Kapsamlı binary'ler yalnızca kendi grubunu arar: vps 64, hosting 75, domains 42, mail 38 vb. Videodaki "118 araç" sayısı eski sürüme ait görünüyor; güncel README her operasyonu tek tek araç olarak değil, üç araç arkasında sunuyor.
## Kanıt
- Claude Code'dan VPS kurma, domain, DNS, site deploy yapılabiliyor (video) → doğrulandı · README, vps/domains/dns/hosting operasyon gruplarını ve deploy-to-hosting, connect-domain skill'lerini listeliyor.
- 118 araç sunuyor (video) → çürütüldü · Güncel README toplam 403 operasyonu tek bir birleşik sunucuda listeliyor ve her binary'nin aynı üç aracı sunduğunu söylüyor. 118 sayısı eski sürüm olabilir.
- Hostinger hesabı ve API token gerekir (video) → doğrulandı · README: HOSTINGER_API_TOKEN ya da OAuth girişi gerekiyor; token yoksa OAuth açılıyor.
- MIT lisanslı, 156 yıldız → doğrulandı · Web arama sonucu MIT ve 156 yıldız gösteriyor; repoda LICENSE dosyası var. LICENSE içeriği doğrudan okunmadı.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- Uzak sunucu (kurulumsuz): claude mcp add --transport http hostinger https://mcp.hostinger.com (tarayıcıda OAuth onayı)
- Yerel: npm install -g @hostinger/mcp (Node.js 24+ gerekir)
- Yerelde token ile: HOSTINGER_API_TOKEN ortam değişkenini ayarla (değeri repoya yazma); binary: hostinger-api-mcp veya kapsamlı hostinger-vps-mcp, hostinger-dns-mcp vb.
- Skill'ler için repodaki skills/ klasörü kullanılır
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude Code'dan doğal dille VPS kurma, domain bağlama, DNS düzenleme, site deploy, WordPress bakımı ve hosting taşıma yapılabilir. Hazır skill'ler bu iş akışlarını yönlendirir. Hostinger müşterisi olan biri için yararlı.
## Maliyet/risk
Gerçek hesapta yıkıcı işlemler yapabilir: VPS silme/yeniden kurma, DNS değiştirme, ücretli satın alma, domain işlemleri. API token geniş yetkilidir; sızarsa hesap risk altındadır. Uzak modda hesap verisi üçüncü taraf sunucudan geçer. Hostinger hesabı ve API erişimi şart. Güvenlik taraması yapılmadı (SkillSpector raporu yok); skill içerikleri incelenmedi. Kullanırken silme ve satın alma çağrılarını elle onaya bağla.
## Tasarruf
Token aracı değil. Yine de 403 operasyonu üç araç arkasında toplayıp arama ile bulduruyor; bu tasarım araç şeması için bağlam maliyetini düşürür. Ölçülmedi.
## Üretilebilir
hedef_tur: skill
tarif: MCP'nin kendisini yeniden yapmaya gerek yok, resmi olanı kullanılır. Kendi skill'imiz için repodaki skills/ klasörü (özellikle connect-domain ve deploy-to-hosting) örnek alınır: aynı iş akışı adımlarını kendi hosting sağlayıcımıza uyarlayan bir SKILL.md yazılır. Yıkıcı adımlar için kullanıcı onayı şartı eklenir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Uzak barındırılan MCP sunucusu (OAuth, kurulumsuz)
kaynak: https://github.com/hostinger/api-mcp-server
### Alana özel binary'ler: vps, dns, domains, hosting, mail, wordpress, billing, ecommerce, reach, horizons, agency-hosting
kaynak: https://github.com/hostinger/api-mcp-server
### Token veya OAuth 2.0 PKCE ile kimlik doğrulama
kaynak: https://github.com/hostinger/api-mcp-server
### 7 hazır agent skill (audit-hosting, connect-domain, deploy-to-hosting, headless, maintain-wordpress, migrate-to-hosting, troubleshoot-website)
kaynak: https://github.com/hostinger/api-mcp-server/tree/main/skills
## Destek
- ZSvcxjNZdxk · 5:40 · Claude Code'dan VPS kurma, domain, DNS, site deploy; 118 araç sunar. Hostinger hesabı ve API token gerekir. · kanıt: hosting our MCP is connected with 118 different tools
