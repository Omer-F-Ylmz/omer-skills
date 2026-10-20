## Stop:.*
id: k02369 · tür: hook · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02369_Stop_._.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\hooks\hooks.json) · 1780 satır · araç adları (1013): .claude/workflows/ecc-pro-security-roadmap.js · .codebuddy/install.js · .codebuddy/install.sh · .codebuddy/uninstall.js · .codebuddy/uninstall.sh · .cursor/hooks/adapter.js · .cursor/hooks/after-file-edit.js · .cursor/hooks/after-mcp-execution.js · .cursor/hooks/after-shell-execution.js · .cursor/hooks/after-tab-file-edit.js · .cursor/hooks/before-mcp-execution.js · .cursor/hooks/before-read-file.js · .cursor/hooks/before-shell-execution-block-no-verify.js · .cursor/hooks/before-shell-execution.js · .cursor/hooks/before-submit-prompt.js · .cursor/hooks/before-tab-file-read.js · .cursor/hooks/pre-compact.js · .cursor/hooks/session-end.js · .cursor/hooks/session-start.js · .cursor/hooks/stop.js · .cursor/hooks/subagent-start.js · .cursor/hooks/subagent-stop.js · .kiro/install.sh · .kiro/scripts/format.sh · .kiro/scripts/quality-gate.sh · .opencode/index.ts · .opencode/plugins/ecc-hooks.ts · .opencode/plugins/index.ts · .opencode/plugins/lib/changed-files-store.ts · .opencode/tools/changed-files.ts
BAŞLIKLAR: 

## SessionStart:.*
id: k02358 · tür: hook · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02358_SessionStart_._.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\hooks\hooks.json) · 825 satır · araç adları (1013): .claude/workflows/ecc-pro-security-roadmap.js · .codebuddy/install.js · .codebuddy/install.sh · .codebuddy/uninstall.js · .codebuddy/uninstall.sh · .cursor/hooks/adapter.js · .cursor/hooks/after-file-edit.js · .cursor/hooks/after-mcp-execution.js · .cursor/hooks/after-shell-execution.js · .cursor/hooks/after-tab-file-edit.js · .cursor/hooks/before-mcp-execution.js · .cursor/hooks/before-read-file.js · .cursor/hooks/before-shell-execution-block-no-verify.js · .cursor/hooks/before-shell-execution.js · .cursor/hooks/before-submit-prompt.js · .cursor/hooks/before-tab-file-read.js · .cursor/hooks/pre-compact.js · .cursor/hooks/session-end.js · .cursor/hooks/session-start.js · .cursor/hooks/stop.js · .cursor/hooks/subagent-start.js · .cursor/hooks/subagent-stop.js · .kiro/install.sh · .kiro/scripts/format.sh · .kiro/scripts/quality-gate.sh · .opencode/index.ts · .opencode/plugins/ecc-hooks.ts · .opencode/plugins/index.ts · .opencode/plugins/lib/changed-files-store.ts · .opencode/tools/changed-files.ts
BAŞLIKLAR: 

## skill-issues
id: k02756 · tür: skill · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02756_skill-issues.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\skills\skill-issues\SKILL.md) · 486 satır · araç adları (1): skill-issues
BAŞLIKLAR: # Issue Tracking · ## Overview · ## When to Use · ## Subcommands · ### 1. List Issues (Default) · ## Open Issues · ### 2. Add Issue · #### Step 1: Gather Information · #### Step 2: Determine Current Phase · # Check if STATE.md exists · #### Step 3: Generate Issue ID · # Get today's date · # Find existing issues for today · # Increment sequence number · # If ISS-20260203-001 exists, next is ISS-20260203-002 · #### Step 4: Append to ISSUES.md · #### Step 5: Confirm · ### 3. Resolve Issue · #### Step 1: Validate Issue Exists · # Check if issue ID exists in Open Issues · #### Step 2: Ask for Resolution Notes · Please provide resolution notes: · #### Step 3: Move to Resolved Section · #### Step 4: Confirm · ### 4. Show Issue Details · #### Step 1: Find Issue · #### Step 2: Display Details · ## Issue Details: ISS-20260203-001 · ## Issue Details: ISS-20260203-001 · #### Step 3: If Not Found · ## File Management · ### Initialize ISSUES.md · # Create .octo directory if needed · # Copy template · # Replace {{PROJECT_NAME}} with actual project name · ### Preserve Existing Issues · # Read existing content · # Modify specific section only · # Append new issue to Open Issues table · # OR move issue from Open to Resolved · # Write back with all content preserved · ## ID Generation Algorithm · # Get today's date in YYYYMMDD format · # Find all issues created today · # Generate ID · ## Severity Levels · ## Integration with Other Skills · ### With skill-debug · ### With skill-task-management ·

## plankton-code-quality
id: k02099 · tür: skill · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02099_plankton-code-quality.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\plankton-code-quality\SKILL.md) · 328 satır · araç adları (1): plankton-code-quality
BAŞLIKLAR: # Plankton Code Quality Skill · ## When to Use · ## How It Works · ### Three-Phase Architecture · ### What the Main Agent Sees · ### Config Protection (Defense Against Rule-Gaming) · ### Package Manager Enforcement · ## Setup · ### Quick Start · # Install core dependencies · # Install Python linters · # Start Claude Code — hooks activate automatically · ### Per-Project Integration · ### Language-Specific Dependencies · ## Pairing with ECC · ### Complementary, Not Overlapping · ### Recommended Combination · ### Avoiding Hook Conflicts · ## Configuration Reference · ## Environment Overrides · ## References · ## ECC v1.8 Additions · ### Copyable Hook Profile · Set strict quality behavior: · ### Language Gate Table · ### Config Tamper Guard · ### CI Integration Pattern · ### Health Metrics · Track: · ## Gabe's addition: oxlint complexity + ratchet ceiling (JS/ · ### Turn on oxlint's `complexity` rule when using it · ### Model-routing row · ### The ratchet-ceiling technique

## operator-approval-loop
id: k02086 · tür: skill · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02086_operator-approval-loop.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\operator-approval-loop\SKILL.md) · 238 satır · araç adları (2): operator-approval-loop · references/approval_claims.py
BAŞLIKLAR: # Operator Approval Loop · ## When to Use · ## How It Works · ### Objects · ### Filing a draft · ### Baseline gate · ### Deciding · ### Delivering · ### Time-boxed auto-approval (optional) · ### Signal linkage · ## Examples · ### File a draft · ### Re-file after a steer · ### Gate refusal · ### Delivery footer in an internal channel · ## Invariants to test

## aciklama_yaz
id: k03393 · tür: cli · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03393_aciklama_yaz.txt (özgün: C:\Projeler\omer-skills\tools\aciklama_yaz.py) · 189 satır · araç adları (1): aciklama_yaz
BAŞLIKLAR: 

## multi-backend
id: k02233 · tür: komut · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02233_multi-backend.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\commands\multi-backend.md) · 164 satır · araç adları (1): multi-backend
BAŞLIKLAR: # Backend - Backend-Focused Development · ## Usage · ## Context · ## Your Role · ## Multi-Model Call Specification · # New session call · # Resume session call · ## Communication Guidelines · ## Core Workflow · ### Phase 0: Prompt Enhancement (Optional) · ### Phase 1: Research · ### Phase 2: Ideation · ### Phase 3: Planning · ### Phase 4: Implementation · ### Phase 5: Optimization · ### Phase 6: Quality Review · ## Key Rules

## loop
id: k02806 · tür: komut · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02806_loop.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\commands\loop.md) · 137 satır · araç adları (1): loop
BAŞLIKLAR: # Loop - Iterative Execution Skill · ## Instructions · ## Quick Usage · Just use natural language: · Or use the explicit command: · ## Loop Execution Approach · ## What You Get · ## Use Cases · ## Safety Features · ## Parameters · ## Natural Language Examples · ## Metric Verification Mode · ### Metric Mode Parameters · ### Metric Mode Examples · ### How It Works · ## Integration with Other Skills

## prp-commit
id: k02252 · tür: komut · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02252_prp-commit.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\commands\prp-commit.md) · 112 satır · araç adları (1): prp-commit
BAŞLIKLAR: # Smart Commit · ## Phase 1 — ASSESS · ## Phase 2 — INTERPRET & STAGE · ## Phase 3 — COMMIT · Types: · Rules: · ## Phase 4 — OUTPUT · Report to user: · Next steps: · ## Examples

## hermes-imports
id: k02016 · tür: skill · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02016_hermes-imports.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\hermes-imports\SKILL.md) · 89 satır · araç adları (1): hermes-imports
BAŞLIKLAR: # Hermes Imports · ## When To Use · ## Import Rules · ## Sanitization Checklist · ## Conversion Pattern · ## Example: Launch Handoff · Local Hermes prompt: · ECC-safe version: · ## Example: Quiet-Hours Operator Job · Local Hermes job: · ECC-safe version: · ## Output Contract · Return:

## spec
id: k02828 · tür: komut · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02828_spec.txt (özgün: C:\Users\pc\.claude\plugins\cache\nyldn-plugins\octo\11.13.1\commands\spec.md) · 69 satır · araç adları (1): spec
BAŞLIKLAR: # Spec - NLSpec Authoring · ## INSTRUCTIONS FOR CLAUDE · ## Quick Usage · ## What Is Spec? · ## What You Get · ## When To Use · ## Natural Language Examples

## harness-optimizer
id: k02310 · tür: agent · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02310_harness-optimizer.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\agents\harness-optimizer.md) · 55 satır · araç adları (1): harness-optimizer
BAŞLIKLAR: ## Prompt Defense Baseline · ## Your Role · ## Workflow · ### Step 1: Understand · ### Step 2: Execute · ### Step 3: Verify · ## Output Format · ## Examples · ### Example: Slow PreToolUse hook flagged by the audit

## continuous-agent-loop
id: k01944 · tür: skill · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01944_continuous-agent-loop.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\continuous-agent-loop\SKILL.md) · 46 satır · araç adları (1): continuous-agent-loop
BAŞLIKLAR: # Continuous Agent Loop · ## Loop Selection Flow · ## Combined Pattern · Recommended production stack: · ## Failure Modes · ## Recovery

## loop-start
id: k02229 · tür: komut · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02229_loop-start.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\commands\loop-start.md) · 36 satır · araç adları (1): loop-start
BAŞLIKLAR: # Loop Start Command · ## Usage · ## Flow · ## Required Safety Checks · ## Arguments

## epic-validate
id: k02202 · tür: komut · katman: B · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02202_epic-validate.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\commands\epic-validate.md) · 22 satır · araç adları (1): epic-validate
BAŞLIKLAR: # /epic-validate · What this checks: · Compatibility aliases:
