# lenis

- tür: kutuphane · durum: KURULU-KANITSIZ · videolar: 4cE9t4rE0-0,Da3O00jpo3R,Dc1ENsHzNSj,Ddh2J6Zppgb,De64R5emX-i,DePG1srTjBo,DePLcw_Dbwo,DeWQJuHxx4I,Deo4rfIFA5A,Deq1je7DsyF,DevrrJ4jvAK
- bizde: docs/envanter/envanter.tsv; omer-kutuphaneler:docs\katalog\yetenek.tsv; kaynak-kutuphane/envanter:docs/kaynak-kutuphane/kutuphane-haritasi.tsv

## Özellikler
- Smooth scroll kütüphanesi; prompt'ta GSAP ScrollTrigger ile birlikte kullanılıyor
- Kaynak: github.com/darkroomengineering/lenis (fifbuilds videosu)
- Next.js App Router + TypeScript + Tailwind CSS ile responsive site yapımında kullanılıyor
- Scroll ile sürülen (scroll-scrubbed) hero video kullanılıyor

## Videoda yapılış
Claude Code'a verilen prompt: Next.js (App Router) + TypeScript + Tailwind, GSAP ScrollTrigger ve Lenis smooth scroll. Hero video önce ffmpeg ile ALL-KEYFRAME MP4'e kodlanıyor (ters ve ara oynatmada takılmayı önlemek için). Medya public klasöründen kullanılıyor, placeholder kullanılmıyor. Kural (b) ve (c) alıntıda kesik.

## Bizdeki karşılık ve fark
docs/envanter/envanter.tsv; omer-kutuphaneler: docs\katalog\yetenek.tsv; kaynak-kutuphane/envanter: docs/kaynak-kutuphane/kutuphane-haritasi.tsv (içerik doğrulanmadı)

## Al
Scroll-scrub video için all-keyframe MP4 ön kodlaması (ffmpeg); Lenis + GSAP ScrollTrigger eşleşmesi

## At
Kural (b) ve (c) alıntıda kesik, eksik kalıyor. Sürüm ve kurulum bilgisi yok. Scroll-scrub yaklaşımı tek video dosyasına bağımlı
