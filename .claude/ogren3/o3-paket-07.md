## sdp
id: k03918 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03918_sdp.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · sdp
BAŞLIKLAR: 

## land-and-deploy
id: k00326 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00326_land-and-deploy.txt (özgün: C:\Users\pc\.claude\skills\land-and-deploy\SKILL.md) · 1036 satır · araç adları (1): land-and-deploy
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Repo Ownership — See Something, Say Something · ## Search Before Building · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · ## Third-Party Web Actions · ## BROWSER SETUP (Aside — run this check BEFORE any browser  · ### Rules for driving a real browser · ## Browser fallback: gstack's own headless browser · ### Find the `$B` binary · ### Translate the Aside scripts step by step · ### What changes without Aside · ## Step 0: Detect platform and base branch · # /land-and-deploy — Merge, Deploy, Verify · ## User-invocable · ## Arguments · ## Automation and approval · ## Voice & Tone · ## Section index — Read each section when its situation appl · ## Step 1: Pre-flight · ## Step 1

## plugin-settings
id: k03002 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03002_plugin-settings.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\plugin-dev\c2bdb427efe8\skills\plugin-settings\SKILL.md) · 544 satır · araç adları (4): examples/read-settings-hook.sh · plugin-settings · scripts/parse-frontmatter.sh · scripts/validate-settings.sh
BAŞLIKLAR: # Plugin Settings Pattern for Claude Code Plugins · ## Overview · ## File Structure · ### Basic Template · # Additional Context · This markdown body can contain: · ### Example: Plugin State File · # Plugin Configuration · ## Reading Settings Files · ### From Hooks (Bash Scripts) · # Define state file path · # Quick exit if file doesn't exist · # Parse YAML frontmatter (between --- markers) · # Extract individual fields · # Check if enabled · # Use configuration in hook logic · ### From Commands · # Process Command · Steps: · ### From Agents · ## Parsing Techniques · ### Extract Frontmatter · # Extract everything between --- markers · ### Read Individual Fields · # Compare: if [[ "$ENABLED" == "true" ]]; then · # Use: if [[ $MAX -gt 100 ]]; then · ### Read Markdown Body · # Get everything after closing --- · ## Common Patterns · ### Pattern 1: Temporarily Active Hooks · # Quick exit if not configured · # Read enabled flag · # Run hook logic · # ... · ### Pattern 2: Agent State Management · # Task Assignment · # Send notification to coordinator · ### Pattern 3: Configuration-Driven Behavior · # Validation Configuration · Use in hooks or commands: · ## Creating Settings Files · ### From Commands · # Setup Command · Steps: · ### Template Generation · ## Configuration · # Plugin Configuration · ## Best Practices · ### File Naming · ### Gitignore · ### Defaults · ### Validation · Validate settings values: · # Validate numeric range · ### Restart Requirement · Document in your READM

## intent-driven-development
id: k02027 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02027_intent-driven-development.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\intent-driven-development\SKILL.md) · 360 satır · araç adları (1): intent-driven-development
BAŞLIKLAR: # Intent-Driven Development · ## When to Activate · ## How It Works · ## Examples · ## Operating Rules · ## Choose The Depth · ### Quick Capture · ### Full Acceptance Brief · ### Existing Specification Review · ## Workflow · ### 1. Establish Goal And Risk · Extract or ask for: · ### 2. Discover Context · ### 3. Define Scope · State: · ### 4. Write Acceptance Criteria · ### 5. Cover Only Relevant Boundaries · ### 6. Present And Continue · ## Output Template · # Acceptance Brief: <Change Name> · ## Revision Log · ## Goal · ## Scope · ## Context · ## Risk Review · ## Acceptance Criteria · ### AC-001: <observable behavior> · ## Blocking Decisions · ## Verification Plan · ## Pass/Fail Examples · ### Pass/Fail Rubric · ## Quality Check · ## Handoff

## rules-distill
id: k03679 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03679_rules-distill.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\ecc-rules-distill.zip!rules-distill/SKILL.md) · 265 satır · araç adları (2): ecc-rules-distill.zip!rules-distill · rules-distill
BAŞLIKLAR: # Rules Distill · ## When to Use · ## How It Works · ### Phase 1: Inventory (Deterministic Collection) · #### 1a. Collect skill inventory · #### 1b. Collect rules index · #### 1c. Present to user · ### Phase 2: Cross-read, Match & Verdict (LLM Judgment) · #### Batching · #### Cross-batch Merge · #### Subagent Prompt · ## Input · ## Extraction Criteria · ## Matching & Verdict · ## Output Format (per candidate) · ## Exclude · #### Verdict Reference · #### Verdict Quality Requirements · # Good · # Bad · ### Phase 3: User Review & Execution · #### Summary Table · # Rules Distillation Report · ## Summary · ## Details · #### User Actions · User responds with numbers to: · #### Save Results · ## Example · ### End-to-end run · # Rules Distillation Report · ## Summary · ## Details · ### 1. LLM Output Validation · Draft: · ## Design Principles

## plan_kur
id: k03469 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03469_plan_kur.txt (özgün: C:\Projeler\omer-skills\tools\plan_kur.py) · 215 satır · araç adları (1): plan_kur
BAŞLIKLAR: # tür: (tanıma deseni [TR→ASCII küçük harf], kapılar, incele · # araç → faz (ad + iş metninde ilk eşleşen; hiçbiri değilse  · # sayısal kapılar: (iş deseni, faz, kapı). ENVANTER-3 kör ya

## council-multi-model
id: k01951 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01951_council-multi-model.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\council-multi-model\SKILL.md) · 167 satır · araç adları (2): council-multi-model · scripts/review-with-codex.js
BAŞLIKLAR: # Council - External Review · ## When to Activate · ## Provider Relationship · ## Workflow · ### 1. Finish the normal council draft · ### 2. Build the minimum review packet · Answer only: · ### 3. Ask for transfer consent · ### 4. Run the bounded adapter · ### 5. Present without hiding disagreement · ## Council with optional external critique: [decision] · ### Raw positions · ### Council synthesis draft · ### [cross-provider external critique | same-provider extern · ### Over to you · ## Persistence · ## Related

## phoenix-requirements-engineer
id: k02972 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02972_phoenix-requirements-engineer.txt (özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-prd-pipeline\1.0.0\skills\phoenix-requirements-engineer\SKILL.md) · 119 satır · araç adları (1): phoenix-requirements-engineer
BAŞLIKLAR: # Phoenix Security — Requirements Engineer (Role 04) · ## Requirement ID Schema · ## Priority Tags · ## Integration Requirements (check when in scope) · ## Performance Benchmarks (use for R-PERF) · ## Core Rules · ## Output Schema · ### NORMATIVE_REQUIREMENTS · #### DEFINITIONS (max 8; only if needed) · #### FUNCTIONAL_REQUIREMENTS · #### INTEGRATION_REQUIREMENTS (if integrations in scope) · #### RELIABILITY_REQUIREMENTS · #### PERFORMANCE_REQUIREMENTS (if applicable) · #### UX_DX_REQUIREMENTS (if applicable) · #### COMPLIANCE_REQUIREMENTS (if applicable) · #### OPEN_QUESTIONS (max 10; blockers only) · ## Stop Conditions · ## Chaining

## scheduler
id: k02824 · tür: komut · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02824_scheduler.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\commands\scheduler.md) · 95 satır · araç adları (1): scheduler
BAŞLIKLAR: # Scheduler · ## MANDATORY COMPLIANCE — DO NOT SKIP · ## Usage · ## Instructions for Claude · ### Step 1: Parse Intent · ### Step 2: Display Banner · Providers: · ### Step 3: Execute and Present · ### Natural Language Examples

## superpowers-using-superpowers
id: k03756 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03756_superpowers-using-superpowers.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\superpowers-superpowers-using-superpowers.zip!superpowers-using-superpowers/SKILL.md) · 64 satır · araç adları (2): superpowers-superpowers-using-superpowers.zip!superpowers-using-superpowers · superpowers-using-superpowers
BAŞLIKLAR: ## The Rule · ## Skill Priority · ## Red Flags · ## Platform Adaptation · ## User Instructions

## git
id: k04249 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04249_git.txt (özgün: C:\Program Files\Git\mingw64\bin\git.EXE) · 47 satır · araç adları (1): git
BAŞLIKLAR: 

## ajn-codex-claude-koprusu
id: k00663 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00663_ajn-codex-claude-koprusu.txt (özgün: C:\Users\pc\.claude\agents\ajn-codex-claude-koprusu.md) · 29 satır · araç adları (1): ajn-codex-claude-koprusu
BAŞLIKLAR: # Work protocol · Kurallar:

## git-canary-izleme
id: k00950 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00950_git-canary-izleme.txt (özgün: C:\Users\pc\.claude\agents\git-canary-izleme.md) · 22 satır · araç adları (1): git-canary-izleme
BAŞLIKLAR: ## Ders bankası · Kurallar:

## pln-bagimlilik-haritasi
id: k01078 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01078_pln-bagimlilik-haritasi.txt (özgün: C:\Users\pc\.claude\agents\pln-bagimlilik-haritasi.md) · 18 satır · araç adları (1): pln-bagimlilik-haritasi
BAŞLIKLAR: Kurallar:

## mcp-launch
id: k03456 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03456_mcp-launch.txt (özgün: C:\Projeler\omer-skills\tools\mcp-launch) · 0 satır · araç adları (3): _trace.cjs · claude-mem-mcp.js · mcp-launch
BAŞLIKLAR: 
