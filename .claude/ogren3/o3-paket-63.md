## gelistirme-is-akisi-paket
id: k03821 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03821_gelistirme-is-akisi-paket.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (3): claudeai_adlar · gelistirme-is-akisi · gelistirme-is-akisi-paket
BAŞLIKLAR: 

## messages-api-sdk
id: k03889 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03889_messages-api-sdk.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · messages-api-sdk
BAŞLIKLAR: 

## local-codex
id: k04001 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04001_local-codex.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · local-codex
BAŞLIKLAR: 

## autonomous-loops
id: k03663 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03663_autonomous-loops.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\ecc-autonomous-loops.zip!autonomous-loops/SKILL.md) · 611 satır · araç adları (2): autonomous-loops · ecc-autonomous-loops.zip!autonomous-loops
BAŞLIKLAR: # Autonomous Loops Skill · ## When to Use · ## Loop Pattern Spectrum · ## 1. Sequential Pipeline (`claude -p`) · ### Core Insight · # daily-dev.sh — Sequential pipeline for a feature branch · # Step 1: Implement the feature · # Step 2: De-sloppify (cleanup pass) · # Step 3: Verify · # Step 4: Commit · ### Key Design Principles · ### Variations · # Research with Opus (deep reasoning) · # Implement with Sonnet (fast, capable) · # Review with Opus (thorough) · # Pass context via files, not prompt length · # Read-only analysis pass · # Write-only implementation pass · ## 2. NanoClaw REPL · # Start the default session · # Named session with skill context · ### How It Works · ### When NanoClaw vs Sequential Pipeline · ## 3. Infinite Agentic Loop · ### Architecture: Two-Prompt System · ### The Pattern · ### Implementation via Claude Code Commands · ### Batching Strategy · ### Key Insight: Uniqueness via Assignment · ## 4. Continuous Claude PR Loop · ### Core Loop · ### Installation · ### Usage · # Basic: 10 iterations · # Cost-limited · # Time-boxed · # With code review pass · # Parallel via worktrees · ### Cross-Iteration Context: SHARED_TASK_NOTES.md · ## Progress · ## Next Steps · ### CI Failure Recovery · ### Completion Signal · ### Key Configuration · ## 5. The De-Sloppify Pattern · ### The Problem · ### Why Not Negative Instructions? · ### The Solution: Separate Pass · # Step 1: Implement (let it be thorough) · # Step 2: De-sloppify (separate context, focused cleanup) · ### In

## deepseek-harness
id: k04164 · tür: repo · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04164_deepseek-harness.txt (özgün: C:\Projeler\.tmp-kurulum6c\deepseek-harness) · 367 satır · araç adları (5134): .agents/skills/record-browser-gif/scripts/encode_gif.py · .agents/skills/record-browser-gif/scripts/test_encode_gif.py · .github/issue-management/github.mjs · .github/issue-management/lifecycle.mjs · .github/issue-management/policy.mjs · .github/issue-management/policy.test.mjs · .github/issue-management/pull-request.mjs · .github/issue-management/rules.mjs · .github/review-ownership/author-weight.mjs · .github/review-ownership/author-weight.test.mjs · .github/review-ownership/blame-ownership.mjs · .github/review-ownership/blame-ownership.test.mjs · .github/review-ownership/blame-production.py · .github/review-ownership/check-approval.mjs · .github/review-ownership/check-approval.test.mjs · .github/review-ownership/test_blame_production.py · @deepseek-ai/dsh-root · apps/cli/src/args.ts · apps/cli/src/bin.ts · apps/cli/src/dump-config-schema.ts · apps/cli/src/dump-config.ts · apps/cli/src/plugin.ts · apps/cli/src/process-shutdown.ts · apps/cli/src/profile-boot.ts · apps/cli/src/startup-diagnostics.ts · apps/cli/tests/agent-team-headless.e2e.ts · apps/cli/tests/args.spec.ts · apps/cli/tests/built-bin.e2e.ts · apps/cli/tests/desktop-host.e2e.ts · apps/cli/tests/dsh-badge.expected.e2e.ts
BAŞLIKLAR: # DeepSeek Harness · ## Developer preview · ## Run · ### Run from `npm` · ### Run from source · ## Community and support · ## Contributing · ## Development · ## Citation · ## License

## _gstack-command
id: k00018 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00018__gstack-command.txt (özgün: C:\Users\pc\.claude\skills\_gstack-command\SKILL.md) · 243 satır · araç adları (1): _gstack-command
BAŞLIKLAR: ## When to invoke this skill · ## Preamble (run first) · ## Plan Mode Safe Operations · ## Skill Invocation During Plan Mode · ## Artifacts Sync (skill start) · ## Model-Specific Behavioral Patch (claude) · ## Voice · ## Completion Status Protocol · ## Operational Self-Improvement · ## Telemetry (run last) · ## Plan Status Footer · ## Route first

## Stop:*
id: k03088 · tür: hook · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03088_Stop__.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-code-plugins\ralph-wiggum\1.0.0\hooks\hooks.json) · 190 satır · araç adları (4): Stop:* · hooks/stop-hook.sh · ralph-wiggum · scripts/setup-ralph-loop.sh
BAŞLIKLAR: # Ralph Wiggum Stop Hook · # Prevents session exit when a ralph-loop is active · # Feeds Claude's output back as input to continue the loop · # Read hook input from stdin (advanced stop hook API) · # Check if ralph-loop is active · # Parse markdown frontmatter (YAML between ---) and extract  · # Extract completion_promise and strip surrounding quotes if · # Validate numeric fields before arithmetic operations · # Check if max iterations reached · # Get transcript path from hook input · # Read last assistant message from transcript (JSONL format  · # First check if there are any assistant messages · # Extract last assistant message with explicit error handlin · # Parse JSON with error handling · # Check if jq succeeded · # Check for completion promise (only if set) · # Not complete - continue loop with SAME PROMPT · # Extract prompt (everything after the closing ---) · # Skip first --- line, skip until second --- line, then prin · # Use i>=2 instead of i==2 to handle --- in prompt content · # Update iteration in frontmatter (portable across macOS and · # Create temp file, then atomically replace · # Build system message with iteration count and completion p · # Output JSON to block the stop and feed prompt back · # The "reason" field contains the prompt that will be sent b · # Exit 0 for successful hook execution

## Autonomous Optimization Architect
id: k00844 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00844_Autonomous_Optimization_Architect.txt (özgün: C:\Users\pc\.claude\agents\engineering-autonomous-optimization-architect.md) · 127 satır · araç adları (3): Autonomous Optimization Architect · aoa · engineering-autonomous-optimization-architect
BAŞLIKLAR: ## Ders bankası · # ⚙️ Autonomous Optimization Architect · ## 🧠 Your Identity & Memory · ## 🎯 Your Core Mission · ## 🚨 Critical Rules You Must Follow · ## 📋 Your Technical Deliverables · ### Example Code: The Intelligent Guardrail Router · ## 🔄 Your Workflow Process · ## 💭 Your Communication Style · ## 🔄 Learning & Memory · ## 🎯 Your Success Metrics · ## 🔍 How This Agent Differs From Existing Roles

## cagri_sayac
id: k03410 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03410_cagri_sayac.txt (özgün: C:\Projeler\omer-skills\tools\cagri_sayac.py) · 99 satır · araç adları (1): cagri_sayac
BAŞLIKLAR: 

## pr-link-issue
id: k00463 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00463_pr-link-issue.txt (özgün: C:\Users\pc\.claude\skills\pr-link-issue\SKILL.md) · 74 satır · araç adları (1): pr-link-issue
BAŞLIKLAR: # Link a GitHub Issue + Linear Ticket on a PR · ## Inputs · ## Steps · ## Notes

## fable-advisor
id: k02438 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02438_fable-advisor.txt (özgün: C:\Users\pc\.claude\plugins\cache\fable-advisor\fable-advisor\6.1.0\agents\fable-advisor.md) · 40 satır · araç adları (1): fable-advisor
BAŞLIKLAR: # Fable Advisor · ## When you're called · Two occasions: · ## Final review, specifically · ## How to answer · ## What you never do

## openclaw-win-paket
id: k00436 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00436_openclaw-win-paket.txt (özgün: C:\Users\pc\.claude\skills\openclaw-win-paket\SKILL.md) · 23 satır · araç adları (2): openclaw-win · openclaw-win-paket
BAŞLIKLAR: # openclaw-win-paket

## pln-proje-yonetimi
id: k01094 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01094_pln-proje-yonetimi.txt (özgün: C:\Users\pc\.claude\agents\pln-proje-yonetimi.md) · 20 satır · araç adları (1): pln-proje-yonetimi
BAŞLIKLAR: Kurallar:

## devfleet
id: k03351 · tür: mcp · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03351_devfleet.txt (özgün: C:\Users\pc\.claude.json) · 10 satır · araç adları (2): .claude · devfleet
BAŞLIKLAR: 
