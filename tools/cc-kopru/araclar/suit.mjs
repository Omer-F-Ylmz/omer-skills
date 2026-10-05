/**
 * Suit koşucusu: sahte worker'ı başlatır ve CLAUDE_MEM_WORKER_PORT ile bütün alt
 * süreçlere geçirir — kos.mjs'nin MEM_KOK'u da claude-mem hook'u da aynı değişkeni
 * okuyor, böylece testlerin hiçbir isteği gerçek worker'a düşmez.
 * Kullanım: node araclar/suit.mjs [ek node --test argümanları]
 */
import { execFileSync, spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { sahteWorker } from "./sahte-worker.mjs";

const KOK = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const w = await sahteWorker();
const ek = process.argv.slice(2);
// dosya listesi elle açılır: `node --test test/` kabuk globu olmadan dizini test sanıyor
const hepsi = fs.readdirSync(path.join(KOK, "test"))
  .filter((f) => f.endsWith(".test.mjs")).map((f) => `test/${f}`);
// Her node alt süreci benzersiz dizine pid'ini yazar (isaret.cjs); suit sonunda canlı
// kalan işaretli süreç = sızıntı -> kırmızı. Node dışı torunlar (powershell, git) sayılmaz.
const ISARET = fs.mkdtempSync(path.join(os.tmpdir(), "cc-kopru-suit-"));
// NODE_OPTIONS tırnak içinde ters eğiği kaçış sayar: yol ileri eğikle verilir
const onyukle = `--require "${path.join(KOK, "araclar", "isaret.cjs").replaceAll("\\", "/")}"`;
const p = spawn(process.execPath, ["--test", ...(ek.length ? ek : hepsi)], {
  cwd: KOK, stdio: "inherit",
  env: { ...process.env, CLAUDE_MEM_WORKER_PORT: String(w.port), CC_KOPRU_SUIT_ISARET: ISARET,
         NODE_OPTIONS: `${process.env.NODE_OPTIONS ?? ""} ${onyukle}`.trim() },
});

// Windows ölen işaretli node'un pid'ini başka sürece (ör. opera.exe) verebilir: yalnız node.exe sayılır
const node = (pid) => process.platform !== "win32" || execFileSync("tasklist", ["/FI", `PID eq ${pid}`, "/FO", "CSV", "/NH"],
  { encoding: "utf8" }).toLowerCase().startsWith('"node.exe"');
const yasiyor = (pid) => { try { process.kill(pid, 0); return node(pid); } catch { return false; } };

p.on("close", async (kod) => {
  console.log(`sahte worker gözlem isteği: ${w.istek.length}`);
  await w.kapat();
  // İlk bekleme: son saniyede başlayan torun işaretini henüz yazmamış olabilir.
  // Sonrası: p.kill() ile kapatılan sunucunun job dışı torunu stdin kapanınca birkaç sn içinde
  // kendiliğinden çıkar (KÜÇÜK-1 K1); sızıntı sayılmadan önce 10 sn'ye kadar beklenir.
  // ponytail: node→node pid yeniden kullanımı hâlâ yanlış pozitif verebilir; olursa oluşturma zamanı karşılaştırılır
  let canli = [];
  for (let i = 0; i < 20; i++) {
    await new Promise((r) => setTimeout(r, 500));
    canli = fs.readdirSync(ISARET).map(Number).filter(yasiyor);
    if (!canli.length) break;
  }
  console.log(`isaretli canli surec: ${canli.length}${canli.length ? " · pid " + canli.join(",") : ""}`);
  fs.rmSync(ISARET, { recursive: true, force: true });
  process.exit(canli.length ? (kod || 1) : (kod ?? 1));
});
