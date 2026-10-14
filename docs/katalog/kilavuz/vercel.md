# vercel — 6 benzersiz kayıt

**Amaç:** Vercel ve React ekosistemi rehberleri: Vercel deploy/env değişkeni, maliyet-performans optimizasyonu, React/RN en iyi uygulamaları, kompozisyon kalıpları, view transitions.

**İç yapı:** Tümü [skill], vercel-<konu>; platform (cli-with-tokens, optimize) ve React kalıpları (react-best-practices, composition-patterns, react-native-skills, react-view-transitions).

## En güçlü parçalar
- `vercel-react-best-practices` — Bileşen, veri çekme, bundle boyutu, performans yazım/inceleme.
- `vercel-composition-patterns` — Boolean prop çoğalmasını giderip esnek bileşen API'si kurmak.
- `vercel-optimize` — Next.js/SvelteKit/Nuxt/Astro için metrik/kullanım toplayıp maliyet-performans.
- `vercel-cli-with-tokens` — Vercel'e deploy, kurulum ve env değişkeni ekleme.

## Birlikte kullanım
- vercel-react-best-practices + vercel-composition-patterns.
- vercel-react-native-skills + expo-plugins ailesi.

## Tuzaklar
- vercel-cli-with-tokens token ister; Vercel hesap/ücret katalog metninde belirtilmemiş.
- vercel-react-view-transitions Next.js'e özel.

## Üyeler
- skill (6): vercel-cli-with-tokens, vercel-composition-patterns, vercel-optimize, vercel-react-best-practices, vercel-react-native-skills, vercel-react-view-transitions
