# Departman: verimlilik

> Token/context tasarrufu, çıktı sıkıştırma, oturum hafızası, maliyet düşürme, ajan verimliliği.

Müdür: `departman-verimlilik`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| headroom | cli | - | - | Keşif |
| rtk | cli | - | - | Büyük içerik |
| headroom | mcp | - | - | Keşif |
| mcp-memory | mcp | - | - | - |
| claude-md-management | plugin | Tools to maintain and improve CLAUDE.md files - audit quality, capture session learnings,… | - | - |
| claude-mem | plugin | Memory compression system for Claude Code - persist context across sessions | - | - |
| headroom | plugin | Headroom startup hooks for Claude Code and GitHub Copilot CLI. | - | Keşif |
| agent-skills:context-engineering | skill | Optimizes agent context setup. | Use when starting a new session, when agent output quality degrades, when switching betwe… | - |
| anthropic-skills:vercel-optimize | skill | Vercel cost and performance optimization for Next.js/SvelteKit/Nuxt/Astro: collect metric… | - | - |
| claude-api:claude-api | skill | Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, too… | - | - |
| claude-mem:cloud-sync | skill | Set up or check claude-mem cloud sync with cmem.ai Pro. | Use when the user says "set up cloud sync", "sync my memories", "cmem pro", "cloud backup… | - |
| claude-mem:how-it-works | skill | Explain how claude-mem captures observations, when memory injection kicks in, and where d… | Use when the user asks "how does claude-mem work?" or "what is this thing doing?" | - |
| claude-mem:knowledge-agent | skill | Build and query AI-powered knowledge bases from claude-mem observations. | Use when users want to create focused "brains" from their observation history, ask questi… | - |
| claude-mem:mem-search | skill | Search claude-mem's persistent cross-session memory database. | Use when user asks "did we already solve this?", "how did we do X last time?", or needs w… | Context |
| claude-mem:smart-explore | skill | Token-optimized structural code search using tree-sitter AST parsing. | - | Hafıza |
| context-restore | skill | Restore working context saved earlier by /context-save. | - | Context |
| context-save | skill | Save working context. | - | Context |
| everything-claude-code:strategic-compact | skill | Suggests manual context compaction at logical intervals to preserve context through task … | - | - |
| ponytail:ponytail-gain | skill | Show ponytail's measured impact as a compact scoreboard: less code, less cost, more speed… | Trigger: /pon | - |
| superpowers:dispatching-parallel-agents | skill | Use when facing 2+ independent tasks that can be worked on without shared state or sequen… | Use when facing 2+ independent tasks that can be worked on without shared state or sequen… | - |

## Elle
