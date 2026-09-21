/**
 * cc-kopru · hook runner (KURULUM-11i K1).
 * Kural kopyalanmaz: hook tanımları CC'nin kendi dosyalarından okunur ve aynen koşar.
 * Kaynak sırası: ~/.claude/settings.json → açık plugin'lerin hooks/hooks.json →
 * <proje>/.claude/settings(.local).json.
 */
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

import { agaciKapat } from "./kos.mjs";

const EV = os.homedir();
const EKLENTI_KOK = path.join(EV, ".claude", "plugins", "cache");
export const IZ_DIZIN = path.join(os.tmpdir(), "cc-kopru");

/** CC'nin matcher'ı regex; ifade matcher'ları (tool=="Bash" && …) desteklenmez. */
export function matcherEslesir(matcher, ad) {
  if (matcher === undefined || matcher === null || matcher === "" || matcher === "*") return true;
  if (/==|&&|\bmatches\b/.test(matcher)) return false; // ifade matcher'ı — atlanır
  try {
    return new RegExp(`^(?:${matcher})$`).test(ad);
  } catch {
    return false;
  }
}

function jsonOku(p) {
  try { return JSON.parse(fs.readFileSync(p, "utf8")); } catch { return null; }
}

/** Okunabilen tüm hook kaynakları: {ad, json, kok}. `kok` = CLAUDE_PLUGIN_ROOT. */
export function hookKaynaklari(projeDir) {
  const out = [];
  const kullanici = jsonOku(path.join(EV, ".claude", "settings.json"));
  if (kullanici) out.push({ ad: "user-settings", json: kullanici, kok: path.join(EV, ".claude") });

  const acik = Object.entries(kullanici?.enabledPlugins || {})
    .filter(([, v]) => v === true)
    .map(([k]) => k.split("@")[0]);
  if (fs.existsSync(EKLENTI_KOK)) {
    for (const sahip of fs.readdirSync(EKLENTI_KOK)) {
      const sd = path.join(EKLENTI_KOK, sahip);
      if (!fs.statSync(sd).isDirectory()) continue;
      for (const ad of fs.readdirSync(sd)) {
        if (!acik.includes(ad)) continue;
        // sürüm klasörü olabilir ya da doğrudan plugin kökü
        const adaylar = [path.join(sd, ad), ...fs.readdirSync(path.join(sd, ad))
          .map((s) => path.join(sd, ad, s))];
        for (const kok of adaylar) {
          const hj = path.join(kok, "hooks", "hooks.json");
          if (!fs.existsSync(hj)) continue;
          const json = jsonOku(hj);
          if (json) out.push({ ad: `plugin:${ad}`, json, kok });
          break;
        }
      }
    }
  }

  for (const dosya of ["settings.json", "settings.local.json"]) {
    const p = path.join(projeDir || ".", ".claude", dosya);
    const json = jsonOku(p);
    if (json) out.push({ ad: `proje:${dosya}`, json, kok: path.dirname(p) });
  }
  return out;
}

/** Kaynakları düz bir tanım listesine açar; kapatılanlar elenir. */
export function hookTanimlari(kaynaklar, kapaliHooklar = []) {
  const kapali = new Set(kapaliHooklar);
  const out = [];
  for (const k of kaynaklar) {
    for (const [olay, gruplar] of Object.entries(k.json?.hooks || {})) {
      for (const g of gruplar || []) {
        for (const h of g.hooks || []) {
          if (h.type && h.type !== "command") continue;
          const anahtar = `${k.ad}|${olay}|${g.matcher ?? "*"}`;
          if (kapali.has(anahtar)) continue;
          // CC iki biçimi destekliyor: `command` tek kabuk satırı, ya da
          // `command` + `args[]` (argv, kabuksuz). İkincisi settings.json'da kullanılıyor.
          const argv = Array.isArray(h.args) ? h.args : null;
          out.push({
            kaynak: k.ad, kok: k.kok, olay, matcher: g.matcher,
            komut: argv ? `${h.command} ${argv.join(" ")}` : h.command,
            exe: h.command, argv, kabuk: h.shell, timeout: h.timeout, anahtar,
          });
        }
      }
    }
  }
  return out;
}

/** Her oturum için asgari transcript — transcript'e bakan hook'lar boşa düşmesin. */
export function izDosyasi(oturumId) {
  fs.mkdirSync(IZ_DIZIN, { recursive: true });
  const p = path.join(IZ_DIZIN, `${oturumId}.jsonl`);
  if (!fs.existsSync(p)) {
    fs.writeFileSync(p, JSON.stringify({
      type: "user", uuid: oturumId, timestamp: new Date().toISOString(),
      message: { role: "user", content: "cc-kopru oturumu" },
    }) + "\n", "utf8");
  }
  return p;
}

function tekHookKos(tanim, girdi, projeDir) {
  const sn = Math.min(Number(tanim.timeout) || 60, 600);
  const coz = (s, ileriEgik) => String(s).replace(
    /\$\{CLAUDE_PLUGIN_ROOT\}|%CLAUDE_PLUGIN_ROOT%/g,
    ileriEgik ? tanim.kok.replace(/\\/g, "/") : tanim.kok);

  let exe, argv, verbatim = false;
  if (tanim.argv) {
    // argv biçimi: kabuk yok, tırnak sorunu yok
    exe = coz(tanim.exe, false);
    argv = tanim.argv.map((a) => coz(a, false));
  } else {
    // kabuk satırı: POSIX görünümlüyse bash, değilse cmd (verbatim, Node tırnağı bozmasın)
    const posix = tanim.kabuk === "bash" || /\.sh\b/.test(tanim.komut) || /^\s*\[\s/.test(tanim.komut);
    const komut = coz(tanim.komut, posix);
    if (posix) {
      exe = "bash";
      argv = ["-c", komut];
    } else {
      exe = process.env.ComSpec || "cmd.exe";
      argv = ["/d", "/s", "/c", `"${komut}"`];
      verbatim = true;
    }
  }

  return new Promise((cozumle) => {
    let p;
    try {
      p = spawn(exe, argv, {
        cwd: projeDir || girdi.cwd || process.cwd(), shell: false, windowsHide: true,
        windowsVerbatimArguments: verbatim,
        env: {
          ...process.env,
          CLAUDE_PROJECT_DIR: projeDir || girdi.cwd || process.cwd(),
          CLAUDE_PLUGIN_ROOT: tanim.kok,
        },
      });
    } catch (e) {
      return cozumle({ kod: -1, out: "", err: String(e) });
    }
    const o = [], h = [];
    p.stdout.on("data", (b) => o.push(b));
    p.stderr.on("data", (b) => h.push(b));
    // cmd.exe'yi oldurmek yetmiyor: cocuk surec borulari acik tutuyor -> agac kapatilir
    const zam = setTimeout(() => agaciKapat(p.pid), sn * 1000);
    p.on("error", (e) => { clearTimeout(zam); cozumle({ kod: -1, out: "", err: String(e) }); });
    p.on("close", (kod) => {
      clearTimeout(zam);
      cozumle({
        kod, out: Buffer.concat(o).toString("utf8"), err: Buffer.concat(h).toString("utf8"),
      });
    });
    p.stdin.end(JSON.stringify(girdi));
  });
}

/**
 * Eşleşen hook'ları sırayla koşar, CC'nin çıkış anlamını uygular.
 * @returns {Promise<{karar:"izin"|"red", sebep:string, girdi:object, ekBaglam:string, kosan:string[]}>}
 */
export async function hookKos(tanimlar, girdi, { projeDir } = {}) {
  let toolInput = girdi.tool_input;
  const baglam = [], kosan = [];
  const olay = girdi.hook_event_name;

  for (const t of tanimlar) {
    if (t.olay !== olay) continue;
    if (!matcherEslesir(t.matcher, girdi.tool_name || girdi.source || "")) continue;
    kosan.push(t.anahtar);

    const r = await tekHookKos(t, { ...girdi, tool_input: toolInput }, projeDir);

    // exit 2 = engelle. PreToolUse'da red; öteki olaylarda uyarı olarak bağlama girer.
    if (r.kod === 2) {
      const sebep = (r.err || r.out).trim() || `${t.anahtar} exit 2`;
      if (olay === "PreToolUse") return { karar: "red", sebep, girdi: toolInput, ekBaglam: baglam.join("\n"), kosan };
      baglam.push(`[${t.kaynak}] ${sebep}`);
      continue;
    }

    let j = null;
    try { j = JSON.parse(r.out.trim()); } catch { /* düz metin hook */ }
    const hso = j?.hookSpecificOutput;
    if (hso?.permissionDecision === "deny") {
      return {
        karar: "red", sebep: hso.permissionDecisionReason || `${t.anahtar} deny`,
        girdi: toolInput, ekBaglam: baglam.join("\n"), kosan,
      };
    }
    if (hso?.updatedInput) toolInput = { ...toolInput, ...hso.updatedInput };
    if (hso?.additionalContext) baglam.push(String(hso.additionalContext));
    if (!j && r.out.trim()) baglam.push(r.out.trim());
    if (r.err.trim()) baglam.push(`[${t.kaynak}] ${r.err.trim()}`);
  }

  return { karar: "izin", sebep: "", girdi: toolInput, ekBaglam: baglam.join("\n"), kosan };
}
