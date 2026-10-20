# kombin-3 — erişilebilirlik + performans kapısı (ÖĞREN-2 d3, G1; d3'te yeniden koşuldu)
- İş türü: bitmiş sayfayı axe + Lighthouse + hareket performansı ile kapıdan geçirme. Dosyalar: lab\frontend\kombin\k3\
- Zincir: (1) run.mjs: playwright + @axe-core/playwright (wcag2a/aa, 21a/aa, 22aa, best-practice) → (2) aynı oturumda CDP `Performance.getMetrics` 3 sn pencerede LayoutCount/LayoutDuration/RecalcStyle farkı → (3) lh.mjs Lighthouse (performance + accessibility, TBT, CLS, non-composited-animations) → (4) fixing-motion-performance kuralıyla düzelt (page-before: `.glow` width/height animasyonu → page-after: `transform: scale` + `will-change:transform` + `prefers-reduced-motion` ile animation:none).
- Devir noktaları: her adım tek satır (`AXE …`, `MOTION3s …`) ya da JSON; ham Lighthouse JSON (≈270 KB) okunmaz, `jq`/node ile 4 alan çekilir.
- KOŞU KANITI (d3, `node run.mjs before|after`): AXE before/after `violations=0` · MOTION3s before `{"LayoutCount":180,"LayoutDurationMs":9.3,"RecalcStyleCount":180}` → after `{"LayoutCount":0,"LayoutDurationMs":0,"RecalcStyleCount":0}`. Lighthouse (lh-*.json): performance 1 / accessibility 1 iki durumda da; TBT 20 ms → 0 ms; CLS 0; `non-composited-animations` 1 öğe → yok.
- Ölçülmüş kazanç: düzen yeniden hesabı 180 → 0 / 3 sn; sayılarla doğrulandı, ekran görüntüsü gerekmedi.
- Çakışma bulgusu: axe ve Lighthouse a11y skoru bu sayfada ikisi de temiz → tek başına axe yeter; Lighthouse yalnız performans/TBT/CLS için gerekli. Önceki ilk LH denemesi `NO_FCP` hatasıyla düştü (lh-before.log) → sunucu ayakta ve sayfa dolu olmalı; sonraki koşu geçti.
- Desktop/CC: tamamı CC (headless, sayı çıktısı); Desktop yalnız sonucu okur.
- Tuzak: skor 1/1 küçük sayfada; gerçek proje sayfasında (TELVE) denenmedi.
