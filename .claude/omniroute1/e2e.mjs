// OMNIROUTE-1 uçtan uca: ajanOrtami(omni) env'iyle tek `claude -p` (combo cc-yedek). Anahtar değeri basılmaz.
import { spawnSync } from "node:child_process";
import { kullaniciEnv } from "../../tools/cc-kopru/kos.mjs";
import { OMNI_COMBO, ajanOrtami } from "../../tools/cc-kopru/omniroute.mjs";

// Köprü Desktop'tan koşar; bu oturumun CC-çocuk değişkenleri (CLAUDECODE, CHILD_SESSION, MESSAGING_*) orada yok → taklit için at.
const taban = Object.fromEntries(Object.entries(process.env).filter(([k]) => !/^(CLAUDECODE|CLAUDE_CODE_(CHILD|MESSAGING|SESSION|ENTRYPOINT|EXECPATH)|CLAUDE_PID)/.test(k)));
const r = ajanOrtami(taban, { apiKredi: false, omni: true, oku: (ad) => process.env[ad] || kullaniciEnv(ad) });
if (r.eksik) { console.log("eksik:", r.eksik); process.exit(1); }
const argv = ["-p", "--output-format", "json", "--model", OMNI_COMBO, "--disable-slash-commands",
  "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}'];
const p = spawnSync("C:/Users/pc/.local/bin/claude.exe", [...r.arg, ...argv], {
  input: "Yalnız şu kelimeyi yaz: TAMAM", env: r.env, encoding: "utf8", timeout: 240000, windowsHide: true });
const cikti = `${p.stdout || ""}${p.stderr || ""}`.split(r.sir).join("***");
try {
  const j = JSON.parse(p.stdout);
  console.log(JSON.stringify({ is_error: j.is_error, result: String(j.result).slice(0, 200), modeller: Object.keys(j.modelUsage || {}),
    usd: j.total_cost_usd, sure_ms: j.duration_ms, env_ok: r.env.KOPRU_OMNIROUTE === "1" && !("ANTHROPIC_API_KEY" in r.env) }));
} catch { console.log("JSON değil:", cikti.slice(0, 600)); }
