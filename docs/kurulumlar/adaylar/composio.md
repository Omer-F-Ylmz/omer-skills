# Composio
ad: Composio
tur: MCP
video: ZSvcxjNZdxk
repo: composiohq/composio
lisans: bilinmiyor (repoda LICENSE dosyası var ama içeriği okunamadı; MIT olduğu yaygın bilgi, doğrulanmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/ComposioHQ/composio
telemetri: bilinmiyor. Not: araç çağrıları ve kimlik doğrulama Composio'nun barındırılan API'si üzerinden geçtiği için çağrı verisi dış servise gider; ayrıca SDK/CLI telemetrisi okunan README bölümünde belirtilmemiş, doğrulanmadı.
yildiz: bilinmiyor
alt_tur: servis
kullanim_kosullari: bilinmiyor (composio.dev kullanım koşulları okunmadı)
ucretsiz_katman: bilinmiyor (API anahtarı dashboard'dan alınıyor; ücretsiz katman limitleri doğrulanmadı)
veri_gizliligi: Araç çağrıları ve bağlı hesap kimlik bilgileri/OAuth token'ları Composio'nun barındırılan altyapısından geçer/orada tutulur; saklama ve gizlilik politikası okunmadı, bilinmiyor.
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
1000+ uygulama/araç paketini (toolkit) önceden kimlik doğrulamalı, kullanıcı bazlı oturumlarla AI ajanlarına bağlayan platform. Monorepo: TypeScript SDK (@composio/core), Python SDK (composio), `composio` CLI ve OpenAI, Claude Agent SDK, Vercel AI SDK, LangChain vb. için sağlayıcı adaptörleri. Her oturum barındırılan (hosted) bir MCP uç noktası da sunar; Claude, Cursor gibi istemciler buna bağlanabilir.
## Mekanizma
Uygulama: composio.create(user_id) ile kullanıcıya özel oturum açılır. Oturum varsayılan olarak tüm araç tanımlarını yüklemek yerine "meta araçlar" verir; bunlar çalışma anında uygun aracı keşfeder, kimlik doğrulamayı (OAuth/bağlantı) yapar ve çalıştırır. MCP modunda (mcp: true) session.mcp.url adresi istemciye verilir. CLI: `composio search` (araç bul), `composio execute` (çalıştır), `composio link` (hesap bağla), `composio run` (TypeScript ile iş akışı). Araçlar ve kimlik bilgileri Composio'nun bulut hesabında durduğu için makineler arası taşınır; çalıştırma Composio API'si üzerinden yapılır ve COMPOSIO_API_KEY gerekir.
## Kanıt
- Tüm uygulama bağlantılarını tek yerde tutar → doğrulandı · README: 1000+ önceden kimlik doğrulamalı toolkit, kullanıcı bazlı oturumlar ve bağlı hesaplar.
- Claude araçları isteğe bağlı keşfeder, token tasarrufu sağlar → doğrulandı · README: varsayılan oturum, araçları çalışma anında keşfeden/doğrulayan/çalıştıran meta araçlar verir, yüzlerce araç tanımını bağlama yüklemez. Tasarruf oranı ölçülmedi.
- Makineler arası taşınır → sınanamadı · Oturumlar session_id ile yeniden kullanılıyor ve hesaplar bulutta; makineler arası taşınma çıkarımsal, denenmedi.
- Claude'da çok araç bağlamı hızla şişirir → sınanamadı · Videodaki söz; bağımsız ölçüm yapılmadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- CLI: curl -fsSL https://composio.dev/install / sh ; yeni terminal açıp `composio login`
- TypeScript: npm install @composio/core (+ sağlayıcı paketi, ör. @composio/openai-agents); daha küçük kurulum için @composio/slim
- Python: pip install composio (+ ör. composio-openai-agents)
- COMPOSIO_API_KEY'i dashboard.composio.dev/settings adresinden al (değeri depoya yazma)
- MCP: composio.create(user, { mcp: true }) sonrası session.mcp.url'yi Claude/Cursor MCP istemcisine ekle
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Tek bir yerde tüm uygulama bağlantıları (Gmail, Slack, GitHub vb.) ve kimlik doğrulamaları; her MCP sunucusunu ayrı ayrı kurma ve bağlamı şişirme derdi yok; hesaplar makineler arası taşınır; Claude araçları isteğe bağlı keşfeder.
## Maliyet/risk
Tüm uygulama hesaplarının (e-posta, takvim, depo vb.) OAuth yetkileri üçüncü taraf bulutta tutulur; yüksek güven ve veri sızıntısı riski. Yazma yetkili eylemler (e-posta gönderme vb.) ajan tarafından otomatik yapılabilir, onay politikası gerekir. Satıcıya bağımlılık, API anahtarı yönetimi, ücretsiz katman/fiyat sınırları bilinmiyor. Lisans doğrulanmadı.
## Tasarruf
Bağlam (token) tasarrufu: yüzlerce araç şemasını başta yüklemek yerine birkaç meta araç verir; gerçek araç tanımları yalnızca ihtiyaç anında keşfedilir. Video da bunu söylüyor (çok MCP aracının bağlamı hızla şişirdiği). Ölçülmüş oran bilinmiyor.
## Üretilebilir
hedef_tur: MCP
tarif: Composio'nun tamamı kopyalanamaz (bulut OAuth altyapısı). Ama 'tembel araç keşfi' deseni yapılabilir: tek bir MCP sunucusu yalnızca 3 meta araç açar (search_tools, get_tool_schema, execute_tool). Kendi araç kataloğumuzu (yerel CLI/API sarmalayıcıları) indeksleyip anahtar kelime/embedding ile arar, şemayı yalnızca seçilince döndürür ve çağrıyı yönlendirir. Gizli bilgiler yerel ortam değişkeni/anahtar deposunda kalır. Alternatif: Composio CLI'yi saran ince bir skill.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### 1000+ önceden kimlik doğrulamalı toolkit, kullanıcı bazlı oturumlar, tetikleyiciler (triggers) ve sandbox
kaynak: https://github.com/ComposioHQ/composio
### Meta araçlarla çalışma anında araç keşfi/kimlik doğrulama/çalıştırma (bağlamı şişirmez)
kaynak: https://github.com/ComposioHQ/composio
### Oturum başına barındırılan MCP uç noktası (Claude, Cursor vb.)
kaynak: https://docs.composio.dev/docs/sessions-via-mcp
### CLI: search, execute, link, run komutları
kaynak: https://docs.composio.dev/docs/cli
### OpenAI, Anthropic, Claude Agent SDK, Vercel AI, LangChain sağlayıcı adaptörleri
kaynak: https://github.com/ComposioHQ/composio
## Destek
- ZSvcxjNZdxk · 12:48 · Tüm uygulama bağlantılarını tek yerde tutar; Claude araçları isteğe bağlı keşfeder, token tasarrufu sağlar, makineler arası taşınır. · kanıt: it can actually bloat the context quite quickly in Claude
