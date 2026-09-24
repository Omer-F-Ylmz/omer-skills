/** Kasıtlı sızıntı: suit.test.mjs bu dosyayı iç suit'te koşar; suit kırmızı dönmeli. */
import { test } from "node:test";
import { spawn } from "node:child_process";
import fs from "node:fs";

test("sizdiran: cocuk sureci kapatmadan biter", () => {
  // detached: libuv doğrudan çocuğu kill-on-close job nesnesine koyar; gerçek sızıntı
  // (cmd/npx arasındaki torun) job dışında kalır, detached onu taklit eder
  const p = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"],
                  { stdio: "ignore", detached: true });
  p.unref();
  fs.writeFileSync(process.env.SIZAN_DOSYA, String(p.pid));
});
