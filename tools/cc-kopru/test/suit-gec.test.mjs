/**
 * KÜÇÜK-1 K1: kill sonrası birkaç saniyede kendiliğinden kapanan işaretli süreç sızıntı sayılmaz;
 * asılı kalan süreç suit.test.mjs'te hâlâ yakalanıyor.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const KOK = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("suit: gec kapanan isaretli surec beklenir, suit yesil", () => {
  const dosya = path.join(os.tmpdir(), `cc-kopru-gec-${process.pid}.txt`);
  const { NODE_TEST_CONTEXT, ...env } = process.env;
  const r = spawnSync(process.execPath, [path.join(KOK, "araclar", "suit.mjs"), "test/yardim/gec-kapanan.mjs"],
                      { cwd: KOK, encoding: "utf8", timeout: 60000, env: { ...env, GEC_DOSYA: dosya } });
  const pid = fs.existsSync(dosya) ? Number(fs.readFileSync(dosya, "utf8")) : 0;
  try {
    assert.ok(pid, "gec-kapanan calismadi:\n" + r.stdout + r.stderr);
    assert.match(r.stdout, /isaretli canli surec: 0/);
    assert.equal(r.status, 0, r.stdout);
  } finally {
    if (pid) try { process.kill(pid); } catch { /* bitmis */ }
    fs.rmSync(dosya, { force: true });
  }
});
