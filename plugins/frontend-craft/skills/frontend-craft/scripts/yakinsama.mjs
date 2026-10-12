// Koşular arası yakınsama: AI'nın yeni slop imzası aynı brief'e (ve farklı brief'lere) hep aynı font/zemin/düzeni seçmesi.
// Kullanım:
//   node scripts/yakinsama.mjs <slop.json> <slop.json> ...  → font/zemin/düzen tekrar oranı (eş çiftlerin payı, 0 = hepsi farklı, 1 = hepsi aynı)
//   node scripts/yakinsama.mjs --gecmis                     → son 5 projenin imzası (slop.mjs her koşuda proje klasörü başına bir satır yazar)
// Geçmiş dosyası: FC_GECMIS ortam değişkeni ya da ~/.claude/frontend-craft/gecmis.tsv
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const GECMIS = () => process.env.FC_GECMIS || path.join(os.homedir(), '.claude', 'frontend-craft', 'gecmis.tsv');
const fam = f => f.toLowerCase().replace(/^__|_[0-9a-f]{6}$/g, '').replace(/_/g, ' ').trim();

// zemin sınıfı: açıklık + ton ailesi (krem #f1e9dc → "açık-sıcak")
export const zemin = h => {
  const [r, g, b] = [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16) / 255);
  const mx = Math.max(r, g, b), mn = Math.min(r, g, b), l = (mx + mn) / 2, d = mx - mn;
  const ac = l >= .8 ? 'açık' : l < .25 ? 'koyu' : 'orta';
  if (d < .02 || d / (1 - Math.abs(2 * l - 1)) < .12) return `${ac}-nötr`;
  const hue = (mx === r ? ((g - b) / d + 6) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4) * 60;
  return `${ac}-${hue < 75 || hue >= 330 ? 'sıcak' : hue < 165 ? 'yeşil' : hue < 270 ? 'soğuk' : 'mor'}`;
};

export const imza = d => ({
  font: [...new Set((d.fontsUsed || []).map(fam))].sort(),
  zemin: zemin(d.bg),
  duzen: `${d.heroCentered ? 'ortalı' : 'sola'} hero, ${d.cards3 > 0 ? 'kart satırı' : 'kartsız'}`,
});

// eş çift payı; font için iki koşu ortak bir aile paylaşıyorsa eş sayılır
export const oran = imzalar => {
  const es = { font: (a, b) => a.some(f => b.includes(f)), zemin: (a, b) => a === b, duzen: (a, b) => a === b };
  const n = imzalar.length, cift = n * (n - 1) / 2, o = {};
  for (const k of Object.keys(es)) {
    let say = 0; for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (es[k](imzalar[i][k], imzalar[j][k])) say++;
    o[k] = cift ? Math.round(say / cift * 100) / 100 : 0;
  }
  o.toplam = Math.round((o.font + o.zemin + o.duzen) / 3 * 100) / 100;
  return o;
};

// slop.mjs çağırır: proje klasörü (cwd) başına tek satır, en yeni sonda
export const gecmisYaz = (d, anahtar = process.cwd()) => {
  const f = GECMIS(), s = imza(d);
  const satirlar = fs.existsSync(f) ? fs.readFileSync(f, 'utf8').split('\n').filter(x => x && x.split('\t')[1] !== anahtar) : [];
  satirlar.push([new Date().toISOString().slice(0, 10), anahtar, s.font.join(', '), s.zemin, s.duzen].join('\t'));
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, satirlar.slice(-50).join('\n') + '\n');
};

export const gecmisOku = (n = 5) => {
  const f = GECMIS();
  return fs.existsSync(f) ? fs.readFileSync(f, 'utf8').split('\n').filter(Boolean).slice(-n).map(x => x.split('\t')) : [];
};

if (process.argv[1]?.endsWith('yakinsama.mjs')) {
  const arg = process.argv.slice(2);
  if (arg[0] === '--gecmis') {
    const g = gecmisOku();
    if (!g.length) console.log('geçmiş yok');
    for (const [t, k, font, z, du] of g) console.log(`${t} · ${path.basename(k)} · font: ${font} · zemin: ${z} · ${du}`);
    process.exit(0);
  }
  if (arg.length < 2) { console.error('kullanım: node yakinsama.mjs <slop.json> <slop.json>... | --gecmis'); process.exit(2); }
  const imzalar = arg.map(a => imza(JSON.parse(fs.readFileSync(a, 'utf8')).d));
  for (const [i, s] of imzalar.entries()) console.log(path.basename(path.dirname(path.resolve(arg[i]))), '·', s.font.join(', '), '·', s.zemin, '·', s.duzen);
  console.log('YAKINSAMA', JSON.stringify(oran(imzalar)));
}
