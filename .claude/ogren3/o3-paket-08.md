## skill-ui-cli
id: k03921 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03921_skill-ui-cli.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (3): claudeai_adlar · skill-ui · skill-ui-cli
BAŞLIKLAR: 

## plan-tune
id: k00460 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00460_plan-tune.txt (özgün: C:\Users\pc\.claude\skills\plan-tune\SKILL.md) · 1000 satır · araç adları (1): plan-tune
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · # /plan-tune — Question Tuning + Developer Profile (v1 obser · ## Step 0: Detect what the user wants · ## Consent + opt-in · ## 5-Q setup (post-consent, or via Setup gate) · ## Inspect profile · ## Review question log · ## Set a preference · ## Edit declared profile · ## Show gap · ## Stats · ## Recent auto-decisions · ## Audit unmarked questions · ## Dream cycle review · ## Dream cycle distill (manual trigger) · ## Important Rules

## landing-report
id: k00329 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00329_landing-report.txt (özgün: C:\Users\pc\.claude\skills\landing-report\SKILL.md) · 495 satır · araç adları (1): landing-report
BAŞLIKLAR: ## When to invoke this skill · # /landing-report — Version Queue Dashboard · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · ## Why this skill exists · ## Step 1: Detect platform and base branch · ## Step 2: Read current state · ## Step 3: Query the queue · ## Step 4: Render the dashboard · Render in this exact format: · ## Step 5: Suggest next action · ## Plan Mode

## git-workflow-and-versioning
id: k01338 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01338_git-workflow-and-versioning.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\git-workflow-and-versioning\SKILL.md) · 355 satır · araç adları (1): git-workflow-and-versioning
BAŞLIKLAR: # Git Workflow and Versioning · ## Overview · ## When to Use · ## Core Principles · ### Trunk-Based Development (Recommended) · ### 1. Commit Early, Commit Often · Work pattern: · Not this: · ### 2. Atomic Commits · # Good: Each commit is self-contained · # Bad: Everything mixed together · ### 3. Descriptive Messages · # Good: Explains intent · # Bad: Describes what's obvious from the diff · ### 4. Keep Concerns Separate · # Good: Separate concerns · # Bad: Mixed concerns · ### 5. Size Your Changes · ## Branching Strategy · ### Feature Branches · ### Branch Naming · ## Working with Worktrees · # Create a worktree for a feature branch · # Each worktree is a separate directory with its own branch · # Agents can work in parallel without interfering · # When done, merge and clean up · Benefits: · ## The Save Point Pattern · ## Change Summaries · CHANGES MADE: · POTENTIAL CONCERNS: · ## Pre-Commit Hygiene · Before every commit: · # 1. Check what you're about to commit · # 2. Ensure no secrets · # 3. Run tests · # 4. Run linting · # 5. Run type checking · Automate this with git hooks: · ## Handling Generated Files · ## Using Git for Debugging · # Find which commit introduced a bug · # Git checkouts midpoints; run your test at each to narrow d · # View what changed recently · # Find who last changed a specific line · # Search commit messages for a keyword · ## Release & Versioning · ### Semantic Versioning · ### Tag the release, and let the tag be the source of truth · ### Keep a ch

## planning-and-task-breakdown
id: k01344 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01344_planning-and-task-breakdown.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\planning-and-task-breakdown\SKILL.md) · 257 satır · araç adları (1): planning-and-task-breakdown
BAŞLIKLAR: # Planning and Task Breakdown · ## Overview · ## When to Use · ## The Planning Process · ### Step 1: Enter Plan Mode · ### Step 2: Identify the Dependency Graph · Map what depends on what: · ### Step 3: Slice Vertically · ### Step 4: Write Tasks · ## Task [N]: [Short descriptive title] · ### Step 5: Order and Checkpoint · Arrange tasks so that: · ## Checkpoint: After Tasks 1-3 · ## Task Sizing Guidelines · ## Output Files · ### Task List Target · ## Plan Document Template · # Implementation Plan: [Feature/Project Name] · ## Overview · ## Architecture Decisions · ## Task List · ### Phase 1: Foundation · ### Checkpoint: Foundation · ### Phase 2: Core Features · ### Checkpoint: Core Features · ### Phase 3: Polish · ### Checkpoint: Complete · ## Risks and Mitigations · ## Open Questions · ## Parallelization Opportunities · ## Common Rationalizations · ## Red Flags · ## Verification · ## See Also

## iterative-retrieval
id: k02032 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02032_iterative-retrieval.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\iterative-retrieval\SKILL.md) · 212 satır · araç adları (1): iterative-retrieval
BAŞLIKLAR: # Iterative Retrieval Pattern · ## When to Activate · ## The Problem · Standard approaches fail: · ## The Solution: Iterative Retrieval · ### Phase 1: DISPATCH · ### Phase 2: EVALUATE · Scoring criteria: · ### Phase 3: REFINE · ### Phase 4: LOOP · ## Practical Examples · ### Example 1: Bug Fix Context · ### Example 2: Feature Implementation · ## Integration with Agents · Use in agent prompts: · ## Best Practices · ## Related

## dispatching-parallel-agents
id: k03126 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03126_dispatching-parallel-agents.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\dispatching-parallel-agents\SKILL.md) · 167 satır · araç adları (1): dispatching-parallel-agents
BAŞLIKLAR: # Dispatching Parallel Agents · ## Overview · ## When to Use · ## The Pattern · ### 1. Identify Independent Domains · ### 2. Create Focused Agent Tasks · Each agent gets: · ### 3. Dispatch in Parallel · # All three run concurrently. · ### 4. Review and Integrate · When agents return: · ## Agent Prompt Structure · Good agent prompts are: · ## Common Mistakes · ## When NOT to Use · ## Real Example from Session · ## Verification · After agents return:

## phoenix-context-curator
id: k02967 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02967_phoenix-context-curator.txt (özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-prd-pipeline\1.0.0\skills\phoenix-context-curator\SKILL.md) · 116 satır · araç adları (1): phoenix-context-curator
BAŞLIKLAR: # Phoenix Security — Context Curator (Role 01) · ## Phoenix Domain Vocabulary (use consistently) · ## Phoenix Integration Surface · ## Task · ## Core Rules · ## Output Schema · ### CLEAN_CONTEXT · #### FACTS (max 12) · #### DECISIONS (max 8) · #### OPEN_QUESTIONS (max 10) · #### CONTRADICTIONS / LIKELY WRONG (max 8) · #### COMPETITOR_FLAGS (only if competitors appear) · ## Stop Conditions · ## Validation Checklist · ## Chaining

## requesting-code-review
id: k03130 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03130_requesting-code-review.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\requesting-code-review\SKILL.md) · 95 satır · araç adları (1): requesting-code-review
BAŞLIKLAR: # Requesting Code Review · ## When to Request Review · ## How to Request · ## Example · ## Common Rationalizations · ## Red Flags

## is-akisi
id: k03543 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03543_is-akisi.txt (özgün: C:\Projeler\omer-skills\dist\claude-ai-26\is-akisi.zip!is-akisi/SKILL.md) · 63 satır · araç adları (2): is-akisi · is-akisi.zip!is-akisi
BAŞLIKLAR: # İş akışı (bağlayıcı) · ## 0. Yasaklar · ## 1. İş başı (sırayla) · ## 2. Süreç ve kaynak · ## 3. Token (kalite düşmeden) · ### Token araç sırası · ## 4. Kalite kapısı · ## 5. Kayıt, devir, bölünme, bitiş

## handoff-protocols
id: k01715 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01715_handoff-protocols.txt (özgün: C:\Users\pc\.claude\plugins\cache\designer-skills\design-agent-orchestration\1.1.0\skills\handoff-protocols\SKILL.md) · 45 satır · araç adları (1): handoff-protocols
BAŞLIKLAR: # Handoff Protocols · ## Anatomy of a Handoff · Every handoff has: · ## Handoff Types · ## Context Transfer · ## Designing for the User · ## Handoff Anti-Patterns · ## Design Artefacts

## ajn-mcp-kurulum-denetci
id: k00665 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00665_ajn-mcp-kurulum-denetci.txt (özgün: C:\Users\pc\.claude\agents\ajn-mcp-kurulum-denetci.md) · 29 satır · araç adları (1): ajn-mcp-kurulum-denetci
BAŞLIKLAR: # Work protocol · Kurallar:

## how-it-works
id: k01547 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01547_how-it-works.txt (özgün: C:\Users\pc\.claude\plugins\cache\thedotmack\claude-mem\13.31.0\skills\how-it-works\SKILL.md) · 22 satır · araç adları (1): how-it-works
BAŞLIKLAR: # How claude-mem works · ## What it does · ## When it kicks in · ## Where data lives

## pln-risk-kaydi
id: k01095 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01095_pln-risk-kaydi.txt (özgün: C:\Users\pc\.claude\agents\pln-risk-kaydi.md) · 18 satır · araç adları (1): pln-risk-kaydi
BAŞLIKLAR: Kurallar:

## gsd-paket
id: k04189 · tür: repo · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04189_gsd-paket.txt (özgün: C:\Projeler\.tmp-kurulum6c-zip\gsd-paket) · 0 satır · araç adları (2): gsd · gsd-paket
BAŞLIKLAR: 
