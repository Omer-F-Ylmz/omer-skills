# yerel-diger — 357 benzersiz kayıt

**Amaç:** Başka aileye oturmayan yerel skill'lerin toplama kümesi: tarayıcı sürme, görsel/logo üretimi, tasarım-sistemi şablonları, Strix güvenlik testi, video izleme, -paket derlemeleri.

**İç yapı:** Düz liste; alt gruplar: '-paket' derlemeleri (adobe, android, azure, animasyon-scroll), 'Create a ... design system' görsel şablonları, gstack etiketli (benchmark, canary, careful), Strix güvenlik skill'leri.

## En güçlü parçalar
- `agent-browser:agent-browser` — Site gezme, form doldurma, tıklama, ekran görüntüsü gereken web etkileşimlerinde ilk seçenek.
- `differential-review:differential-review` — PR/commit/diff'i güvenlik açığı ve önceki açığın geri gelmesi açısından incelerken.
- `watch:watch` — URL ya da yerel videoyu yt-dlp ile indirip ffmpeg kareleri ve transkriptle izletir.
- `last30days:last30days` — Bir konuda son 30 günde Reddit, X, YouTube'da insanların ne dediğini etkileşimle toplar.
- `logo-design:logo-design` — Brief'ten konsepte, üretim dosyalarına kadar logo/marka işareti tasarımı.
- `brainstorming` — Özellik, bileşen ya da işlev eklemeden önce zorunlu yaratıcı ön aşama olarak tanımlı.
- `check` — Merge öncesi /check verify ile gerçek uygulamayı sürüp her kabul ölçütünü kanıtlar.
- `application-security-testing` — Strix ile ürün genelinde hangi varlığa hangi testin gerektiğine karar verir.
- `claude-settings-audit` — Yeni projede ayarları denetler, izin verilecek salt-okur bash komutlarını belirler.
- `archify` — Sistem mimarisi, altyapı, bulut/ağ topolojisi görselleştirme istendiğinde.

## Birlikte kullanım
- agent-browser:agent-browser + browser-video-recording: tarayıcı akışını sürüp imleç/zoom'lu kayıt üretmek.
- api-security-testing ve ci-security-scanning-with-strix: Strix'i önce elle API'de, sonra CI'da diff kapsamlı koşturmak.
- brainstorming → architect → check: fikir, yaklaşım seçimi, merge öncesi doğrulama sırası.
- tastemaker ile 'Create a ... design system' şablonları (blue-cloudy-clean-modern vb.) birlikte UI üretiminde.

## Tuzaklar
- Çakışan kopyalar: banana-claude:banana ile banana, agent-browser:agent-browser ile agent-browser-paket, browse/built-in-browser/chrome-browser.
- claude-mem-cowork:mem-setup cmem anahtarı ister; banana Google Gemini görüntü modellerine bağlı.
- chinese-novelist yalnız Çince roman yazar, Türkçe metin değil; beautiful-article açıklaması Çince.
- Küme 357 üyeli ve tematik değil; doğru skill'i ad yerine katalog metniyle aramak gerekir.

## Üyeler
- skill (357): 0day-scanner, 9router-paket, VibeSec-Skill, adobe-paket, agency-grid-layout-minimal, agent-browser-paket, agent-browser:agent-browser, agent-reach, agents-md, agents-sdk, agentshield-paket, ai-etkilesim-tasarim-paket, ai-labs-paket, ambient-section-particles, anatomy, android-paket, animasyon-scroll-paket, animate, animate-expo, api-security-testing, app-store-screenshots, apple-design, application-security-testing, arayuz-iyilestirme-paket, archify, archify-review, architect, article-prompts-to-skills, ask-sonner, atmosphere-background, aura-asset-images, author-game-levels, autoclip-paket, autoplan, azure-altyapi-paket, azure-uygulama-ai-paket, backend-patterns, background-grid-webgl, banana, banana-claude:banana …
