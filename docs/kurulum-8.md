# KURULUM-8 · 64 listenin eksikleri · 20 Eyl 2026

KARAR (Ömer): hiçbir şey elenmez, SkillSpector kapısı yok · ücretli servis/abonelik kurulmaz (claude-mem-cowork dahil) · gstack claude.ai'ye gitmez · yerel MCP'ler yalnız CC'ye, Claude Desktop config'e dokunulmaz · anahtarlar `~/.claude.json`'a değer değil `${VAR}` literal.
Kaynak: docs/kurulum-6-cc.md, docs/kurulum-7.md, docs/claude-ai-mcp.md. Yedek: `~/.claude.json.bak8`.

## Aday havuzu

| küme | sayı |
|---|---|
| plugin skill'leri (benzersiz ad, marketplace.json `skills:` alanına göre) | 190 |
| `~/.claude/skills` yerel (synced hariç) | 65 |
| − synced 164 · − claude.ai yerleşiği 15 · − `gstack` | 213 |
| − gstack paketi (55 alt-skill) · − cowork'ün `mem-setup`'ı · − klasör adıyla saklanan 10 synced taste-skill | **148** |
| + yeni `omer-kutuphaneler` | **149 zip · 8 parti** |

Envanter kuralı: `installed_plugins.json` → `installPath`; skill dizinleri ilgili `marketplace.json`'daki plugin girdisinin **`skills:` alanından** alınır, yoksa `installPath/skills/**/SKILL.md`. (Kritik: `anthropic-agent-skills` klonunda `skills/` altında 19 skill var ama `claude-api` plugin'i yalnız 1'ini ilan ediyor — dizin taraması 3 katı fazla sayıyordu.)

**Skill kimliği = frontmatter `name`, klasör adı değil.** `taste-skill` plugin'inde ikisi ayrışıyor (`skills/soft-skill/` → `name: high-end-visual-design`, `skills/taste-skill/` → `name: design-taste-frontend`). Klasör adıyla sayıldığında bu 10 skill "yeni" görünüp synced kopyalarının üstüne ad değiştirerek gidiyordu; `name` ile sayılınca 10'u "zaten claude.ai", yalnız synced'de bulunmayan **design-taste-frontend (v2)** yukle-8'e girdi. `name` slug değilse (hookify: `Writing Hookify Rules`) klasör adı kimlik sayılır.

**Ad çakışması yok.** `mem-search` cowork çıkınca tek kaldı (claude-mem'inki kendi adıyla), `test-driven-development` / `superpowers-tdd` synced'de → "zaten claude.ai". `<plugin>-<ad>` kuralı kodda duruyor, tetiklenmedi.

**Taşınmayanlar (skill değil):** 44 komut · 49 agent · 69 hook · 0 output-style. Sayıldı, zip'lenmedi.

### "claude.ai'de çalışır" ölçütü

Mekanik: SKILL.md'nin kabuk kod bloklarında yerel ikili/servis çağrısı (`dotnet`, `npx`, `node`, `bun`, `uvx`, `docker`, `WORKER_PORT`, `127.0.0.1`…) varsa **hayır**; kabuk bloğu var ama yerel ikili yoksa **kısmen**; saf rehberse **evet**.
Sonuç: **evet 138 · kısmen 1 · hayır 10**. "hayır" olanlar yine zip'lendi (KARAR: hiçbir şey elenmez).

- claude-mem: babysit · ccs-align · cloud-sync · standup · timeline-report · weekly-digests → yerel claude-mem worker (`127.0.0.1:37777`) ister
- everything-claude-code: continuous-learning · strategic-compact → CC `settings.json` hook kurulumu ister
- phoenix-cti-search: cti-domain-research → CC eklenti/komut dosyası (`notebooklm-connector`) ister
- superpowers: finishing-a-development-branch → `git worktree` ister · systematic-debugging **kısmen** (kabuk bloğu var, ikili yok)

## Zip üretimi ve denetim

Zip kuralı (7c/7f yöntemi): `<plugin>-<ad>.zip`, içi `<ad>/SKILL.md` · `description` ≤200 · `.sh`/shebang'li dosyalar LF · iç içe zip, `.claude-plugin/`, `plugin.json` çıkarıldı · yolda yasak karakter yok · açık boyut ≤30 MB (en büyük: claude-api 415 KB).

Üretimde uygulanan düzeltmeler: **119 description kısaltması** · **24 referans** skill dışından `_ref/` altına kopyalandı (ör. `security-assessment/_ref/security-reviewer/checklists/*`) · **1 `name` düzeltmesi** · **3 frontmatter üretimi** (everything-claude-code'un eval-harness, project-guidelines-example, verification-loop dosyalarında hiç frontmatter yoktu — H1 + ilk paragraftan üretildi). `${CLAUDE_PLUGIN_ROOT}` → `$(ls -d /mnt/skills/*/<ad> | head -1)`.

KURULUM-8b'de eklenen üç düzeltme (`tools/yukle8.py`):

1. **Kök dışındaki her `SKILL.md` → `SKILL.ref.md`** (`ref_skillmd`). `referans_getir` başka bir skill'i `_ref/` altına kopyaladığında zip'te birden çok `SKILL.md` oluşuyordu; claude.ai tam olarak bir tane istiyor. Yeniden adlandırılan dosyaya **gerçekten çözülen** başvurular güncelleniyor (dosyaya göreli + kök göreli), çözülmeyene dokunulmuyor — 8b'de 5 başvuru güncellendi, 0 kırık.
2. **Üç yeniden adlandırma** (`YENI_AD`): `claude-api` → `messages-api-sdk` · `claude-md-improver` → `memory-md-improver` · `claude-opus-4-5-migration` → `opus-4-5-migration`. Yalnız **zip içi `name` + klasör** değişir; `/mnt/skills/*/<ad>` yolları yeni adla üretilir, `description` aynen kalır. CC plugin adlarına ve kaynak skill'lere dokunulmadı (zip dosya adı `<plugin>-<yeni ad>.zip`).
3. **`description`'da açılı parantez yok**: `<…>` içeriği parantezsiz yazılır (`<file>` → `file`), `->`/`<-` ok işaretine (`→`/`←`) çevrilir. Anlam korunur.

```
python tools/skill_denetim.py dist/yukle-8    → 141 zip · 0 hata · 53 ~/.claude uyarısı
python tools/skill_denetim.py dist/yukle-8b   → 8 zip · 0 hata (yama partisi)
python tools/skill_denetim.py dist            → 318 zip · 0 hata (gerileme yok)
```

**claude.ai'de yüklü 141/149; yama 8 (`dist/yukle-8b`).** claude.ai Add ekranı bu 8'i üç gerekçeyle reddetti; kapıya üç kural, zip üretimine üç düzeltme eklendi (aşağıda). Eski 8 zip `dist/yukle-8`'den silindi, orada 141 kaldı.

### tools/skill_denetim.py · KURULUM-8b kapısı (claude.ai ret kuralları)

Üçü de claude.ai Add ekranının kendi hata metninden; kalibrasyon (eski 8 zip silinmeden): **8 zip'te beklenen hatalar, diğer 141'de 0**.

1. **Zip'te tam olarak bir `SKILL.md`** (basename, büyük/küçük harf fark etmez) — *"Zip must contain exactly one SKILL.md file. Currently there are N"*.
2. **`name`'de `claude`/`anthropic` yok** — *"Skill name in SKILL.md cannot contain the reserved word 'claude'"*.
3. **`name` ve `description`'da `<` ya da `>` yok** — *"SKILL.md description cannot contain XML tags"*. (Kural claude.ai'den katı: `tm-security-review`'in `->` okları claude.ai'yi geçerdi ama kapı yakaladı, o da düzeltildi.)

Yeni kapı **dist'in tamamında** (318 zip) koşturuldu: eski partilerde hata yok, düzeltme gerekmedi.

### tools/skill_denetim.py · KURULUM-8 incelmeleri

1. **`~/.claude-mem` artık eşleşmiyor** (`CLAUDE_EV = ~/\.claude(?:/|\b(?!-))`) — ayrı bir dizin, CC ev dizini değil.
2. **`~/.claude` iki kademe:** SKILL.md'nin kod bloğunda ya da `./` ile çağırdığı betikte geçiyorsa **hata** (skill akışı CC evine bağlı); düz metin/başvuru dosyasında geçiyorsa **uyarı** (53 uyarı; CRLF'in 7b'deki kademelemesiyle aynı mantık).
3. **17 yeni gerekçeli istisna** (`YANLIS_ALARM`), üç sınıfta — hepsi raporda adıyla ve gerekçesiyle basılıyor:
   - *CC kurulumunu anlatan kod bloğu* (3): continuous-learning, strategic-compact, cti-domain-research — tabloda "claude.ai'de çalışmaz" işaretli.
   - *düz metin örnek* (9): skill-development (skill yazmayı anlatan öğretici, 21 örnek yol), git-workflow `../project-feature-a|b`, minimal-api-file-upload `etc/passwd` (path traversal örneği), msbuild-antipatterns, platform-detection/run-tests `scripts/CI`, scroll-craft `assets/01*.mp4`, writing-skills `../some-skill`, 0day-scanner glob.
   - *kaynak pakette de yok* (5): ccs-align `../../src/`, mode-creator `scripts/worker-service.cjs`, version-bump `scripts/generate-changelog.js`, design-principles `references/`, threat-modeling `../../docs/` — üst akış eksiği, zip kusuru değil.

## Skill tablosu

`zaten claude.ai` = synced 164'ün içinde (asgari listeden: test-driven-development/superpowers-tdd, playwright-cli, brand-systems, design-masters, design-movements, 21st-ui, ponytail ×6, taste-skill'in 11 kopyası…). design-taste-frontend · imagegen-frontend-web · webapp-testing bu listeden çıktı: tabloda yukle-8'deler, claude.ai'de tek kopya.
`CC-özel` = claude.ai'ye gitmez.

| kaynak | skill | durum | claude.ai'de çalışır | parti |
|---|---|---|---|---|
| gstack (55 alt-skill + `_gstack-command`) | — | CC-özel (7f: preamble yolu yer tutucu, bun/browse ikilisi, "invalid characters" reddi) | hayır | — |
| claude-mem-cowork | mem-setup | CC-özel, kurulmadı (CMEM Cloud ücretli; Ömer kararı) | — | — |
| synced (claude.ai) | 164 skill | zaten claude.ai | — | — |
| claude.ai yerleşiği | 15 skill (docx/pdf/pptx/xlsx, frontend-design, skill-creator, mcp-builder, theme-factory, canvas-design, web-artifacts-builder, algorithmic-art, brand-guidelines, doc-coauthoring, internal-comms, slack-gif-creator) | zaten claude.ai | — | — |
| (yerel/yeni) | agent-reach | yukle-8 | evet | 1 |
| (yerel/yeni) | graphify | yukle-8 | evet | 3 |
| (yerel/yeni) | hetzner-deploy | yukle-8 | evet | 3 |
| (yerel/yeni) | omer-kutuphaneler | yukle-8 | evet | 8 |
| (yerel/yeni) | roblox-game-development-lifecycle | yukle-8 | evet | 6 |
| (yerel/yeni) | wpf-rule-mvvm-constraints | yukle-8 | evet | 8 |
| agent-skills | api-and-interface-design | yukle-8 | evet | 1 |
| agent-skills | browser-testing-with-devtools | yukle-8 | evet | 1 |
| agent-skills | ci-cd-and-automation | yukle-8 | evet | 1 |
| agent-skills | code-simplification | yukle-8 | evet | 2 |
| agent-skills | constraint-driven-development | yukle-8 | evet | 2 |
| agent-skills | context-engineering | yukle-8 | evet | 2 |
| agent-skills | doubt-driven-development | yukle-8 | evet | 3 |
| agent-skills | git-workflow-and-versioning | yukle-8 | evet | 3 |
| agent-skills | security-and-hardening | yukle-8 | evet | 6 |
| agent-skills | shipping-and-launch | yukle-8 | evet | 6 |
| agent-skills | source-driven-development | yukle-8 | evet | 6 |
| andrej-karpathy-skills | karpathy-guidelines | yukle-8 | evet | 4 |
| claude-api | messages-api-sdk | yukle-8b · ret: "reserved word 'claude'" → zip içi ad `messages-api-sdk` | evet | 1 |
| claude-md-management | memory-md-improver | yukle-8b · ret: "reserved word 'claude'" → zip içi ad `memory-md-improver` | evet | 1 |
| claude-mem | babysit | yukle-8 | hayır | 1 |
| claude-mem | ccs-align | yukle-8 | hayır | 1 |
| claude-mem | cloud-sync | yukle-8 | hayır | 2 |
| claude-mem | design-is | yukle-8 | evet | 2 |
| claude-mem | do | yukle-8 | evet | 3 |
| claude-mem | how-it-works | yukle-8 | evet | 4 |
| claude-mem | knowledge-agent | yukle-8 | evet | 4 |
| claude-mem | learn-codebase | yukle-8 | evet | 4 |
| claude-mem | make-plan | yukle-8 | evet | 4 |
| claude-mem | mem-search | yukle-8 | evet | 4 |
| claude-mem | mode-creator | yukle-8 | evet | 4 |
| claude-mem | oh-my-issues | yukle-8 | evet | 4 |
| claude-mem | pathfinder | yukle-8 | evet | 5 |
| claude-mem | smart-explore | yukle-8 | evet | 6 |
| claude-mem | standup | yukle-8 | hayır | 6 |
| claude-mem | timeline-report | yukle-8 | hayır | 7 |
| claude-mem | version-bump | yukle-8 | evet | 7 |
| claude-mem | weekly-digests | yukle-8 | hayır | 8 |
| claude-mem | what-the | yukle-8 | evet | 8 |
| claude-mem | wowerpoint | yukle-8b · ret: "description cannot contain XML tags" → description'daki `<file>` açılı parantezsiz | evet | 1 |
| claude-opus-4-5-migration | opus-4-5-migration | yukle-8b · ret: "reserved word 'claude'" → zip içi ad `opus-4-5-migration` | evet | 1 |
| design-mastery | design-principles | yukle-8 | evet | 2 |
| discernment-nudge | discernment-nudge | yukle-8 | evet | 3 |
| dotnet-aspnetcore | configuring-opentelemetry-dotnet | yukle-8 | evet | 2 |
| dotnet-aspnetcore | convert-blazor-server-to-webapp | yukle-8 | evet | 2 |
| dotnet-aspnetcore | dotnet-webapi | yukle-8 | evet | 3 |
| dotnet-aspnetcore | minimal-api-file-upload | yukle-8 | evet | 4 |
| dotnet-data | create-datadriven-aspnetcore | yukle-8 | evet | 2 |
| dotnet-data | optimizing-ef-core-queries | yukle-8 | evet | 5 |
| dotnet-msbuild | binlog-failure-analysis | yukle-8 | evet | 1 |
| dotnet-msbuild | binlog-generation | yukle-8 | evet | 1 |
| dotnet-msbuild | build-parallelism | yukle-8 | evet | 1 |
| dotnet-msbuild | build-perf-baseline | yukle-8 | evet | 1 |
| dotnet-msbuild | build-perf-diagnostics | yukle-8 | evet | 1 |
| dotnet-msbuild | check-bin-obj-clash | yukle-8 | evet | 1 |
| dotnet-msbuild | copy-to-output-directory | yukle-8 | evet | 2 |
| dotnet-msbuild | directory-build-organization | yukle-8 | evet | 3 |
| dotnet-msbuild | eval-performance | yukle-8 | evet | 3 |
| dotnet-msbuild | extension-points | yukle-8 | evet | 3 |
| dotnet-msbuild | including-generated-files | yukle-8 | evet | 4 |
| dotnet-msbuild | incremental-build | yukle-8 | evet | 4 |
| dotnet-msbuild | item-management | yukle-8 | evet | 4 |
| dotnet-msbuild | msbuild-antipatterns | yukle-8 | evet | 4 |
| dotnet-msbuild | msbuild-modernization | yukle-8 | evet | 4 |
| dotnet-msbuild | property-patterns | yukle-8 | evet | 6 |
| dotnet-msbuild | resolve-project-references | yukle-8 | evet | 6 |
| dotnet-msbuild | target-authoring | yukle-8 | evet | 7 |
| dotnet-nuget | convert-to-cpm | yukle-8 | evet | 2 |
| dotnet-test | assertion-quality | yukle-8 | evet | 1 |
| dotnet-test | code-testing-agent | yukle-8 | evet | 2 |
| dotnet-test | code-testing-extensions | yukle-8 | evet | 2 |
| dotnet-test | coverage-analysis | yukle-8 | evet | 2 |
| dotnet-test | crap-score | yukle-8 | evet | 2 |
| dotnet-test | detect-static-dependencies | yukle-8 | evet | 3 |
| dotnet-test | filter-syntax | yukle-8 | evet | 3 |
| dotnet-test | find-untested-sources | yukle-8 | evet | 3 |
| dotnet-test | generate-testability-wrappers | yukle-8 | evet | 3 |
| dotnet-test | grade-tests | yukle-8 | evet | 3 |
| dotnet-test | migrate-static-to-wrapper | yukle-8 | evet | 4 |
| dotnet-test | mtp-hot-reload | yukle-8 | evet | 4 |
| dotnet-test | platform-detection | yukle-8 | evet | 5 |
| dotnet-test | run-tests | yukle-8 | evet | 6 |
| dotnet-test | scaffold-dotnet-test-project | yukle-8 | evet | 6 |
| dotnet-test | test-analysis-extensions | yukle-8 | evet | 7 |
| dotnet-test | test-anti-patterns | yukle-8 | evet | 7 |
| dotnet-test | test-gap-analysis | yukle-8 | evet | 7 |
| dotnet-test | test-smell-detection | yukle-8 | evet | 7 |
| dotnet-test | test-tagging | yukle-8 | evet | 7 |
| dotnet-test | testability-obstacle | yukle-8 | evet | 7 |
| dotnet-test | writing-mstest-tests | yukle-8 | evet | 8 |
| everything-claude-code | backend-patterns | yukle-8 | evet | 1 |
| everything-claude-code | clickhouse-io | yukle-8 | evet | 2 |
| everything-claude-code | coding-standards | yukle-8 | evet | 2 |
| everything-claude-code | continuous-learning | yukle-8 | hayır | 2 |
| everything-claude-code | eval-harness | yukle-8 | evet | 3 |
| everything-claude-code | frontend-patterns | yukle-8 | evet | 3 |
| everything-claude-code | project-guidelines-example | yukle-8 | evet | 6 |
| everything-claude-code | security-review | yukle-8 | evet | 6 |
| everything-claude-code | strategic-compact | yukle-8 | hayır | 7 |
| everything-claude-code | tdd-workflow | yukle-8 | evet | 7 |
| everything-claude-code | verification-loop | yukle-8 | evet | 7 |
| example-skills | webapp-testing | yukle-8 | evet | 8 |
| hookify | writing-rules | yukle-8 | evet | 8 |
| nateherk-design | scroll-craft | yukle-8 | evet | 6 |
| phoenix-cti-search | cti-domain-research | yukle-8 | hayır | 2 |
| phoenix-docs-research | notebooklm | yukle-8 | evet | 4 |
| phoenix-docs-research | phoenix-research-pipeline | yukle-8 | evet | 5 |
| phoenix-docs-research | project-documenter | yukle-8 | evet | 6 |
| phoenix-prd-pipeline | phoenix-ambiguity-hunter | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-batch-planner | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-constraint-distiller | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-context-curator | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-contract-architect | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-final-gate | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-orchestrator | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-pipeline-navigator | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-requirements-engineer | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-scope-cutter | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-security-engineer | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | phoenix-verification-matrix | yukle-8 | evet | 5 |
| phoenix-prd-pipeline | prd-generator | yukle-8 | evet | 6 |
| phoenix-readiness-reviews | plan-readiness-review | yukle-8 | evet | 5 |
| phoenix-readiness-reviews | production-readiness-review | yukle-8 | evet | 6 |
| phoenix-sast-rules | opengrep-rule-generator | yukle-8 | evet | 5 |
| phoenix-sast-rules | opengrep-rule-generator-research | yukle-8 | evet | 5 |
| phoenix-security-review | 0day-scanner | yukle-8b · ret: "exactly one SKILL.md … there are 2" → `_ref/**/SKILL.md` → `SKILL.ref.md` | evet | 1 |
| phoenix-security-review | security-assessment | yukle-8 | evet | 6 |
| phoenix-security-review | security-reviewer | yukle-8 | evet | 6 |
| phoenix-security-review | threat-modeling | yukle-8 | evet | 7 |
| phoenix-security-review | tm-quick-security-assessment | yukle-8b · ret: "… there are 3" → `_ref/**/SKILL.md` → `SKILL.ref.md` | evet | 1 |
| phoenix-security-review | tm-security-review | yukle-8b · ret: "… there are 3" → `_ref/**/SKILL.md` → `SKILL.ref.md`; ayrıca description'daki `->` → `→` | evet | 1 |
| plugin-dev | agent-development | yukle-8 | evet | 1 |
| plugin-dev | command-development | yukle-8 | evet | 2 |
| plugin-dev | hook-development | yukle-8 | evet | 4 |
| plugin-dev | mcp-integration | yukle-8 | evet | 4 |
| plugin-dev | plugin-settings | yukle-8 | evet | 5 |
| plugin-dev | plugin-structure | yukle-8 | evet | 6 |
| plugin-dev | skill-development | yukle-8b · ret: "… there are 7" → `_ref/**/SKILL.md` → `SKILL.ref.md` | evet | 1 |
| supabase | supabase | yukle-8 | evet | 7 |
| supabase | supabase-postgres-best-practices | yukle-8 | evet | 7 |
| superpowers | brainstorming | yukle-8 | evet | 1 |
| superpowers | executing-plans | yukle-8 | evet | 3 |
| superpowers | finishing-a-development-branch | yukle-8 | hayır | 3 |
| superpowers | subagent-driven-development | yukle-8 | evet | 7 |
| superpowers | systematic-debugging | yukle-8 | kısmen | 7 |
| superpowers | using-superpowers | yukle-8 | evet | 7 |
| superpowers | writing-skills | yukle-8 | evet | 8 |
| taste-skill | design-taste-frontend | yukle-8 | evet | 3 |
| taste-skill | imagegen-frontend-web | yukle-8 | evet | 4 |

## MCP tablosu

| MCP | yöntem | durum |
|---|---|---|
| code-review | KURULUM-7 M21'den; `uvx code-review-mcp@2.0.0`, `GITHUB_TOKEN` User env var'ı tanımlı | **✔** (uyarı: GITLAB_TOKEN boş — kasıtlı) |
| obsidian | **`claude mcp add` yok.** Eklenti WebSocket ile otomatik keşfediliyor: Ömer Obsidian'ı açar, CC'de `/ide` ile kasayı seçer | eklenti kuruldu, bağlantı Ömer'in `/ide` adımında |
| stitch | gcloud'lu M3 girdisi kaldırıldı; `claude mcp add stitch -s user -e 'STITCH_API_KEY=${STITCH_API_KEY}' -- cmd /c npx -y @_davideast/stitch-mcp@0.9.0 proxy` (0.9.0 npm'de güncel). gcloud kurulmadı | **✔** |
| omniroute | ✘ girdi kaldırıldı; `npm.cmd i -g omniroute@3.8.50` + `claude mcp add omniroute -s user -- cmd /c omniroute --mcp` | **✔** (2 deneme) |
| playwright (plugin) | dokunulmadı | **✔** — KURULUM-7'deki ✘ kendiliğinden düzelmiş, teşhis gerekmedi |
| mem-search (claude-mem plugin) | dokunulmadı | **✔** |

**omniroute kök nedeni:** `npx -y omniroute --mcp` paketi her açılışta kurmaya çalışıyor (rc=1) ve `[DB] Sync driver … failed` satırlarını **stdout'a** basıp JSON-RPC akışını bozuyordu. Global kurulum ikisini de çözdü. Native postinstall script'leri (`better-sqlite3`, `keytar`, `esbuild`…) engelli kaldı — sunucu bu uyarılarla da bağlanıyor. Ayrı OmniRoute sunucusu gerekmiyor; HTTP yolu (`http://localhost:20128/api/mcp/stream`) kullanılmadı, Windows servisi/otomatik başlatma kurulmadı, `ANTHROPIC_BASE_URL` ve `settings.json` env'e dokunulmadı.

## CC araçları

| araç | yapılan | doğrulama |
|---|---|---|
| playwright-cli | `npm install -g @playwright/cli@latest` → 0.1.21 | `playwright-cli --version` exit 0 |
| playwright-core | `C:\Users\pc\Desktop\Portale` (scrollcraft'ın proje kökü) zaten `playwright-core@^1.63.0` devDependency'si taşıyor; npm "up to date" dedi, dosya değişmedi | `node -e "require('playwright-core')"` exit 0 |
| pixeljury | `npm.cmd i -g pixeljury@0.1.5` (MIT) | `pixeljury --help` exit 0 |
| skill-ui | **kurulamadı** — README `npm install -g skill-ui` diyor ama paket 2023'te npm'den kaldırılmış (404), GitHub release yok, repoda lisans yok → lisans kapısı zaten REF diyor | `omer-kutuphaneler` REF satırında |
| Obsidian | `winget install Obsidian.Obsidian` → 1.13.7; kasa `C:\Users\pc\Desktop\Obsidian` açıldı | kurulu |
| obsidian-claude-code-mcp | release 1.1.8 (0BSD): `main.js`, `manifest.json`, `styles.css` → `kasa\.obsidian\plugins\claude-code-mcp\`; `community-plugins.json` → `["claude-code-mcp"]` | dosyalar yerinde |

## claude-mem (yerel motor; cowork bağlanmadı)

**worker ✔** (pid 32984, port 37777, `/health` → `{"status":"ok","activeSessions":1}`, `observer-health.json` 0 ardışık hata) · **103 gözlem** (hepsi 19 Eyl'den sonra; 5 oturum özeti, 178 tool_use, 9 SDK oturumu) · `mem-search` MCP ✔ · onarım gerekmedi.

**Ölçüm** (ayar değiştirilmedi, `claude -p` çağrısı yok):

- **SessionStart enjeksiyonu ~10.160 karakter ≈ 2.540 token/oturum** (45 gözlem satırı 4.759 + 5 oturum başlığı 942 + son özetin tam metni 3.707 + ~750 sabit başlık/legend).
- **PreToolUse Read file-context**: toplam 4 enjeksiyon (bu oturumda 3: kurulum-7.md, claude-ai-mcp.md, skill_denetim.py), her biri ~450 karakter ≈ **~110 token**.
- **Worker'ın Agent SDK çağrısı / oturum** (log'dan, yanıt karakteri ÷4): session-7 1 çağrı ~12 tok · session-8 4 çağrı ~41 tok · session-9 (bu oturum, sürüyor) 80 çağrı ~29.350 tok. İstek tarafı log'da karakter sayısıyla tutulmuyor.
- **Faturalama**: `observed_billing=max`, `CLAUDE_MEM_CLAUDE_AUTH_METHOD=subscription` → worker Ömer'in Max aboneliğinden çalışıyor, ek API ücreti yok.

**Sağlayıcı ayarı — dosya `C:\Users\pc\.claude-mem\settings.json`, değiştirilmedi:**
`CLAUDE_MEM_PROVIDER = claude` · `CLAUDE_MEM_MODEL = claude-haiku-4-5-20251001` · `CLAUDE_MEM_CLAUDE_AUTH_METHOD = subscription` · Gemini/OpenRouter anahtarları boş · **`CLAUDE_MEM_CONTEXT_OBSERVATIONS = 50`** (bağlam gözlem sayısı) · `CLAUDE_MEM_CONTEXT_SESSION_COUNT = 10` · `CLAUDE_MEM_CONTEXT_SHOW_LAST_SUMMARY = true`.

`claude-mem-cowork` plugin'ine dokunulmadı (anahtarsız pasif), `CMEM_API_KEY` tanımlanmadı.

## Kurulmayanlar

- **nano-banana-2 anahtarı** — Gemini API ücretsiz katmanında görsel üretimi yok.
- **headroom-desktop** — ücretli abonelik (7 gün deneme); Headroom CLI + MCP zaten kurulu.
- **claude-mem-cowork** — CMEM Cloud ücretli; Ömer kararı. Plugin pasif duruyor, skill'leri yukle-8'e girmedi.
- **github Docker alternatifi** — http taşıması çalışıyor, Docker gerekmiyor.
- **Burhan PDF kiti** — dosya bekleniyor.
- **gstack paketi** — 7f kararı (CC native v1.87.4.0 olarak duruyor).
- **skill-ui** — npm paketi yayından kaldırılmış, release yok, lisans yok.
- **gcloud** — stitch artık anahtarla çalışıyor, gerekmiyor.

## Sync sonrası tek blok — **ŞİMDİ KOŞMA**

yukle-8 **ve yukle-8b** claude.ai'ye yüklenip CC'ye sync olduktan sonra, plugin kopyası açık olan 148 ad için synced kopyayı kapatır (`omer-kutuphaneler` hariç — onun plugin kopyası yok):

```powershell
Add-Type -AssemblyName System.IO.Compression.FileSystem
$p = "$env:USERPROFILE\.claude\settings.json"
$s = Get-Content $p -Raw | ConvertFrom-Json
Get-ChildItem @("C:\Projeler\omer-skills\dist\yukle-8", "C:\Projeler\omer-skills\dist\yukle-8b") -Recurse -Filter *.zip | ForEach-Object {
  $z = [IO.Compression.ZipFile]::OpenRead($_.FullName)
  $ad = $z.Entries[0].FullName.Split('/')[0]
  $z.Dispose()
  if ($ad -ne 'omer-kutuphaneler') {
    $s.skillOverrides | Add-Member -NotePropertyName "anthropic-skills:$ad" -NotePropertyValue 'off' -Force
  }
}
[IO.File]::WriteAllText($p, ($s | ConvertTo-Json -Depth 30), (New-Object Text.UTF8Encoding $false))
```

## 8c doğrulama

Sync-off bloğu koşuldu: synced 149/149, `skillOverrides` off **73 → 221** (+148, hepsi `anthropic-skills:`; `.bak8s` farkıyla doğrulandı, kalkan override yok). Ölçüm: `claude -p /context` (2 çağrı) + dosya envanteri.

- **a) Aktif kopyası sıfır kalan 17 ad**, üç nedenle — hiçbiri 7b tabanına göre gerileme değil, üçü de 8'den önce de listede değildi:
  1. *Plugin kapalı* (`enabledPlugins:false`), synced kopya off → tek çare synced'i geri açmak (8 ad): `plugin-dev` → agent-development · command-development · hook-development · mcp-integration · plugin-settings · plugin-structure · skill-development; `claude-md-management` → memory-md-improver (kaynak adı claude-md-improver).
  2. *Yerel kopya bare-ad override ile off* (3 ad): hetzner-deploy · roblox-game-development-lifecycle · wpf-rule-mvvm-constraints. Bunlarda `anthropic-skills:<ad>` kaldırmak yetmez — bare-ad override synced kopyayı da kapatıyor (kanıt: docx/pdf/pptx/xlsx/import-memory/morning yalnız bare override'la off ve `/context`'te yoklar). Kapalılık 8'den önce, kasıtlı (PERSONAL listesi) → bloğa alınmadı.
  3. *Plugin kopyası CC'ye hiç kayıtlı değil* (6 ad): `user-invocable: false` → dotnet-test'in code-testing-extensions · filter-syntax · test-analysis-extensions; frontmatter'sız SKILL.md → everything-claude-code'un eval-harness · project-guidelines-example · verification-loop. Referans dosyalar; bloğa alınmadı.
- **b) Aktif kopyası ≥2 olan 10 ad:** algorithmic-art · brand-guidelines · doc-coauthoring · internal-comms · slack-gif-creator · writing-plans (plugin + synced); frontend-design · skill-creator · test-driven-development · mem-search (iki plugin). Yalnız mem-search 148'in içinde.
- **c) Aktif toplam 397** (`/context`, 35.5k token) = 351 disk kopyası + 36 plugin slash-komutu + 11 yerleşik. Dosya envanteri 363 ham kopya sayıyor; fark 12+1: 6 bare-ad override'ın synced kopyayı da kapatması, 6 kayıtsız plugin skill'i (yukarıda), 1 hookify ad farkı (`writing-rules` ↔ `Writing Hookify Rules`). Beklenen 396'ya göre **+1 = omer-kutuphaneler**; Ömer'in oturumundaki 401 bu ortamda üretilemedi, 4 fark doğrulanamadı.
- **d) Aktif skill name+description = 112.435 karakter / SLASH_COMMAND_TOOL_CHAR_BUDGET 106.983 = %105,1.** Bütçe aşılmış görünüyor ama `/context` "excluded" uyarısı basmıyor — eşik bu değerle uygulanmıyor.

### (a.1) için tek blok — PowerShell

```powershell
$p = "$env:USERPROFILE\.claude\settings.json"
Copy-Item $p "$p.bak8c"
$s = Get-Content $p -Raw | ConvertFrom-Json
"Once off: " + ($s.skillOverrides.PSObject.Properties | Where-Object { $_.Value -eq 'off' }).Count
@('agent-development','command-development','hook-development','mcp-integration',
  'plugin-settings','plugin-structure','skill-development','memory-md-improver') | ForEach-Object {
  $s.skillOverrides.PSObject.Properties.Remove("anthropic-skills:$_")
}
[IO.File]::WriteAllText($p, ($s | ConvertTo-Json -Depth 30), (New-Object Text.UTF8Encoding $false))
$s2 = Get-Content $p -Raw | ConvertFrom-Json
"Sonra off: " + ($s2.skillOverrides.PSObject.Properties | Where-Object { $_.Value -eq 'off' }).Count
```
