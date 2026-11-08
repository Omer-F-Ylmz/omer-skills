/**
 * KÖPRÜ-HIZ: `ajan` tek kuyruğa (sirala) girmez; ajanTavan ömür boyu değil EŞZAMANLI tavandır.
 * Sahte claude bırakma dosyası görene dek koşar; API çağrısı yok.
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
const GECICI = fs.mkdtempSync(path.join(os.tmpdir(), "cc-kopru-tavan-"));

// Sahte claude: basladi-<pid> yazar, birak-<pid> ya da birak-hepsi görünce -p JSON'u döner.
const SAHTE = path.join(GECICI, "sahte-claude.mjs");
fs.writeFileSync(SAHTE, `
import fs from "node:fs";
import path from "node:path";
const D = ${JSON.stringify(GECICI)};
process.stdin.resume();
fs.writeFileSync(path.join(D, "basladi-" + process.pid), "");
const t0 = Date.now();
const z = setInterval(() => {
  const bitti = ["birak-" + process.pid, "birak-hepsi"].some((a) => fs.existsSync(path.join(D, a)));
  if (!bitti && Date.now() - t0 < 120000) return;
  clearInterval(z);
  process.stdout.write(JSON.stringify({ type: "result", subtype: "success", is_error: false,
    num_turns: 1, session_id: "sahte-" + process.pid, result: "OK", total_cost_usd: 0,
    usage: { input_tokens: 1, output_tokens: 1 }, modelUsage: { sonnet: {} } }));
  process.exit(0);
}, 50);
`, "utf8");

const AYAR_YOLU = path.join(GECICI, "kopru.json");
const ayar = JSON.parse(fs.readFileSync(path.join(KOK, "kopru.json"), "utf8"));
ayar.claudeYolu = process.execPath;
ayar.claudeOnArgs = [SAHTE];
ayar.ajanTavan = 2;
fs.writeFileSync(AYAR_YOLU, JSON.stringify(ayar), "utf8");

const bekle = (ms) => new Promise((r) => setTimeout(r, ms));
async function kosul(f, sure = 20000) {
  const t0 = Date.now();
  while (!f()) {
    if (Date.now() - t0 > sure) throw new Error("koşul zaman aşımı");
    await bekle(50);
  }
}
const baslayanlar = () => fs.readdirSync(GECICI).filter((a) => a.startsWith("basladi-"));
const govde = (r) => (r.content || []).map((c) => c.text).join("\n");

/** Tek sunucu süreci; her çağrı kendi id'siyle, yanıtlar sırasız toplanır. */
function sunucuAc() {
  const p = spawn(process.execPath, [path.join(KOK, "sunucu.mjs")], {
    cwd: "C:\\Windows\\System32", shell: false,
    env: { ...process.env, CC_KOPRU_AYAR: AYAR_YOLU },
  });
  const bekleyen = new Map();
  let tampon = "", sira = 1;
  const gonder = (o) => p.stdin.write(JSON.stringify(o) + "\n");
  p.stdout.on("data", (b) => {
    tampon += b.toString("utf8");
    let i;
    while ((i = tampon.indexOf("\n")) >= 0) {
      const s = tampon.slice(0, i).trim(); tampon = tampon.slice(i + 1);
      let m; try { m = JSON.parse(s); } catch { continue; }
      bekleyen.get(m.id)?.(m.result || m.error);
    }
  });
  const istek = (method, params) => new Promise((coz) => {
    const id = sira++;
    bekleyen.set(id, coz);
    gonder({ jsonrpc: "2.0", id, method, params });
  });
  const hazir = istek("initialize", { protocolVersion: "2024-11-05", capabilities: {},
                                      clientInfo: { name: "t", version: "0" } })
    .then(() => gonder({ jsonrpc: "2.0", method: "notifications/initialized" }));
  return {
    cagir: async (name, args) => { await hazir; return istek("tools/call", { name, arguments: args }); },
    kapat: () => p.kill(),
  };
}

test("ajan: eşzamanlı tavan", async (t) => {
  const s = sunucuAc();
  t.after(() => { fs.writeFileSync(path.join(GECICI, "birak-hepsi"), ""); s.kapat(); });

  const a1 = s.cagir("ajan", { gorev: "bir", cwd: PROJE });
  const a2 = s.cagir("ajan", { gorev: "iki", cwd: PROJE });
  let a4, biten = 0;
  for (const a of [a1, a2]) a.then(() => { biten += 1; });

  await t.test("iki ajan aynı anda koşar (kuyruk yok)", async () => {
    await kosul(() => baslayanlar().length === 2);
  });

  await t.test("tavan doluyken yeni ajan RED", async () => {
    const r = await s.cagir("ajan", { gorev: "uc", cwd: PROJE });
    assert.equal(r.isError, true, govde(r));
    assert.match(govde(r), /eşzamanlı ajan tavanı \(2\) dolu/);
    assert.equal(baslayanlar().length, 2, "RED alan ajan süreç başlatmamalı");
  });

  await t.test("ajanlar koşarken komut bloke olmaz", async () => {
    const r = await s.cagir("komut", { arac: "gitleaks", args: ["version"], cwd: PROJE });
    assert.notEqual(r.isError, true, govde(r));
    assert.match(govde(r), /exit 0/);
    assert.equal(biten, 0, "komut ajanların bitmesini beklememeli");
  });

  await t.test("bir ajan bitince yeni ajan kabul edilir", async () => {
    fs.writeFileSync(path.join(GECICI, "birak-" + baslayanlar()[0].slice("basladi-".length)), "");
    const ilk = await Promise.race([a1, a2]);
    assert.notEqual(ilk.isError, true, govde(ilk));
    assert.match(govde(ilk), /^OK/);
    a4 = s.cagir("ajan", { gorev: "dort", cwd: PROJE });
    await kosul(() => baslayanlar().length === 3);
  });

  await t.test("bırakılan ajanlar sızıntısız döner", async () => {
    fs.writeFileSync(path.join(GECICI, "birak-hepsi"), "");
    for (const r of await Promise.all([a1, a2, a4])) {
      assert.notEqual(r.isError, true, govde(r));
      assert.match(govde(r), /^OK/);
    }
  });
});
