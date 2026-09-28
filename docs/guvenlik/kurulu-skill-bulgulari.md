# Kurulu skill güvenlik bulguları — Parti D (28 Eyl 2026)

kaynak: SkillSpector `--no-llm` JSON (`C:\Projeler\.video-cache\skillspector\<o__r>.json`, 28 Eyl 17:34-17:35); yalnız HIGH/CRITICAL satırları.
karar: Desktop + Ömer. Bu belge kaldırma / devre dışı bırakma önermez; kurulu dosyalara dokunulmadı.
alanlar: araç · önem · kural · dosya:satır · kısa açıklama · ilk değerlendirme.

## taste-skill (Leonxlnx/taste-skill) — HIGH 4 · MEDIUM 33
- HIGH · P6 System Prompt Leakage (c0.85) · skills/imagegen-frontend-web/SKILL.md:3, :6, :399 · eşleşen metin "OUTPUT RULE" (frontmatter/çıktı kuralı başlığı).
  ilk değerlendirme: **olası yanlış alarm** — skill kendi çıktı biçimini tanımlıyor, sistem promptu sızdırma yok.
- HIGH · P2 Prompt Injection (c0.7) · skills/taste-skill/SKILL.md:272 · placeholder görsel için `picsum.photos` URL'si + yanıt sonunda "This page needs real images at…" deme talimatı.
  ilk değerlendirme: **olası yanlış alarm** — kullanıcıya yönelik çıktı talimatı; dış ağ yalnız placeholder görsel URL'si (düşük risk, not edilir).

## scroll-craft (nateherkai/scroll-craft) — HIGH 14 · MEDIUM 5
- HIGH · PE3 Privilege Escalation (c0.6) · .env.example:1 · .gitignore:2, :3 · scripts/doctor.mjs:129, :139 · scripts/kie.mjs:20, :39, :50 · `.env` / `.env.local` anılması ("Never commit .env").
  ilk değerlendirme: **olası yanlış alarm** — kie.ai API anahtarı yerel .env'den okunuyor, .gitignore'da; yetki yükseltme değil. **Gerçek dikkat noktası:** skill görsel üretimi için ücretli dış API (kie.ai) çağırıyor — kullanımda tavan gerekir.
- HIGH · AR2 Anti-Refusal (c0.85) · references/approved-collection.md:88 · "Do not judge an alpha image solely by a previewer's … color".
  ilk değerlendirme: **olası yanlış alarm** — görsel değerlendirme yönergesi, reddetmeyi bastırma değil.
- HIGH · AR1 Anti-Refusal (c0.85) · references/assets.md:111 · "do not refuse" eşleşmesi; bağlam per-call bütçe tavanı planlaması.
  ilk değerlendirme: **olası yanlış alarm** — bütçe/tavan metni; bağlam dar okundu, Desktop teyidi önerilir.
- HIGH · P2 Prompt Injection (c0.7) · references/device-diag.html:2 · references/template.html:2, :50, :65 · HTML yorum bloğu (şablon/teşhis açıklaması).
  ilk değerlendirme: **olası yanlış alarm** — geliştiriciye yönelik HTML yorumları; :50/:65 satırlarının metni bu turda okunmadı.

## design-dna (zanwei/design-dna) — HIGH 2 · MEDIUM 45 · LOW 2
- HIGH · AE1 (c?) · SKILL.md:55, :95 · ayrıntı metni bu turda okunmadı (tur tavanı).
  ilk değerlendirme: **belirsiz** — Desktop incelemesinde SKILL.md:55 ve :95 okunmalı; karar verilmedi.

## Özet
- gerçek risk: yok kesinleşmedi; scroll-craft'ın ücretli kie.ai çağrısı maliyet riski (güvenlik değil).
- olası yanlış alarm: taste-skill 4/4 · scroll-craft 14/14 (2 satır teyitle).
- açık: design-dna AE1 ×2.
