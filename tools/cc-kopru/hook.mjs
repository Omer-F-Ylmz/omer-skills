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

import { agaciKapat, stdinYaz } from "./kos.mjs";

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

/**
 * Git Bash'in mutlak yolu. PATH'e güvenilmez: Desktop'ın MCP sürecinde bash yok
 * (11i-FIX-2 B2, 6 SessionStart hook'u "spawn bash ENOENT" verdi).
 * System32\\bash.exe (WSL) hiçbir zaman seçilmez — CC hook'ları Git Bash bekliyor.
 */
export function bashYolu() {
  const ozel = process.env.CLAUDE_CODE_GIT_BASH_PATH;
  if (ozel && !/system32/i.test(ozel) && fs.existsSync(ozel)) return ozel;
  return "C:\\Program Files\\Git\\bin\\bash.exe";
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

/**
 * Açık plugin'lerin kökleri: {ad, kok}. hookKaynaklari ile aynı keşif, ama
 * `hooks/hooks.json` şartı yok — katalog komut/agent/skill de sayar (11k K2b).
 * hookKaynaklari bilerek kopyalanmadı: orada arama hooks.json'da DURUYOR.
 */
export function eklentiKokleri() {
  const kullanici = jsonOku(path.join(EV, ".claude", "settings.json")) || {};
  const acik = Object.entries(kullanici.enabledPlugins || {})
    .filter(([, v]) => v === true).map(([k]) => k.split("@")[0]);
  const out = [];
  if (!fs.existsSync(EKLENTI_KOK)) return out;
  for (const sahip of fs.readdirSync(EKLENTI_KOK)) {
    const sd = path.join(EKLENTI_KOK, sahip);
    if (!fs.statSync(sd).isDirectory()) continue;
    for (const ad of fs.readdirSync(sd)) {
      if (!acik.includes(ad)) continue;
      const adaylar = [path.join(sd, ad), ...fs.readdirSync(path.join(sd, ad))
        .map((s) => path.join(sd, ad, s))];
      const kok = adaylar.find((k) => ["commands", "agents", "skills", "plugin.json"]
        .some((x) => fs.existsSync(path.join(k, x))));
      if (kok) out.push({ ad, kok });
    }
  }
  return out;
}

/**
 * 11l-FIX K2 ölçümü: hedef ajanların ilk cümleleri 45 · 63 · 298 karakter; eski
 * 160'lık tavan üçünü de cümle ortasından kesiyordu. Tavan en uzun ilk cümleye pay.
 */
export const ACIKLAMA_TAVAN = 320;

/** Tavanı aşan metni son cümle sınırından, cümle yoksa son kelimeden kırpar. */
function cumleKirp(s, tavan = ACIKLAMA_TAVAN) {
  if (s.length <= tavan) return s;
  const bas = s.slice(0, tavan);
  const son = [...bas.matchAll(/[.!?](?=\s|$)/g)].pop();
  if (son) return bas.slice(0, son.index + 1);
  const bosluk = bas.lastIndexOf(" ");
  return (bosluk > 0 ? bas.slice(0, bosluk) : bas) + "…";
}

/**
 * SKILL.md / komut dosyasından tek satır açıklama.
 * 11l K3: `description:` bir YAML blok skaleri olabilir (`|` · `>` · `|-` · `>-` · `|+`
 * · `>+`); o zaman satırın kendisi göstergeden ibaret, metin izleyen girintili
 * satırlardadır. Eskiden göstergenin kendisi açıklama sanılıp basılıyordu.
 * 11l-FIX K2: devam satırları da okunur. `|` satır sonlarını korur (ilk satır alınır),
 * `>` ve göstergesiz çok satırlı plain scalar katlanır — cümle ortasından kesilmez.
 */
export function aciklamaOku(dosya) {
  try {
    const bas = fs.readFileSync(dosya, "utf8").slice(0, 1500);
    const satirlar = bas.split(/\r?\n/);
    const n = satirlar.findIndex((x) => /^description:\s*/.test(x));
    let s;
    if (n >= 0) {
      s = satirlar[n].replace(/^description:\s*/, "");
      // devam satırları girintilidir; boş satır (paragraf) ya da yeni anahtar bitirir
      const devam = [];
      for (let i = n + 1; i < satirlar.length && /^\s+\S/.test(satirlar[i]); i++) {
        devam.push(satirlar[i].trim());
      }
      const gosterge = /^([|>])[-+]?\d*$/.exec(s.trim());
      if (gosterge) s = gosterge[1] === "|" ? (devam[0] || "") : devam.join(" ");
      else if (devam.length) s = [s.trim(), ...devam].join(" ");
    } else {
      s = satirlar.find((x) => x.trim() && !/^(---|#|name:)/.test(x.trim())) || "";
    }
    return cumleKirp(s.trim().replace(/^["']|["']$/g, "").trim());
  } catch { return ""; }
}

/**
 * CC'de açık plugin komutları · agent'lar · skill adları.
 * skillOverrides'ta "off" olanlar elenir. API çağrısı yok, yalnız dosya sistemi.
 */
export function katalogTopla(tur = "hepsi", ara = "") {
  const kullanici = jsonOku(path.join(EV, ".claude", "settings.json")) || {};
  const kapali = new Set(Object.entries(kullanici.skillOverrides || {})
    .filter(([, v]) => v === "off").map(([k]) => k));
  const out = [];
  const suzgec = String(ara || "").toLowerCase();
  const ekle = (t, ad, dosya) => {
    if (tur !== "hepsi" && tur !== t) return;
    if (suzgec && !ad.toLowerCase().includes(suzgec)) return;
    out.push({ tur: t, ad, aciklama: aciklamaOku(dosya) });
  };

  for (const { ad: pAd, kok } of [{ ad: "", kok: path.join(EV, ".claude") }, ...eklentiKokleri()]) {
    const on = pAd ? pAd + ":" : "";
    for (const [t, dizin] of [["komut", "commands"], ["ajan", "agents"]]) {
      const d = path.join(kok, dizin);
      if (!fs.existsSync(d)) continue;
      for (const f of fs.readdirSync(d)) {
        if (f.endsWith(".md")) ekle(t, on + f.replace(/\.md$/, ""), path.join(d, f));
      }
    }
    const sd = path.join(kok, "skills");
    if (!fs.existsSync(sd)) continue;
    for (const s of fs.readdirSync(sd)) {
      const sm = path.join(sd, s, "SKILL.md");
      if (!fs.existsSync(sm)) continue;
      if (kapali.has(`${pAd}:${s}`) || kapali.has(s)) continue;
      ekle("skill", on + s, sm);
    }
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
      exe = bashYolu();
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
    stdinYaz(p, JSON.stringify(girdi));
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
    // hook hatası bağlamda kalır: hook adı · exit · stderr ilk satırı
    if (r.kod !== 0 || r.err.trim()) {
      const ilk = r.err.trim().split(/\r?\n/)[0] || "";
      baglam.push(`[hook] ${t.anahtar} · exit ${r.kod} · ${ilk}`);
    }
  }

  return { karar: "izin", sebep: "", girdi: toolInput, ekBaglam: baglam.join("\n"), kosan };
}
