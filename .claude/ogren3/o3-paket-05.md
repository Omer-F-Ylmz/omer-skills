## omni-webhooks
id: k03905 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03905_omni-webhooks.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · omni-webhooks
BAŞLIKLAR: 

## devex-review
id: k00220 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00220_devex-review.txt (özgün: C:\Users\pc\.claude\skills\devex-review\SKILL.md) · 1117 satır · araç adları (1): devex-review
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Repo Ownership — See Something, Say Something · ## Search Before Building · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · ## Step 0: Detect platform and base branch · ## BROWSER SETUP (Aside — run this check BEFORE any browser  · ### Rules for driving a real browser · ## Browser fallback: gstack's own headless browser · ### Find the `$B` binary · ### Translate the Aside scripts step by step · ### What changes without Aside · ### Cookbook (verified against Aside CLI 1.26 — use these sh · # /devex-review: Live Developer Experience Audit · ## DX First Principles · ## The Seven DX Characteristics · ## Cognitive Patterns — How Great DX Leaders Think · ## DX Scoring Rubric (0-10

## kalite3_hiz
id: k03433 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03433_kalite3_hiz.txt (özgün: C:\Projeler\omer-skills\tools\kalite3_hiz.py) · 552 satır · araç adları (1): kalite3_hiz
BAŞLIKLAR: Current definition:

## executing-plans
id: k03127 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03127_executing-plans.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\executing-plans\SKILL.md) · 373 satır · araç adları (1): executing-plans
BAŞLIKLAR: # Executing Plans · ## When to Use · ## The Process · ## Setup · ## The Task Loop · ### 1. Take the task · ### 2. Work the steps · ### 3. The completion contract · ### 4. Complete the task · ## Final Review · ## Finish · ## Common Rationalizations · ## Example Workflow · Rulings I made: · Deferred minors:

## omni-providers
id: k03745 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03745_omni-providers.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\omniroute-omni-providers.zip!omni-providers/SKILL.md) · 273 satır · araç adları (2): omni-providers · omniroute-omni-providers.zip!omni-providers
BAŞLIKLAR: ## Overview · ## Authentication · ## Endpoints · ### GET /api/providers · ### POST /api/providers · ### GET /api/providers/{id} · ### PATCH /api/providers/{id} · ### DELETE /api/providers/{id} · ### POST /api/providers/{id}/test · ### GET /api/providers/{id}/models · ### POST /api/providers/test-batch · ### POST /api/providers/validate · ### GET /api/providers/client · ### POST /api/providers/agy-auth/import · ### POST /api/providers/agy-auth/import-bulk · ### POST /api/providers/agy-auth/zip-extract · ### POST /api/providers/agy-auth/apply-local · ### GET /api/provider-nodes · ### POST /api/provider-nodes · ### PATCH /api/provider-nodes/{id} · ### DELETE /api/provider-nodes/{id} · ### POST /api/provider-nodes/validate · ### GET /api/provider-models · ## Payloads · ## Additional endpoints · ### POST /api/providers/{id}/refresh · ### GET /api/provider-metrics · ### GET /api/providers/health-matrix

## agent-sdk-dev
id: k01321 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01321_agent-sdk-dev.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-code-plugins\agent-sdk-dev\1.0.0) · 221 satır · araç adları (2): 1.0 · agent-sdk-dev
BAŞLIKLAR: # Agent SDK Development Plugin · ## Overview · ## Features · ### Command: `/new-sdk-app` · Or simply: · # → Creates a new Agent SDK project for a customer support a · # → Sets up TypeScript or Python environment · # → Installs latest SDK version · # → Verifies the setup automatically · ### Agent: `agent-sdk-verifier-py` · ### Agent: `agent-sdk-verifier-ts` · ## Workflow Example · # Set your API key · # Run your agent · ## Installation · ## Best Practices · ## Resources · ## Troubleshooting · ### Type errors in TypeScript project · ### Python import errors · ### Verification fails with warnings · ## Author · ## Version

## production-readiness-review
id: k02979 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02979_production-readiness-review.txt (özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-readiness-reviews\1.0.0\skills\production-readiness-review\SKILL.md) · 172 satır · araç adları (2): production-readiness-review · scripts/scan_repo.sh
BAŞLIKLAR: # Production readiness review · ## Phase 0 — Input contract · ## Phase 1 — Deterministic scan · ## Phase 2 — Requirement trace matrix · ## Phase 3 — Test integrity · ## Phase 4 — Blast radius · ## Phase 5 — Non-functional gates · ## Severity rubric · ## Output · ## Phase 6 — Remediation (only after the audit is emitted) · ## Re-runs

## diagnosing-superpowers
id: k03125 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03125_diagnosing-superpowers.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\diagnosing-superpowers\SKILL.md) · 120 satır · araç adları (1): diagnosing-superpowers
BAŞLIKLAR: # Diagnosing Superpowers · ## Overview · ## Workflow · ## Quick reference · ## Hard rules · ## Red Flags

## example-skills
id: k02384 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02384_example-skills.txt (özgün: C:\Users\pc\.claude\plugins\cache\anthropic-agent-skills\example-skills\dbd4588f9e10) · 98 satır · araç adları (79): dbd4588f9e10 · example-skills · skills/algorithmic-art/templates/generator_template.js · skills/claude-api/shared/evals/report/build-report-lite.mjs · skills/claude-api/shared/evals/report/runner-scaffold.mjs · skills/claude-api/shared/preserved-thinking-migration/drop_block_probe.py · skills/claude-api/shared/preserved-thinking-migration/prefix_diff.py · skills/docx/scripts/__init__.py · skills/docx/scripts/accept_changes.py · skills/docx/scripts/comment.py · skills/docx/scripts/merge_runs.py · skills/docx/scripts/office/helpers/__init__.py · skills/docx/scripts/office/helpers/pptx_chart.py · skills/docx/scripts/office/helpers/pptx_slide.py · skills/docx/scripts/office/helpers/pptx_theme.py · skills/docx/scripts/office/soffice.py · skills/docx/scripts/office/validate.py · skills/docx/scripts/office/validators/__init__.py · skills/docx/scripts/office/validators/base.py · skills/docx/scripts/office/validators/docx.py · skills/docx/scripts/office/validators/pptx.py · skills/docx/scripts/office/validators/redlining.py · skills/mcp-builder/scripts/connections.py · skills/mcp-builder/scripts/evaluation.py · skills/pdf/scripts/check_bounding_boxes.py · skills/pdf/scripts/check_fillable_fields.py · skills/pdf/scripts/convert_pdf_to_images.py · skills/pdf/scripts/create_validation_image.py · skills/pdf/scripts/extract_form_field_info.py · skills/pdf/scripts/extract_form_structure.py
BAŞLIKLAR: # Skills · # About This Repository · ## Disclaimer · # Skill Sets · # Try in Claude Code, Claude.ai, and the API · ## Claude Code · ## Claude.ai · ## Claude API · # Creating a Basic Skill · # My Skill Name · ## Examples · ## Guidelines · # Partner Skills

## using-superpowers
id: k03135 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03135_using-superpowers.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\using-superpowers\SKILL.md) · 65 satır · araç adları (1): using-superpowers
BAŞLIKLAR: ## The Rule · ## Skill Priority · ## Red Flags · ## Platform Adaptation · ## User Instructions

## skill-ui-desktop
id: k03385 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03385_skill-ui-desktop.txt (özgün: C:\Projeler\omer-skills\skills\skill-ui-desktop\SKILL.md) · 48 satır · araç adları (1): skill-ui-desktop
BAŞLIKLAR: # skill-ui — bu arac Claude Code'da kosar, Desktop'ta kosmaz · ## Kullanim (yalniz Claude Code'da) · ## Desktop'te ne yapilir · ## Desktop'ta cc-kopru koprusu varsa (KURULUM-11k) · Kurallar:

## ollama
id: k04259 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04259_ollama.txt (özgün: C:\Users\pc\AppData\Local\Programs\Ollama\ollama.EXE) · 31 satır · araç adları (1): ollama
BAŞLIKLAR: Usage: · Available Commands: · Flags:

## otm-tarayici-otomasyon
id: k01057 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01057_otm-tarayici-otomasyon.txt (özgün: C:\Users\pc\.claude\agents\otm-tarayici-otomasyon.md) · 23 satır · araç adları (1): otm-tarayici-otomasyon
BAŞLIKLAR: ## Ders bankası · Kurallar:

## ajn-slash-komut-yazar
id: k00672 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00672_ajn-slash-komut-yazar.txt (özgün: C:\Users\pc\.claude\agents\ajn-slash-komut-yazar.md) · 18 satır · araç adları (1): ajn-slash-komut-yazar
BAŞLIKLAR: Kurallar:

## mcp-sequential-thinking
id: k03317 · tür: mcp · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03317_mcp-sequential-thinking.txt (özgün: C:\Users\pc\.claude.json) · 5 satır · araç adları (2): .claude · mcp-sequential-thinking
BAŞLIKLAR: 
