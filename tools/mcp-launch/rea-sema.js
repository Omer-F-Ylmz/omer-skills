// KUCUK-6: rea-agents mcp stdio sarmalayıcısı. compare_web_captures inputSchema'sı 166 KB / derinlik 31 / 226 anyOf;
// Desktop "problem with that connector" ile reddediyor. tools/list yanıtında yalnız o şemayı sadeleştirir; geri kalan akış aynen geçer.
// Çağrı doğrulamasını sunucu kendi yapar, sadeleştirme yalnız istemciye giden şemayı etkiler.
const cp = require('child_process');
const path = require('path');
const readline = require('readline');

const NODE_KOK = path.dirname(process.execPath);
const betik = path.join(NODE_KOK, 'node_modules', 'rea-agents', 'scripts', 'rea.mjs');
const ch = cp.spawn(process.execPath, [betik, 'mcp'], { stdio: ['pipe', 'pipe', 'inherit'], windowsHide: true });

process.stdin.pipe(ch.stdin);
const SADE = ['before', 'after', 'before_scenario', 'after_scenario', 'normalization'];
function sadelestir(t) {
  const aciklama = t.inputSchema.description;
  const props = {};
  for (const k of SADE) props[k] = { type: 'object', description: (t.inputSchema.properties[k] || {}).description || k };
  t.inputSchema = { type: 'object', description: aciklama, properties: props, additionalProperties: false };
}
readline.createInterface({ input: ch.stdout }).on('line', l => {
  try {
    const m = JSON.parse(l);
    const c = m.result && Array.isArray(m.result.tools) && m.result.tools.find(t => t.name === 'compare_web_captures');
    if (c) { sadelestir(c); l = JSON.stringify(m); }
  } catch (e) {}
  process.stdout.write(l + '\n');
});
for (const s of ['SIGTERM', 'SIGINT', 'SIGHUP']) process.on(s, () => { try { ch.kill(s); } catch (e) {} });
ch.on('exit', code => process.exit(code == null ? 0 : code));
