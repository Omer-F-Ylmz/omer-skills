# Departman: test-qa

> Test yazma ve koşma, uygulamayı tarayıcıda deneme/kullanma, e2e, görsel QA, performans ölçümü.

Müdür: `departman-test-qa`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| pixeljury | cli | - | - | Doğrulama |
| playwright-cli | cli | - | - | Görsel QA |
| puppeteer | mcp | - | - | - |
| dotnet-test | plugin | Skills for running, generating, analyzing, and improving .NET tests: test execution, filt… | - | - |
| playwright | plugin | Browser automation and end-to-end testing MCP server by Microsoft. | - | - |
| agent-skills:browser-testing-with-devtools | skill | Tests in real browsers via Chrome DevTools MCP. | Use when building or debugging anything that runs in a browser | - |
| agent-skills:debugging-and-error-recovery | skill | Guides systematic root-cause debugging. | Use when tests fail, builds break, something that worked yesterday broke, behavior doesn'… | - |
| agent-skills:performance-optimization | skill | Optimizes application performance across frontend, backend, queries, and databases. | Use when performance requirements exist, when you suspect performance regressions, when C… | - |
| agent-skills:test-driven-development | skill | Drives development with tests using the red-green-refactor loop. | Use when implementing any logic, fixing any bug, or changing any behavior | Test yazımı |
| anthropic-skills:departman-test-qa | skill | Test/QA müdürü: test yazma, koşma, uygulamayı tarayıcıda deneme ve görsel QA sırası. | - | - |
| anthropic-skills:playwright-cli | skill | Automate browser interactions, test web pages and work with Playwright tests. | - | Görsel QA |
| anthropic-skills:playwright-cli-desktop | skill | playwright-cli CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında… | - | - |
| benchmark | skill | Performance regression detection. | - | Doğrulama |
| benchmark-models | skill | Cross-model benchmark for gstack skills. | - | - |
| browse | skill | Drive a real browser through Aside: open a page, read it, click through a flow, take scre… | - | Görsel QA |
| connect-chrome | skill | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. | - | - |
| dotnet-test:assertion-quality | skill | Analyze assertion quality, depth, variety, and false confidence in existing tests. | USE when asked about weak, shallow, trivial, always-true, self-referential, assertion-fre… | - |
| dotnet-test:code-testing-agent | skill | ALWAYS USE whenever asked to write, add, or generate unit tests for existing code, includ… | USE whenever asked to write, add, or generate unit tests for existing code, including one… | Koşma |
| dotnet-test:code-testing-extensions | skill | Provides file paths to language-specific extension files for the code-testing pipeline. | - | - |
| dotnet-test:coverage-analysis | skill | Interprets .NET Cobertura line, branch, and condition evidence and, when explicitly reque… | USE for "why is branch coverage lower than lin | - |
| dotnet-test:crap-score | skill | Calculates CRAP (Change Risk Anti-Patterns) for a named .NET method, class, or file. | USE FOR: explicit CRAP calculation or coverage-and-complexity risk within that named targ… | - |
| dotnet-test:detect-static-dependencies | skill | Scan C# source files for hard-to-test static dependencies — DateTime.Now/UtcNow, File.*, … | - | - |
| dotnet-test:filter-syntax | skill | Reference-only filter syntax for VSTest and MTP with MSTest, NUnit, xUnit v3, and TUnit. | - | - |
| dotnet-test:find-untested-sources | skill | MANDATORY for static source-to-test pairing: find or list source files/modules without co… | - | Koşma |
| dotnet-test:generate-testability-wrappers | skill | DO NOT USE when the target already consumes an injected interface or built-in abstraction… | USE when the target already consumes an injected interface or built-in abstraction such a… | - |
| dotnet-test:grade-tests | skill | Grade specified test methods individually and produce a concise PR-ready table with each … | USE FOR per-test feedback on a curated | - |
| dotnet-test:migrate-static-to-wrapper | skill | ALWAYS USE when asked to migrate, replace, or make testable existing C# static calls with… | USE when asked to migrate, replace, or make testable existing C# static calls with a name… | - |
| dotnet-test:mtp-hot-reload | skill | Set up or recover MTP hot reload for a long-lived edit/re-run loop. | Use for "hot reload tests", "dotnet run or dotnet test for hot reload", a host that keeps… | - |
| dotnet-test:platform-detection | skill | Identify a .NET project's test platform, framework, command mode, and SDK-style vs classi… | - | - |
| dotnet-test:run-tests | skill | ALWAYS USE before running .NET tests or answering with a test command or flags. | USE before running | Uygulamayı deneme |
| dotnet-test:scaffold-dotnet-test-project | skill | MUST USE when an existing .NET test project was excluded from a .slnf/CI solution filter,… | USE when an existing | - |
| dotnet-test:test-analysis-extensions | skill | Provides file paths to language-specific reference files for the test ANALYSIS skills (as… | - | - |
| dotnet-test:test-anti-patterns | skill | Audit a test file or suite; produce a severity-ranked diagnostic report. | USE for tests that verify nothing, missing/tautological assertions, swallowed/broad excep… | - |
| dotnet-test:test-gap-analysis | skill | Pseudo-mutation analysis ONLY: answer whether tests would catch a bug if production code … | - | Koşma |
| dotnet-test:test-smell-detection | skill | Audits existing tests in any language using formal, research-backed test smell names and … | Use when the caller asks for an academic or citable test-smell r | - |
| dotnet-test:test-tagging | skill | Classifies existing tests by standard traits and reports their distribution. | - | - |
| dotnet-test:testability-obstacle | skill | MUST USE for C#/.NET deterministic tests that require the smallest production seam for Da… | USE for C#/ | - |
| dotnet-test:writing-mstest-tests | skill | ALWAYS USE when asked to fix, rewrite, update, improve, modernize, show corrected code fo… | USE when asked to fix, rewrite, update, improve, modernize, show corrected code for, or e… | Koşma |
| everything-claude-code:eval-harness | skill | A formal evaluation framework for Claude Code sessions, implementing eval-driven developm… | - | - |
| everything-claude-code:tdd-workflow | skill | Use this skill when writing new features, fixing bugs, or refactoring code. | Use this skill when writing new features, fixing bugs, or refactoring code | - |
| example-skills:webapp-testing | skill | Toolkit for interacting with and testing local web applications using Playwright. | - | Görsel QA |
| investigate | skill | Systematic debugging with root cause investigation. | - | - |
| ios-design-review | skill | Visual design audit for iOS apps on real hardware. | - | - |
| ios-fix | skill | Autonomous iOS bug fixer. | - | - |
| ios-qa | skill | Live-device iOS QA for SwiftUI apps. | - | - |
| qa | skill | Systematically QA test a web application and fix bugs found. | - | Görsel QA |
| qa-only | skill | Report-only QA testing. | - | Görsel QA |
| setup-browser-cookies | skill | Import cookies from your real Chromium browser into the headless browse session. | - | Görsel QA |
| superpowers:systematic-debugging | skill | Use when encountering any bug, test failure, or unexpected behavior, before proposing fix… | Use when encountering any bug, test failure, or unexpected behavior, before proposing fix… | Test yazımı |
| superpowers:test-driven-development | skill | Use when implementing any feature or bugfix, before writing implementation code | Use when implementing any feature or bugfix, before writing implementation code | Test yazımı |

## Elle
