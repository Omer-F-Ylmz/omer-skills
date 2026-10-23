// REA-FIX-2: rea-agents compact girdi profilinin "reduced" şemasından üst seviye minProperties'i düşürür.
// Yalnız İLAN edilen şema etkilenir; sunucu canonical doğrulamayı korur. Tekrar koşulabilir (npm güncellemesinden sonra).
// Kullanım: node rea_yama.js [kurulu rea-agents dizini]   (varsayılan: node.exe yanındaki node_modules/rea-agents)
const fs = require('fs');
const path = require('path');
const kok = process.argv[2] || path.join(path.dirname(process.execPath), 'node_modules', 'rea-agents');
const dist = path.join(kok, 'dist');
const KALIP = /\n[ \t]*\.\.\.\(?typeof schema\.minProperties === "number"\s*\?\s*\{ minProperties: schema\.minProperties \}\s*:\s*\{\}\)?,/;
const yurut = (d) => {
  for (const ad of fs.readdirSync(d, { withFileTypes: true })) {
    const y = path.join(d, ad.name);
    if (ad.isDirectory()) { if (ad.name !== 'node_modules') yurut(y); continue; }
    if (!/\.(m?js)$/.test(ad.name)) continue;
    const t = fs.readFileSync(y, 'utf8');
    if (!t.includes('reduceToShallowProperties')) continue;
    if (!KALIP.test(t)) { console.log('zaten yamali / kalip yok', path.relative(kok, y)); continue; }
    if (!fs.existsSync(y + '.bak')) fs.writeFileSync(y + '.bak', t);
    fs.writeFileSync(y, t.replace(KALIP, ''));
    console.log('yamalandi', path.relative(kok, y));
  }
};
yurut(dist);
