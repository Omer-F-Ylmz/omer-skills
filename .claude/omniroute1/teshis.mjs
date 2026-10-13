// OMNIROUTE-1 d2 teşhis: model çağrısı yok. Sahte yerel uç → CC isteği nereye gidiyor, hangi kimlik başlığıyla?
import http from "node:http";
import { spawnSync, spawn } from "node:child_process";
import { kullaniciEnv } from "../../tools/cc-kopru/kos.mjs";
import { OMNI_COMBO, ajanOrtami } from "../../tools/cc-kopru/omniroute.mjs";

const taban = Object.fromEntries(Object.entries(process.env).filter(([k]) => !/^(CLAUDECODE|CLAUDE_CODE_(CHILD|MESSAGING|SESSION|ENTRYPOINT|EXECPATH)|CLAUDE_PID)/.test(k)));
const r = ajanOrtami(taban, { apiKredi: false, omni: true, oku: (ad) => process.env[ad] || kullaniciEnv(ad) });
if (r.eksik) { console.log("eksik:", r.eksik); process.exit(1); }
const gelen = [];
const srv = http.createServer((q, s) => {
  gelen.push({ yol: q.url, bearer_dogru: q.headers.authorization === `Bearer ${r.sir}`, baska_auth: !!q.headers.authorization && q.headers.authorization !== `Bearer ${r.sir}`, x_api_key: "x-api-key" in q.headers });
  s.writeHead(400, { "content-type": "application/json" });
  s.end('{"type":"error","error":{"type":"invalid_request_error","message":"teshis"}}');
}).listen(0, "127.0.0.1", () => {
  const env = { ...r.env, ANTHROPIC_BASE_URL: `http://127.0.0.1:${srv.address().port}` };
  const exe = "C:/Users/pc/.local/bin/claude.exe";
  const durum = spawnSync(exe, ["auth", "status"], { env, encoding: "utf8", timeout: 30000, windowsHide: true });
  console.log("auth status:", `${durum.stdout}${durum.stderr}`.split(r.sir).join("***").replace(/\s+/g, " ").slice(-400));
  const p = spawn(exe, ["--settings", JSON.stringify({ env: { ANTHROPIC_BASE_URL: env.ANTHROPIC_BASE_URL } }), "-p", "--model", OMNI_COMBO, "--disable-slash-commands", "--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}',
    ...process.argv.slice(2)], { env, windowsHide: true });
  let c = "";
  p.stdout.on("data", (d) => (c += d)); p.stderr.on("data", (d) => (c += d));
  p.stdin.end("TAMAM yaz");
  const t = setTimeout(() => p.kill(), 90000);
  p.on("close", () => {
    clearTimeout(t); srv.close();
    console.log("cikti:", c.split(r.sir).join("***").replace(/\s+/g, " ").slice(-400));
    console.log("gelen istek:", JSON.stringify(gelen.slice(0, 5)), "toplam", gelen.length);
  });
});
