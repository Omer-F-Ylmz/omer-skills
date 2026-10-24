// REA-AGIR-1 parçalı mod işçisi: TEK betiği taze süreçte analiz eder (analyzeScript) ya da parçaları birleştirir.
// Kullanım: node [--max-old-space-size=2048] rea_parcali_isci.mjs <rea-dist> script <oge.json> <cikti.json>
//           node rea_parcali_isci.mjs <rea-dist> birlestir <inspection-metinsiz.json> <cikti.json> <acc1.json> [acc2.json ...]
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const [dist, mod, girdi, cikti, ...acclar] = process.argv.slice(2);
const al = (f) => import(pathToFileURL(join(dist, "domain", f)).href);
const { analyzeScript, emptyAccumulator } = await al("webBundleAnalyzerInspection.js");

if (mod === "script") {
  const oge = JSON.parse(readFileSync(girdi, "utf8"));
  const acc = emptyAccumulator();
  const t0 = Date.now();
  analyzeScript(oge, acc);
  acc.seen = [...acc.seen];
  writeFileSync(cikti, JSON.stringify({ acc, ms: Date.now() - t0, rss_mb: Math.round(process.memoryUsage().rss / 2 ** 20) }));
} else if (mod === "birlestir") {
  const { buildWebBundleAnalysis } = await al("webBundleAnalyzerResult.js");
  const { isIncludedScript } = await al("webBundleAnalyzerInspection.js");
  const inspection = JSON.parse(readFileSync(girdi, "utf8"));
  const m = emptyAccumulator();
  for (const f of acclar) {
    const { acc } = JSON.parse(readFileSync(f, "utf8"));
    for (const k of ["edges", "routes", "endpoints", "webMcp", "inferences", "failedScripts", "recoveredScripts"]) m[k].push(...acc[k]);
    for (const s of acc.seen) m.seen.add(s);
    m.visitedNodes += acc.visitedNodes;
    m.parsedScripts += acc.parsedScripts;
  }
  const kaynak = inspection.scripts.items.filter(isIncludedScript);
  const sonuc = buildWebBundleAnalysis(inspection, kaynak, { status: "not_requested", requested: 0, processed: 0, items: [] }, m);
  writeFileSync(cikti, JSON.stringify(sonuc));
} else {
  throw new Error("mod: script | birlestir");
}
