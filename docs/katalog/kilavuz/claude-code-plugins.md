# claude-code-plugins — 13 benzersiz kayıt

**Amaç:** Anthropic'in resmi Claude Code eklentileri: commit/PR komutları, çok ajanlı kod/PR incelemesi, özellik geliştirme akışı, hook üretimi, güvenlik rehberi, çıktı stilleri, model göçü.

**İç yapı:** Çoğu [plugin]; iki eklentinin alt skill'i var (claude-opus-4-5-migration, hookify:Writing Hookify Rules).

## En güçlü parçalar
- `code-review` — Güven puanlı çok uzman ajanlı otomatik PR incelemesi.
- `pr-review-toolkit` — Yorum, test, hata işleme, tip tasarımı, sadeleştirme odaklı PR ajanları.
- `feature-dev` — Keşif, mimari tasarım ve kalite ajanlarıyla uçtan uca özellik akışı.
- `hookify` — Konuşma kalıplarını analiz edip istenmeyen davranışı engelleyen hook üretir.
- `security-guidance` — Düzenlemede kalıp uyarısı, Stop'ta LLM diff incelemesi.
- `commit-commands` — Commit, push ve PR açmayı basit komutlara indirir.

## Birlikte kullanım
- feature-dev → code-review / pr-review-toolkit → commit-commands.
- hookify + hookify:Writing Hookify Rules: kural sözdizimi ve üretim.
- security-guidance + sec ailesi ajanları.

## Tuzaklar
- code-review ile pr-review-toolkit kapsamı çakışır.
- claude-opus-4-5-migration yalnız Sonnet 4.x/Opus 4.1'den Opus 4.5'e göç içindir; güncel model için değil.
- ralph-wiggum sürekli öz-referanslı döngü çalıştırır; durma koşulu katalog metninde belirtilmemiş.

## Üyeler
- plugin (11): agent-sdk-dev, claude-opus-4-5-migration, code-review, commit-commands, explanatory-output-style, feature-dev, hookify, learning-output-style, pr-review-toolkit, ralph-wiggum, security-guidance
- skill (2): claude-opus-4-5-migration:claude-opus-4-5-migration, hookify:Writing Hookify Rules
