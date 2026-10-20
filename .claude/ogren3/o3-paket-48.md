## cli-a2a
id: k03779 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03779_cli-a2a.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · cli-a2a
BAŞLIKLAR: 

## gstack-pair-agent
id: k03857 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03857_gstack-pair-agent.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · gstack-pair-agent
BAŞLIKLAR: 

## plugin-dev-plugin-validator
id: k03913 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03913_plugin-dev-plugin-validator.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · plugin-dev-plugin-validator
BAŞLIKLAR: 

## cc-hooks
id: k03646 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03646_cc-hooks.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\daymade-claude-code-cc-hooks.zip!cc-hooks/SKILL.md) · 1369 satır · araç adları (2): cc-hooks · daymade-claude-code-cc-hooks.zip!cc-hooks
BAŞLIKLAR: # Claude Code Hooks · ## When a hook is the right tool (and when it isn't) · ## Hook types and what the exit code means · ## The skeleton (PreToolUse Bash guard) · # 0-fork fast path: a builtin `case` on the raw JSON, BEFORE · # Your guard runs on EVERY matching tool call, so the irrele · # that has to be cheap. Keep this filter BROADER than what y · # never flag-level — it answers "is this even about X", noth · # ... precise detection here ... · ## Rules that separate a working guard from a session-poison · ### 1. Match at the **token level with shlex**, never awk-sp · ### 2. Test with **bash -n + a real JSON event, end-to-end,  · ### 3. Installer-owned source, installation and recovery · ### 4. Registration is per-profile — converge ALL profiles,  · ### 5. Decide the failure **direction**, and test *that* — n · ### 6. Judge on a fact the world can answer — never on your  · ### 7. If the hook **demands remediation**, prove the loop t · Filled review-loop example: · # TERMINATION: V = 1 - exists(<receipt path>) · # decreased by: R writes the receipt; nothing R does afterwa · ### 8. Waiting needs the same proof — notifications are advi · ### 9. Fixtures cannot tell you the false-positive rate — re · ### 10. A guard that blocks legitimate work needs a **consen · ## Build order (in sequence) · ## Known pitfalls (read before debugging a misfiring hook) · ## Reference material · ## Maintenance — where new content goes

## marketplace-dev
id: k03653 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03653_marketplace-dev.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\daymade-claude-code-marketplace-dev.zip!marketplace-dev/SKILL.md) · 464 satır · araç adları (2): daymade-claude-code-marketplace-dev.zip!marketplace-dev · marketplace-dev
BAŞLIKLAR: # marketplace-dev · ## Route the task before editing · ## Phase 0: Evidence Intake · ## Phase 1: Analyze the Target Repo · ### Step 1: Discover all skills · # Find every SKILL.md · ### Step 2: Read the repo metadata · ### Step 3: Determine categories · ### Step 4: Choose plugin boundaries · ## Phase 2: Create marketplace.json · ### The official schema (memorize this) · ### Generate the marketplace.json · ### Naming the marketplace · Choose a name that is: · ### Description rules · ## Maintaining an existing marketplace · ### Adding a member skill to an existing suite · ## Phase 3: Validate · ### Step 1: One-shot pre-flight check · What it checks: · ### Step 2: Installation test · # Add as local marketplace · # Install a plugin · # Verify it appears · # Check for updates (should say "already at latest") · # Clean up · ### Step 3: Cache footprint test · Expected results: · ### Step 4: GitHub installation test (if pushed) · # Test from GitHub (requires the branch to be pushed) · # Verify · # Clean up · ## Pre-flight Checklist (MUST pass before proceeding to PR) · ### Automated checks · ### Metadata check · ### Per-plugin check · For each plugin entry: · ### Final validation · ## Phase 4: Create PR · ### Principles · ### README update (if appropriate) · ## Install · ### PR description template · Include: · ## Bundled hooks (optional, auto-activated) · ## Anti-Patterns (things that went wrong and how to fix them

## cli-serve
id: k03734 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03734_cli-serve.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\omniroute-cli-serve.zip!cli-serve/SKILL.md) · 314 satır · araç adları (2): cli-serve · omniroute-cli-serve.zip!cli-serve
BAŞLIKLAR: ## Overview · ## Quick install · ## Subcommands · ### `dashboard` · ### `restart` · ### `serve` · ### `stop` · ## Setup · ### Install · # or: use the binary bundled with the desktop app · Verify: · ### Connection · For a remote server: · ### Global flags · ### Output formats · ### Quick start: one-shot server + provider setup · # 1. Start server · # 2. (First run) interactive setup wizard · # 3. Verify everything is healthy · ### CLI capability skills · ### Errors · ## Admin lifecycle · ### Server lifecycle · ### Setup & provisioning · #### Interactive wizard · #### Non-interactive (CI / Docker) · ### Diagnostics · ### Backup & restore · ### Autostart (system tray / startup) · ### Tunnels (public URL) · ### Config & environment · ### Recovery · ### Logs · ### Update · ### Errors

## ghostty-use
id: k02458 · tür: plugin · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02458_ghostty-use.txt (özgün: C:\Users\pc\.claude\plugins\cache\daymade-skills\ghostty-use\1.6.1) · 215 satır · araç adları (9): 1.6 · ghostty-use · scripts/ghostty_session.py · scripts/ghostty_storage.py · scripts/ghostty_switch.py · scripts/ghostty_watch.py · scripts/test_ghostty_session.py · scripts/test_ghostty_switch.py · scripts/test_ghostty_watch.py
BAŞLIKLAR: # ghostty-use · ## Entry decision tree · ## Codex account switch · # User: finish work, exit the saved Codex TUIs and manually  · ## Quick start · # Before quitting (from any directory): · # After restart (from any directory; needs Accessibility per · ## Automatic change-only backups · ## No suitable snapshot: reconstruct the recovery manifest · # Review candidates without writing state or opening tabs: · # Build one chosen set in a NEW file; --only accepts unambig · # Restore the full selected set in one invocation, including · ## What manual snapshot records per session · ## Restore mechanics and limits · ## Profile environment mapping (optional) · ## Troubleshooting · ## Deeper details

## skill-writer
id: k00558 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00558_skill-writer.txt (özgün: C:\Users\pc\.claude\skills\skill-writer\SKILL.md) · 156 satır · araç adları (2): scripts/quick_validate.py · skill-writer
BAŞLIKLAR: # Skill Writer · ## Core Workflow References · ## Artifact Layout References · ## Workflow Mechanic References · ## Claude Code References · ## Example Profiles · ## Step 1: Resolve target, path, and shape · ## Step 2: Run synthesis when needed · ## Step 3: Run iteration first when improving from outcomes/ · ## Step 4: Author or update skill artifacts · ## Step 5: Optimize description quality · ## Step 6: Register and validate · ## Output format · Return:

## omni-auth
id: k03738 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03738_omni-auth.txt (özgün: C:\Projeler\omer-skills\dist\yukle-7\omniroute-omni-auth.zip!omni-auth/SKILL.md) · 117 satır · araç adları (2): omni-auth · omniroute-omni-auth.zip!omni-auth
BAŞLIKLAR: ## Overview · ## Authentication · ## Endpoints · ### POST /api/auth/login · ### POST /api/auth/logout · ## Payloads · # OmniRoute · ## Setup · ## Discover models · ## Capability skills · ## CLI skills (omniroute binary) · ## Errors · ## Differentiators vs OpenAI direct

## workflow-threads-manager
id: k00648 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00648_workflow-threads-manager.txt (özgün: C:\Users\pc\.claude\skills\workflow-threads-manager\SKILL.md) · 93 satır · araç adları (6): scripts/audit-changelog.py · scripts/contact-sheet.py · scripts/live-check.sh · scripts/repo-status.sh · scripts/save-captures.sh · workflow-threads-manager
BAŞLIKLAR: # Workflow: threads manager · ## Tools · ## The check · ## Triage · ## Changelog gaps · ## Guardrails · ## Report format

## ajan_getir_zip
id: k03394 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03394_ajan_getir_zip.txt (özgün: C:\Projeler\omer-skills\tools\ajan_getir_zip.py) · 57 satır · araç adları (1): ajan_getir_zip
BAŞLIKLAR: 

## convex-deploy-guard
id: k00141 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00141_convex-deploy-guard.txt (özgün: C:\Users\pc\.claude\skills\convex-deploy-guard\SKILL.md) · 29 satır · araç adları (1): convex-deploy-guard
BAŞLIKLAR: # Deployment target guard · ## Workflow · ## Rules

## vrm-worktree-paralel
id: k01235 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01235_vrm-worktree-paralel.txt (özgün: C:\Users\pc\.claude\agents\vrm-worktree-paralel.md) · 21 satır · araç adları (1): vrm-worktree-paralel
BAŞLIKLAR: Kurallar:

## fable_ajan_hook
id: k03419 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03419_fable_ajan_hook.txt (özgün: C:\Projeler\omer-skills\tools\fable_ajan_hook.py) · 19 satır · araç adları (1): fable_ajan_hook
BAŞLIKLAR: 

## agent-browser-paket
id: k04183 · tür: repo · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04183_agent-browser-paket.txt (özgün: C:\Projeler\.tmp-kurulum6c-zip\agent-browser-paket) · 0 satır · araç adları (5): agent-browser · agent-browser-paket · agent-browser-paket/skills/core/templates/authenticated-session.sh · agent-browser-paket/skills/core/templates/capture-workflow.sh · agent-browser-paket/skills/core/templates/form-automation.sh
BAŞLIKLAR: 
