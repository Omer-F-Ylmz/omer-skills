# kombin-2 — sahne/animasyon zinciri (ÖĞREN-2 d3, G1; d3'te yeniden koşuldu)
- İş türü: three.js sahnesi + scroll/giriş animasyonu + azaltılmış hareket. Dosyalar: lab\frontend\kombin\k2\
- Zincir: (1) build.mjs esbuild ile r.js/v.js paketleme (three r186 npm; CDN yok) → (2) r.html/v.html → (3) run.mjs playwright headless: WebGL renderer + piksel rengi örnekleme, animasyonlu öğe stili ölçümü normal ve `prefers-reduced-motion: reduce` altında, Lenis başlatma bayrağı.
- Hangi projede hangisi: React'siz = düz three + Lenis + Motion/CSS (bu koşu); React'li = R3F + `motion/react`. React'li dal d3'te DENENMEDİ.
- Devir noktaları: build çıktısı tek bundle dosyası; run.mjs satırları `THREE|V|MOTION|ERR` önekli (log parse edilir, görüntü okunmaz).
- KOŞU KANITI (d3, `node run.mjs`): `THREE {"rev":"186","renderer":"WebGL 2.0 (OpenGL ES 3.0 Chromium)"}` · `THREE distinct colours 4` · `V reduce {"lenis":false}` (azaltılmış harekette Lenis başlamıyor) · `MOTION normal 0.38|matrix(1, 0, 0, 1, 0, 12.3304) -> 1|none` (giriş animasyonu opaklık 0,38→1, translateY 12,3→0) · `MOTION reduced 1|none -> 1|none` (animasyon yok) · `ERR -` (konsol hatası 0).
- Token-verimli: tek run.mjs, 5 satır çıktı; sahne için ekran görüntüsü gerekmez (renk sayısı + renderer).
- Desktop/CC: build + ölçüm = CC; sahne estetiği (kamera, ışık, ritim) = Desktop bakışı. GSAP ScrollTrigger dalı bu koşuda YOK (denenmedi); gsap-frameworks / cinematic-gsap-lenis-motion-system kartlarının kuralları (ctx.revert, plugin bir kez kayıt) kaynak okumasından, koşulmadı.
- Tuzak: headless WebGL yazılım renderer'ı (SwiftShader) olabilir → performans ölçümü temsilî değil; `distinct colours 4` yalnız "boş değil" kanıtıdır.
