## build-perf-diagnostics
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\build-perf-diagnostics.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\dotnet-agent-skills\dotnet-msbuild\0.1.10\skills\build-perf-diagnostics\SKILL.md) · 150 satır · araç adları (1): build-perf-diagnostics
BAŞLIKLAR: ## Performance Analysis Methodology · ### Alternate flow when MCP is unavailable: binlog replay to · ## Key Metrics and Thresholds · ## Common Bottlenecks · ### 1. ResolveAssemblyReference (RAR) Slowness · ### 2. Roslyn Analyzers and Source Generators · ### 3. Serialization Bottlenecks (Single-threaded targets) · ### 4. Excessive File I/O (Copy tasks) · ### 5. Evaluation Overhead · ### 6. NuGet Restore in Build · ### 7. Large Project Count and Graph Shape · ## Using Binlog Replay for Performance Analysis · ## Quick Wins Checklist · ## Impact Categorization

## crap-score
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\crap-score.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\dotnet-agent-skills\dotnet-test\0.2.19\skills\crap-score\SKILL.md) · 225 satır · araç adları (1): crap-score
BAŞLIKLAR: # CRAP Score Analysis · ## Background · Where: · ## When to Use · ## When Not to Use · ## Inputs · ## Workflow · ### Step 1: Collect code coverage data · #### Never estimate coverage · ### Step 2: Compute cyclomatic complexity · ### Step 3: Extract per-method coverage from Cobertura XML · ### Step 4: Calculate CRAP scores · ### Step 5: Present results · Include: · ### Step 6: Provide actionable recommendations · ## Validation · ## Common Pitfalls

## db-veri-modelleme-nosql
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\db-veri-modelleme-nosql.txt (çözülmüş; özgün: C:\Users\pc\.claude\agents\db-veri-modelleme-nosql.md) · 37 satır · araç adları (1): db-veri-modelleme-nosql
BAŞLIKLAR: ## Ders bankası · # Work protocol

## dn-dotnet-performans
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\dn-dotnet-performans.txt (çözülmüş; özgün: C:\Users\pc\.claude\agents\dn-dotnet-performans.md) · 22 satır · araç adları (1): dn-dotnet-performans
BAŞLIKLAR: ## Ders bankası · Kurallar:

## dn-signalr-gercek-zamanli
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\dn-signalr-gercek-zamanli.txt (çözülmüş; özgün: C:\Users\pc\.claude\agents\dn-signalr-gercek-zamanli.md) · 23 satır · araç adları (1): dn-signalr-gercek-zamanli
BAŞLIKLAR: ## Ders bankası

## generate-testability-wrappers
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\generate-testability-wrappers.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\dotnet-agent-skills\dotnet-test\0.2.19\skills\generate-testability-wrappers\SKILL.md) · 352 satır · araç adları (1): generate-testability-wrappers
BAŞLIKLAR: # Generate Testability Wrappers · ## When to Use · ## When Not to Use · ## Inputs · ## Workflow · ### Step 1: Determine the abstraction strategy · ### Step 2: Generate built-in abstraction adoption (Time, HT · #### TimeProvider (.NET 8+) · #### TimeProvider (pre-.NET 8) · #### IHttpClientFactory · ### Step 3: Generate custom wrappers (Environment, Console,  · #### Interface — define the minimal surface · #### Default implementation — delegate to the real static · #### DI registration · ### Step 4: Generate file system wrapper adoption · ### Step 5: Generate a signature-preserving ambient context · ### Step 6: Place generated files · Always generate: · ## Validation · ## Common Pitfalls

## msbuild-code-review
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\msbuild-code-review.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\dotnet-agent-skills\dotnet-msbuild\0.1.10\agents\msbuild-code-review.agent.md) · 79 satır · araç adları (2): msbuild-code-review · msbuild-code-review.agent
BAŞLIKLAR: # MSBuild Code Review Agent · ## Domain Relevance Check · ## Review Workflow · ### Category 1: Modernization · ### Category 2: Style & Organization · ### Category 3: Consolidation Opportunities · ### Category 4: Correctness & Gotchas · ## Specialized Skills Reference

## pia-generation
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\pia-generation.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\claude-for-legal\privacy-legal\1.0.2\skills\pia-generation\SKILL.md) · 282 satır · araç adları (1): pia-generation
BAŞLIKLAR: # /pia-generation · # PIA Generation · ## Matter context · ## Destination check · ## Purpose · ## Jurisdiction assumption · ## Load prior context on this feature / activity · If a prior PIA exists: · ## Load house style · ## Step 0: Is a PIA needed? · ## The intake · ### What and why · ### Legal basis / regime-specific checks · ### Who and where · ### What could go wrong · ## Writing the PIA · # Privacy Impact Assessment: [Feature/Product Name] · ## Executive summary · ## 1. Description of processing · ## 2. Lawful basis · ## 3. Data flow · ## 4. Privacy policy consistency · ## 5. Risks and mitigations · ## 6. Data subject rights · ## 7. Recommendation · ## Risk quality standards · ## Privacy policy diff · ## Handoff · ## Gate: submitting a DPIA to a regulator · ## Close with the next-steps decision tree · ## What this skill does not do

## qa-flaky-avci
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\qa-flaky-avci.txt (çözülmüş; özgün: C:\Users\pc\.claude\agents\qa-flaky-avci.md) · 22 satır · araç adları (1): qa-flaky-avci
BAŞLIKLAR: ## Ders bankası · Kurallar:

## security-review
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\security-review.txt (çözülmüş; özgün: C:\Users\pc\.claude\skills\security-review\SKILL.md) · 312 satır · araç adları (1): security-review
BAŞLIKLAR: # Security Review Skill · ## Scope: Research vs. Reporting · ## Confidence Levels · ## Do Not Flag · ### General Rules · ### Server-Controlled Values (NOT Attacker-Controlled) · # SAFE: URL comes from Django settings (server-controlled) · # VULNERABLE: URL comes from request (attacker-controlled) · ### Framework-Mitigated Patterns · ## Review Process · ### 1. Detect Context · ### 2. Load Language Guide · ### 3. Load Infrastructure Guide (if applicable) · ### 4. Research Before Flagging · ### 5. Verify Exploitability · ### 6. Report HIGH Confidence Only · ## Severity Classification · ## Quick Patterns Reference · ### Always Flag (Critical) · ### Always Flag (High) · ### Always Flag (Secrets) · ### Check Context First (MUST Investigate Before Flagging) · # SSRF - ONLY if URL is from user input, NOT from settings/c · # Path traversal - ONLY if path is from user input · # Open redirect - ONLY if URL is from user input · # Weak crypto - ONLY if used for security purposes · ## Output Format · ## Security Review: [File/Component Name] · ### Summary · ### Findings · #### [VULN-001] [Vulnerability Type] (Severity) · ### Needs Verification · #### [VERIFY-001] [Potential Issue] · ## Reference Files · ### Core Vulnerabilities (`references/`) · ### Language Guides (`languages/`) · ### Infrastructure (`infrastructure/`)

## test-smell-detection
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\test-smell-detection.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\dotnet-agent-skills\dotnet-test\0.2.19\skills\test-smell-detection\SKILL.md) · 161 satır · araç adları (1): test-smell-detection
BAŞLIKLAR: # Test Smell Detection · ## Scope · ## Audit Workflow · ## High-Signal Decisions · ## Calibration Rules · ## Severity · ## Output Contract · Scale the response to the input: · ## Validation
