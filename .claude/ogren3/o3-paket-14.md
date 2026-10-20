## grill-with-docs
id: k03993 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03993_grill-with-docs.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · grill-with-docs
BAŞLIKLAR: 

## skill-debate
id: k03705 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03705_skill-debate.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\octo-skill-debate.zip!skill-debate/SKILL.md) · 713 satır · araç adları (2): octo-skill-debate.zip!skill-debate · skill-debate
BAŞLIKLAR: # AI Debate Hub Skill v4.8 · ## MANDATORY COMPLIANCE — DO NOT SKIP · ## ⚠️ MANDATORY: Visual Indicators Protocol · Participants: · ## CRITICAL: External CLI Syntax (v0.101.0+) · ### Interface-design debates · ## How Users Invoke This Skill · ### Basic Invocation · ### With Flags · ### With File References · ### Examples Users Might Say · ## Flags · ### Flag Precedence Rules · ## Your Role: Participant + Moderator · ### Multi-Provider Debate Structure · ## Claude-Octopus Enhancements · ### 1. Session-Aware Storage · ### 2. Quality Gates for Debate Responses · ### 3. Cost Tracking & Analytics · ### 4. Document Export · ## Implementation Steps · ### Step 1: Check Provider Availability & Display Banner · Provider Availability: · ### Step 2: Ask Clarifying Questions · ### Step 3: Parse Arguments & Build Debate Fleet · # Extract question and flags · # Dynamic advisor selection — the fleet builder remains the  · ### Step 4: Setup Debate Folder · # Create debate directory structure · # Write context.md · # Debate: ${QUESTION} · ## Question · ## Clarifying Context · ## Additional Context · # Initialize state.json · ### Step 5: Conduct Rounds · #### 5.2: Launch optional host subagent (Pragmatic Implement · #### 5.3: Write Your Analysis (Opus) · # Read what all advisors said · # Write your analysis as moderator · # current host model Analysis - Round 1 · #### 5.4: Quality Gates (Claude-Octopus Enhancement) · ### Step 6: Final Synthesis · # Final Synthesis: ${QUESTION} · ## Summary of Pe

## agent-skills
id: k01325 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01325_agent-skills.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10) · 425 satır · araç adları (43): 0.6 · agent-skills · evals/fixtures/browser-testing-with-devtools/server.js · evals/fixtures/ci-cd-and-automation/src/slug.js · evals/fixtures/ci-cd-and-automation/test/slug.test.js · evals/fixtures/code-simplification/config-parser.js · evals/fixtures/code-simplification/config-parser.test.js · evals/fixtures/debugging-and-error-recovery/pagination.js · evals/fixtures/debugging-and-error-recovery/pagination.test.js · evals/fixtures/git-workflow-and-versioning/app.js · evals/fixtures/git-workflow-and-versioning/app.test.js · evals/fixtures/incremental-implementation-pressure/draft-export.js · evals/fixtures/incremental-implementation/reports.js · evals/fixtures/incremental-implementation/reports.test.js · evals/fixtures/observability-and-instrumentation/payment-retry.js · evals/fixtures/performance-optimization/benchmark.js · evals/fixtures/performance-optimization/products.js · evals/fixtures/security-and-hardening/webhook.js · evals/fixtures/security-and-hardening/webhook.test.js · evals/fixtures/test-driven-development-ecosystem/ledger.py · evals/fixtures/test-driven-development-ecosystem/test_ledger.py · evals/fixtures/test-driven-development/src/split.js · evals/fixtures/test-driven-development/test/split.test.js · hooks/sdd-cache-post.sh · hooks/sdd-cache-pre.sh · hooks/session-start-test.sh · hooks/session-start.sh · hooks/simplify-ignore-test.sh · hooks/simplify-ignore.sh · scripts/lib/skill-lint-test.js
BAŞLIKLAR: # Agent Skills · ## Commands · ## Quick Start · Or grab individual skills: · ## Adoption · ## All 25 Skills · ### Meta - Discover which skill applies · ### Define - Clarify what to build · ### Plan - Break it down · ### Build - Write the code · ### Verify - Prove it works · ### Review - Quality gates before merge · ### Ship - Deploy with confidence · ## Agent Personas · ## Reference Checklists · ## How Skills Work · ## Project Structure · ## Why Agent Skills? · ## How it compares · ## Contributing · ## Team · ## License

## code-reviewer
id: k02287 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02287_code-reviewer.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\agents\code-reviewer.md) · 323 satır · araç adları (1): code-reviewer
BAŞLIKLAR: ## Prompt Defense Baseline · ## Review Process · When invoked: · ## Confidence-Based Filtering · ### Pre-Report Gate · ### HIGH / CRITICAL Require Proof · ### It Is Acceptable And Expected To Return Zero Findings · ## Common False Positives - Skip These · ## Review Checklist · ### Security (CRITICAL) · ### Code Quality (HIGH) · ### React/Next.js Patterns (HIGH) · ### Node.js/Backend Patterns (HIGH) · When reviewing backend code: · ### Performance (MEDIUM) · ### Best Practices (LOW) · ## Review Output Format · ### Summary Format · End every review with: · ## Review Summary · ## Approval Criteria · ## Project-Specific Guidelines · ## v1.8 AI-Generated Code Review Addendum · Cost-awareness check:

## doubt-driven-development
id: k01336 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01336_doubt-driven-development.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\doubt-driven-development\SKILL.md) · 243 satır · araç adları (1): doubt-driven-development
BAŞLIKLAR: # Doubt-Driven Development · ## Overview · ## When to Use · Apply the skill when: · ## Loading Constraints · ## The Process · Doubt cycle: · ### Step 1: CLAIM — Surface what stands · ### Step 2: EXTRACT — Smallest reviewable unit · ### Step 3: DOUBT — Invoke the fresh-context reviewer · #### Cross-model escalation · # Write the adversarial prompt + ARTIFACT + CONTRACT to a te · # Then pipe via stdin so shell metacharacters in the artifac · # Codex (read-only sandbox keeps the CLI from writing to you · # Gemini ('--approval-mode plan' is read-only; '-p ""' trigg · # mode and the prompt is read from stdin): · ### Step 4: RECONCILE — Fold findings back · ### Step 5: STOP — Bounded loop, not recursion · Stop when: · ## Common Rationalizations · ## Red Flags · ## Interaction with Other Skills · ## Verification

## using-agent-skills
id: k01350 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01350_using-agent-skills.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\using-agent-skills\SKILL.md) · 192 satır · araç adları (1): using-agent-skills
BAŞLIKLAR: # Using Agent Skills · ## Overview · ## Skill Discovery · ## Core Operating Behaviors · ### 1. Surface Assumptions · ### 2. Manage Confusion Actively · ### 3. Push Back When Warranted · ### 4. Enforce Simplicity · ### 5. Maintain Scope Discipline · Do NOT: · ### 6. Verify, Don't Assume · ## Failure Modes to Avoid · ## Skill Rules · ## Lifecycle Sequence · ## Quick Reference

## typesafe-ai
id: k03713 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03713_typesafe-ai.txt (özgün: C:\Projeler\omer-skills\dist\yukle-13\typesafe-ai.zip!typesafe-ai/SKILL.md) · 142 satır · araç adları (2): typesafe-ai · typesafe-ai.zip!typesafe-ai
BAŞLIKLAR: # Build with TypeSafe · ## Read the live docs · ## Find the useful shape · ## Design the judgments · ## Compose and verify

## canary-watch
id: k01924 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01924_canary-watch.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\canary-watch\SKILL.md) · 108 satır · araç adları (1): canary-watch
BAŞLIKLAR: # Canary Watch — Post-Deploy Monitoring · ## When to Use · ## How It Works · ### What It Watches · ### Watch Modes · ### Alert Thresholds · ### Notifications · ## Output · ## Canary Report — myapp.com — 2026-03-23 03:15 PST · ### Status: HEALTHY ✓ · ### No regressions detected. Deploy is clean. · ## Integration · Pair with:

## parallel-execution-optimizer
id: k02093 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02093_parallel-execution-optimizer.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\parallel-execution-optimizer\SKILL.md) · 74 satır · araç adları (1): parallel-execution-optimizer
BAŞLIKLAR: # Parallel Execution Optimizer · ## Core Pattern · ## Lane Matrix · ## Execution Rules · ## Output Shape · Use this when reporting: · Parallel execution result: · ## Failure Modes

## departman-surec-inceleme
id: k03608 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03608_departman-surec-inceleme.txt (özgün: C:\Projeler\omer-skills\dist\token-10\departman-surec-inceleme.zip!departman-surec-inceleme/SKILL.md) · 54 satır · araç adları (2): departman-surec-inceleme · departman-surec-inceleme.zip!departman-surec-inceleme
BAŞLIKLAR: # Departman: surec-inceleme — iş sırası · ## Adımlar · ## Kapılar · ## Çakışma · ## Profil dışı üyeler (yalnız CC) · ## Dizin · ### claude.ai + Claude Code · ### yalnız Claude Code

## tone-calibration
id: k03147 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03147_tone-calibration.txt (özgün: C:\Users\pc\.claude\plugins\cache\designer-skills\system-behavior-shaping\1.0.0\skills\tone-calibration\SKILL.md) · 39 satır · araç adları (1): tone-calibration
BAŞLIKLAR: # Tone Calibration · ## Tone Dimensions · ## Tone Triggers · ## The Tone Matrix · ## Tone Consistency Rules · ## Design Artefacts

## plan-kur
id: k03558 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03558_plan-kur.txt (özgün: C:\Projeler\omer-skills\dist\envanter-3\plan-kur.zip!plan-kur/SKILL.md) · 27 satır · araç adları (2): plan-kur · plan-kur.zip!plan-kur
BAŞLIKLAR: # plan-kur — zor işte sağlam plan (tek çağrı) · ## Ne zaman · ## Nasıl · ## Kurallar

## ajn-migrasyon-model
id: k00667 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00667_ajn-migrasyon-model.txt (özgün: C:\Users\pc\.claude\agents\ajn-migrasyon-model.md) · 19 satır · araç adları (1): ajn-migrasyon-model
BAŞLIKLAR: Kurallar:

## pln-gorev-bolme
id: k01082 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01082_pln-gorev-bolme.txt (özgün: C:\Users\pc\.claude\agents\pln-gorev-bolme.md) · 15 satır · araç adları (1): pln-gorev-bolme
BAŞLIKLAR: 
