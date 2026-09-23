# Departman: surec

> Planlama, spec, kod review, git/commit/PR, CI, yayın/deploy, iş akışı ve skill/plugin yazımı.

Müdür: `departman-surec`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| agent-reach | cli | - | - | - |
| bun | cli | - | - | - |
| bunx | cli | - | - | - |
| gh | cli | - | - | - |
| git | cli | - | - | - |
| node | cli | - | - | - |
| npm | cli | - | - | - |
| uv | cli | - | - | - |
| uvx | cli | - | - | - |
| vercel | cli | - | - | - |
| code-review | mcp | - | - | Git |
| github | mcp | - | - | - |
| mcp-filesystem | mcp | - | - | - |
| mcp-git | mcp | - | - | - |
| mcp-sequential-thinking | mcp | - | - | - |
| mcp-time | mcp | - | - | - |
| agent-sdk-dev | plugin | Claude Agent SDK Development Plugin | - | - |
| agent-skills | plugin | Production-grade engineering skills for AI coding agents — covering the full software dev… | - | - |
| andrej-karpathy-skills | plugin | Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy'… | - | - |
| claude-api | plugin | - | - | - |
| claude-opus-4-5-migration | plugin | Migrate your code and prompts from Sonnet 4.x and Opus 4.1 to Opus 4.5. | - | - |
| cli-anything | plugin | Build powerful, stateful CLI interfaces for any GUI application using the cli-anything ha… | - | - |
| code-review | plugin | Automated code review for pull requests using multiple specialized agents with confidence… | - | Git |
| commit-commands | plugin | Streamline your git workflow with simple commands for committing, pushing, and creating p… | - | - |
| discernment-nudge | plugin | - | - | - |
| everything-claude-code | plugin | Complete collection of battle-tested Claude Code configs from an Anthropic hackathon winn… | - | - |
| example-skills | plugin | - | - | - |
| feature-dev | plugin | Comprehensive feature development workflow with specialized agents for codebase explorati… | - | - |
| hookify | plugin | Easily create hooks to prevent unwanted behaviors by analyzing conversation patterns | - | - |
| phoenix-readiness-reviews | plugin | Two adversarial review gates. | - | - |
| plugin-dev | plugin | Plugin development toolkit with skills for creating agents, commands, hooks, MCP integrat… | - | - |
| ponytail | plugin | Lazy senior dev mode. | - | Review |
| pr-review-toolkit | plugin | Comprehensive PR review agents specializing in comments, tests, error handling, type desi… | - | - |
| ralph-wiggum | plugin | Implementation of the Ralph Wiggum technique - continuous self-referential AI loops for i… | - | - |
| skill-creator | plugin | Create new skills, improve existing skills, and measure skill performance. | Use when users want to create a skill from scratch, update or optimize an existing skill,… | - |
| superpowers | plugin | Core skills library for Claude Code: TDD, debugging, collaboration patterns, and proven t… | - | - |
| typesafe | plugin | Agent skills for building with the TypeSafe System One API. | - | - |
| _gstack-command | skill | Router for the gstack skill suite. | - | - |
| agent-skills:ci-cd-and-automation | skill | Automates CI/CD pipeline setup. | Use when setting up or modifying build and deployment pipelines | - |
| agent-skills:code-review-and-quality | skill | Conducts multi-axis code review. | Use before merging any change | - |
| agent-skills:code-simplification | skill | Simplifies code for clarity. | Use when refactoring code for clarity without changing behavior | - |
| agent-skills:constraint-driven-development | skill | Establishes a project's quality bar as a written contract and stops agents quietly loweri… | - | - |
| agent-skills:deprecation-and-migration | skill | Manages deprecation and migration. | Use when removing old systems, APIs, or features | - |
| agent-skills:doubt-driven-development | skill | Subjects every non-trivial decision to a fresh-context adversarial review before it stand… | Use when you want every assumption cross-examined before proceeding, when stress-testing … | - |
| agent-skills:git-workflow-and-versioning | skill | Structures git workflow practices. | Use when making any code change | - |
| agent-skills:idea-refine | skill | Refines raw ideas into sharp, actionable concepts through structured divergent and conver… | Use when an idea is still vague, when you need to stress-test assumptions before committi… | - |
| agent-skills:incremental-implementation | skill | Delivers changes incrementally in thin, verifiable slices. | Use when implementing any feature or change that touches more than one file, or when pick… | - |
| agent-skills:interview-me | skill | Extracts what the user actually wants instead of what they think they should want. | Use when an | - |
| agent-skills:planning-and-task-breakdown | skill | Breaks work into ordered tasks. | Use when you have a spec or clear requirements and need to break work into implementable … | - |
| agent-skills:shipping-and-launch | skill | Prepares production launches. | Use when preparing to deploy to production, or when asking what needs to be in place befo… | - |
| agent-skills:spec-driven-development | skill | Creates specs before coding. | Use when starting a new project, feature, or significant change and no specification exis… | Plan |
| agent-skills:using-agent-skills | skill | Discovers and invokes agent skills. | Use when starting a session, or when you need to decide which skill or workflow applies t… | - |
| andrej-karpathy-skills:karpathy-guidelines | skill | Behavioral guidelines to reduce common LLM coding mistakes. | Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical… | - |
| anthropic-skills:agent-reach-desktop | skill | agent-reach CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında ko… | - | - |
| anthropic-skills:code-review-skill | skill | Code review guidance across React, Vue, Angular, Svelte, Rust, TypeScript, Java, PHP, Rub… | - | - |
| anthropic-skills:config-codex-cli | skill | Step-by-step agent workflow to configure the OpenAI Codex CLI on any machine (Linux, macO… | - | - |
| anthropic-skills:context7-cli | skill | Use the ctx7 CLI to fetch library documentation, manage AI coding skills, and configure C… | - | - |
| anthropic-skills:deploy-to-vercel | skill | Deploy applications and websites to Vercel. | Use when the user requests deployment actions like "deploy my app", "deploy and give me t… | - |
| anthropic-skills:graphify-desktop | skill | graphify CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşma… | - | - |
| anthropic-skills:jev | skill | Jev (TypeSafe) tipli yargı: çok öğeli sınıflandırma/puanlama, kalibre olasılık, ikinci gö… | - | - |
| anthropic-skills:rtk-desktop | skill | rtk CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. | - | - |
| anthropic-skills:sdp | skill | Yalniz Divisima reposunda (C:\\Users\\pc\\Desktop\\smart\\Divisima.Solution) kullanilir; … | - | - |
| anthropic-skills:semgrep-desktop | skill | semgrep CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. | - | - |
| anthropic-skills:skill-ui-cli | skill | Use when an agent or desktop AI client needs to discover/list available skills, compare d… | Use when an agent or desktop AI client needs to discover/list available skills, compare d… | - |
| anthropic-skills:skill-ui-desktop | skill | skill-ui CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşma… | - | - |
| anthropic-skills:superpowers-executing-plans | skill | Use when executing an implementation plan in the current session as the implementer yours… | Use when executing an implementation plan in the current session as the implementer yours… | - |
| anthropic-skills:surec | skill | Yalniz Divisima reposunda (C:\\Users\\pc\\Desktop\\smart\\Divisima.Solution) kullanilir; … | - | - |
| anthropic-skills:task-observer | skill | Monitors task execution for skill improvement opportunities during any multi-step or agen… | - | - |
| anthropic-skills:vercel-cli-with-tokens | skill | Deploy and manage Vercel projects with token-based auth instead of interactive login. | Use for deploy to vercel, set up vercel, or add environment variables to vercel | - |
| autoplan | skill | Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk an… | - | - |
| canary | skill | Post-deploy canary monitoring. | - | Kapanış |
| claude-md-management:claude-md-improver | skill | Audit and improve CLAUDE.md files in repositories. | Use when user asks to check, audit, update, improve, or fix CLAUDE | - |
| claude-mem:babysit | skill | Watch a pull request or review cycle until it is ready to merge. | Use when asked to babysit, monitor, or keep checking PR comments, reviews, and CI until a… | - |
| claude-mem:ccs-align | skill | Run the CCS Align seat's hourly breathing cycle — prove the local claude-mem worker is he… | - | - |
| claude-mem:do | skill | Execute a phased implementation plan using subagents. | Use when asked to execute, run, or carry out a plan — especially one created by make-plan | - |
| claude-mem:make-plan | skill | Create a detailed, phased implementation plan with documentation discovery. | Use when asked to plan a feature, task, or multi-step implementation — especially before … | - |
| claude-mem:mode-creator | skill | Interactively create, install, activate, and verify custom claude-mem modes, including do… | - | - |
| claude-mem:oh-my-issues | skill | Cluster a GitHub issue backlog by root cause into a small set of plan-master issues, redi… | - | - |
| claude-mem:pathfinder | skill | Map a codebase into feature-grouped flowcharts, identify duplicated concerns across featu… | Use when asked to "find the ideal path," unify duplicated systems, or | - |
| claude-mem:standup | skill | Facilitate a read-only standup across git worktrees, branches, or PRs to compare changes … | - | - |
| claude-mem:version-bump | skill | Automated semantic versioning and release workflow for Claude Code plugins. | - | - |
| claude-mem:what-the | skill | What the? | Use when the user wants a plain-English breakdown of something technical — the who, what,… | - |
| claude-opus-4-5-migration:claude-opus-4-5-migration | skill | Migrate prompts and code from Claude Sonnet 4.0, Sonnet 4.5, or Opus 4.1 to Opus 4.5. | Use when the user wants to update their codebase, prompts, or API calls to use Opus 4 | - |
| codex | skill | OpenAI Codex CLI wrapper — three modes. | - | - |
| devex-review | skill | Live developer experience audit. | - | - |
| discernment-nudge:discernment-nudge | skill | After you give a substantive answer or draft that the user may act on — advice or recomme… | - | - |
| everything-claude-code:coding-standards | skill | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, Reac… | - | - |
| everything-claude-code:continuous-learning | skill | Automatically extract reusable patterns from Claude Code sessions and save them as learne… | - | - |
| everything-claude-code:project-guidelines-example | skill | This is an example of a project-specific skill. | Use this as a template for your own projects | - |
| example-skills:mcp-builder | skill | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to … | Use when building MCP servers to integrate externa | - |
| example-skills:skill-creator | skill | Create new skills, modify and improve existing skills, and measure skill performance. | Use when users want to create a skill from scratch, edit, or optimize an existing skill, … | - |
| freeze | skill | Restrict file edits to a specific directory for the session. | - | - |
| graphify | skill | Use for any question about a codebase, its architecture, file relationships, or project c… | Use for any question about a codebase, its architecture, file relationships, or project c… | - |
| gstack | skill | Router for the gstack skill suite. | - | - |
| gstack-upgrade | skill | Upgrade gstack to the latest version. | - | - |
| health | skill | Code quality dashboard. | - | - |
| hookify:writing-rules | skill | This skill should be used when the user asks to "create a hookify rule", "write a hook ru… | - | - |
| ios-sync | skill | Regenerate the iOS debug bridge against the latest upstream gstack templates. | - | - |
| land-and-deploy | skill | Land and deploy workflow. | - | Kapanış |
| landing-report | skill | Read-only queue dashboard for workspace-aware ship. | - | - |
| learn | skill | Manage project learnings. | - | - |
| office-hours | skill | YC Office Hours — two modes. | - | - |
| pair-agent | skill | Pair a remote AI agent with your browser. | - | - |
| phoenix-prd-pipeline:phoenix-batch-planner | skill | Role 09 of the Phoenix Security spec pipeline. | - | - |
| phoenix-prd-pipeline:phoenix-orchestrator | skill | Run the full Phoenix Security spec pipeline (roles 01–10) from raw context to a ship-read… | - | - |
| phoenix-prd-pipeline:prd-generator | skill | Generate a full security-focused PRD (Product Requirements Document) from a plain-languag… | Use this skill whenever someone wants to create a PRD, product spec, feature spec, requi | - |
| phoenix-readiness-reviews:plan-readiness-review | skill | Adversarial senior/staff-engineer review of a PRD, plan, spec, RFC, design doc, or implem… | - | - |
| phoenix-readiness-reviews:production-readiness-review | skill | Adversarial senior/staff-engineer review that verifies a real codebase against its PRD, p… | - | - |
| plan-ceo-review | skill | CEO/founder-mode plan review. | - | - |
| plan-design-review | skill | Designer's eye plan review — interactive, like CEO and Eng review. | - | - |
| plan-devex-review | skill | Interactive developer experience plan review. | - | - |
| plan-eng-review | skill | Eng manager-mode plan review. | - | - |
| plan-tune | skill | Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). | - | - |
| plugin-dev:agent-development | skill | This skill should be used when the user asks to "create an agent", "add an agent", "write… | - | - |
| plugin-dev:command-development | skill | This skill should be used when the user asks to "create a slash command", "add a command"… | - | - |
| plugin-dev:hook-development | skill | This skill should be used when the user asks to "create a hook", "add a PreToolUse/PostTo… | - | - |
| plugin-dev:mcp-integration | skill | This skill should be used when the user asks to "add MCP server", "integrate MCP", "confi… | - | - |
| plugin-dev:plugin-settings | skill | This skill should be used when the user asks about "plugin settings", "store plugin confi… | - | - |
| plugin-dev:plugin-structure | skill | This skill should be used when the user asks to "create a plugin", "scaffold a plugin", "… | - | - |
| plugin-dev:skill-development | skill | This skill should be used when the user wants to "create a skill", "add a skill to plugin… | - | - |
| ponytail:ponytail | skill | Forces the laziest solution that actually works, simplest, shortest, most minimal. | - | Review |
| ponytail:ponytail-audit | skill | Whole-repo audit for over-engineering. | - | - |
| ponytail:ponytail-debt | skill | Harvest every `ponytail:` comment in the codebase into a debt ledger, so the deliberate s… | Use when | - |
| ponytail:ponytail-help | skill | Quick-reference card for all ponytail modes, skills, and commands. | Trigger: /ponytail-help, "ponytail help", "what ponytail commands", "how do I use ponytai… | - |
| ponytail:ponytail-review | skill | Code review focused exclusively on over-engineering. | - | - |
| retro | skill | Weekly engineering retrospective. | - | - |
| review | skill | Pre-landing PR review. | - | - |
| setup-deploy | skill | Configure deployment settings for /land-and-deploy. | - | - |
| setup-gbrain | skill | Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supaba… | - | - |
| ship | skill | Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update C… | - | Kapanış |
| skill-creator:skill-creator | skill | Create new skills, modify and improve existing skills, and measure skill performance. | Use when users want to create a skill from scratch, edit, or optimize an existing skill, … | - |
| skillify | skill | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. | - | - |
| spec | skill | Turn vague intent into a precise, executable spec in five phases. | - | - |
| superpowers:brainstorming | skill | You MUST use this before any creative work - creating features, building components, addi… | use this before any creative work - creating features, building components, adding functi… | Plan |
| superpowers:diagnosing-superpowers | skill | Use when a superpowers session went wrong and your human partner wants to know why — repe… | Use when a superpowers session went wrong and your human partner wants to know why — repe… | - |
| superpowers:executing-plans | skill | Use when executing an implementation plan in the current session as the implementer yours… | Use when executing an implementation plan in the current session as the implementer yours… | Yapım disiplini |
| superpowers:finishing-a-development-branch | skill | Use when implementation is complete, all tests pass, and you need to decide how to integr… | Use when implementation is complete, all tests pass, and you need to decide how to integr… | - |
| superpowers:receiving-code-review | skill | Use when receiving code review feedback, before implementing suggestions, especially if f… | Use when receiving code review feedback, before implementing suggestions, especially if f… | Git |
| superpowers:requesting-code-review | skill | Use when completing tasks, implementing major features, or before merging to verify work … | Use when completing tasks, implementing major features, or before merging to verify work … | - |
| superpowers:subagent-driven-development | skill | Use when executing implementation plans with independent tasks in the current session | Use when executing implementation plans with independent tasks in the current session | Yapım disiplini |
| superpowers:using-git-worktrees | skill | Use when starting feature work that needs isolation from current workspace or before exec… | Use when starting feature work that needs isolation from current workspace or before exec… | - |
| superpowers:using-superpowers | skill | Use when starting any conversation - establishes how to find and use skills, requiring sk… | Use when starting any conversation - establishes how to find and use skills, requiring sk… | - |
| superpowers:writing-plans | skill | Use when you have a spec or requirements for a multi-step task, before touching code | Use when you have a spec or requirements for a multi-step task, before touching code | Yapım disiplini |
| superpowers:writing-skills | skill | Use when creating new skills, editing existing skills, or verifying skills work before de… | Use when creating new skills, editing existing skills, or verifying skills work before de… | - |
| sync-gbrain | skill | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. | - | - |
| taste-skill:output-skill | skill | Overrides default LLM truncation behavior. | - | - |
| unfreeze | skill | Clear the freeze boundary set by /freeze, allowing edits to all directories again. | - | - |

## Elle
