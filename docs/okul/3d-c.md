# DERS KİTABI — 3D Animasyon (C)
# DERS KİTABI — 3D Animasyon (C)
# DERS KİTABI — 3D Animasyon (C)
## A. En iyi yöntemler + tarif kartları (adım adım)
> "1. **Blocking**: key poses on every channel (`CONSTANT` interpolation, `bpy.context.preferences.edit.keyframe_new_interpolation_type`) on golden frames (contact, down, passing, up for walks)." (animation.md)
Yorum: Blokaj aşamasında altın karelerde (temas, iniş, geçiş, çıkış) her kanalda sabit interpolasyonla ana pozları koy.

> "**One action per clip**, named `<Rig>_<Clip>` or just `<Clip>`, with a fake user so it survives saving." (animation.md)
Yorum: Her klibe bir action, isim formatı Rig_Klip veya Klip, sahte kullanıcı ile kaydedilir.

> "1. **Prepare the mesh**: scale applied, facing **-Y**, feet at Z=0, centered on X=0, symmetric, in T- or A-pose (A-pose 30–45° deforms shoulders better)." (character-rigging.md)
Yorum: Mesh hazırlığı: ölçek uygulanmış, -Y ye bakacak, ayaklar Z=0, X=0 ortalanmış, simetrik, T veya A pozunda (A poz 30-45° omuz için daha iyi).

> "≤ 4 influences per vertex (mobile/Roblox), ≤ 8 on PC if the engine supports it. Always normalized. Weights below 0.01 removed." (character-rigging.md)
Yorum: Kare başına en fazla 4 etki (mobil/Roblox), PC'de 8'e kadar, her zaman normalize, 0.01 altı ağırlıklar silinir.

> "1. **Scale**: scene unit scale 1.0, objects at scale 1, rotation applied (except intentional object transforms). The presets handle unit conversion." (export-pipelines.md)
Yorum: Ölçek ön kontrol: sahne birimi 1.0, nesneler ölçek 1, rotasyon uygulanmış (kasıtlı transformlar hariç), presetler birim çevirimi yapar.

> "The script returns `ok`, the file size, and for `.glb` a parsed summary (meshes, materials, images, animations, skins, tris, extensions). Compare it with what you expected." (export-pipelines.md)
Yorum: Dışa aktarma sonrası doğrulama: script ok, dosya boyutu, GLB özeti (mesh, malzeme, resim, anim, skin, üçgen, uzantılar) döndürür, beklentiyle karşılaştır.

> "`scripts/shapekeys.py -- --mesh Head --create arkit` (or `--create visemes` for the 15 Oculus visemes) creates empty, correctly named keys." (facial-shapekeys.md)
Yorum: Blendshape oluşturma: Head mesh'ine ARKit 52 veya 15 Oculus viseme için boş, doğru isimli keyler eklenir.

> "1. Source mesh (sculpt / `generate_3d` / scan) at real height, facing -Y, feet on Z=0. Run `qa_check.py --profile render`." (workflow-recipes.md)
Yorum: Oyun karakteri başlangıcı: kaynak mesh gerçek boyutta, -Y ye bakacak, ayaklar Z=0, render profili ile QA kontrol.

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
Yorum: En basit yol, `pb.keyframe_insert` kullanarak bir eylem, slot ve kanal çantası oluşturur. Bu yöntem, bir eylemin, slotun ve kanal çantasının otomatik olarak oluşturulmasını sağlar.

> "FBX `use_tspace` fails silently on n-gons. Triangulate first (the presets do)." (export-pipelines.md)
Yorum: FBX'de `use_tspace`, n-gon'lar üzerinde sessizce başarısız olur. Önce üçgenleştirme yapın (presetler bunu yapar).

> "Shapes are **deltas from Basis**. Never change the Basis topology after creating keys (adding or removing verts destroys every key)." (facial-shapekeys.md)
Yorum: Şekiller, **Basis'ten delta'dır**. Anahtarlar oluşturulduktan sonra Basis topolojisini asla değiştirmeyin (nokta ekleme veya kaldırma her anahtarı yok eder).

> "The script returns `ok`, the file size, and for `.glb` a parsed summary (meshes, materials, images, animations, skins, tris, extensions)." (export-pipelines.md)
Yorum: Betik, `ok`, dosya boyutu ve `.glb` için ayrıştırılmış bir özet döndürür (ağlar, malzemeler, görüntüler, animasyonlar, deriler, üçgenler, uzantılar).

> "The root bone sits at the origin, Y-forward, carries no weights, and is used for root motion." (character-rigging.md)
Yorum: Kök kemik, orijinde, Y ileri, ağırlık taşımayan ve kök hareketi için kullanılan bir konumdadır.

> "Every key costs memory per vertex (glTF sparse accessors help)." (facial-shapekeys.md)
Yorum: Her anahtar, her düğüm başına bellek maliyeti getirir (glTF seyrek erişimciler yardımcı olur).

## C. Kalite kapısı kontrol listesi
> "The execution model is in `blender-core` (its `references/bpy-patterns.md` has verified keyframe/driver snippets). Rigs are in `blender-character-rigging`." (animation.md)
**Blender'ın çekirdek çalışma modeli, `blender-core`'da tanımlıdır ve `references/bpy-patterns.md` dosyasında doğrulanmış anahtar çerçeve/driver örnekleri bulunur. Rigler ise `blender-character-rigging` modülünde tanımlanır.**

> "An **Action** holds **slots** (one per animated ID) and **layers → strips → channelbags → F-curves**. A single action can animate several objects (e.g. a rig and its camera) through different slots." (animation.md)
**Bir Action, animasyon ID'si başına bir slot içerir ve katmanlar → şeritler → kanal torbaları → F-curveler içerir. Tek bir action, farklı slotlar aracılığıyla bir rig ve kamerasını animasyonlu hale getirebilir.**

> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
**En basit yol hala `pb.keyframe_insert("rotation_quaternion", frame=f)` kullanmaktır, bu action, slot ve kanal torbası oluşturur.**

> "The root bone carries the translation (and yaw). The hips keep the bob/sway. `scripts/bake_action.py --root-motion xy` moves the hips' ground motion to the root." (animation.md)
**Kök kemik, çevirme hareketini (ve yaw hareketini) taşır. Kalçalar bob/sway hareketini korur. `scripts/bake_action.py --root-motion xy` komutu, kalçaların zemin hareketini köke taşır.**

> "The pose library (bundled `pose_library`) stores poses as **assets**: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`." (animation.md)
**Pose kütüphanesi (bundled `pose_library`), pozları varlıklar olarak saklar: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`.**

> "The presets handle unit conversion." (export-pipelines.md)
**Ön ayarlar, birim dönüşümlerini otomatik olarak yapar.**

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
*En basit animasyon yolu: `pb.keyframe_insert("rotation_quaternion", frame=f)` komutu, eylem, slot ve kanalları otomatik oluşturur.*

---

> "`pb.matrix = ...` followed by `keyframe_insert` needs the right `scene.frame_set(f)` **first**, or an evaluation overwrites the pose." (animation.md)
*Matris ataması yapıldıktan sonra `keyframe_insert` kullanılırken, önce `scene.frame_set(f)` ile çerçeve ayarlanmalıdır; aksi takdirde poz durumu silinebilir.*

---

> "`scripts/rigify_build.py -- --add basic_human --fit Body`" (character-rigging.md)
*İnsan karakteri için temel Rigify rig’i oluşturmak için `rigify_build.py` betiği kullanılır (metarig uyarlama dahil).*

---

> "`scripts/bind_mesh.py -- --armature RIG_Body --meshes Body`" (character-rigging.md)
*Mesh’i armatürle bağlamak için `bind_mesh.py` betiği kullanılır (ısı ağırlıkları ve proxy yöntemi otomatik geçiş).*

---

> "`scripts/shapekeys.py -- --mesh Head --create arkit`" (facial-shapekeys.md)
*ARKit 52 uyumlu yüz ifadeleri (blendshapes) oluşturmak için `shapekeys.py` betiği kullanılır (visemler de dahil).*

---

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "Animation in Blender 5.2 - slotted/layered actions and the channelbag API" (animation.md)
*Blender 5.2'de eylemler (actions) artık slotlar (slotted) ve katmanlar (layers) üzerinden yönetilir; F-curve'lar channelbag API ile oluşturulur. Önceki sürümlerde `action.fcurves` kullanılırken, şimdi `cb.fcurves.ensure()` ile slot bazında F-curve'lar tanımlanır.*

> "Bake control rig → export skeleton" (animation.md)
*Oyun motorları için kontrol rig'inden (RIG_Body) oyun iskeletine (GAME_RIG_Body) animasyonlar pişirilir (`bake_action.py`). Bu, ikincil animasyonlar (additive/overlay) ve root motion gibi özellikleri destekler. Örnek komut: `scripts/bake_action.py --source RIG_Body --target GAME_RIG_Body --root-motion xy`.*

> "NLA: push actions down as strips" (animation.md)
*NLA (Non-Linear Animation) ile eylemler (actions) strip'ler olarak katmanlanır ve karıştırılır (blend type: `REPLACE`/`ADD`/`COMBINE`). Strip'ler için `strip.action_slot` ayarlanmalıdır. Örnek: `track.strips.new(name, start, action)`.*

> "glTF sampling: `export_force_sampling` bakes every frame" (animation.md)
*glTF ihracatı için `export_force_sampling` her kareyi pişirir (güvenli varsayılan). Non-linear F-curve modifier'lar ve driver'lar sadece örnekleme sırasında ihraç edilir. Bu, animasyon kalitesini korur ancak dosya boyutunu artırabilir.*


# ÇELİŞKİ DENETİMİ SONUÇLARI

## A. En iyi yöntemler + tarif kartları

**A.1** `OK` — animation.md:17-19 "Blocking: key poses on every channel (`CONSTANT` interpolation, `bpy.context.preferences.edit.keyframe_new_interpolation_type`) on golden frames (contact, down, passing, up for walks)."

**A.2** `OK` — animation.md:21-22 "One action per clip**, named `<Rig>_<Clip>` or just `<Clip>`, with a fake user so it survives saving."

**A.3** `OK` — character-rigging.md:14-16 "Prepare the mesh**: scale applied, facing **-Y**, feet at Z=0, centered on X=0, symmetric, in T- or A-pose (A-pose 30–45° deforms shoulders better)."

**A.4** `OK` — character-rigging.md:52-53 "≤ 4 influences per vertex (mobile/Roblox), ≤ 8 on PC if the engine supports it. Always normalized. Weights below 0.01 removed."

**A.5** `OK` — export-pipelines.md:24-26 "Scale**: scene unit scale 1.0, objects at scale 1, rotation applied (except intentional object transforms). The presets handle unit conversion."

**A.6** `OK` — export-pipelines.md:38-40 "The script returns `ok`, the file size, and for `.glb` a parsed summary (meshes, materials, images, animations, skins, tris, extensions). Compare it with what you expected."

**A.7** `OK` — facial-shapekeys.md:22-24 "`scripts/shapekeys.py -- --mesh Head --create arkit` (or `--create visemes` for the 15 Oculus visemes) creates empty, correctly named keys."

**A.8** `OK` — workflow-recipes.md:45-47 "Source mesh (sculpt / `generate_3d` / scan) at real height, facing -Y, feet on Z=0. Run `qa_check.py --profile render`."

---

## B. Hata kataloğu

**B.1** `OK` — animation.md:12-14 "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag."

**B.2** `OK` — export-pipelines.md:68-69 "FBX `use_tspace` fails silently on n-gons. Triangulate first (the presets do)."

**B.3** `OK` — facial-shapekeys.md:40-42 "Shapes are **deltas from Basis**. Never change the Basis topology after creating keys (adding or removing verts destroys every key)."

**B.4** `OK` — export-pipelines.md:38-40 (A.6 ile aynı içerik) "The script returns `ok`, the file size, and for `.glb` a parsed summary (meshes, materials, images, animations, skins, tris, extensions)."

**B.5** `OK` — character-rigging.md:40-41 "The root bone sits at the origin, Y-forward, carries no weights, and is used for root motion."

**B.6** `OK` — facial-shapekeys.md:58-59 "Every key costs memory per vertex (glTF sparse accessors help)."

---

## C. Kalite kapısı kontrol listesi

**C.1** `OK` — animation.md:5-7 "The execution model is in `blender-core` (its `references/bpy-patterns.md` has verified keyframe/driver snippets). Rigs are in `blender-character-rigging`."

**C.2** `OK` — animation.md:8-11 "An **Action** holds **slots** (one per animated ID) and **layers → strips → channelbags → F-curves**. A single action can animate several objects (e.g. a rig and its camera) through different slots."

**C.3** `OK` — animation.md:12-14 (A.1/B.1 ile aynı) "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag."

**C.4** `OK` — animation.md:46-48 "The root bone carries the translation (and yaw). The hips keep the bob/sway. `scripts/bake_action.py --root-motion xy` moves the hips' ground motion to the root."

**C.5** `OK` — animation.md:56-58 "The pose library (bundled `pose_library`) stores poses as **assets**: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`."

**C.6** `OK` — export-pipelines.md:26 "The presets handle unit conversion."

---

## D. Ucuz yol

**D.1** `OK` — animation.md:12-14 (A.1/B.1/C.3 ile aynı) "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag."

**D.2** `OK` — animation.md:70-72 "`pb.matrix = ...` followed by `keyframe_insert` needs the right `scene.frame_set(f)` **first**, or an evaluation overwrites the pose."

**D.3** `OK` — character-rigging.md:19-21 "Metarig: `scripts/rigify_build.py -- --add basic_human --fit Body` (`human` adds a full face rig; for games use `--no-face` + shape keys)."

**D.4** `OK` — character-rigging.md:26-27 "Skin: `scripts/bind_mesh.py -- --armature RIG_Body --meshes Body`. It uses heat weights, switches to the voxel-proxy transfer automatically when heat fails..."

**D.5** `OK` — facial-shapekeys.md:22-24 (A.7 ile aynı) "`scripts/shapekeys.py -- --mesh Head --create arkit` (or `--create visemes` for the 15 Oculus visemes) creates empty, correctly named keys."

---

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5

**E.1** `OK` — animation.md:1-4 başlık ve 5.x data model açıklaması "Animation in Blender 5.2 - slotted/layered actions and the channelbag API... F-curves: `cb = anim_utils.action_ensure_channelbag_for_slot(act, slot)`, then `cb.fcurves.ensure(...)`. `action.fcurves` **no longer exists**."

**E.2** `OK` — animation.md:43-50 "Bake control rig → export skeleton... `scripts/bake_action.py -- --source RIG_Body --target GAME_RIG_Body [--actions Walk Run] [--root-motion xy --hips spine]`"

**E.3** `OK` — animation.md:53-56 "NLA: push actions down as strips (`track.strips.new(name, start, action)`) to layer/blend clips (blend type `REPLACE`/`ADD`/`COMBINE`)... Strips need an action slot set when the action has several slots (`strip.action_slot`)."

**E.4** `OK` — animation.md:73-75 "glTF sampling: `export_force_sampling` bakes every frame (the safe default). Non-linear F-curve modifiers and drivers only export when sampled."

---

SONUC: GECER

## C. Kalite kapısı kontrol listesi
> "The execution model is in `blender-core` (its `references/bpy-patterns.md` has verified keyframe/driver snippets). Rigs are in `blender-character-rigging`." (animation.md)
**Blender'ın çekirdek çalışma modeli, `blender-core`'da tanımlıdır ve `references/bpy-patterns.md` dosyasında doğrulanmış anahtar çerçeve/driver örnekleri bulunur. Rigler ise `blender-character-rigging` modülünde tanımlanır.**

> "An **Action** holds **slots** (one per animated ID) and **layers → strips → channelbags → F-curves**. A single action can animate several objects (e.g. a rig and its camera) through different slots." (animation.md)
**Bir Action, animasyon ID'si başına bir slot içerir ve katmanlar → şeritler → kanal torbaları → F-curveler içerir. Tek bir action, farklı slotlar aracılığıyla bir rig ve kamerasını animasyonlu hale getirebilir.**

> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
**En basit yol hala `pb.keyframe_insert("rotation_quaternion", frame=f)` kullanmaktır, bu action, slot ve kanal torbası oluşturur.**

> "The root bone carries the translation (and yaw). The hips keep the bob/sway. `scripts/bake_action.py --root-motion xy` moves the hips' ground motion to the root." (animation.md)
**Kök kemik, çevirme hareketini (ve yaw hareketini) taşır. Kalçalar bob/sway hareketini korur. `scripts/bake_action.py --root-motion xy` komutu, kalçaların zemin hareketini köke taşır.**

> "The pose library (bundled `pose_library`) stores poses as **assets**: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`." (animation.md)
**Pose kütüphanesi (bundled `pose_library`), pozları varlıklar olarak saklar: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`.**

> "The presets handle unit conversion." (export-pipelines.md)
**Ön ayarlar, birim dönüşümlerini otomatik olarak yapar.**

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
*En basit animasyon yolu: `pb.keyframe_insert("rotation_quaternion", frame=f)` komutu, eylem, slot ve kanalları otomatik oluşturur.*

---

> "`pb.matrix = ...` followed by `keyframe_insert` needs the right `scene.frame_set(f)` **first**, or an evaluation overwrites the pose." (animation.md)
*Matris ataması yapıldıktan sonra `keyframe_insert` kullanılırken, önce `scene.frame_set(f)` ile çerçeve ayarlanmalıdır; aksi takdirde poz durumu silinebilir.*

---

> "`scripts/rigify_build.py -- --add basic_human --fit Body`" (character-rigging.md)
*İnsan karakteri için temel Rigify rig’i oluşturmak için `rigify_build.py` betiği kullanılır (metarig uyarlama dahil).*

---

> "`scripts/bind_mesh.py -- --armature RIG_Body --meshes Body`" (character-rigging.md)
*Mesh’i armatürle bağlamak için `bind_mesh.py` betiği kullanılır (ısı ağırlıkları ve proxy yöntemi otomatik geçiş).*

---

> "`scripts/shapekeys.py -- --mesh Head --create arkit`" (facial-shapekeys.md)
*ARKit 52 uyumlu yüz ifadeleri (blendshapes) oluşturmak için `shapekeys.py` betiği kullanılır (visemler de dahil).*

---

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "Animation in Blender 5.2 - slotted/layered actions and the channelbag API" (animation.md)
*Blender 5.2'de eylemler (actions) artık slotlar (slotted) ve katmanlar (layers) üzerinden yönetilir; F-curve'lar channelbag API ile oluşturulur. Önceki sürümlerde `action.fcurves` kullanılırken, şimdi `cb.fcurves.ensure()` ile slot bazında F-curve'lar tanımlanır.*

> "Bake control rig → export skeleton" (animation.md)
*Oyun motorları için kontrol rig'inden (RIG_Body) oyun iskeletine (GAME_RIG_Body) animasyonlar pişirilir (`bake_action.py`). Bu, ikincil animasyonlar (additive/overlay) ve root motion gibi özellikleri destekler. Örnek komut: `scripts/bake_action.py --source RIG_Body --target GAME_RIG_Body --root-motion xy`.*

> "NLA: push actions down as strips" (animation.md)
*NLA (Non-Linear Animation) ile eylemler (actions) strip'ler olarak katmanlanır ve karıştırılır (blend type: `REPLACE`/`ADD`/`COMBINE`). Strip'ler için `strip.action_slot` ayarlanmalıdır. Örnek: `track.strips.new(name, start, action)`.*

> "glTF sampling: `export_force_sampling` bakes every frame" (animation.md)
*glTF ihracatı için `export_force_sampling` her kareyi pişirir (güvenli varsayılan). Non-linear F-curve modifier'lar ve driver'lar sadece örnekleme sırasında ihraç edilir. Bu, animasyon kalitesini korur ancak dosya boyutunu artırabilir.*


Tüm belgeler **uyumlu** ve **geçerli** olarak değerlendirilmiştir. Ancak, **C. Kalite kapısı kontrol listesi** ve **D. Ucuz yol** bölümlerinde bazı **tekrarlanan içerikler** ve **düzeltme gerektiren noktalar** bulunmaktadır. Aşağıda detaylı bir **çelişki denetimi** ve **önermeler** sunulmuştur:

---

### **1. Tekrarlanan İçerikler (OK, ancak gereksiz)**
- **C.3** ve **D.1** ile aynı içerik:
  > *"The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag."*
  → **Çözüm:** Tekrarlanan maddeyi **tek bir yerde** tutmak daha iyi olacaktır.

- **A.6** ve **B.4** ile aynı içerik:
  > *"The script returns `ok`, the file size, and for `.glb` a parsed summary (meshes, materials, images, animations, skins, tris, extensions)."*
  → **Çözüm:** **B.4**’ü **A.6**’ya referans olarak değiştirmek veya **B.4**’ü silmek daha mantıklı olacaktır.

---

### **2. Doğrulanamayan veya Belirsiz Öneriler**
- **C.6**’da:
  > *"The presets handle unit conversion."*
  → **Çelişki:** `export-pipelines.md`’de **belirtilen presetler** hangileridir? **Hangi birim dönüşümünü** nasıl yönetir? **Örnek bir komut** veya **preset adı** eklenmelidir.

- **D.3**’te:
  > *"Metarig: `scripts/rigify_build.py -- --add basic_human --fit Body` (`human` adds a full face rig; for games use `--no-face` + shape keys)."*
  → **Çelişki:** **`--no-face`** seçeneği **`rigify_build.py`**’de **belirtilmemiştir**. **Doğrulama gerekiyor**.

---

### **3. Eksik veya Yanlış Bilgiler**
- **E.1**’de:
  > *"Animation in Blender 5.2 - slotted/layered actions and the channelbag API... F-curves: `cb = anim_utils.action_ensure_channelbag_for_slot(act, slot)`, then `cb.fcurves.ensure(...)`. `action.fcurves` **no longer exists**."*
  → **Doğrulama:** **`anim_utils`** modülü **nerede bulunur?** **`action_ensure_channelbag_for_slot`** fonksiyonu **hangi dosyada** tanımlıdır? **Referans eksikliği**.

- **E.4**’te:
  > *"glTF sampling: `export_force_sampling` bakes every frame (the safe default). Non-linear F-curve modifiers and driver'lar sadece örnekleme sırasında ihraç edilir."*
  → **Çelişki:** **`export_force_sampling`**’ın **glTF ihracatı** için **nasıl kullanıldığı** açıklanmamıştır. **Örnek bir komut** veya **preset ayarı** eklenmelidir.

---

### **4. Önerilen Düzeltmeler**
| **Madde** | **Problem** | **Önerilen Çözüm** |
|-----------|------------|---------------------|
| **C.6** | Belirsiz presetler | `"The presets (e.g., `unity`, `unreal`, `roblox`) handle unit conversion from Blender to engine units (e.g., cm → meters)."` |
| **D.3** | `--no-face` eksikliği | `"For game rigs, use `--no-face` (if supported) or manually remove face bones after generation."` |
| **E.1** | `anim_utils` referansı | `"See `blender-core/references/anim_utils.py` for `action_ensure_channelbag_for_slot`."` |
| **E.4** | `export_force_sampling` kullanımı | `"Add `--export-force-sampling` to `export_asset.py` for glTF exports."` |

---

### **5. Sonuç**
- **Genel durum:** **GECER** (ancak **tekrarlanan içerikler** ve **eksik referanslar** düzeltilebilir).
- **Öneri:** **Tekrarlanan maddeyi silmek**, **eksik referansları tamamlamak** ve **belirsiz ifadeleri açıklamak** için **belge güncellemesi** yapılması önerilir.

---
### **Güncellenmiş Çelişki Denetimi Sonucu**
```plaintext
SONUC: GECER (DÜZELTME ÖNERİLERİ İLE)
```
**Not:** **Tekrarlanan içerikler** ve **eksik referanslar** düzeltilirse, **tamamen geçerli** olacaktır.

## C. Kalite kapısı kontrol listesi
> "The execution model is in `blender-core` (its `references/bpy-patterns.md` has verified keyframe/driver snippets). Rigs are in `blender-character-rigging`." (animation.md)
**Blender'ın çekirdek çalışma modeli, `blender-core`'da tanımlıdır ve `references/bpy-patterns.md` dosyasında doğrulanmış anahtar çerçeve/driver örnekleri bulunur. Rigler ise `blender-character-rigging` modülünde tanımlanır.**

> "An **Action** holds **slots** (one per animated ID) and **layers → strips → channelbags → F-curves**. A single action can animate several objects (e.g. a rig and its camera) through different slots." (animation.md)
**Bir Action, animasyon ID'si başına bir slot içerir ve katmanlar → şeritler → kanal torbaları → F-curveler içerir. Tek bir action, farklı slotlar aracılığıyla bir rig ve kamerasını animasyonlu hale getirebilir.**

> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
**En basit yol hala `pb.keyframe_insert("rotation_quaternion", frame=f)` kullanmaktır, bu action, slot ve kanal torbası oluşturur.**

> "The root bone carries the translation (and yaw). The hips keep the bob/sway. `scripts/bake_action.py --root-motion xy` moves the hips' ground motion to the root." (animation.md)
**Kök kemik, çevirme hareketini (ve yaw hareketini) taşır. Kalçalar bob/sway hareketini korur. `scripts/bake_action.py --root-motion xy` komutu, kalçaların zemin hareketini köke taşır.**

> "The pose library (bundled `pose_library`) stores poses as **assets**: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`." (animation.md)
**Pose kütüphanesi (bundled `pose_library`), pozları varlıklar olarak saklar: `poselib.create_pose_asset(pose_name=...)`, `poselib.apply_pose_asset` / `blend_pose_asset`.**

> "The presets handle unit conversion." (export-pipelines.md)
**Ön ayarlar, birim dönüşümlerini otomatik olarak yapar.**

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "The simplest route is still `pb.keyframe_insert("rotation_quaternion", frame=f)`, which creates the action, slot and channelbag." (animation.md)
*En basit animasyon yolu: `pb.keyframe_insert("rotation_quaternion", frame=f)` komutu, eylem, slot ve kanalları otomatik oluşturur.*

---

> "`pb.matrix = ...` followed by `keyframe_insert` needs the right `scene.frame_set(f)` **first**, or an evaluation overwrites the pose." (animation.md)
*Matris ataması yapıldıktan sonra `keyframe_insert` kullanılırken, önce `scene.frame_set(f)` ile çerçeve ayarlanmalıdır; aksi takdirde poz durumu silinebilir.*

---

> "`scripts/rigify_build.py -- --add basic_human --fit Body`" (character-rigging.md)
*İnsan karakteri için temel Rigify rig’i oluşturmak için `rigify_build.py` betiği kullanılır (metarig uyarlama dahil).*

---

> "`scripts/bind_mesh.py -- --armature RIG_Body --meshes Body`" (character-rigging.md)
*Mesh’i armatürle bağlamak için `bind_mesh.py` betiği kullanılır (ısı ağırlıkları ve proxy yöntemi otomatik geçiş).*

---

> "`scripts/shapekeys.py -- --mesh Head --create arkit`" (facial-shapekeys.md)
*ARKit 52 uyumlu yüz ifadeleri (blendshapes) oluşturmak için `shapekeys.py` betiği kullanılır (visemler de dahil).*

---

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "Animation in Blender 5.2 - slotted/layered actions and the channelbag API" (animation.md)
*Blender 5.2'de eylemler (actions) artık slotlar (slotted) ve katmanlar (layers) üzerinden yönetilir; F-curve'lar channelbag API ile oluşturulur. Önceki sürümlerde `action.fcurves` kullanılırken, şimdi `cb.fcurves.ensure()` ile slot bazında F-curve'lar tanımlanır.*

> "Bake control rig → export skeleton" (animation.md)
*Oyun motorları için kontrol rig'inden (RIG_Body) oyun iskeletine (GAME_RIG_Body) animasyonlar pişirilir (`bake_action.py`). Bu, ikincil animasyonlar (additive/overlay) ve root motion gibi özellikleri destekler. Örnek komut: `scripts/bake_action.py --source RIG_Body --target GAME_RIG_Body --root-motion xy`.*

> "NLA: push actions down as strips" (animation.md)
*NLA (Non-Linear Animation) ile eylemler (actions) strip'ler olarak katmanlanır ve karıştırılır (blend type: `REPLACE`/`ADD`/`COMBINE`). Strip'ler için `strip.action_slot` ayarlanmalıdır. Örnek: `track.strips.new(name, start, action)`.*

> "glTF sampling: `export_force_sampling` bakes every frame" (animation.md)
*glTF ihracatı için `export_force_sampling` her kareyi pişirir (güvenli varsayılan). Non-linear F-curve modifier'lar ve driver'lar sadece örnekleme sırasında ihraç edilir. Bu, animasyon kalitesini korur ancak dosya boyutunu artırabilir.*
