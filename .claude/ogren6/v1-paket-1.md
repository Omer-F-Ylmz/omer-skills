## 0day-scanner
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\0day-scanner.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-security-review\1.0.0\skills\0day-scanner\SKILL.md) · 391 satır · araç adları (1): 0day-scanner
BAŞLIKLAR: # 0-Day Vulnerability Scanner Skill · ## Purpose · ## When to Use · ## Workflow · ### 1. Parse User Request · Extract: · ### 2. Invoke Scanner · ### 3. Monitor Progress · ### 4. Present Results · ### 5. Follow-Up Actions · Offer to: · ## Example Interactions · ### Example 1: Quick Commit Analysis · Would you like me to: · ### Example 2: PR Review · ### Example 3: File Analysis · Would you like me to: · ### Example 4: Full Repository Analysis · Would you like me to: · ## Key APIs · ### MCP Tool · ### REST API · # Light-touch analysis · # Full repository analysis · # Programmatic launch · # Get scan status · # Stream updates (SSE) · ## Configuration · ### Default Settings · ### User Preferences · Users can override defaults: · ## Best Practices · ## Integration Points · ## Limitations · ## Example Cypher Queries

## chrome-devtools
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\chrome-devtools.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\chrome-devtools-plugins\chrome-devtools-mcp\1.10.1\skills\chrome-devtools\SKILL.md) · 74 satır · araç adları (1): chrome-devtools
BAŞLIKLAR: ## Core Concepts · ## Workflow Patterns · ### Before interacting with a page · ### Efficient data retrieval · ### Tool selection · ### Parallel execution · ### Testing an extension · ## Troubleshooting

## cti-domain-research
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\cti-domain-research.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-cti-search\1.0.0\skills\cti-domain-research\SKILL.md) · 276 satır · araç adları (2): cti-domain-research · scripts/install.sh
BAŞLIKLAR: # CTI Domain Research · ## Customization · # Edit .env with your API keys · # Add a domain (one per line) · # Add tier mapping · # Edit data/tier-map.json and add: · # "your-security-blog.com": { "tier": 3, "authority": 70 } · ## Workflow · ## Query Parsing · ## Domain Tiers · ## Search Execution · # Example batch query construction · # For CVEs, always include NVD and MSRC · ## Result Schema · ## Output Formats · ### Default — CTI Brief (table + bullets) · ## CTI Brief: <query> — <date> · ### Key Findings · ### Source Table · ### IOC Summary · ### Next Steps · ### `--full` — Long-Form Brief · ### `--json` · ## NotebookLM Integration · ### Connector flow: · ### Plugin call pattern (Claude Code): · # Check connector is installed · # Call connector with source list · ### Required env var: · # Or pass via --notebook-id flag at query time · ### Fallback (Claude.ai — no plugin runtime): · ## Slash Command (Claude Code) · Flags: · ## Installation Script · ## Error Handling · ## Reference Files

## debug
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\debug.txt (çözülmüş; özgün: C:\Users\pc\.claude\skills\debug\SKILL.md) · 100 satır · araç adları (1): debug
BAŞLIKLAR: ## Output style (plain words, no dashes, no hyphens) · ## What this skill does · ## Asks vs acts · ## Artifact ownership · ## Portability (any OS, any agent) · ## Execution · ### Step 0: Capture the symptom · ### Step 1: Reproduce reliably · ### Step 2: Localize · ### Step 3: Hypothesize (one at a time) · ### Step 4: Test the hypothesis · ### Step 5: Fix at the root · ### Step 6: Verify and protect · ### Optional: run it in a subagent · ### Report · ## /debug complete Â· <the bug, one line>

## dn-efcore-seed-veri
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\dn-efcore-seed-veri.txt (çözülmüş; özgün: C:\Users\pc\.claude\agents\dn-efcore-seed-veri.md) · 30 satır · araç adları (1): dn-efcore-seed-veri
BAŞLIKLAR: ## Ders bankası · # Work protocol · Kurallar:

## dotnet
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\dotnet.txt (çözülmüş; özgün: C:\Program Files\dotnet\dotnet.EXE) · 3357 satır · araç adları (1): dotnet
BAŞLIKLAR: 

## grade-tests
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\grade-tests.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\dotnet-agent-skills\dotnet-test\0.2.19\skills\grade-tests\SKILL.md) · 348 satır · araç adları (1): grade-tests
BAŞLIKLAR: # Grade Tests · ## Why a Per-Test Grade · ## When to Use · ## When Not to Use · ## Inputs · ### Step 0: Validate the input · ## Workflow · ### Step 1: Detect language and load extension · ### Step 2: Resolve the test bodies · ### Step 3: Score each test · #### Three sub-dimensions · ##### A. Assertion strength · ##### B. Structure & focus · ##### C. Anti-pattern hygiene · #### Combining sub-grades · ### Step 4: Build the note · ### Step 5: Report · #### 1. Summary · #### 2. Per-test table · ## Validation · ## Common Pitfalls

## opengrep-rule-generator
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\opengrep-rule-generator.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\phoenix-security\phoenix-sast-rules\1.0.0\skills\opengrep-rule-generator\SKILL.md) · 477 satır · araç adları (1): opengrep-rule-generator
BAŞLIKLAR: # Opengrep Rule Generator · ## Overview · ## When to Use · ## Process Flow · ## Reference Documentation · ## Workflow 1: Guided Discovery · ### Step 1 — What are we detecting? · Examples: · ### Step 2 — What language and frameworks? · ### Step 3 — Show me the vulnerable code · ### Step 4 — Where does user input enter? (if applicable) · ### Step 5 — Severity and scope · ## Workflow 2: Vulnerability-Driven Generation · ### Vulnerability Research Plan · # Research: <vulnerability type> in <language/framework> · # Sources: <where untrusted data enters> · # Sinks: <where data becomes dangerous> · # Sanitizers: <what makes data safe> · # References researched: · #   - <url1> · #   - <url2> · # Coverage gaps found: <what existing rules miss> · ### Mode Selection Guide · ## Rule Generation Template · ### Naming Convention · ### Message Quality · Good messages include: · ## Test File Generation · # === True Positives (MUST trigger) === · # ruleid: <rule-id> · # ruleid: <rule-id> · # === True Negatives (must NOT trigger) === · # ok: <rule-id> · # ok: <rule-id> · ## Advanced Patterns Cookbook · ### Detect missing security check (pattern-not-inside) · ### Detect tainted string concatenation (taint + metavariabl · ### Detect weak config values (metavariable-comparison) · ### Detect across multiple call variants (pattern-either + m · ### Detect with type constraints (typed metavariables) · # Go: match only http.Request types · ### Multi-step taint with labels · ## Reducing False Positives 

## playwright
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\playwright.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\claude-plugins-official\playwright\c2bdb427efe8) · 9 satır · araç adları (2): c2bdb427efe8 · playwright
BAŞLIKLAR: 

## qa-manuel-test-plani
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\qa-manuel-test-plani.txt (çözülmüş; özgün: C:\Users\pc\.claude\agents\qa-manuel-test-plani.md) · 32 satır · araç adları (1): qa-manuel-test-plani
BAŞLIKLAR: ## Ders bankası · # Work protocol · Kurallar:

## sql-queries
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\sql-queries.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\synced\924f0f64-fcbf-4e91-8e2f-e62bad8245c0_5bf6859c-713e-459a-9126-5fb1dcc493b6\data~g2\skills\sql-queries\SKILL.md) · 428 satır · araç adları (1): sql-queries
BAŞLIKLAR: # SQL Queries Skill · ## Dialect-Specific Reference · ### PostgreSQL (including Aurora, RDS, Supabase, Neon) · ### Snowflake · ### BigQuery (Google Cloud) · ### Redshift (Amazon) · ### Databricks SQL · ## Common SQL Patterns · ### Window Functions · ### CTEs for Readability · ### Cohort Retention · ### Funnel Analysis · ### Deduplication · ## Error Handling and Debugging · When a query fails:

## use-case-triage
kaynak: C:\Projeler\omer-skills\.claude\ogren6\kaynak\use-case-triage.txt (çözülmüş; özgün: C:\Users\pc\.claude\plugins\cache\claude-for-legal\privacy-legal\1.0.2\skills\use-case-triage\SKILL.md) · 295 satır · araç adları (1): use-case-triage
BAŞLIKLAR: # /use-case-triage · # Privacy Use Case Triage · ## Matter context · ## Destination check · ## Purpose · ## Jurisdiction assumption · ## Read the config first · ### Provisional mode · ## Triage process · ### Step 1: Understand the activity · ### Step 2: Check house triggers · ### Step 3: Mandatory assessment check · ### Step 4: Privacy policy conflict check · ### Step 5: Classification and output · ### Bottom line · ### Step 6: Cross-plugin handoffs · ## Batch triage · ## Edge cases and failure modes · ## Close with the next-steps decision tree
