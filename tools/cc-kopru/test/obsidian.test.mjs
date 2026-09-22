/** KURULUM-11m-A K1 — Obsidian köprüsü: kapalı uç · önbellek · yeniden bağlanma. */
import assert from "node:assert/strict";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const ARACLAR = [{
  name: "obsidian_ara",
  description: "kasada arama",
  inputSchema: { type: "object", properties: { q: { type: "string" } }, required: ["q"] },
}];

/** Eklentiyi taklit eden SSE ucu: gerçek Obsidian açılmadan da yol denenebilsin. */
async function sahteUc() {
  const srv = new Server({ name: "sahte-obsidian", version: "0" }, { capabilities: { tools: {} } });
  srv.setRequestHandler(ListToolsRequestSchema, () => ({ tools: ARACLAR }));
  srv.setRequestHandler(CallToolRequestSchema, (i) => ({
    content: [{ type: "text", text: `çağrıldı: ${i.params.name} ${JSON.stringify(i.params.arguments)}` }],
  }));
  let tasima = null;
  const http_ = http.createServer(async (req, res) => {
    if (req.method === "GET") {
      tasima = new SSEServerTransport("/mesaj", res);
      await srv.connect(tasima);
    } else if (tasima) {
      await tasima.handlePostMessage(req, res);
    } else { res.writeHead(400).end(); }
  });
  await new Promise((r) => http_.listen(0, "127.0.0.1", r));
  // SSE bağlantısı açık kaldığı sürece `close()` beklemede kalır ve `node --test`
  // olay döngüsü hiç boşalmaz; soketler de kapatılır.
  return {
    uc: `http://127.0.0.1:${http_.address().port}/sse`,
    kapat: () => { http_.closeAllConnections(); http_.close(); },
  };
}

const gecici = () => path.join(os.tmpdir(), `obs-sema-${Date.now()}-${Math.random().toString(36).slice(2)}.json`);

test("uç kapalıyken tools/list atmaz, önbellekten döner", async () => {
  const { araclariGetir, baglantiDusur } = await import("../obsidian.mjs");
  const sema = gecici();
  fs.writeFileSync(sema, JSON.stringify(ARACLAR), "utf8");
  baglantiDusur();
  // 127.0.0.1:1 dinlenmiyor: bağlantı reddi anında gelir.
  const r = await araclariGetir({ uc: "http://127.0.0.1:1/sse", sema, zamanMs: 3000 });
  assert.equal(r.canli, false);
  assert.equal(r.araclar.length, 1);
  assert.equal(r.araclar[0].name, "obsidian_ara");
  fs.rmSync(sema, { force: true });
});

test("uç kapalı, önbellek de yoksa tools/list boş liste döner (atmaz)", async () => {
  const { araclariGetir, baglantiDusur } = await import("../obsidian.mjs");
  baglantiDusur();
  const r = await araclariGetir({ uc: "http://127.0.0.1:1/sse", sema: gecici(), zamanMs: 3000 });
  assert.deepEqual(r.araclar, []);
  assert.equal(r.canli, false);
});

test("uç kapalıyken araç çağrısı 'Obsidian kapalı' döner", async () => {
  const { KAPALI_METIN, aracCagir, baglantiDusur } = await import("../obsidian.mjs");
  baglantiDusur();
  const r = await aracCagir("obsidian_ara", { q: "x" }, { uc: "http://127.0.0.1:1/sse", zamanMs: 3000 });
  assert.equal(r.isError, true);
  assert.match(r.content[0].text, new RegExp(KAPALI_METIN));
});

test("uç sonradan açılınca aynı süreçte ilk çağrı bağlanır ve şema önbelleğe yazılır", async () => {
  const { aracCagir, araclariGetir, baglantiDusur, semaOku } = await import("../obsidian.mjs");
  const sema = gecici();
  baglantiDusur();

  // 1) kapalı: çağrı reddedilir
  const kapali = await aracCagir("obsidian_ara", { q: "a" }, { uc: "http://127.0.0.1:1/sse", zamanMs: 3000 });
  assert.equal(kapali.isError, true);

  // 2) uç açılır — süreç yeniden başlatılmaz
  const u = await sahteUc();
  try {
    const liste = await araclariGetir({ uc: u.uc, sema, zamanMs: 5000 });
    assert.equal(liste.canli, true);
    assert.equal(liste.araclar[0].name, "obsidian_ara");
    assert.equal(semaOku(sema)[0].name, "obsidian_ara", "başarılı liste önbelleğe yazılır");

    const r = await aracCagir("obsidian_ara", { q: "a" }, { uc: u.uc, zamanMs: 5000 });
    assert.ok(!r.isError, JSON.stringify(r));
    assert.match(r.content[0].text, /çağrıldı: obsidian_ara/);
  } finally {
    baglantiDusur();
    u.kapat();
    fs.rmSync(sema, { force: true });
  }
});
