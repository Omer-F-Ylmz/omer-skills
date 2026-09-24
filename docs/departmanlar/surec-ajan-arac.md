# Departman: surec-ajan-arac

> Skill/plugin/MCP/hook/agent geliştirme, Claude Code ve ajan yardımcıları, genel CLI araçları.

Müdür: `departman-surec-ajan-arac`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| bun | cli | - | - | - |
| bunx | cli | - | - | - |
| jev | cli | - | - | Doğrulama |
| node | cli | - | - | - |
| npm | cli | - | - | - |
| npx | cli | - | - | - |
| python | cli | - | - | - |
| skill-ui | cli | - | - | - |
| uv | cli | - | - | - |
| uvx | cli | - | - | - |
| jev | mcp | - | - | Doğrulama |
| mcp-filesystem | mcp | - | - | - |
| mcp-sequential-thinking | mcp | - | - | - |
| mcp-time | mcp | - | - | - |
| agent-sdk-dev | plugin | Claude Agent SDK Development Plugin | - | Doğrulama |
| agent-skills | plugin | Production-grade engineering skills for AI coding agents — covering the full software dev… | - | - |
| andrej-karpathy-skills | plugin | Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy'… | - | - |
| claude-api | plugin | - | - | Doğrulama |
| claude-md-management | plugin | Tools to maintain and improve CLAUDE.md files - audit quality, capture session learnings,… | - | - |
| claude-opus-4-5-migration | plugin | Migrate your code and prompts from Sonnet 4.x and Opus 4.1 to Opus 4.5. | - | - |
| cli-anything | plugin | Build powerful, stateful CLI interfaces for any GUI application using the cli-anything ha… | - | - |
| discernment-nudge | plugin | - | - | - |
| everything-claude-code | plugin | Complete collection of battle-tested Claude Code configs from an Anthropic hackathon winn… | - | - |
| example-skills | plugin | - | - | - |
| feature-dev | plugin | Comprehensive feature development workflow with specialized agents for codebase explorati… | - | - |
| hookify | plugin | Easily create hooks to prevent unwanted behaviors by analyzing conversation patterns | - | Skill |
| plugin-dev | plugin | Plugin development toolkit with skills for creating agents, commands, hooks, MCP integrat… | - | - |
| ralph-wiggum | plugin | Implementation of the Ralph Wiggum technique - continuous self-referential AI loops for i… | - | - |
| skill-creator | plugin | Create new skills, improve existing skills, and measure skill performance. | Use when users want to create a skill from scratch, update or optimize an existing skill,… | MCP |
| superpowers | plugin | Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven t… | - | - |
| typesafe | plugin | Agent skills for building with the TypeSafe System One API. | - | - |
| _gstack-command | skill | Router for the gstack skill suite. | - | - |
| agent-skills:deprecation-and-migration | skill | Manages deprecation and migration. | Use when removing old systems, APIs, or features | - |
| agent-skills:incremental-implementation | skill | Delivers changes incrementally in thin, verifiable slices. | Use when implementing any feature or change that touches more than one file, or when pick… | - |
| agent-skills:using-agent-skills | skill | Discovers and invokes agent skills. | Use when starting a session, or when you need to decide which skill or workflow applies t… | - |
| anthropic-skills:config-codex-cli | skill | Step-by-step agent workflow to configure the OpenAI Codex CLI on any machine (Linux, macO… | - | - |
| anthropic-skills:jev | skill | Jev (TypeSafe) tipli yargı: çok öğeli sınıflandırma/puanlama, kalibre olasılık, ikinci gö… | - | Doğrulama |
| anthropic-skills:sdp | skill | Yalniz Divisima reposunda (C:\\Users\\pc\\Desktop\\smart\\Divisima.Solution) kullanilir; … | - | - |
| anthropic-skills:skill-ui-cli | skill | Use when an agent or desktop AI client needs to discover/list available skills, compare d… | Use when an agent or desktop AI client needs to discover/list available skills, compare d… | - |
| anthropic-skills:skill-ui-desktop | skill | skill-ui CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşma… | - | - |
| anthropic-skills:task-observer | skill | Monitors task execution for skill improvement opportunities during any multi-step or agen… | - | - |
| claude-api:claude-api | skill | Reference for the Claude API / Anthropic SDK — model ids, pricing, params, streaming, too… | - | Doğrulama |
| claude-md-management:claude-md-improver | skill | Audit and improve CLAUDE.md files in repositories. | Use when user asks to check, audit, update, improve, or fix CLAUDE | - |
| claude-mem:ccs-align | skill | Run the CCS Align seat's hourly breathing cycle — prove the local claude-mem worker is he… | - | - |
| claude-mem:mode-creator | skill | Interactively create, install, activate, and verify custom claude-mem modes, including do… | - | - |
| claude-mem:what-the | skill | What the? | Use when the user wants a plain-English breakdown of something technical — the who, what,… | - |
| claude-opus-4-5-migration:claude-opus-4-5-migration | skill | Migrate prompts and code from Claude Sonnet 4.0, Sonnet 4.5, or Opus 4.1 to Opus 4.5. | Use when the user wants to update their codebase, prompts, or API calls to use Opus 4 | - |
| codex | skill | OpenAI Codex CLI wrapper — three modes. | - | - |
| discernment-nudge:discernment-nudge | skill | After you give a substantive answer or draft that the user may act on — advice or recomme… | - | - |
| everything-claude-code:continuous-learning | skill | Automatically extract reusable patterns from Claude Code sessions and save them as learne… | - | - |
| everything-claude-code:project-guidelines-example | skill | This is an example of a project-specific skill. | Use this as a template for your own projects | - |
| example-skills:mcp-builder | skill | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to … | Use when building MCP servers to integrate externa | Claude API / ajan |
| example-skills:skill-creator | skill | Create new skills, modify and improve existing skills, and measure skill performance. | Use when users want to create a skill from scratch, edit, or optimize an existing skill, … | MCP |
| freeze | skill | Restrict file edits to a specific directory for the session. | - | - |
| gstack | skill | Router for the gstack skill suite. | - | - |
| gstack-upgrade | skill | Upgrade gstack to the latest version. | - | - |
| hookify:writing-rules | skill | This skill should be used when the user asks to "create a hookify rule", "write a hook ru… | - | - |
| ios-sync | skill | Regenerate the iOS debug bridge against the latest upstream gstack templates. | - | - |
| learn | skill | Manage project learnings. | - | - |
| pair-agent | skill | Pair a remote AI agent with your browser. | - | - |
| plan-tune | skill | Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). | - | - |
| plugin-dev:agent-development | skill | This skill should be used when the user asks to "create an agent", "add an agent", "write… | - | - |
| plugin-dev:command-development | skill | This skill should be used when the user asks to "create a slash command", "add a command"… | - | - |
| plugin-dev:hook-development | skill | This skill should be used when the user asks to "create a hook", "add a PreToolUse/PostTo… | - | Skill |
| plugin-dev:mcp-integration | skill | This skill should be used when the user asks to "add MCP server", "integrate MCP", "confi… | - | Claude API / ajan |
| plugin-dev:plugin-settings | skill | This skill should be used when the user asks about "plugin settings", "store plugin confi… | - | - |
| plugin-dev:plugin-structure | skill | This skill should be used when the user asks to "create a plugin", "scaffold a plugin", "… | - | Skill |
| plugin-dev:skill-development | skill | This skill should be used when the user wants to "create a skill", "add a skill to plugin… | - | MCP |
| setup-gbrain | skill | Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supaba… | - | - |
| skill-creator:skill-creator | skill | Create new skills, modify and improve existing skills, and measure skill performance. | Use when users want to create a skill from scratch, edit, or optimize an existing skill, … | MCP |
| skillify | skill | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. | - | - |
| superpowers:diagnosing-superpowers | skill | Use when a superpowers session went wrong and your human partner wants to know why — repe… | Use when a superpowers session went wrong and your human partner wants to know why — repe… | - |
| superpowers:subagent-driven-development | skill | Use when executing implementation plans with independent tasks in the current session | Use when executing implementation plans with independent tasks in the current session | - |
| superpowers:using-superpowers | skill | Use when starting any conversation - establishes how to find and use skills, requiring sk… | Use when starting any conversation - establishes how to find and use skills, requiring sk… | - |
| superpowers:writing-skills | skill | Use when creating new skills, editing existing skills, or verifying skills work before de… | Use when creating new skills, editing existing skills, or verifying skills work before de… | MCP |
| sync-gbrain | skill | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. | - | - |
| taste-skill:output-skill | skill | Overrides default LLM truncation behavior. | - | - |
| typesafe:typesafe-ai | skill | Build AI-powered software with TypeSafe: small units of AI intelligence you can use like … | - | - |
| unfreeze | skill | Clear the freeze boundary set by /freeze, allowing edits to all directories again. | - | - |

## Videodan gelen

- neden-ver · ZATEN VAR · video vcU85OrwuV0
- hyperagent · RED · video vcU85OrwuV0
- caveman-secici · ÖĞREN · video jf1sv2geEWo
- ozel-skill-olusturma · ZATEN VAR · video jf1sv2geEWo
- php-artisan-make-enum · RED · video jf1sv2geEWo
- pint · RED · video jf1sv2geEWo

## Elle
