/* KURULUM-11f gecici izi. node --require ile yuklenir (NODE_OPTIONS degil).
 *
 * Amac: Desktop'in MCP sunucusunu HANGI calisma dizininde baslattigini olcmek ve
 * sessiz cikislarin nedenini yakalamak. puppeteer-mcp-server tum hatalarini
 * cwd'ye goreli dosya gunlugune yazip process.exit(1) cagirdigi icin Desktop
 * log'unda stderr bos gorunuyor.
 *
 * Kurallar: stdout'a TEK BAYT yazilmaz (JSON-RPC kanali). Ortam degiskenlerinin
 * yalnizca ADLARI kaydedilir, degerleri asla. Iz kendi hatasini yutar.
 * Kapanista wrapper'lardaki --require cikar, bu dosya tools/ altinda kalir.
 */
const fs = require("fs");
const path = require("path");
const tty = require("tty");

const DIZIN = "C:\\Projeler\\.tmp-mcp-trace";
const AD = process.env.K11F_AD || "bilinmeyen";
const DOSYA = path.join(DIZIN, `${AD}-${process.pid}.jsonl`);

function kayit(olay, veri) {
  try {
    fs.appendFileSync(DOSYA, JSON.stringify({ t: new Date().toISOString(), olay, ...veri }) + "\n");
  } catch { /* iz sunucuyu asla dusurmez */ }
}

function fdTuru(fd) {
  try {
    const s = fs.fstatSync(fd);
    return (s.isFIFO() && "pipe") || (s.isFile() && "file") ||
           (s.isCharacterDevice() && (tty.isatty(fd) ? "tty" : "chardev")) || "diger";
  } catch (e) { return "hata:" + e.code; }
}

function yigin(e, n = 5) {
  return String((e && e.stack) || e).split("\n").slice(0, n);
}

try {
  fs.mkdirSync(DIZIN, { recursive: true });
  kayit("acilis", {
    pid: process.pid,
    ppid: process.ppid,
    cwd: process.cwd(),
    // wrapper duzeltmeden ONCE yakaladigi Desktop cwd'si -- asil kanit satiri
    cwd0: process.env.K11F_CWD0 || null,
    execPath: process.execPath,
    argv: process.argv.slice(1),
    envAdlari: Object.keys(process.env).sort(),   // YALNIZ AD
    fd: { 0: fdTuru(0), 1: fdTuru(1), 2: fdTuru(2) },
  });

  // stdin'i akis moduna sokmadan gozlemle: 'data' dinlemek yerine emit'i sar.
  let ilkGirdi = true;
  const stdinEmit = process.stdin.emit.bind(process.stdin);
  process.stdin.emit = function (olay, ...a) {
    try {
      if (olay === "data" && ilkGirdi) {
        ilkGirdi = false;
        const ham = String(a[0]);
        let method = null;
        try { method = JSON.parse(ham.split("\n")[0]).method || null; } catch {}
        kayit("stdin-ilk", { bayt: Buffer.byteLength(ham), method });
      } else if (olay === "end" || olay === "close") {
        kayit("stdin-" + olay, {});
      }
    } catch { }
    return stdinEmit(olay, ...a);
  };

  let ilkCikti = true;
  const stdoutWrite = process.stdout.write.bind(process.stdout);
  process.stdout.write = function (parca, ...a) {
    if (ilkCikti) { ilkCikti = false; kayit("stdout-ilk", { bayt: Buffer.byteLength(String(parca)) }); }
    return stdoutWrite(parca, ...a);
  };

  const cik = process.exit.bind(process);
  process.exit = function (kod) {
    kayit("exit-cagrisi", { kod, cagiran: yigin(new Error("cagiran")) });
    return cik(kod);
  };

  // Not: bu dinleyici logger.js'inkinden once kaydolur. Kaydettikten sonra 1 ile
  // cikiyoruz; boylece iz, yutulmus gibi gorunen bir cokusu maskelemis olmaz.
  process.on("uncaughtException", (e) => {
    kayit("uncaughtException", { mesaj: String(e && e.message), kod: e && e.code, yigin: yigin(e) });
    cik(1);
  });
  process.on("unhandledRejection", (e) => {
    kayit("unhandledRejection", { mesaj: String(e && e.message), kod: e && e.code, yigin: yigin(e) });
  });

  process.on("exit", (kod) => kayit("exit", { kod }));
} catch (e) {
  kayit("iz-hatasi", { mesaj: String(e && e.message), yigin: yigin(e) });
}
