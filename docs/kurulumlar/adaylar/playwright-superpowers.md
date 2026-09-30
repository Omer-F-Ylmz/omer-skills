# Playwright + Superpowers
ad: Playwright + Superpowers
tur: plugin
video: cAeQjck1jHs
repo: obra/superpowers
lisans: MIT (Superpowers; LICENSE dosyası ağaçta var ama metni getirilemedi, MIT bilgisi doğrulanmadı) · Playwright MCP: Apache-2.0 (doğrulanmadı)
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/obra/superpowers
telemetri: Superpowers README'sinde "Visual companion telemetry" başlıklı bir bölüm var. İçeriği getirilemedi, ayrıntı bilinmiyor; kurmadan önce o bölüm okunmalı. Playwright MCP telemetrisi doğrulanmadı.
yildiz: bilinmiyor
alt_tur: araç
skillspector: bilinmiyor
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun-7)
## Ne
İki ayrı aracın birlikte kullanımı. Superpowers, kodlama ajanına yerleşik bir yazılım geliştirme yöntemi (beceri seti) kazandırır. Playwright, tarayıcıyı otomatikleştirir; ajan yerel uygulamayı gerçek kullanıcı gibi gezip test eder ve ekran görüntüsü alır.
## Mekanizma
Superpowers: birleştirilebilir skill'ler ve oturum başlangıcında çalışan talimat/hook ile ajan koda atlamaz. Önce ne yapmak istediğini sorar ve spec'i okunabilir parçalar halinde gösterir. Onaydan sonra red/green TDD, YAGNI ve DRY vurgulu bir uygulama planı çıkarır. "Go" denince subagent-driven-development ile her görevi alt ajanlara yaptırır, işi inceler ve ilerler. Skill'ler otomatik tetiklenir. Playwright: MCP sunucusu (@playwright/mcp) sayfayı piksel yerine erişilebilirlik ağacı (accessibility snapshot) üzerinden sürer. Tıklama, yazma ve gezinme araçları sunar. Microsoft ayrıca token açısından daha hafif olan playwright-cli + SKILLS seçeneğini öneriyor. Videoda ikisi de Code uygulamasındaki plugin marketplace'ten kuruluyor; Playwright'ın makinede kurulu olması gerekiyor.
## Kanıt
- Superpowers önce plan, test ve kendi kendini inceleme zorlar. → doğrulandı · README: önce spec çıkarır, sonra TDD vurgulu plan yapar, ardından subagent-driven-development ile işi inceleyerek ilerler.
- Playwright yerel uygulamayı gerçek kullanıcı gibi test eder, ekran görüntüsü alır. → sınanamadı · Playwright MCP README'si tarayıcı otomasyonunu doğruluyor ama erişilebilirlik ağacını öne çıkarıyor. Ekran görüntüsü özelliği getirilen kısımda görünmedi.
- İkisi de plugin marketplace'ten kuruluyor. → doğrulandı · Superpowers için /plugin install superpowers@claude-plugins-official komutu README'de var. Playwright için README'de claude mcp add komutu var. Playwright'ın marketplace yolu doğrulanmadı.
- Video içeriği (8:12, cAeQjck1jHs). → sınanamadı · Video sayfası yalnızca başlık verdi: '9 Claude Skills I Use Every Single Day'. Transkript alınamadı.
- güvenlik ön taraması: koşmadı (repo yok)
## Kurulum
- Superpowers (Claude Code): /plugin install superpowers@claude-plugins-official
- Alternatif marketplace: /plugin marketplace add obra/superpowers-marketplace, sonra /plugin install superpowers@superpowers-marketplace
- Playwright MCP: claude mcp add playwright npx @playwright/mcp@latest (Node.js 18+ gerekir)
- Videoya göre Playwright plugin'i marketplace'ten de kurulabilir; tarayıcı/Playwright makinede kurulu olmalı
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajan plansız koda girmez. Testi ve kendi incelemesini yapar, uygulamayı gerçek tarayıcıda doğrular. Bu da UI hatalarını ve "çalışıyor sanılan" kodu azaltır.
## Maliyet/risk
Playwright ajana gerçek tarayıcı kontrolü verir, bu yüzden güvenilmeyen sayfalarda prompt injection riski taşır. Superpowers ajanı saatlerce özerk çalıştırabilir, bu da maliyeti ve kontrolü etkiler. Sürümler ve telemetri doğrulanmadı. Repo URL'si adayda verilmemişti; obra/superpowers olarak varsaydım.
## Tasarruf
Token aracı değil. Tek dolaylı etki: Playwright MCP'nin erişilebilirlik ağacı verbose olabilir. Microsoft README'sine göre CLI+SKILLS yolu MCP'den daha az token harcar. Superpowers planı uzun ve alt ajanlı çalışır, bu da token tüketimini artırabilir.
## Üretilebilir
hedef_tur: skill
tarif: Superpowers'ın çekirdeği bir skill seti: (1) brainstorm/spec skill'i önce hedefi sorar ve spec'i parçalar halinde onaylatır, (2) plan skill'i görevleri TDD adımlarıyla listeler, (3) subagent-driven skill'i her görevi alt ajana verip inceler. Bunları bir SessionStart hook'u tetikler. UI doğrulaması için Playwright MCP'yi (npx @playwright/mcp@latest) ya da playwright-cli'yi çağıran ayrı bir 'ui-doğrula' skill'i yazılır. Hazır plugin zaten kurulabildiği için kendi sürümümüz yalnızca özelleştirme gerekirse anlamlı.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun-7/panel.md → Ömer sütunu
## Özellikler
### Otomatik tetiklenen skill'lerle spec, plan, TDD ve alt ajan tabanlı uygulama iş akışı
kaynak: https://github.com/obra/superpowers
### Erişilebilirlik ağacıyla tarayıcı otomasyonu yapan MCP sunucusu; token açısından hafif CLI+SKILLS alternatifi de var
kaynak: https://github.com/microsoft/playwright-mcp
### Çoklu ajan desteği: Claude Code, Codex, Cursor, Gemini CLI, OpenCode ve diğerleri
kaynak: https://github.com/obra/superpowers
## Destek
- cAeQjck1jHs · 8:12 · Playwright yerel uygulamayı gerçek kullanıcı gibi test eder, ekran görüntüsü alır; Superpowers önce plan, test ve kendi kendini inceleme zorlar. · kanıt: İkisi de Code uygulamasındaki plugin marketplace'ten kuruluyor; Playwright makinede kurulu olmalı.
