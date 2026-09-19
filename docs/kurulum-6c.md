# KURULUM-6c · skill zip onarımı + yükleme paketi · 19 Eyl 2026

Girdi: 19 Eyl'deki claude.ai skill kontrolü (107 zip). 7 zip yüklenemedi, 13 skill'de kırık referans vardı. Yalnız bunlar değişti; diğer zip'lerin SHA256 değeri öncekiyle aynı (`C:\Projeler\.tmp-kurulum6\sha256-once.tsv`). Eski sürümler `C:\Projeler\.tmp-kurulum6\eski-6c\` altında. Denetim: `python tools/skill_denetim.py dist` → docs/kurulum-6c-denetim.md (0 hata).

## dist/yukle-6c/replace/ (13, claude.ai'de Replace)
- agent-skills-code-review-and-quality.zip · references/security-checklist.md + performance-checklist.md eklendi, `../../references/` → `references/`
- agent-skills-frontend-ui-engineering.zip · references/accessibility-checklist.md eklendi
- agent-skills-incremental-implementation.zip · references/definition-of-done.md eklendi
- agent-skills-observability-and-instrumentation.zip · references/observability-checklist.md eklendi
- agent-skills-performance-optimization.zip · references/performance-checklist.md eklendi (2 bağlantı)
- agent-skills-planning-and-task-breakdown.zip · references/definition-of-done.md eklendi
- agent-skills-test-driven-development.zip · references/testing-patterns.md eklendi
- agent-skills-using-agent-skills.zip · references/definition-of-done.md eklendi
- claude-design-skills-design-system.zip · `~/.claude/skills/ui-designer/references/ai-slop-detector.md` → `references/ai-slop-detector.md`; dosya ui-designer'dan kopyalandı
- ui-ux-pro-max-claudeai.zip · 17 yerde `~/.claude/skills/ui-ux-pro-max/scripts/search.py` → `scripts/search.py`
- design-mastery-claude-code-brand-systems.zip · 4 ölü bağlantı çıkarıldı
- design-mastery-claude-code-design-masters.zip · 5 ölü bağlantı çıkarıldı (saul-bass.md zip'te var, kaldı)
- design-mastery-claude-code-design-movements.zip · 5 ölü bağlantı çıkarıldı, boşalan "## Resources" başlığı silindi

## dist/yukle-6c/yeni/ (1)
- superpowers-superpowers-tdd.zip · klasör + name `superpowers-tdd` (addyosmani `test-driven-development` ile ad çakışması); description "superpowers (obra/superpowers) TDD: …" 147 karakter. Eski `superpowers-test-driven-development.zip` dist'ten eski-6c'ye taşındı.

## Kopyalanan referans dosyaları (10), SkillSpector --no-llm
- Kaynak addyosmani__agent-skills/references/ (6 dosya, 9 kopya) ve Gustavosilveira23 skills/ui-designer/references/ai-slop-detector.md. Kopyalanan dosyalarda HIGH/CRITICAL bulgu 0, geri alınan kopya yok.

## Çıkarılan ölü bağlantılar (14) — gerekçe: hedef dosya HermeticOrmus__design-mastery-claude-code klonunun hiçbir yerinde yok (rglob ile arandı)
- brand-systems: references/logo-design.md · color-palettes.md · typography-pairing.md · brand-voice.md (madde satırları silindi)
- design-masters: references/massimo-vignelli.md · dieter-rams.md · paula-scher.md · david-carson.md · josef-muller-brockmann.md (madde satırları silindi)
- design-movements: references/bauhaus.md · swiss-international.md · memphis-group.md · art-deco.md · minimalism.md (madde satırları + boş başlık silindi)

## Yanlış alarm listesi (denetimde gerekçeli istisna, zip'ler değişmedi)
- policy-monitor:20 ve use-case-triage:18 · `~/.claude/plugins/config/claude-for-legal/privacy-legal/CLAUDE.md` isteğe bağlı profil; dosya yoksa skill profilsiz çalışır
- claude-design-skills-ux-research:543 · Obsidian/kişisel kurulum bölümü, repo dışı olarak belgelenmiş
- context7-context7-cli references/setup.md · ctx7 kurulum hedefini anlatan yorum satırı
- Tarifte sayılan diğer yanlış alarmlar (omni-* docs/openapi.yaml, sdp docs/muhur, ux-research Mind/ yolu, writing-plans/spec-driven-development/strix örnek yolları) denetim kalıplarına hiç takılmadı, bu yüzden listede yok.

## dist/_yerlesik/ (6, yüklenmez)
- skills-algorithmic-art · skills-brand-guidelines · skills-canvas-design · skills-internal-comms · skills-slack-gif-creator · skills-web-artifacts-builder — claude.ai'de Anthropic'in yerleşik adları; Directory'den açılır (içerik aynı, fark yalnız CRLF).

## claude.ai'de bağımlılığı bulunmayanlar
- OmniRoute 29 (OmniRoute sunucusu) · strix 6 (Strix CLI/bulut) · görsel üretim 4 (generate-image, brandkit, imagegen-frontend-mobile, image-to-code; görsel üretim aracı ister) · figma-craft (Figma MCP) · stitch-design-taste (Google Stitch) — yüklü kalır, claude.ai'de çağrılsa da aracı olmadan çalışmaz.
