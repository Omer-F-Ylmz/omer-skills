/**
 * cc-kopru · koşucu katmanı (KURULUM-11i K1).
 * Allowlist · cwd denetimi · redaksiyon · timeout + süreç ağacı · çıktı tavanı.
 * shell:false; .cmd shim'inde gerçek hedef çözülür, çözülemezse denetimli `cmd /c`.
 */
import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const BURASI = path.dirname(fileURLToPath(import.meta.url));
export const LOG_DIZIN = path.join(os.tmpdir(), "cc-kopru");

/** altIzin/altYasak tanımlanmamış araçlarda uygulanan ağ. */
const YASAK_FIIL = new Set([
  "install", "uninstall", "update", "upgrade", "self-update",
  "wrap", "unwrap", "proxy", "run", "pipe", "exec", "serve", "deploy", "init",
  "login", "logout", "auth", "publish", "recover",
]);

/** Argümanda hiçbir koşulda kabul edilmeyen kabuk metakarakterleri.
 *  `;` ve satır sonu de komut ayırıcıdır: `log -1;whoami` tek argüman gibi görünür. */
const METAKARAKTER = /[&|<>^`;\r\n]/;
/** `cmd /c` yoluna düşüldüğünde ek olarak reddedilenler. */
const CMD_EK = /[%"!]/;

export function ayarYukle(yol) {
  const p = yol || process.env.CC_KOPRU_AYAR || path.join(BURASI, "kopru.json");
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

/** Aynı sürücü/dizin ağacında mı — Windows'ta büyük/küçük harf duyarsız. */
function altinda(yol, kok) {
  const a = path.resolve(yol).toLowerCase();
  const b = path.resolve(kok).toLowerCase();
  return a === b || a.startsWith(b + path.sep);
}

export function cwdCoz(cwd, ayar) {
  if (!cwd) throw new Error("cwd zorunlu");
  let p = path.resolve(cwd);
  if (!fs.existsSync(p)) throw new Error("cwd yok: " + p);
  // sembolik bağ ve .. birlikte çözülür, denetim çözülmüş yol üstünde yapılır
  p = fs.realpathSync.native(p);
  if (!ayar.cwdKokleri.some((k) => altinda(p, k))) {
    throw new Error("cwd izinli köklerin dışında: " + p);
  }
  return p;
}

const yolOnbellek = new Map();
export function yolBul(arac) {
  if (yolOnbellek.has(arac)) return yolOnbellek.get(arac);
  const r = spawnSync(process.platform === "win32" ? "where" : "which", [arac],
                      { encoding: "utf8" });
  const satirlar = (r.stdout || "").split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  // `where npm` ONCE uzantisiz POSIX shim'ini donduruyor; onu kabuksuz spawn etmek
  // ENOENT veriyor (11k K1). Yurutulebilir uzantisi olan aday once gelir.
  const ilk = satirlar.find((s) => /\.(exe|cmd|bat|com)$/i.test(s)) || satirlar[0] || null;
  yolOnbellek.set(arac, ilk);
  return ilk;
}

/**
 * Konum argumanlari: bayraklar ve (tirnaksiz) bayrak degerleri atilir.
 * `python -m pytest` -> [] (pytest, -m'in degeri), `gh repo delete` -> [repo, delete].
 * altIzin denetimi bilerek args[0] uzerinde kalir: alt komut bayragin arkasina gizlenemez.
 */
export function konumlar(args) {
  const out = [];
  for (let i = 0; i < args.length; i += 1) {
    const a = args[i];
    if (a.startsWith("-")) {
      if (!a.includes("=")) i += 1;   // bir sonraki jeton bu bayragin degeri sayilir
      continue;
    }
    out.push(a);
  }
  return out;
}

/**
 * Bayrak tek jetonda degeriyle kaynasmis da olabilir: `-c print(1)` ve `-cprint(1)`
 * ikisi de python icin gecerli. Kisa bayrakta (tek tireli, tek harf) onek eslesmesi
 * yapilir; uzun bayrakta `=` ya da bosluk aranir.
 */
const bayrakVar = (args, bayrak) => args.some((a) =>
  a === bayrak || a.startsWith(bayrak + "=") || a.startsWith(bayrak + " ")
  || (/^-[^-]$/.test(bayrak) && a.startsWith(bayrak)));

/** `gh api` yalniz okuma: metot yok ya da GET, alan yazimi yok. */
function ghApiDenetle(args) {
  const i = args.findIndex((a) => a === "-X" || a === "--method" || a.startsWith("--method="));
  if (i >= 0) {
    const deger = args[i].includes("=") ? args[i].split("=")[1] : args[i + 1];
    if (String(deger).toUpperCase() !== "GET") {
      throw new Error(`gh api yalniz okuma: metot ${deger} reddedildi`);
    }
  }
  for (const b of ["-f", "-F", "--field", "--raw-field"]) {
    if (bayrakVar(args, b)) throw new Error(`gh api yalniz okuma: ${b} alan yazimi reddedildi`);
  }
}

/**
 * ~/.claude/settings.json permissions.deny kurallari koprude de uygulanir.
 * Yalniz `Bash(...)` (ve ciplak `Bash`) girdileri komut yuzeyine bakar; `Read(...)`
 * kurallarinin karsiligi K5 kanca gecidindedir.
 */
export function denyDenetle(satir, denyListesi = []) {
  for (const kural of denyListesi) {
    const m = /^Bash(?:\((.*)\))?$/.exec(String(kural).trim());
    if (!m) continue;
    const kalip = m[1];
    if (kalip === undefined || kalip === "*") throw new Error(`permissions.deny: ${kural}`);
    const re = new RegExp("^" + kalip.split("*").map(kacir).join(".*") + "$");
    if (re.test(satir)) throw new Error(`permissions.deny: ${kural}`);
  }
}

const kacir = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/**
 * CC yol kalıbı → regex. `**` dizin sınırını aşar, `*` tek segmentte kalır.
 * Karşılaştırma küçük harfte: Windows yolları büyük/küçük harf duyarsız.
 */
function yolRe(kalip) {
  const govde = kalip.toLowerCase().split("**")
    .map((par) => par.split("*").map(kacir).join("[^/]*")).join(".*");
  return new RegExp("^" + govde + "$");
}

/**
 * permissions.deny'ın `Read(...)` kuralları — asıl karşılığı K5 kanca geçidinde.
 * `./x` proje köküne, çıplak ad her dizine (`**\/x`), `**` ile başlayan kalıp
 * mutlak yola uygulanır.
 */
export function okumaDeny(dosyaYolu, denyListesi = [], projeDir = "") {
  const yol = path.resolve(dosyaYolu).replace(/\\/g, "/").toLowerCase();
  for (const kural of denyListesi) {
    const m = /^Read(?:\((.*)\))?$/.exec(String(kural).trim());
    if (!m) continue;
    let kalip = m[1];
    if (kalip === undefined || kalip === "*") throw new Error(`permissions.deny: ${kural}`);
    kalip = kalip.replace(/\\/g, "/");
    if (kalip.startsWith("./")) {
      kalip = path.resolve(projeDir || ".", kalip.slice(2)).replace(/\\/g, "/");
    } else if (!/^([a-z]:|\/|\*)/i.test(kalip)) {
      kalip = "**/" + kalip;
    }
    if (yolRe(kalip).test(yol)) throw new Error(`permissions.deny: ${kural}`);
  }
}

/** Kullanici ayarlarindaki deny listesi; okunamazsa bos. */
export function denyListesi() {
  try {
    const p = path.join(os.homedir(), ".claude", "settings.json");
    return JSON.parse(fs.readFileSync(p, "utf8")).permissions?.deny || [];
  } catch { return []; }
}

/** npm/winget .cmd shim'inden gerçek `node <js>` hedefini çıkarır. */
function shimCoz(cmdYolu) {
  let metin;
  try { metin = fs.readFileSync(cmdYolu, "utf8"); } catch { return null; }
  const m = metin.match(/"%_prog%"\s+"%dp0%\\([^"]+)"|node\s+"%~dp0\\([^"]+)"/i);
  const rel = m && (m[1] || m[2]);
  if (!rel) return null;
  const hedef = path.resolve(path.dirname(cmdYolu), rel.replace(/\\/g, path.sep));
  return fs.existsSync(hedef) ? { komut: process.execPath, on: [hedef] } : null;
}

/**
 * Yürütücüye komut/dosya yolu enjekte eden seçenekler. `git -c core.pager=calc.exe log`
 * allowlist'ten geçen bir alt komutun arkasına kod saklar — hepsi koşulsuz reddedilir.
 */
const TEHLIKELI_SECENEK =
  /^--?(c|C|config|config-env|exec-path|git-dir|work-tree|namespace|upload-pack|receive-pack|ssh-command|pager|[\w-]*-command)(=|$)/i;

/** Tek başına verilebilen zararsız bilgi bayrakları. */
const BILGI_BAYRAGI = /^--?(version|help|v|h)$/i;

export function komutDenetle(arac, args, ayar, cwd) {
  const kural = ayar.izinli[arac];
  if (!kural) throw new Error(`'${arac}' allowlist'te değil`);
  if (kural.kos === false) throw new Error(`'${arac}' koşmaz: ${kural.sebep}`);

  for (const a of args) {
    if (METAKARAKTER.test(a)) throw new Error(`argümanda metakarakter: ${a}`);
    if (TEHLIKELI_SECENEK.test(a)) throw new Error(`yürütücüye komut geçiren secenek: ${a}`);
  }

  denyDenetle(komutSatiri(arac, args), ayar.denyListesi || denyListesi());

  const bilgi = args.length === 1 && BILGI_BAYRAGI.test(args[0]);

  for (const b of kural.yasakBayrak || []) {
    if (bayrakVar(args, b)) throw new Error(`'${arac}' için yasak bayrak: ${b}`);
  }
  if (!bilgi) {
    const konum = konumlar(args);
    for (const dizi of kural.yasakDizi || []) {
      if (dizi.every((jeton, n) => konum[n] === jeton)) {
        throw new Error(`'${arac}' için yasak alt komut: ${dizi.join(" ")}`);
      }
    }
    for (const b of kural.gerekliBayrak || []) {
      if (!bayrakVar(args, b)) throw new Error(`'${arac}' yalnız ${b} ile koşar`);
    }
    if (kural.ghApiSaltOkur && konum[0] === "api") ghApiDenetle(args);
    if (kural.dosyaGerek && konum.length) {
      const dosya = path.resolve(cwd || process.cwd(), konum[0]);
      if (!fs.existsSync(dosya) || !fs.statSync(dosya).isFile()) {
        throw new Error(`'${arac}' için dosya yok: ${konum[0]}`);
      }
      if (!ayar.cwdKokleri.some((k) => altinda(dosya, k))) {
        throw new Error(`'${arac}' dosyası izinli köklerin dışında: ${dosya}`);
      }
    }
  }
  if (kural.altIzin) {
    // Alt komut ILK jeton olmali; bayrak arkasina gizlenemez.
    if (!bilgi && !kural.altIzin.includes(args[0])) {
      throw new Error(`'${arac}' için izinli olmayan alt komut: ${args[0] ?? "(yok)"}`);
    }
  } else if (!bilgi) {
    const alt = args.find((a) => !a.startsWith("-") && !a.includes("="));
    if (alt && ((kural.altYasak || []).includes(alt) || YASAK_FIIL.has(alt))) {
      throw new Error(`'${arac}' için yasak alt komut: ${alt}`);
    }
  }

  const yol = yolBul(arac);
  if (!yol) throw new Error(`'${arac}' PATH'te bulunamadı`);
  return { arac, args, yol };
}

/** Adı KEY/TOKEN/SECRET/PAT/PASSWORD segmenti içeren değişkenlerin DEĞERLERİ. */
function sirDegerleri() {
  const out = [];
  for (const [ad, deger] of Object.entries(process.env)) {
    if (!deger || deger.length < 4) continue;
    const segmentler = ad.toUpperCase().split(/[^A-Z0-9]+/);
    if (segmentler.some((s) => ["KEY", "TOKEN", "SECRET", "PAT", "PASSWORD"].includes(s))) {
      out.push(deger);
    }
  }
  return out.sort((a, b) => b.length - a.length);
}

/**
 * `claude -p` argv'sine geçen alanlar: bayrağa dönüşemeyecek kadar dar bir sınıf.
 * `--agent <deger>` bir değeri tüketse de, değeri bayrağa benzeyen girdi ayrıştırıcıya
 * göre yeniden bayrak olarak okunabiliyor — kaynakta kesilir.
 */
export function ajanAlanDenetle(alan, deger) {
  const s = String(deger ?? "");
  if (!/^[A-Za-z0-9._-]+$/.test(s) || s.startsWith("-")) {
    throw new Error(`${alan}: yalnız [A-Za-z0-9._-] kabul edilir, '-' ile başlayamaz`);
  }
  return s;
}

export function redakte(metin) {
  let s = String(metin ?? "");
  for (const d of sirDegerleri()) s = s.split(d).join("***");
  return s;
}

export function kirp(metin, tavan) {
  const s = String(metin ?? "");
  if (s.length <= tavan) return { metin: s, kirpildi: false };
  const bas = s.slice(0, 5000);
  const son = s.slice(-(tavan - 5000));
  return {
    metin: `${bas}\n\n… [${s.length - tavan} karakter kırpıldı; tamamı log dosyasında] …\n\n${son}`,
    kirpildi: true,
  };
}

export const SIKISTIR_ESIK = 8000;
/** Headroom'un kendi router tavanı 20 sn; üstüne bağlantı payı. */
export const SIKISTIR_ZAMAN_MS = 45000;

/**
 * >8 KB çıktı Headroom'a verilir. Tek yol `headroom mcp serve` stdio MCP'si:
 * HTTP tarafında sıkıştırma rotası yok (`/compress` 404, 11k K6 ölçümü).
 * Dönen zarf `{compressed, hash, original_tokens, compressed_tokens, ...}`; hash'i
 * Desktop'ta zaten kayıtlı olan `headroom` MCP'sinin `headroom_retrieve`'i açar.
 * @returns {Promise<object|null>} zarf, ya da null (eşik altı / başarısız)
 */
export async function sikistir(metin) {
  const s = String(metin ?? "");
  if (s.length <= SIKISTIR_ESIK) return null;
  const yol = yolBul("headroom");
  if (!yol) return null;
  const { Client } = await import("@modelcontextprotocol/sdk/client/index.js");
  const { StdioClientTransport } = await import("@modelcontextprotocol/sdk/client/stdio.js");
  const c = new Client({ name: "cc-kopru", version: "0.1.0" });
  const tasima = new StdioClientTransport({ command: yol, args: ["mcp", "serve"] });
  try {
    await c.connect(tasima);
    const r = await c.callTool({ name: "headroom_compress", arguments: { content: s } },
                               undefined, { timeout: SIKISTIR_ZAMAN_MS });
    const t = (r?.content || []).map((x) => x.text || "").join("\n").trim();
    return t ? JSON.parse(t) : null;
  } catch { return null; } finally {
    // `close()` tek başına yetmiyor: headroom.exe sürüyor ve düğüm olay döngüsünü
    // açık tutuyor (11k K6b: `node --test` hiç bitmedi). Süreç ağacı da kapatılır.
    const pid = tasima.pid;
    try { await c.close(); } catch { /* kapandı */ }
    if (pid) agaciKapat(pid);
  }
}

/**
 * Çıktı yolu: eşiğin üstü Headroom'a, altı `kirp`e.
 * Headroom "fail-open" çalışıyor — router zaman aşımına düşerse içeriği AYNEN geri
 * verir (11k K6b ölçümü: 33 480 → 33 499 karakter, tokens_saved 1). O yüzden sonuç
 * gerçekten küçülmediyse ham metin kırpılarak döner; şişmiş zarf çıktıya basılmaz.
 */
export async function ciktiHazirla(metin, tavan) {
  const z = await sikistir(metin);
  const kazanc = z ? (z.original_tokens || 0) - (z.compressed_tokens || 0) : 0;
  if (!z || kazanc <= 0 || String(z.compressed || "").length >= String(metin).length) {
    return kirp(metin, tavan).metin;
  }
  return `${z.compressed}\n\n[headroom] ${z.original_tokens} → ${z.compressed_tokens} jeton `
    + `(%${z.savings_percent}) · tamamı: headroom_retrieve hash=${z.hash}`;
}

export function agaciKapat(pid) {
  try {
    spawnSync("taskkill", ["/T", "/F", "/PID", String(pid)], { stdio: "ignore" });
  } catch { /* süreç zaten bitmiş olabilir */ }
}

/**
 * @returns {Promise<{kod:number, cikti:string, sureDoldu:boolean, log:string}>}
 */
export function kos({ arac, args, cwd, timeoutSn, ayar, env, denetimAtla }) {
  // denetimAtla: cagiran zaten komutDenetle'den gecirdi (hook yeniden yazimi sarmalamasi)
  const calisma = cwdCoz(cwd, ayar);
  const yol = denetimAtla ? yolBul(arac) : komutDenetle(arac, args, ayar, calisma).yol;
  if (!yol) throw new Error(`'${arac}' PATH'te bulunamadi`);
  const sn = Math.min(Math.max(Number(timeoutSn) || 120, 1), 600);

  let komut = yol;
  let tamArgs = args;
  if (/\.(cmd|bat)$/i.test(yol)) {
    const cozulen = shimCoz(yol);
    if (cozulen) {
      komut = cozulen.komut;
      tamArgs = [...cozulen.on, ...args];
    } else {
      for (const a of args) {
        if (CMD_EK.test(a)) throw new Error(`.cmd shim çözülemedi, argümanda riskli karakter: ${a}`);
      }
      komut = process.env.ComSpec || "cmd.exe";
      tamArgs = ["/d", "/s", "/c", yol, ...args];
    }
  }

  fs.mkdirSync(LOG_DIZIN, { recursive: true });
  const log = path.join(LOG_DIZIN, `${Date.now()}-${arac}.log`);

  // git'in sistem/global config'i uzerinden komut calistirmasi kapatilir
  const gitOrtam = arac === "git"
    ? { GIT_CONFIG_NOSYSTEM: "1", GIT_CONFIG_GLOBAL: "NUL" } : {};

  return new Promise((cozumle) => {
    const p = spawn(komut, tamArgs, {
      cwd: calisma, shell: false, windowsHide: true,
      env: { ...process.env, ...gitOrtam, ...(env || {}) },
    });
    const parcalar = [];
    let sureDoldu = false;
    p.stdout.on("data", (b) => parcalar.push(b));
    p.stderr.on("data", (b) => parcalar.push(b));

    const zamanlayici = setTimeout(() => {
      sureDoldu = true;
      agaciKapat(p.pid);
    }, sn * 1000);

    const bitir = (kod) => {
      clearTimeout(zamanlayici);
      let tam = redakte(Buffer.concat(parcalar).toString("utf8"));
      if (sureDoldu) tam += `\n[cc-kopru] zaman aşımı: ${sn} sn doldu, süreç ağacı kapatıldı.`;
      fs.writeFileSync(log, tam, "utf8");
      const { metin, kirpildi } = kirp(tam, ayar.ciktiTavan ?? 30000);
      cozumle({
        kod: kod ?? -1,
        cikti: kirpildi ? `${metin}\n[tam çıktı] ${log}` : metin,
        sureDoldu, log,
      });
    };

    p.on("error", (e) => { parcalar.push(Buffer.from(String(e))); bitir(-1); });
    p.on("close", (kod) => bitir(kod));
  });
}

/** argv'yi hook'lara verilecek tek komut satırına çevirir. */
export function komutSatiri(arac, args) {
  return [arac, ...args].map((a) => (/\s/.test(a) ? JSON.stringify(a) : a)).join(" ");
}

/**
 * Hook yeniden yazımı: yalnız ["rtk", ...orijinal argv] biçimi kabul edilir.
 * Satırı yeniden jetonlara bölmek argüman sınırlarını değiştirebiliyor
 * (`-1;whoami` -> `-1;` + `whoami`), o yüzden karşılaştırma satır üstünde yapılır.
 * @returns {string[]|null} kabul edilen argv ya da null (yazım yok sayılır)
 */
export function yenidenYazimKabul(orijinalArgv, yeniKomut) {
  const [arac, ...args] = orijinalArgv;
  const beklenen = komutSatiri("rtk", [arac, ...args]);
  return String(yeniKomut).trim() === beklenen ? ["rtk", arac, ...args] : null;
}

/**
 * claude-mem worker gövdesi. Şema strict: text/title/project/metadata dışı her anahtar
 * 400 ValidationError. "desktop" etiketi metadata.platformSource alanına girer —
 * worker bunu manual session'ın platformSource'u olarak okuyor.
 */
export function memGovde(proje, baslik, metin) {
  return { project: proje, title: baslik, text: metin, metadata: { platformSource: "desktop" } };
}

export const MEM_KOK = "http://127.0.0.1:37777";

/**
 * CC'nin kendi PostToolUse hook'uyla AYNI uç: POST /api/sessions/observations.
 * Uç, claude-mem hooks.json → worker-service.cjs zincirinden okundu (11k K3b);
 * uydurulmadı. Şema `.passthrough()`, zorunlu alanlar contentSessionId + tool_name.
 */
export function gozlemGovde(oturum, aracAdi, girdi, yanit, cwd) {
  return {
    contentSessionId: oturum,
    tool_name: aracAdi,
    tool_input: girdi,
    tool_response: yanit,
    cwd,
    platformSource: "claude-desktop",
  };
}

/** @returns {Promise<string>} boş = yazıldı, dolu = sebep (çağrıyı bozmaz). */
export async function gozlemYaz(govde) {
  try {
    const y = await fetch(`${MEM_KOK}/api/sessions/observations`, {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify(govde),
    });
    return y.ok ? "" : `gözlem yazılamadı: worker ${y.status}`;
  } catch (e) { return "gözlem yazılamadı: " + String(e?.message || e); }
}

/**
 * statusline.ps1'in stdin'de okuduğu DÖRT alan — fazlası yazılmaz.
 * Kaynak: son `ajan` çağrısının usage sayıları. Ajan hiç koşmadıysa null.
 */
export function statuslineGovde(son) {
  if (!son) return null;
  const girdi = son.girdi || 0;
  const pencere = son.pencere || 200000;
  return {
    model: { display_name: son.model },
    context_window: { used_percentage: Math.min(100, Math.round((girdi / pencere) * 1000) / 10) },
    prompt_cache: { hit_ratio: girdi ? (son.okunan || 0) / girdi : 0 },
  };
}

/**
 * gitleaks kapısı: metin sızıntı taşıyorsa ret sebebi, temizse null.
 * `kaydet` ve otomatik gözlem aynı kapıdan geçer.
 */
export async function sizintiKapisi(baslik, govde, ayar) {
  // gitleaks --source dizin ister ve cwd izinli kök altında olmalı → C:\Projeler altına
  const gDizin = path.join("C:/Projeler/.tmp-cc-kopru",
                           `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`);
  fs.mkdirSync(gDizin, { recursive: true });
  fs.writeFileSync(path.join(gDizin, "not.md"), `# ${baslik}\n\n${govde}\n`, "utf8");
  try {
    // --no-banner --no-color: ret çıktısında banner ve ANSI olmaz. Bulgular JSON rapora
    // yazılır; çıktıya yalnız sayı ve kural adı geçer, değer asla.
    const t = await kos({
      arac: "gitleaks",
      args: ["detect", "--no-git", "--redact", "--no-banner", "--no-color",
             "--report-format", "json", "--report-path", "bulgu.json", "--source", "."],
      cwd: gDizin, ayar,
    });
    if (t.kod === 0) return null;
    let rapor = null;
    try {
      rapor = JSON.parse(fs.readFileSync(path.join(gDizin, "bulgu.json"), "utf8"));
    } catch { /* rapor yazılamadıysa sayı bilinmez */ }
    return gitleaksOzet(rapor, t.kod);
  } finally {
    fs.rmSync(gDizin, { recursive: true, force: true });
  }
}

/** gitleaks JSON raporundan ret mesajı: sayı + kural adı. Bulgu değeri asla basılmaz. */
export function gitleaksOzet(rapor, kod) {
  const b = Array.isArray(rapor) ? rapor : [];
  if (!b.length) return `YAZILMADI — gitleaks: bulgu raporu okunamadı (exit ${kod})`;
  const kurallar = [...new Set(b.map((x) => String(x.RuleID ?? "?")))];
  return `YAZILMADI — gitleaks: ${b.length} bulgu (${kurallar.join(", ")})`;
}
