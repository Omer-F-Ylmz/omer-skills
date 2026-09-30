# Composio MCP
ad: Composio MCP
tur: MCP
video: uuUo7gWuH9w
repo: composiohq/composio
lisans: bilinmiyor (repoda LICENSE dosyası var, ancak türü okunamadı; SDK açık kaynak, barındırılan servis kapalı)
son_commit: bilinmiyor (aktif görünüyor: changeset dosyaları, rc sürümleri)
arsiv: bilinmiyor
kaynak: https://github.com/ComposioHQ/composio
telemetri: bilinmiyor. Çağrılar ve kimlik bilgileri Composio bulutundan geçtiği için sunucu tarafında kayıt tutulması beklenir. Gizlilik politikası doğrulanmadı.
yildiz: bilinmiyor
alt_tur: servis
kullanim_kosullari: bilinmiyor (doğrulanmadı)
ucretsiz_katman: bilinmiyor (doğrulanmadı; fiyatlandırma sayfası kontrol edilmeli)
veri_gizliligi: bilinmiyor. Araç çağrıları ve OAuth token'ları Composio bulutundan geçer. Saklama ve eğitim politikası doğrulanmadı.
bizde_karsilik: Bizde doğrudan karşılığı yok. Tek tek MCP sunucuları (ör. Gmail) kullanılabilir.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Yapay zekâ ajanlarına 1000+ uygulamaya (Gmail vb.) önceden kimlik doğrulanmış erişim veren platform. Hesaplar web panelinde bağlanır, ajana tek MCP bağlantısıyla sunulur. SDK (TS/Python), CLI ve sağlayıcı adaptörleri de var.
## Mekanizma
Kullanıcı başına bir "session" oluşturulur. Session varsayılan olarak meta araçlar sunar: uygulama araçlarını çalışma anında keşfeder, kimlik doğrular ve çalıştırır. Yüzlerce araç tanımı bağlama yüklenmez. composio.create(user, mcp: true) ile barındırılan bir MCP uç noktası (session.mcp.url) döner. Claude, Cursor gibi istemciler buna bağlanır. OAuth/kimlik işlemleri Composio bulutunda yürür. Araç çağrıları Composio sunucularından geçer.
## Kanıt
- Birçok hesap/araç tek panelde bağlanıp tek bağlantıyla ajana sunulur → doğrulandı · README: 1000+ toolkit, oturum başına barındırılan MCP uç noktası (session.mcp.url), dashboard'tan API anahtarı.
- Araçlar isteğe bağlı keşfedilir → doğrulandı · README: varsayılan meta araçlar keşif, kimlik doğrulama ve yürütme yapar; yüzlerce araç tanımı bağlama yüklenmez.
- Tek API anahtarıyla tüm araçlar çalışır → sınanamadı · README API anahtarını anlatıyor, ancak uygulama başına yetkilendirme (OAuth) gerekebilir; çalıştırılıp denenmedi.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Dashboard'tan COMPOSIO_API_KEY alın (dashboard.composio.dev/settings)
- SDK: npm install @composio/core veya pip install composio
- Kodda: const session = await composio.create('user_id', {mcp: true}); session.mcp.url adresini MCP istemcisine ekleyin
- CLI: curl -fsSL https://composio.dev/install / sh, sonra composio login
- Web panelinde hesapları bağlayın (Gmail vb.)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tek bağlantıyla çok sayıda SaaS'a OAuth yönetimi yazmadan erişim sağlar. Bağlam şişmesini azaltır. Çok kullanıcılı ajan uygulamaları için uygundur.
## Maliyet/risk
E-posta gibi hassas hesap erişimi üçüncü taraf buluta emanet edilir. Tek API anahtarı sızarsa tüm bağlı hesaplar risk altına girer. Hizmete bağımlılık ve fiyat/limit belirsizliği var. Lisans ve ücretsiz katman doğrulanmadı. Video yalnızca demo gösteriyor.
## Tasarruf
Dolaylı bağlam tasarrufu: araçlar isteğe bağlı keşfedilir, bu yüzden yüzlerce araç şeması baştan bağlama girmez. Ölçülmüş bir oran bulunamadı.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### 1000+ önceden kimlik doğrulanmış toolkit, kullanıcı başına session
kaynak: https://github.com/ComposioHQ/composio
### Meta araçlarla çalışma anında araç keşfi, kimlik doğrulama ve yürütme
kaynak: https://github.com/ComposioHQ/composio
### Session başına barındırılan MCP uç noktası
kaynak: https://docs.composio.dev/docs/sessions-via-mcp
### CLI: search, execute, link, run komutları
kaynak: https://docs.composio.dev/docs/cli
## Destek
- uuUo7gWuH9w · 17:33 · Birçok hesap/aracı tek web panelinde bağlayıp tek bağlantıyla AI ajanlarına sunar; araçları isteğe bağlı keşfeder. · kanıt: Tek API anahtarı/bağlantı dizesiyle tüm araçlar; Gmail demosu.
