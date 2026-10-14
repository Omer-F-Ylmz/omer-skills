# threejs — 29 benzersiz kayıt

**Amaç:** Web'de Three.js ile etkileşimli 3D sahne kurma ve hata ayıklama skill'leri: prosedürel dünya/malzeme, atmosfer, su, bulut, hava, ışık, gölge, bloom ve görsel doğrulama.

**İç yapı:** threejs ana skill + threejs-3d-paket (65 skill'lik paket) + threejs-skill-router yönlendirici; threejs-<konu> alt skill'leri: procedural-* (geometry, materials, fields, planets, vegetation, architecture, animation, vfx), görüntü hattı (bloom, exposure, image-pipeline, ssao, shadow-systems), doğa (ocean, clouds, weather, water-optics).

## En güçlü parçalar
- `threejs` — Sahne/kamera/renderer, ışık ve malzemeyle etkileşimli 3D sahne kurma ve hata ayıklama için giriş noktası.
- `threejs-skill-router` — Geometri, malzeme, atmosfer gibi birden çok alana yayılan yeni görsel deneyimlerde doğru skill'e yönlendirir.
- `threejs-visual-validation` — Sabit görüş görsel sözleşmesi, post'suz taban çizgisi ve seed taramalarıyla görsel doğrulama.
- `threejs-landscape` — Hero arka planı, ürün sahnesi, scroll dünyası gibi nesnenin bir ortama oturması gereken sahneler.
- `threejs-image-pipeline` — Derinlik/normal/albedo sahipliği, GTAO, bloom, göz uyumu, ton eşleme ve 3D LUT hattı.
- `threejs-shadow-systems` — Büyük prosedürel dünya, şehir ve hareketli kamerada WebGPU/TSL gölge düğümleri ve kaskadlar.
- `threejs-procedural-materials` — Doku destekli PBR ile prosedürel displacement ve maskeli hibrit malzemeler.

## Birlikte kullanım
- threejs-skill-router → ilgili threejs-<konu> skill'i → threejs-visual-validation: yönlendir, kur, doğrula.
- threejs-landscape + threejs-weather + threejs-volumetric-clouds: hava durumu kontrollü hero arka planı.
- threejs-image-pipeline + threejs-bloom + threejs-exposure-color-grading: HDR görüntü hattı.

## Tuzaklar
- threejs-3d-paket 65 skill'lik paket; tek iş için tamamı yerine ilgili alt skill seçilmeli.
- Birçok alt skill (spectral-ocean, shadow-systems) WebGPU/TSL hedefler; yalnız WebGL hedefleyen projede uyum kontrol edilmeli.

## Üyeler
- skill (29): threejs, threejs-3d-paket, threejs-atmosphere-aerial-perspective, threejs-bloom, threejs-camera-direction, threejs-exposure-color-grading, threejs-image-pipeline, threejs-landscape, threejs-parallax-occlusion-mapping, threejs-precipitation-surfaces, threejs-procedural-animation, threejs-procedural-architecture, threejs-procedural-fields, threejs-procedural-geometry, threejs-procedural-materials, threejs-procedural-planets, threejs-procedural-vegetation, threejs-procedural-vfx, threejs-raymarched-space-effects, threejs-screen-space-ambient-occlusion, threejs-shadow-systems, threejs-skill-router, threejs-spectral-ocean, threejs-temporal-surfaces, threejs-towers, threejs-visual-validation, threejs-volumetric-clouds, threejs-water-optics, threejs-weather
