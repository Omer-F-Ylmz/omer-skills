import fs from 'node:fs';
import { PNG } from '../w/node_modules/pngjs/lib/png.js';
import pixelmatch from '../w/node_modules/pixelmatch/index.js';
const A = PNG.sync.read(fs.readFileSync('yon-a.png'));
for (const t of ['ref','t1','t2','t3','t4']) { const B = PNG.sync.read(fs.readFileSync(`r-${t}.png`)); console.log(t, +(pixelmatch(A.data, B.data, null, 1440, 900, {threshold:0.1})/(1440*900)*100).toFixed(2)); }
