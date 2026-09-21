/**
 * 11i-FIX-1: görev metni argv'ye GİRMEZ, `claude -p`'ye stdin'den gider.
 * Sahte bir claude yürütücüsüyle argv+stdin yakalanır; API çağrısı yok.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const KOK = path.join(path.dirname(fileURLToPath(import.meta.url)), "..");
const PROJE = "C:/Projeler/omer-skills";
const GECICI = fs.mkdtempSync(path.join(os.tmpdir(), "cc-kopru-fix1-"));
const YAKALA = path.join(GECICI, "yakala.json");

// Sahte claude: argv + stdin'i dosyaya yazar, geçerli bir -p JSON'u döner.
const SAHTE = path.join(GECICI, "sahte-claude.mjs");
fs.writeFileSync(SAHTE, `
import fs from "node:fs";
let g = ""; process.stdin.setEncoding("utf8");
process.stdin.on("data", (d) => { g += d; });
process.stdin.on("end", () => {
  fs.writeFileSync(${JSON.stringify(YAKALA)}, JSON.stringify({ argv: process.argv.slice(2), stdin: g }));
  process.stdout.write(JSON.stringify({ type: "result", subtype: "success", is_error: false,
    num_turns: 1, session_id: "sahte-1", result: "OK", total_cost_usd: 0,
    usage: { input_tokens: 1, output_tokens: 1 }, modelUsage: { sonnet: {} } }));
});
`, "utf8");

// sahte yürütücüyü .cmd ile sar: sunucu doğrudan yürütücü yolunu çağırıyor
const SAHTE_CMD = path.join(GECICI, "sahte-claude.cmd");
fs.writeFileSync(SAHTE_CMD, `@echo off\r\n"${process.execPath}" "${SAHTE}" %*\r\n`, "utf8");

const AYAR_YOLU = path.join(GECICI, "kopru.json");
const ayar = JSON.parse(fs.readFileSync(path.join(KOK, "kopru.json"), "utf8"));
ayar.claudeYolu = process.execPath;
ayar.claudeOnArgs = [SAHTE];
fs.writeFileSync(AYAR_YOLU, JSON.stringify(ayar), "utf8");

function ajanCagir(args, sure = 60000) {
  return new Promise((coz, ret) => {
    const p = spawn(process.execPath, [path.join(KOK, "sunucu.mjs")], {
      cwd: "C:\\Windows\\System32", shell: false,
      env: { ...process.env, CC_KOPRU_AYAR: AYAR_YOLU },
    });
    let tampon = "";
    const gonder = (o) => p.stdin.write(JSON.stringify(o) + "\n");
    const zam = setTimeout(() => { p.kill(); ret(new Error("yanıt yok")); }, sure);
    p.stdout.on("data", (b) => {
      tampon += b.toString("utf8");
      let i;
      while ((i = tampon.indexOf("\n")) >= 0) {
        const s = tampon.slice(0, i).trim(); tampon = tampon.slice(i + 1);
        if (!s) continue;
        let m; try { m = JSON.parse(s); } catch { continue; }
        if (m.id === 1) {
          gonder({ jsonrpc: "2.0", method: "notifications/initialized" });
          gonder({ jsonrpc: "2.0", id: 2, method: "tools/call",
                   params: { name: "ajan", arguments: args } });
        } else if (m.id === 2) { clearTimeout(zam); p.kill(); coz(m.result || m.error); }
      }
    });
    gonder({ jsonrpc: "2.0", id: 1, method: "initialize",
             params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "t", version: "0" } } });
  });
}

for (const kotu of ["--dangerously-skip-permissions", "--permission-mode bypassPermissions"]) {
  test(`gorev argv'ye girmez: ${kotu}`, async () => {
    fs.rmSync(YAKALA, { force: true });
    await ajanCagir({ gorev: kotu, cwd: PROJE });
    const y = JSON.parse(fs.readFileSync(YAKALA, "utf8"));
    assert.ok(!y.argv.includes(kotu), "gorev metni argv'de olmamali: " + JSON.stringify(y.argv));
    assert.ok(!y.argv.some((a) => /dangerously-skip-permissions|bypassPermissions/i.test(a)),
              "argv izin atlama bayragi tasimamali: " + JSON.stringify(y.argv));
    assert.match(y.stdin, new RegExp(kotu.replace(/[-]/g, "\\-")), "gorev stdin'den gitmeli");
  });
}

test("argv yalnizca sabit bayraklardan olusur", async () => {
  fs.rmSync(YAKALA, { force: true });
  await ajanCagir({ gorev: "merhaba", cwd: PROJE, model: "sonnet", ajan_adi: "Explore" });
  const y = JSON.parse(fs.readFileSync(YAKALA, "utf8"));
  assert.deepEqual(y.argv,
    ["-p", "--output-format", "json", "--model", "sonnet", "--agent", "Explore"]);
});
