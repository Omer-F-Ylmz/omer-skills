# Chrome DevTools
ad: Chrome DevTools
tur: MCP
video: jqoFP9QapXI
repo: chromedevtools/chrome-devtools-mcp
lisans: Apache-2.0 (LICENSE dosyası repoda var; SPDX kimliği README'den doğrulanmadı, projenin bilinen lisansı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/ChromeDevTools/chrome-devtools-mcp
telemetri: Google kullanım istatistiği toplar (araç çağrı başarı oranı, gecikme, ortam bilgisi). Varsayılan AÇIK. `--no-usage-statistics` bayrağı ya da CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS veya CI ortam değişkeni ile kapanır. Performans araçları iz URL'lerini Google CrUX API'sine gönderebilir; `--no-performance-crux` ile kapanır. Npm kayıt defterinden periyodik güncelleme kontrolü yapar; CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS ile kapanır.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
Kodlama ajanının (Claude, Cursor, Copilot, Antigravity vb.) canlı bir Chrome tarayıcısını kontrol edip incelemesini sağlayan resmi Chrome DevTools MCP sunucusu. Ajan sayfayı açar, tıklar, form doldurur, ağ isteklerini, konsol mesajlarını ve ekran görüntüsünü okur, performans izi kaydeder. MCP'siz kullanım için CLI de var. Videoda ("hack 21") uygulamanın işlevselliğini tarayıcıda test ettirmek için öneriliyor.
## Mekanizma
Node.js ile yazılmış MCP sunucusu. İlk tarayıcı gerektiren araç çağrısında Chrome'u başlatır. Otomasyon için Puppeteer kullanır ve eylem sonuçlarını otomatik bekler. Performans izlerinden içgörü çıkarmak için devtools-frontend kodunu kullanır. Konsol mesajlarını source-map'li yığın izleriyle verir. Ayrıca skills/ altında a11y-debugging, debug-optimize-lcp, memory-leak-debugging, cookie-debugging gibi skill'ler ve Claude/Cursor/Gemini plugin manifestleri var. `--slim` modu az sayıda temel araç açar. `--headless` desteklenir.
## Kanıt
- Videoda: Chrome DevTools tarayıcıyı açıp uygulama işlevselliğini test eder → doğrulandı · README: MCP sunucusu ajanın canlı Chrome'u kontrol etmesini, Puppeteer ile eylem otomasyonunu, ağ/konsol incelemesini ve ilk istemde tarayıcıyı açıp performans izi kaydetmeyi anlatıyor. Araç çağrısı yapılarak çalıştırılmadı.
- Lisans Apache-2.0 → sınanamadı · Repo ağacında LICENSE dosyası var ama içeriği okunmadı; Apache-2.0 bilgiye dayanıyor.
- Telemetri varsayılan açık ve kapatılabilir → doğrulandı · README 'Usage statistics' bölümü: varsayılan etkin, --no-usage-statistics ile kapanır.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- MCP istemci yapılandırmasına ekle: {"mcpServers":{"chrome-devtools":{"command":"npx","args":["-y","chrome-devtools-mcp@latest"]}}}
- Gereksinimler: Node.js LTS, güncel Chrome stable, npm
- Yalnız temel görevler için: args'a "--slim", "--headless" ekle
- Telemetriyi kapatmak için args'a "--no-usage-statistics" ve "--no-performance-crux" ekle
- Test: 'Check the performance of https://developers.chrome.com' istemi tarayıcıyı açıp performans izi almalı
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajan yazdığı kodu gerçek tarayıcıda çalıştırıp doğrulayabilir. Konsol hatalarını, ağ isteklerini ve performans darboğazlarını kendisi görür. Ön yüz geliştirmede elle test ve kopyala-yapıştır hata bildirimi ihtiyacını azaltır.
## Maliyet/risk
Tarayıcı içeriğini (çerezler, oturumlar, DevTools verisi) MCP istemcisine açar. README hassas veri paylaşmamayı uyarıyor. Kişisel profille kullanılırsa oturum açık hesaplar ajana görünür; ayrı profil kullanılmalı. Telemetri varsayılan açık. Yalnız Chrome ve Chrome for Testing resmen destekleniyor. `@latest` ile çalıştırmak her seferinde güncel paketi çeker (tedarik zinciri riski; sürüm sabitlenebilir). Yıldız sayısı ve son commit doğrulanamadı.
## Tasarruf
Token aracı değil. Yalnız `--slim` modu daha az araç tanımı yükleyerek bağlam yükünü azaltır; ölçülmüş bir oran yok. Repoda scripts/count_tokens.ts var, yani token maliyeti izleniyor.
## Üretilebilir
hedef_tur: skill
tarif: Kendi MCP'mizi yazmaya gerek yok; resmi MCP kullanılır. Üstüne ince bir 'tarayıcıda doğrula' skill'i yazılabilir. Adımlar: 1) dev sunucuyu başlat, 2) MCP ile sayfayı aç, 3) kritik akışı (tıkla, form doldur) çalıştır, 4) konsol hatalarını ve başarısız ağ isteklerini oku, 5) ekran görüntüsü al, 6) bulguları raporla. Skill, MCP'yi --no-usage-statistics --no-performance-crux --headless bayraklarıyla ve ayrı Chrome profiliyle kullanmayı zorunlu kılar. Repodaki skills/chrome-devtools ve skills/debug-optimize-lcp örnek alınabilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Performans izi kaydı ve içgörü çıkarma (CrUX alan verisiyle)
kaynak: https://github.com/ChromeDevTools/chrome-devtools-mcp
### Ağ istekleri analizi, ekran görüntüsü, source-map'li konsol mesajları
kaynak: https://github.com/ChromeDevTools/chrome-devtools-mcp
### Puppeteer ile otomatik beklemeli güvenilir tarayıcı otomasyonu
kaynak: https://github.com/ChromeDevTools/chrome-devtools-mcp
### --slim modu ve MCP'siz CLI
kaynak: https://github.com/ChromeDevTools/chrome-devtools-mcp
### Hazır skill'ler: a11y, LCP, bellek sızıntısı, çerez hata ayıklama
kaynak: https://github.com/ChromeDevTools/chrome-devtools-mcp/tree/main/skills
## Destek
- jqoFP9QapXI · 8:59 · Tarayıcıyı açıp uygulama işlevselliğini test eder. · kanıt: Hack number 21 is to use Chrome DevTools.
