## grill-me
id: k03992 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03992_grill-me.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · grill-me
BAŞLIKLAR: 

## pair-agent
id: k00441 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00441_pair-agent.txt (özgün: C:\Users\pc\.claude\skills\pair-agent\SKILL.md) · 737 satır · araç adları (1): pair-agent
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## AskUserQuestion Format · ### Tool resolution (read first) · ### When AskUserQuestion is unavailable or a call fails · Tell these apart: · ### Format · Pros / cons: · ### Handling 5+ options — split, never drop · ### Self-check before emitting · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Context Recovery · ## Writing Style (skip entirely if `EXPLAIN_LEVEL: terse` ap · ## Completeness Principle — Boil the Ocean · ## Confusion Protocol · ## Claims Need Evidence · ## Context Health (soft directive) · ## Question Tuning (skip entirely if `QUESTION_TUNING: false · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · # /pair-agent — Share Your Browser With Another AI Agent · ## How it works · ## SETUP (run this check BEFORE any browse command) · ## Step 1: Check prerequisites · ## Step 2: Ask what they want · Use AskUserQuestion: · Options: · ## Step 3: Local or remote? · Use AskUserQuestion: · Options: · ## Step 4: Execute pairing · Options: · ### If same machine (option A): · ### If different machine (option B): · Then detect ngrok status: · Then tell the user: · Tell the user: · Tell the user: · ## Step 5: Verify connection · ## What the remote agent can do · ## Troubleshooting · ## Platform-specific notes · ### OpenClaw / AlphaClaw · ### C

## superpowers
id: k03123 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03123_superpowers.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\superpowers\6.4.1) · 448 satır · araç adları (71): .hermes-plugin/__init__.py · .opencode/plugins/superpowers.js · .pi/extensions/superpowers.ts · 6.4 · index.js · scripts/bump-version.sh · scripts/lint-shell.sh · scripts/package-codex-plugin.sh · scripts/sync-to-codex-plugin.sh · skills/brainstorming/scripts/helper.js · skills/brainstorming/scripts/server.cjs · skills/brainstorming/scripts/start-server.sh · skills/brainstorming/scripts/stop-server.sh · skills/systematic-debugging/condition-based-waiting-example.ts · skills/systematic-debugging/find-polluter.sh · skills/writing-skills/render-graphs.js · superpowers · tests/antigravity/run-tests.sh · tests/antigravity/test-antigravity-tools.sh · tests/brainstorm-server/auth.test.js · tests/brainstorm-server/branding.test.js · tests/brainstorm-server/browser-launcher.test.js · tests/brainstorm-server/helper.test.js · tests/brainstorm-server/lifecycle.test.js · tests/brainstorm-server/server.test.js · tests/brainstorm-server/start-server.test.sh · tests/brainstorm-server/stop-server.test.sh · tests/brainstorm-server/windows-lifecycle.test.sh · tests/brainstorm-server/ws-protocol.test.js · tests/claude-code/analyze-token-usage.py
BAŞLIKLAR: # Superpowers · ## Table of Contents · ## How it works · ## Commercial Services · ## Installation · ### Claude Code · #### Official Marketplace · #### Superpowers Marketplace · ### Antigravity · ### Codex App · ### Codex CLI · ### Cursor · ### Devin CLI · ### Factory Droid · ### Gemini CLI · ### GitHub Copilot CLI · ### Grok Build CLI · ### Kimi Code · ### OpenCode · ### Pi · ### Qwen Code · ### Hermes Agent · ### Muse · ## The Basic Workflow · ## When Something Goes Wrong · ## Community · ## What's Inside · ### Skills Library · ## Philosophy · ## Contributing · ## Updating · ## License · ## Visual companion telemetry

## pr-review-toolkit
id: k03016 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03016_pr-review-toolkit.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-code-plugins\pr-review-toolkit\1.0.0) · 326 satır · araç adları (2): 1.0 · pr-review-toolkit
BAŞLIKLAR: # PR Review Toolkit · ## Overview · ## Agents · ### 1. comment-analyzer · ### 2. pr-test-analyzer · ### 3. silent-failure-hunter · ### 4. type-design-analyzer · ### 5. code-reviewer · ### 6. code-simplifier · ## Usage Patterns · ### Individual Agent Usage · ### Comprehensive PR Review · ### Proactive Review · ## Installation · # Find "pr-review-toolkit" · # Install · ## Agent Details · ### Confidence Scoring · ### Output Formats · ## Best Practices · ### When to Use Each Agent · ### Running Multiple Agents · ## Tips · ## Troubleshooting · ### Agent Not Triggering · ### Agent Analyzing Wrong Files · ## Integration with Workflow · This plugin works great with: · ## Contributing · ## License · ## Author

## deprecation-and-migration
id: k01334 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01334_deprecation-and-migration.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\deprecation-and-migration\SKILL.md) · 247 satır · araç adları (1): deprecation-and-migration
BAŞLIKLAR: # Deprecation and Migration · ## Overview · ## When to Use · ## Core Principles · ### Code Is a Liability · ### Hyrum's Law Makes Removal Hard · ### Deprecation Planning Starts at Design Time · ## The Deprecation Decision · ## Compulsory vs Advisory Deprecation · ## The Migration Process · ### Step 1: Build the Replacement · ### Step 2: Announce and Document · ## Deprecation Notice: OldService · ### Migration Guide · ### Step 3: Migrate Incrementally · ### Step 4: Remove the Old System · ## Migration Patterns · ### Strangler Pattern · ### Adapter Pattern · ### Feature Flag Migration · ### Database Schema Migrations (Expand/Contract) · ## Zombie Code · ## Common Rationalizations · ## Red Flags · ## Verification · After completing a deprecation:

## ima-copilot
id: k02517 · tür: plugin · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02517_ima-copilot.txt (özgün: C:\Users\pc\.claude\plugins\cache\daymade-skills\ima-copilot\1.2.1) · 194 satır · araç adları (5): 1.2 · ima-copilot · scripts/diagnose.sh · scripts/install_ima_skill.sh · scripts/search_fanout.py
BAŞLIKLAR: # IMA Copilot · ## Overview · ## Architectural principles (do not violate) · ## What this skill does · ## Routing · ## Capability 1: Install upstream ima-skill · To run it: · ## Capability 2: Configure API credentials · ## Capability 3: Diagnose and fix known issues · ### Step 1 — Run the read-only diagnosis · ### Step 2 — Parse the report and ask the user · ### Step 3 — Ask for explicit consent before touching upstre · ### Step 4 — Execute the chosen strategy · ### Step 5 — Re-run diagnose to confirm · ### An important note about upstream updates · ## Capability 4: Personalized fan-out search · ## Capability 5: Import URLs and extract content · ## What this skill refuses to do · ## File layout

## omni-resilience
id: k03746 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03746_omni-resilience.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\omniroute-omni-resilience.zip!omni-resilience/SKILL.md) · 144 satır · araç adları (2): omni-resilience · omniroute-omni-resilience.zip!omni-resilience
BAŞLIKLAR: ## Overview · ## Authentication · ## Endpoints · ### GET /api/monitoring/health · ## Payloads · # OmniRoute — Monitoring & Health · ## System health · Unauthenticated quick check: · # → {"ok":true} · ## Provider circuit breakers · ## Per-provider metrics (p50/p95/p99) · Response shape per provider: · ## Via MCP (if OmniRoute is your MCP server) · ## Quota check · ## Budget guard (spend limit) · ## MCP audit log · ## Errors

## terminal-ops
id: k02169 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02169_terminal-ops.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\terminal-ops\SKILL.md) · 110 satır · araç adları (1): terminal-ops
BAŞLIKLAR: # Terminal Ops · ## Skill Stack · ## When to Use · ## Guardrails · ## Workflow · ### 1. Resolve the working surface · Settle: · ### 2. Read the failing surface first · Before changing anything: · ### 3. Keep the fix narrow · ### 4. Report exact execution state · Use exact status words: · ## Output Format · ## Pitfalls · ## Verification

## configure
id: k01524 · tür: komut · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01524_configure.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-hud\claude-hud\0.10.0\commands\configure.md) · 77 satır · araç adları (1): configure
BAŞLIKLAR: # Configure Claude HUD · ## Read the current config · ## Ask · ## Preview and confirm · ## Write

## departman-surec-git-yayin
id: k03607 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03607_departman-surec-git-yayin.txt (özgün: C:\Projeler\omer-skills\dist\token-10\departman-surec-git-yayin.zip!departman-surec-git-yayin/SKILL.md) · 55 satır · araç adları (2): departman-surec-git-yayin · departman-surec-git-yayin.zip!departman-surec-git-yayin
BAŞLIKLAR: # Departman: surec-git-yayin — iş sırası · ## Adımlar · ## Kapılar · ## Profil dışı üyeler (yalnız CC) · ## Dizin · ### claude.ai + Claude Code · ### yalnız Claude Code

## projects
id: k02250 · tür: komut · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02250_projects.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\commands\projects.md) · 39 satır · araç adları (1): projects
BAŞLIKLAR: # Projects Command · ## Implementation · ## Usage · ## What to Do

## pln-teknik-spec
id: k01102 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01102_pln-teknik-spec.txt (özgün: C:\Users\pc\.claude\agents\pln-teknik-spec.md) · 27 satır · araç adları (1): pln-teknik-spec
BAŞLIKLAR: Kurallar:

## ajn-claude-api-gelistirici
id: k00662 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00662_ajn-claude-api-gelistirici.txt (özgün: C:\Users\pc\.claude\agents\ajn-claude-api-gelistirici.md) · 19 satır · araç adları (1): ajn-claude-api-gelistirici
BAŞLIKLAR: Kurallar:

## ajn-ajan-tanimi-yazar
id: k00659 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00659_ajn-ajan-tanimi-yazar.txt (özgün: C:\Users\pc\.claude\agents\ajn-ajan-tanimi-yazar.md) · 15 satır · araç adları (1): ajn-ajan-tanimi-yazar
BAŞLIKLAR: Kurallar:
