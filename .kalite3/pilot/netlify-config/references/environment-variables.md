## Environment variables

Two storage methods:
- **UI / CLI / API** — stored on Netlify (not the repo). Supports site + shared vars, per-context values, scopes; reaches builds, functions/edge/ODB, snippet injection, forms, signed proxies. **Recommended for anything sensitive.**
- **`netlify.toml`** — stored in the repo. Site vars only, per-context values, **no scope selection** (everything gets **Builds** + **Post processing**), reaches builds + snippet injection only.

`netlify.toml` env vars **override** same-key UI/CLI/API vars.

Per-context values in TOML:
```toml
[context.production]
  environment = { NODE_VERSION = "14.15.3" }
[context.deploy-preview.environment]
  NOT_PRIVATE_ITEM = "not so secret"
[context.branch-deploy.environment]
  NODE_ENV = "development"
```

CLI:
```bash
netlify env:set KEY value          # --secret marks it a secret
netlify env:import .env             # site vars; --replace-existing wipes others first
netlify env:unset KEY
netlify env:list --plain --context production > .env
netlify build                       # local build with Netlify's env vars
```
API: `createEnvVars` / `updateEnvVar` (`is_secret: true`) / `setEnvVarValue` / `deleteEnvVar` / `deleteEnvVarValue`.

**Access syntax:** Bash `$VAR` in `build.command`/`ignore.command`; `process.env.VAR` in Node scripts and plugins.

**Scopes** (Pro/Enterprise; default all): Builds (site builds) · Functions (Functions/Edge/ODB) · Runtime (forms, signed proxies) · Post processing (snippet injection). Shared vars are Pro/Enterprise and **Team-Owner-only** to read/edit. Precedence for a site+shared key collision resolves **per scope** — a site var only wins within the scopes it actually carries.

**Naming/limits:** keys alphanumeric + underscore, must start with a letter (`1KEY`, `_KEY1` invalid); keys ≤255 chars, values ≤5,000 chars. Read-only variable names are reserved. Changes need a build + deploy.

**Set the build language via reserved config vars** — `NODE_VERSION`, `NPM_FLAGS`, `YARN_VERSION`, `BUN_VERSION`, `RUBY_VERSION`, `PHP_VERSION`, `PYTHON_VERSION`, `GO_VERSION`, `HUGO_VERSION`, `PNPM_FLAGS`, `NPM_TOKEN` (Yarn: `YARN_NPM_AUTH_TOKEN`), etc.

**Must be set in UI/CLI/API, NOT `netlify.toml`** (read after the repo is cloned or a runtime-only var): `AWS_LAMBDA_JS_RUNTIME`, `GIT_LFS_ENABLED`, `GIT_LFS_FETCH_INCLUDE`, `NETLIFY_BUILD_DEBUG`.

**`CI` gotcha:** defaults to `true`; if it breaks a build, prepend `CI='' ` to the build command.

### Injecting env values into headers/redirects
`key = "$VAR"` is unsupported. Only path (scope must include **Builds**):
```toml
[build]
  command = "sed -i \"s|HEADER_PLACEHOLDER|${PROD_API_LOCATION}|g\" netlify.toml && yarn build"
```
`sed` substitution works **only** for `[[headers]]`/`[[redirects]]` (read after the build) and is **not** visible to build plugins (they run before the build command). For plugin-visible changes, use a local build plugin editing `netlifyConfig`.

### Useful read-only build vars
`CONTEXT` (`production`/`deploy-preview`/`branch-deploy`/`dev`), `BRANCH`, `COMMIT_REF`, `CACHED_COMMIT_REF`, `PULL_REQUEST`, `REVIEW_ID`, `URL`, `DEPLOY_URL`, `DEPLOY_PRIME_URL`, `SITE_ID`, `SITE_NAME`.

