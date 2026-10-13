// OMNIROUTE-1 d3: normal mod (bayrak yok) — ajanOrtami env'i dokunmaz, Headroom yolu (settings.json ANTHROPIC_BASE_URL) çalışıyor mu. Tek `claude -p`.
import { spawnSync } from "node:child_process";
import { ajanOrtami } from "../../tools/cc-kopru/omniroute.mjs";

// API kredisi kapalı → ANTHROPIC_API_KEY çocuğa verilmez (plan limiti); CC-çocuk değişkenleri e2e.mjs'teki gibi atılır.
const taban = Object.fromEntries(Object.entries(process.env).filter(([k]) => k !== "ANTHROPIC_API_KEY" && !/^(CLAUDECODE|CLAUDE_CODE_(CHILD|MESSAGING|SESSION|ENTRYPOINT|EXECPATH)|CLAUDE_PID)/.test(k)));
const r = ajanOrtami(taban, { apiKredi: false, omni: false, oku: () => undefined });
const p = spawnSync("C:/Users/pc/.local/bin/claude.exe", [...r.arg, "-p", "--output-format", "json", "--model", "haiku", "--disable-slash-commands",
  "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}'], { input: "Yalnız şu kelimeyi yaz: TAMAM", env: r.env, encoding: "utf8", timeout: 240000, windowsHide: true });
try {
  const j = JSON.parse(p.stdout);
  console.log(JSON.stringify({ is_error: j.is_error, result: String(j.result).slice(0, 200), modeller: Object.keys(j.modelUsage || {}), sure_ms: j.duration_ms,
    env_dokunulmadi: r.env === taban && r.arg.length === 0 }));
} catch { console.log("JSON değil:", `${p.stdout || ""}${p.stderr || ""}`.slice(0, 600)); }
