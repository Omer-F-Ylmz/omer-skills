DOGRULAMA: TSV 22473 satir = diskte tekil 22407 (komut .md + SKILL.md, gercek yol, .trash haric) + 2 ayni-dosyaya-giden ek satir + 64 yerlesik; fark 0 (sadece-diskte 0, bunun 0'i tarama basladiktan sonra eklenen/degisen dosya; sadece-tsvde 0)

# Slash komut envanteri 1105

Tarama: 2026-11-05 · betik: `.kos/kopru/slash_envanter_1105.py` (+ `kategori_1105.py`, `slash_dogrula_1105.py`, `slash_md_1105.py`) · veri: `slash-komutlar-1105.tsv` (ad, tur, etkin, kaynak, description, argument-hint, kategori, not).

**Etkin = çağrılabilir kopya:** kullanıcı komut/skill (skillOverrides=off hariç), kurulu+açık plugin'in `cache` sürümü, yerleşik. `docs/`, çeviri, örnek altındaki `commands/*.md` dosyaları gerçek komut değildir (`docs-kopyasi`, etkin=hayir; `slash_docskomut_1105.py`). `marketplaces/` ve `synced/` kopyaları, kapalı/kurulu olmayan/eski sürüm plugin'ler `hayir`.

## Toplam

**22473 satır** · etkin **13565** · pasif 8908

| tür | etkin | pasif | toplam |
|---|---|---|---|
| komut | 24 | 0 | 24 |
| skill | 8662 | 65 | 8727 |
| plugin-komut | 636 | 1698 | 2334 |
| plugin-skill | 4179 | 7145 | 11324 |
| yerlesik | 64 | 0 | 64 |

| kategori | etkin | pasif | toplam |
|---|---|---|---|
| video | 753 | 356 | 1109 |
| gorsel | 438 | 277 | 715 |
| blender | 220 | 42 | 262 |
| kod | 1941 | 1038 | 2979 |
| frontend | 730 | 551 | 1281 |
| backend | 708 | 410 | 1118 |
| test | 765 | 509 | 1274 |
| guvenlik | 677 | 870 | 1547 |
| git | 745 | 417 | 1162 |
| belge | 850 | 939 | 1789 |
| arastirma | 1029 | 371 | 1400 |
| token | 461 | 232 | 693 |
| ajan | 1466 | 1531 | 2997 |
| sosyal | 1149 | 745 | 1894 |
| veri | 1038 | 387 | 1425 |
| diger | 595 | 233 | 828 |

Kategori = ad ağırlıklı anahtar sözcük sınıflaması (`kategori_1105.py`); sınır vakalarda yanılabilir, kesin kaynak TSV'deki ad/description.

## Eşleme tablosu: şu iş gelince önce bu /komutlar

Kural: işe başlamadan önce bu tabloya bak; uyan /komut varsa çağır. `—` işareti: etkin değil/yok (çağırma).

### video (753 etkin)

| iş | önce çağır |
|---|---|
| Video linki izle/uygula/tara | `/video-izle` → `/video-tarama` → `/video-uygula` |
| Kısa video / reel kurgusu | `/short-form-edit` → `/reel-plan` → `/reel-scripter` → `/reel-builder` → `/text-over-footage` → `/auto-editor` |
| Kod ile video (React/HTML) | `/hyperframes` → `/remotion-best-practices` → `/ffmpeg` |
| Altyazı / transkript / ses | `/omnicaptions-transcribe` → `/elevenlabs-tts` |
| Otomatik video hattı | `/moneyprinter-paket` → `/autoclip-paket` → `/content-factory` |

### gorsel (438 etkin)

| iş | önce çağır |
|---|---|
| Görsel üret | `/gorsel-uret` → `/image-generation` → `/generate-image` |
| Marka/tasarım dokümanı | `/design-md` → `/logo-design` → `/brand-guidelines` |
| Diyagram / çizim | `/excalidraw` → `/diagram-design-paket` → `/baoyu-diagram` |

### blender (220 etkin)

| iş | önce çağır |
|---|---|
| Blender oturumu / sahne | `/blender-oturum` → `/blender-uretim` |
| 3D varlık üretim / rig | `/3d-asset-production` → `/3d-asset-generation` → `/character-rigging` → `/cli-anything-blender` |
| Blender → web | `/blender-to-web` → `/al-3d-blender` |

### kod (1941 etkin)

| iş | önce çağır |
|---|---|
| Sadeleştirme / refactor | `/simplify` → `/ponytail:ponytail` → `/caveman:surgical-patch` |
| Hata ayıklama | `/superpowers:systematic-debugging` → `/agent-skills:debugging-and-error-recovery` |
| Kod yazma disiplini | `/karpathy-guidelines` → `/superpowers:test-driven-development` → `/agent-skills:incremental-implementation` |

### frontend (730 etkin)

| iş | önce çağır |
|---|---|
| Her UI işi (önce) | `/frontend-craft` → `/impeccable` → `/ui-ux-pro-max` → `/departman-frontend` |
| Stil / tasarım dili | `/design-md` → `/web-design-guidelines` → `/build-awwwards-quality-sites` → `/improve-ui` → `/superdesign-paket` |
| Animasyon | `/animate` → `/animasyon-atolyesi` |

### backend (708 etkin)

| iş | önce çağır |
|---|---|
| Backend / .NET | `/departman-backend-dotnet` → `/dotnet-msbuild:binlog-failure-analysis` → `/agent-skills:api-and-interface-design` |

### test (765 etkin)

| iş | önce çağır |
|---|---|
| Test yaz / koş / uygulamayı denetle | `/departman-test-qa` → `/superpowers:test-driven-development` → `/playwright-cli` → `/qa-expert:qa-expert` |
| Kapanış kanıtı | `/superpowers:verification-before-completion` → `/verification-loop` |

### guvenlik (677 etkin)

| iş | önce çağır |
|---|---|
| Sır / SAST / pentest / KVKK | `/departman-guvenlik` → `/security-review` → `/gitleaks-desktop` → `/semgrep-desktop` |

### git (745 etkin)

| iş | önce çağır |
|---|---|
| Commit / PR / CI / deploy | `/departman-surec-git-yayin` → `/commit-commands:commit` → `/commit-commands:commit-push-pr` → `/git-safety-net:git-safety-net` |
| Dal / worktree | `/superpowers:using-git-worktrees` → `/superpowers:finishing-a-development-branch` |

### belge (850 etkin)

| iş | önce çağır |
|---|---|
| docx / pptx / pdf / xlsx | `/departman-belge` → `/docx-official` → `/pptx-official` → `/pdf-official` → `/xlsx-official` |
| Yazım / spec | `/prd-yaz` → `/writing-guidelines` |

### arastirma (1029 etkin)

| iş | önce çağır |
|---|---|
| Araştırma sırası | `/departman-arastirma-ogrenme` → `/deep-research` → `/graphify` → `/beyin` |
| Web / video kaynak | `/video-izle` → `/video-tarama` → `/agent-reach` |

### token (461 etkin)

| iş | önce çağır |
|---|---|
| Bağlam / maliyet | `/departman-verimlilik` → `/context-mode:ctx-stats` → `/codeburn:cost` → `/compact` → `/clear` → `/context` → `/cost` |
| Sıkıştırma / kısa çıktı | `/rtk-desktop` → `/caveman:caveman` → `/thrifty:thrifty` → `/headroom-compress` |

### ajan (1466 etkin)

| iş | önce çağır |
|---|---|
| Zor / çok alanlı iş | `/plan-kur` → `/yetenek-getir` → `/ajan-getir` → `/kombin-rehber` |
| Plan / paralel / tartışma | `/departman-surec-plan` → `/superpowers:brainstorming` → `/superpowers:dispatching-parallel-agents` → `/roast-room` |
| Araç yönetimi | `/departman-surec-ajan-arac` → `/agents` → `/mcp` → `/plugin` |

### sosyal (1149 etkin)

| iş | önce çağır |
|---|---|
| Reel / kısa video içerik | `/reel-plan` → `/reel-scripter` → `/viral-hook-writer` → `/hormozi-hooks` → `/caption-and-hashtags` → `/social-short-production` |
| Yayın / dağıtım | `/crosspost` → `/best-time-scheduler` → `/content-factory` |
| Dinleme / analiz | `/social-listening` → `/ig-reel` |

### veri (1038 etkin)

| iş | önce çağır |
|---|---|
| Veri / DB | `/departman-veri-db` → `/jev` → `/xlsx-official` → `/exploratory-data-analysis` |

### diger (595 etkin)

| iş | önce çağır |
|---|---|
| Oyun / mod / geri kalan | `/departman-diger` → `/graphify` |

## Somut öneriler (hat sırası)

**Sosyal-oto video hattı** (konu → yayın): 
1. Konu/kaynak: `/video-izle` (tek link) veya `/video-tarama` (1-8 link) → `/video-uygula` (işe yarayanı kur). 
2. Senaryo: `/reel-plan` → `/viral-hook-writer` + `/hormozi-hooks` → `/reel-scripter`. 
3. Üretim: `/moneyprinter-paket` (konudan otomatik kısa video) ya da `/autoclip-paket` (uzun videoyu kes) ya da `/hyperframes` + `/remotion-best-practices` (kod ile). 
4. Kurgu/ses: `/short-form-edit` → `/text-over-footage` → `/omnicaptions-transcribe` (altyazı) → `/elevenlabs-tts` (ses). 
5. Yayın: `/caption-and-hashtags` → `/best-time-scheduler` → `/crosspost`; toplu hat için `/content-factory`. 
6. Geri bildirim: `/social-listening`.

**Blender:** `/blender-oturum` (önce, oturum+MCP) → `/blender-uretim` (bpy/ürün) → varlık için `/3d-asset-production`, rig için `/character-rigging`, web çıktısı için `/blender-to-web`; toplu CLI için `/cli-anything-blender`. Ayrıca Blender 5.2 skill ailesi etkin: önce `/blender-core`, teslimden önce `/blender-asset-qa`, dışa aktarımda `/blender-export-pipelines`, uçtan uca iş için `/blender-workflow-recipes`.

**Site/UI:** `/frontend-craft` (zorunlu ilk, Bölüm 6 raporu) → `/impeccable` → `/ui-ux-pro-max` (frontend-craft > impeccable > ui-ux-pro-max kuralı) → stil için `/design-md`, `/web-design-guidelines`, `/build-awwwards-quality-sites`; mevcut ekranı iyileştirme: `/improve-ui`; müdür: `/departman-frontend`.

**Kurulum:** önce `/yetenek-getir` (tek çağrı, katalog 3.3k) veya çok alanlı işte `/plan-kur`; ajan için `/ajan-getir`; en iyi 1-3 araç kombini `/kombin-rehber`; plugin/MCP: yerleşik `/plugin`, `/mcp`, `/agents`; skill keşfi `/find-skills`; müdür `/departman-surec-ajan-arac`. Dış repo kodu: önce lisans.

**İnceleme:** yerleşik `/review` ve `/security-review` + `/simplify`; kalite `/ponytail:ponytail-review`; derin: `/code-review:code-review`; müdür `/departman-surec-inceleme`; zor karar için `/roast-room`; güvenlik `/departman-guvenlik`; kapanış kanıtı `/superpowers:verification-before-completion`.

## Aynı adlı / çakışan

- Aynı tam ad birden fazla **etkin** satırda: **1869** ad (tam liste: `slash-komutlar-1105-sorunlu.tsv`, tür=cakisma).
- Yerleşik ile aynı adlı kullanıcı komutu/skill'i: `/agents`, `/batch`, `/cost`, `/debug`, `/doctor`, `/fewer-permission-prompts`, `/help`, `/init`, `/keybindings-help`, `/loop`, `/release-notes`, `/resume`, `/review`, `/schedule`, `/security-review`, `/simplify`, `/status`, `/todos`, `/update-config`, `/usage`.
- Aynı kısa ad ≥4 farklı plugin'de etkin: **12** kısa ad; en yaygın: `setup`(10), `review`(8), `search`(7), `handoff`(6), `seo-audit`(6), `help`(5), `code-review`(4), `learn`(4), `skill-creator`(4), `start`(4), `onboarding`(4), `content-strategy`(4).
- Pratik: belirsizlikte tam ad (`plugin:ad`) çağır; çıplak `/ad` kullanıcı skill'ine çözülür (bkz. synced-skill-gölgesi).

İlk 25 çakışma:

- `/designlang:designlang-tokens` ×24 (plugin-skill)
- `/ecc:backend-patterns` ×10 (plugin-skill)
- `/ecc:coding-standards` ×10 (plugin-skill)
- `/ecc:frontend-patterns` ×10 (plugin-skill)
- `/ecc:security-review` ×10 (plugin-skill)
- `/ecc:tdd-workflow` ×10 (plugin-skill)
- `/ecc:verification-loop` ×10 (plugin-skill)
- `/skill-creator` ×10 (skill)
- `/ecc:golang-patterns` ×9 (plugin-skill)
- `/ecc:golang-testing` ×9 (plugin-skill)
- `/ecc:nextjs-turbopack` ×9 (plugin-skill)
- `/ecc:postgres-patterns` ×9 (plugin-skill)
- `/ecc:api-design` ×8 (plugin-skill)
- `/ecc:e2e-testing` ×8 (plugin-skill)
- `/ecc:eval-harness` ×8 (plugin-skill)
- `/uizze:anti-ui-slop` ×8 (plugin-skill)
- `/agent-sdk-dev:new-sdk-app` ×7 (plugin-komut)
- `/code-review` ×7 (skill)
- `/ecc:continuous-learning` ×7 (plugin-skill)
- `/ecc:continuous-learning-v2` ×7 (plugin-skill)
- `/ecc:database-migrations` ×7 (plugin-skill)
- `/ecc:deployment-patterns` ×7 (plugin-skill)
- `/ecc:django-patterns` ×7 (plugin-skill)
- `/ecc:docker-patterns` ×7 (plugin-skill)
- `/ecc:jpa-patterns` ×7 (plugin-skill)

## Frontmatter'ı bozuk / eksik

Toplam sorunlu satır: **587** (etkin: 363).

| sorun | etkin | pasif |
|---|---|---|
| description yok | 76 | 211 |
| frontmatter yok | 73 | 211 |
| yaml hatasi | 287 | 13 |

Ek uyarı: frontmatter `name` ≠ dizin adı olan satır: 1836 (çağrı adı `name` alanıdır; TSV `ad` sütunu name'i verir).

Etkin sorunlular (ilk 40; tamamı sorunlu.tsv):

- `/agentmemory:recall` — frontmatter yok, description yok — `~\plugins\cache\agentmemory\agentmemory\0.9.21\opencode\commands\recall.md`
- `/agentmemory:remember` — frontmatter yok, description yok — `~\plugins\cache\agentmemory\agentmemory\0.9.21\opencode\commands\remember.md`
- `/cli-anything:cli-anything` — frontmatter yok, description yok — `~\plugins\cache\cli-anything\cli-anything\b1e9d53e9d0d\commands\cli-anything.md`
- `/cli-anything:list` — frontmatter yok, description yok — `~\plugins\cache\cli-anything\cli-anything\b1e9d53e9d0d\commands\list.md`
- `/cli-anything:refine` — frontmatter yok, description yok — `~\plugins\cache\cli-anything\cli-anything\b1e9d53e9d0d\commands\refine.md`
- `/cli-anything:test` — frontmatter yok, description yok — `~\plugins\cache\cli-anything\cli-anything\b1e9d53e9d0d\commands\test.md`
- `/cli-anything:validate` — frontmatter yok, description yok — `~\plugins\cache\cli-anything\cli-anything\b1e9d53e9d0d\commands\validate.md`
- `/code-modernization:modernize` — yaml hatasi — `~\plugins\cache\claude-plugins-official\code-modernization\1.0.0\commands\modernize.md`
- `/designlang:gallery` — yaml hatasi — `~\plugins\cache\designlang\designlang\13.3.2\commands\gallery.md`
- `/designlang:studio` — yaml hatasi — `~\plugins\cache\designlang\designlang\13.3.2\commands\studio.md`
- `/ecc:loop-start` — frontmatter yok, description yok — `~\plugins\cache\ecc\ecc\2.2.3\.opencode\commands\loop-start.md`
- `/ecc:loop-status` — frontmatter yok, description yok — `~\plugins\cache\ecc\ecc\2.2.3\.opencode\commands\loop-status.md`
- `/ecc:model-route` — frontmatter yok, description yok — `~\plugins\cache\ecc\ecc\2.2.3\.opencode\commands\model-route.md`
- `/ecc:quality-gate` — frontmatter yok, description yok — `~\plugins\cache\ecc\ecc\2.2.3\.opencode\commands\quality-gate.md`
- `/mindful-claude:mindful` — frontmatter yok, description yok — `~\plugins\cache\mindful-claude\mindful-claude\2.0.0\legacy\commands\mindful.md`
- `/taskmaster:add-dependency` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\add-dependency.md`
- `/taskmaster:add-subtask` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\add-subtask.md`
- `/taskmaster:add-task` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\add-task.md`
- `/taskmaster:analyze-complexity` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\analyze-complexity.md`
- `/taskmaster:analyze-project` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\analyze-project.md`
- `/taskmaster:auto-implement-tasks` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\auto-implement-tasks.md`
- `/taskmaster:command-pipeline` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\command-pipeline.md`
- `/taskmaster:complexity-report` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\complexity-report.md`
- `/taskmaster:convert-task-to-subtask` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\convert-task-to-subtask.md`
- `/taskmaster:expand-all-tasks` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\expand-all-tasks.md`
- `/taskmaster:expand-task` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\expand-task.md`
- `/taskmaster:fix-dependencies` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\fix-dependencies.md`
- `/taskmaster:help` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\help.md`
- `/taskmaster:init-project` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\init-project.md`
- `/taskmaster:init-project-quick` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\init-project-quick.md`
- `/taskmaster:install-taskmaster` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\install-taskmaster.md`
- `/taskmaster:learn` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\learn.md`
- `/taskmaster:list-tasks` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\list-tasks.md`
- `/taskmaster:list-tasks-by-status` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\list-tasks-by-status.md`
- `/taskmaster:list-tasks-with-subtasks` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\list-tasks-with-subtasks.md`
- `/taskmaster:next-task` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\next-task.md`
- `/taskmaster:parse-prd` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\parse-prd.md`
- `/taskmaster:parse-prd-with-research` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\parse-prd-with-research.md`
- `/taskmaster:project-status` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\project-status.md`
- `/taskmaster:quick-install-taskmaster` — frontmatter yok, description yok — `~\plugins\cache\taskmaster\taskmaster\c0c98d367c55\commands\quick-install-taskmaster.md`



## Yeni (5 Kas 14:35, jakubkrehel/skills — IG DfVTwF2iVF_, NİHAİ 36(J))
| /komut | Ne zaman |
|---|---|
| /better-interface (jk-better-interface) | Ekran/akış/arayüz tam incelemesi: erişilebilirlik, yerleşim, metin, tipografi, renk |
| /better-accessibility (jk-) | Klavye/odak, ARIA, form, ekran okuyucu düzeltme |
| /better-colors (jk-) | Palet, semantik token, renk dönüştürme/kontrast |
| /better-layout (jk-) | Gruplama, hizalama, okuma sırası, responsive |
| /better-typography (jk-) | Tip ölçeği, aralık, font özellikleri, satır kırma |
| /better-ui (jk-) | Yüzey/ikon/hareket cilası: radius, gölge, optik hizalama |
| /better-writing (jk-) | Arayüz metni: etiket, hata, boş durum, onay |
| /break | Bileşeni tüm senaryolarda geçici sayfada stres testi |
| /build-design | Figma/tasarım görselinden mevcut token'larla birebir UI |
| /explain-interface | Canlı URL/ekran görüntüsünden efekt/animasyonun nasıl yapıldığını çözer |
| /interface-review | Branch/PR/commit edilmemiş değişikliğin arayüz incelemesi (yalnız elle çağrılır) |
| /state-machine | Bileşenin her durumunu mock veri + switcher ile gösterir |
| /teardown | Fiziksel nesne / nasıl çalışır teknik illüstrasyonu |
| /variant | Bileşenin çoklu varyantını üretip seçtirir (yalnız elle çağrılır) |


## ECC (everything-claude-code 2.2.3) — eksik komutlar + ajanlar (5 Kas 17:35, NİHAİ 48)
Kurulu ve etkin; son 7 günde 11.718 oturumda HİÇ kullanılmamıştı. İş başında bu tablo da taranır.
| /komut | Ne zaman |
|---|---|
| /ecc:aside | Answer a quick side question without interrupting or losing context from the current task. Resume work automatically after answering. |
| /ecc:auto-update | Pull the latest ECC repo changes and reinstall the current managed targets. |
| /ecc:build-fix | Detect the project build system and incrementally fix build/type errors with minimal safe changes. |
| /ecc:checkpoint | Create, verify, or list workflow checkpoints after running verification checks. |
| /ecc:code-review | Code review — local uncommitted changes or GitHub PR (pass PR number/URL for PR mode). Use for a step-by-step PRP-style checklist review; for a multi- |
| /ecc:cost-report | Generate a local Claude Code cost report from the ECC cost-tracker metrics log. Use for a terminal summary or CSV export of tracked spend; the cost-tr |
| /ecc:cpp-build | Fix C++ build errors, CMake issues, and linker problems incrementally. Invokes the cpp-build-resolver agent for minimal, surgical fixes. |
| /ecc:cpp-review | Comprehensive C++ code review for memory safety, modern C++ idioms, concurrency, and security. Invokes the cpp-reviewer agent. |
| /ecc:cpp-test | Enforce TDD workflow for C++. Write GoogleTest tests first, then implement. Verify coverage with gcov/lcov. |
| /ecc:ecc-guide | Navigate ECC's current agents, skills, commands, hooks, install profiles, and docs from the live repository surface. This is the slash-command entrypo |
| /ecc:epic-claim | Claim an epic issue, stamp coordination state, and sync local ownership. |
| /ecc:epic-decompose | Break an epic into task children without creating task branches. |
| /ecc:epic-publish | Publish a validated epic update back to the issue and local cache. |
| /ecc:epic-review | Mark epic review requested, approved, or changes requested. |
| /ecc:epic-sync | Sync epic issue bodies, labels, and local coordination snapshots from GitHub. |
| /ecc:epic-unblock | Sweep blocked epic issues and reopen anything whose dependencies are closed. |
| /ecc:epic-validate | Validate epic readiness, dependencies, and coordination policy. |
| /ecc:evolve | Analyze instincts and suggest or generate evolved structures |
| /ecc:fastapi-review | Review a FastAPI application for architecture, async correctness, dependency injection, Pydantic schemas, security, performance, and testability. |
| /ecc:feature-dev | Guided feature development with codebase understanding and architecture focus |
| /ecc:flutter-build | Fix Dart analyzer errors and Flutter build failures incrementally. Invokes the dart-build-resolver agent for minimal, surgical fixes. |
| /ecc:flutter-review | Review Flutter/Dart code for idiomatic patterns, widget best practices, state management, performance, accessibility, and security. Invokes the flutte |
| /ecc:flutter-test | Run Flutter/Dart tests, report failures, and incrementally fix test issues. Covers unit, widget, golden, and integration tests. |
| /ecc:gan-build | Run a generator/evaluator build loop for implementation tasks with bounded iterations and scoring. |
| /ecc:gan-design | Run a generator/evaluator design loop for frontend or visual work with bounded iterations and scoring. |
| /ecc:go-build | Fix Go build errors, go vet warnings, and linter issues incrementally. Invokes the go-build-resolver agent for minimal, surgical fixes. |
| /ecc:go-review | Comprehensive Go code review for idiomatic patterns, concurrency safety, error handling, and security. Invokes the go-reviewer agent. |
| /ecc:go-test | Enforce TDD workflow for Go. Write table-driven tests first, then implement. Verify 80%+ coverage with go test -cover. |
| /ecc:gradle-build | Fix Gradle build errors for Android and KMP projects |
| /ecc:harness-audit | Run a deterministic repository harness audit and return a prioritized scorecard. Use for a deterministic overall repo-readiness scorecard; for a secur |
| /ecc:hookify-configure | Enable or disable hookify rules interactively |
| /ecc:hookify-help | Get help with the hookify system |
| /ecc:hookify-list | List all configured hookify rules |
| /ecc:hookify | Create hooks to prevent unwanted behaviors from conversation analysis or explicit instructions. Use to generate a new hook rule file from conversation |
| /ecc:instinct-export | Export instincts from project/global scope to a file |
| /ecc:instinct-import | Import instincts from file or URL into project/global scope |
| /ecc:instinct-status | Show learned instincts (project + global) with confidence |
| /ecc:jira | Retrieve a Jira ticket, analyze requirements, update status, or add comments. Uses the jira-integration skill and MCP or REST API. |
| /ecc:kotlin-build | Fix Kotlin/Gradle build errors, compiler warnings, and dependency issues incrementally. Invokes the kotlin-build-resolver agent for minimal, surgical  |
| /ecc:kotlin-review | Comprehensive Kotlin code review for idiomatic patterns, null safety, coroutine safety, and security. Invokes the kotlin-reviewer agent. |
| /ecc:kotlin-test | Enforce TDD workflow for Kotlin. Write Kotest tests first, then implement. Verify 80%+ coverage with Kover. |
| /ecc:learn-eval | Extract reusable patterns from the session, self-evaluate quality before saving, and determine the right save location (Global vs Project). |
| /ecc:learn | Extract reusable patterns from the current session and save them as candidate skills or guidance. Use to review a session on demand and persist an app |
| /ecc:marketing-campaign | Plan and execute a full marketing campaign. Accepts a product brief and returns positioning, landing page copy, email sequence, social posts, ad varia |
| /ecc:multi-backend | Run a backend-focused multi-model workflow for APIs, algorithms, data, and business logic. |
| /ecc:multi-execute | Execute a multi-model implementation plan while preserving Claude as the only filesystem writer. |
| /ecc:multi-frontend | Run a frontend-focused multi-model workflow for components, layouts, animation, and UI polish. |
| /ecc:multi-plan | Create a multi-model (Codex + Antigravity) implementation plan without modifying production code. Requires the external ccg-workflow runtime, not part |
| /ecc:multi-workflow | Run a full multi-model development workflow with research, planning, execution, optimization, and review. |
| /ecc:orch-add-feature | Orchestrate building a brand-new feature end to end — research, plan, TDD, review, gated commit. Wrapper that kicks off the orch-add-feature skill. |
| /ecc:orch-build-mvp | Orchestrate bootstrapping a working MVP from a design/spec doc — ingest, slice, scaffold, TDD, review, gated commit (reuses the GAN harness). Wrapper  |
| /ecc:orch-change-feature | Orchestrate altering an existing, working feature to new desired behavior — update tests to the new spec, change impl, review, gated commit. Wrapper f |
| /ecc:orch-fix-defect | Orchestrate fixing a bug — reproduce it as a failing regression test, fix to green, review, gated commit. Wrapper for the orch-fix-defect skill. |
| /ecc:orch-refine-code | Orchestrate a behavior-preserving refactor — confirm tests green, restructure without changing behavior, keep green, review, gated commit. Wrapper for |
| /ecc:orch-review | Run the orch-review native Workflow over a diff (local changes or a GitHub PR) and report blocking vs advisory findings. Surface for the orch-review w |
| /ecc:plan-canvas | Open a plan or HTML artifact in the browser Plan Canvas for annotate-and-approve review. This is a thin slash-command entrypoint over the plan-canvas  |
| /ecc:plan-prd | Generate a lean, problem-first PRD and hand off to /plan for implementation planning. |
| /ecc:plan | Restate requirements, assess risks, and create step-by-step implementation plan. WAIT for user CONFIRM before touching any code. Use for a single-mode |
| /ecc:pm2 | Analyze a project and generate PM2 service commands for detected frontend, backend, or database services. |
| /ecc:pr | Create a GitHub PR from current branch with unpushed commits — discovers templates, analyzes changes, pushes |
| /ecc:project-init | Detect a project's stack and produce a dry-run ECC onboarding plan using the repository's install manifests and stack mappings. Use to onboard ECC int |
| /ecc:projects | List known projects and their instinct statistics |
| /ecc:promote | Promote project-scoped instincts to global scope |
| /ecc:prp-commit | Quick commit with natural language file targeting — describe what to commit in plain English |
| /ecc:prp-implement | Execute an implementation plan with rigorous validation loops |
| /ecc:prp-plan | Create comprehensive feature implementation plan with codebase analysis and pattern extraction |
| /ecc:prp-pr | Alias of /pr for the PRP workflow series. Use when creating a pull request mid-PRP workflow; otherwise use /pr. |
| /ecc:prp-prd | Interactive PRD generator - problem-first, hypothesis-driven product spec with back-and-forth questioning |
| /ecc:prune | Delete pending instincts older than 30 days that were never promoted. Thin CLI wrapper for continuous-learning-v2's instinct-cli.py prune command; use |
| /ecc:python-review | Comprehensive Python code review for PEP 8 compliance, type hints, security, and Pythonic idioms. Invokes the python-reviewer agent. |
| /ecc:react-build | Fix React build failures (Vite, webpack, Next.js, CRA, Parcel, esbuild, Bun) incrementally — JSX/TSX compile errors, hydration mismatches, server/clie |
| /ecc:react-review | Comprehensive React/JSX code review for hook correctness, render performance, server/client component boundaries, accessibility, and React-specific se |
| /ecc:react-test | Enforce TDD workflow for React. Write React Testing Library tests first (behavior-focused, accessibility-first), then implement components. Detects Vi |
| /ecc:refactor-clean | Safely identify and remove dead code with verification after each change. |
| /ecc:resume-session | Load the most recent session file from ~/.claude/session-data/ and resume work with full context from where the last session ended. |
| /ecc:review-pr | Comprehensive PR review using specialized agents (code-reviewer, comment-analyzer, pr-test-analyzer, silent-failure-hunter, type-design-analyzer, code |
| /ecc:rust-build | Fix Rust build errors, borrow checker issues, and dependency problems incrementally. Invokes the rust-build-resolver agent for minimal, surgical fixes |
| /ecc:rust-review | Comprehensive Rust code review for ownership, lifetimes, error handling, unsafe usage, and idiomatic patterns. Invokes the rust-reviewer agent. |
| /ecc:rust-test | Enforce TDD workflow for Rust. Write tests first, then implement. Verify 80%+ coverage with cargo-llvm-cov. |
| /ecc:santa-loop | Adversarial dual-review convergence loop — two independent model reviewers must both approve before code ships. Use for the CLI-driven version of this |
| /ecc:save-session | Save current session state to a dated file in ~/.claude/session-data/ so work can be resumed in a future session with full context. |
| /ecc:security-scan | Run AgentShield against agent, hook, MCP, permission, and secret surfaces. This is the slash-command entrypoint for that audit; prefer the security-sc |
| /ecc:sessions | Manage Claude Code session history, aliases, and session metadata. |
| /ecc:setup-pm | Configure your preferred package manager (npm/pnpm/yarn/bun) |
| /ecc:skill-create | Analyze local git history to extract coding patterns and generate SKILL.md files. Local version of the Skill Creator GitHub App. Use to generate new s |
| /ecc:skill-health | Show skill portfolio health dashboard with charts and analytics. Use for the quantitative usage/success-rate dashboard; for a qualitative compliance o |
| /ecc:test-coverage | Analyze coverage, identify gaps, and generate missing tests toward the target threshold. |
| /ecc:update-codemaps | Scan project structure and generate token-lean architecture codemaps. |
| /ecc:update-docs | Sync documentation from source-of-truth files such as scripts, schemas, routes, and exports. |
| /ecc:vue-review | Comprehensive Vue.js code review for Composition API correctness, reactivity, composable patterns, template security, accessibility, and Vue-specific  |

| Ajan | Ne zaman |
|---|---|
| ecc:a11y-architect (ajan) | Accessibility Architect specializing in WCAG 2.2 compliance for Web and Native platforms. |
| ecc:agent-evaluator (ajan) | Evaluates agent output against 5-axis quality rubric (accuracy, completeness, clarity, actionability, conciseness). |
| ecc:architect (ajan) | Software architecture specialist for system design, scalability, and technical decision-making. |
| ecc:build-error-resolver (ajan) | Build and TypeScript error resolution specialist. Use PROACTIVELY when build fails or type errors occur. |
| ecc:chief-of-staff (ajan) | Personal communication chief of staff that triages email, Slack, LINE, and Messenger. |
| ecc:code-architect (ajan) | Designs feature architectures by analyzing existing codebase patterns and conventions, then providing implementation blueprints with concrete files… |
| ecc:code-explorer (ajan) | Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, and documenting dependencies to inform new develop |
| ecc:code-reviewer (ajan) | Expert code review specialist. Proactively reviews code for quality, security, and maintainability. |
| ecc:code-simplifier (ajan) | Simplifies and refines code for clarity, consistency, and maintainability while preserving behavior. |
| ecc:comment-analyzer (ajan) | Analyze code comments for accuracy, completeness, maintainability, and comment rot risk. |
| ecc:conversation-analyzer (ajan) | Use this agent when analyzing conversation transcripts to find behaviors worth preventing with hooks. Triggered by /hookify without arguments. |
| ecc:cpp-build-resolver (ajan) | C++ build, CMake, and compilation error resolution specialist. |
| ecc:cpp-reviewer (ajan) | Expert C++ code reviewer specializing in memory safety, modern C++ idioms, concurrency, and performance. |
| ecc:csharp-reviewer (ajan) | Expert C# code reviewer specializing in .NET conventions, async patterns, security, nullable reference types, and performance. |
| ecc:dart-build-resolver (ajan) | Dart/Flutter build, analysis, and dependency error resolution specialist. |
| ecc:database-reviewer (ajan) | PostgreSQL database specialist for query optimization, schema design, security, and performance. |
| ecc:django-build-resolver (ajan) | Django/Python build, migration, and dependency error resolution specialist. |
| ecc:django-reviewer (ajan) | Expert Django code reviewer specializing in ORM correctness, DRF patterns, migration safety, security misconfigurations, and production-grade Django p |
| ecc:doc-updater (ajan) | Documentation and codemap specialist. Use PROACTIVELY for updating codemaps and documentation. |
| ecc:docs-lookup (ajan) | When the user asks how to use a library, framework, or API or needs up-to-date code examples, use Context7 MCP to fetch current documentation and retu |
| ecc:e2e-runner (ajan) | End-to-end testing specialist using Vercel Agent Browser (preferred) with Playwright fallback. |
| ecc:fastapi-reviewer (ajan) | Reviews FastAPI applications for async correctness, dependency injection, Pydantic schemas, security, OpenAPI quality, testing, and production readine |
| ecc:flutter-reviewer (ajan) | Flutter and Dart code reviewer. Reviews Flutter code for widget best practices, state management patterns, Dart idioms, performance pitfalls, accessib |
| ecc:fsharp-reviewer (ajan) | Expert F# code reviewer specializing in functional idioms, type safety, pattern matching, computation expressions, and performance. |
| ecc:gan-evaluator (ajan) | GAN Harness — Evaluator agent. Tests the live running application via Playwright, scores against rubric, and provides actionable feedback to the Gener |
| ecc:gan-generator (ajan) | GAN Harness — Generator agent. Implements features according to the spec, reads evaluator feedback, and iterates until quality threshold is met. |
| ecc:gan-planner (ajan) | GAN Harness — Planner agent. Expands a one-line prompt into a full product specification with features, sprints, evaluation criteria, and design direc |
| ecc:go-build-resolver (ajan) | Go build, vet, and compilation error resolution specialist. |
| ecc:go-reviewer (ajan) | Expert Go code reviewer specializing in idiomatic Go, concurrency patterns, error handling, and performance. |
| ecc:harmonyos-app-resolver (ajan) | HarmonyOS application development expert specializing in ArkTS and ArkUI. |
| ecc:harness-optimizer (ajan) | Improve local agent-harness configuration reliability and cost using eval-driven grading (pass@k/pass^k) derived from the eval-harness skill. |
| ecc:healthcare-reviewer (ajan) | Reviews healthcare application code for clinical safety, CDSS accuracy, PHI compliance, and medical data integrity. |
| ecc:homelab-architect (ajan) | Designs home and small-lab network plans from hardware inventory, goals, and operator experience level, with safe staged changes and rollback guidance |
| ecc:java-build-resolver (ajan) | Java/Maven/Gradle build, compilation, and dependency error resolution specialist. |
| ecc:java-reviewer (ajan) | Expert Java code reviewer for Spring Boot and Quarkus projects. |
| ecc:kotlin-build-resolver (ajan) | Kotlin/Gradle build, compilation, and dependency error resolution specialist. |
| ecc:kotlin-reviewer (ajan) | Kotlin and Android/KMP code reviewer. Reviews Kotlin code for idiomatic patterns, coroutine safety, Compose best practices, clean architecture violati |
| ecc:loop-operator (ajan) | Operate autonomous agent loops, monitor progress, and intervene safely when loops stall. |
| ecc:marketing-agent (ajan) | Marketing strategist and copywriter for campaign planning, audience research, positioning, copy creation, and content review. |
| ecc:mle-reviewer (ajan) | Production machine-learning engineering reviewer for data contracts, feature pipelines, training reproducibility, offline/online evaluation, model ser |
| ecc:network-architect (ajan) | Designs enterprise or multi-site network architecture from requirements, using existing network skills for focused routing, validation, automation, an |
| ecc:network-config-reviewer (ajan) | Reviews router and switch configurations for security, correctness, stale references, risky change-window commands, and missing operational guardrails |
| ecc:network-troubleshooter (ajan) | Diagnoses network connectivity, routing, DNS, interface, and policy symptoms with a read-only OSI-layer workflow and evidence-backed root cause summar |
| ecc:opensource-forker (ajan) | Fork any project for open-sourcing. Copies files, strips secrets and credentials (20+ patterns), replaces internal references with placeholders, gener |
| ecc:opensource-packager (ajan) | Generate complete open-source packaging for a sanitized project. |
| ecc:opensource-sanitizer (ajan) | Verify an open-source fork is fully sanitized before release. |
| ecc:performance-optimizer (ajan) | Performance analysis and optimization specialist. Use PROACTIVELY for identifying bottlenecks, optimizing slow code, reducing bundle sizes, and improv |
| ecc:php-reviewer (ajan) | Expert PHP code reviewer specializing in PSR-12 compliance, PHP type system, Eloquent ORM patterns, security, and performance. |
| ecc:planner (ajan) | Expert planning specialist for complex features and refactoring. |
| ecc:pr-test-analyzer (ajan) | Review pull request test coverage quality and completeness, with emphasis on behavioral coverage and real bug prevention. |
| ecc:python-reviewer (ajan) | Expert Python code reviewer specializing in PEP 8 compliance, Pythonic idioms, type hints, security, and performance. |
| ecc:pytorch-build-resolver (ajan) | PyTorch runtime, CUDA, and training error resolution specialist. |
| ecc:rag-pipeline-reviewer (ajan) | Reviews RAG (Retrieval-Augmented Generation) pipelines for retrieval quality, chunking strategy, embedding choices, and evaluation coverage. |
| ecc:react-build-resolver (ajan) | Diagnose and fix React build failures across Vite, webpack, Next.js, CRA, Parcel, esbuild, and Bun. |
| ecc:react-reviewer (ajan) | Expert React/JSX code reviewer specializing in hook correctness, render performance, server/client component boundaries, accessibility, and React-spec |
| ecc:refactor-cleaner (ajan) | Dead code cleanup and consolidation specialist. Use PROACTIVELY for removing unused code, duplicates, and refactoring. |
| ecc:rust-build-resolver (ajan) | Rust build, compilation, and dependency error resolution specialist. |
| ecc:rust-reviewer (ajan) | Expert Rust code reviewer specializing in ownership, lifetimes, error handling, unsafe usage, and idiomatic patterns. |
| ecc:security-reviewer (ajan) | Security vulnerability detection and remediation specialist. |
| ecc:seo-specialist (ajan) | SEO specialist for technical SEO audits, on-page optimization, structured data, Core Web Vitals, and content/keyword mapping. |
| ecc:silent-failure-hunter (ajan) | Review code for silent failures, swallowed errors, bad fallbacks, and missing error propagation. |
| ecc:spec-miner (ajan) | Extracts behavioral specs from existing codebases for OpenSpec. |
| ecc:swift-build-resolver (ajan) | Swift/Xcode build, compilation, and dependency error resolution specialist. |
| ecc:swift-reviewer (ajan) | Expert Swift code reviewer specializing in protocol-oriented design, value semantics, ARC memory management, Swift Concurrency, and idiomatic patterns |
| ecc:tdd-guide (ajan) | Test-Driven Development specialist enforcing write-tests-first methodology. |
| ecc:type-design-analyzer (ajan) | Analyze type design for encapsulation, invariant expression, usefulness, and enforcement. |
| ecc:typescript-reviewer (ajan) | Expert TypeScript/JavaScript code reviewer specializing in type safety, async correctness, Node/web security, and idiomatic patterns. |
| ecc:vue-reviewer (ajan) | Expert Vue.js code reviewer specializing in Composition API correctness, reactivity pitfalls, component architecture, template security, and Vue-speci |

## claude-code-setup 1.0.0
| skill | Ne zaman |
|---|---|
| claude-automation-recommender | Proje/kod tabanı için hook, alt ajan, skill, plugin, MCP önerisi; yeni projede ve kurulum gözden geçirmede |
