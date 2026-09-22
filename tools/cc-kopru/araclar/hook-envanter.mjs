/**
 * KURULUM-11m-A-FIX-2 EK K1 — hook ortam eşitliği envanteri.
 *
 * Köprünün koşturduğu her Pre/PostToolUse hook'unu SAHTE payload'la çağırır ve
 * exit kodu · stdin okundu mu · karar/etki tablosunu basar. Komut çalıştırılmaz.
 *
 * Kullanım:  node araclar/hook-envanter.mjs [--desktop] [--proje <dizin>]
 *   --desktop  Claude Desktop'ın MCP beyaz listesini taklit eder (settings.json env yok)
 *
 * Girdi 64 KB boru tamponunu aşacak kadar doldurulur: aksi halde girdiyi okumadan
 * çıkan hook'un yazımı da "başarılı" görünür (11m-A-FIX-2 stdinYaz notu).
 */
import { hookKaynaklari, hookTanimlari, matcherEslesir, tekHookKos } from "../hook.mjs";

/** Claude Desktop'ın alt sürece geçirdiği değişkenler (app.asar ofset 3899305). */
const DESKTOP_ENV = ["APPDATA", "HOMEDRIVE", "HOMEPATH", "LOCALAPPDATA", "PATH",
  "PROCESSOR_ARCHITECTURE", "SYSTEMDRIVE", "SYSTEMROOT", "TEMP", "USERNAME",
  "USERPROFILE", "PROGRAMFILES"];

/** Ortamı Desktop beyaz listesine indirir; geri alma işlevi döner. Değer basılmaz. */
export function desktopOrtamiUygula() {
  const yedek = { ...process.env };
  for (const ad of Object.keys(process.env)) {
    if (!DESKTOP_ENV.includes(ad.toUpperCase())) delete process.env[ad];
  }
  return () => {
    for (const ad of Object.keys(process.env)) delete process.env[ad];
    Object.assign(process.env, yedek);
  };
}

/** hookKos'un çıkış anlamıyla aynı sınıflama — tek hook için. */
function etki(olay, r) {
  if (r.kod === 2) return olay === "PreToolUse" ? "RED" : "uyarı→bağlam";
  let j = null;
  try { j = JSON.parse(r.out.trim()); } catch { /* düz metin hook */ }
  const hso = j?.hookSpecificOutput;
  if (hso?.permissionDecision === "deny") return "RED";
  if (hso?.updatedInput) return "girdi yeniden yazıldı";
  if (r.kod !== 0) return `hata (exit ${r.kod})`;
  // exit 0 + systemMessage: hook kendi hatasını bildiriyor (hookify import hatası gibi)
  if (j?.systemMessage) return `uyarı: ${String(j.systemMessage).slice(0, 60)}`;
  if (hso?.additionalContext || (!j && r.out.trim())) return "bağlam eklendi";
  return "izin";
}

export async function envanter(projeDir, olaylar = ["PreToolUse", "PostToolUse"]) {
  const defs = hookTanimlari(hookKaynaklari(projeDir), []);
  const dolgu = "x".repeat(80 * 1024);
  const out = [];
  for (const olay of olaylar) {
    for (const t of defs.filter((x) => x.olay === olay)) {
      if (!matcherEslesir(t.matcher, "Bash")) continue;
      const girdi = {
        session_id: "envanter", cwd: projeDir, hook_event_name: olay, tool_name: "Bash",
        tool_input: { command: "git status", description: "hook-envanter" },
        tool_response: { stdout: "", exitCode: 0 },
        _dolgu: dolgu,
      };
      const r = await tekHookKos(t, girdi, projeDir);
      out.push({ anahtar: t.anahtar, kod: r.kod, girdiYazildi: r.girdiYazildi, etki: etki(olay, r) });
    }
  }
  return out;
}

if (process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, "/"))) {
  const proje = process.argv[process.argv.indexOf("--proje") + 1] || process.cwd();
  const desktop = process.argv.includes("--desktop");
  const geri = desktop ? desktopOrtamiUygula() : () => {};
  const satirlar = await envanter(proje);
  geri();
  console.log(`ortam: ${desktop ? "Desktop taklidi" : "CC"} · proje: ${proje}`);
  for (const s of satirlar) {
    const g = s.girdiYazildi === null ? "?" : s.girdiYazildi ? "evet" : "HAYIR";
    console.log(`${s.anahtar} | exit ${s.kod} | stdin ${g} | ${s.etki}`);
  }
}
