# lab · post yığını (ref lusion · eşleşme 9)
Demo `labs/post/` · modül `tools/site-kit/sablon/src/sahne/post.js` (`kademe` 'yuksek'/'dusuk').
- Mekanizma: pmndrs postprocessing EffectComposer (HalfFloat, yüksekte MSAA 4) → Bloom + DoF + kromatik + gren (Noise) + vinyet + ToneMapping.
- Parametre: bloom eşik 0.7, yoğunluk 1.4; vinyet ofset 0.3; kromatik ofset 0.0015; gren opaklık 0.35.
- Bütçe: 60 fps yüksek ve düşük kademede (masaüstü); düşük kademe yalnız bloom + vinyet, MSAA yok.
- Tuzak: DoF ile kromatik aynı EffectPass'e girmez (konvolüsyon çakışması) → iki pass. RT'ye çizerken renderer ton eşlemesi uygulanmaz → ToneMappingEffect şart, yoksa sahne soluk/aşırı parlak.
- Mobil düşüş: `postYigini(r, s, kam, 'dusuk')`.
- Lisans: postprocessing Zlib (serbest).
