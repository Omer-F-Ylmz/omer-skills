const path = require('path');
const { spawn } = require('child_process');
const kok = path.join(path.dirname(process.execPath), 'node_modules', 'rea-agents', 'scripts', 'rea.mjs');
const p = spawn(process.execPath, [kok, 'mcp'], { env: { ...process.env, REA_MCP_INPUT_SCHEMA_PROFILE: 'compact', REA_MCP_OUTPUT_SCHEMA_PROFILE: 'off' } });
let buf = '';
const gonder = (m) => p.stdin.write(JSON.stringify(m) + '\n');
p.stdout.on('data', (d) => {
  buf += d.toString();
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const s = buf.slice(0, i); buf = buf.slice(i + 1);
    let m; try { m = JSON.parse(s); } catch { continue; }
    if (m.id === 1) { gonder({ jsonrpc: '2.0', method: 'notifications/initialized' }); gonder({ jsonrpc: '2.0', id: 2, method: 'tools/list' }); }
    else if (m.id === 2) {
      const t = m.result.tools;
      const sayac = {};
      for (const x of t) for (const k of Object.keys(x.inputSchema || {})) (sayac[k] = sayac[k] || []).push(x.name);
      for (const [k, v] of Object.entries(sayac)) console.log(k, v.length, v.length <= 5 ? v.join(',') : ''); console.log('reduced:', t.filter(x => /reduced form/.test(x.inputSchema.description || '')).map(x => x.name + (x.inputSchema.minProperties ? '[minP]' : '')).join(','));
      p.kill(); process.exit(0);
    }
  }
});
gonder({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: '2025-06-18', capabilities: {}, clientInfo: { name: 'anahtar', version: '1' } } });
setTimeout(() => { console.log('zaman asimi'); p.kill(); process.exit(1); }, 60000);
