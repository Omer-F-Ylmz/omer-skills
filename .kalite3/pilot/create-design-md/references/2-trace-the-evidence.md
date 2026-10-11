## 2. Trace the evidence

In repository mode, inspect in this order:

1. Existing `DESIGN.md` and explicit repository guidance
2. Tokens, themes, variables, and global styles
3. Shared primitives and their variants
4. Representative routes and rendered consumers
5. Surface-local implementations

A source participates only when the selected product imports, references, inherits, or renders it. Exclude proposals, migrations, examples, generated outputs, legacy implementations, and similarly named packages unless the selected product uses them.

In URL mode, sample representative elements for:

- colors and surface roles
- typography roles
- spacing and layout
- borders, radii, and elevation
- navigation, buttons, inputs, cards, and repeated content structures
- desktop and mobile presentation

Prefer computed values and loaded CSS declarations over visual estimation.

Before drafting URL-mode prose or YAML, build a private evidence ledger for each sampled page and viewport. For each candidate, record: page, viewport, element role, computed property/value, and the matching loaded-CSS declaration or custom property when available. Inspect the public stylesheets loaded by the page, including custom properties and media-query rules; a stylesheet value is usable only when it is connected to a rendered element or recurs across the sampled pages.

Promote a URL value into DESIGN.md when either (a) the rendered computed value and a loaded declaration/custom property agree, or (b) the same computed value recurs for the same role across the required samples. If neither condition holds, omit the value. You may preserve an exposed custom-property name only when its declaration and rendered use are directly observable; do not invent semantic aliases from a raw value.

For every URL-mode claim, require all three proofs before writing it:

1. Observation: the pattern or value is visible or computed on the rendered page.
2. Basis: it is measured, or recurs across the required sampled pages/viewports.
3. Consequence: it changes a concrete implementation choice in DESIGN.md.

If any proof is missing, omit the claim. Do not turn a visual impression into a token, a single occurrence into a site-wide rule, or a guessed value into YAML. Exact values require computed styles or loaded CSS; otherwise describe the role without a value or omit it.

