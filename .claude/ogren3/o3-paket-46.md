## built-in-browser
id: k03776 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03776_built-in-browser.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): built-in-browser · claudeai_adlar
BAŞLIKLAR: 

## gstack-learn
id: k03854 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03854_gstack-learn.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · gstack-learn
BAŞLIKLAR: 

## plugin-dev-agent-creator
id: k03911 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03911_plugin-dev-agent-creator.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · plugin-dev-agent-creator
BAŞLIKLAR: 

## writing-for-agents
id: k04065 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k04065_writing-for-agents.txt (özgün: .kos/kopru/claudeai_adlar.json) · 1597 satır · araç adları (2): claudeai_adlar · writing-for-agents
BAŞLIKLAR: 

## prompt-master
id: k00472 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00472_prompt-master.txt (özgün: C:\Users\pc\.claude\skills\prompt-master\SKILL.md) · 496 satır · araç adları (1): prompt-master
BAŞLIKLAR: ## PRIMACY ZONE — Identity, Hard Rules, Output Lock · Output format: · ## MIDDLE ZONE — Execution Logic, Tool Routing, Diagnostics · ### Intent Extraction · ### Tool Routing · ### Model Recency Gate · ### Credential Safety · ### Input Sanitization -- Pasted Prompts · ### Diagnostic Checklist · ### Memory Block · ## Context (carry forward) · ### Safe Techniques — Apply Only When Genuinely Needed · ### Agentic Output Warning · ## RECENCY ZONE — Verification and Success Lock · ## Reference Files

## sentry-sdk-skill-creator
id: k00542 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00542_sentry-sdk-skill-creator.txt (özgün: C:\Users\pc\.claude\skills\sentry-sdk-skill-creator\SKILL.md) · 326 satır · araç adları (1): sentry-sdk-skill-creator
BAŞLIKLAR: # Create a Sentry SDK Skill Bundle · ## Invoke This Skill When · ## Phase 1: Identify the SDK · # What SDK? What's the package name? · # Examples: sentry-go, @sentry/sveltekit, sentry-python, sen · # Read 1-2 existing SDK skills for pattern reference · ## Phase 2: Research · ### Research Strategy · ### Research the Sentry Wizard · # Check the SDK's docs landing page for wizard instructions · # Visit: https://docs.sentry.io/platforms/<platform>/ · # Look for: "npx @sentry/wizard@latest -i <integration>" · If a wizard integration exists: · ### Research Batching · ### Research Quality Gate · # Quick verification · ## Phase 3: Create the Main SKILL.md · ### Gather Context First · ### SKILL.md Structure · # Sentry <Platform> SDK · ## Invoke This Skill When · ## Phase 1: Detect · ## Phase 2: Recommend · ## Phase 3: Guide · ### Option 1: Wizard (Recommended)   ← if wizard exists for  · ### Option 2: Manual Setup            ← always include · ### Install · ### Quick Start — Recommended Init · ### Source Maps Setup                  ← required for fronte · ### Framework Middleware (if applicable) · ### For Each Agreed Feature · ## Configuration Reference · ## Verification · ## Phase 4: Cross-Link · ## Troubleshooting · ### Key Principles for the Main SKILL.md · ## Phase 4: Create Reference Files · ### Reference File Structure · # <Feature> — Sentry <Platform> SDK · ## Configuration · ## Code Examples · ### Basic usage · ### Advanced patterns · ### Framework-specific notes (if applicabl

## build-mcp-server
id: k02683 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k02683_build-mcp-server.txt (özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\mcp-server-dev\c2bdb427efe8\skills\build-mcp-server\SKILL.md) · 221 satır · araç adları (1): build-mcp-server
BAŞLIKLAR: # Build an MCP Server · ## Phase 1 — Interrogate the use case · ### 1. What does it connect to? · ### 2. Who will use it? · ### 3. How many distinct actions does it expose? · ### 4. Does a tool need mid-call user input or rich display? · ### 5. What auth does the upstream service use? · ## Phase 2 — Recommend a deployment model · ### ⭐ Remote streamable-HTTP MCP server (default recommendat · ### Elicitation (structured input, no UI build) · ### MCP app (remote HTTP + interactive UI) · ### MCPB (bundled local server) · ### Local stdio (npx / uvx) — *not recommended for distribut · ## Phase 3 — Pick a tool-design pattern · ### Pattern A: One tool per action (small surface) · ### Pattern B: Search + execute (large surface) · ## Phase 4 — Pick a framework · ## Phase 5 — Scaffold and hand off · ## Beyond tools — the other primitives · ## Phase 6 — Test in Claude and publish · Once the server runs: · ## Quick reference: decision matrix · ## Reference files

## pr-writer
id: k00464 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00464_pr-writer.txt (özgün: C:\Users\pc\.claude\skills\pr-writer\SKILL.md) · 160 satır · araç adları (1): pr-writer
BAŞLIKLAR: # PR Writer · ## Inspect the Change · ## Core Rules · ## Titles · ## Body Shape · Choose the minimum useful shape: · Default: · ## Reviewer Aids · ## Boundaries · ## Create or Update · ## Examples · Small change: · Breaking contract: · Before: · After:

## Software Architect
id: k00893 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00893_Software_Architect.txt (özgün: C:\Users\pc\.claude\agents\engineering-software-architect.md) · 118 satır · araç adları (3): Software Architect · engineering-software-architect · sa
BAŞLIKLAR: ## Ders bankası · # Software Architect Agent · ## 🧠 Your Identity & Memory · ## 🎯 Your Core Mission · ## 🔧 Critical Rules · ## 📋 Architecture Decision Record Template · # ADR-001: [Decision Title] · ## Status · ## Context · ## Decision · ## Consequences · ## 🏗️ System Design Process · ### 1. Domain Discovery · ### 2. Domain Modeling Guidance · ### 3. Architecture Selection · ### 4. Dependency & Boundary Rules · ### 5. Quality Attribute Analysis · ## 💬 Communication Style

## kurulum-turu-5b-1
id: k03450 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03450_kurulum-turu-5b-1.txt (özgün: C:\Projeler\omer-skills\tools\kurulum-turu-5b-1.sh) · 95 satır · araç adları (1): kurulum-turu-5b-1
BAŞLIKLAR: # Kurulum turu 5b-1 — tur-5b-1 KUR: expo/skills plugin "expo · # Kullanım: bash tools/kurulum-turu-5b-1.sh [--kuru]   (--ku · # Her adım: kuruluysa atla → kur → doğrula → hata ise yalnız · # klonla repo sha → KD (pinli SHA'da klon) · # uzaktan betik çeken/çalıştıran dosya (md hariç) varsa şüph · # S|repo|sha|alt-yol|atlanacak-adlar   → alt-yol altındaki S · # P|repo|sha|market|plugin-adları   → yalnız listelenen plug

## jev
id: k03377 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03377_jev.txt (özgün: C:\Projeler\omer-skills\skills\jev\SKILL.md) · 59 satır · araç adları (1): jev
BAŞLIKLAR: # Jev — tipli yargı aracı · ## Ne zaman çağır · ## Ne zaman çağırma · ## Soru yazımı · ## Güven (choice/score `confidence`; noul'da max(p, 1-p)) · ## Ömer haritası · ## Yargıç / eşdeğerlik (JEV-1 ölçümü, 2026-10-11) · ## Türkçe · ## Referanslar

## triage
id: k00617 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00617_triage.txt (özgün: C:\Users\pc\.claude\skills\triage\SKILL.md) · 30 satır · araç adları (1): triage
BAŞLIKLAR: # Herdr Issue Triage · Use this table shape: · Classify with these lights:

## inc-refaktor
id: k00974 · tür: agent · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00974_inc-refaktor.txt (özgün: C:\Users\pc\.claude\agents\inc-refaktor.md) · 21 satır · araç adları (1): inc-refaktor
BAŞLIKLAR: Kurallar:

## davila7-ai-maestro-paket
id: k00175 · tür: skill · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k00175_davila7-ai-maestro-paket.txt (özgün: C:\Users\pc\.claude\skills\davila7-ai-maestro-paket\SKILL.md) · 19 satır · araç adları (2): davila7-ai-maestro · davila7-ai-maestro-paket
BAŞLIKLAR: # davila7-ai-maestro-paket

## skill-paket
id: k03479 · tür: cli · katman: C · kaynak: C:\Projeler\omer-skills\.claude\ogren3\o3-kaynak\k03479_skill-paket.txt (özgün: C:\Projeler\omer-skills\tools\skill-paket) · 0 satır · araç adları (13): ekle.py · envanter.py · paketle.py · skill · skill-paket · tek-sefer/aile_paket.py · tek-sefer/ecc_paket.py · tek-sefer/p3.py · tek-sefer/tek_skillmd.py · test_envanter.py · test_paketle.py · test_zip_denetle.py · zip_denetle.py
BAŞLIKLAR: 
