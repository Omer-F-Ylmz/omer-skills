# Superpowers
ad: Superpowers
tur: skill
video: BiEvvC_66AQ
repo: obra/superpowers
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/obra/superpowers
telemetri: README'de 'Visual companion telemetry' başlıklı bir bölüm var. Okunan kısım kesildiği için içeriği doğrulanamadı: neyin gönderildiği ve kapatma yolu bilinmiyor. Kurmadan önce o bölümü okumak gerekir. Çekirdek skill'lerin telemetri yaptığına dair bir bulgu yok.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı
arastirma: tam (motor hafif claude -p · parti 2026-10-03-short)
## Ne
Kodlama ajanları için, birleştirilebilir skill'ler üzerine kurulu tam bir yazılım geliştirme metodolojisi. Brainstorming, plan yazma, TDD, subagent odaklı geliştirme, kod review, debugging ve doğrulama gibi 15 skill içerir.
## Mekanizma
Oturum başında bir session-start hook'u (hooks/session-start) 'using-superpowers' yönergesini ajana yükler. Skill'ler bu sayede otomatik tetiklenir. Ajan koda atlamaz. Önce kullanıcıya soru sorarak spec çıkarır ve spec'i okunabilir parçalarla onaya sunar. Sonra YAGNI, DRY ve red/green TDD vurgulu bir uygulama planı yazar. Kullanıcı 'go' deyince subagent-driven-development çalışır. Her görev için ayrı bir alt ajan işi yapar, işi inceler ve sonraki göreve geçer. README'ye göre ajan bazen birkaç saat plandan sapmadan özerk çalışır. Aynı repo Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Antigravity, Kimi, Hermes ve diğer ortamlar için plugin manifestleri içerir.
## Kanıt
- Lisans MIT. → doğrulandı · Videoda MIT license sekmesi görünüyor. Repo ağacında LICENSE dosyası var. Lisans metnini kendim okumadım.
- Claude'un doğrudan koda atlamasını engeller, önce plan ve test yapmayı zorlar. → doğrulandı · README 'How it works' bölümü: ajan hemen kod yazmaz, spec çıkarır, plan yazar, red/green TDD vurgular.
- Resmî Claude plugin marketplace üzerinden kurulabilir. → doğrulandı · README: /plugin install superpowers@claude-plugins-official.
- Strateji, yapı ve geliştirmeyi kapsayan tam çerçeve. → doğrulandı · README 'complete software development methodology' diyor. skills/ altında 15 skill var.
- güvenlik ön taraması: koşmadı
## Kurulum
- Claude Code (resmî marketplace): /plugin install superpowers@claude-plugins-official
- Alternatif: /plugin marketplace add obra/superpowers-marketplace, sonra /plugin install superpowers@superpowers-marketplace
- Antigravity: agy plugin install https://github.com/obra/superpowers
- Diğer ortamlar (Codex, Cursor, Gemini CLI, OpenCode vb.) için README'deki ilgili bölüme bakın. Her ortama ayrı kurulur.
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanın doğrudan koda atlamasını önler. Önce spec, plan ve test disiplinini zorlar. Uzun görevlerde plana bağlı kalmayı sağlar. Birçok ajan ortamında çalışır.
## Maliyet/risk
Telemetri bölümü doğrulanmadı. Subagent akışı token ve maliyeti artırabilir. Oturum başı hook'u her oturuma talimat enjekte eder. Kendi skill'lerimizle çakışabilir. Uzun özerk çalışma gözetim gerektirir. Yıldız sayısı ve son commit okunamadı.
## Tasarruf
Token aracı değil. Amaç kalitedir. Önce plan yapmak yeniden işi azaltabilir. Subagent kullanımı ve uzun özerk çalışma ise token tüketimini artırabilir.
## Üretilebilir
hedef_tur: skill
tarif: Doğrudan kurmak yeterli. Kendi sürümümüz gerekirse, MIT lisansı izin verdiği için lisans notunu koruyup şu dört skill'i uyarlayabiliriz: brainstorming (spec çıkarma), writing-plans, test-driven-development ve verification-before-completion. Bunları omer-skills altına SKILL.md olarak koyar, tetikleme açıklamalarını Türkçe yazarız. Oturum başı zorlama gerekirse küçük bir SessionStart hook'u ekleriz. Subagent akışını isteğe bağlı bırakırız, çünkü token maliyeti yüksektir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-10-03-short/panel.md → Ömer sütunu
## Özellikler
### Otomatik tetiklenen skill seti: brainstorming, writing-plans, test-driven-development, subagent-driven-development, systematic-debugging, requesting/receiving-code-review, verification-before-completion, using-git-worktrees, finishing-a-development-branch ve diğerleri
kaynak: https://github.com/obra/superpowers/tree/main/skills
### Oturum başı hook'u ile skill'lerin otomatik devreye girmesi
kaynak: https://github.com/obra/superpowers/tree/main/hooks
### Çoklu ajan ortamı desteği: Claude Code, Codex, Cursor, Gemini CLI, OpenCode, Antigravity, Kimi, Hermes, Pi, Qwen vb.
kaynak: https://github.com/obra/superpowers#installation
### Yeni skill yazmak için writing-skills skill'i
kaynak: https://github.com/obra/superpowers/tree/main/skills/writing-skills
### Superpowers strateji, yapı ve build'i kapsayan tam geliştirme çerçevesidir.
video: BiEvvC_66AQ · iddia: Superpowers strateji, yapı ve build'i kapsayan tam geliştirme çerçevesidir.
sonuc: doğrulandı
arastirma: README ilk cümlesi şöyle diyor: "Superpowers is a complete software development methodology for your coding agents, built on top of a set of composable skills and some initial instructions that make sure your agent uses them." Yani "tam bir geliştirme metodolojisi" ifadesi belgede geçiyor. Bu ifade yalnızca bir pazarlama cümlesi değil, akışta da karşılığı var. Ajan hemen kod yazmaz. Önce kullanıcıya ne yapmak istediğini sorar (strateji/spec). Spec'i okunabilir parçalar halinde onaya sunar. Onaydan sonra YAGNI, DRY ve red/green TDD vurgulu bir uygulama planı yazar (yapı/plan). Kullanıcı "go" deyince subagent-driven-development başlar. Her görev için ayrı ajan çalışır, işi inceler ve devam eder (build). README'ye göre ajan bazen birkaç saat plandan sapmadan çalışır. Repo ağacında skills/ altında 15 skill klasörü var: brainstorming, writing-plans, executing-plans, test-driven-development, subagent-driven-development, systematic-debugging, requesting-code-review, receiving-code-review, verification-before-completion, using-git-worktrees, finishing-a-development-branch, dispatching-parallel-agents, writing-skills, using-superpowers ve diagnosing-superpowers. Bu skill'ler spec'ten plana, uygulamadan review'a ve dala ilişkin bitirme adımına kadar uzanıyor. Skill'ler otomatik tetiklenir. hooks/session-start dosyası var ve Antigravity bölümü session-start hook'unun çalıştığını söylüyor. Repoda Claude Code, Codex, Cursor, Devin, Gemini, Hermes, Kimi, Muse ve Pi için plugin manifestleri var. Lisans: ağaçta LICENSE dosyası var. Metnini ben okumadım, MIT bilgisi aday dosyasından geliyor. Sınırlar: "tam çerçeve" bir kapsam iddiası. Ürünün gerçek kalitesini ya da otonom çalışma süresini ben denemedim. README'nin 279 satırı kesildiği için "Visual companion telemetry" bölümünü okuyamadım. Orada neyin gönderildiği ve nasıl kapatıldığı bilinmiyor. Kurmadan önce o bölüm okunmalı. Yıldız sayısı ve son commit de bilinmiyor.
kaynak: https://github.com/obra/superpowers
### Superpowers, Claude'u koda atlamadan önce plan ve test yapmaya zorlar (spec → plan → red/green TDD).
video: k0gwr-vC2Z4 · iddia: Superpowers, Claude'u koda atlamadan önce plan ve test yapmaya zorlar.
sonuc: doğrulandı
arastirma: README "How it works" bölümü iddiayı destekliyor. Ajan bir şey inşa edildiğini fark edince hemen kod yazmaz. Önce kullanıcıya gerçekte ne yapmak istediğini sorar. Konuşmadan bir spec çıkarır ve okunabilir parçalar halinde onaya sunar. Tasarım onaylanınca bir uygulama planı yazar. Plan gerçek red/green TDD, YAGNI ve DRY vurgular. Kullanıcı "go" deyince subagent-driven-development başlar. Her görevi ayrı bir alt ajan yapar, işi inceler ve sonraki göreve geçer. README, ajanın bazen birkaç saat plandan sapmadan özerk çalıştığını söylüyor. Skill'ler otomatik tetiklenir, kullanıcının özel bir şey yapması gerekmez. Repo ağacında hooks/session-start, hooks/hooks.json ve skills/ altında brainstorming, writing-plans, test-driven-development, verification-before-completion gibi klasörler var. Antigravity bölümü session-start hook'unun Superpowers'ı ilk mesajdan itibaren etkin kıldığını söylüyor. Claude Code'a resmî marketplace'ten kurulur: /plugin install superpowers@claude-plugins-official. Sınırlar: "zorlar" ifadesi README'de yok. Mekanizma hook ile yüklenen talimat ve skill'lerdir, yani ajanın talimata uymasına dayanır, teknik bir engel değildir. Skill dosyalarının içeriğini ve hook betiğini ben okumadım. README'nin 279 satırı kesildi. Telemetri bölümü ("Visual companion telemetry") okunamadı, içeriği bilinmiyor. Yıldız sayısı ve son commit bilinmiyor.
kaynak: https://github.com/obra/superpowers#how-it-works
## Destek
- BiEvvC_66AQ · 0:30 · Strateji, yapı ve geliştirmeyi kapsayan tam yazılım geliştirme çerçevesi. · kanıt: Kare Superpowers README'sini gösteriyor. (karede: GitHub README: seçili 'Superpowers' başlığı, 'Quickstart', 'Give your agent Superpowers: Claude Code, Gemini CLI, OpenCode, Cursor'; MIT license sekmesi.) · iddia: Superpowers strateji, yapı ve build'i kapsayan tam geliştirme çerçevesidir.
- k0gwr-vC2Z4 · 0:09 · Claude'un doğrudan koda atlamasını engeller; önce plan yapmayı ve test etmeyi zorlar. · kanıt: Kare: Claude Code için Superpowers kurulum sayfası; altyazıda plan ve test önceliği anlatılıyor. (karede: Koyu arka planda 'Claude Code' kutusu: Superpowers resmî Claude plugin marketplace üzerinden mevcut; altında /plugin install komutu.) · iddia: Superpowers, Claude'u koda atlamadan önce plan ve test yapmaya zorlar.

## Güncellik (2026-10-04)
- kurulu 5bf4e78 ↔ upstream 8ca22db · son commit 2026-09-25
- yeni skill/komut/ajan: yok
