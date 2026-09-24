# threejs-spiral-gallery
ad: threejs-spiral-gallery
tur: uygulama
video: JfmAm3sxCSc
repo: YildizDikme/3D-threejs-spiral-gallery
lisans: yok
son_commit: 2026-05-12
arsiv: hayır
kaynak: yok
telemetri: yok

## Ne
Claude Code'a (Opus 4.7) tek promptla ürettirilen, Three.js+GLSL 3D sarmal (helezon) görsel galerili, Lenis+GSAP ScrollTrigger'lı vanilla JS stüdyo landing page demosu. Vite ile geliştirilir, Netlify'da yayında. npm registry'de paket değil, klonlanıp çalıştırılan kaynak-kod demosu (`package.json` adı `lumen-practice`, `private:true`).

## Kanıt
19 yıldız · son push 2026-05-12 · lisans yok (LICENSE dosyası yok, GitHub `licenseInfo` null) · arşiv değil · SkillSpector koşulmadı (tür skill değil).

## Kurulum
(boş — README'deki kurulum `cd 3D-threejs-spiral-gallery` + `npm install` + `npm run dev` üç ayrı komut; tek-komut kısıtına uymuyor, ayrıca npm registry'de yayımlı bir paket değil. Gerekçe İzinler'de.)

## İzinler
Kurulum serbest metin/çoklu-komut gerektiriyor, yasaklı kalıba giriyor; bu yüzden Kurulum boş bırakıldı. Ek izin talebi yok (yerel dev sunucusu, ağ/hesap gerekmiyor).

## Duman testi
(uygulanamaz — npm registry paketi/CLI/MCP/plugin değil.)

## Geri alma
(uygulanamaz — kurulum yapılmadı.)

## Köprü izni
(uygulanamaz — köprüden çağrılacak bir CLI/MCP değil.)

## Önerilen katman
RED (kurulum) — repo lisanssız (14a T1 kapsamı dışı) ve npm paketi değil, kurulacak bir "araç" yok. İçerik tarafında: temel mekanizma (helezon galeri, kaydırma hız itkisi, kamera paralaksı, bento galeri hover, film gren overlay) zaten skills/web-sahne-desenleri §1/§2c'de satır satır kayıtlı (ZATEN VAR) — bkz. Özellikler.

## Telemetri kapatma
(yok — telemetri: yok; yerel Vite dev sunucusu, dış servise veri göndermiyor.)

## Özellikler

### helezon-galeri-3d
ne: BufferGeometry ile kavisli karo (curved tile) halkalarından kurulu dikey 3D sarmal galeri; Lenis kaydırma hızı sarmala ek dönüş itkisi verir, kamera Y ekseninde kaydırma ilerlemesine lerp'le bağlı, masaüstünde fare X/Z eğim paralaksı var.
kurulum: script.js'te tek `CONFIG` nesnesi (totalImages, tilesPerRevolution, revolutions, startRadius/endRadius, tileSegments:24, spiralGap, rotationDecay:0.9, scrollRotationMultiplier, parallaxStrength:0.1); `requestIdleCallback` ile LCP sonrası kurulur, dokular yüklenince `is-ready` sınıfıyla opaklık geçişi.
lisans: yok
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: skills/web-sahne-desenleri §2c (Helezon galeri + kaydırma hızı itkisi) — kavisli BufferGeometry karo/24 segment, taban hız + Lenis velocity×katsayı itkisi ×0.9 sönüm, kamera Y lerp + ±0.1 rad fare paralaksı, requestIdleCallback ile LCP sonrası kurulum, `is-ready` opaklık geçişi satır satır aynı; bu repo o desenin kaynaklarından biri ya da birebir eşdeğeri.

### bento-galeri-hover
ne: Hero altındaki 12 kolonlu bento galeri (7/5, 8/4 span; 4:5, 16:10 oran) kartlarında hover'da görsel `scale(1.04)→scale(1)` + `brightness(0.78)→1`, 1.2s cubic-bezier geçiş.
kurulum: styles.css `.field__card img` / `.field__card:hover img` kuralları; ek kütüphane yok, salt CSS.
lisans: yok
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: skills/web-sahne-desenleri §1 "Galeri: 12 kolon bento... Hover: görsel 1.04→1 ölçek + parlaklık 0.78→1, 1.2 s" — sayı sayı aynı.

### film-gren-overlay
ne: Tüm sayfayı kaplayan, SVG `feTurbulence` tabanlı düşük opaklıkta film grenli doku katmanı (`.grain`, `aria-hidden`, `pointer-events:none`).
kurulum: index.html'de `<div class="grain">`; styles.css'te SVG data-URI `feTurbulence` filtresi.
lisans: yok
etiket: teknik
karar: ZATEN VAR
gerekce: zaten var: skills/web-sahne-desenleri §1 "%6-8 opak SVG gren... yüzeyi zenginleştirir, pointer-events: none" — aynı teknik.

### gsap-scroll-reveal-hmr
ne: Hero altındaki her `.reveal-text` bloğu kendi ScrollTrigger'ıyla fade+translateY(50→0) açılır (`once:true`); tüm trigger'lar `gsap.context()` içinde toplanıp Vite `import.meta.hot.dispose` kancasına bağlanır, aksi halde her kayıtta trigger çoğalır.
kurulum: script.js — `gsap.context(fn)`, `revealCtx.revert()` dispose'ta.
lisans: yok
etiket: teknik
karar: UYARLA
fikir: Vite tabanlı GSAP/ScrollTrigger sahnelerinde `gsap.context()` + `ctx.revert()`'i `import.meta.hot.dispose`'a bağlamak, HMR'de tekrarlayan trigger birikimini önler.
hedef: skills/web-sahne-desenleri (§1 editoryal dil / Vite+GSAP kurulum notu)
etki: yalnız dev deneyimi (konsol/performans gürültüsü azalır); prod build'de etkisiz, token kazancı yok.
kapsam: fikir notu; kod bu dalgada yazılmaz.

## Mekanizma

### helezon-galeri-3d
nasıl: Sarmal, düz plane değil sin/cos eğrisiyle bükülmüş `BufferGeometry` şerit karolardan kurulur (segments=24); her karo kendi `ShaderMaterial`'ı ile GLSL'de kenar vinyeti + kameraya uzaklığa göre derinlik solması + soğuk-sıcak ton karışımı uygular. Kaydırma hızı (Lenis `onScroll` velocity) her karede sarmala ek açısal itki verir, bu itki `rotationDecay=0.9` ile katlanarak söner — sabit iskelet (CONFIG, geometri, shader) hiç değişmez, yalnız dönüş/kamera durumu (`state`) her karede yeniden hesaplanır, orijinal veriye (doku, CONFIG) dokunulmaz.
neden: Token kazandırmaz; "teknik" — kaydırma-tepkili 3D sahne kurmak için önceden doğrulanmış, ölçülmüş bir tarif verir, sıfırdan prompt'la aynı sonucu üretmek çok tur/deneme ister.
koşul: WebGL bağlamı yoksa (context kaybı, eski cihaz) düşer; skill'in §3 kalite kapısındaki "reduced-motion + IntersectionObserver ile duraklatma" bu repoda YOK (script.js'te ne `matchMedia('(prefers-reduced-motion)')` ne `IntersectionObserver` var) — kazanç yalnız kalite kapısı ayrıca uygulanırsa tam geçerli.
bizde: skills/web-sahne-desenleri §2c zaten bu deseni taşıyor; ek araç/skill kurulmuyor, yalnız kalite-kapısı eksikliği not düşüldü.

### bento-galeri-hover
nasıl: CSS `transform: scale(1.04)` varsayılan, `:hover`'da `scale(1)`e döner (1.2s cubic-bezier) — sıkıştırma yok, saf görsel durum geçişi.
neden: Teknik (UI mikro-etkileşimi); JS'siz, tek CSS kuralıyla "derinlik" hissi verir.
koşul: Dokunmatik cihazda hover olayı yok — statik `scale(1.04)` kalır (bilinen sınır, repo bunu ayrıca ele almıyor).
bizde: skills/web-sahne-desenleri §1 zaten aynı sayılarla (1.04→1, 0.78→1, 1.2s) kayıtlı.

### film-gren-overlay
nasıl: SVG `feTurbulence` (fractalNoise) + `feColorMatrix` ile üretilen gürültü dokusu, data-URI arka plan olarak tüm sayfaya `pointer-events:none`, düşük opaklıkla bindirilir — çalışma zamanında hesap yok, tek statik SVG.
neden: Teknik; JS/GPU maliyeti sıfıra yakın, editoryal/"prodüksiyon" hissi ucuza eklenir.
koşul: Yüksek opaklıkta okunabilirliği bozar; repo zaten düşük opaklık kullanıyor.
bizde: skills/web-sahne-desenleri §1 zaten aynı deseni (%6-8 opak SVG gren) taşıyor.

### gsap-scroll-reveal-hmr
nasıl: Her reveal öğesi ayrı `ScrollTrigger` alır (`start:'top 80%'`, `once:true`); tüm trigger'lar `gsap.context()` kapsamında toplanır, Vite `import.meta.hot.dispose` tetiklendiğinde `ctx.revert()` çağrılır ve trigger'lar temizlenir — prod build'de HMR yok, bu kod dalı etkisiz kalır.
neden: Teknik; token kazandırmaz, dev-deneyimi iyileştirir (kayıt-kayıt tekrarlayan trigger birikimini önler).
koşul: Yalnız Vite dev sunucusunda anlamlı; prod'da fark yaratmaz, HMR kullanmayan build sistemlerinde uygulanamaz.
bizde: Henüz kayıtlı değil; UYARLA fikri olarak not düşüldü, ayrı araç/skill kurulmadı.

## Bağımsız kanıt
- https://stately-naiad-8f0d7f.netlify.app/ — WebFetch başarısız oldu (API 400; WebGL-ağırlıklı sayfa muhtemelen anlamlı statik HTML vermiyor), doğrulama doğrudan kaynak koddan yapıldı (script.js/shaders.js/styles.css).
- Küçük kişisel demo (19 yıldız, tek commit geçmişi, fork/PR yok) — bağımsız blog/inceleme bulunamadı; ek arama (2/3 kalan bütçe) düşük beklenen değer nedeniyle yapılmadı.

## İddia sınama
| iddia | kaynak | sonuç | not | kart |
|---|---|---|---|---|
| Three.js bölümü (CONFIG, sahne/kamera/renderer, createCurvedTileGeometry, buildSpiral) tamamen otomatik üretildi, dokunulmadı | docs/video-tarama/2026-09-24-JfmAm3sxCSc.md (6:37) | doğrulanamadı | video anlatımı/ekran metni; repo tek "main" dalı, PR/diff geçmişi yok, bu iddiayı ne doğrular ne çürütür | - |
| gsap.context()+ctx.revert() Vite import.meta.hot.dispose kancasına bağlandı | docs/video-tarama/2026-09-24-JfmAm3sxCSc.md (6:37) | doğru | script.js satır 103-133'te birebir görülüyor | - |
| Galeri görselinde hover'da görsel "yavaşça geriye gidiyor" (8:09) | docs/video-tarama/2026-09-24-JfmAm3sxCSc.md (8:09) | abartılı | Kod, gerçek z-translate/geri kayma değil; styles.css'te yalnız `scale(1.04→1)` + parlaklık geçişi var — küçülme "geri gitme" hissi verir ama gerçek derinlik/translate yok | bento-galeri-hover |
| CONFIG dosyasında görsel sayısı/hız gibi genel ayarlar tek yerden değişir (4:02, merkezi-config.md İddia sınama satırı) | https://github.com/YildizDikme/3D-threejs-spiral-gallery/blob/main/src/script.js | doğru | script.js başında tek `CONFIG` nesnesi 17 alanla (totalImages, revolutions, startRadius/endRadius, rotationDecay, parallaxStrength, vb.) tüm görsel/hareket parametrelerini topluyor | merkezi-config |
| Hover'da geri kayma efektini Claude prompt'ta istenmeden kendiliğinden ekledi | docs/video-tarama/2026-09-24-JfmAm3sxCSc.md (8:09) | doğrulanamadı | Repo tek/squash commit geçmişi; prompt-öncesi/sonrası diff yok, iddia doğrulanamaz | - |
