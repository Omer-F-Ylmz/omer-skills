const fs = require('fs');
const path = require('path');
const os = require('os');
const cp = require('child_process');

const kok = path.join(os.homedir(), '.claude', 'plugins', 'cache', 'thedotmack', 'claude-mem');
const surum = n => n.split('-')[0].split('.').map(x => parseInt(x, 10) || 0);
const kars = (a, b) => {
  const x = surum(a), y = surum(b);
  return (y[0] - x[0]) || (y[1] - x[1]) || (y[2] - x[2]);
};
let adaylar = [];
try {
  adaylar = fs.readdirSync(kok)
    .filter(n => /^\d/.test(n))
    .filter(n => !fs.existsSync(path.join(kok, n, '.orphaned_at')))
    .filter(n => fs.existsSync(path.join(kok, n, 'scripts', 'mcp-server.cjs')))
    .sort(kars);
} catch (e) {}
if (!adaylar.length) {
  process.stderr.write('claude-mem: mcp-server.cjs bulunamadi: ' + kok + '\n');
  process.exit(1);
}
const betik = path.join(kok, adaylar[0], 'scripts', 'mcp-server.cjs');
const ch = cp.spawn(process.execPath, [betik], { stdio: 'inherit', windowsHide: true });
for (const s of ['SIGTERM', 'SIGINT', 'SIGHUP']) process.on(s, () => { try { ch.kill(s); } catch (e) {} });
ch.on('exit', code => process.exit(code == null ? 0 : code));
