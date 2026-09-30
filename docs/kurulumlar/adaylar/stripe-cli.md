# Stripe CLI
ad: Stripe CLI
tur: CLI
video: V2RIVnGCy74
repo: stripe/stripe-cli
lisans: Apache-2.0
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/stripe/stripe-cli
telemetri: Var, varsayılan olarak açık (Stripe'ın wiki telemetri sayfası ve arama sonucuna göre). Toplanan verinin ayrıntısı incelenmedi. Kapatmak için STRIPE_CLI_TELEMETRY_OPTOUT=1 (veya true) ortam değişkeni kullanılır. Ayrıca ikili dosyada otomatik güncelleme denetimi için pkg/autoupdate paketi bulunuyor.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-5)
## Ne
Stripe entegrasyonunu terminalden geliştirmek, test etmek ve yönetmek için Stripe'ın resmî komut satırı aracı (Go ile yazılmış). Webhook'ları yerelde dinleme, olay tetirleme/yeniden gönderme, API istek günlüklerini canlı izleme ve API nesnelerini oluşturma/okuma/güncelleme/silme işlemlerini yapar.
## Mekanizma
Go ile yazılmış tek ikili dosya. `stripe login` ile hesaba bağlanır; anahtarlar yerel keyring'de (canlı mod için password store) tutulur. `stripe listen` Stripe'a websocket ile bağlanıp webhook olaylarını yerel URL'ye iletir. `stripe trigger` fixture'larla test olayları üretir. `stripe logs tail` istek günlüklerini akıtır. Kaynakta api/openapi-spec vardır; API kaynak komutları (ör. `stripe customers create`) OpenAPI şemasından üretilmiş görünüyor. Depoda pkg/agentsetup ve pkg/agentskills dizinleri ile CLAUDE.md var; bunlar yapay zekâ ajanı entegrasyonuna işaret edebilir ama içerikleri incelenmedi. Videodaki "doğal dil" iddiası buradan çıkarıldı, doğrulanmadı.
## Kanıt
- Stripe CLI, Stripe ile uğraşmayı çok daha kolay hale getiriyor (videoda). → sınanamadı · Bu öznel bir değerlendirme. README yalnızca webhook testi, olay tetikleme, log izleme ve API nesnesi işlemlerini sayıyor. Aracı çalıştırıp denemedim.
- Stripe'ı doğal dille yönetmeyi kolaylaştırır (video özeti). → sınanamadı · README'de doğal dil özelliği yok. Depoda pkg/agentsetup ve pkg/agentskills dizinleri ile CLAUDE.md dosyası var, ama içeriklerine bakmadım.
- Terminalden webhook test etme, olay tetikleme, log izleme ve CRUD yapılabilir. → doğrulandı · README'nin 'With the CLI, you can' listesi bunu doğrudan söylüyor.
- Açık kaynak ve Apache-2.0 lisanslı. → doğrulandı · Web arama sonucu Apache-2.0 diyor. Depoda LICENSE dosyası var ama içeriğini okumadım.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- npm install -g @stripe/cli (Node.js >= 18) veya npx @stripe/cli login
- macOS: brew install stripe
- Windows: winget install Stripe.StripeCLI veya scoop bucket add stripe https://github.com/stripe/scoop-stripe-cli.git && scoop install stripe
- Linux: apt veya yum/dnf deposu (README'deki packages.stripe.dev komutları)
- Docker: docker run --rm -it stripe/stripe-cli version
- Ardından: stripe login
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ödeme alan uygulamalarda webhook'ları üçüncü parti tünel aracı olmadan yerelde test etmeyi, olay tetiklemeyi ve API çağrılarını komut satırından yapmayı sağlar. Bu sayede Stripe entegrasyonu geliştirmek ve ayıklamak hızlanır. Bir ajan bunu kabuk üzerinden doğrudan kullanabilir.
## Maliyet/risk
Canlı mod anahtarı (secret key) gerektirebilir; ajana verilirse gerçek para/müşteri verisi üzerinde yıkıcı işlemler (silme, iade) yapılabilir. Test modunda kalınmalı, `--live` ve `--api-key` kullanımı bilinçli olmalı. Telemetri varsayılan açık. README'deki yum deposu örneğinde gpgcheck=0 var (imza doğrulaması kapalı), bu yüzden apt yolu veya npm tercih edilmeli. SkillSpector taraması yapılmadı.
## Tasarruf
Token aracı değil; geçerli değil.
## Üretilebilir
hedef_tur: skill
tarif: Stripe CLI'yi yeniden yazmaya gerek yok. Onu saran bir skill yazılabilir. SKILL.md içinde şunlar olur: (1) her zaman test modu ve `stripe listen --forward-to localhost:PORT` ile başla, (2) `stripe trigger <olay>` ile olay üret, (3) `stripe logs tail` ile ayıkla, (4) `--live`/silme/iade komutlarını kullanıcı onayına bağla, (5) STRIPE_CLI_TELEMETRY_OPTOUT=1 ayarla. Anahtarları dosyaya yazdırmayan bir kontrol listesi de ekle. İstenirse canlı mod komutlarını engelleyen bir PreToolUse hook'u da eklenebilir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-5/panel.md → Ömer sütunu
## Özellikler
### Webhook'ları üçüncü parti yazılım olmadan güvenle test etme (stripe listen ile yerele iletme)
kaynak: https://github.com/stripe/stripe-cli
### Webhook olaylarını tetikleme veya yeniden gönderme
kaynak: https://github.com/stripe/stripe-cli
### API istek günlüklerini gerçek zamanlı izleme
kaynak: https://github.com/stripe/stripe-cli
### API nesnelerini oluşturma, okuma, güncelleme, silme
kaynak: https://github.com/stripe/stripe-cli
### npm, Homebrew, apt, yum, WinGet, Scoop ve Docker ile kurulum
kaynak: https://github.com/stripe/stripe-cli
### Telemetriyi STRIPE_CLI_TELEMETRY_OPTOUT ile kapatma
kaynak: https://github.com/stripe/stripe-cli/wiki/telemetry
## Destek
- V2RIVnGCy74 · 16:12 · Ödeme alan uygulamalarda Stripe'ı terminal ve doğal dille yönetmeyi kolaylaştırır. · kanıt: Stripe CLI, Stripe ile uğraşmayı çok daha kolay hale getiriyor. (karede: İlgili kare yok; altyazıdan.)
