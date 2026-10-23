// REA-FIX-2: ~/.claude.json rea girdisini Desktop ile aynı kurulu yola çevirir (npx önbelleği yamayı taşımaz). env değerleri dokunulmaz/yazdırılmaz.
const fs = require('fs'), path = require('path'), os = require('os');
const y = path.join(os.homedir(), '.claude.json');
const ham = fs.readFileSync(y, 'utf8');
const j = JSON.parse(ham);
const betik = path.join(path.dirname(process.execPath), 'node_modules', 'rea-agents', 'scripts', 'rea.mjs').replace(/\\/g, '/');
let n = 0;
const gez = (o) => {
  if (!o || typeof o !== 'object') return;
  for (const [k, v] of Object.entries(o)) {
    if (k === 'mcpServers' && v && v.rea) {
      v.rea.command = process.execPath.replace(/\\/g, '/');
      v.rea.args = [betik, 'mcp'];
      n++;
    } else gez(v);
  }
};
gez(j);
if (!n) { console.log('rea girdisi yok'); process.exit(0); }
fs.writeFileSync(y + '.bak-rea2', ham);
const tmp = y + '.tmp-rea';
fs.writeFileSync(tmp, JSON.stringify(j, null, 2));
JSON.parse(fs.readFileSync(tmp, 'utf8'));
fs.renameSync(tmp, y);
console.log('guncellendi', n, 'girdi');
