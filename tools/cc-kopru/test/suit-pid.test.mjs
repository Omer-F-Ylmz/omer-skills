/**
 * O38: işaretli pid'i yeniden kullanan node dışı süreç (ör. opera.exe) sızıntı sayılmaz.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const KOK = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

test("suit: isaretli pid node disi surece gecmisse sizinti sayilmaz", () => {
  const dosya = path.join(os.tmpdir(), `cc-kopru-yabanci-${process.pid}.txt`);
  const { NODE_TEST_CONTEXT, ...env } = process.env;
  const r = spawnSync(process.execPath, [path.join(KOK, "araclar", "suit.mjs"), "test/yardim/yabanci-pid.mjs"],
                      { cwd: KOK, encoding: "utf8", timeout: 60000, env: { ...env, YABANCI_DOSYA: dosya } });
  const pid = fs.existsSync(dosya) ? Number(fs.readFileSync(dosya, "utf8")) : 0;
  try {
    assert.ok(pid, "yabanci-pid calismadi:\n" + r.stdout + r.stderr);
    assert.match(r.stdout, /isaretli canli surec: 0/);
    assert.equal(r.status, 0, r.stdout);
  } finally {
    if (pid) try { process.kill(pid); } catch { /* bitmis */ }
    fs.rmSync(dosya, { force: true });
  }
});
