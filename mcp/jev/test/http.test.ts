import { afterEach, beforeEach, describe, expect, it } from "vitest";
import { createServer, type Server } from "node:http";
import type { AddressInfo } from "node:net";
import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import handler, { yetkili } from "../src/http.js";

const TOKEN = "a".repeat(64);
let sunucu: Server;
let url: string;

beforeEach(async () => {
  process.env.JEV_MCP_TOKEN = TOKEN;
  sunucu = createServer((req, res) => void handler(req, res));
  await new Promise<void>((r) => sunucu.listen(0, "127.0.0.1", r));
  url = `http://127.0.0.1:${(sunucu.address() as AddressInfo).port}/api/mcp`;
});
afterEach(() => {
  sunucu.close();
  delete process.env.JEV_MCP_TOKEN;
});

const listele = (baslik: Record<string, string>) =>
  fetch(url, {
    method: "POST",
    headers: { "content-type": "application/json", accept: "application/json, text/event-stream", ...baslik },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/list", params: {} }),
  });

describe("X-Jev-Token", () => {
  it("tokensiz 401", async () => expect((await listele({})).status).toBe(401));
  it("yanlis token 401", async () => expect((await listele({ "x-jev-token": "b".repeat(64) })).status).toBe(401));
  it("onek token 401", async () => expect((await listele({ "x-jev-token": TOKEN.slice(0, 63) })).status).toBe(401));
  it("Authorization kabul edilmez", async () => expect((await listele({ authorization: `Bearer ${TOKEN}` })).status).toBe(401));
  it("sunucuda token yoksa 401", async () => {
    delete process.env.JEV_MCP_TOKEN;
    expect((await listele({ "x-jev-token": TOKEN })).status).toBe(401);
  });
  it("dogru token tools/list 3 arac", async () => {
    const r = await listele({ "x-jev-token": TOKEN });
    expect(r.status).toBe(200);
    const govde = await r.json();
    expect(govde.result.tools.map((t: { name: string }) => t.name).sort()).toEqual(["jev_batch", "jev_evaluate", "jev_models"]);
  });
  it("dogru x-api-key 200", async () => expect((await listele({ "x-api-key": TOKEN })).status).toBe(200));
  it("yanlis x-api-key 401", async () => expect((await listele({ "x-api-key": "b".repeat(64) })).status).toBe(401));
  it("celiskili basliklar 401 (x-api-key yanlis)", async () =>
    expect((await listele({ "x-jev-token": TOKEN, "x-api-key": "b".repeat(64) })).status).toBe(401));
  it("celiskili basliklar 401 (x-jev-token yanlis)", async () =>
    expect((await listele({ "x-jev-token": "b".repeat(64), "x-api-key": TOKEN })).status).toBe(401));
  it("iki baslik da dogru 200", async () => expect((await listele({ "x-jev-token": TOKEN, "X-API-Key": TOKEN })).status).toBe(200));
  it("yetkili: esit uzunlukta tek karakter fark reddedilir", () => {
    expect(yetkili(TOKEN, TOKEN)).toBe(true);
    expect(yetkili(TOKEN.slice(0, -1) + "b", TOKEN)).toBe(false);
    expect(yetkili(undefined, TOKEN)).toBe(false);
    expect(yetkili(TOKEN, undefined)).toBe(false);
  });
});

// claude.ai 401 + WWW-Authenticate/resource_metadata görünce OAuth akışına girer.
describe("OAuth izi yok", () => {
  it("401'de WWW-Authenticate ve resource_metadata yok", async () => {
    const r = await listele({});
    expect(r.status).toBe(401);
    expect(r.headers.get("www-authenticate")).toBeNull();
    expect(await r.text()).not.toMatch(/resource_metadata|oauth/i);
  });
  it("tek rota /mcp; .well-known icin fonksiyon/statik dosya yok", () => {
    const kok = fileURLToPath(new URL("..", import.meta.url));
    expect(JSON.parse(readFileSync(join(kok, "vercel.json"), "utf8")).rewrites).toEqual([{ source: "/mcp", destination: "/api/mcp" }]);
    expect(readdirSync(join(kok, "api"))).toEqual(["mcp.js"]);
    expect(readdirSync(join(kok, "public"))).toEqual([".gitkeep"]);
  });
});
