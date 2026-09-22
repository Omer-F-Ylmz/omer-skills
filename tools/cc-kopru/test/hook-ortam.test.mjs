/**
 * KURULUM-11m-A-FIX-2 EK — hook ortam eşitliği (K1 · K3).
 *
 * Desktop yerel MCP sunucularını MCP SDK'nın beyaz listesiyle başlatır; köprü o
 * kısıtlı ortamı hook süreçlerine AYNEN geçiriyordu. CC ise hook'lara kendi tam
 * ortamını (+ settings.json `env` bloğu) verir. Fark, hook'ları sessizce bozuyor.
 * Değerler basılmaz: testler yalnız exit kodu ve çıktı metnine bakar.
 */
import assert from "node:assert/strict";
import test from "node:test";

import { desktopOrtamiUygula, envanter } from "../araclar/hook-envanter.mjs";
import { hookKaynaklari, hookKos, hookTanimlari, tekHookKos } from "../hook.mjs";

const PROJE = "C:/Projeler/omer-skills";

/** node -e ile Windows'ta kosan sahte hook uretir. */
const sahte = (govde) => ({ type: "command", command: `node -e "${govde.replace(/"/g, '\\"')}"` });
const kaynak = (olay, matcher, hook) => [{
  ad: "sahte",
  json: { hooks: { [olay]: [{ matcher, hooks: [hook] }] } },
  kok: "C:/sahte-eklenti",
}];

const girdi = (olay, komut) => ({
  session_id: "ortam-testi", cwd: PROJE, hook_event_name: olay, tool_name: "Bash",
  tool_input: { command: komut, description: "hook-ortam testi" },
  tool_response: { stdout: "", exitCode: 0 },
});

test("K3.1 Desktop taklidinde block-destructive yasak komutu reddeder", async () => {
  const defs = hookTanimlari(hookKaynaklari(PROJE), []);
  const geri = desktopOrtamiUygula();
  let r;
  try {
    r = await hookKos(defs, girdi("PreToolUse", "git reset --hard"), { projeDir: PROJE });
  } finally { geri(); }
  assert.equal(r.karar, "red", r.ekBaglam);
  assert.match(r.sebep, /yıkıcı komut/);
}, { timeout: 120000 });

test("K3.2 Desktop taklidinde hookify ModuleNotFound ile çıkmaz", async () => {
  const defs = hookTanimlari(hookKaynaklari(PROJE), [])
    .filter((t) => t.anahtar.startsWith("plugin:hookify|PreToolUse"));
  assert.ok(defs.length, "hookify PreToolUse hook'u bulunamadı");
  const geri = desktopOrtamiUygula();
  let r;
  try { r = await tekHookKos(defs[0], girdi("PreToolUse", "git status"), PROJE); } finally { geri(); }
  assert.equal(r.kod, 0);
  assert.doesNotMatch(r.out + r.err, /No module named/, r.out.slice(0, 200));
}, { timeout: 120000 });

test("K3.3 hata koduyla çıkan hook sessiz geçmez", async () => {
  for (const olay of ["PreToolUse", "PostToolUse"]) {
    const t = hookTanimlari(kaynak(olay, "Bash",
      sahte("process.stderr.write('patladi');process.exit(1)")), []);
    const r = await hookKos(t, girdi(olay, "git status"));
    assert.equal(r.karar, "izin");
    assert.match(r.ekBaglam, new RegExp(`\\[hook hata: sahte\\|${olay}\\|Bash exit 1\\]`), r.ekBaglam);
  }
}, { timeout: 60000 });

test("K1 envanteri iki ortamda aynı", async () => {
  const cc = await envanter(PROJE);
  const geri = desktopOrtamiUygula();
  let dt;
  try { dt = await envanter(PROJE); } finally { geri(); }
  assert.ok(cc.length >= 6, `hook envanteri beklenmedik kadar kısa: ${cc.length}`);
  assert.deepEqual(dt, cc);
}, { timeout: 300000 });
