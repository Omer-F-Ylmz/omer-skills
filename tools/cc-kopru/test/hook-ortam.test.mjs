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

import * as fsS from "node:fs";
import * as osS from "node:os";

test("K1 envanteri iki ortamda aynı", async () => {
  // sayaç hook'u gerçek oturum sayacına değil geçici dizine yazar: sonuç sayaçtan bağımsız
  const sayacDizin = fsS.mkdtempSync(`${osS.tmpdir()}/cagri-sayac-`);
  const onceki = process.env.CAGRI_SAYAC_DIZIN;
  process.env.CAGRI_SAYAC_DIZIN = sayacDizin;
  let cc, dt;
  try {
    cc = await envanter(PROJE);
    const geri = desktopOrtamiUygula();
    process.env.CAGRI_SAYAC_DIZIN = sayacDizin;
    try { dt = await envanter(PROJE); } finally { geri(); }
  } finally { process.env.CAGRI_SAYAC_DIZIN = onceki; }
  assert.equal(fsS.readFileSync(`${sayacDizin}/cagri-sayac.txt`, "utf8"), "2");
  assert.ok(cc.length >= 6, `hook envanteri beklenmedik kadar kısa: ${cc.length}`);
  assert.deepEqual(dt, cc);
}, { timeout: 300000 });

test("suit sayacı geçici dizine yönlendirir; Desktop ortamı korur", () => {
  // K2: bütün hook testleri gerçek .claude/cagri-sayac.txt yerine suit dizinine sayar
  const d = process.env.CAGRI_SAYAC_DIZIN;
  assert.ok(d && d.startsWith(osS.tmpdir()), "CAGRI_SAYAC_DIZIN suit ortamında yok");
  const geri = desktopOrtamiUygula();
  try { assert.equal(process.env.CAGRI_SAYAC_DIZIN, d); } finally { geri(); }
});
