/**
 * KURULUM-11m-A-FIX-2 K2 — Desktop taklidi: köprü kısıtlı ortamda ayakta kalıyor mu?
 *
 * Desktop yerel MCP sunucularını tam kullanıcı ortamıyla değil, MCP SDK'nın beyaz
 * listesiyle başlatır (DEFAULT_INHERITED_ENV_VARS) ve cwd=System32 verir. O ortamda
 * hook süreçleri (PYTHONPATH'siz python, vb.) girdilerini OKUMADAN çıkıyor; köprü de
 * onların stdin'ine yazarken EPIPE/EOF alıp "Unhandled 'error' event" ile düşüyordu.
 * Belirti: ilk `komut` çağrısı "Tool execution failed", sonrasında her araç kopuk.
 */
import assert from "node:assert/strict";
import http from "node:http";
import path from "node:path";
import test from "node:test";

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const KOPRU = path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), "..");
const PROJE = path.resolve(KOPRU, "..", "..");
/** Claude Desktop'ın alt sürece geçirdiği değişkenler (app.asar ofset 3899305). */
const DESKTOP_ENV = ["APPDATA", "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA", "PATH",
  "PROCESSOR_ARCHITECTURE", "SYSTEMDRIVE", "SYSTEMROOT", "TEMP", "USERNAME",
  "USERPROFILE", "PROGRAMFILES"];

async function desktopKopru(ekOrtam = {}) {
  const t = new StdioClientTransport({
    command: path.join(PROJE, "tools", "mcp-launch", "cc-kopru.cmd"),
    args: [],
    env: {
      ...Object.fromEntries(DESKTOP_ENV.filter((k) => process.env[k]).map((k) => [k, process.env[k]])),
      ...ekOrtam,
    },
    cwd: path.join(process.env.SYSTEMROOT, "System32"),
  });
  const c = new Client({ name: "desktop-testi", version: "0.1.0" });
  await c.connect(t);
  c.cagir = async (ad, args) => {
    const r = await c.callTool({ name: ad, arguments: args }, undefined, { timeout: 60000 });
    return (r?.content || []).map((x) => x.text || "").join("\n");
  };
  return c;
}

test("Desktop ortamında gh api yanıt verir", async () => {
  const c = await desktopKopru();
  try {
    const s = await c.cagir("komut", {
      arac: "gh", args: ["api", "repos/Omer-F-Ylmz/omer-skills/commits"], cwd: PROJE,
    });
    assert.match(s, /exit 0/, s.slice(0, 200));
    assert.ok(s.includes('"sha"') || s.includes("headroom"), s.slice(0, 200));
    // hook ortamı CC ile eşit: kısıtlı ortamda hiçbir hook hata koduyla çıkmaz (EK K2).
    // Yalnız başlık sınanır: gövde gh'ın JSON'u ve commit metinleri bu kalıbı içerebiliyor.
    const bas = s.slice(0, s.indexOf("exit "));
    assert.doesNotMatch(bas, /\[hook hata:/, bas);
  } finally { await c.close(); }
}, { timeout: 180000 });

/**
 * 11m-A-FIX-3 K1: aynı komut worker'a İKİ kez yazılıyordu — claude-mem'in PostToolUse
 * hook'u (tool=Bash) ve köprünün kendi gözlemi (tool=cc-kopru:komut). Kanıt: worker
 * log session-406, 14:00:55 ve 14:00:57 ENQUEUED, tek `gh api` çağrısı.
 * Sahte worker hem köprünün hem hook'un portudur (ikisi de CLAUDE_MEM_WORKER_PORT okur).
 */
test("köprüden bir komut worker'a tek gözlem isteği yazar", async () => {
  const istek = [];
  const srv = http.createServer((q, y) => {
    if (q.url.startsWith("/api/sessions/observations")) istek.push(q.url);
    y.writeHead(200, { "content-type": "application/json" });
    y.end(JSON.stringify({ status: "queued", healthy: true, ready: true }));
  });
  await new Promise((r) => srv.listen(0, "127.0.0.1", r));
  const c = await desktopKopru({ CLAUDE_MEM_WORKER_PORT: String(srv.address().port) });
  try {
    const s = await c.cagir("komut", { arac: "git", args: ["log", "-3", "--oneline"], cwd: PROJE });
    assert.match(s, /exit 0/, s.slice(0, 200));
    assert.equal(istek.length, 1, `gözlem isteği sayısı: ${istek.length}`);
  } finally {
    await c.close();
    await new Promise((r) => srv.close(r));
  }
}, { timeout: 180000 });

test("hatalı komut aynı süreçteki sonraki çağrıyı düşürmez", async () => {
  const c = await desktopKopru();
  try {
    // Hook süreçleri bu ortamda girdiyi okumadan çıkıyor. Küçük girdi boru
    // tamponuna sığıp sorunsuz geçiyor; köprüyü düşüren BÜYÜK çıktılı çağrı.
    try {
      await c.cagir("komut", {
        arac: "gh", args: ["api", "repos/Omer-F-Ylmz/omer-skills/commits"], cwd: PROJE,
      });
    } catch { /* bu çağrının sonucu önemsiz; süreç ayakta kalmalı */ }
    const s = await c.cagir("komut", { arac: "git", args: ["log", "-3", "--oneline"], cwd: PROJE });
    assert.match(s, /exit 0/, s.slice(0, 200));
  } finally { await c.close(); }
}, { timeout: 180000 });
