## 1. Choose the mode

### Repository mode

Use when a local product repository is available. Create or update `DESIGN.md` at the root of the selected product.

If the repository contains multiple deployable products, select the one named by the user. If the request does not identify one and ownership is ambiguous, ask before writing.

Repository evidence may establish normative values, token names, component ownership, and documented rationale.

### URL mode

Use when the user provides a public URL without its source repository. Create a reconstructed `DESIGN.md` draft in the current workspace.

URL mode requires rendered browser access. Inspect the DOM, computed styles, and publicly loaded stylesheets at desktop and mobile widths. Screenshots may support interpretation but cannot establish exact values by themselves.

Inspect the supplied page and shared chrome. For a site-wide request, sample up to three same-origin pages that represent distinct templates.

URL evidence may establish only observable visual patterns and computed values. It cannot establish internal token names, component ownership, undocumented rationale, or whether a pattern is intentionally canonical.

If rendered inspection is unavailable, ask for screenshots or source files. Do not create a DESIGN.md from copy, metadata, or HTML structure alone.

Choose repository mode whenever source is available. A supplied URL may verify rendered presentation but does not replace repository evidence.

