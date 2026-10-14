# lab · SplitText + dev tip/3B katmanlama (ref lando · eşleşme 9)
Demo `labs/metin/` · modül `tools/site-kit/sablon/src/sahne/metin.js`.
- Mekanizma: dev başlık (25vw) DOM'da, saydam WebGL kanvası üstünde (z-index 1, pointer-events none) → 3B nesne tipin önünden geçer; SplitText chars/lines + ScrollTrigger girişleri.
- Parametre: harf `yPercent 110→0`, expo.out, stagger 0.035–0.05; dev tip parallax `yPercent -35`.
- Bütçe: talep üzerine render → boşta 0 kare/sn.
- Tuzak: `mix-blend-mode: difference` küçük metinde kontrastı sahneye bağlar (WCAG düşer) → yarı saydam koyu zemin + açık metin. Linter kök yollu (`/labs/ortak.css`) stylesheet'i çözemez → arka planı elemanda açık yaz.
- Mobil düşüş (önerilen, uygulanmadı): SplitText yalnız `lines`.
- Lisans: GSAP 3.15 + SplitText "standard no-charge license" (MIT değil) — ücretsiz, ticari kullanım serbest; GSAP'a rakip ürün/araçta yasak. Teslimde koşul not edilir.
