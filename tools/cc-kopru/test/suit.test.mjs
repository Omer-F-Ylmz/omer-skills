/**
 * FIX-6 K1: suit'in başlattığı süreçler işaretlenir; suit sonunda işaretli canlı süreç
 * kalırsa suit kırmızı döner (22 Eyl'de 48 gecit.mjs sızmıştı).
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const KOK = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("suit: isaretli sureci sizdiran test suit'i kirmizi yapar", () => {
  const dosya = path.join(os.tmpdir(), `cc-kopru-sizan-${process.pid}.txt`);
  // NODE_TEST_CONTEXT kalirsa ic `node --test` kendini ic ice sanip dosyalari atliyor
  const { NODE_TEST_CONTEXT, ...env } = process.env;
  const r = spawnSync(process.execPath, [path.join(KOK, "araclar", "suit.mjs"), "test/yardim/sizdiran.mjs"],
                      { cwd: KOK, encoding: "utf8", timeout: 60000, env: { ...env, SIZAN_DOSYA: dosya } });
  const pid = fs.existsSync(dosya) ? Number(fs.readFileSync(dosya, "utf8")) : 0;
  try {
    assert.ok(pid, "sizdiran calismadi:\n" + r.stdout + r.stderr);
    assert.notEqual(r.status, 0, "sizinti varken suit yesil:\n" + r.stdout);
    assert.match(r.stdout, new RegExp(`isaretli canli surec: 1 · pid ${pid}`));
  } finally {
    if (pid) try { process.kill(pid); } catch { /* bitmis */ }
    fs.rmSync(dosya, { force: true });
  }
});
