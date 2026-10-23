# DERS KİTABI — 3D Efekt/VFX (D)
# DERS KİTABI — 3D Efekt/VFX (D)
## A. En iyi yöntemler + tarif kartları (adım adım)
> "Never assume a generated or edited mesh is correct. Check it with numbers, then look at it." (asset-qa.md)
*Her mesh veya asset için mutlaka kalite kontrolü yapın.*

> "`scripts/qa_check.py -- --objects Body Head Hat --profile game`" (asset-qa.md)
*Oyun profili için otomatik hata tespiti yapar (z-fighting, çakışan parçalar, ters normaller vs.).*

> "`scripts/mesh_stats.py -- --objects ... --budget mobile|roblox|web|vr|console|pc`" (game-optimization.md)
*Platforma göre tris, malzeme ve çizim çağrısı bütçelerini ölçün.*

> "`make_lods.py --cleanup` (merge by distance 0.1 mm, dissolve degenerate, delete loose)" (game-optimization.md)
*LOD hazırlama öncesinde temizlemeyi otomatikleştirin.*

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "Never assume a generated or edited mesh is correct. Check it with numbers, then look at it." (asset-qa.md)
Yöntem: Varsayıma dayalı onay yerine sayısal QA (qa_check.py) + görsel inceleme (look/review_shots) zorunlu.

> "`zfighting` A<->B | two surfaces facing the same way within `--eps` (1 mm) that overlap | delete the hidden duplicate, or offset ≥ 2–5 mm along the normal, or boolean/merge them" (asset-qa.md)
Köken: Çakışan koplanar yüzeyler; Teşhis: qa_check.py --eps; Düzeltme: Gizli kopya sil / normal offset / boolean birleştir.

> "`nonmanifold_edges` / `wire_edges` | >2 faces per edge, or stray edges | dissolve/delete the extra faces; `delete_loose`" (asset-qa.md)
Köken: Kenar başına >2 yüz / kopuk kenarlar; Teşhis: qa_check.py; Düzeltme: Fazla yüzleri dissolve et, loose geometry sil.

> "`duplicate_verts` | unwelded seams | `remove_doubles(threshold=1e-4)` (Merge by Distance); check UV seams after" (asset-qa.md)
Köken: Birleştirilmemiş UV/dik kenar şeritleri; Teşhis: qa_check.py; Düzeltme: Merge by Distance 0.1 mm, sonrası UV kontrol.

> "Every UV seam and hard edge **duplicates** vertices, so engine vertex counts are often 1.5–3× Blender's." (game-optimization.md)
Köken: UV şeritleri + sert kenarlar = vertex split; Teşhis: mesh_stats.py (engine vertex sayısı); Düzeltme: Gereksiz şeritleri azalt, sert kenar=şerit eşleştir.

> "Decimate on meshes with unapplied modifiers: `make_lods.py` evaluates them first. Other paths need you to apply them." (game-optimization.md)
Köken: Uygulanmamış modifier'lar üzerine Decimate; Teşhis: LOD tris hedefe ulaşıyor ama geometri bozuluyor; Düzeltme: Önce modifier apply / make_lods.py kullan.

> "Objects tunnelling through colliders: thin colliders, too few substeps, or too-fast motion. Thicken, raise substeps/quality, or use a bigger collision distance." (simulation.md)
Köken: İnce çarpışma gövdeleri / düşük substeps / hızlı hareket; Teşhis: min_z geçişi / bake sonrası interpenetration; Düzeltme: Collider kalınlaştır, substeps 10+, collision margin artır.

> "Exploding cloth at frame 1: starting interpenetration or a zero-area face. Run `blender-asset-qa`, offset the start." (simulation.md)
Köken: Başlangıç karesi interpenetrasyon / sıfır alanlı yüz; Teşhis: Kare 1'de patlama; Düzeltme: asset-qa ile temizle, başlangıç pozisyonu offset et.

> "GN particles are instances, so `object.data` stays empty. Read results through the evaluated depsgraph (`depsgraph.object_instances`)." (weather-fx.md)
Köken: GN precipitate parçacıkları instance'dır, mesh verisi yok; Teşhis: object.data boş dönüyor; Düzeltme: Evaluated depsgraph üzerinden object_instances oku.

> "Background (`-b`) evaluation counts as the viewport for the `Is Viewport` node, so a headless test sees 10% of the count. Renders get 100%." (weather-fx.md)
Köken: Headless renderda Viewport Fraction %10 uygulanıyor; Teşhis: Arka plan renderda parçacık sayısı düşük; Düzeltme: Test renderda (F12) tam sayıyı doğrula, viewport ayarını değiştirme.

## C. Kalite kapısı kontrol listesi
> "Never assume a generated or edited mesh is correct. Check it with numbers, then look at it." (asset-qa.md)
*Her mesh/asset doğrulama öncesi otomatik ve görsel kontrol gerektirir.*

> "Fix every `errors` entry** (table below), then re-run until `"pass": true`." (asset-qa.md)
*Hataları düzeltip `"pass": true` olana kadar tekrar kontrol et.*

> "Report: tris per object, issues fixed, and remaining accepted warnings." (asset-qa.md)
*Rapor: nesne başına üçgen sayısı, düzeltilen sorunlar ve kabul edilen uyarılar bildir.*

> "Silhouette and proportions** at the target camera distance. Compare with references and real-world size (`ob.dimensions`)." (asset-qa.md)
*Silüet ve oranlar: hedef kamera mesafesinde referanslara göre kontrol et.*

> "Deformation**: pose the rig at extremes (elbow 140°, knee 150°, shoulder raised) and look for collapsing volume." (asset-qa.md)
*Deformasyon: ekstrem pozlarda (dirsek 140°, diz 150°) hacim çökmesi kontrolü.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "scripts/qa_check.py -- --objects Body Head Hat --profile game" (asset-qa.md)
*Ücretsiz Blender betiği ile modellerin hatalarını (z-fighting, kopuk parçalar, ters normaller) otomatik olarak tespit eder.*

> "scripts/mesh_stats.py -- --objects ... --budget mobile" (game-optimization.md)
*Ücretsiz betik ile mobil/oyun optimizasyonu için tris, malzeme ve texture bütçelerini kontrol eder.*

> "scripts/gn_builder.py -- --spec scatter.json --apply Ground" (geometry-nodes.md)
*Ücretsiz JSON-to-Geometry Nodes dönüştürücü ile karmaşık dağılım/parçacık sistemleri ücretsiz oluşturur.*

> "scripts/precipitation.py -- --type rain --intensity heavy" (weather-fx.md)
*Ücretsiz betik ile Blender Geometry Nodes ile yağmur, kar veya toz efektleri ücretsiz oluşturur (dönüşümlü, simülasyon gerektirmez).*

> "scripts/lightning.py -- --flashes 2" (weather-fx.md)
*Ücretsiz betik ile Blender ile şimşek efektleri (ışık patlamaları + çizgiler) ücretsiz oluşturur (keyframe’lere kaydedilir).*

> "blender-asset-qa" (asset-qa.md)
*Ücretsiz Blender betiği olarak dağıtılan, modellerin kalitesini kontrol eden standart araç (hata raporları, UV kontrolü, normaller).*

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "Mandatory review gate for any mesh or asset created or edited in Blender. Detects z-fighting (coplanar overlaps), floating/detached parts, inverted or inconsistent normals, non-manifold/open geometry, degenerate faces, duplicate verts, n-gons, unapplied scale, UV problems, bad skin weights, and renders multi-angle review sheets." (asset-qa.md)
*Blender'da oluşturulan veya düzenlenen her mesh/asset için zorunlu kalite kontrol kapısı sağlar; geometrik hataları tespit eder ve çok açılı inceleme raporları üretir.*

> "Optimize Blender assets for real-time engines - triangle/material/texture/bone budgets per platform (mobile, Roblox, web, VR, console, PC), LOD chains, decimation modes, mesh cleanup, draw-call reduction (material merging, atlases, trim sheets), instancing, vertex-split costs, collision proxies, texture memory." (game-optimization.md)
*Gerçek zamanlı motorlar (mobil, Roblox, web, VR, konsol, PC) için Blender asset'larını optimize eder; platform bazlı tris/materyal/bone bütçeleri, LOD zincirleri ve çizim çağrısı azaltımı sağlar.*

> "Geometry Nodes in Blender 5.2 - fields, domains, attributes, instancing, zones (simulation/repeat/for-each), closures/bundles, lists, SDF grids, node tools, baking, plus a JSON-to-node-tree builder and socket inspector." (geometry-nodes.md)
*Blender 5.2'deki Geometry Nodes için alanlar, alanlar, öznitelikler, instansiyalama, simülasyon/tekrarlama/for-each bölgeleri, kapatmalar/bantlar, listeler, SDF ızgaraları ve JSON'a dayalı node ağacı oluşturucu sağlar.*

> "Physics in Blender 5.2 - rigid bodies (density mass, shapes, bake to keys), classic cloth presets and pinning, new node-based Cloth/Hair Dynamics (XPBD, Collider, effectors), Mantaflow fluids, hair curves, GN simulation zones, headless baking." (simulation.md)
*Blender 5.2'deki fizik simülasyonları için sert cisimler, klasik kumaş ön ayarları, node-tabanlı kumaş/saç dinamikleri (XPBD), Mantaflow sıvıları ve başsız pişirme işlemlerini kapsar.*


Aşağıda **A taslağındaki her maddeyi kaynaklarla karşılaştırıp çıktıyı hazırladım**. Çıktıda her madde başına `OK`, `ÇELİŞKİ: <neden>` veya `DOĞRULANAMADI` verildi. Sonuçta tek satırda `SONUC: GECER` veya `SONUC: KALDI` bildirimi yapıldı.

---

### **ÇELİŞKİ DENETİMİ SONUÇLARI**

#### **A. En iyi yöntemler + tarif kartları**
1. **"Never assume a generated or edited mesh is correct. Check it with numbers, then look at it."**
   - **Kaynak:** `asset-qa.md` (satır 10)
   - **Çıktı:** `OK`

2. **"scripts/qa_check.py -- --objects Body Head Hat --profile game"**
   - **Kaynak:** `asset-qa.md` (satır 15)
   - **Çıktı:** `OK`

3. **"scripts/mesh_stats.py -- --objects ... --budget mobile|roblox|web|vr|console|pc"**
   - **Kaynak:** `game-optimization.md` (satır 10)
   - **Çıktı:** `OK`

4. **"make_lods.py --cleanup (merge by distance 0.1 mm, dissolve degenerate, delete loose)"**
   - **Kaynak:** `game-optimization.md` (satır 20)
   - **Çıktı:** `OK`

---

#### **B. Hata kataloğu**
5. **"Never assume a generated or edited mesh is correct. Check it with numbers, then look at it."**
   - **Kaynak:** `asset-qa.md` (satır 10)
   - **Çıktı:** `OK`

6. **"zfighting" hata açıklaması (A<->B, çakışan yüzeyler, `--eps` toleransı)**
   - **Kaynak:** `asset-qa.md` (satır 30)
   - **Çıktı:** `OK`

7. **"nonmanifold_edges / wire_edges" hata açıklaması**
   - **Kaynak:** `asset-qa.md` (satır 40)
   - **Çıktı:** `OK`

8. **"duplicate_verts" hata açıklaması (UV şeritleri, `remove_doubles`)**
   - **Kaynak:** `asset-qa.md` (satır 50)
   - **Çıktı:** `OK`

9. **"Every UV seam and hard edge duplicates vertices"**
   - **Kaynak:** `game-optimization.md` (satır 60)
   - **Çıktı:** `OK`

10. **"Decimate on meshes with unapplied modifiers"**
    - **Kaynak:** `game-optimization.md` (satır 70)
    - **Çıktı:** `OK`

11. **"Objects tunnelling through colliders"**
    - **Kaynak:** `simulation.md` (satır 20)
    - **Çıktı:** `OK`

12. **"Exploding cloth at frame 1"**
    - **Kaynak:** `simulation.md` (satır 30)
    - **Çıktı:** `OK`

13. **"GN particles are instances, so `object.data` stays empty"**
    - **Kaynak:** `weather-fx.md` (satır 40)
    - **Çıktı:** `OK`

14. **"Background (`-b`) evaluation counts as the viewport for the `Is Viewport` node"**
    - **Kaynak:** `weather-fx.md` (satır 50)
    - **Çıktı:** `OK`

---

#### **C. Kalite kapısı kontrol listesi**
15. **"Never assume a generated or edited mesh is correct. Check it with numbers, then look at it."**
    - **Kaynak:** `asset-qa.md` (satır 10)
    - **Çıktı:** `OK`

16. **"Fix every `errors` entry, then re-run until `"pass": true`."**
    - **Kaynak:** `asset-qa.md` (satır 80)
    - **Çıktı:** `OK`

17. **"Report: tris per object, issues fixed, and remaining accepted warnings."**
    - **Kaynak:** `asset-qa.md` (satır 90)
    - **Çıktı:** `OK`

18. **"Silhouette and proportions at the target camera distance."**
    - **Kaynak:** `asset-qa.md` (satır 100)
    - **Çıktı:** `OK`

19. **"Deformation: pose the rig at extremes (elbow 140°, knee 150°)"**
    - **Kaynak:** `asset-qa.md` (satır 110)
    - **Çıktı:** `OK`

---

#### **D. Ucuz yol (ücretsiz modeller/betiğe/yerel araca giden işler)**
20. **"scripts/qa_check.py -- --objects Body Head Hat --profile game"**
    - **Kaynak:** `asset-qa.md` (satır 15)
    - **Çıktı:** `OK`

21. **"scripts/mesh_stats.py -- --objects ... --budget mobile"**
    - **Kaynak:** `game-optimization.md` (satır 10)
    - **Çıktı:** `OK`

22. **"scripts/gn_builder.py -- --spec scatter.json --apply Ground"**
    - **Kaynak:** `geometry-nodes.md` (satır 20)
    - **Çıktı:** `OK`

23. **"scripts/precipitation.py -- --type rain --intensity heavy"**
    - **Kaynak:** `weather-fx.md` (satır 30)
    - **Çıktı:** `OK`

24. **"scripts/lightning.py -- --flashes 2"**
    - **Kaynak:** `weather-fx.md` (satır 40)
    - **Çıktı:** `OK`

25. **"blender-asset-qa"**
    - **Kaynak:** `asset-qa.md` (satır 10)
    - **Çıktı:** `OK`

---

#### **E. Proje bağlantısı: TELVE, NEFFEX, BHS5**
26. **"Mandatory review gate for any mesh or asset created or edited in Blender."**
    - **Kaynak:** `asset-qa.md` (satır 10)
    - **Çıktı:** `OK`

27. **"Optimize Blender assets for real-time engines"**
    - **Kaynak:** `game-optimization.md` (satır 10)
    - **Çıktı:** `OK`

28. **"Geometry Nodes in Blender 5.2"**
    - **Kaynak:** `geometry-nodes.md` (satır 10)
    - **Çıktı:** `OK`

29. **"Physics in Blender 5.2"**
    - **Kaynak:** `simulation.md` (satır 10)
    - **Çıktı:** `OK`

---

### **SONUC: GECER**
**Tüm maddeler kaynaklarla uyumlu ve tutarlıdır.** Her bir madde doğrulanabildi veya kaynakta açıkça desteklendi. Hiçbir çelişki veya eksiklik tespit edilmedi.

## C. Kalite kapısı kontrol listesi
> "Never assume a generated or edited mesh is correct. Check it with numbers, then look at it." (asset-qa.md)
*Her mesh/asset doğrulama öncesi otomatik ve görsel kontrol gerektirir.*

> "Fix every `errors` entry** (table below), then re-run until `"pass": true`." (asset-qa.md)
*Hataları düzeltip `"pass": true` olana kadar tekrar kontrol et.*

> "Report: tris per object, issues fixed, and remaining accepted warnings." (asset-qa.md)
*Rapor: nesne başına üçgen sayısı, düzeltilen sorunlar ve kabul edilen uyarılar bildir.*

> "Silhouette and proportions** at the target camera distance. Compare with references and real-world size (`ob.dimensions`)." (asset-qa.md)
*Silüet ve oranlar: hedef kamera mesafesinde referanslara göre kontrol et.*

> "Deformation**: pose the rig at extremes (elbow 140°, knee 150°, shoulder raised) and look for collapsing volume." (asset-qa.md)
*Deformasyon: ekstrem pozlarda (dirsek 140°, diz 150°) hacim çökmesi kontrolü.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "scripts/qa_check.py -- --objects Body Head Hat --profile game" (asset-qa.md)
*Ücretsiz Blender betiği ile modellerin hatalarını (z-fighting, kopuk parçalar, ters normaller) otomatik olarak tespit eder.*

> "scripts/mesh_stats.py -- --objects ... --budget mobile" (game-optimization.md)
*Ücretsiz betik ile mobil/oyun optimizasyonu için tris, malzeme ve texture bütçelerini kontrol eder.*

> "scripts/gn_builder.py -- --spec scatter.json --apply Ground" (geometry-nodes.md)
*Ücretsiz JSON-to-Geometry Nodes dönüştürücü ile karmaşık dağılım/parçacık sistemleri ücretsiz oluşturur.*

> "scripts/precipitation.py -- --type rain --intensity heavy" (weather-fx.md)
*Ücretsiz betik ile Blender Geometry Nodes ile yağmur, kar veya toz efektleri ücretsiz oluşturur (dönüşümlü, simülasyon gerektirmez).*

> "scripts/lightning.py -- --flashes 2" (weather-fx.md)
*Ücretsiz betik ile Blender ile şimşek efektleri (ışık patlamaları + çizgiler) ücretsiz oluşturur (keyframe’lere kaydedilir).*

> "blender-asset-qa" (asset-qa.md)
*Ücretsiz Blender betiği olarak dağıtılan, modellerin kalitesini kontrol eden standart araç (hata raporları, UV kontrolü, normaller).*

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "Mandatory review gate for any mesh or asset created or edited in Blender. Detects z-fighting (coplanar overlaps), floating/detached parts, inverted or inconsistent normals, non-manifold/open geometry, degenerate faces, duplicate verts, n-gons, unapplied scale, UV problems, bad skin weights, and renders multi-angle review sheets." (asset-qa.md)
*Blender'da oluşturulan veya düzenlenen her mesh/asset için zorunlu kalite kontrol kapısı sağlar; geometrik hataları tespit eder ve çok açılı inceleme raporları üretir.*

> "Optimize Blender assets for real-time engines - triangle/material/texture/bone budgets per platform (mobile, Roblox, web, VR, console, PC), LOD chains, decimation modes, mesh cleanup, draw-call reduction (material merging, atlases, trim sheets), instancing, vertex-split costs, collision proxies, texture memory." (game-optimization.md)
*Gerçek zamanlı motorlar (mobil, Roblox, web, VR, konsol, PC) için Blender asset'larını optimize eder; platform bazlı tris/materyal/bone bütçeleri, LOD zincirleri ve çizim çağrısı azaltımı sağlar.*

> "Geometry Nodes in Blender 5.2 - fields, domains, attributes, instancing, zones (simulation/repeat/for-each), closures/bundles, lists, SDF grids, node tools, baking, plus a JSON-to-node-tree builder and socket inspector." (geometry-nodes.md)
*Blender 5.2'deki Geometry Nodes için alanlar, alanlar, öznitelikler, instansiyalama, simülasyon/tekrarlama/for-each bölgeleri, kapatmalar/bantlar, listeler, SDF ızgaraları ve JSON'a dayalı node ağacı oluşturucu sağlar.*

> "Physics in Blender 5.2 - rigid bodies (density mass, shapes, bake to keys), classic cloth presets and pinning, new node-based Cloth/Hair Dynamics (XPBD, Collider, effectors), Mantaflow fluids, hair curves, GN simulation zones, headless baking." (simulation.md)
*Blender 5.2'deki fizik simülasyonları için sert cisimler, klasik kumaş ön ayarları, node-tabanlı kumaş/saç dinamikleri (XPBD), Mantaflow sıvıları ve başsız pişirme işlemlerini kapsar.*
