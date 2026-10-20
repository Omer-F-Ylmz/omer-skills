## surec
id: k03923 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03923_surec.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · surec
BAŞLIKLAR: 

## autoplan
id: k00053 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00053_autoplan.txt (özgün: C:\Users\pc\.claude\skills\autoplan\SKILL.md) · 995 satır · araç adları (6): autoplan · bin/guard-journal.ts · bin/guard-log.ts · bin/guard-reasons.ts · bin/owned-read.ts · bin/phase-publication-hook.ts
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Repo Ownership — See Something, Say Something · ## Search Before Building · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · ## Step 0: Detect platform and base branch · ## Design Doc Check · ## Prerequisite Skill Offer · Options: · If they choose A: · # /autoplan — Auto-Review Pipeline · ## Section index — Read each section when its situation appl · ## The 6 Decision Principles · ## Decision Classification · ## Sequential Execution — MANDATORY · ## What "Auto-Decide" Means · ## Filesystem Boundary — Codex Prompts · Prefix every Codex prompt: · ## Phase 0: Intake + Restore Point · ### Step 1: Capture restore point · Before scope/review: · ### Step 2: Read context · ### Step 3

## skill-creator
id: k03110 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03110_skill-creator.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\skill-creator\c2bdb427efe8\skills\skill-creator\SKILL.md) · 485 satır · araç adları (11): eval-viewer/generate_review.py · scripts/__init__.py · scripts/aggregate_benchmark.py · scripts/generate_report.py · scripts/improve_description.py · scripts/package_skill.py · scripts/quick_validate.py · scripts/run_eval.py · scripts/run_loop.py · scripts/utils.py · skill-creator
BAŞLIKLAR: # Skill Creator · ## Communicating with the user · ## Creating a skill · ### Capture Intent · ### Interview and Research · ### Write the SKILL.md · ### Skill Writing Guide · #### Anatomy of a Skill · #### Progressive Disclosure · #### Principle of Lack of Surprise · #### Writing Patterns · ## Report structure · ALWAYS use this exact template: · # [Title] · ## Executive summary · ## Key findings · ## Recommendations · ## Commit message format · ### Writing Style · ### Test Cases · ## Running and evaluating test cases · ### Step 1: Spawn all runs (with-skill AND baseline) in the  · Execute this task: · ### Step 2: While runs are in progress, draft assertions · ### Step 3: As runs complete, capture timing data · ### Step 4: Grade, aggregate, and launch the viewer · Once all runs are done: · ### What the user sees in the viewer · ### Step 5: Read the feedback · ## Improving the skill · ### How to think about improvements · ### The iteration loop · After improving the skill: · Keep going until: · ## Advanced: Blind comparison · ## Description Optimization · ### Step 1: Generate trigger eval queries · ### Step 2: Review with user · ### Step 3: Run the optimization loop · ### How skill triggering works · ### Step 4: Apply the result · ### Package and Present (only if `present_files` tool is ava · ## Claude.ai-specific instructions · ## Cowork-Specific Instructions · ## Reference files

## vercel-cli-with-tokens
id: k03715 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03715_vercel-cli-with-tokens.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\agent-skills-vercel-cli-with-tokens.zip!vercel-cli-with-tokens/SKILL.md) · 352 satır · araç adları (2): agent-skills-vercel-cli-with-tokens.zip!vercel-cli-with-tokens · vercel-cli-with-tokens
BAŞLIKLAR: # Vercel CLI with Tokens · ## Step 1: Locate the Vercel Token · ### A) `VERCEL_TOKEN` is already set in the environment · ### B) Token is in a `.env` file under `VERCEL_TOKEN` · ### C) Token is in a `.env` file under a different name · ### D) No token found — ask the user · # Bad — token visible in shell history and process listings · # Good — CLI reads VERCEL_TOKEN from the environment · ## Step 2: Locate the Project and Team · # Check environment · # Or check .env · # e.g. "my-team" from "https://vercel.com/my-team/my-project · ## CLI Setup · ## Deploying a Project · ### Quick Deploy (have project ID — no linking needed) · Check status: · ### Full Deploy Flow (no project ID — need to link) · #### Check project state first · # Does the project have a git remote? · # Is it already linked to a Vercel project? · #### Link the project · #### Deploy after linking · Check status: · ### Deploying from a Remote Repository (code not cloned loca · ### About `.vercel/` Directory · A linked project has either: · ## Managing Environment Variables · # Set for all environments · # Set for a specific environment (production, preview, devel · # List environment variables · # Pull env vars to local .env.local file · # Remove a variable · ## Inspecting Deployments · # List recent deployments · # Inspect a specific deployment · # View build logs (requires Vercel CLI v35+) · # View runtime request logs (follows live by default; add -- · ## Managing Domains · # List domains · # Add a domain to th

## katalog_ara
id: k03436 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03436_katalog_ara.txt (özgün: C:\Projeler\omer-skills\tools\katalog_ara.py) · 257 satır · araç adları (1): katalog_ara
BAŞLIKLAR: # TR → EN (ve tersi) eş anlamlar; sorgu genişletmesi için. K · # d8 ızgarası (altın küme ayar 20 iş): ilk 80 + tür tabanı 1 · # katalog_yenile'nin standart cagri kalıbı: satırda ad tekra · # PLAN-KUR-2 yığın süzgeci: ad → (aile, desen). Aynı ailede  · # (ENVANTER-3: Astro işine React gerektiren araç önerildi); 

## discernment-nudge
id: k01507 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01507_discernment-nudge.txt (özgün: C:\Users\pc\.claude\plugins\cache\anthropic-agent-skills\claude-api\dbd4588f9e10\skills\discernment-nudge\SKILL.md) · 209 satır · araç adları (1): discernment-nudge
BAŞLIKLAR: # Discernment nudge · ## Why this exists · ## When to offer the nudge · ## When not to · ## Writing the prompts · Each prompt should do one of: · ## Output format

## using-git-worktrees
id: k03134 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03134_using-git-worktrees.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1\skills\using-git-worktrees\SKILL.md) · 167 satır · araç adları (1): using-git-worktrees
BAŞLIKLAR: # Using Git Worktrees · ## Overview · ## Step 0: Detect Existing Isolation · # If this returns a path, you're in a submodule, not a workt · Report with branch state: · ## Step 1: Create Isolated Workspace · ### 1a. Native Worktree Tools (preferred) · ### 1b. Git Worktree Fallback · #### Directory Selection · #### Safety Verification (project-local directories only) · #### Create the Worktree · # Determine path based on chosen location · ## Step 2: Project Setup · # Node.js · # Rust · # Python · # Go · ## Step 3: Verify Clean Baseline · # Use project-appropriate command · ### Report · ## Quick Reference · ## Common Rationalizations

## discipline
id: k02795 · tür: komut · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02795_discipline.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\commands\discipline.md) · 115 satır · araç adları (1): discipline
BAŞLIKLAR: # Discipline Mode · ## Usage · ## What Discipline Mode Does · ### Development Gates · ### Knowledge Work Gates · ## How It Works · When off: · ## What Discipline Mode Does NOT Do · ## Execution Contract

## ecc-guide
id: k02195 · tür: komut · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02195_ecc-guide.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\commands\ecc-guide.md) · 93 satır · araç adları (1): ecc-guide
BAŞLIKLAR: # /ecc-guide · ## Usage · ## Operating Rules · ## What To Inspect · ## Response Patterns · ### No Arguments · Give a compact menu: · ### Topic Lookup · ### Search Mode · ### Feature Lookup · For a specific feature name: · ## Related Commands

## departman-surec-plan
id: k03553 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03553_departman-surec-plan.txt (özgün: C:\Projeler\omer-skills\dist\envanter-2\departman-surec-plan.zip!departman-surec-plan/SKILL.md) · 61 satır · araç adları (2): departman-surec-plan · departman-surec-plan.zip!departman-surec-plan
BAŞLIKLAR: # Departman: surec-plan — iş sırası · ## Adımlar · ## Kapılar · ## Çakışma · ## Profil dışı üyeler (yalnız CC) · ## Dizin · ### claude.ai + Claude Code · ### yalnız Claude Code

## ponytail-debt
id: k03012 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03012_ponytail-debt.txt (özgün: C:\Users\pc\.claude\plugins\cache\ponytail\ponytail\5.2.0\skills\ponytail-debt\SKILL.md) · 45 satır · araç adları (1): ponytail-debt
BAŞLIKLAR: ## Scan · ## Output · ## Boundaries

## ajn-mcp-sunucu-yazar
id: k00666 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00666_ajn-mcp-sunucu-yazar.txt (özgün: C:\Users\pc\.claude\agents\ajn-mcp-sunucu-yazar.md) · 28 satır · araç adları (1): ajn-mcp-sunucu-yazar
BAŞLIKLAR: Kurallar:

## ajn-hook-yazar
id: k00664 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00664_ajn-hook-yazar.txt (özgün: C:\Users\pc\.claude\agents\ajn-hook-yazar.md) · 21 satır · araç adları (1): ajn-hook-yazar
BAŞLIKLAR: Kurallar:

## pln-karar-kaydi
id: k01087 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01087_pln-karar-kaydi.txt (özgün: C:\Users\pc\.claude\agents\pln-karar-kaydi.md) · 17 satır · araç adları (1): pln-karar-kaydi
BAŞLIKLAR: Kurallar:

## cc-kopru
id: k06070 · tür: mcp · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k06070_cc-kopru.txt (özgün: C:\Users\pc\AppData\Roaming\Claude\claude_desktop_config.json) · 0 satır · araç adları (2): cc-kopru · claude_desktop_config
BAŞLIKLAR: 
