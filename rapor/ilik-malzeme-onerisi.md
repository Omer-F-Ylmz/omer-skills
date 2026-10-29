---
type: rapor
status: oneri
tags: [ilik, malzeme, 3d, yaka-cicegi]
relatedTo: [tools/uret_malzeme.py, docs/malzeme-envanter.md]
---
# İLİK yaka çiçeği: malzeme önerisi (SITE-MALZEME-1, 30 Eki)

İlik-v2 koduna dokunulmadı; yalnız öneri. Ömer: ücretli servis yok → Tripo/fal atlandı, ücretsiz yol yazıldı.

- **Çiçek (3D):** ürün fotoğrafından `python tools/uret_malzeme.py 3d --girdi <foto> --saglayici hf-zerogpu` (Hunyuan3D-2, $0; duman testinde 5,1 MB şekil-glb çıktı). Çıktı dokusuz: PBR için Blender headless bake (`blender-oturum` → `blender-uretim`; kumaş/ipek için sheen + roughness ~0,5, normal map). Tripo image-to-3D PBR daha hızlı olurdu ama ücretli (fal bakiyesi 0, TRIPO_API_KEY yok) → bakiye gelene dek yok.
- **Giriş (kare dizisi):** çiçeğin Blender turntable / açılış render'ı → `--kare` ile webp dizisi (≤120 kare, ~1024 px), sayfada `scroll-image-sequence` / `scroll-scrubbed-visual-sequence` skill'leri; kaydırma ilerlemesi kare indeksine bağlanır, hero'da canvas.
- **Gerçek zamanlı yedek:** GLB ≤3 MB, ≤60k yüz, doku ≤1024 (frontend-craft Bölüm 13); `threejs-procedural-materials` + `3d-retina-resolution`.
- **Sıra:** (1) HF kota varken glb al, (2) Blender bake, (3) render → kare dizisi, (4) ilik-v2'de yalnız varlık yolu değiştirilir.
- **Açık risk:** HF ZeroGPU günlük kota; dolarsa sıfırlanmayı bekle. Dokulu Hunyuan3D-2.1/TRELLIS yolu kota 0 yüzünden doğrulanmadı.
