# context7 /vitejs/vite — build rollup manualChunks code splitting dynamic import asset inlining

### Removed object form `build.rollupOptions.output.manualChunks` and deprecate function form one

Source: https://github.com/vitejs/vite/blob/main/docs/guide/migration.md

The object form `output.manualChunks` option is not supported anymore. The function form `output.manualChunks` is deprecated. Rolldown has the more flexible [`codeSplitting`](https://rolldown.rs/reference/OutputOptions.codeSplitting) option. See Rolldown's docs for more details about `codeSplitting`: [Manual Code Splitting - Rolldown](https://rolldown.rs/in-depth/manual-code-splitting).

--------------------------------

### Using build.rolldownOptions.output.codeSplitting for chunking

Source: https://github.com/vitejs/vite/blob/main/docs/guide/build.md

Shows how to configure chunk splitting using `build.rolldownOptions.output.codeSplitting` as the replacement for the deprecated `manualChunks` option.

```markdown
## Chunking Strategy

You can configure how chunks are split using [`build.rolldownOptions.output.codeSplitting`](https://rolldown.rs/reference/OutputOptions.codeSplitting) (see [Rolldown docs](https://rolldown.rs/in-depth/manual-code-splitting)). If you use a framework, refer to their documentation for configuring how chunks are split.
```

--------------------------------

### codeSplitting config resolution (replaces manualChunks)

Source: https://github.com/vitejs/vite/blob/main/packages/vite/src/node/build.ts

In buildOutputOptions(), the codeSplitting option replaces the old manualChunks. Defaults to false for umd/iife/single-entry SSR webworker; otherwise undefined (Rolldown decides).

```typescript
codeSplitting:
  output.codeSplitting ??
  (output.format === 'umd' ||
  output.format === 'iife' ||
  (isSsrTargetWebworkerEnvironment &&
    (typeof input === 'string' || Object.keys(input).length === 1))
    ? false
    : undefined),
```

--------------------------------

### manualChunks flows through output spread

Source: https://github.com/vitejs/vite/blob/main/packages/vite/src/node/build.ts

In `buildOutputOptions`, the user's output config (carrying `manualChunks`) is spread via `...output` into the final Rolldown output options. This is how Vite passes the user-defined chunk-splitting function to the bundler.

```typescript
    return {
      dir: outDir,
      format,
      exports: 'auto',
      sourcemap: options.sourcemap,
      name: libOptions ? libOptions.name : undefined,
      generatedCode: {
        preset: 'es2015',
      },
      entryFileNames: ssr
        ? `[name].${jsExt}`
        : libOptions
          ? ({ name }) =>
              resolveLibFilename(
                libOptions,
                format,
                name,
                root,
                jsExt,
                packageCache,
              )
          : path.posix.join(options.assetsDir, `[name]-[hash].${jsExt}`),
      chunkFileNames: libOptions
        ? `[name]-[hash].${jsExt}`
        : path.posix.join(options.assetsDir, `[name]-[hash].${jsExt}`),
      assetFileNames: libOptions
        ? `[name].[ext]`
        : path.posix.join(options.assetsDir, `[name]-[hash].[ext]`),
      codeSplitting:
        output.codeSplitting ??
        (output.format === 'umd' ||
        output.format === 'iife' ||
        (isSsrTargetWebworkerEnvironment &&
          (typeof input === 'string' || Object.keys(input).length === 1))
          ? false
          : undefined),
      topLevelVar: true,
      ...output,
```

--------------------------------

### Control asset inlining with ?inline and ?no-inline

Source: https://github.com/vitejs/vite/blob/main/docs/guide/assets.md

Forces an asset to be explicitly inlined as a base64 data URL with `?inline` or prevents inlining using `?no-inline`.

```js
import 'vite/client'
// ---cut---
// prettier-ignore
import imgUrl1 from './img.svg?no-inline'
import imgUrl2 from './img.png?inline'
```