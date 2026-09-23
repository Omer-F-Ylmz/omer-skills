# Departman: surec-inceleme

> Kod review, sadeleştirme, doğrulama, kalite kapısı, PR yorumları.

Müdür: `departman-surec-inceleme`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| code-review | mcp | - | - | Yorum |
| code-review | plugin | Automated code review for pull requests using multiple specialized agents with confidence… | - | Yorum |
| phoenix-readiness-reviews | plugin | Two adversarial review gates. | - | - |
| ponytail | plugin | Lazy senior dev mode. | - | Review |
| pr-review-toolkit | plugin | Comprehensive PR review agents specializing in comments, tests, error handling, type desi… | - | Yorum |
| agent-skills:code-review-and-quality | skill | Conducts multi-axis code review. | Use before merging any change | - |
| agent-skills:code-simplification | skill | Simplifies code for clarity. | Use when refactoring code for clarity without changing behavior | Review |
| agent-skills:constraint-driven-development | skill | Establishes a project's quality bar as a written contract and stops agents quietly loweri… | - | - |
| agent-skills:doubt-driven-development | skill | Subjects every non-trivial decision to a fresh-context adversarial review before it stand… | Use when you want every assumption cross-examined before proceeding, when stress-testing … | - |
| andrej-karpathy-skills:karpathy-guidelines | skill | Behavioral guidelines to reduce common LLM coding mistakes. | Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical… | - |
| anthropic-skills:code-review-skill | skill | Code review guidance across React, Vue, Angular, Svelte, Rust, TypeScript, Java, PHP, Rub… | - | - |
| claude-mem:babysit | skill | Watch a pull request or review cycle until it is ready to merge. | Use when asked to babysit, monitor, or keep checking PR comments, reviews, and CI until a… | - |
| claude-mem:pathfinder | skill | Map a codebase into feature-grouped flowcharts, identify duplicated concerns across featu… | Use when asked to "find the ideal path," unify duplicated systems, or | - |
| devex-review | skill | Live developer experience audit. | - | - |
| everything-claude-code:coding-standards | skill | Universal coding standards, best practices, and patterns for TypeScript, JavaScript, Reac… | - | - |
| everything-claude-code:verification-loop | skill | A comprehensive verification system for Claude Code sessions. | - | - |
| health | skill | Code quality dashboard. | - | - |
| phoenix-readiness-reviews:plan-readiness-review | skill | Adversarial senior/staff-engineer review of a PRD, plan, spec, RFC, design doc, or implem… | - | - |
| phoenix-readiness-reviews:production-readiness-review | skill | Adversarial senior/staff-engineer review that verifies a real codebase against its PRD, p… | - | Devir |
| ponytail:ponytail | skill | Forces the laziest solution that actually works, simplest, shortest, most minimal. | - | Review |
| ponytail:ponytail-audit | skill | Whole-repo audit for over-engineering. | - | - |
| ponytail:ponytail-debt | skill | Harvest every `ponytail:` comment in the codebase into a debt ledger, so the deliberate s… | Use when | - |
| ponytail:ponytail-gain | skill | Show ponytail's measured impact as a compact scoreboard: less code, less cost, more speed… | Trigger: /pon | - |
| ponytail:ponytail-help | skill | Quick-reference card for all ponytail modes, skills, and commands. | Trigger: /ponytail-help, "ponytail help", "what ponytail commands", "how do I use ponytai… | - |
| ponytail:ponytail-review | skill | Code review focused exclusively on over-engineering. | - | Review |
| retro | skill | Weekly engineering retrospective. | - | - |
| review | skill | Pre-landing PR review. | - | - |
| superpowers:receiving-code-review | skill | Use when receiving code review feedback, before implementing suggestions, especially if f… | Use when receiving code review feedback, before implementing suggestions, especially if f… | Doğrulama |
| superpowers:requesting-code-review | skill | Use when completing tasks, implementing major features, or before merging to verify work … | Use when completing tasks, implementing major features, or before merging to verify work … | Yorum |
| superpowers:verification-before-completion | skill | Use when about to claim work is complete, fixed, or passing, before committing or creatin… | Use when about to claim work is complete, fixed, or passing, before committing or creatin… | Devir |

## Elle
