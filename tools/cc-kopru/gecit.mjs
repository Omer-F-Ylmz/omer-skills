#!/usr/bin/env node
/**
 * cc-kopru · kanca geçidi (KURULUM-11k K5).
 * Desktop ↔ geçit ↔ gerçek MCP sunucusu. Satır tabanlı JSON-RPC proxy: `tools/call`
 * yakalanır, CC aracına eşlenir, CC'nin kendi PreToolUse/PostToolUse hook'ları ve
 * ~/.claude/settings.json permissions.deny kuralları uygulanır. Eşlenmeyen her
 * mesaj ham satır olarak iletilir. stdout yalnız JSON-RPC; günlük stderr'e.
 *
 * Kullanım: node gecit.mjs <ad> -- <gerçek sunucu komutu> [args...]
 */
import { spawn } from "node:child_process";
import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import readline from "node:readline";

import { ayarYukle, denyListesi, gozlemGovde, gozlemYaz, okumaDeny,
         sizintiKapisi } from "./kos.mjs";
import { hookKaynaklari, hookKos, hookTanimlari, izDosyasi } from "./hook.mjs";

const AYAR = ayarYukle();
const OTURUM = crypto.randomUUID();
const IZ = izDosyasi(OTURUM);
const DENY = denyListesi();

/**
 * Yazan git araçları komut satırına çevrilir; hook'lar (block-destructive gibi)
 * `tool_input.command`a bakıyor. Salt okur git araçları (status/log/diff/show)
 * eşlenmez — CC'de de Bash değiller, geçit onlara dokunmaz.
 */
const GIT_KOMUT = {
  git_commit: (a) => `git commit -m ${JSON.stringify(String(a.message ?? ""))}`,
  git_add: (a) => `git add ${(a.files || ["."]).join(" ")}`,
  git_reset: (a) => `git reset${a.mode ? " --" + a.mode : ""}${a.hard ? " --hard" : ""}`,
  git_checkout: (a) => `git checkout ${a.branch_name ?? ""}`.trim(),
  git_create_branch: (a) => `git checkout -b ${a.branch_name ?? ""}`.trim(),
  git_init: (a) => `git init ${a.repo_path ?? ""}`.trim(),
};

/** Desktop MCP aracı → CC aracı. Eşlenmeyen araç için null. */
export function ccArac(ad, args = {}) {
  const git = GIT_KOMUT[ad];
  if (git) {
    return {
      matcher: "Bash", okunan: [], yol: args.repo_path,
      girdi: { command: git(args), description: "cc-kopru geçidi" },
    };
  }
  switch (ad) {
    case "read_file": case "read_text_file": case "read_media_file":
      return { matcher: "Read", okunan: [args.path], yol: args.path,
               girdi: { file_path: args.path } };
    case "read_multiple_files":
      return { matcher: "Read", okunan: args.paths || [], yol: (args.paths || [])[0],
               girdi: { file_path: (args.paths || []).join(", ") } };
    case "edit_file":
      return { matcher: "Edit", okunan: [], yol: args.path,
               girdi: { file_path: args.path } };
    case "write_file": case "create_directory":
      return { matcher: "Write", okunan: [], yol: args.path,
               girdi: { file_path: args.path, content: args.content } };
    case "move_file":
      return { matcher: "Write", okunan: [], yol: args.destination,
               girdi: { file_path: args.destination, content: `move from ${args.source}` } };
    default:
      return null;
  }
}

/** `./bin/**` gibi proje göreli deny kalıpları için: en yakın .git/.claude atası. */
export function projeKoku(hedef) {
  let d = path.resolve(hedef || process.cwd());
  if (fs.existsSync(d) && !fs.statSync(d).isDirectory()) d = path.dirname(d);
  for (let ust = d; ; ust = path.dirname(ust)) {
    if (fs.existsSync(path.join(ust, ".git")) || fs.existsSync(path.join(ust, ".claude"))) {
      return ust;
    }
    if (path.dirname(ust) === ust) return d;
  }
}

/** Sureci ayaga kaldirir. Modul ice aktarildiginda kosmaz: ccArac/projeKoku saf.
 */
function baslat() {
  // ------------------------------------------------------------------ süreç
  const ayirici = process.argv.indexOf("--");
  const AD = process.argv[2] && process.argv[2] !== "--" ? process.argv[2] : "gecit";
  const KOMUT = ayirici >= 0 ? process.argv.slice(ayirici + 1) : [];
  if (!KOMUT.length) {
    process.stderr.write("kullanim: gecit.mjs <ad> -- <komut> [args...]\n");
    process.exit(2);
  }

  const alt = spawn(KOMUT[0], KOMUT.slice(1),
                    { stdio: ["pipe", "pipe", "inherit"], shell: false, windowsHide: true });
  alt.on("error", (e) => { process.stderr.write(`[gecit] sunucu baslamadi: ${e}\n`); process.exit(1); });
  alt.on("close", (k) => process.exit(k ?? 0));

  const gunluk = (s) => process.stderr.write(`[gecit:${AD}] ${s}\n`);
  const yaz = (o) => process.stdout.write(JSON.stringify(o) + "\n");
  // Alt sunucu kapanmışsa yazım EPIPE atar; geçit onunla birlikte düşmesin.
  alt.stdin.on("error", () => { /* kapanış `close` dalında ele alınır */ });
  const ilet = (satir) => alt.stdin.write(satir + "\n");
  const redCevap = (id, sebep) =>
    yaz({ jsonrpc: "2.0", id, result: { content: [{ type: "text", text: sebep }], isError: true } });

  const bekleyen = new Map();

  /**
   * Çağrı claude-mem'e K3(b) yolundan girer. Read yanıtının GÖVDESİ yazılmaz:
   * dosya içeriği gitleaks'ten geçmeden gözleme düşmesin, ve her okumada gitleaks
   * koşması geçidi kullanılamaz hale getirirdi.
   * ponytail: içerik gözlemi gerekirse aynı kapı (sizintiKapisi) okuma yoluna da açılır.
   */
  async function gozle(aracAdi, girdi, yanit, proje) {
    const sizinti = await sizintiKapisi(`cc-kopru gecit ${aracAdi}`,
                                        JSON.stringify(girdi).slice(0, 20000), AYAR);
    if (sizinti) return gunluk(`gozlem yazilmadi: ${sizinti}`);
    const not = await gozlemYaz(gozlemGovde(OTURUM, aracAdi, girdi, yanit, proje));
    if (not) gunluk(not);
  }

  function ortak(proje) {
    return { session_id: OTURUM, transcript_path: IZ, cwd: proje };
  }

  async function cagriyiIsle(m, satir) {
    const ad = m.params?.name;
    const args = m.params?.arguments || {};
    const es = ccArac(ad, args);
    if (!es) return ilet(satir);

    const proje = projeKoku(es.yol);
    try {
      for (const y of es.okunan) okumaDeny(y, DENY, proje);
    } catch (e) {
      gunluk(`${ad} -> ${es.matcher} · RED · ${e.message}`);
      await gozle(`cc-kopru:gecit:${ad}`, args, { red: e.message }, proje);
      return redCevap(m.id, "RED: " + e.message);
    }

    const defs = hookTanimlari(hookKaynaklari(proje), AYAR.kapaliHooklar || []);
    const on = await hookKos(defs, {
      ...ortak(proje), hook_event_name: "PreToolUse",
      tool_name: es.matcher, tool_input: es.girdi,
    }, { projeDir: proje });

    if (on.karar === "red") {
      gunluk(`${ad} -> ${es.matcher} · RED · hooks: ${on.kosan.join(",")}`);
      await gozle(`cc-kopru:gecit:${ad}`, args, { red: on.sebep }, proje);
      return redCevap(m.id, "HOOK REDDETTİ: " + on.sebep);
    }

    gunluk(`${ad} -> ${es.matcher} · izin · hooks: ${on.kosan.join(",")}`);
    bekleyen.set(m.id, { ad, args, es, proje, defs });
    ilet(satir);
  }

  readline.createInterface({ input: process.stdin }).on("line", (satir) => {
    if (!satir.trim()) return;
    let m;
    try { m = JSON.parse(satir); } catch { return ilet(satir); }
    if (m.method !== "tools/call" || m.id === undefined) return ilet(satir);
    cagriyiIsle(m, satir).catch((e) => {
      gunluk("gecit hatasi: " + e);
      redCevap(m.id, "RED: gecit hatasi: " + e.message);
    });
  });

  readline.createInterface({ input: alt.stdout }).on("line", async (satir) => {
    if (!satir.trim()) return;
    let m;
    try { m = JSON.parse(satir); } catch { return process.stdout.write(satir + "\n"); }
    const b = m.id === undefined ? null : bekleyen.get(m.id);
    if (!b) return process.stdout.write(satir + "\n");
    bekleyen.delete(m.id);

    const yanit = b.es.matcher === "Read" ? { ok: !m.error } : (m.result ?? m.error);
    const son = await hookKos(b.defs, {
      ...ortak(b.proje), hook_event_name: "PostToolUse",
      tool_name: b.es.matcher, tool_input: b.es.girdi, tool_response: yanit,
    }, { projeDir: b.proje });
    gunluk(`${b.ad} · PostToolUse hooks: ${son.kosan.join(",")}`);
    await gozle(`cc-kopru:gecit:${b.ad}`, b.args, yanit, b.proje);
    process.stdout.write(satir + "\n");
  });
}

if (import.meta.main) baslat();
