/** Geç kapanan çocuk: suit-gec.test.mjs bu dosyayı iç suit'te koşar; çocuk 4 sn sonra kendiliğinden çıkar, suit yeşil kalmalı. */
import { test } from "node:test";
import { spawn } from "node:child_process";
import fs from "node:fs";

test("gec-kapanan: cocuk birkac saniye sonra kendiliginden cikar", () => {
  // detached: kill-on-close job dışında kalan torunu taklit eder (bkz. sizdiran.mjs)
  const p = spawn(process.execPath, ["-e", "setTimeout(() => {}, 4000)"],
                  { stdio: "ignore", detached: true });
  p.unref();
  fs.writeFileSync(process.env.GEC_DOSYA, String(p.pid));
});
