# Garden skills (web design engineer)
ad: Garden skills (web design engineer)
tur: skill
video: Ysr7oNDajJI
repo: conardli/garden-skills
lisans: MIT
son_commit: bilinmiyor
arsiv: bilinmiyor
kaynak: https://github.com/conardli/garden-skills
telemetri: Okunan README'de telemetri ifadesi yok. Skill'ler yalnızca Markdown ve şablon içerdiği için telemetri beklenmez. Kod tabanını taramadım, bu yüzden kesin değil. web-video-presentation'ın isteğe bağlı TTS sağlayıcıları (MiniMax, OpenAI) ayrı bir konudur: kullanıcı seçerse ses metni o sağlayıcıya gider.
yildiz: bilinmiyor
alt_tur: araç
skillspector: koşmadı: SkillSpector raporu yok
arastirma: tam (motor hafif claude -p · parti 2026-09-30-uzun)
## Ne
Claude Code, Cursor, Codex gibi ajanlar için hazırlanmış bir Agent Skills koleksiyonu. README'de 5 skill sayılıyor: web-video-presentation, web-design-engineer, gpt-image-2, beautiful-article ve kb-retriever. Ağaçta kb-retriever klasörü de görünüyor, ama README'nin okunan kısmında anlatılmıyor. Aday olan web-design-engineer, ajanı "tasarım mühendisi" gibi çalıştırır. Önce ürün bağlamını anlar, sonra tasarım sistemini beyan eder, erken bir v0 gösterir, tam deneyimi kurar ve sonucu doğrular.
## Mekanizma
Saf istem/talimat tabanlı bir SKILL.md paketidir. Ağır iş modelin kendisinde yapılır, ayrı bir sunucu ya da çalışan servis yoktur. Akış şöyle: (1) Brief, beş kadranlı bir "Design Read"e çevrilir: varyans, hareket, yoğunluk, varlık bağımlılığı ve marka sadakati. (2) Mevcut ürün için extension, preserve ve overhaul modlarından biri seçilir. (3) Design Direction Advisor altı farklı okul sunar. Bunlara ek olarak 25 sabitlenmiş stil tarifi vardır (Linear, Aesop, Pentagram, Bloomberg, Stripe Press, Mid-Century vb.). Her tarifte palet, tipografi, imza hareketler ve anti-pattern'ler bulunur. (4) "Anti-cliché" kara listesi jenerik yapay zekâ arayüzlerini engeller. (5) Uygulama kuralları: inline React + Babel, CSS token'ları, oklch() renkleri, container query'ler, reduced-motion. Cihaz çerçeveleri, slayt motorları ve animasyon zaman çizelgeleri için ileri düzey bir kalıp referansı da var. (6) Tarayıcı kabul testi yalnızca kullanıcı açıkça isterse çalışır. Videodaki "gerçek tasarım referansı arama" ve "puanlama" adımlarını README'nin okunan kısmında doğrulayamadım. SKILL.md'yi okumadım.
## Kanıt
- Repo 5 skill içeriyor → doğrulandı · README rozeti 'skills-5'. Ağaçta beautiful-article, gpt-image-2, kb-retriever, web-design-engineer ve web-video-presentation klasörleri var.
- Lisans MIT → doğrulandı · README'deki lisans rozeti MIT. Ağaçta LICENSE dosyası var. Dosya içeriğini okumadım.
- Video: web design engineer gereksinimleri netleştirir → doğrulandı · README: 'first understanding product context' ve beş kadranlı Design Read.
- Video: gerçek tasarım referansları arar → sınanamadı · README'de web araması yapıldığına dair ifade yok. 25 hazır stil tarifi ve Design Direction Advisor var. Gerçek zamanlı arama SKILL.md'de olabilir, okumadım.
- Video: tasarımı puanlar → sınanamadı · README'nin okunan kısmında puanlama yok. Yalnızca kullanıcı isterse çalışan tarayıcı kabul testi ve son doğrulama adımı anılıyor.
- güvenlik ön taraması: koşmadı: SkillSpector raporu yok
## Kurulum
- npx ile skills CLI (Seçenek A): README'deki komutu kullanın. Tam komut satırı kesilen kısımda kaldı, bu yüzden yazmıyorum.
- Claude Code plugin marketplace (Seçenek B): repoda .claude-plugin/marketplace.json var.
- Releases sayfasından sabit sürüm .zip indirme (Seçenek C).
- skills/web-design-engineer klasörünü projeye elle kopyalama (Seçenek D).
- Git submodule olarak ekleme (Seçenek E).
## Bizde durum
kurulu değil (envanter eşleşmesi yok)
## Beklenen fayda
Ajanın jenerik "yapay zekâ arayüzü" çıktısı yerine bilinçli ve tutarlı tasarım üretmesini sağlar. Brief'i netleştirir, somut stil tarifleri verir ve kalıp referansları sunar. Landing page, dashboard ve HTML slayt işlerinde işe yarar.
## Maliyet/risk
Düşük. MIT lisanslı ve içerik ağırlıklı olarak talimat metnidir. Riskler: (1) Güvenlik ön taraması çalışmadı, SkillSpector raporu yok. (2) Skill'ler ajana talimat verdiği için SKILL.md ve referanslar kuruma alınmadan önce incelenmelidir. (3) Stil tarifleri Linear, Stripe Press gibi markalara atıf yapıyor, marka taklidi hassasiyeti olabilir. (4) Yıldız sayısı ve son commit doğrulanamadı. (5) Kapsam geniş, yalnızca web-design-engineer alınırsa diğer skill'ler gerekmez.
## Tasarruf
Token tasarrufu aracı değil. Kalıp ve tarifler gerektiğinde yüklenir. Tek seferde daha nitelikli çıktı üretip yeniden yapma turlarını azaltabilir, ama bunu ölçmedim.
## Üretilebilir
hedef_tur: skill
tarif: Kendi 'design-engineer' skill'imizi yazın. (1) SKILL.md: Design Read adımı olarak brief'i beş kadrana (varyans, hareket, yoğunluk, varlık, marka) çevirsin. Ardından tasarım sistemi beyanı, erken v0, tam yapım ve doğrulama sırası gelsin. (2) references/style-recipes/ altında her stil için palet, tipografi, imza hareketler ve anti-pattern içeren kısa bir dosya olsun. Yalnızca seçilen tarif yüklensin. (3) anti-cliché kara listesi ayrı bir dosyada tutulsun. (4) İsteğe bağlı kabul adımı için mevcut tarayıcı/Playwright aracımızı çağırsın. Kod kopyalamak yerine yapıyı örnek alıp içeriği kendimiz yazalım. MIT lisansı atıf gerektirir. Önce SKILL.md ve references dosyalarını okuyup tarifi netleştirmek gerekir.
## Karar
SOR (karar paneli)
## Sonraki adım
docs/kurulumlar/parti/2026-09-30-uzun/panel.md → Ömer sütunu
## Özellikler
### Beş kadranlı Design Read (varyans, hareket, yoğunluk, varlık bağımlılığı, marka sadakati)
kaynak: https://github.com/conardli/garden-skills
### Extension / preserve / overhaul yeniden tasarım modları
kaynak: https://github.com/conardli/garden-skills
### Design Direction Advisor (6 okul) + 25 sabitlenmiş stil tarifi
kaynak: https://github.com/conardli/garden-skills
### Anti-cliché kara listesi
kaynak: https://github.com/conardli/garden-skills
### Yalnızca istenirse çalışan tarayıcı kabul testi
kaynak: https://github.com/conardli/garden-skills
### İleri düzey kalıp referansı: cihaz çerçeveleri, slayt motoru, animasyon zaman çizelgesi, dashboard
kaynak: https://github.com/conardli/garden-skills
### Kurulum: npx skills CLI, Claude Code marketplace, zip, elle kopyalama, submodule
kaynak: https://github.com/conardli/garden-skills
## Destek
- Ysr7oNDajJI · 3:49 · 5 skill'lik set; web design engineer gereksinimleri netleştirir, gerçek tasarım referansları arar, tasarımı puanlar. · kanıt: good design never starts from thin air
