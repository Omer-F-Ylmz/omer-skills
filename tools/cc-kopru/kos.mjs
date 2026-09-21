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
  const ilk = (r.stdout || "").split(/\r?\n/).map((s) => s.trim()).filter(Boolean)[0] || null;
  yolOnbellek.set(arac, ilk);
  return ilk;
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

export function komutDenetle(arac, args, ayar) {
  const kural = ayar.izinli[arac];
  if (!kural) throw new Error(`'${arac}' allowlist'te değil`);
  if (kural.kos === false) throw new Error(`'${arac}' koşmaz: ${kural.sebep}`);

  for (const a of args) {
    if (METAKARAKTER.test(a)) throw new Error(`argümanda metakarakter: ${a}`);
    if (TEHLIKELI_SECENEK.test(a)) throw new Error(`yürütücüye komut geçiren secenek: ${a}`);
  }

  const bilgi = args.length === 1 && BILGI_BAYRAGI.test(args[0]);
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
  const yol = denetimAtla ? yolBul(arac) : komutDenetle(arac, args, ayar).yol;
  if (!yol) throw new Error(`'${arac}' PATH'te bulunamadi`);
  const calisma = cwdCoz(cwd, ayar);
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

/** gitleaks JSON raporundan ret mesajı: sayı + kural adı. Bulgu değeri asla basılmaz. */
export function gitleaksOzet(rapor, kod) {
  const b = Array.isArray(rapor) ? rapor : [];
  if (!b.length) return `YAZILMADI — gitleaks: bulgu raporu okunamadı (exit ${kod})`;
  const kurallar = [...new Set(b.map((x) => String(x.RuleID ?? "?")))];
  return `YAZILMADI — gitleaks: ${b.length} bulgu (${kurallar.join(", ")})`;
}
