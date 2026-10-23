# Okul 3D kuyruk (usta-blender-1 çıktısı)
- usta-3d-d1-duman: quick_smoke headless bake'te yoğunluk görünmedi (yalnız emitter); neden kanıtsız. Önce `ds` yoğunluk grid'ini oku (bake sonrası) / MCP'li canlı Blender'da dene.
- usta-3d-hakem-tekrar: A1/B1/C1 puanı yargıçsız (gemini+nvidia günlük 429); kota dönünce `gorsel_hakem.py` ile 4 çift puanla (.kos/kopru/ara/blender-s1/).
- usta-3d-icerik-doldur: `python tools/okul/hat.py 3d-a|3d-b|3d-c|3d-d` (ÇEKİŞMELİ/BEKLE; ücretsiz havuz dönünce) → ders kitabı içeriği.
- usta-3d-a1-sap: cezve sapı gövdeye gerçek bağlanmalı (şimdi yaklaşık); A2 hard-surface silah/mobilya.
- usta-3d-b2 stüdyo ışığı · usta-3d-c2 rig+yürüyüş · usta-3d-c3 oyun anim seti · usta-3d-d3 oyun VFX flipbook · usta-3d-a4 karakter (MPFB taban) · usta-3d-e poli bütçesi/LOD.
- (USTA-BLENDER-2) D1 duman ÇÖZÜLDÜ: headless `bake_all` async, cache'e yalnız kare 1 yazar → `ds.cache_frame_end` + `frame_set` döngüsü (ex.py). Hakem + hat.py 3d içerik: tüm ücretsiz havuz günlük 429 (gemini/nvidia/alibaba) → kota dönünce tekrar.
