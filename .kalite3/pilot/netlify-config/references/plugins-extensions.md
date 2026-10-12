## Plugins & extensions

```toml
[[plugins]]
package = "netlify-plugin-check-output-for-puppy-references"
  [plugins.inputs]
  breeds = ["pomeranian", "chihuahua"]

[[integrations]]              # build-time extension; install on team first
  name = "abc-performance-extension"
  [integrations.config]
    output_path = "reports/performance-reports.html"
```

Full reference pages: build environment variables at https://docs.netlify.com/build/configure-builds/environment-variables.md, env-var overview at https://docs.netlify.com/build/environment-variables/overview.md, Secrets Controller at https://docs.netlify.com/build/environment-variables/secrets-controller.md, redirects at https://docs.netlify.com/manage/routing/redirects/overview.md, redirect options at https://docs.netlify.com/manage/routing/redirects/redirect-options.md, rewrites/proxies at https://docs.netlify.com/manage/routing/redirects/rewrites-proxies.md, custom headers at https://docs.netlify.com/manage/routing/headers.md, and file-based config at https://docs.netlify.com/build/configure-builds/file-based-configuration.md.

<!-- Plan gating for the sensitive variable policy itself is unspecified in the sources; only its public-repo requirement and the smart-detection plan list are documented. -->

<!-- system: agent-context/config/system.md — human-owned, merged by ctx-gen; edit system.md, not this section -->
# Netlify house rules (config)

These are org conventions, not docs facts — merged into the rendered skill by
ctx-gen and never generated. Owned by the skills maintainer.

1. Env vars set in `netlify.toml` are NOT available to functions or edge
   functions at runtime — reading them there returns `undefined`. Set
   runtime vars in the UI or with `netlify env:set`, not `netlify.toml`.
2. Never put secrets in client-prefixed env vars (`VITE_`, `NEXT_PUBLIC_`,
   `PUBLIC_`, ...) — they are inlined into the client bundle; `--secret`
   does not protect them.
3. When snapshotting env vars locally (`netlify env:list --plain > .env`),
   keep `.env` gitignored — never commit it.
4. State env-var scope interaction explicitly: a site variable scoped to
   Builds does not shadow the shared variable for other scopes — precedence
   resolves independently per scope (site beats shared only within the
   scopes the site variable actually carries).
