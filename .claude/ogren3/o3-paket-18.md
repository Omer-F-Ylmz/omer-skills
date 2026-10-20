## wayfinder
id: k04060 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04060_wayfinder.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · wayfinder
BAŞLIKLAR: 

## skill-development
id: k03004 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03004_skill-development.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\plugin-dev\c2bdb427efe8\skills\skill-development\SKILL.md) · 637 satır · araç adları (1): skill-development
BAŞLIKLAR: # Skill Development for Claude Code Plugins · ## About Skills · ### What Skills Provide · ### Anatomy of a Skill · #### SKILL.md (required) · #### Bundled Resources (optional) · ##### Scripts (`scripts/`) · ##### References (`references/`) · ##### Assets (`assets/`) · ### Progressive Disclosure Design Principle · ## Skill Creation Process · ### Step 1: Understanding the Skill with Concrete Examples · ### Step 2: Planning the Reusable Skill Contents · ### Step 3: Create Skill Structure · ### Step 4: Edit the Skill · #### Start with Reusable Skill Contents · #### Update SKILL.md · ## Additional Resources · ### Reference Files · ### Example Files · ### Step 5: Validate and Test · ### Step 6: Iterate · ## Plugin-Specific Considerations · ### Skill Location in Plugins · ### Auto-Discovery · ### No Packaging Needed · ### Testing in Plugins · # Test with --plugin-dir · # Ask questions that should trigger the skill · # Verify skill loads correctly · ## Examples from Plugin-Dev · ## Progressive Disclosure in Practice · ### What Goes in SKILL.md · ### What Goes in references/ · ### What Goes in examples/ · ### What Goes in scripts/ · ## Writing Style Requirements · ### Imperative/Infinitive Form · ### Third-Person in Description · ### Objective, Instructional Language · ## Validation Checklist · Before finalizing a skill: · ## Common Mistakes to Avoid · ### Mistake 1: Weak Trigger Description · ### Mistake 2: Too Much in SKILL.md · ### Mistake 3: Second Person Writing · ### Mistake 4: 

## gstack-upgrade
id: k00279 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00279_gstack-upgrade.txt (özgün: C:\Users\pc\.claude\skills\gstack-upgrade\SKILL.md) · 416 satır · araç adları (17): gstack-upgrade · migrations/v0.15.2.0.sh · migrations/v0.16.2.0.sh · migrations/v1.0.0.0.sh · migrations/v1.1.3.0.sh · migrations/v1.17.0.0.sh · migrations/v1.27.0.0.sh · migrations/v1.37.0.0.sh · migrations/v1.38.1.0.sh · migrations/v1.40.0.0.sh · migrations/v1.58.0.0.sh · migrations/v1.65.0.0.sh · migrations/v1.67.0.0.sh · migrations/v1.78.0.0.sh · migrations/v1.86.0.0.sh · migrations/v1.91.19.0.sh · migrations/v1.91.65.0.sh
BAŞLIKLAR: ## When to invoke this skill · # /gstack-upgrade · ## Inline upgrade flow · ### Step 1: Ask the user (or auto-upgrade) · ### Step 2: Detect install type · ### Step 3: Save old version · ### Step 4: Upgrade · # Discard render-footprint dirt: older gbrain-enabled instal · # generated SKILL.md / sections files IN PLACE. They are reg · # re-renders to ~/.gstack/render), so discarding is lossless · # Same pre-advance check as the auto-updater: the incoming r · # A stale .bak from a previously crashed upgrade would make  · # the live install inside it and the failure-restore arm wou · # stale backup. It may also be the only good copy from that  · # abort and let the human inspect, never delete it silently. · ### Step 4.5: Handle local vendored copy · ### Step 4.75: Run version migrations · ### Step 4.8: Stop any stale daemon (unconditional) · ### Step 5: Write marker + clear cache · ### Step 6: Show What's New · Format: · ### Step 7: Continue · ## Standalone usage

## santa-method
id: k02136 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02136_santa-method.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\santa-method\SKILL.md) · 307 satır · araç adları (1): santa-method
BAŞLIKLAR: # Santa Method · ## When to Activate · Invoke this skill when: · ## Architecture · ## Phase Details · ### Phase 1: Make a List (Generate) · # The generator runs as normal · ### Phase 2: Check It Twice (Independent Dual Review) · ## Task Specification · ## Output Under Review · ## Evaluation Rubric · ## Instructions · # Spawn reviewers in parallel (Claude Code subagents) · # Both run concurrently — neither sees the other · ### Rubric Design · #### Domain-Specific Rubric Extensions · ### Phase 3: Naughty or Nice (Verdict Gate) · ### Phase 4: Fix Until Nice (Convergence Loop) · # Exhausted iterations — escalate · ## Implementation Patterns · ### Pattern A: Claude Code Subagents (Recommended) · # In a Claude Code session, use the Agent tool to spawn revi · # Both agents run in parallel for speed · # Pseudocode for Agent tool invocation · ### Pattern B: Sequential Inline (Fallback) · ### Pattern C: Batch Sampling · ## Failure Modes and Mitigations · ## Integration with Other Skills · ## Metrics · ## Cost Analysis

## skill_denetim
id: k03480 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03480_skill_denetim.txt (özgün: C:\Projeler\omer-skills\tools\skill_denetim.py) · 236 satır · araç adları (1): skill_denetim
BAŞLIKLAR: # (zip deseni, tür, öğe deseni, gerekçe) — tür "yol": SKILL. · # "@": gstack playwright-core@1.62.1.patch ile claude.ai "in · # 8: ~/.claude-mem ayrı bir dizin, eşleşmemeli; yalnız CC ev · # 9c: claude.ai gstack paketi -- dosyalar 644, kabuk durumu  · # 7b: md/txt sayılmaz; öteki shebang'li betik uyarı, SKILL.m

## unified-notifications-ops
id: k02176 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02176_unified-notifications-ops.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\unified-notifications-ops\SKILL.md) · 188 satır · araç adları (1): unified-notifications-ops
BAŞLIKLAR: # Unified Notifications Ops · ## When to Use · ## Preferred Surface · Start from what already exists: · ## Non-Negotiable Rules · ## Event Pipeline · Treat the lane as: · ## Default Severity Model · ## Workflow · ### 1. Inventory the current surface · List: · ### 2. Decide what deserves interruption · Use these defaults: · ### 3. Collapse duplicates before adding channels · Look for: · Prefer: · ### 4. Design the ECC-native workflow · ### 5. Return an action-biased design · End with: · ## Output Format · ## Recommendation Rules · ## Good Use Cases · ## Related Skills

## skill-council
id: k02741 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02741_skill-council.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\skills\skill-council\SKILL.md) · 132 satır · araç adları (1): skill-council
BAŞLIKLAR: # Council · ## EXECUTION CONTRACT: MANDATORY · ## Phase 0A: Interactive Clarification · Default council clarification: · Translate answers as follows: · ## Phase 0: Preflight · Collect or infer: · ## Quorum · ## Council Procedure · ## Implementation Gates · ## Interactive Choice Handling

## phoenix-scope-cutter
id: k02973 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02973_phoenix-scope-cutter.txt (özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-prd-pipeline\1.0.0\skills\phoenix-scope-cutter\SKILL.md) · 103 satır · araç adları (1): phoenix-scope-cutter
BAŞLIKLAR: # Phoenix Security — Scope Cutter (Role 02) · ## Phoenix Scope Anchors · ## Team Constraint · ## Success Metric Benchmarks · ## Core Rules · ## Output Schema · ### SCOPE_DEFINITION · #### GOALS (max 6) · #### NON_GOALS (max 6) · #### IN_SCOPE (max 10) · #### OUT_OF_SCOPE (max 10) · #### ASSUMPTIONS (max 6; map to FACT/DECISION IDs) · #### SUCCESS_METRICS (max 5; quantified where possible) · #### SCOPE_OPEN_QUESTIONS (max 7; blockers only) · #### ENTERPRISE_FLAGS (only if active accounts affected) · ## Chaining

## parallel
id: k02811 · tür: komut · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02811_parallel.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\commands\parallel.md) · 68 satır · araç adları (1): parallel
BAŞLIKLAR: # Parallel - Team of Teams · ## INSTRUCTIONS FOR CLAUDE · ## Quick Usage · ## What Is Parallel? · ## What You Get · ## When To Use · ## Natural Language Examples

## ponytail
id: k03010 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03010_ponytail.txt (özgün: C:\Users\pc\.claude\plugins\cache\ponytail\ponytail\5.2.0\skills\ponytail\SKILL.md) · 52 satır · araç adları (1): ponytail
BAŞLIKLAR: # Ponytail · ## Before you write · ## The smallest complete change · ## Levels

## claude-opus-4-5-migration
id: k01572 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01572_claude-opus-4-5-migration.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-code-plugins\claude-opus-4-5-migration\1.0.0) · 34 satır · araç adları (2): 1.0 · claude-opus-4-5-migration
BAŞLIKLAR: # Claude Opus 4.5 Migration Plugin · ## Overview · ## Usage · ## Learn More · ## Authors

## git-ci-boru-hatti
id: k00951 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00951_git-ci-boru-hatti.txt (özgün: C:\Users\pc\.claude\agents\git-ci-boru-hatti.md) · 24 satır · araç adları (1): git-ci-boru-hatti
BAŞLIKLAR: ## Ders bankası · Kurallar:

## pln-fikir-olgunlastir
id: k01081 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01081_pln-fikir-olgunlastir.txt (özgün: C:\Users\pc\.claude\agents\pln-fikir-olgunlastir.md) · 19 satır · araç adları (1): pln-fikir-olgunlastir
BAŞLIKLAR: Kurallar:

## model-sec
id: k03594 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03594_model-sec.txt (özgün: C:\Projeler\omer-skills\dist\router-1\model-sec.zip!model-sec/SKILL.md) · 14 satır · araç adları (2): model-sec · model-sec.zip!model-sec
BAŞLIKLAR: # model-sec
