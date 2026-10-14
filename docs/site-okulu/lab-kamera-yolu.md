# lab · sürekli kamera yolu (ref igloo · eşleşme 8)
Demo `labs/kamera-yolu/` · modül `tools/site-kit/sablon/src/sahne/kamera-yolu.js` (+ `dongu.js` talep üzerine render).
- Mekanizma: CatmullRomCurve3 konum yolu + ayrı bakış yolu; ScrollTrigger ilerlemesi (Lenis yumuşatmalı) → `getPointAt(u)`; kamera yalnız ilerleme değişince çizilir.
- Parametre: konum ve bakış ayrı eğri → dönüşler yumuşar; FogExp2 0.05 derinlik verir.
- Bütçe: talep üzerine render → boşta 0 kare/sn; kaydırırken 60 fps (RTX 4070 Ti, d3d11).
- Tuzak: `getPoint` (eşit parametre) hız dalgalandırır, `getPointAt` (yay uzunluğu) kullan; `lookAt` her kare yeniden hesaplanır, up vektörü sabit kalmalı.
- Mobil düşüş (önerilen, uygulanmadı): DPR ≤1.5, sis yoğunluğu ↑.
- Eksik (Gemini): referansta atmosferik sis katmanları + holografik ara efektler daha zengin.
