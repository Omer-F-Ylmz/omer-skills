# claude.ai skill yükleme rehberi · 2026-09-17
Kaynak: support.claude.com/en/articles/12512198 · platform.claude.com/docs/en/agents-and-tools/agent-skills/overview. Zip'ler `dist/` altında (gitignore'da).

## Önkoşul
1. Settings → Capabilities → "Code execution and file creation" açık (custom skill için zorunlu; Pro/Max/Team/Enterprise).
2. Zip yapısı `<ad>.zip → <ad>/SKILL.md`, klasör adı frontmatter `name` ile aynı (5 zip'te kontrol edildi). SKILL.md'nin zip kökünde olması dokümanda "yanlış yapı".

## Yükleme: Customize → Skills (claude.ai/customize/skills) → Add → zip yükle; sıra
1. `frontend-craft.zip` — UI işlerinin disiplin skill'i.
2. `ui-ux-pro-max-claudeai.zip` — tüm data/ + scripts/ (Python) dahil.
3. `impeccable-claudeai.zip` — SKILL.md + reference/ + LICENSE + NOTICE.md (Apache-2.0).
4. `sdp-claudeai.zip`, `surec-claudeai.zip` — Divisima tarifleri için.
frontend-design yüklenmez: anthropics/skills'te var, claude.ai Directory'den eklenir.

## Açıklama sınırı
- claude.ai açıklama sınırı 200 karakter (platform dokümanı 1024 der). Zip'lerde: frontend-craft 195 (kaynakta, 1.5.1) · ui-ux-pro-max 185 · impeccable 192 (bu ikisi yalnız zip kopyasında; kaynak 495/895) · sdp 94 · surec 105.

## claude.ai'de çalışmayacak parçalar
- frontend-craft: `screenshot.mjs`, `audit.mjs`, `olc-renk.mjs` puppeteer ister (sandbox'ta tarayıcı belgelenmemiş, npm ağ ayarına bağlı); `serve.mjs` localhost:3000 açar, sandbox dışından görülmez. 3 genişlik screenshot döngüsü ve audit PASS kabulü yapılamaz.
- impeccable: scripts/ pakette yok → adım 1 `scripts/impeccable context` CLI'ı ve `live` modu çalışmaz; komut tablosundaki reference/ dosyaları okunabilir.
- ui-ux-pro-max: komutlar `~/.claude/skills/ui-ux-pro-max/scripts/search.py` yolunu verir; claude.ai'de skill başka dizinde, yol düzeltilerek çalıştırılır.
- surec: `dotnet build/test/format/run`, `git checkout`, `ci-izle.py` Divisima reposu + yerel araç ister; yalnız süreç metni işe yarar. sdp: `git diff` adımı aynı.
- sdp/surec'teki proje yolu referansları olduğu gibi bırakıldı.
