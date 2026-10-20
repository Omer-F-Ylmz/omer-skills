# ornek-thinking-orbs — açık kaynak örnek (Jakubantalik/thinking-orbs, MIT; canlı: orbs.jakubantalik.com)

**Durum: KISMİ.** Canlı site probu boş döndü: canvas 0, WebGL/2D çağrı 0, ağ'da script yanıtı 0, getAnimations 0, scroll yüksekliği 720 → sayfa headless'ta içerik üretmedi (muhtemelen istemci render/algılama); mekanizma kanıtı runtime'dan alınamadı.
**Mekanizma (yalnız yerel README'den)**: düz 2D canvas'ta noktalı "düşünme küresi", 9 elle ayarlı durum, her biri iki boyutta; WebGL/filtre yok (kanıt: uygulamalar/thinking-orbs/README.md l.3 "rendered on a plain 2D canvas — no WebGL, no filters"). Kaynak: src/components/ThinkingOrb.tsx, presets.ts, theme.ts (açılmadı).
**Yeniden kurulum farkı**: yapılmadı (ölçülemedi); sayı yok.
**Ders → tersine**: probun "içerik yok" durumunu yakalaması gerekir (canvas+script+animasyon hepsi 0 ise `--bekle` artır / etkileşim tetikle, ya da kaynak depodan oku); bu not o kuralın kanıtı.
