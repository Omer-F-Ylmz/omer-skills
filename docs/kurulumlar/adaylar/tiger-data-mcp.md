# Tiger Data MCP
ad: Tiger Data MCP
tur: MCP
video: uuUo7gWuH9w
repo: timescale/tiger-cli
lisans: bilinmiyor (repoda LICENSE ve NOTICE dosyası var, ama türü okunamadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/timescale/tiger-cli
telemetri: Repoda internal/analytics paketi var, yani kullanım analitiği toplanıyor olabilir. İçeriği, neyin gönderildiği ve kapatma yolu doğrulanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-6)
## Ne
Tiger Cloud (Timescale, şimdiki adıyla Tiger Data) için Go ile yazılmış komut satırı aracı. İçinde MCP sunucusu var. Claude gibi yapay zekâ asistanları bu sunucuyla Postgres/TimescaleDB servisleri oluşturabilir, yönetebilir, fork alabilir ve sorgu çalıştırabilir.
## Mekanizma
MCP sunucusu ayrı bir paket değil, `tiger` ikili dosyasının içine gömülü. Araçlar CLI komutlarının karşılığıdır: servis list/create/fork/start/stop/resize/delete, db query, logs. `tiger auth login` ile Tiger Cloud'a giriş yapılır. `tiger mcp install` Claude Code, Cursor, Windsurf, Codex, Gemini CLI ve VS Code istemcilerinin yapılandırmasını otomatik yazar (pkg/mcpinstall). Claude Code için `tiger mcp install claude-code` kullanılır. Komutlar Tiger Cloud API'sine (openapi.yaml) gider. Sunucuda ayrıca Postgres/Timescale dokümantasyonu ve en iyi uygulama istemleri de bulunduğu belirtiliyor; bunu doğrulamadım.
## Kanıt
- `tiger mcp install` ile MCP kurulur → doğrulandı · Repo README'sindeki Quick Start bölümünde `tiger mcp install` komutu yer alıyor. Web araması Claude Code için `tiger mcp install claude-code` kullanımını da gösteriyor.
- Claude servis fork alabilir → doğrulandı · README'de `tiger service fork` komutu var. MCP araçlarının CLI'yi yansıttığı belirtiliyor. Araç adlarını tek tek kontrol etmedim.
- Claude tablo oluşturur ve sorgu çalıştırır; hypertable ile optimize eder → sınanamadı · `tiger db query` komutu var, ama hypertable optimizasyonunu yapan MCP aracını ya da davranışını doğrulamadım. Canlı deneme yapmadım.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- curl -fsSL https://cli.tigerdata.com / sh (Windows: irm https://cli.tigerdata.com/install.ps1 / iex; ayrıca brew, apt, yum, go install)
- tiger auth login
- tiger mcp install claude-code (istemci adı verilmezse etkileşimli seçim çıkar)
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Claude komut satırına ya da panele geçmeden doğrudan gerçek Postgres/TimescaleDB oluşturabilir ve yönetebilir. Fork sayesinde veritabanının kopyasında güvenle deneme yapılabilir. Hypertable ile optimizasyon ve şema/sorgu işleri aynı akışta yürür.
## Maliyet/risk
Video sponsorlu, bu yüzden tanıtım tonu var. Claude'a canlı bulut veritabanı üzerinde silme, yeniden boyutlandırma ve sorgu yetkisi verilir. Bu yetkiler hatalı kullanılırsa veri kaybına veya maliyete yol açabilir. Bir Tiger Cloud hesabı gerekir ve ücretlendirme/ücretsiz katman doğrulanmadı. Kurulum `curl / sh` ile yapılıyor. Telemetri belirsiz.
## Tasarruf
Token aracı değil.
## Üretilebilir
hedef_tur: yok
tarif: yok
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-6/panel.md → Ömer sütunu
## Özellikler
### Servis yaşam döngüsü: oluşturma, fork, başlatma/durdurma, yeniden boyutlandırma, silme, loglar
kaynak: https://github.com/timescale/tiger-cli
### Tek komutla birçok istemciye MCP kurulumu (claude-code, cursor, windsurf, codex, gemini, vscode)
kaynak: https://www.tigerdata.com/docs/ai/latest/mcp-server
### `tiger db query` ile psql olmadan sorgu çalıştırma
kaynak: https://github.com/timescale/tiger-cli
## Destek
- uuUo7gWuH9w · 10:15 · Claude'a gerçek Postgres/TimescaleDB veritabanı kurup yönetme, fork alma ve hypertable ile optimize etme yeteneği verir (sponsorlu). · kanıt: Claude tablo oluşturur, sorgu çalıştırır; tiger mcp install ile kurulur.
