/**
 * Sunucu entegrasyon testleri. Birim testleri yeşilken bağlantının kopuk olması
 * (ajanAlanDenetle yazılmış ama argv'ye bağlanmamış) gerçekten yaşandı — bu dosya
 * denetimlerin sunucu yüzeyinde uygulandığını kanıtlar. Hiçbir vaka API çağırmaz.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const SUNUCU = path.join(path.dirname(fileURLToPath(import.meta.url)), "..", "sunucu.mjs");
const PROJE = "C:/Projeler/omer-skills";

/** Sunucuyu ayağa kaldırır, verilen tools/call'ları sırayla sorar. */
function cagir(vakalar, sure = 60000) {
  return new Promise((coz, ret) => {
    const p = spawn(process.execPath, [SUNUCU], { cwd: "C:\\Windows\\System32", shell: false });
    const sonuc = new Map();
    let tampon = "";
    const gonder = (o) => p.stdin.write(JSON.stringify(o) + "\n");
    const zam = setTimeout(() => { p.kill(); ret(new Error("sunucu yanıt vermedi")); }, sure);

    p.stdout.on("data", (b) => {
      tampon += b.toString("utf8");
      let i;
      while ((i = tampon.indexOf("\n")) >= 0) {
        const satir = tampon.slice(0, i).trim();
        tampon = tampon.slice(i + 1);
        if (!satir) continue;
        let m;
        try { m = JSON.parse(satir); } catch { continue; }
        if (m.id === 1) {
          gonder({ jsonrpc: "2.0", method: "notifications/initialized" });
          vakalar.forEach((v, n) => gonder({
            jsonrpc: "2.0", id: n + 2, method: "tools/call",
            params: { name: v.arac, arguments: v.args },
          }));
        } else if (m.id >= 2) {
          sonuc.set(m.id - 2, m.result || m.error);
          if (sonuc.size === vakalar.length) {
            clearTimeout(zam); p.kill();
            coz(vakalar.map((_, n) => sonuc.get(n)));
          }
        }
      }
    });
    gonder({
      jsonrpc: "2.0", id: 1, method: "initialize",
      params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "t", version: "0" } },
    });
  });
}

const govde = (r) => (r?.content || [{}])[0]?.text || "";

test("ajan: argv alanlari sunucu yuzeyinde reddedilir (surec baslatilmaz)", async () => {
  const [a, b, c] = await cagir([
    { arac: "ajan", args: { gorev: "x", cwd: PROJE, ajan_adi: "--dangerously-skip-permissions" } },
    { arac: "ajan", args: { gorev: "x", cwd: PROJE, model: "-p" } },
    { arac: "ajan", args: { gorev: "x", cwd: PROJE, devam_id: "y --permission-mode bypassPermissions" } },
  ]);
  for (const [ad, r] of [["ajan_adi", a], ["model", b], ["devam_id", c]]) {
    assert.equal(r.isError, true, ad + " reddedilmeli");
    assert.match(govde(r), /RED: /, ad);
    assert.doesNotMatch(govde(r), /claude -p/, ad + ": surec baslatilmis olmamali");
  }
});

test("komut: git -c ve --exec-path sunucu yuzeyinde reddedilir", async () => {
  const [a, b] = await cagir([
    { arac: "komut", args: { arac: "git", args: ["-c", "core.pager=calc.exe", "log"], cwd: PROJE } },
    { arac: "komut", args: { arac: "git", args: ["log", "--exec-path=C:/x"], cwd: PROJE } },
  ]);
  for (const r of [a, b]) {
    assert.equal(r.isError, true);
    assert.match(govde(r), /secenek/i);
  }
});

test("komut: normal yol calisir ve rtk hook'u devrede", async () => {
  const [r] = await cagir([
    { arac: "komut", args: { arac: "gitleaks", args: ["version"], cwd: PROJE } },
  ]);
  assert.notEqual(r.isError, true, govde(r));
  assert.match(govde(r), /exit 0/);
});

/**
 * 11l-FIX K1: denetimin eklediği `--` ayırıcısı hook yeniden yazımından sonra da
 * argv'de kalmalı. Ayırıcısız `npx --no pixeljury --version` npm'in kendi sürümünü
 * basıyor (11.17.0); ayırıcıyla paket koşuyor (0.1.5). rtk hook'u gerçek uçta koşar.
 */
test("komut: npx `--` ayiricisi hook yeniden yaziminda korunur", async () => {
  const [r] = await cagir([
    { arac: "komut", args: { arac: "npx", args: ["--no", "pixeljury", "--version"], cwd: PROJE } },
  ]);
  assert.match(govde(r), /rtk npx --no -- pixeljury --version/, govde(r));
  assert.match(govde(r), /0\.1\.5/, govde(r));
  assert.doesNotMatch(govde(r), /11\.17\.0/, govde(r));
});
