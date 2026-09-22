#!/usr/bin/env node
/**
 * KURULUM-11l K1 — claude-design köprüsü.
 *
 * 23 şema `tasarim-semalar.json`'dan **birebir** yayınlanır (kaynak: K1b yakalayıcı,
 * CC'nin kendi API isteğindeki `tools` dizisi). Gövde tek ortak aktarıcıya gider:
 * `claude -p` CC'nin OAuth'lu claude-design bağlantısını yeniden kullanır, sonuç
 * modelin cümlesinden değil stream-json'daki `tool_result` bloğundan alınır.
 *
 * Açılışta hiç süreç başlatılmaz — Desktop sunucuyu 4 süreçle açıyor (11l kanıtı).
 * Şemaların geçerliliği ilk çağrının zaten gelen `init` olayından denetlenir.
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";

import { agaciKapat, ciktiHazirla, redakte, yolBul } from "./kos.mjs";

const BURASI = path.dirname(fileURLToPath(import.meta.url));

export const ONEK = "mcp__claude-design__";
export const SEMA_DOSYASI = path.join(BURASI, "tasarim-semalar.json");
export const DESIGN_URL = "https://api.anthropic.com/v1/design/mcp";
export const SISTEM_PROMPT =
  "Yalnız istenen aracı verilen argümanlarla bir kez çağır, başka hiçbir şey yapma.";

export const kisaAd = (tamAd) => tamAd.replace(ONEK, "");

/** Aktarıcı argv'si — taban düşürme bayrakları burada tek yerde durur (K1b aynısını kullanır). */
export function aktariciArgv(tamAd) {
  return [
    "-p", "--output-format", "stream-json", "--verbose", "--model", "haiku",
    "--setting-sources", "",          // CLAUDE.md · hook · plugin · SessionStart düşer
    "--tools", "",                    // yerleşik araç yok
    "--system-prompt", SISTEM_PROMPT, // varsayılan sistem promptunun yerine geçer
    "--strict-mcp-config", "--mcp-config",
    JSON.stringify({ mcpServers: { "claude-design": { type: "http", url: DESIGN_URL } } }),
    "--allowedTools", tamAd,
  ];
}

let semaOnbellek = null;
export function semaYukle() {
  if (!semaOnbellek) semaOnbellek = JSON.parse(fs.readFileSync(SEMA_DOSYASI, "utf8"));
  return semaOnbellek;
}

/** Anahtar sırasından bağımsız karşılaştırma: argüman eşitliği biçime takılmasın. */
function sabitle(v) {
  if (Array.isArray(v)) return v.map(sabitle);
  if (v && typeof v === "object") {
    return Object.keys(v).sort().reduce((o, k) => ((o[k] = sabitle(v[k])), o), {});
  }
  return v;
}
const esit = (a, b) => JSON.stringify(sabitle(a)) === JSON.stringify(sabitle(b));

/** stream-json satırlarından sonucu çıkarır; her sapma hata döner, özet üretilmez. */
export function sonucCikar(satirlar, beklenenAd, beklenenGirdi, beklenenAdlar) {
  let init = null, kullanim = null, sonuc = null;
  for (const satir of satirlar) {
    let o;
    try { o = JSON.parse(satir); } catch { continue; }
    if (o.type === "system" && o.subtype === "init") init = o.tools || [];
    for (const blok of o.message?.content || []) {
      if (blok.type === "tool_use" && !kullanim) kullanim = blok;
      if (blok.type === "tool_result" && !sonuc) sonuc = blok;
    }
  }

  if (init) {
    const gelen = init.filter((a) => a.startsWith(ONEK)).sort();
    const beklenen = [...beklenenAdlar].sort();
    if (!esit(gelen, beklenen)) {
      return { hata: `şema önbelleği geçersiz: uçta ${gelen.length} araç, dosyada ${beklenen.length}` };
    }
  }

  if (!kullanim) return { hata: "aktarıcı aracı çağırmadı (tool_use yok)" };
  if (kullanim.name !== beklenenAd) {
    return { hata: `başka araç çağrıldı: ${kullanim.name} (beklenen ${beklenenAd})` };
  }
  if (!esit(kullanim.input || {}, beklenenGirdi || {})) {
    return { hata: "argümanlar birebir değil: " + redakte(JSON.stringify(kullanim.input)) };
  }
  if (!sonuc) return { hata: "tool_result gelmedi (zaman aşımı ya da boş akış)" };

  const icerik = sonuc.content;
  const metin = typeof icerik === "string"
    ? icerik
    : (icerik || []).map((b) => b.text ?? JSON.stringify(b)).join("\n");
  return { metin };
}

/**
 * Test tohumu (11l K1c): yalnız `test/yardim/` altındaki var olan bir dosya kabul edilir.
 * Başka yol ya da tanımsız değişken yok sayılır — aktarıcı gerçek `claude` ikilisini seçer,
 * böylece dışarıdan verilen bir yol köprünün çağırdığı ikiliyi değiştiremez.
 */
export function sahteAktarici(deger = process.env.CC_KOPRU_SAHTE_AKTARICI) {
  if (!deger) return null;
  const yol = path.resolve(String(deger));
  const kok = path.join(BURASI, "test", "yardim") + path.sep;
  return yol.startsWith(kok) && fs.existsSync(yol) ? yol : null;
}

/** Ortak aktarıcı: ilk `tool_result` geldiği anda süreç kapatılır (--max-turns yok). */
export function aktar(tamAd, girdi, { timeoutSn = 120 } = {}) {
  return new Promise((coz) => {
    // Test tohumu: Windows'ta sahte `claude.exe` üretilemediği için (node .cmd'yi
    // kabuksuz spawn etmiyor, bilinmeyen bayrakta da düşüyor) aktarıcı yerine bir
    // node betiği koşulur. Üretimde değişken yoktur.
    const sahte = sahteAktarici();
    const claude = sahte ? process.execPath : yolBul("claude");
    if (!claude) return coz({ hata: "claude PATH'te bulunamadı" });

    // ANTHROPIC_BASE_URL düşürülür: yerel headroom vekili tools dizisini tek arama
    // aracına indiriyor, model list_projects'i hiç görmüyor → tool_use gelmiyor (B2).
    const ortam = { ...process.env };
    delete ortam.ANTHROPIC_BASE_URL;
    const argv = sahte ? [sahte, ...aktariciArgv(tamAd)] : aktariciArgv(tamAd);
    const p = spawn(claude, argv, { shell: false, cwd: os.tmpdir(), env: ortam });
    const parcalar = [];
    let bitti = false;
    const kapat = () => { if (!bitti) { bitti = true; agaciKapat(p.pid); p.kill(); } };
    const zam = setTimeout(kapat, timeoutSn * 1000);

    // Çocuk istemi okumadan çıkarsa EPIPE sunucuyu düşürmesin (11m-A-FIX-2).
    p.stdin.on("error", () => { /* istem yazılamadı; çıkış kodu değerlendirilir */ });
    p.stdin.end(`${kisaAd(tamAd)} aracını şu argümanlarla çağır: ${JSON.stringify(girdi || {})}`);
    p.stdout.on("data", (b) => {
      parcalar.push(b);
      if (b.toString("utf8").includes('"tool_result"')) kapat();
    });
    p.stderr.on("data", (b) => parcalar.push(b));
    p.on("error", (e) => { clearTimeout(zam); coz({ hata: "aktarıcı başlatılamadı: " + e.message }); });
    p.on("close", () => {
      clearTimeout(zam);
      const satirlar = Buffer.concat(parcalar).toString("utf8").split(/\r?\n/).filter(Boolean);
      coz(sonucCikar(satirlar, tamAd, girdi, semaYukle().map((s) => s.name)));
    });
  });
}

/**
 * Şemalar JSON Schema olarak birebir yayınlanır. `McpServer.registerTool` Zod
 * bekliyor (SDK 1.30 `getZodSchemaObject`) — Zod'a çevirip geri üretmek şemayı
 * bozacağı için alt seviye `Server` istek işleyicileri kullanılır.
 */
async function ana() {
  const semalar = semaYukle();
  const srv = new Server({ name: "claude-design", version: "0.1.0" }, { capabilities: { tools: {} } });

  srv.setRequestHandler(ListToolsRequestSchema, () => ({
    tools: semalar.map((s) => ({
      name: kisaAd(s.name), description: s.description, inputSchema: s.input_schema,
    })),
  }));

  srv.setRequestHandler(CallToolRequestSchema, async (istek) => {
    const tamAd = ONEK + istek.params.name;
    if (!semalar.some((s) => s.name === tamAd)) {
      return { content: [{ type: "text", text: "bilinmeyen araç: " + istek.params.name }], isError: true };
    }
    const r = await aktar(tamAd, istek.params.arguments || {});
    if (r.hata) return { content: [{ type: "text", text: "HATA: " + r.hata }], isError: true };
    return { content: [{ type: "text", text: await ciktiHazirla(r.metin, 30000) }] };
  });

  await srv.connect(new StdioServerTransport());
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  await ana();
}
