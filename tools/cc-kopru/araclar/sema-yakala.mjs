#!/usr/bin/env node
/**
 * KURULUM-11l K1b — şema yakalayıcı (tek seferlik).
 *
 * Birebir kaynak: CC'nin API isteğindeki `tools` dizisi. Aktarıcı argv'si aynen
 * `tasarim.mjs`'ten gelir; alt sürecin ortamına yalnız iki değişken eklenir:
 *   ANTHROPIC_BASE_URL=<yerel yakalayıcı>   ENABLE_TOOL_SEARCH=false (araçlar ertelenmesin)
 *
 * İlk /v1/messages gövdesinden yalnız `mcp__claude-design__*` girişleri (name ·
 * description · input_schema) alınır, gövdenin geri kalanı atılır. İstek İLETİLMEZ
 * (503 döner) → API maliyeti 0. İstek başlıkları (authorization · x-api-key ·
 * cookie) okunmaz, hiçbir dosyaya/günlüğe/çıktıya yazılmaz.
 *
 * Kullanım: node tools/cc-kopru/araclar/sema-yakala.mjs
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import http from "node:http";
import os from "node:os";

import { agaciKapat, yolBul } from "../kos.mjs";
import { ONEK, SEMA_DOSYASI, aktariciArgv } from "../tasarim.mjs";

const TIMEOUT_MS = 180000;
let yakalanan = null;

const srv = http.createServer((req, res) => {
  const iletme = () => {
    res.writeHead(503, { "content-type": "application/json" });
    res.end('{"type":"error","error":{"type":"api_error","message":"sema-yakala: iletim yok"}}');
  };
  if (req.method !== "POST" || !req.url.includes("/v1/messages")) {
    req.resume();
    return iletme();
  }
  const parcalar = [];
  req.on("data", (b) => parcalar.push(b));
  req.on("end", () => {
    iletme();
    if (yakalanan) return;
    let govde;
    try { govde = JSON.parse(Buffer.concat(parcalar).toString("utf8")); } catch { return; }
    yakalanan = (govde.tools || [])
      .filter((t) => typeof t?.name === "string" && t.name.startsWith(ONEK))
      .map((t) => ({ name: t.name, description: t.description, input_schema: t.input_schema }));
  });
});

srv.listen(0, "127.0.0.1", () => {
  const port = srv.address().port;
  const claude = yolBul("claude");
  if (!claude) { console.error("DUR: claude PATH'te yok"); process.exit(2); }

  const p = spawn(claude, aktariciArgv(ONEK + "list_projects"), {
    shell: false,
    cwd: os.tmpdir(),
    env: { ...process.env, ANTHROPIC_BASE_URL: `http://127.0.0.1:${port}`, ENABLE_TOOL_SEARCH: "false" },
  });
  p.stdin.end("list_projects aracını boş argümanla çağır.");
  p.stdout.resume();
  p.stderr.resume();

  const bitir = () => {
    agaciKapat(p.pid); p.kill(); srv.close();
    if (!yakalanan) { console.error("DUR: /v1/messages isteği gelmedi, tools dizisi yakalanmadı"); process.exit(2); }
    fs.writeFileSync(SEMA_DOSYASI, JSON.stringify(yakalanan, null, 2) + "\n", "utf8");
    console.log(`yakalanan giriş: ${yakalanan.length} → ${SEMA_DOSYASI}`);
    for (const t of yakalanan) console.log("  " + t.name);
    if (yakalanan.length !== 23) {
      console.error(`DUR: 23 giriş beklendi, ${yakalanan.length} geldi`);
      process.exit(2);
    }
    process.exit(0);
  };

  const zam = setTimeout(bitir, TIMEOUT_MS);
  const bekle = setInterval(() => { if (yakalanan) { clearTimeout(zam); clearInterval(bekle); bitir(); } }, 200);
  p.on("close", () => { clearTimeout(zam); clearInterval(bekle); bitir(); });
});
