## cli-models
id: k03789 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03789_cli-models.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · cli-models
BAŞLIKLAR: 

## gstack-review
id: k03866 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03866_gstack-review.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · gstack-review
BAŞLIKLAR: 

## codebase-design
id: k03964 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03964_codebase-design.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · codebase-design
BAŞLIKLAR: 

## codex
id: k00120 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00120_codex.txt (özgün: C:\Users\pc\.claude\skills\codex\SKILL.md) · 900 satır · araç adları (1): codex
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Repo Ownership — See Something, Say Something · ## Search Before Building · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · ## Step 0: Detect platform and base branch · # /codex — Multi-AI Second Opinion · ## Section index — Read each section when its situation appl · ## Step 0.4: Check codex binary · ## Step 0.5: Auth probe + model probe + version check · # GSTACK_ACTIVE_HOST names the harness, never the model. · ## Step 0.6: Resolve portable roots · ## Step 1: Detect mode · ## Filesystem Boundary · ## Synthesis recommendation (REQUIRED) — all modes · ## Plan File Review Report · ### Detect the plan file · ### Generate the report · Produce this markdown table: · ## GSTACK R

## skill-doctor
id: k03706 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03706_skill-doctor.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\octo-skill-doctor.zip!skill-doctor/SKILL.md) · 434 satır · araç adları (2): octo-skill-doctor.zip!skill-doctor · skill-doctor
BAŞLIKLAR: # Environment Doctor · ## Overview · ## When to Use · ## The Process · ### Step 1: Resolve Plugin Root and Run Full Diagnostics · ### Step 2: Filter by Category (Optional) · ### Step 3: Check & Install Dependencies · ### Step 4: Verbose or JSON Output · # Detailed output for troubleshooting · # Machine-readable output · # Combine: specific category + verbose · ### Step 5: Interactive Remediation (MANDATORY for fixable i · ## Check Categories · ## Interpreting Results · ### Healthy Output · ### Common Issues and Fixes · ## Integration with Other Skills · ## Context and intensity profiles · ## Legacy intensity profile · ### What the Doctor Checks · ### Legacy intensity summary · ### Optional context profile summary · ## Project Tier Hint · ## Remote Session Checks · ## Runtime Context · ### What the Doctor Checks · ### Why It Matters · ## Quick Reference

## superpowers-brainstorming
id: k03753 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03753_superpowers-brainstorming.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\superpowers-superpowers-brainstorming.zip!superpowers-brainstorming/SKILL.md) · 284 satır · araç adları (2): superpowers-brainstorming · superpowers-superpowers-brainstorming.zip!superpowers-brainstorming
BAŞLIKLAR: # Brainstorming Ideas Into Designs · ## Establish Shared Understanding · ## Three Paths · ## Anti-Pattern: "Too Simple To Need Approval" · ## Red Flags · ## Checklist · ## Process Flow · ## The Process · ## After the Design (architectural path) · ## Visual Companion

## build-mcpb
id: k02684 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02684_build-mcpb.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\mcp-server-dev\c2bdb427efe8\skills\build-mcpb\SKILL.md) · 199 satır · araç adları (1): build-mcpb
BAŞLIKLAR: # Build an MCPB (Bundled Local MCP Server) · ## What an MCPB bundle contains · ## Manifest · ## Server code: same as local stdio · ## Build pipeline · ### Node · # or: copy node_modules wholesale if native deps resist bund · ### Python · ## MCPB has no sandbox — security is on you · ## MCPB + UI widgets · ## Testing · # Interactive manifest creation (first time) · # Run the server directly over stdio, poke it with the inspe · # Validate manifest against schema, then pack · # Sign for distribution · # Install: drag the .mcpb file onto Claude Desktop · ## Reference files

## sync
id: k00577 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00577_sync.txt (özgün: C:\Users\pc\.claude\skills\sync\SKILL.md) · 146 satır · araç adları (1): sync
BAŞLIKLAR: ## Output style (plain words, no dashes, no hyphens) · ## What this skill does · ## Boundaries · ## Asks vs acts · ## Artifact ownership · ## Portability (any OS, any agent) · ## Execution · ### 1. Scope the change set (cheap, with per file status) · ### 2. Locate the context files and specs (paths only, do NO · ### 2.5 Discover Agent Skills and optional MCPs for newly ad · ### 3. Do the maintenance (main thread) · The inputs to apply: · ### 4. Relay the result · ## /sync complete Â· reconciled <N> changed files · ## Subagent prompt template

## katalog_kanca
id: k03437 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03437_katalog_kanca.txt (özgün: C:\Projeler\omer-skills\tools\katalog_kanca.py) · 108 satır · araç adları (1): katalog_kanca
BAŞLIKLAR: # liste B' ile aynı (katalog_ara varsayılanı ~95 aday, ~37k) · # CC 10k üstü additionalContext'i dosyaya yazıp 2k önizleme  · # katlanmış (ASCII, küçük harf) metinde kelime başı kalıplar

## voicestudio-maintainer
id: k00636 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00636_voicestudio-maintainer.txt (özgün: C:\Users\pc\.claude\skills\voicestudio-maintainer\SKILL.md) · 82 satır · araç adları (1): voicestudio-maintainer
BAŞLIKLAR: # VoiceStudio maintenance · ## Triage and implementation · ## Review and authorized landing · ## Release preparation · ## Communication · ## VoiceStudio-specific routing · ## Current development commands · Run from the repository root:

## check
id: k00107 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00107_check.txt (özgün: C:\Users\pc\.claude\skills\check\SKILL.md) · 52 satır · araç adları (1): check
BAŞLIKLAR: ## Output style (plain words, no dashes, no hyphens) · ## What this skill does · ## Pick the mode (route before doing anything else) · ## Portability (any OS, any agent)

## davila7-railway-paket
id: k00198 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00198_davila7-railway-paket.txt (özgün: C:\Users\pc\.claude\skills\davila7-railway-paket\SKILL.md) · 25 satır · araç adları (2): davila7-railway · davila7-railway-paket
BAŞLIKLAR: # davila7-railway-paket

## inc-karmasiklik-olcum
id: k00969 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00969_inc-karmasiklik-olcum.txt (özgün: C:\Users\pc\.claude\agents\inc-karmasiklik-olcum.md) · 20 satır · araç adları (1): inc-karmasiklik-olcum
BAŞLIKLAR: Kurallar:

## status
id: k01594 · tür: komut · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01594_status.txt (özgün: C:\Users\pc\.claude\plugins\cache\openai-codex\codex\1.0.6\commands\status.md) · 17 satır · araç adları (1): status
BAŞLIKLAR: If the user did pass a job ID:

## gsd-core-omer
id: k04216 · tür: repo · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04216_gsd-core-omer.txt (özgün: C:\Projeler\gsd-core-omer) · 0 satır · araç adları (1397): gsd-core-omer · kaynak/.kilo/plugins/gsd-core.js · kaynak/.opencode/plugins/gsd-core.js · kaynak/.release-monitor.sh · kaynak/bin/gsd-mcp-server.js · kaynak/bin/install.js · kaynak/eslint-rules/lib/platform-guard.cjs · kaynak/eslint-rules/lib/portability-vocab.cjs · kaynak/eslint-rules/lib/readfilesync-trace.cjs · kaynak/eslint-rules/no-adhoc-markdown-parsing.cjs · kaynak/eslint-rules/no-adhoc-regex-escape.cjs · kaynak/eslint-rules/no-adhoc-timeout-literal.cjs · kaynak/eslint-rules/no-bare-npm-exec.cjs · kaynak/eslint-rules/no-crlf-fragile-split.cjs · kaynak/eslint-rules/no-duplicate-fold-marker.cjs · kaynak/eslint-rules/no-elapsed-assertion.cjs · kaynak/eslint-rules/no-exact-case-env-access.cjs · kaynak/eslint-rules/no-external-require-in-bin.cjs · kaynak/eslint-rules/no-hardcoded-tmp.cjs · kaynak/eslint-rules/no-magic-sleep-in-tests.cjs · kaynak/eslint-rules/no-path-literal-in-assert.cjs · kaynak/eslint-rules/no-posix-mode-bit-assert.cjs · kaynak/eslint-rules/no-private-binary-resolution.cjs · kaynak/eslint-rules/no-raw-rmsync-in-tests.cjs · kaynak/eslint-rules/no-rendered-text-length-assert.cjs · kaynak/eslint-rules/no-runtime-name-literal.cjs · kaynak/eslint-rules/no-source-grep.cjs · kaynak/eslint-rules/no-swallowed-precondition.cjs · kaynak/eslint-rules/no-tautological-assert.cjs · kaynak/eslint-rules/no-unbounded-dirname-walk.cjs
BAŞLIKLAR: 
