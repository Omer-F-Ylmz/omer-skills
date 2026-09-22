#!/usr/bin/env node
/**
 * KURULUM-11m-A K4 ölçümü (tek seferlik).
 * Üç örnek gövde için: sınıf · ham karakter · katman sonrası karakter · kazanç.
 * rtk hook'u açıkken koşulur; kazanç rtk'nın ÜSTÜNE eklenen kazançtır.
 * Kullanım: node tools/cc-kopru/araclar/olc-11m.mjs
 */
import { execFileSync } from "node:child_process";
import path from "node:path";

import { ciktiHazirla, ciktiSinifi } from "../kos.mjs";
import { katalogTopla } from "../hook.mjs";

const KOK = path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), "..", "..", "..");

const kos = (k, a) => {
  try { return execFileSync(k, a, { cwd: KOK, encoding: "utf8", maxBuffer: 1 << 28 }); }
  catch (e) { return String(e.stdout || "") + String(e.stderr || ""); }
};

const ornekler = [
  ["node --test", () => kos(process.execPath, ["--test", "tools/cc-kopru/test/allowlist.test.mjs", "tools/cc-kopru/test/kos.test.mjs"])],
  ["git log -100 --stat", () => kos("git", ["log", "-100", "--stat"])],
  ["katalog tur=skill", () => {
    const l = katalogTopla("skill", "");
    return `${l.length} kayıt (tür=skill)\n`
      + l.map((x) => `- [${x.tur}] ${x.ad}${x.aciklama ? " — " + x.aciklama : ""}`).join("\n");
  }],
];

console.log("| örnek | sınıf | yol | ham krk | katman sonrası | kazanç |");
console.log("|---|---|---|---|---|---|");
for (const [ad, uret] of ornekler) {
  const ham = String(uret() || "");
  const sinif = ciktiSinifi(ham);
  const t0 = Date.now();
  // Tavan bilerek devasa: kirpma karismasin, olculen YALNIZ katmanin kazanci.
  const sonra = await ciktiHazirla(ham, 10_000_000);
  const kazanc = ham.length ? Math.round((1 - sonra.length / ham.length) * 100) : 0;
  const yol = sonra.startsWith("[headroom %") ? "headroom" : (sonra.startsWith("[headroom yok") ? "kazanc yok" : "katman disi");
  console.log(`| \`${ad}\` | ${sinif} | ${yol} | ${ham.length} | ${sonra.length} | %${kazanc} `
    + `(${((Date.now() - t0) / 1000).toFixed(1)} sn) |`);
}
