/**
 * KURULUM-11l K1 — claude-design köprüsü (tasarim.mjs).
 * Hiçbir vaka gerçek API çağırmaz: aktarıcı argv'si ve stream-json çözümlemesi
 * saf fonksiyon olarak sınanır, sunucu yüzeyi sahte `claude` ikilisiyle koşar.
 */
import { test } from "node:test";
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { aktariciArgv, kisaAd, semaYukle, sonucCikar } from "../tasarim.mjs";

const BURASI = path.dirname(fileURLToPath(import.meta.url));
const TASARIM = path.join(BURASI, "..", "tasarim.mjs");
const ONEK = "mcp__claude-design__";

const akis = (...olaylar) => olaylar.map((o) => JSON.stringify(o));
const initOlayi = (adlar) => ({ type: "system", subtype: "init", tools: adlar });
const kullan = (ad, girdi) => ({
  type: "assistant",
  message: { content: [{ type: "tool_use", id: "t1", name: ad, input: girdi }] },
});
const sonuc = (metin) => ({
  type: "user",
  message: { content: [{ type: "tool_result", tool_use_id: "t1", content: [{ type: "text", text: metin }] }] },
});

test("aktarici argv'si taban dusurme bayraklarini birebir tasir", () => {
  const argv = aktariciArgv(ONEK + "list_projects");
  const deger = (bayrak) => argv[argv.indexOf(bayrak) + 1];

  assert.equal(deger("--setting-sources"), "", "CLAUDE.md/hook/plugin/SessionStart düşmeli");
  assert.equal(deger("--tools"), "", "yerleşik araç kalmamalı");
  assert.equal(deger("--model"), "haiku");
  assert.equal(deger("--output-format"), "stream-json");
  assert.ok(argv.includes("--strict-mcp-config"), "yalnız verilen MCP config geçerli");
  assert.equal(argv.filter((a) => a === "--allowedTools").length, 1, "tek --allowedTools");
  assert.equal(deger("--allowedTools"), ONEK + "list_projects");
  assert.ok(!argv.includes("--max-turns"), "CC CLI'da böyle bir bayrak yok");
  assert.ok(!argv.some((a) => /dangerously|bypassPermissions|permission-mode/i.test(a)));
});

test("sema dosyasi 23 gercek girisi init adlariyla birebir tutar", () => {
  const semalar = semaYukle();
  assert.equal(semalar.length, 23, "yakalanan şema sayısı");
  for (const s of semalar) {
    assert.ok(s.name.startsWith(ONEK), "yabancı giriş: " + s.name);
    assert.equal(typeof s.description, "string");
    assert.ok(s.description.length > 0, s.name + ": açıklama boş");
    assert.equal(s.input_schema?.type, "object", s.name + ": şema gövdesi yok");
  }
  assert.equal(kisaAd(ONEK + "list_projects"), "list_projects");
});

test("sonuc modelin cumlesinden degil tool_result'tan birebir alinir", () => {
  const adlar = semaYukle().map((s) => s.name);
  const r = sonucCikar(akis(
    initOlayi(adlar),
    kullan(ONEK + "list_projects", {}),
    sonuc('{"projects":[]}'),
    { type: "result", result: "Kayıtlı proje bulunmuyor." },
  ), ONEK + "list_projects", {}, adlar);
  assert.equal(r.metin, '{"projects":[]}');
  assert.ok(!r.hata, r.hata);
});

test("baska arac cagrilirsa hata doner", () => {
  const adlar = semaYukle().map((s) => s.name);
  const r = sonucCikar(akis(initOlayi(adlar), kullan(ONEK + "create_project", {}), sonuc("x")),
                       ONEK + "list_projects", {}, adlar);
  assert.match(r.hata || "", /başka araç|create_project/i);
});

test("argumanlar birebir degilse hata doner", () => {
  const adlar = semaYukle().map((s) => s.name);
  const r = sonucCikar(akis(initOlayi(adlar), kullan(ONEK + "get_project", { id: "b" }), sonuc("x")),
                       ONEK + "get_project", { id: "a" }, adlar);
  assert.match(r.hata || "", /argüman/i);
});

test("tool_result gelmezse hata doner (zaman asimi/bos akis)", () => {
  const adlar = semaYukle().map((s) => s.name);
  const r = sonucCikar(akis(initOlayi(adlar), kullan(ONEK + "list_projects", {})),
                       ONEK + "list_projects", {}, adlar);
  assert.match(r.hata || "", /tool_result/i);
});

test("init ad listesi degisirse onbellek gecersiz sayilir", () => {
  const adlar = semaYukle().map((s) => s.name);
  const r = sonucCikar(akis(initOlayi(adlar.slice(1)), kullan(ONEK + "list_projects", {}), sonuc("x")),
                       ONEK + "list_projects", {}, adlar);
  assert.match(r.hata || "", /önbellek|geçersiz/i);
});

test("acilista claude spawn edilmez, 23 arac dosyadan yayinlanir", async () => {
  const kum = fs.mkdtempSync(path.join(os.tmpdir(), "tasarim-"));
  const isaret = path.join(kum, "spawn-oldu.txt");
  fs.writeFileSync(path.join(kum, "claude.cmd"),
    "@echo off\r\necho spawn > \"" + isaret + "\"\r\n");

  const tools = await new Promise((coz, ret) => {
    const p = spawn(process.execPath, [TASARIM], {
      cwd: "C:\\Windows\\System32",
      shell: false,
      env: { ...process.env, PATH: kum + path.delimiter + process.env.PATH },
    });
    let tampon = "";
    const gonder = (o) => p.stdin.write(JSON.stringify(o) + "\n");
    const zam = setTimeout(() => { p.kill(); ret(new Error("sunucu yanıt vermedi")); }, 30000);
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
          gonder({ jsonrpc: "2.0", id: 2, method: "tools/list", params: {} });
        } else if (m.id === 2) {
          clearTimeout(zam); p.kill(); coz(m.result?.tools || []);
        }
      }
    });
    gonder({
      jsonrpc: "2.0", id: 1, method: "initialize",
      params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "t", version: "0" } },
    });
  });

  assert.equal(tools.length, 23, "yayınlanan araç sayısı");
  assert.ok(tools.some((t) => t.name === "list_projects"), "kısa adla yayınlanmalı");
  assert.equal(fs.existsSync(isaret), false, "açılışta claude çağrılmış");
  fs.rmSync(kum, { recursive: true, force: true });
});

/** B2 kök neden pini: alt süreç ANTHROPIC_BASE_URL'i miras alırsa araç hiç çağrılmaz. */
test("aktarici ANTHROPIC_BASE_URL'i alt surece gecirmez (vekil araclari gizliyor)", async () => {
  const yardimci = path.join(BURASI, "yardim", "sahte-claude.mjs");

  const metin = await new Promise((coz, ret) => {
    const p = spawn(process.execPath, [TASARIM], {
      cwd: "C:\\Windows\\System32",
      shell: false,
      env: {
        ...process.env,
        CC_KOPRU_SAHTE_AKTARICI: yardimci,
        ANTHROPIC_BASE_URL: "http://127.0.0.1:1",
      },
    });
    let tampon = "";
    const gonder = (o) => p.stdin.write(JSON.stringify(o) + "\n");
    const zam = setTimeout(() => { p.kill(); ret(new Error("sunucu yanıt vermedi")); }, 30000);
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
          gonder({ jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "list_projects", arguments: {} } });
        } else if (m.id === 2) {
          clearTimeout(zam); p.kill();
          coz((m.result?.content || []).map((c) => c.text).join("\n"));
        }
      }
    });
    gonder({
      jsonrpc: "2.0", id: 1, method: "initialize",
      params: { protocolVersion: "2024-11-05", capabilities: {}, clientInfo: { name: "t", version: "0" } },
    });
  });

  assert.equal(metin, "SAHTE-SONUC", "vekil miras alındı: model aracı görmedi, tool_use gelmedi");
});
