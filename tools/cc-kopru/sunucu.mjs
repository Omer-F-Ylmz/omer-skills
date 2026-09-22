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

import { MEM_KOK, ajanAlanDenetle, ayarYukle, ciktiHazirla, cwdCoz, denyListesi, gozlemGovde,
         gozlemYaz, komutDenetle,
         komutSatiri, kos, memGovde, redakte, sizintiKapisi, statuslineGovde,
         yenidenYazimKabul, yerelGun, yolBul } from "./kos.mjs";
import { ARALIK_TAVAN, logKoku, oku } from "./oku.mjs";
import { hookKaynaklari, hookKos, hookTanimlari, izDosyasi, katalogTopla } from "./hook.mjs";
import os from "node:os";

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
/** Son `ajan` çağrısının kullanım sayıları — `durum` statusline'ı bununla besler. */
let sonAjan = null;

/**
 * Köprünün her çağrısı CC'nin PostToolUse hook'uyla aynı uçtan claude-mem'e girer.
 * gitleaks kapısından geçmeyen metin yazılmaz. Hata çağrıyı bozmaz, nota düşer.
 */
async function gozle(aracAdi, girdi, yanit, cwd) {
  const metinGovde = JSON.stringify({ girdi, yanit }).slice(0, 20000);
  const sizinti = await sizintiKapisi(`cc-kopru ${aracAdi}`, metinGovde, AYAR);
  if (sizinti) return `[gözlem yazılmadı] ${sizinti}`;
  return await gozlemYaz(gozlemGovde(OTURUM, aracAdi, girdi, yanit, cwd));
}

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
    ham: z.boolean().default(false)
      .describe("Headroom çıktı katmanını atlar; çıktı yalnız tavanda kırpılır (11m-A K4)"),
  },
}, ({ arac, args, cwd, timeout_sn, ham }) => sirala(async () => {
  let proje;
  try {
    proje = cwdCoz(cwd, AYAR);
    // 11l-FIX K1: denetimden ÇIKAN argv kullanılır. Denetimin eklediği `--` ayırıcısı
    // (11l K2) hook satırına girmezse, hook `rtk <ayırıcısız argv>` yazıyor ve sarmalama
    // normalleşmeyi geri alıyordu (`npx --no pixeljury --version` -> npm'in sürümü).
    args = komutDenetle(arac, args, AYAR).args;
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

  const not = await gozle("cc-kopru:komut", { command: komutSatiri(cArac, cArgs) },
                          { stdout: r.cikti, exitCode: r.kod }, proje);

  const bas = `${yazildi}${on.ekBaglam ? on.ekBaglam + "\n" : ""}${not ? not + "\n" : ""}`
    + `exit ${r.kod}${r.sureDoldu ? " (zaman aşımı)" : ""}\n`;
  // tam çıktı zaten kos()'un yazdığı log dosyasında; katman yeni dosya açmaz.
  const govde = bas + await ciktiHazirla(r.cikti, AYAR.ciktiTavan ?? 30000, { ham, log: r.log });
  return r.kod === 0 ? metin(govde) : hata(govde);
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
  const govde = await ciktiHazirla(redakte(j.result || ""), AYAR.ciktiTavan ?? 30000);
  sonAjan = { model: Object.keys(j.modelUsage || {})[0] || model, girdi, okunan };
  const not = await gozle("cc-kopru:ajan", { gorev: a.gorev, model, cwd: proje },
                          { result: govde, session_id: j.session_id }, proje);
  return metin(`${govde}\n\nsession_id: ${j.session_id}\n${durum}${not ? "\n" + not : ""}`);
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
  const govde = await ciktiHazirla(redakte(parcalar.join("\n\n")), AYAR.oturumTavan ?? 12000);
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
  const sizinti = await sizintiKapisi(baslik, govde, AYAR);
  if (sizinti) return hata(sizinti);

  const y = await fetch(`${MEM_KOK}/api/memory/save`, {
    method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify(memGovde(proje, baslik, govde)),
  });
  const c = await y.text();
  return y.ok ? metin("kaydedildi: " + c) : hata(`worker ${y.status}: ${c}`);
}));

// ---------------------------------------------------------------- katalog
srv.registerTool("katalog", {
  title: "CC komut · ajan · skill kataloğu",
  description: "Claude Code'da açık plugin komutlarını, agent'ları ve skill adlarını "
    + "listeler (ad + tek satır). skillOverrides'ta kapatılanlar elenir.",
  inputSchema: {
    tur: z.enum(["hepsi", "komut", "ajan", "skill"]).default("hepsi"),
    ara: z.string().default("").describe("Ada göre süzgeç (alt dize)"),
    sayi: z.boolean().default(false)
      .describe("Yalnız tür başına sayı döner, liste basılmaz (11l K3)"),
  },
}, ({ tur, ara, sayi }) => sirala(async () => {
  const liste = katalogTopla(tur, ara);
  if (sayi) {
    const s = { komut: 0, ajan: 0, skill: 0 };
    for (const x of liste) s[x.tur] += 1;
    return metin(`komut ${s.komut} · ajan ${s.ajan} · skill ${s.skill}`
      + ` · toplam ${liste.length}${ara ? ` (ara=${ara})` : ""}`);
  }
  if (!liste.length) return metin("(eşleşme yok)");
  const satirlar = liste.map((x) => `- [${x.tur}] ${x.ad}${x.aciklama ? " — " + x.aciklama : ""}`);
  const bas = `${liste.length} kayıt (tür=${tur}${ara ? `, ara=${ara}` : ""})\n`;
  const govde = await ciktiHazirla(bas + satirlar.join("\n"), AYAR.ciktiTavan ?? 30000);
  return metin(govde);
}));

// ---------------------------------------------------------------- oku
srv.registerTool("oku", {
  title: "Dosya iskeleti · sembol · satır aralığı",
  description: "Kaynak dosyayı tam okumadan gösterir: iskelet = semboller + satırları, "
    + "sembol = yalnız o sembolün gövdesi, aralik = satır aralığı (graf gerekmez). "
    + "Kaynak projenin graphify-out/graph.json'u; Read deny kuralları önce uygulanır.",
  inputSchema: {
    proje_yolu: z.string().describe("Proje kökü (yalnız izinli kökler altında)"),
    dosya: z.string().describe("Köke göreli dosya yolu"),
    mod: z.enum(["iskelet", "sembol", "aralik"]).default("iskelet"),
    ad: z.string().optional().describe("mod=sembol için sembol adı"),
    bas: z.number().int().min(1).optional().describe("mod=aralik başlangıç satırı"),
    bit: z.number().int().min(1).optional().describe(`mod=aralik bitiş satırı (tavan ${ARALIK_TAVAN} satır)`),
  },
}, ({ proje_yolu, dosya, mod, ad, bas, bit }) => sirala(async () => {
  // Köprünün kendi log dizini salt-okuma kök: graf yok, yalnız satır aralığı (K3).
  let kok = logKoku(proje_yolu);
  if (kok && mod !== "aralik") return hata("RED: log dizini yalnız mod=aralik ile okunur");
  if (!kok) {
    try { kok = cwdCoz(proje_yolu, AYAR); } catch (e) { return hata("RED: " + e.message); }
  }
  try {
    const govde = oku({ kok, mod, dosya, ad, bas, bit, deny: AYAR.denyListesi || denyListesi() });
    return metin(await ciktiHazirla(govde, AYAR.ciktiTavan ?? 30000));
  } catch (e) { return hata("RED: " + e.message); }
}));

// ---------------------------------------------------------------- durum
/** Bugün değişmiş CC transcript'lerinden token toplamı.
 *  ponytail: dosyalar baştan sona okunur; günlük hacim büyürse mtime+offset takibi gerekir. */
function gunlukCC() {
  const kok = path.join(os.homedir(), ".claude", "projects");
  const bugun = yerelGun();
  let girdi = 0, cikti = 0, dosya = 0;
  const yuru = (d) => {
    for (const f of fs.readdirSync(d, { withFileTypes: true })) {
      const p = path.join(d, f.name);
      if (f.isDirectory()) { yuru(p); continue; }
      if (!f.name.endsWith(".jsonl")) continue;
      if (yerelGun(fs.statSync(p).mtime) !== bugun) continue;
      dosya += 1;
      for (const satir of fs.readFileSync(p, "utf8").split("\n")) {
        if (!satir.includes('"usage"')) continue;
        try {
          const u = JSON.parse(satir).message?.usage;
          if (!u) continue;
          girdi += (u.input_tokens || 0) + (u.cache_read_input_tokens || 0)
                 + (u.cache_creation_input_tokens || 0);
          cikti += u.output_tokens || 0;
        } catch { /* yarım satır */ }
      }
    }
  };
  try { yuru(kok); } catch { /* dizin yoksa 0 */ }
  return { girdi, cikti, dosya };
}

async function jsonAl(url) {
  try {
    const y = await fetch(url, { signal: AbortSignal.timeout(6000) });
    return y.ok ? await y.json() : { hata: `HTTP ${y.status}` };
  } catch (e) { return { hata: String(e?.message || e) }; }
}

srv.registerTool("durum", {
  title: "Köprü durum satırı",
  description: "CC statusline'ını son ajan oturumunun kullanımıyla besler; Headroom, "
    + "claude-mem worker/kota ve günlük CC token toplamını ekler.",
  inputSchema: {},
}, () => sirala(async () => {
  const parcalar = [];

  const g = statuslineGovde(sonAjan);
  if (!g) {
    parcalar.push("## statusline\n(bu oturumda ajan çağrısı yok — statusline'ı besleyecek "
      + "kullanım verisi yok; uydurma yüzde basılmaz)");
  } else {
    const ps1 = path.join(os.homedir(), ".claude", "statusline.ps1");
    const satir = await new Promise((coz) => {
      const p = spawn("powershell", ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps1],
                      { shell: false, windowsHide: true });
      const o = [];
      p.stdout.on("data", (b) => o.push(b));
      p.on("error", (e) => coz("(statusline koşmadı: " + e.message + ")"));
      p.on("close", () => coz(Buffer.concat(o).toString("utf8").trim()));
      p.stdin.end(JSON.stringify(g));
    });
    parcalar.push("## statusline\n" + satir);
  }

  const hr = await jsonAl("http://127.0.0.1:6767/stats");
  parcalar.push("## headroom\n" + (hr.hata ? "erişilemedi: " + hr.hata
    : `istek ${hr.summary?.api_requests} · sıkıştırılan ${hr.summary?.compression?.requests_compressed}`
      + ` · kazanç %${hr.summary?.cost?.savings_pct} ($${hr.summary?.cost?.total_saved_usd})`));

  const [sag, kuyruk] = await Promise.all([
    jsonAl(`${MEM_KOK}/api/health`), jsonAl(`${MEM_KOK}/api/processing-status`),
  ]);
  parcalar.push("## claude-mem\n" + (sag.hata ? "worker erişilemedi: " + sag.hata
    : `worker ${sag.status} v${sag.version} · sağlayıcı ${sag.ai?.provider}`
      + ` · kuyruk ${kuyruk.queueDepth ?? "?"} · park ${kuyruk.parkedSessions ?? "?"}`));

  const c = gunlukCC();
  parcalar.push(`## günlük CC (${yerelGun()})\n`
    + `${c.dosya} transcript · girdi ${c.girdi} · çıktı ${c.cikti} token`);

  parcalar.push("## yapısal sınır\nDesktop sohbetinin kendi ctx %'si ölçülemiyor: "
    + "statusline.ps1'in beklediği context_window.used_percentage'ı Desktop hiçbir "
    + "yerel kaynağa yazmıyor. Yukarıdaki yüzde son `ajan` alt oturumunundur.");

  const govde = await ciktiHazirla(parcalar.join("\n\n"), AYAR.ciktiTavan ?? 30000);
  return metin(govde);
}));

// ---------------------------------------------------------------- oturum_ozeti
srv.registerTool("oturum_ozeti", {
  title: "claude-mem oturum özeti",
  description: "CC'nin Stop hook'uyla aynı uçtan (/api/sessions/summarize) özet "
    + "kuyruklar ve projenin mevcut özetlerini döner.",
  inputSchema: { proje: z.string() },
}, ({ proje }) => sirala(async () => {
  let kuyruklandi = "";
  try {
    const y = await fetch(`${MEM_KOK}/api/sessions/summarize`, {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ contentSessionId: OTURUM, platformSource: "claude-desktop" }),
      signal: AbortSignal.timeout(8000),
    });
    kuyruklandi = `${y.status} ${(await y.text()).slice(0, 200)}`;
  } catch (e) { kuyruklandi = "istek başarısız: " + String(e?.message || e); }

  const kuyruk = await jsonAl(`${MEM_KOK}/api/processing-status`);
  const ozetler = await jsonAl(`${MEM_KOK}/api/summaries`);
  const liste = Array.isArray(ozetler) ? ozetler : (ozetler.summaries || []);
  const secili = liste
    .filter((s) => !proje || String(s.project || "").includes(path.basename(proje)))
    .slice(-5)
    .map((s) => `- ${s.created_at || s.createdAt || "?"} · ${String(s.text || s.summary || "")
      .replace(/\s+/g, " ").slice(0, 300)}`);

  const govde = [
    `## özet isteği\n${kuyruklandi}`,
    `## kuyruk\nderinlik ${kuyruk.queueDepth ?? "?"} · park ${kuyruk.parkedSessions ?? "?"}`
      + ` · işliyor ${kuyruk.isProcessing ?? "?"}`,
    `## mevcut özetler (son 5)\n${secili.join("\n") || "(yok)"}`,
    "Not: özetleme asenkron bir LLM işi; sağlayıcı kotası doluyken kuyrukta bekler.",
  ].join("\n\n");
  const kirpik = await ciktiHazirla(redakte(govde), AYAR.oturumTavan ?? 12000);
  return metin(kirpik);
}));

await srv.connect(new StdioServerTransport());
