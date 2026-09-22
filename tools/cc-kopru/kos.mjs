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

/**
 * 11m-A K2: git uzun secenekte benzersiz ONEK kisaltmasini kabul eder — `--out`
 * `--output`tur, `--no-ind` `--no-index`tir. Tam ad esitligi (bayrakVar) bu yuzden
 * yetmez; yasak liste onek eslemesiyle uygulanir. `=` ile birlesik deger ve kisa
 * bayraga bitisik deger (`-Oless`) ayni kapidan gecer.
 * Uzun bayrakta 5 karakter alt siniri var: daha kisa onekleri git'in kendisi de
 * "ambiguous" diye reddediyor, `--name-only` gibi mesru bayraklar da elenmemeli.
 */
export function yasakOnekVar(args, bayrak) {
  return args.some((a) => {
    if (!bayrak.startsWith("--")) return a === bayrak || a.startsWith(bayrak);
    const ad = a.split("=")[0];
    return ad.length >= 5 && bayrak.startsWith(ad);
  });
}

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
  for (const b of kural.yasakOnekBayrak || []) {
    if (yasakOnekVar(args, b)) throw new Error(`'${arac}' için yasak bayrak: ${b}`);
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

  // 11l K2: npm'in npx ayrıştırması `--` olmadan paketin bayrağını kendine mal ediyor —
  // `npx --no pixeljury --version` npm'in kendi sürümünü (11.17.0) döndü, paket koşmadı;
  // `npx --no -- pixeljury --version` 0.1.5 döndü. Aynı sonuç rtk'sız doğrudan çağrıda da
  // çıktığı için kök neden npm, rtk değil. Gerekli bayraktan sonra ayırıcı eklenir.
  // (uvx'in `--offline`ı aynı sorunu yaşamıyor; bu yüzden liste araca bağlı.)
  let cikanArgs = args;
  if ((arac === "npx" || arac === "bunx") && !args.includes("--")) {
    const n = args.findIndex((a) => (kural.gerekliBayrak || [])
      .some((b) => a === b || a.startsWith(b + "=")));
    if (n >= 0) cikanArgs = [...args.slice(0, n + 1), "--", ...args.slice(n + 1)];
  }

  const yol = yolBul(arac);
  if (!yol) throw new Error(`'${arac}' PATH'te bulunamadı`);
  return { arac, args: cikanArgs, yol };
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

/**
 * Yerel (Europe/Istanbul) gün, `YYYY-MM-DD`. 11l K5: `toISOString()` UTC verir, Istanbul
 * UTC+3 olduğu için yerel 00:00-03:00 arası bir önceki güne sayılıyordu.
 * `sv-SE` yerel ayarı zaten ISO biçimi üretir — ayrı biçimlendirmeye gerek yok.
 */
export const yerelGun = (d = new Date()) =>
  new Intl.DateTimeFormat("sv-SE", { timeZone: "Europe/Istanbul" }).format(d);

export function kirp(metin, tavan) {
  const s = String(metin ?? "");
  if (s.length <= tavan) return { metin: s, kirpildi: false };
  // Etiket tavanIN İÇİNDE kalır. 11m-A-FIX K2 öncesi çıktı tavan + etiket kadardı;
  // ikinci katman (sunucu) da her çağrıda yalnız o ~130 karakteri kırpıyordu.
  const etiket = (n) => `\n\n… [${n} karakter kırpıldı; tamamı log dosyasında] …\n\n`;
  const pay = etiket(s.length).length;
  const basN = Math.max(0, Math.min(5000, Math.floor((tavan - pay) / 2)));
  const sonN = Math.max(0, tavan - pay - basN);
  return {
    metin: s.slice(0, basN) + etiket(s.length - basN - sonN) + (sonN ? s.slice(-sonN) : ""),
    kirpildi: true,
  };
}

export const SIKISTIR_ESIK = 8000;
/**
 * 11l K7 ölçümü: başarılı sıkıştırma (tekrarlı 87 KB log) 6,3 sn sürüyor — tarifin
 * 3 sn tavanı bütün sıkıştırmayı kapatırdı. Tavan ölçülen süreye pay eklenerek 10 sn;
 * aşılırsa `sikistir` null döner ve çıktı kırpmaya düşer (fail-open).
 */
export const SIKISTIR_ZAMAN_MS = 10000;

/**
 * Çıktı sınıfı. 11m-A K4: sıkıştırma kararı metnin TÜRÜNE bağlanır, 11l'in 3-gram
 * tekrar oranına değil — tekrarsız ama sıkıştırılabilir log (farklı satırlar, aynı
 * biçim) kapıya takılıyordu. Markdown ve kod sıkıştırılmaz: 11l K7 ölçümünde 31 KB'lık
 * başlık + tablo gövdesi 13784→1834 jetona iniyor ama `## Bolum` başlıkları ve
 * `Kanit …` satırları çıktıda hiç yok — kayıplı.
 * @returns {"json"|"markdown"|"kod"|"log"}
 */
const ETIKET_SATIRI = /^\[[^\]]*\]$/;

/**
 * Köprü ve rtk kendi tam-satır `[...]` etiketlerini gövdenin başına/sonuna ekliyor
 * (`[hook yeniden yazdı] ...`, rtk'nin `[N words compressed ...]` altlığı). Sınıflama
 * onların üstünde yapılınca JSON `}` ile bitmiyor ve `log` sayılıyordu (11m-A-FIX K1).
 */
export function govdeAyikla(metin) {
  const l = String(metin ?? "").split("\n");
  // Uzunluk kapisi sart: tek satirlik JSON dizisi de `[...]` bicimindedir ve
  // etiket sanilip govdenin kendisi ayiklanirdi. Etiketler tek kisa satirdir.
  const etiket = (x) => !x.trim() || (x.trim().length <= 200 && ETIKET_SATIRI.test(x.trim()));
  while (l.length && etiket(l[0])) l.shift();
  while (l.length && etiket(l[l.length - 1])) l.pop();
  return l.join("\n");
}

export function ciktiSinifi(metin) {
  const s = govdeAyikla(metin).trim();
  if (!s) return "log";
  if ((s.startsWith("{") && s.endsWith("}")) || (s.startsWith("[") && s.endsWith("]"))) {
    try { JSON.parse(s); return "json"; } catch { /* JSON değil, aşağıdaki kapılara düşer */ }
  }
  const satirlar = s.split("\n");
  const kac = (re) => satirlar.filter((l) => re.test(l)).length;
  if (kac(/^#{1,6}\s/) || kac(/^\s*```/) || kac(/^\s*\|.*\|\s*$/) >= 2) return "markdown";
  if (kac(/^\s*(import|export|from|def|class|function|const|let|var|public|private|using|namespace)\s/)
      >= Math.max(3, satirlar.length * 0.1)) return "kod";
  if (kac(/^\s*[-*]\s/) >= satirlar.length * 0.5) return "markdown";
  return "log";
}

/**
 * Katmandan geçen sınıflar — ölçümle belirlendi (11m-A K4, docs/kurulum-11m.md).
 * `json` 20865→16424 karakter (%21) · `log` ise gerçek komut çıktısında hiç kazanmıyor:
 * `git log -100 --stat` 92377→92463, yani Headroom içeriği aynen (biraz da şişirerek)
 * geri veriyor. Yapay tekrarlı log gövdesinde %30 kazanıyor ama gerçek çıktıda değil,
 * bu yüzden `log` tarifin %15 eşiğine takılıp katmandan ÇIKTI. Büyük log çıktısının
 * kazancı sıkıştırmadan değil, tavanda kırpma + tam çıktının log dosyasında
 * kalmasından geliyor (92377→30142 karakter).
 */
export const SIKISAN_SINIFLAR = new Set(["json"]);

/**
 * >8 KB çıktı Headroom'a verilir (sınıf kapısı çağıranda).
 * Tek yol `headroom mcp serve` stdio MCP'si:
 * HTTP tarafında sıkıştırma rotası yok (`/compress` 404, 11k K6 ölçümü).
 * Dönen zarf `{compressed, hash, original_tokens, compressed_tokens, ...}`; hash'i
 * Desktop'ta zaten kayıtlı olan `headroom` MCP'sinin `headroom_retrieve`'i açar.
 * @returns {Promise<object|null>} zarf, ya da null (eşik altı / başarısız)
 */
export async function sikistir(metin, zamanMs = SIKISTIR_ZAMAN_MS) {
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
                               undefined, { timeout: zamanMs });
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
 * Çıktı tavanı (karakter). `kopru.json` yoksa/anahtar eksikse geçerli değer budur;
 * beş çağrı yerinde tekrarlanan `?? 30000` Desktop tavanının üç katıydı (11m-A-FIX K2).
 */
export const CIKTI_TAVAN = 10000;

/** LOG_DIZIN'de tutulan dosya sayısı; fazlası en eskiden silinir. */
export const LOG_TAVAN = 200;

export function logBudama(tavan = LOG_TAVAN) {
  let adlar;
  try { adlar = fs.readdirSync(LOG_DIZIN); } catch { return 0; }
  if (adlar.length <= tavan) return 0;
  const sirali = adlar
    .map((ad) => {
      try { return { ad, t: fs.statSync(path.join(LOG_DIZIN, ad)).mtimeMs }; } catch { return null; }
    })
    .filter(Boolean)
    .sort((a, b) => b.t - a.t);
  let silinen = 0;
  for (const { ad } of sirali.slice(tavan)) {
    try { fs.rmSync(path.join(LOG_DIZIN, ad), { force: true }); silinen += 1; } catch { /* kilitli */ }
  }
  return silinen;
}

/** Tam çıktı dosyası. Çağıran metni REDAKTE edilmiş verir; burada yeniden taranmaz. */
export function logaYaz(metin, etiket = "cikti") {
  fs.mkdirSync(LOG_DIZIN, { recursive: true });
  const yol = path.join(LOG_DIZIN, `${Date.now()}-${etiket}.log`);
  fs.writeFileSync(yol, String(metin ?? ""), "utf8");
  logBudama();
  return yol;
}

/**
 * Çıktı katmanı (11m-A K4). Eşiğin üstündeki log/JSON çıktısı yerel Headroom ile
 * sıkıştırılır, tam çıktı log dosyasında kalır, ilk satır `[headroom %X · tam: <yol>]`.
 * Markdown/kod sıkıştırılmaz. `ham` katmanı tümüyle atlar. Ağ çağrısı yoktur.
 *
 * Headroom "fail-open" çalışıyor — router zaman aşımına düşerse içeriği AYNEN geri
 * verir (11k K6b ölçümü: 33 480 → 33 499 karakter, tokens_saved 1). Sonuç gerçekten
 * küçülmediyse ham metin döner; şişmiş zarf çıktıya basılmaz.
 *
 * @param {{ham?:boolean, log?:string}} secenek log: çağıranın zaten yazdığı tam çıktı yolu
 */
export async function ciktiHazirla(metin, tavan, { ham = false, log = "" } = {}) {
  const s = String(metin ?? "");
  const kirpik = () => {
    if (s.length <= tavan) return s;
    const yol = log || logaYaz(s);
    const on = `[kırpıldı · tam: ${yol}]\n`;
    return on + kirp(s, tavan - on.length).metin;
  };
  if (ham || s.length <= SIKISTIR_ESIK || !SIKISAN_SINIFLAR.has(ciktiSinifi(s))) return kirpik();

  // Headroom'un içerik algılaması rtk'nin başlık/altlık satırlarında bozuluyor: aynı
  // gövde sarılı halde %0 kazanıyor (90 243 kr değişmeden geri), ayıklanmış halde %52,4.
  // Sıkıştırma da ayıklanmış gövdede yapılır; rtk'nin altlığı (recall hash'i) geri eklenir.
  const cekirdek = govdeAyikla(s);
  const artik = s.slice(s.indexOf(cekirdek) + cekirdek.length).trim();
  const z = await sikistir(cekirdek);
  const kazanc = z ? (z.original_tokens || 0) - (z.compressed_tokens || 0) : 0;
  if (!z || kazanc <= 0 || String(z.compressed || "").length >= cekirdek.length) {
    // Sıkıştırma hatası ya da kazançsız: ham çıktı + uyarı satırı, uydurma yüzde yok.
    const yol = log || logaYaz(s);
    const on = `[headroom yok · tam: ${yol}]\n`;
    return on + kirp(s, tavan - on.length).metin;
  }
  const yol = log || logaYaz(s);
  // Sıkıştırılmış gövde de tavana tabi: `gh api` %48,1 kazançla bile 67 622 karakterle
  // bağlama giriyordu (11m-A-FIX K2 canlı ölçümü). Tamamı yine log dosyasında.
  const on = `[headroom %${z.savings_percent} · tam: ${yol}]\n`;
  return on + kirp(z.compressed + (artik ? `\n${artik}` : ""), tavan - on.length).metin;
}

/**
 * Çocuğa stdin verisi yazar. Kısıtlı Desktop ortamında hook süreçleri girdiyi
 * OKUMADAN çıkıyor (PYTHONPATH'siz python vb.); 64 KB boru tamponunu aşan yazımda
 * yarım kalan write EPIPE/EOF atıyor ve `stdin` üzerinde dinleyici olmadığı için
 * Node "Unhandled 'error' event" ile BÜTÜN köprüyü düşürüyordu (11m-A-FIX-2).
 * Yazılamayan hook girdisi hata değildir: süreç zaten kendi çıkış koduyla değerlendirilir.
 * @returns {Promise<boolean>} girdi tamamı yazıldı mı (false = çocuk okumadan çıktı)
 */
export function stdinYaz(p, veri) {
  return new Promise((cozumle) => {
    p.stdin.on("error", () => cozumle(false)); // çocuk girdiyi okumadan çıktı
    p.stdin.end(veri, () => cozumle(true));
  });
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
  // denetim `--` ayiricisini eklemis olabilir (11l K2); kosan argv denetimden cikandir.
  const d = denetimAtla ? { yol: yolBul(arac), args } : komutDenetle(arac, args, ayar, calisma);
  const yol = d.yol;
  if (!yol) throw new Error(`'${arac}' PATH'te bulunamadi`);
  args = d.args;   // asagidaki her dal (shim · cmd /c · dogrudan) ayni argv'yi gormeli
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
      // Kırpma/sıkıştırma TEK katmanda: `ciktiHazirla`. Burada da kırpınca sınıf kapısı
      // JSON'u göremiyor, tavan iki kez uygulanıyor (ikincisi yalnız ilk etiketi kesiyor)
      // ve log yolu çıktıda iki kez geçiyordu (11m-A-FIX K1/K2). Tam çıktı `log` dosyasında.
      cozumle({ kod: kod ?? -1, cikti: tam, sureDoldu, log });
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

/** Port claude-mem'in kendi değişkeninden okunur (worker de onu okuyor); yoksa 37777. */
export const MEM_KOK = `http://127.0.0.1:${process.env.CLAUDE_MEM_WORKER_PORT || 37777}`;

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

/**
 * @returns {Promise<string>} boş = kuyruğa girdi, dolu = sebep (çağrıyı bozmaz).
 * 11m-A-FIX-3 K3: worker sessiz reddi 200 ile bildiriyor ({status:"skipped",
 * reason:"project_excluded"|"tool_excluded"|"private"}); eskiden bu "yazıldı" sayılıyordu.
 */
export async function gozlemYaz(govde) {
  try {
    const y = await fetch(`${MEM_KOK}/api/sessions/observations`, {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify(govde),
    });
    const j = await y.json().catch(() => null);
    if (!y.ok) return `gözlem yazılamadı: worker ${y.status}${j?.reason ? " " + j.reason : ""}`;
    if (j?.status && j.status !== "queued") return `gözlem yazılmadı: worker ${j.status} (${j.reason || "?"})`;
    return "";
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
