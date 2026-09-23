# Departman: guvenlik

> Güvenlik denetimi, zafiyet taraması, pentest, sır taraması, tehdit modeli, KVKK/gizlilik uyumu.

Müdür: `departman-guvenlik`
<!-- `video departman` üretir; yalnız '## Elle' altı korunur. Düzeltme: docs/departmanlar/elle.json -->

| araç | tür | ne işe yarar | ne zaman | sıradaki adım |
|---|---|---|---|---|
| gitleaks | cli | - | - | Diff taraması |
| semgrep | cli | - | - | Tasarım riski |
| strix | cli | - | - | Bağımlılık |
| phoenix-cti-search | plugin | Cyber threat intelligence search across 595 curated security domains in 4 authority tiers… | - | - |
| phoenix-sast-rules | plugin | Generate opengrep/semgrep SAST rules for 30+ languages, including pattern and taint-mode … | - | - |
| phoenix-security-review | plugin | AppSec review suite: multi-language security-reviewer (8-point check, 7 language packs, O… | - | - |
| security-guidance | plugin | Security review for Claude-generated code. | - | - |
| agent-skills:security-and-hardening | skill | Hardens code against vulnerabilities. | Use when auditing an input handler for vulnerabilities, when handling user input, authent… | KVKK |
| anthropic-skills:api-security-testing | skill | Security-test a REST, GraphQL, or gRPC API with Strix — autonomous agents that enumerate … | - | Bağımlılık |
| anthropic-skills:application-security-testing | skill | Application security testing (AppSec) across a whole product with Strix — decide which as… | - | - |
| anthropic-skills:ci-security-scanning-with-strix | skill | Add Strix AI pentest scanning to CI/CD (GitHub Actions, GitLab CI, or managed app.strix.a… | - | - |
| anthropic-skills:departman-guvenlik | skill | Güvenlik müdürü: sır taraması, SAST, pentest, KVKK sırası. | - | - |
| anthropic-skills:find-security-vulnerabilities-in-code | skill | Find security vulnerabilities in a codebase or repository with Strix — a white-box AI sec… | - | - |
| anthropic-skills:fix-security-vulnerabilities-with-strix | skill | Fix security vulnerabilities found by a Strix pentest (open-source CLI or app.strix.ai cl… | - | Bağımlılık |
| anthropic-skills:gitleaks-desktop | skill | gitleaks CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşma… | - | - |
| anthropic-skills:managed-pentesting-with-strix | skill | Run a managed Strix pentest via app.strix.ai (strix cloud CLI/API): upload source, scan, … | - | - |
| anthropic-skills:owasp-top-10-testing | skill | Test an application against the OWASP Top 10 with Strix — autonomous AI agents that attem… | - | Bağımlılık |
| anthropic-skills:penetration-testing-with-strix | skill | Pentest a web app, API, codebase, or URL with Strix: autonomous AI pentesting that exploi… | - | - |
| anthropic-skills:semgrep-desktop | skill | semgrep CC'de PATH'te, Desktop'ta cc-kopru komut ile koşar; claude.ai sandbox'ında koşmaz. | - | - |
| anthropic-skills:web-app-penetration-testing | skill | Pentest a web app or website end to end — black-box testing of a live URL, staging enviro… | - | Bağımlılık |
| careful | skill | Safety guardrails for destructive commands. | - | - |
| cso | skill | Security audit: supported static findings; qualified profiles add reproduction and repair… | - | - |
| everything-claude-code:security-review | skill | Use this skill when adding authentication, handling user input, working with secrets, cre… | Use this skill when adding authentication, handling user input, working with secrets, cre… | Tasarım riski |
| guard | skill | Full safety mode: destructive command warnings + directory-scoped edits. | - | - |
| phoenix-cti-search:cti-domain-research | skill | Search for threat intelligence, CVEs, malware analysis, breach reports, and security rese… | - | - |
| phoenix-prd-pipeline:phoenix-security-engineer | skill | Role 06 of the Phoenix Security spec pipeline. | - | - |
| phoenix-sast-rules:opengrep-rule-generator | skill | Use when the user wants to create opengrep/semgrep SAST rules, detect vulnerabilities in … | Use when the user wants to create opengrep/semgrep SAST rules, detect vulnerabilities in … | - |
| phoenix-sast-rules:opengrep-rule-generator-research | skill | Use when the user wants to research vulnerabilities and create opengrep/semgrep SAST rule… | Use when the user wants to research vulnerabilities and create opengrep/semgrep SAST rule… | - |
| phoenix-security-review:0day-scanner | skill | LLM-powered zero-day vulnerability analysis of code changes — a commit, a pull request, a… | Use whene | Tasarım riski |
| phoenix-security-review:security-assessment | skill | Comprehensive OWASP Top 10 2025 and ASVS Level 1 security assessment across a whole codeb… | Use whenever someone asks to r | - |
| phoenix-security-review:security-reviewer | skill | Multi-language security review for web apps, APIs, and CLIs. | Use whenever code is added or modified — new endpoints, auth/RBAC changes, template or DO… | - |
| phoenix-security-review:threat-modeling | skill | Automated STRIDE and DREAD threat modelling from code analysis. | - | Uygulama testi |
| phoenix-security-review:tm-quick-security-assessment | skill | The QUICK tier. | - | - |
| phoenix-security-review:tm-security-review | skill | The COMPREHENSIVE tier. | - | Uygulama testi |
| pia-generation | skill | Yeni veri işleme faaliyeti için Türk KVKK pratiğine uygun VKED/PIA taslağı üretir. | - | - |
| policy-monitor | skill | Gizlilik politikası, aydınlatma metinleri, açık rıza metinleri, çerez/CMP, İYS/ticari ile… | - | - |
| use-case-triage | skill | Yeni veri işleme faaliyeti, ürün özelliği, tedarikçi, AI/model eğitimi, çalışan izleme, p… | - | - |

## Elle
