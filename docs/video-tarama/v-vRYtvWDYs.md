# Claude Code Token İsrafına Son Verdim
kanal: Muzaffer Kadir (mkdir dev) · süre: 7 dk · altyazı: otomatik tr
ana iddia: settings.json'a 3 satır eklemek (thinking token tavanı), doğru model seçmek ve context-mode MCP/plugin kurmak Claude Code maliyetini "dramatik" düşürür; kanalın kendi ölçümünde token kullanımı ~%88 azalmış (iddia, tek kullanıcı anekdotu).
## kalemler
| ad | durum | etiket | not |
|---|---|---|---|
| mksglu/context-mode | YENİ | ELE | MCP+hook ile tool çıktısını sandbox'lıyor, "%98 azaltma" iddiası (repo açıklaması); kurulu RTK (token-azaltıcı proxy/hook) ile aynı kategori — çift |
| affaan-m/everything-claude-code | YENİ | ELE | açıklamada ikinci link olarak geçiyor, videoda kullanılmıyor; skill/hafıza/güvenlik paketi, npx ile kurulan GitHub App + npm paketleri |
| settings.json max thinking tokens ayarı | YENİ | BEKLE | "settings Jason dosyasına 3 satır" (sözlü); Claude Code'un resmi/dokümante bir alanı mı doğrulanmadı; kazanç %88 tek kullanıcı iddiası |
| doğru model seçimi (Bölüm 2, basit iş için ucuz model) | ZATEN VAR | BEKLE | genel tavsiye, kurulu sette CLAUDE.md/skill kademesi (sonnet/haiku) mantığıyla örtüşüyor |
## ölçütler (ELE)
- mksglu/context-mode: bakım=aktif (pushed 2026-09-16, 23211 yıldız, archived=false) ancak lisans NOASSERTION (belirsiz, MIT/Apache değil) · çift=RTK ile aynı niş (token azaltımı) · izin=MCP + hook, `npx -y context-mode` veya `npm install -g`; Node≥22.5 gerekiyor · context=11 MCP tool açıklaması her oturuma eklenir · kurulum: `/plugin install context-mode@context-mode` veya `claude mcp add context-mode -- npx -y context-mode`
- affaan-m/everything-claude-code: bakım=pushed 2026-09-15 ama 260051 yıldız şüpheli derecede yüksek (küçük/niş bir araç için olağandışı) · çift=kapsamı superpowers/frontend-craft ile örtüşebilir (skill+hafıza+güvenlik) · izin=GitHub App kurulumu + npx paketi; kısmi ücretli (özel repo $19/ay) · context=plugin kurulunca skill/hook sayısı README'de netleşmiyor · kurulum: `npx ecc-universal@2.2.1 setup`
- settings.json ayarı: bakım=— (yerel dosya, teknik) · çift=yok · izin=yok, dosya düzenleme · context=0 · kurulum: —
## hedefler (BİLGİ)
- yok
