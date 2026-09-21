#!/usr/bin/env node
/**
 * cc-kopru · Claude Code katmanını Desktop sohbetine açan yerel stdio MCP sunucusu.
 * KURULUM-11i. 4 araç: komut · ajan · oturum · kaydet.
 * stdout JSON-RPC kanalıdır; sunucu dışında tek bayt basılmaz (tanılama stderr'e).
 */
import { spawn, spawnSync } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

import { ajanAlanDenetle, ayarYukle, cwdCoz, gitleaksOzet, komutDenetle, komutSatiri, kirp, kos,
         memGovde, redakte, yenidenYazimKabul, yolBul } from "./kos.mjs";
import { hookKaynaklari, hookKos, hookTanimlari, izDosyasi } from "./hook.mjs";

const AYAR = ayarYukle();
const CLAUDE = AYAR.claudeYolu || yolBul("claude");
// claude bir betik olarak kuruluysa (node <js>) yurutucuden once gelen argumanlar
const CLAUDE_ON = AYAR.claudeOnArgs || [];
/** hafif modun bayrakları gerçekten var mı — `claude --help` bir kez okunur. */
const HAFIF_VAR = (() => {
  if (AYAR.claudeOnArgs?.length) return true;   // test/sahte yürütücü
  const r = spawnSync(CLAUDE, ["--help"], { encoding: "utf8", windowsHide: true });
  const h = r.stdout || "";
  return ["--disable-slash-commands", "--strict-mcp-config", "--mcp-config"]
    .every((b) => h.includes(b));
})();
if (!CLAUDE) throw new Error("claude yurutucusu bulunamadi; kopru.json claudeYolu yazin");
const OTURUM = crypto.randomUUID();
const IZ = izDosyasi(OTURUM);
let ajanSayaci = 0;

/** Aynı anda tek süreç: bütün koşular tek kuyruktan geçer. */
let kuyruk = Promise.resolve();
const sirala = (is) => (kuyruk = kuyruk.then(is, is));

const metin = (s) => ({ content: [{ type: "text", text: String(s) }] });
const hata = (s) => ({ content: [{ type: "text", text: String(s) }], isError: true });

function tanimlar(projeDir) {
  return hookTanimlari(hookKaynaklari(projeDir), AYAR.kapaliHooklar || []);
}

const ortak = (projeDir) => ({
  session_id: OTURUM, transcript_path: IZ, cwd: projeDir,
});

const srv = new McpServer({ name: "cc-kopru", version: "0.1.0" });

// ---------------------------------------------------------------- komut
srv.registerTool("komut", {
  title: "CC allowlist komutu",
  description: "Claude Code'un PATH araçlarından birini, CC'nin kendi PreToolUse/PostToolUse "
    + "hook'ları uygulanarak koşar. Allowlist dışı araç ve yasak alt komut reddedilir.",
  inputSchema: {
    arac: z.enum(Object.keys(AYAR.izinli)).describe("Allowlist'teki araç adı"),
    args: z.array(z.string()).default([]).describe("Argümanlar; kabuk yok, metakarakter yasak"),
    cwd: z.string().describe("Çalışma dizini (yalnız izinli kökler altında)"),
    timeout_sn: z.number().int().min(1).max(600).optional().describe("Varsayılan 120, tavan 600"),
  },
}, ({ arac, args, cwd, timeout_sn }) => sirala(async () => {
  let proje;
  try {
    proje = cwdCoz(cwd, AYAR);
    komutDenetle(arac, args, AYAR);
  } catch (e) {
    return hata("RED: " + e.message);
  }

  const defs = tanimlar(proje);
  const on = await hookKos(defs, {
    ...ortak(proje), hook_event_name: "PreToolUse", tool_name: "Bash",
    tool_input: { command: komutSatiri(arac, args), description: "cc-kopru" },
  }, { projeDir: proje });
  if (on.karar === "red") return hata("HOOK REDDETTİ: " + redakte(on.sebep));

  // updatedInput yalnız ["rtk", ...orijinal argv] biçiminde kabul edilir (11i-FIX-2 K3):
  // satırı yeniden jetonlara bölmek argüman sınırını değiştirebiliyordu. Başkası yok sayılır.
  let cArac = arac, cArgs = args, yazildi = "", sarmalandi = false;
  const yeni = on.girdi?.command;
  if (yeni && yeni !== komutSatiri(arac, args)) {
    const sarma = AYAR.izinli.rtk ? yenidenYazimKabul([arac, ...args], yeni) : null;
    if (sarma) {
      [cArac, ...cArgs] = sarma;
      sarmalandi = true;
      yazildi = `[hook yeniden yazdı] ${yeni}\n`;
    } else {
      yazildi = "[hook yeniden yazımı yok sayıldı]\n";
    }
  }

  const r = await kos({ arac: cArac, args: cArgs, cwd: proje, timeoutSn: timeout_sn,
                        ayar: AYAR, denetimAtla: sarmalandi });

  await hookKos(defs, {
    ...ortak(proje), hook_event_name: "PostToolUse", tool_name: "Bash",
    tool_input: { command: komutSatiri(cArac, cArgs) },
    tool_response: { stdout: r.cikti, exitCode: r.kod },
  }, { projeDir: proje });

  const bas = `${yazildi}${on.ekBaglam ? on.ekBaglam + "\n" : ""}exit ${r.kod}${r.sureDoldu ? " (zaman aşımı)" : ""}\n`;
  return r.kod === 0 ? metin(bas + r.cikti) : hata(bas + r.cikti);
}));

// ---------------------------------------------------------------- ajan
srv.registerTool("ajan", {
  title: "Gerçek CC oturumu",
  description: "Görevi `claude -p` ile gerçek bir Claude Code oturumunda koşturur: CC'nin "
    + "izinleri, hook'ları, skill ve plugin'leri geçerlidir. İzin atlama bayrakları yasak.",
  inputSchema: {
    gorev: z.string().min(1),
    cwd: z.string(),
    model: z.string().default("sonnet"),
    ajan_adi: z.string().optional().describe("CC'de tanımlı agent adı (--agent)"),
    max_turns: z.number().int().min(1).max(60).default(20),
    devam_id: z.string().optional().describe("Önceki session_id (--resume)"),
    timeout_sn: z.number().int().min(30).max(3600).default(900),
    hafif: z.boolean().default(false).describe(
      "Skill/slash komut yüklemesini ve MCP sunucularını kapatır; hook'lar ve CLAUDE.md "
      + "açık kalır. Bağlam pahalı, iş basitse aç."),
  },
}, (a) => sirala(async () => {
  // FIX-1: görev metni artık argv'ye girmediği için içeriğine göre elenmez — bayrak
  // adı geçen bir istem yalnızca metindir. Bayrak kaçakçılığı argv tarafında kesilir.
  if (ajanSayaci >= (AYAR.ajanTavan ?? 10)) {
    return hata(`RED: oturum başına ajan çağrı tavanı (${AYAR.ajanTavan ?? 10}) doldu.`);
  }
  let proje, model, ajanAdi, devamId;
  try {
    proje = cwdCoz(a.cwd, AYAR);
    // argv'ye giden her alan dar bir karakter sınıfıyla denetlenir: bayrak kaçakçılığı yok
    model = ajanAlanDenetle("model", a.model);
    ajanAdi = a.ajan_adi ? ajanAlanDenetle("ajan_adi", a.ajan_adi) : null;
    devamId = a.devam_id ? ajanAlanDenetle("devam_id", a.devam_id) : null;
  } catch (e) { return hata("RED: " + e.message); }
  ajanSayaci += 1;

  // --max-turns bayrağı CC CLI'da yok (11i K0-b); bütçe göreve yazılır, dönüşte doğrulanır.
  const gorev = `${a.gorev}\n\n[bütçe] En fazla ${a.max_turns} tur kullan.`;
  // FIX-1: görev metni argv'ye GİRMEZ — bayrağa benzeyen istem bayrak olarak okunabilir.
  // `claude -p` istemi stdin'den alır (aşağıda p.stdin.end(gorev)).
  const argv = ["-p", "--output-format", "json", "--model", model];
  if (ajanAdi) argv.push("--agent", ajanAdi);
  if (devamId) argv.push("--resume", devamId);
  // hafif: yalnız `claude --help`te doğrulanmış bayraklar (11i devam K1). Uydurma bayrak yok.
  // --disable-slash-commands "Disable all skills" · --strict-mcp-config + boş --mcp-config
  // = hiçbir MCP sunucusu. Hook'lar ve CLAUDE.md etkilenmez.
  if (a.hafif) {
    if (!HAFIF_VAR) return hata("RED: hafif mod bayrakları bu claude sürümünde yok.");
    argv.push("--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}');
  }
  // kurulan argv son kez taranır: artık her jeton ya sabit bayrak ya denetlenmiş değer
  if (argv.some((x) => /dangerously-skip-permissions|bypassPermissions|^--permission-mode/i.test(x))) {
    return hata("RED: argv izin atlama bayrağı taşıyor.");
  }

  const cikti = await new Promise((coz) => {
    const p = spawn(CLAUDE, [...CLAUDE_ON, ...argv], { cwd: proje, shell: false, windowsHide: true });
    p.stdin.end(gorev);   // istem stdin'den
    const o = [];
    p.stdout.on("data", (b) => o.push(b));
    p.stderr.on("data", (b) => o.push(b));
    const zam = setTimeout(() => { try { p.kill(); } catch { /* bitti */ } }, a.timeout_sn * 1000);
    p.on("error", (e) => { clearTimeout(zam); coz(String(e)); });
    p.on("close", () => { clearTimeout(zam); coz(Buffer.concat(o).toString("utf8")); });
  });

  let j;
  try { j = JSON.parse(cikti); } catch { return hata("claude -p JSON dönmedi:\n" + redakte(cikti).slice(0, 2000)); }
  const u = j.usage || {};
  const okunan = u.cache_read_input_tokens || 0;
  const girdi = (u.input_tokens || 0) + okunan + (u.cache_creation_input_tokens || 0);
  const durum = [
    `model ${Object.keys(j.modelUsage || {})[0] || model}`,
    `girdi ${girdi}`, `çıktı ${u.output_tokens || 0}`,
    `cache okuma %${girdi ? Math.round((okunan / girdi) * 100) : 0}`,
    `$${(j.total_cost_usd || 0).toFixed(4)}`,
    `${j.num_turns} tur${j.num_turns > a.max_turns ? " (bütçe aşıldı)" : ""}`,
  ].join(" · ");
  const { metin: govde } = kirp(redakte(j.result || ""), AYAR.ciktiTavan ?? 30000);
  return metin(`${govde}\n\nsession_id: ${j.session_id}\n${durum}`);
}));

// ---------------------------------------------------------------- oturum
srv.registerTool("oturum", {
  title: "Proje oturum bağlamı",
  description: "CC'nin SessionStart hook'larını (source=startup) koşar ve proje CLAUDE.md + "
    + "dalga.md ile birlikte döner.",
  inputSchema: { proje_yolu: z.string() },
}, ({ proje_yolu }) => sirala(async () => {
  let proje;
  try { proje = cwdCoz(proje_yolu, AYAR); } catch (e) { return hata("RED: " + e.message); }

  const r = await hookKos(tanimlar(proje), {
    ...ortak(proje), hook_event_name: "SessionStart", source: "startup",
  }, { projeDir: proje });

  const parcalar = [];
  if (r.ekBaglam) parcalar.push("## SessionStart\n" + r.ekBaglam);
  for (const [ad, p] of [["CLAUDE.md", "CLAUDE.md"], ["dalga.md", ".claude/dalga.md"]]) {
    const tam = path.join(proje, p);
    if (fs.existsSync(tam)) parcalar.push(`## ${ad}\n` + fs.readFileSync(tam, "utf8"));
  }
  parcalar.push(`## koşan hook'lar\n${r.kosan.join("\n") || "(yok)"}`);
  const { metin: govde } = kirp(redakte(parcalar.join("\n\n")), AYAR.oturumTavan ?? 12000);
  return metin(govde);
}));

// ---------------------------------------------------------------- kaydet
srv.registerTool("kaydet", {
  title: "claude-mem'e not",
  description: "Metni önce gitleaks'ten geçirir, temizse claude-mem worker'ına 'desktop' "
    + "kaynak etiketiyle yazar. Sızıntı bulunursa yazmaz.",
  inputSchema: {
    proje: z.string(), baslik: z.string(), metin: z.string(),
  },
}, ({ proje, baslik, metin: govde }) => sirala(async () => {
  // gitleaks --source dizin ister ve cwd izinli kök altında olmalı → C:\Projeler altına yazılır
  const gDizin = path.join("C:/Projeler/.tmp-cc-kopru", String(Date.now()));
  fs.mkdirSync(gDizin, { recursive: true });
  const gecici = path.join(gDizin, "not.md");
  fs.writeFileSync(gecici, `# ${baslik}\n\n${govde}\n`, "utf8");
  try {
    // --no-banner --no-color: ret çıktısında banner ve ANSI olmaz. Bulgular JSON rapora
    // yazılır; çıktıya yalnız sayı ve kural adı geçer, değer asla.
    const t = await kos({
      arac: "gitleaks",
      args: ["detect", "--no-git", "--redact", "--no-banner", "--no-color",
             "--report-format", "json", "--report-path", "bulgu.json", "--source", "."],
      cwd: gDizin, ayar: AYAR,
    });
    if (t.kod !== 0) {
      let rapor = null;
      try {
        rapor = JSON.parse(fs.readFileSync(path.join(gDizin, "bulgu.json"), "utf8"));
      } catch { /* rapor yazılamadıysa sayı bilinmez */ }
      return hata(gitleaksOzet(rapor, t.kod));
    }

    const y = await fetch("http://127.0.0.1:37777/api/memory/save", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify(memGovde(proje, baslik, govde)),
    });
    const c = await y.text();
    return y.ok ? metin("kaydedildi: " + c) : hata(`worker ${y.status}: ${c}`);
  } finally {
    fs.rmSync(gDizin, { recursive: true, force: true });
  }
}));

await srv.connect(new StdioServerTransport());
