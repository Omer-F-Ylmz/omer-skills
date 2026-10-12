# ANİMASYON-1 aday tablosu (d3, 12 Eki)

Kaynak: docs/video-tarama raporlarında geçme sayısı (grep, md) + bilinen lisans/bakım. Karar: KUR (araç/tarif olarak kullanılır) · UYARLA (mekanizma tarife alındı) · REF (ayrı skill/elle kullanım) · RED (çift ya da lisans). Lisans "doğrula" yazanlar kurulumdan önce repo LICENSE'ından teyit edilir.

| aday | geçme | lisans | karar | gerekçe |
|---|---|---|---|---|
| View Transitions API | — | tarayıcı yerlisi | UYARLA | `sayfa-gecisi.html`; barba.js gereksiz |
| CSS/IntersectionObserver giriş-scroll | — | yerli | UYARLA | `giris-scroll.html`; bağımlılık yok |
| three.js parçacık | — | MIT | UYARLA | `parcacik-three.html` (CDN importmap) |
| ffmpeg drawtext/fade | — | LGPL/GPL | KUR | `video_intro.py`; kurulu |
| Blender keyframe + glTF anim dışa aktarım | — | GPL (Blender) | KUR | `blender_patlat.py` (-b), TELVE exploded |
| Remotion | 1600 | Remotion lisansı (≥4 kişi şirket ücretli) | REF | çok sahneli video → remotion-video-paket |
| hyperframes | 867 | Apache-2.0 (gh, 12 Eki aktif) | REF | hyperframes-paket mevcut |
| GSAP (+ScrollTrigger/SplitText) | 707/150 | GSAP no-charge (OSI değil) | REF | karmaşık zaman çizelgesi → animasyon-scroll-paket |
| Cascadeur | 649 | tescilli (masaüstü kurulu) | REF | karakter animasyonu elle; CLI yok |
| Motion / framer-motion | 555 | MIT | REF | yalnız React projesinde |
| Lenis | 200 | MIT | REF | smooth scroll; scroll-craft içinde |
| Spline | 131 | tescilli SaaS | RED | bulut editörü, kod kontrolü yok |
| Lottie / dotLottie | 125 | MIT | REF | tasarımcıdan gelen JSON animasyon oynatma |
| Rive | 113 | runtime MIT, editör tescilli | REF | etkileşimli durum makinesi gerekirse |
| Mixamo | 79 | Adobe ToS (web) | REF | rig+hareket elle indirilir, otomasyon yok |
| Rigify / auto-rig | 26 | GPL (Blender yerleşik) | KUR (sıradaki tarif) | Blender'da yerleşik; bpy ile etkinleştirilir |
| Theatre.js | — | repo Apache-2.0 (gh); studio paketi AGPL (doğrula) | REF | 3D sahne kurgusu; son push 2024-08 → bakım zayıf |
| Motion Canvas | — | MIT | RED | Remotion/hyperframes ile çift |
| anime.js | 20 | MIT | RED | GSAP/CSS ile çift |
| barba.js | 9 | MIT | RED | View Transitions yerlisi yeter |
| tsParticles | — | MIT | RED | three tarifi yeter, ek bağımlılık |

Sıradaki tarif adayları (ölçüm KABUL olursa): Blender rigid body/cloth bake → GLB, Rigify otomatik rig, GSAP ScrollTrigger pin tarifi (animasyon-scroll-paket'le çakışmadan).
