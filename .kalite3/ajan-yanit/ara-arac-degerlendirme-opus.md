Subagent `ara-arac-degerlendirme` answer, verbatim:

How to evaluate a new dev tool before adopting it. Turn each criterion into a pass/fail check, then run the steps in order.

1. **Need first:** write one line on the job the tool should do, a gain you can measure (minutes saved, tokens, failures avoided), and the stop condition. If there is no measurable gain, stop.
2. **Gain:** measure it on one real task, comparing what you do today with the tool. Don't trust the README's claims.
3. **Cost:** count price or tier, any API calls with a numeric ceiling ("at most N"), install size, extra config, and time to learn it.
4. **License:** read the LICENSE file and the dependencies' licenses. Flag anything that isn't MIT or Apache and write its conditions into the report (https://choosealicense.com/licenses/).
5. **Safety, supply chain:** run OpenSSF Scorecard on the repo (Maintained, Signed-Releases, Pinned-Dependencies, Dangerous-Workflow, Token-Permissions) and OSV/OSV-Scanner for known vulnerabilities.
6. **Safety, runtime:** check which permissions, network access and secrets it needs, and whether hooks or MCP give it too much reach. Put downloads in their own empty folder.
7. **Windows install:** prefer `winget search`, then `winget show`, then `winget install`. WinGet uses SHA256 hashes from manifests. Running it as admin skips elevation prompts, so watch for that. Try the install in Windows Sandbox first.
8. **Alternatives:** compare 2-3 options. Always include "do nothing" and whatever is already installed (stdlib, existing CLI, existing skill), and score them on the same criteria.
9. **Steps:** need → shortlist → license and Scorecard/OSV → sandbox install → one real-task trial → decision: adopt, reject, or re-check later.
10. **Report:** decision, measured gain, cost, open risks, how to roll back (uninstall or `winget pin`), and a date to check again.
11. **Biggest risks:** supply-chain compromise, licenses with conditions, unbounded paid calls, and over-wide permissions.

Sources:
- https://github.com/ossf/scorecard (checks; run with `scorecard --repo=github.com/<owner>/<repo>`, needs a GitHub token)
- https://osv.dev/ (vulnerability database across 38 ecosystems; OSV-Scanner scans lockfiles, SBOMs and containers)
- https://learn.microsoft.com/en-us/windows/package-manager/winget/ (search/show/install/hash/pin/export; admin and Windows Sandbox notes)
- https://learn.microsoft.com/en-us/windows/security/threat-protection/windows-sandbox/windows-sandbox-overview (link taken from the WinGet page; I didn't open it)
- https://choosealicense.com/licenses/ (license comparison; I didn't open it this session)

Not done: I loaded the required phoenix-research-pipeline skill but didn't run it. It does trending-content research and pushes to NotebookLM, which needs a Brave API key and a Google login, and it has no call ceiling. That doesn't fit a methods question. I checked three sources (Scorecard, OSV, WinGet); the license and Sandbox links are named but I didn't open them. The steps come from the department checklist (license gate, distilling sources) plus these sources, not from a measured trial.