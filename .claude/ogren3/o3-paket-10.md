## writing-rules
id: k03933 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03933_writing-rules.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · writing-rules
BAŞLIKLAR: 

## command-development
id: k02999 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02999_command-development.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\plugin-dev\c2bdb427efe8\skills\command-development\SKILL.md) · 884 satır · araç adları (1): command-development
BAŞLIKLAR: # Command Development for Claude Code · ## Overview · ## Command Basics · ### What is a Slash Command? · ### Critical: Commands are Instructions FOR Claude · ### Command Locations · ## File Format · ### Basic Structure · ### With YAML Frontmatter · ## YAML Frontmatter Fields · ### description · ### allowed-tools · ### model · ### argument-hint · ### disable-model-invocation · ## Dynamic Arguments · ### Using $ARGUMENTS · ### Using Positional Arguments · ### Combining Arguments · ## File References · ### Using @ Syntax · ### Multiple File References · Reference multiple files: · Identify: · ### Static File References · Ensure: · ## Bash Execution in Commands · ## Command Organization · ### Flat Structure · ### Namespaced Structure · ## Best Practices · ### Command Design · ### Argument Handling · ### File References · ### Bash Commands · ### Documentation · ## Common Patterns · ### Review Pattern · Review each file for: · ### Testing Pattern · ### Documentation Pattern · ### Workflow Pattern · ## Troubleshooting · ## Plugin-Specific Features · ### CLAUDE_PLUGIN_ROOT Variable · # Execute plugin script · # Load plugin configuration · # Use plugin template · # Access plugin resources · ### Plugin Command Organization · ### Plugin Command Patterns · ## Integration with Plugin Components · ### Agent Integration · The agent will analyze: · Agent uses plugin resources: · ### Skill Integration · ### Hook Coordination · ### Multi-Component Workflows · ## Validation Patterns · ### Argum

## plugin-structure
id: k03003 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03003_plugin-structure.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\plugin-dev\c2bdb427efe8\skills\plugin-structure\SKILL.md) · 476 satır · araç adları (1): plugin-structure
BAŞLIKLAR: # Plugin Structure for Claude Code · ## Overview · ## Directory Structure · ## Plugin Manifest (plugin.json) · ### Required Fields · ### Recommended Metadata · ### Component Path Configuration · ## Component Organization · ### Commands · ### Agents · ### Skills · ### Hooks · ### MCP Servers · ## Portable Path References · ### ${CLAUDE_PLUGIN_ROOT} · ### Path Resolution Rules · # ${CLAUDE_PLUGIN_ROOT} available as environment variable · ## File Naming Conventions · ### Component Files · ### Supporting Files · ## Auto-Discovery Mechanism · ## Best Practices · ### Organization · ### Naming · ### Portability · ### Maintenance · ## Common Patterns · ### Minimal Plugin · ### Full-Featured Plugin · ### Skill-Focused Plugin · Plugin providing only skills: · ## Troubleshooting

## code-simplification
id: k01330 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01330_code-simplification.txt (özgün: C:\Users\pc\.claude\plugins\cache\addy-agent-skills\agent-skills\0.6.10\skills\code-simplification\SKILL.md) · 331 satır · araç adları (1): code-simplification
BAŞLIKLAR: # Code Simplification · ## Overview · ## When to Use · ## The Five Principles · ### 1. Preserve Behavior Exactly · ASK BEFORE EVERY CHANGE: · ### 2. Follow Project Conventions · ### 3. Prefer Clarity Over Cleverness · ### 4. Maintain Balance · ### 5. Scope to What Changed · ## The Simplification Process · ### Step 1: Understand Before Touching (Chesterton's Fence) · ### Step 2: Identify Simplification Opportunities · ### Step 3: Apply Changes Incrementally · FOR EACH SIMPLIFICATION: · ### Step 4: Verify the Result · COMPARE BEFORE AND AFTER: · ## Language-Specific Guidance · ### TypeScript / JavaScript · ### Python · # SIMPLIFY: Verbose dictionary building · # Before · # After · # SIMPLIFY: Nested conditionals with early return · # Before · # After · ### React / JSX · ## Common Rationalizations · ## Red Flags · ## Verification

## katalog_yenile
id: k03438 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03438_katalog_yenile.txt (özgün: C:\Projeler\omer-skills\tools\katalog_yenile.py) · 257 satır · araç adları (1): katalog_yenile
BAŞLIKLAR: 

## configure-ecc
id: k03667 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03667_configure-ecc.txt (özgün: C:\Projeler\omer-skills\dist\yukle-12-kirmizi\ecc-configure-ecc.zip!configure-ecc/SKILL.md) · 206 satır · araç adları (2): configure-ecc · ecc-configure-ecc.zip!configure-ecc
BAŞLIKLAR: # Configure ECC · ## Route by the current harness · ## Claude Code: run the full conversational wizard · ### 1. Inventory without changing anything · ### 2. Collect exactly two choices · ### 3. Preview and confirm once · ### 4. Apply the explicit choices · Fallback: · ### 5. Verify, then render the welcome · ## Codex: use the native plugin lifecycle · ## Kimi: install the project surface

## plan-readiness-review
id: k02978 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02978_plan-readiness-review.txt (özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-readiness-reviews\1.0.0\skills\plan-readiness-review\SKILL.md) · 166 satır · araç adları (1): plan-readiness-review
BAŞLIKLAR: # Plan readiness review · ## Phase 0 — Input contract · ## Phase 1 — Requirement inventory · ## Phase 2 — Per-requirement readiness test · ## Phase 3 — Cross-cutting sweeps · ## Phase 4 — Falsification pass · ## Severity rubric · ## Output · ## Working on the fixes

## pathfinder
id: k01554 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k01554_pathfinder.txt (özgün: C:\Users\pc\.claude\plugins\cache\thedotmack\claude-mem\13.31.0\skills\pathfinder\SKILL.md) · 111 satır · araç adları (1): pathfinder
BAŞLIKLAR: # Pathfinder · ## Delegation Model · ### Subagent Reporting Contract (MANDATORY) · ## Output Artifacts · ## Phases · ### Phase 0: Feature Discovery (ALWAYS FIRST) · ### Phase 1: Per-Feature Flowcharts (FAN OUT) · ### Phase 2: Duplication Hunt · ### Phase 3: Unified Proposal (ORCHESTRATOR) · ### Phase 4: Per-System Handoff Prompts · ## Key Principles · ## Failure Modes to Prevent

## gsd-paket
id: k00277 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00277_gsd-paket.txt (özgün: C:\Users\pc\.claude\skills\gsd-paket\SKILL.md) · 85 satır · araç adları (2): gsd · gsd-paket
BAŞLIKLAR: # gsd-paket

## departman-surec-plan
id: k03609 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03609_departman-surec-plan.txt (özgün: C:\Projeler\omer-skills\dist\token-10\departman-surec-plan.zip!departman-surec-plan/SKILL.md) · 60 satır · araç adları (2): departman-surec-plan · departman-surec-plan.zip!departman-surec-plan
BAŞLIKLAR: # Departman: surec-plan — iş sırası · ## Adımlar · ## Kapılar · ## Çakışma · ## Profil dışı üyeler (yalnız CC) · ## Dizin · ### claude.ai + Claude Code · ### yalnız Claude Code

## orch-refine-code
id: k02092 · tür: skill · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02092_orch-refine-code.txt (özgün: C:\Users\pc\.claude\plugins\cache\ecc\ecc\2.2.3\skills\orch-refine-code\SKILL.md) · 44 satır · araç adları (1): orch-refine-code
BAŞLIKLAR: # orch-refine-code · ## When to Use · ## Operation settings · ## How It Works · ## Example

## inc-uretim-hazirligi
id: k00978 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00978_inc-uretim-hazirligi.txt (özgün: C:\Users\pc\.claude\agents\inc-uretim-hazirligi.md) · 28 satır · araç adları (1): inc-uretim-hazirligi
BAŞLIKLAR: Kurallar:

## ajn-prompt-denetci
id: k00670 · tür: agent · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00670_ajn-prompt-denetci.txt (özgün: C:\Users\pc\.claude\agents\ajn-prompt-denetci.md) · 21 satır · araç adları (1): ajn-prompt-denetci
BAŞLIKLAR: Kurallar:

## skill-ui
id: k04267 · tür: cli · katman: A · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04267_skill-ui.txt (özgün: C:\Users\pc\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.19.0-win-x64\skill-ui.CMD) · 17 satır · araç adları (1): skill-ui
BAŞLIKLAR: 
