/**
 * Suit koşucusu: sahte worker'ı başlatır ve CLAUDE_MEM_WORKER_PORT ile bütün alt
 * süreçlere geçirir — kos.mjs'nin MEM_KOK'u da claude-mem hook'u da aynı değişkeni
 * okuyor, böylece testlerin hiçbir isteği gerçek worker'a düşmez.
 * Kullanım: node araclar/suit.mjs [ek node --test argümanları]
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { sahteWorker } from "./sahte-worker.mjs";

const KOK = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const w = await sahteWorker();
const ek = process.argv.slice(2);
// dosya listesi elle açılır: `node --test test/` kabuk globu olmadan dizini test sanıyor
const hepsi = fs.readdirSync(path.join(KOK, "test"))
  .filter((f) => f.endsWith(".test.mjs")).map((f) => `test/${f}`);
const p = spawn(process.execPath, ["--test", ...(ek.length ? ek : hepsi)], {
  cwd: KOK, stdio: "inherit",
  env: { ...process.env, CLAUDE_MEM_WORKER_PORT: String(w.port) },
});
p.on("close", async (kod) => {
  console.log(`sahte worker gözlem isteği: ${w.istek.length}`);
  await w.kapat();
  process.exit(kod ?? 1);
});
