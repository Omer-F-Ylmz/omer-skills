# TELVE referans çıkarımı (SİTE-TELVE Faz 0, 12 Eki 2026)

Kapsam: üç referansın teknik çıkarımı + TELVE (C:\Users\pc\Desktop\TELVE) envanteri + Faz 1 önerisi. Kod kopyası yok; alıntılar ≤15 kelime. TELVE klasörüne yazılmadı.

## 1. Referans: YouTube ptGXxk1-Uj4 ("Claude Opus 5.5 ile Ödüllü 3D Web Sitesi")
Kaynak: mevcut tarama `docs/video-tarama/2026-09-30-ptGXxk1-Uj4.md` (yeni claude -p koşulmadı).
- **Sahne kurgusu:** Ciao Energy'den esinlenen "Blazing Energy": ortada aydınlık kutu, yanlarda karanlık kutular (vitrin carousel), alt sayaç 05/05, tat seçilince arka plan rengi değişiyor; özellik listesi model dönüşüyle senkron.
- **Teknik:** Sketchfab hazır modeller + codrops-noise-transition (arka plan alev/gürültü) + referans URL'si verilip "Awwwards seviyesi" istenmiş. Asıl ders iş akışı: model tarayıcıda kendi çıktısını adım adım test edip hatayı (Vector3 dizi gibi indekslenmiş → NaN) düzeltiyor.
- **Scroll bağlama:** kaydırmada modeller "rüzgârda eğilir" gibi bükülüyor; ayrıntı videoda yok.
- **Performans:** ölçüm yok; sunucu "ışık patlamaları fazla" diyor; mobilde özellik seçimi alta taşınmış.
- **TELVE'ye uyarlama:** (a) her bölümden sonra headless tarayıcı turu (playwright) zorunlu adım; (b) parça seçimi ↔ HUD metni senkronu (exploded parçaya hover/tık → parça adı/işlevi); (c) bölüm başına renk/ton geçişi.

## 2. Referans: awwwards Ciao Energy (https://www.ciaoenergy.com/, SOTD 30 Tem 2026, Skaald)
Ölçüm: headless python-playwright 1.63 (chromium, swiftshader) + `npx lighthouse` mobil; ham çıktı `.claude/ciao/` (izlenmiyor).
- **Sahne kurgusu:** 11 section + 1 `position:fixed` tam ekran WebGL2 canvas; tek sahnede 6 tatlı kutu carousel'i; scrollHeight 12807 px, Lenis `infinite:true` ile sonsuz scroll.
- **Teknik:** three r161 (jsdelivr importmap, ESM), GSAP 3.15.0 + ScrollTrigger + SplitText, Lenis (`autoRaf:false, syncTouch:true`), Webflow + jQuery 3.5.1. Özel shader yok: MeshPhysicalMaterial'a `onBeforeCompile` ile tint enjeksiyonu. Postprocess: RenderPass → UnrealBloom(0.1,0.1,1) → OutputPass → SMAA; ACESFilmic, HalfFloat RT, HDR (PMREM). Raycaster imleç etkileşimi. Ses: 4 mp3.
- **Scroll bağlama:** scrub YOK (kodda "scrub" 0). Section başına `ScrollTrigger.create({onToggle})` + `toggleActions:'play reverse play reverse'`; tek `data` nesnesi (camPosZ 29, fov 20, canSpin, spacing, wave, swirl, tint…) bölümler arası GSAP ile tween, render döngüsünde lerp. Masaüstü wheel paging (1–1.5 sn), mobil swipe paging; pinning yok.
- **Performans bütçesi (ölçülen):** 73 istek ~5.9 MB; JS 622 KB transfer / 2382 KB decoded (three.module 252 KB); hdri2.hdr 1398 KB, base.glb 608 KB, can.glb 160 KB (Draco/KTX2 yok); 6 avif doku ~190–250 KB; 2 webm 1.2 MB. Draw call (draw* sayaç, 60 kare): masaüstü ~42 intro / ~20 kaydırılmış; mobil 13 / 4. Mobilde varlıklar aynen iniyor; yalnız `lowPower` (iOS ya da <1024 px) basit malzeme.
- **Lighthouse mobil:** Performance 36 · LCP 7.3 sn · TBT 4170 ms · CLS 0.002 · SI 4.5 sn · 5078 KiB. → Görsel olarak "aşırı iyi" ama TELVE kabulünü (LCP < 2.5) karşılamıyor; taklit edilecek olan kurgu ve his, bütçe değil.
- **TELVE'ye uyarlama:** tek fixed canvas + section'lar; tek "sahne durumu" nesnesi + lerp deseni (zaten TELVE sahne.ts'de benzeri var); toggle tween (exploded tetikli) ile scrub'ı karıştırmak; bloom düşük eşikle tek pass; HDR yerine RoomEnvironment/küçük (≤256 px) HDR; glb Draco/Meshopt ile.

## 3. Referans: Codrops noise transition
Makale "Model Texture Transition and Procedural Radial Noise using WebGL" (2 May 2024), repo github.com/mohAmineBrs/codrops-noise-transition, demo tympanus.net/Development/TextureTransition/. Makale sayfası 403 verdi; çıkarım repo kaynağından.
- **Lisans:** GitHub `license: null`, LICENSE dosyası yok (README "MIT" diyor ama bağlantı boş) → kod aynen alınmaz, teknik yeniden yazılır. Model CC-BY-4.0 (Sketchfab, atıf).
- **Sahne kurgusu:** tek GLB kutu + tam ekran arka plan plane'i; tıkla → kutu dokusu dikey "silme" ile yeni renge, arka planda radyal halka yayılır.
- **Teknik:** R3F (three ^0.163, fiber 8, drei 9) + vite 5; tween framer-motion `animate` + d3-ease `easeQuadOut` (GSAP değil). Noise: tek oktav 4D klasik Perlin (Gustavson cnoise). Model: MeshStandardMaterial `onBeforeCompile`, fragment'te `smoothstep` dikey maske + noise, bant genişliği `u_width*parabola(progress)`, sert eşik `smoothstep(1.,1.01,…)`. Arka plan: iki smoothstep çember farkı (halka) + yüksek ölçekli noise noktaları + sin-hash grain.
- **Zamanlama:** model 1 sn, arka plan 2 sn, easeQuadOut; tetik görünmez plane'e tık; zustand ile eşleme.
- **Maliyet:** ~3 draw call; piksel başı 1 adet 4D Perlin (tam ekran + yüzey); DPR sınırı/mobil dalı yok. GLB 1.1 MB, HDR 256 px 101 KB.
- **TELVE'ye uyarlama:** exploded parça malzemelerine aynı fikir (onBeforeCompile maske) ama silme ekseni parçanın ayrılma ekseni; kenara koyu "telve granülü" (yüksek ölçekli noise × hash); arka plandaki radyal halka makine merkezinden "demleme dalgası". 3D Perlin, tek oktav, DPR ≤1.5 ile yeniden yazım. TELVE `dunya.ts` zaten radyal noise arka plan içeriyor → genişletme, ikinci shader değil.

## 4. TELVE envanteri (HEAD 091fa01 "D4.1", 12 commit; salt okuma)
- **Yığın:** Astro ^7.3.5 (entegrasyon yok), three 0.186.1, gsap 3.15.0, lenis 1.3.26, Archivo variable + JetBrains Mono (self-host); size-limit bütçesi giriş 3.1 kB, sahne paketi 190 kB; test `node --test src/sahne/hacim.test.ts`.
- **Yapı:** tek sayfa `pages/index.astro` (S0–S2 + SVG fincan konturu), `bilesenler/Dugme.astro` (ses/hareket aç-kapa), `sahne/`: sahne.ts (motor: tek canvas, scrub timeline, tetikli exploded, WebGL yoksa poster), config.ts (tüm sayılar), kaplar.ts (Lathe fincan/tabak + morph), sivi.ts (espresso/crema shader), akis.ts (dökme + damla), dunya.ts (radyal noise arka plan), exploded.ts (dönüş → bekleme → ayrılma), etkilesim.ts (sürükle-döndür, ok tuşları), hud.ts, kamera.ts, ses.ts (Web Audio sentezi), yukleme.ts (gerçek yüzdeli yükleyici).
- **Animasyon/scroll:** Lenis gsap.ticker'a bağlı (sahne.ts:38-41), tek timeline + scrub ScrollTrigger (sahne.ts:51), reduced-motion anlık poz (sahne.ts:49), IntersectionObserver görünmezken çizim durdurur (sahne.ts:182), ana döngü gsap.ticker.
- **3D varlık:** GLB/glTF/KTX2/doku YOK; tüm geometri kodla. `Blender/*.blend` (4 dosya ~97–99 KB, untracked) kodda kullanılmıyor. DESIGN.md:34 bu fazda "GLB / HDR / fotoğraf" yasaklı.
- **D1–D2:** D1 üç yön (docs/yon/{a,b,c}). D2 /prototip reddi ("aşırı kötü, animasyon yok", docs/ref/d2-teshis.md:2) kod nedeni: timeline yalnız durum nesnesini `ease:'none'` ile tweenliyordu, görünen tek hareket sıvı boyu; kamera sabit (fov 30, uzaklık 5); tek renk zemin; pointer/raycast/exploded/model/ses yoktu. D4/D4.1 bunları ekledi; açık: S1'de cam koyu okunuyor, ses kulakla doğrulanmadı, hover/exploded espresso tonu, S3+ Ömer onayı bekliyor (docs/ref/d4-denetim.md).
- **DESIGN.md:** "Gece Demhanesi": zemin #15120F, mürekkep #ECE2D0, kül #8E8475, çizgi #2A251F; dünya paleti yalnız 3D'de (espresso #2B1A10, crema #C8873A); Archivo 800 wdth 125 + JetBrains Mono; tek eğri cubic-bezier(.22,1,.36,1), süreler 0.3/0.6/1.0/1.8 sn, scrub 1.2; exploded 1 sn dönüş + 0.5 bekleme + 1.8 ayrılma.
- **graphify-out:** 9d925e38'den üretilmiş, HEAD'in gerisinde (Faz 1 kapısında yenilenmeli).

## 5. Faz 1 önerisi
**Yığın (mevcut korunur):** Astro + three 0.186.1 + gsap 3.15.0 (ScrollTrigger, CustomEase) + lenis 1.3.26; ek bağımlılık yalnız `three/examples` yükleyicileri (GLTFLoader + DRACOLoader/MeshoptDecoder). R3F'ye geçiş yok (codrops R3F ama TELVE vanilla motoru çalışıyor).

**Araç sırası (departman-frontend):** graphify (TELVE kapısı, yenile) → DESIGN.md güncelle (GLB yasağı kalkar, yalnız exploded makine için) → frontend-craft iki pass → web-sahne-desenleri 2b (normalize + poz tablosu, mobil/masaüstü kademe) + animasyon-scroll-paket cinematic-gsap-lenis → threejs-3d-paket bütçe tablosu → screenshot döngüsü 390/768/1440 (2–4 tur, sayıyla diff) → axe → Lighthouse mobil → jev kalite yargısı. scroll-craft yalnız poster/video yedeği için (GLB exploded'a uymaz).

**Bölüm sırası:** S0 yükleyici + hero (metin LCP, WebGL requestIdleCallback ile) → S1 fincan/espresso (mevcut D4) → S2 dökme akışı → **S3 makine exploded** (BLENDER-1 glb; scrub ile ayrılma + tetikli dönüş; parça hover → HUD adı) → S4 noise "demleme dalgası" geçişi (dunya.ts genişletme, codrops fikri yeniden yazım) → S5 kapanış/CTA.

**BLENDER-1 bağlantısı:** g4 çıktısı `C:\Users\pc\Desktop\BlenderOlcum\blender\g4-tarif-{1,2}\telve.glb` (rapor `.kos/kopru/rapor/blender-1.md`; görev tanımı `tools/olcum/blender_faz5.py:48`, kol/blender). Ölçülen: tarif-1 51 KB, 5 mesh (GEO-Taban/Govde/Hazne/Cezve/Kapak), 1256 üçgen, 4 malzeme; tarif-2 71 KB, 2092 üçgen, `KHR_materials_transmission`; ikisinde de sıkıştırma ve animasyon yok, parçalar Z'de ≥5 cm aralıklı. Faz 1'de: bu glb ölçüm amaçlıydı → TELVE için aynı tarifle (blender-uretim) yeniden üret, toplanmış pozda dışa aktar, ayrılma ofsetleri koddan (poz tablosu) verilir; `tools/glb_hat.py` (kol/blender) ile Draco/Meshopt.

**Sayısal kabul ölçütleri (öneri):**
- Lighthouse mobil Performance ≥ 85, LCP < 2.5 sn (LCP öğesi metin/poster), TBT < 300 ms, CLS < 0.05.
- 60 fps orta donanımda: kare süresi ≤ 16.7 ms (mobil en kötü ≤ 25 ms), dt 1/30 ile sınırlı, kalite yöneticisi önce DPR düşürür; DPR mobil ≤ 1.5, masaüstü ≤ 2.
- Draw call ≤ 50 (Ciao masaüstü intro ~42), makine glb ≤ 20k üçgen ve ≤ 300 KB (Draco/Meshopt sonrası), doku ≤ 2048 px (mobil), HDR yok ya da ≤ 256 px.
- JS: size-limit sahne paketi 190 kB → yükleyiciler dahil ≤ 230 kB gz (Ciao 622 KB); toplam ilk yük ≤ 1.5 MB (Ciao 5.9 MB).
- a11y: axe 0 ihlal; reduced-motion CSS+JS; WebGL yok/context kaybı → poster; scroll hiçbir aşamada kilitlenmez.
- Her bölüm screenshot döngüsüyle (390/768/1440) sayısal diff kanıtlı; jev yargısı rapora girer.
