# DERS KİTABI — 3D Modelleme (A)
# DERS KİTABI — 3D Modelleme (A)
## A. En iyi yöntemler + tarif kartları (adım adım)
> "Gerçek boyut `references/olculer.md`'den. Tablo dışı nesnede ölçüyü brief'ten ya da bulunan kaynaktan al, **uydurma**; kaynak yoksa sor." (blender-uretim.md)
Boyutları referans tablosundan veya brief'ten alır; hiçbir zaman uydurmaz, eksikse sorar.

> "1. **Blockout** at real scale (`ob.dimensions`) from primitives. Settle the silhouette and proportions before any detail. Check against references." (hardsurface-modeling.md)
İlk adım gerçek ölçekte primitiflerle blokaj; silüet ve oran referansla kilitlenmeden detaya geçilmez.

> "Run `scripts/scene_audit.py` (add `--fix purge scale paths` only on files you own). It reports units, unapplied/negative scale, default names, objects in the scene root, missing images, orphans and far-off origins." (scene-setup.md)
Her proje başında ve teslim öncesi `scene_audit.py` çalıştırılır; rapor boşaldığında (veya kalanlar kastense) hygiene geçer.

> "Name everything with the conventions below. Rename after every duplicate or join so no `.001` suffixes remain." (scene-setup.md)
Tüm nesneler isim kuralına (SM_, M_, T_ vb.) göre adlandırılır; duplicate/join sonrası `.001` kalmaz.

> "Set origins: props at the bottom-center (they sit on the ground at Z=0), characters at world origin between the feet, doors/hinges at the pivot." (scene-setup.md)
Origin konumu tipine göre sabittir: prop alt-orta, karakter ayak arası dünya orijini, kapı/menteşe pivot noktasında.

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "Weighted Normal has no effect: faces are flat-shaded, or an earlier modifier destroyed the custom normals." (hardsurface-modeling.md)
*Hata: Weighted Normal modülü etkisiz → **Neden:** Yüzler düz şekillendirilmiş veya önceki bir modül özelleştirilmiş normalları yok etti.*

---

> "Sockets that are disabled for the current mode/data type are still in `node.inputs` with the same name." (geometry-nodes.md)
*Hata: Geometry Nodes modülünde devre dışı soketler hata verir → **Neden:** Soketler devre dışı olsa bile `node.inputs` listesinde görünür.*

---

> "5.0+: UV selection is shared across UV maps (`.uv_select_*` attributes)." (retopology-uv.md)
*Hata: UV seçimi tutarsız → **Neden:** 5.0+ sürümlerde UV seçimi tüm UV haritaları arasında paylaşılır.*

## C. Kalite kapısı kontrol listesi
> "Tarif eğitim varsayılanlarını kendisi uygular (85 mm, ince pah, doğrusal turntable, EEVEE RT); elle seçilecek ışık/malzeme/kamera/GN/GLB kuralları ve render öncesi kontrol listesi: `references/egitim.md`." (blender-uretim.md)
*Standart ayarların doğru uygulanıp uygulanmadığını doğrulayın.*

> "Kendi kontrol render'ın ≤512 px (Workbench/Eevee); kontrol görüntülerine en fazla 3 Read." (blender-uretim.md)
*Kontrol render boyutunu ve okuma sayısını sınırlayın.*

> "Avoid coplanar boolean faces: extend cutters slightly past the surface. They also cause z-fighting." (hardsurface-modeling.md)
*Boolean işlemlerinde çakışma ve z-fighting kontrolü.*

> "Spend density where the silhouette needs it, not on flat faces." (hardsurface-modeling.md)
*Silüet hassasiyetine göre poligon yoğunluğunun dağılımını doğrulayın.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Gerçek boyut `references/olculer.md`'den. Tablo dışı nesnede ölçüyü brief'ten ya da bulunan kaynaktan al, **uydurma**; kaynak yoksa sor. Birim metre (Blender), tabloda mm." (blender-uretim.md)
- Ölçüleri olculer.md dosyasından almak, tabloda belirtilen ölçüleri kullanmak ve tablo dışı nesneler için brief veya mevcut kaynaklardan ölçüleri almak ücretsiz bir yoldur.

> "Varlık işinin adım/komut/kapı sırası: `docs/atlas/site-3d.md` Bölüm B." (blender-uretim.md)
- Varlık işinin adım, komut ve kapı sırası site-3d.md dosyasındaki Bölüm B'de belirtilen sırayla uygulanabilir.

> "Sıfırdan modelleme yok; hazır varlık merdiveni: yerel → Objaverse (Sketchfab uid) → Poly Haven / ambientCG → görüntü→3D → en son sade bpy. `python varlik_getir.py ara|indir …` (hesapsız; `atif.json`'a lisans + yazar; CC-BY ise atıf kolofona). Blender'da yalnız küçük düzenleme: `blender -b -P duzenle_b.py -- gir.glb cik.glb --yukseklik … --ucgen …` (önce `--bak`)." (blender-uretim.md)
- Sıfırdan modelleme yerine hazır varlıkları kullanmak, yerel kaynaklardan veya Objaverse, Poly Haven, ambientCG gibi platformlardan varlıkları indirmek ve küçük düzenlemeler yapmak ücretsiz bir yoldur.

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "TELVE-R2d cezve, uid 3b5bb5d4…, 2496 üçgen, 57 KB GLB (#6)" (blender-uretim.md)
TELVE projesinde kullanılan 3D cezve modeli, 2496 üçgen ve 57 KB boyutunda GLB formatında.

> "scripts/gn_builder.py -- --describe GeometryNodeDistributePointsOnFaces GeometryNodeInstanceOnPoints" (geometry-nodes.md)
Geometry Nodes için kullanılan komut, belirli düğümlerin özelliklerini açıklamak için.

> "SM_<Name>[_LOD#]" (scene-setup.md)
Statik mesh isimlendirme kuralı, LOD seviyeleri için kullanılır.

> "T_<Name>_<Suffix>: _BC base color, _N normal, _ORM (R=AO G=Rough B=Metal), _E emissive, _M mask" (scene-setup.md)
Metin isimlendirme kuralı, renk, normal, AO, metalik gibi özellikler için kullanılır.

> "scripts/auto_retopo.py -- --objects Sculpt --tris 8000 --method ..." (retopology-uv.md)
Otomatik retopoloji işlemi için kullanılan komut, hedef üçgen sayısı ve yöntem belirtilir.

> "scripts/texel_density.py --res 2048" (retopology-uv.md)
Texel yoğunluğu hesaplaması için kullanılan komut, çözünürlük belirtilir.

> "scripts/scene_audit.py" (scene-setup.md)
Sahne denetimi için kullanılan komut, sahne düzenini ve hataları kontrol eder.

> "scripts/sculpt_ops.py" (sculpting.md)
Heykeltıraş işlemleri için kullanılan komut, heykeltıraş işlemlerini gerçekleştirir.

> "scripts/apply_stack.py -- --objects Body --preset midpoly --cutters Cut1 Cut2" (hardsurface-modeling.md)
Modifiye yığın uygulama işlemi için kullanılan komut, nesneler ve kesiciler belirtilir.


# Çelişki Denetimi

## A. En iyi yöntemler + tarif kartları (adım adım)

**Madde 1:**
- **Çelişki:** "Boyutları referans tablosundan veya brief'ten alır; hiçbir zaman uydurmaz, eksikse sorar."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

**Madde 2:**
- **Çelişki:** "İlk adım gerçek ölçekte primitiflerle blokaj; silüet ve oran referansla kilitlenmeden detaya geçilmez."
- **Kaynak:** hardsurface-modeling.md
- **Sonuç:** OK

**Madde 3:**
- **Çelişki:** "Her proje başında ve teslim öncesi `scene_audit.py` çalıştırılır; rapor boşaldığında (veya kalanlar kastense) hygiene geçer."
- **Kaynak:** scene-setup.md
- **Sonuç:** OK

**Madde 4:**
- **Çelişki:** "Tüm nesneler isim kuralına (SM_, M_, T_ vb.) göre adlandırılır; duplicate/join sonrası `.001` kalmaz."
- **Kaynak:** scene-setup.md
- **Sonuç:** OK

**Madde 5:**
- **Çelişki:** "Origin konumu tipine göre sabittir: prop alt-orta, karakter ayak arası dünya orijini, kapı/menteşe pivot noktasında."
- **Kaynak:** scene-setup.md
- **Sonuç:** OK

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)

**Madde 1:**
- **Çelişki:** "Weighted Normal modülü etkisiz → **Neden:** Yüzler düz şekillendirilmiş veya önceki bir modül özelleştirilmiş normalları yok etti."
- **Kaynak:** hardsurface-modeling.md
- **Sonuç:** OK

**Madde 2:**
- **Çelişki:** "Geometry Nodes modülünde devre dışı soketler hata verir → **Neden:** Soketler devre dışı olsa bile `node.inputs` listesinde görünür."
- **Kaynak:** geometry-nodes.md
- **Sonuç:** OK

**Madde 3:**
- **Çelişki:** "5.0+ sürümlerde UV seçimi tüm UV haritaları arasında paylaşılır."
- **Kaynak:** retopology-uv.md
- **Sonuç:** OK

## C. Kalite kapısı kontrol listesi

**Madde 1:**
- **Çelişki:** "Standart ayarların doğru uygulanıp uygulanmadığını doğrulayın."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

**Madde 2:**
- **Çelişki:** "Kontrol render boyutunu ve okuma sayısını sınırlayın."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

**Madde 3:**
- **Çelişki:** "Boolean işlemlerinde çakışma ve z-fighting kontrolü."
- **Kaynak:** hardsurface-modeling.md
- **Sonuç:** OK

**Madde 4:**
- **Çelişki:** "Silüet hassasiyetine göre poligon yoğunluğunun dağılımını doğrulayın."
- **Kaynak:** hardsurface-modeling.md
- **Sonuç:** OK

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)

**Madde 1:**
- **Çelişki:** "Ölçüleri olculer.md dosyasından almak, tabloda belirtilen ölçüleri kullanmak ve tablo dışı nesneler için brief veya mevcut kaynaklardan ölçüleri almak ücretsiz bir yoldur."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

**Madde 2:**
- **Çelişki:** "Varlık işinin adım, komut ve kapı sırası site-3d.md dosyasındaki Bölüm B'de belirtilen sırayla uygulanabilir."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

**Madde 3:**
- **Çelişki:** "Sıfırdan modelleme yerine hazır varlıkları kullanmak, yerel kaynaklardan veya Objaverse, Poly Haven, ambientCG gibi platformlardan varlıkları indirmek ve küçük düzenlemeler yapmak ücretsiz bir yoldur."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5

**Madde 1:**
- **Çelişki:** "TELVE projesinde kullanılan 3D cezve modeli, 2496 üçgen ve 57 KB boyutunda GLB formatında."
- **Kaynak:** blender-uretim.md
- **Sonuç:** OK

**Madde 2:**
- **Çelişki:** "Geometry Nodes için kullanılan komut, belirli düğümlerin özelliklerini açıklamak için."
- **Kaynak:** geometry-nodes.md
- **Sonuç:** OK

**Madde 3:**
- **Çelişki:** "Statik mesh isimlendirme kuralı, LOD seviyeleri için kullanılır."
- **Kaynak:** scene-setup.md
- **Sonuç:** OK

**Madde 4:**
- **Çelişki:** "Metin isimlendirme kuralı, renk, normal, AO, metalik gibi özellikler için kullanılır."
- **Kaynak:** scene-setup.md
- **Sonuç:** OK

**Madde 5:**
- **Çelişki:** "Otomatik retopoloji işlemi için kullanılan komut, hedef üçgen sayısı ve yöntem belirtilir."
- **Kaynak:** retopology-uv.md
- **Sonuç:** OK

**Madde 6:**
- **Çelişki:** "Texel yoğunluğu hesaplaması için kullanılan komut, çözünürlük belirtilir."
- **Kaynak:** retopology-uv.md
- **Sonuç:** OK

**Madde 7:**
- **Çelişki:** "Sahne denetimi için kullanılan komut, sahne düzenini ve hataları kontrol eder."
- **Kaynak:** scene-setup.md
- **Sonuç:** OK

**Madde 8:**
- **Çelişki:** "Heykeltıraş işlemleri için kullanılan komut, heykeltıraş işlemlerini gerçekleştirir."
- **Kaynak:** sculpting.md
- **Sonuç:** OK

**Madde 9:**
- **Çelişki:** "Modifiye yığın uygulama işlemi için kullanılan komut, nesneler ve kesiciler belirtilir."
- **Kaynak:** hardsurface-modeling.md
- **Sonuç:** OK

SONUC: GECER

## C. Kalite kapısı kontrol listesi
> "Tarif eğitim varsayılanlarını kendisi uygular (85 mm, ince pah, doğrusal turntable, EEVEE RT); elle seçilecek ışık/malzeme/kamera/GN/GLB kuralları ve render öncesi kontrol listesi: `references/egitim.md`." (blender-uretim.md)
*Standart ayarların doğru uygulanıp uygulanmadığını doğrulayın.*

> "Kendi kontrol render'ın ≤512 px (Workbench/Eevee); kontrol görüntülerine en fazla 3 Read." (blender-uretim.md)
*Kontrol render boyutunu ve okuma sayısını sınırlayın.*

> "Avoid coplanar boolean faces: extend cutters slightly past the surface. They also cause z-fighting." (hardsurface-modeling.md)
*Boolean işlemlerinde çakışma ve z-fighting kontrolü.*

> "Spend density where the silhouette needs it, not on flat faces." (hardsurface-modeling.md)
*Silüet hassasiyetine göre poligon yoğunluğunun dağılımını doğrulayın.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Gerçek boyut `references/olculer.md`'den. Tablo dışı nesnede ölçüyü brief'ten ya da bulunan kaynaktan al, **uydurma**; kaynak yoksa sor. Birim metre (Blender), tabloda mm." (blender-uretim.md)
- Ölçüleri olculer.md dosyasından almak, tabloda belirtilen ölçüleri kullanmak ve tablo dışı nesneler için brief veya mevcut kaynaklardan ölçüleri almak ücretsiz bir yoldur.

> "Varlık işinin adım/komut/kapı sırası: `docs/atlas/site-3d.md` Bölüm B." (blender-uretim.md)
- Varlık işinin adım, komut ve kapı sırası site-3d.md dosyasındaki Bölüm B'de belirtilen sırayla uygulanabilir.

> "Sıfırdan modelleme yok; hazır varlık merdiveni: yerel → Objaverse (Sketchfab uid) → Poly Haven / ambientCG → görüntü→3D → en son sade bpy. `python varlik_getir.py ara|indir …` (hesapsız; `atif.json`'a lisans + yazar; CC-BY ise atıf kolofona). Blender'da yalnız küçük düzenleme: `blender -b -P duzenle_b.py -- gir.glb cik.glb --yukseklik … --ucgen …` (önce `--bak`)." (blender-uretim.md)
- Sıfırdan modelleme yerine hazır varlıkları kullanmak, yerel kaynaklardan veya Objaverse, Poly Haven, ambientCG gibi platformlardan varlıkları indirmek ve küçük düzenlemeler yapmak ücretsiz bir yoldur.

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "TELVE-R2d cezve, uid 3b5bb5d4…, 2496 üçgen, 57 KB GLB (#6)" (blender-uretim.md)
TELVE projesinde kullanılan 3D cezve modeli, 2496 üçgen ve 57 KB boyutunda GLB formatında.

> "scripts/gn_builder.py -- --describe GeometryNodeDistributePointsOnFaces GeometryNodeInstanceOnPoints" (geometry-nodes.md)
Geometry Nodes için kullanılan komut, belirli düğümlerin özelliklerini açıklamak için.

> "SM_<Name>[_LOD#]" (scene-setup.md)
Statik mesh isimlendirme kuralı, LOD seviyeleri için kullanılır.

> "T_<Name>_<Suffix>: _BC base color, _N normal, _ORM (R=AO G=Rough B=Metal), _E emissive, _M mask" (scene-setup.md)
Metin isimlendirme kuralı, renk, normal, AO, metalik gibi özellikler için kullanılır.

> "scripts/auto_retopo.py -- --objects Sculpt --tris 8000 --method ..." (retopology-uv.md)
Otomatik retopoloji işlemi için kullanılan komut, hedef üçgen sayısı ve yöntem belirtilir.

> "scripts/texel_density.py --res 2048" (retopology-uv.md)
Texel yoğunluğu hesaplaması için kullanılan komut, çözünürlük belirtilir.

> "scripts/scene_audit.py" (scene-setup.md)
Sahne denetimi için kullanılan komut, sahne düzenini ve hataları kontrol eder.

> "scripts/sculpt_ops.py" (sculpting.md)
Heykeltıraş işlemleri için kullanılan komut, heykeltıraş işlemlerini gerçekleştirir.

> "scripts/apply_stack.py -- --objects Body --preset midpoly --cutters Cut1 Cut2" (hardsurface-modeling.md)
Modifiye yığın uygulama işlemi için kullanılan komut, nesneler ve kesiciler belirtilir.
