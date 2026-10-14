# __AD__ — tasarım ve storyboard

## 1. Yön
Tek cümle tez · ton · 2 referans site (neyi alıyoruz). Renk/tip: `src/sayfa.css` :root.

## 2. Storyboard
Her bölüm `src/pages/index.astro` `bolumler` dizisinde bir satır; sahnesi varsa `src/sahne/bolum/<id>.ts` (örnek: `ornek.ts`).

| # | id | boy (vh) | ilk kare (poster) | scroll 0→1 ne olur | etkileşim | reduced-motion karşılığı |
|---|----|----------|-------------------|--------------------|-----------|--------------------------|
| 01 | giris | 200 | | | | |
| 02 | ornek | 240 | | | | bölüm pozuna 0.3 s atlama |

## 3. Varlıklar
- Poster: her bölüm `public/poster-<id>.avif` (yatay) + `-m.avif` (dikey); kanvasın ilk karesi. PNG → AVIF: `ffmpeg -i k.png -c:v libaom-av1 -still-picture 1 -crf 32 public/poster-<id>.avif`.
- 3B model / doku / HDR: `python tools/varlik_getir.py` (omer-skills) · Blender: blender-uretim skill'i.
- Sıvı: `src/sahne/sivi-glsl.js` — TELVE fincanının onBeforeCompile GLSL parçaları (SIVI_ORTAK, SIVI_KES); malzemeye enjekte edilir, uniform sözleşmesi dosya yorumlarında.

## 4. Kapı
`npm run kapi` → build + `kapi.mjs` (Chrome headless; masaüstü · mobil · reduced-motion). Eşikler `kapi.esik.json`: hata 0 · kare p95 · ilk/toplam JS gz. Döküm `kapi.json`. Kapıdan geçmeyen bölüm bitmiş sayılmaz.
