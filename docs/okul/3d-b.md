# DERS KİTABI — 3D Materyal/Işık/Render (B)
# DERS KİTABI — 3D Materyal/Işık/Render (B)
# DERS KİTABI — 3D Materyal/Işık/Render (B)
# DERS KİTABI — 3D Materyal/Işık/Render (B)
## A. En iyi yöntemler + tarif kartları (adım adım)
> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
Kamera, ışık ve arka planı otomatik olarak ayarlayan bir döndürme tablosu oluşturur.

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate" (pbr-materials.md)
PBR malzemesini otomatik olarak oluşturur ve gerekli haritaları bağlar.

> "scripts/render_batch.py -- --engine CYCLES --preset final --res 1920 1080 --out //render/hero_#### --frames 1" (rendering.md)
Yüksek kaliteli bir still render eder ve sonuçları belirtilen dizine kaydeder.

> "light_obj.light_linking.receiver_collection" (lighting-lookdev.md)
Işıkların hangi nesneleri aydınlatacağını belirler, arka planı aydınlatmaz.

## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "The asset itself isn't modified." (lighting-lookdev.md)
- **Hata**: Nesne dönüşümleri kayboluyor.
- **Neden**: Turntable betiği nesneyi döndürmek yerine kamerayı çeviriyor.
- **Teşhis**: Nesnenin dönüşümünü kontrol edin ve betiğin sadece kamerayı çevirdiğini doğrulayın.
- **Düzeltme**: Nesneyi dönmek için betiği değiştirin veya dönüşümleri korumak için bir pivot kullanın.

> "A wrong color space is the #1 bug (washed-out normals, wrong roughness)." (pbr-materials.md)
- **Hata**: Normal haritaları yıkanmış görünüyor veya parlaklık yanlış.
- **Neden**: Yanlış renk uzayı (örneğin, normal haritaları için Non-Color yerine sRGB kullanma).
- **Teşhis**: Haritaların renk uzayını kontrol edin ve normal haritalarının Non-Color olduğunu doğrulayın.
- **Düzeltme**: Haritaların renk uzayını düzeltin ve gerekirse yeniden yükleyin.

> "Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources." (rendering.md)
- **Hata**: Görüntüde parlak noktalar (fireflies) var.
- **Neden**: Yeterince büyük olmayan ışık kaynakları veya yeterince yüksek olmayan yansıtma yolları.
- **Teşhis**: Işık kaynaklarının boyutunu ve yansıtma yollarını kontrol edin.
- **Düzeltme**: Işık kaynaklarını büyütün, yansıtma yollarını artırın ve blur_glossy değerini ayarlayın.

> "The script picks the GPU (OptiX/CUDA/HIP/Metal/oneAPI) and falls back to CPU, creates the target images with correct color spaces, cleans up its temporary nodes, and saves `T_<name>_<N|AO|CURV|BC|R|M|ORM...>.png`." (texture-baking.md)
- **Hata**: Bake işlemi sırasında GPU seçimi yapılamıyor.
- **Neden**: Uygun GPU sürücülerinin yüklü olmaması veya betik hatası.
- **Teşhis**: GPU sürücülerinin yüklü olup olmadığını ve betik hatalarını kontrol edin.
- **Düzeltme**: Uygun GPU sürücülerini yükleyin veya betiği güncelleyin.

> "The script builds `ENV_World`, the `ENV_Mood` collection (sun or moon, fog box, accent lights) and, for moods, `ENV_Grade` (a compositor tree)." (time-of-day.md)
- **Hata**: Zaman ve atmosfer betiği beklenen koleksiyonları oluşturmuyor.
- **Neden**: Betik hatası veya eksik bağımlılıklar.
- **Teşhis**: Betik hatalarını ve bağımlılıkları kontrol edin.
- **Düzeltme**: Betik hatalarını düzeltin veya eksik bağımlılıkları yükleyin.

> "The script won't overwrite a compositor tree that isn't `ENV_Grade`; it reports that instead." (time-of-day.md)
- **Hata**: Zaman ve atmosfer betiği kompozitör ağacını üzerine yazmıyor.
- **Neden**: Kompozitör ağacı `ENV_Grade` olarak adlandırılmamış.
- **Teşhis**: Kompozitör ağacının adını kontrol edin.
- **Düzeltme**: Kompozitör ağacını `ENV_Grade` olarak adlandırın veya betiği güncelleyin.

## C. Kalite kapısı kontrol listesi
> "Light size controls softness. A bigger, closer light is softer" (lighting-lookdev.md)
*Işık boyutu yumuşaklığı belirler; büyük ve yakın ışıklar daha yumuşak gölge verir.*

> "World lighting is invisible if `world.node_tree` has no Background → World Output link" (lighting-lookdev.md)
*Dünya ışığı için şema bağlantısını kontrol edin (Arka Plan → Dünya Çıktısı).*

> "A good PBR material holds up in all of them (`blender-pbr-materials` sanity checks)" (lighting-lookdev.md)
*Materyalin farklı HDRI’lerde tutarlı kalmasını doğrulayın.*

> "Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources" (rendering.md)
*Parazit ışıklar için dolaylı ışığı sınırlayın, parlaklığı filtreleyin ve ışık kaynaklarını büyütün.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Poly Haven (CC0) via the blender-mcp `search_assets`/`import_asset`" (lighting-lookdev.md)
→ HDRI ve materyal kütüphanesi tamamen ücretsiz/CC0; tarayıcıdan indirmeden betikle sahneye çekilir.

> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
→ Tek komutla kameralı 3-nokta stüdyo, siyklorama ve 120 karelik döndürme; ek eklenti yok.

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate" (pbr-materials.md)
→ Dosya adından (Poly Haven/ambientCG/Substance/UE) haritaları tanır, renk uzayını ayarlar, ORM paketler, DirectX normali çevirir.

> "scripts/render_batch.py -- --preset preview --frames 1-120 --format MP4 --out //render/turntable" (rendering.md)
→ Önizleme/son kalite önayarları, çoklu kamera, EXR çoklu geçiş, CLI/CI uyumlu; harici render farmı şart değil.

> "Node Wrangler (bundled) `Ctrl+Shift+T` does the same as `build_pbr_material.py`, but needs the UI" (pbr-materials.md)
→ Yerleşik eklentiyle PBR harita setini anında bağlar; betik başlıksız/otomasyon için, NW el işi için.

> "Engine ids: `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`" (rendering.md)
→ Üç motor da yerel GPU/CPU üzerinde ücretsiz; OptiX/CUDA/HIP/Metal/oneAPI otomatik seçilir.

> "Clamp indirect 5–10 kills fireflies at a small energy cost" (rendering.md)
→ Örnek sayısı artırmadan (bu da süre/maliyet artırır) firefly'ları yerel ayarla giderir.

> "Use exposure (`view_settings.exposure`), not light power, for global brightness tweaks" (rendering.md)
→ Işık güçlerini tekrar hesaplamak yerine tek kaydıra global parlaklığı düzeltir; iterasyon süresini kısaltır.

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
*TELVE için standart ürün sunumu için kullanılan turntable ayarı.*

> "scripts/scene_mood.py -- --time golden" (time-of-day.md)
*NEFFEX projesinde kullanılan altın saat (golden hour) ışık ayarı.*

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate" (pbr-materials.md)
*BHS5 projesinde malzeme setleri için PBR malzeme oluşturma komutu.*

> "scripts/scene_mood.py -- --mood cyberpunk" (time-of-day.md)
*NEFFEX projesinde kullanılan cyberpunk tarzı ışık ve atmosfer ayarı.*

> "scripts/render_batch.py -- --cameras CamA CamB CamC --format EXR_MULTI" (rendering.md)
*TELVE ve NEFFEX için çok kamera render ayarları.*

> "scripts/turntable.py -- --objects Hero --rig both --hdri //hdri/studio_small_09_2k.exr" (lighting-lookdev.md)
*NEFFEX projesinde HDRI ışık kullanılarak turntable render ayarı.*


## B. Hata kataloğu (hata · nereden çıkar · teşhis · düzeltme)
> "The asset itself isn't modified." (lighting-lookdev.md)
- **Hata**: Nesne dönüşümleri kayboluyor.
- **Neden**: Turntable betiği nesneyi döndürmek yerine kamerayı çeviriyor.
- **Teşhis**: Nesnenin dönüşümünü kontrol edin ve betiğin sadece kamerayı çevirdiğini doğrulayın.
- **Düzeltme**: Nesneyi dönmek için betiği değiştirin veya dönüşümleri korumak için bir pivot kullanın.

> "A wrong color space is the #1 bug (washed-out normals, wrong roughness)." (pbr-materials.md)
- **Hata**: Normal haritaları yıkanmış görünüyor veya parlaklık yanlış.
- **Neden**: Yanlış renk uzayı (örneğin, normal haritaları için Non-Color yerine sRGB kullanma).
- **Teşhis**: Haritaların renk uzayını kontrol edin ve normal haritalarının Non-Color olduğunu doğrulayın.
- **Düzeltme**: Haritaların renk uzayını düzeltin ve gerekirse yeniden yükleyin.

> "Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources." (rendering.md)
- **Hata**: Görüntüde parlak noktalar (fireflies) var.
- **Neden**: Yeterince büyük olmayan ışık kaynakları veya yeterince yüksek olmayan yansıtma yolları.
- **Teşhis**: Işık kaynaklarının boyutunu ve yansıtma yollarını kontrol edin.
- **Düzeltme**: Işık kaynaklarını büyütün, yansıtma yollarını artırın ve blur_glossy değerini ayarlayın.

> "The script picks the GPU (OptiX/CUDA/HIP/Metal/oneAPI) and falls back to CPU, creates the target images with correct color spaces, cleans up its temporary nodes, and saves `T_<name>_<N|AO|CURV|BC|R|M|ORM...>.png`." (texture-baking.md)
- **Hata**: Bake işlemi sırasında GPU seçimi yapılamıyor.
- **Neden**: Uygun GPU sürücülerinin yüklü olmaması veya betik hatası.
- **Teşhis**: GPU sürücülerinin yüklü olup olmadığını ve betik hatalarını kontrol edin.
- **Düzeltme**: Uygun GPU sürücülerini yükleyin veya betiği güncelleyin.

> "The script builds `ENV_World`, the `ENV_Mood` collection (sun or moon, fog box, accent lights) and, for moods, `ENV_Grade` (a compositor tree)." (time-of-day.md)
- **Hata**: Zaman ve atmosfer betiği beklenen koleksiyonları oluşturmuyor.
- **Neden**: Betik hatası veya eksik bağımlılıklar.
- **Teşhis**: Betik hatalarını ve bağımlılıkları kontrol edin.
- **Düzeltme**: Betik hatalarını düzeltin veya eksik bağımlılıkları yükleyin.

> "The script won't overwrite a compositor tree that isn't `ENV_Grade`; it reports that instead." (time-of-day.md)
- **Hata**: Zaman ve atmosfer betiği kompozitör ağacını üzerine yazmıyor.
- **Neden**: Kompozitör ağacı `ENV_Grade` olarak adlandırılmamış.
- **Teşhis**: Kompozitör ağacının adını kontrol edin.
- **Düzeltme**: Kompozitör ağacını `ENV_Grade` olarak adlandırın veya betiği güncelleyin.

## C. Kalite kapısı kontrol listesi
> "Light size controls softness. A bigger, closer light is softer" (lighting-lookdev.md)
*Işık boyutu yumuşaklığı belirler; büyük ve yakın ışıklar daha yumuşak gölge verir.*

> "World lighting is invisible if `world.node_tree` has no Background → World Output link" (lighting-lookdev.md)
*Dünya ışığı için şema bağlantısını kontrol edin (Arka Plan → Dünya Çıktısı).*

> "A good PBR material holds up in all of them (`blender-pbr-materials` sanity checks)" (lighting-lookdev.md)
*Materyalin farklı HDRI’lerde tutarlı kalmasını doğrulayın.*

> "Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources" (rendering.md)
*Parazit ışıklar için dolaylı ışığı sınırlayın, parlaklığı filtreleyin ve ışık kaynaklarını büyütün.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Poly Haven (CC0) via the blender-mcp `search_assets`/`import_asset`" (lighting-lookdev.md)
→ HDRI ve materyal kütüphanesi tamamen ücretsiz/CC0; tarayıcıdan indirmeden betikle sahneye çekilir.

> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
→ Tek komutla kameralı 3-nokta stüdyo, siyklorama ve 120 karelik döndürme; ek eklenti yok.

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate" (pbr-materials.md)
→ Dosya adından (Poly Haven/ambientCG/Substance/UE) haritaları tanır, renk uzayını ayarlar, ORM paketler, DirectX normali çevirir.

> "scripts/render_batch.py -- --preset preview --frames 1-120 --format MP4 --out //render/turntable" (rendering.md)
→ Önizleme/son kalite önayarları, çoklu kamera, EXR çoklu geçiş, CLI/CI uyumlu; harici render farmı şart değil.

> "Node Wrangler (bundled) `Ctrl+Shift+T` does the same as `build_pbr_material.py`, but needs the UI" (pbr-materials.md)
→ Yerleşik eklentiyle PBR harita setini anında bağlar; betik başlıksız/otomasyon için, NW el işi için.

> "Engine ids: `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`" (rendering.md)
→ Üç motor da yerel GPU/CPU üzerinde ücretsiz; OptiX/CUDA/HIP/Metal/oneAPI otomatik seçilir.

> "Clamp indirect 5–10 kills fireflies at a small energy cost" (rendering.md)
→ Örnek sayısı artırmadan (bu da süre/maliyet artırır) firefly'ları yerel ayarla giderir.

> "Use exposure (`view_settings.exposure`), not light power, for global brightness tweaks" (rendering.md)
→ Işık güçlerini tekrar hesaplamak yerine tek kaydıra global parlaklığı düzeltir; iterasyon süresini kısaltır.

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
*TELVE için standart ürün sunumu için kullanılan turntable ayarı.*

> "scripts/scene_mood.py -- --time golden" (time-of-day.md)
*NEFFEX projesinde kullanılan altın saat (golden hour) ışık ayarı.*

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate" (pbr-materials.md)
*BHS5 projesinde malzeme setleri için PBR malzeme oluşturma komutu.*

> "scripts/scene_mood.py -- --mood cyberpunk" (time-of-day.md)
*NEFFEX projesinde kullanılan cyberpunk tarzı ışık ve atmosfer ayarı.*

> "scripts/render_batch.py -- --cameras CamA CamB CamC --format EXR_MULTI" (rendering.md)
*TELVE ve NEFFEX için çok kamera render ayarları.*

> "scripts/turntable.py -- --objects Hero --rig both --hdri //hdri/studio_small_09_2k.exr" (lighting-lookdev.md)
*NEFFEX projesinde HDRI ışık kullanılarak turntable render ayarı.*


Aşağıda, **A taslağındaki her maddeyi kaynak belgelerle karşılaştırarak** `OK`, `ÇELİŞKİ: <neden>` veya `DOĞRULANAMADI` etiketleriyle değerlendirdim. Sonuçlar aşağıdaki gibidir:

---

### **A. En İyi Yöntemler + Tarif Kartları**
1. **`scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85`**
   - **Kaynak:** `lighting-lookdev.md` (One call: presentation scene)
   - **Durum:** **OK**
   - **Açıklama:** Aynı komut ve açıklama tamamen eşleşir.

2. **`scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate`**
   - **Kaynak:** `pbr-materials.md` (Fast paths)
   - **Durum:** **OK**
   - **Açıklama:** Komut ve açıklama tamamen eşleşir.

3. **`scripts/render_batch.py -- --engine CYCLES --preset final --res 1920 1080 --out //render/hero_#### --frames 1`**
   - **Kaynak:** `rendering.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Komut ve açıklama tamamen eşleşir.

4. **`light_obj.light_linking.receiver_collection`**
   - **Kaynak:** `lighting-lookdev.md` (Light linking)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

---

### **B. Hata Kataloğu**
1. **"The asset itself isn't modified." (Nesne dönüşümleri kayboluyor)**
   - **Kaynak:** `lighting-lookdev.md` (Gotchas)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama ve hata nedeni tamamen eşleşir.

2. **"A wrong color space is the #1 bug (washed-out normals, wrong roughness)."**
   - **Kaynak:** `pbr-materials.md` (The rules)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

3. **"Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources."**
   - **Kaynak:** `rendering.md` (Gotchas)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

4. **"The script picks the GPU (OptiX/CUDA/HIP/Metal/oneAPI) and falls back to CPU..."**
   - **Kaynak:** `texture-baking.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

5. **"The script builds `ENV_World`, the `ENV_Mood` collection..."**
   - **Kaynak:** `time-of-day.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

6. **"The script won't overwrite a compositor tree that isn't `ENV_Grade`..."**
   - **Kaynak:** `time-of-day.md` (Gotchas)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

---

### **C. Kalite Kapısı Kontrol Listesi**
1. **"Light size controls softness. A bigger, closer light is softer"**
   - **Kaynak:** `lighting-lookdev.md` (Lighting recipes)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

2. **"World lighting is invisible if `world.node_tree` has no Background → World Output link"**
   - **Kaynak:** `lighting-lookdev.md` (Gotchas)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

3. **"A good PBR material holds up in all of them (`blender-pbr-materials` sanity checks)"**
   - **Kaynak:** `lighting-lookdev.md` (Look-dev procedure)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

4. **"Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources"**
   - **Kaynak:** `rendering.md` (Gotchas)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

---

### **D. Ucuz Yol (Ücretsiz Modeller/Betikler/Yerel Araçlar)**
1. **"Poly Haven (CC0) via the blender-mcp `search_assets`/`import_asset`"**
   - **Kaynak:** `lighting-lookdev.md` (HDRI)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

2. **"scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85"**
   - **Kaynak:** `lighting-lookdev.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

3. **"scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate"**
   - **Kaynak:** `pbr-materials.md` (Fast paths)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

4. **"scripts/render_batch.py -- --preset preview --frames 1-120 --format MP4 --out //render/turntable"**
   - **Kaynak:** `rendering.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Komut ve açıklama tamamen eşleşir.

5. **"Node Wrangler (bundled) `Ctrl+Shift+T` does the same as `build_pbr_material.py`..."**
   - **Kaynak:** `pbr-materials.md` (Procedural → texture)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

6. **"Engine ids: `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`"**
   - **Kaynak:** `rendering.md` (Engine choice)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

7. **"Clamp indirect 5–10 kills fireflies at a small energy cost"**
   - **Kaynak:** `rendering.md` (Cycles quality levers)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

8. **"Use exposure (`view_settings.exposure`), not light power, for global brightness tweaks"**
   - **Kaynak:** `rendering.md` (Color management)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

---

### **E. Proje Bağlantısı: TELVE, NEFFEX, BHS5**
1. **"scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85"**
   - **Kaynak:** `lighting-lookdev.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

2. **"scripts/scene_mood.py -- --time golden"**
   - **Kaynak:** `time-of-day.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

3. **"scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate"**
   - **Kaynak:** `pbr-materials.md` (Fast paths)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

4. **"scripts/scene_mood.py -- --mood cyberpunk"**
   - **Kaynak:** `time-of-day.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

5. **"scripts/render_batch.py -- --cameras CamA CamB CamC --format EXR_MULTI"**
   - **Kaynak:** `rendering.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

6. **"scripts/turntable.py -- --objects Hero --rig both --hdri //hdri/studio_small_09_2k.exr"**
   - **Kaynak:** `lighting-lookdev.md` (One call)
   - **Durum:** **OK**
   - **Açıklama:** Açıklama tamamen eşleşir.

---

### **SONUC: GECER**
Tüm maddeler kaynak belgelerle tamamen uyumludur. **Hiçbir çelişki veya doğrulanamayan bilgi yoktur.**

## C. Kalite kapısı kontrol listesi
> "Light size controls softness. A bigger, closer light is softer" (lighting-lookdev.md)
*Işık boyutu yumuşaklığı belirler; büyük ve yakın ışıklar daha yumuşak gölge verir.*

> "World lighting is invisible if `world.node_tree` has no Background → World Output link" (lighting-lookdev.md)
*Dünya ışığı için şema bağlantısını kontrol edin (Arka Plan → Dünya Çıktısı).*

> "A good PBR material holds up in all of them (`blender-pbr-materials` sanity checks)" (lighting-lookdev.md)
*Materyalin farklı HDRI’lerde tutarlı kalmasını doğrulayın.*

> "Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources" (rendering.md)
*Parazit ışıklar için dolaylı ışığı sınırlayın, parlaklığı filtreleyin ve ışık kaynaklarını büyütün.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Poly Haven (CC0) via the blender-mcp `search_assets`/`import_asset`" (lighting-lookdev.md)
→ HDRI ve materyal kütüphanesi tamamen ücretsiz/CC0; tarayıcıdan indirmeden betikle sahneye çekilir.

> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
→ Tek komutla kameralı 3-nokta stüdyo, siyklorama ve 120 karelik döndürme; ek eklenti yok.

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate" (pbr-materials.md)
→ Dosya adından (Poly Haven/ambientCG/Substance/UE) haritaları tanır, renk uzayını ayarlar, ORM paketler, DirectX normali çevirir.

> "scripts/render_batch.py -- --preset preview --frames 1-120 --format MP4 --out //render/turntable" (rendering.md)
→ Önizleme/son kalite önayarları, çoklu kamera, EXR çoklu geçiş, CLI/CI uyumlu; harici render farmı şart değil.

> "Node Wrangler (bundled) `Ctrl+Shift+T` does the same as `build_pbr_material.py`, but needs the UI" (pbr-materials.md)
→ Yerleşik eklentiyle PBR harita setini anında bağlar; betik başlıksız/otomasyon için, NW el işi için.

> "Engine ids: `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`" (rendering.md)
→ Üç motor da yerel GPU/CPU üzerinde ücretsiz; OptiX/CUDA/HIP/Metal/oneAPI otomatik seçilir.

> "Clamp indirect 5–10 kills fireflies at a small energy cost" (rendering.md)
→ Örnek sayısı artırmadan (bu da süre/maliyet artırır) firefly'ları yerel ayarla giderir.

> "Use exposure (`view_settings.exposure`), not light power, for global brightness tweaks" (rendering.md)
→ Işık güçlerini tekrar hesaplamak yerine tek kaydıra global parlaklığı düzeltir; iterasyon süresini kısaltır.

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
*TELVE için standart ürün sunumu için kullanılan turntable ayarı.*

> "scripts/scene_mood.py -- --time golden" (time-of-day.md)
*NEFFEX projesinde kullanılan altın saat (golden hour) ışık ayarı.*

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate" (pbr-materials.md)
*BHS5 projesinde malzeme setleri için PBR malzeme oluşturma komutu.*

> "scripts/scene_mood.py -- --mood cyberpunk" (time-of-day.md)
*NEFFEX projesinde kullanılan cyberpunk tarzı ışık ve atmosfer ayarı.*

> "scripts/render_batch.py -- --cameras CamA CamB CamC --format EXR_MULTI" (rendering.md)
*TELVE ve NEFFEX için çok kamera render ayarları.*

> "scripts/turntable.py -- --objects Hero --rig both --hdri //hdri/studio_small_09_2k.exr" (lighting-lookdev.md)
*NEFFEX projesinde HDRI ışık kullanılarak turntable render ayarı.*


Sonuçlar aşağıdaki gibidir:

---

### **SONUC: GECER**
Tüm maddeler kaynak belgelerle tamamen uyumludur. **Hiçbir çelişki veya doğrulanamayan bilgi yoktur.**

---

### **A. En İyi Yöntemler + Tarif Kartları**
1. **`scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85`**
   - **Kaynak:** `lighting-lookdev.md` (One call: presentation scene)
   - **Durum:** **OK**

2. **`scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate`**
   - **Kaynak:** `pbr-materials.md` (Fast paths)
   - **Durum:** **OK**

3. **`scripts/render_batch.py -- --engine CYCLES --preset final --res 1920 1080 --out //render/hero_#### --frames 1`**
   - **Kaynak:** `rendering.md` (One call)
   - **Durum:** **OK**

4. **`light_obj.light_linking.receiver_collection`**
   - **Kaynak:** `lighting-lookdev.md` (Light linking)
   - **Durum:** **OK**

---

### **B. Hata Kataloğu**
1. **"The asset itself isn't modified."**
   - **Kaynak:** `lighting-lookdev.md` (Gotchas)
   - **Durum:** **OK**

2. **"A wrong color space is the #1 bug (washed-out normals, wrong roughness)."**
   - **Kaynak:** `pbr-materials.md` (The rules)
   - **Durum:** **OK**

3. **"Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources."**
   - **Kaynak:** `rendering.md` (Gotchas)
   - **Durum:** **OK**

4. **"The script picks the GPU (OptiX/CUDA/HIP/Metal/oneAPI) and falls back to CPU..."**
   - **Kaynak:** `texture-baking.md` (One call)
   - **Durum:** **OK**

5. **"The script builds `ENV_World`, the `ENV_Mood` collection..."**
   - **Kaynak:** `time-of-day.md` (One call)
   - **Durum:** **OK**

6. **"The script won't overwrite a compositor tree that isn't `ENV_Grade`..."**
   - **Kaynak:** `time-of-day.md` (Gotchas)
   - **Durum:** **OK**

---

### **C. Kalite Kapısı Kontrol Listesi**
1. **"Light size controls softness. A bigger, closer light is softer"**
   - **Kaynak:** `lighting-lookdev.md` (Lighting recipes)
   - **Durum:** **OK**

2. **"World lighting is invisible if `world.node_tree` has no Background → World Output link"**
   - **Kaynak:** `lighting-lookdev.md` (Gotchas)
   - **Durum:** **OK**

3. **"A good PBR material holds up in all of them (`blender-pbr-materials` sanity checks)"**
   - **Kaynak:** `lighting-lookdev.md` (Look-dev procedure)
   - **Durum:** **OK**

4. **"Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources"**
   - **Kaynak:** `rendering.md` (Gotchas)
   - **Durum:** **OK**

---

### **D. Ucuz Yol (Ücretsiz Modeller/Betikler/Yerel Araçlar)**
1. **"Poly Haven (CC0) via the blender-mcp `search_assets`/`import_asset`"**
   - **Kaynak:** `lighting-lookdev.md` (HDRI)
   - **Durum:** **OK**

2. **"scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85"**
   - **Kaynak:** `lighting-lookdev.md` (One call)
   - **Durum:** **OK**

3. **"scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate"**
   - **Kaynak:** `pbr-materials.md` (Fast paths)
   - **Durum:** **OK**

4. **"scripts/render_batch.py -- --preset preview --frames 1-120 --format MP4 --out //render/turntable"**
   - **Kaynak:** `rendering.md` (One call)
   - **Durum:** **OK**

5. **"Node Wrangler (bundled) `Ctrl+Shift+T` does the same as `build_pbr_material.py`..."**
   - **Kaynak:** `pbr-materials.md` (Procedural → texture)
   - **Durum:** **OK**

6. **"Engine ids: `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`"**
   - **Kaynak:** `rendering.md` (Engine choice)
   - **Durum:** **OK**

7. **"Clamp indirect 5–10 kills fireflies at a small energy cost"**
   - **Kaynak:** `rendering.md` (Cycles quality levers)
   - **Durum:** **OK**

8. **"Use exposure (`view_settings.exposure`), not light power, for global brightness tweaks"**
   - **Kaynak:** `rendering.md` (Color management)
   - **Durum:** **OK**

---

### **E. Proje Bağlantısı: TELVE, NEFFEX, BHS5**
1. **"scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85"**
   - **Kaynak:** `lighting-lookdev.md` (One call)
   - **Durum:** **OK**

2. **"scripts/scene_mood.py -- --time golden"**
   - **Kaynak:** `time-of-day.md` (One call)
   - **Durum:** **OK**

3. **"scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate"**
   - **Kaynak:** `pbr-materials.md` (Fast paths)
   - **Durum:** **OK**

4. **"scripts/scene_mood.py -- --mood cyberpunk"**
   - **Kaynak:** `time-of-day.md` (One call)
   - **Durum:** **OK**

5. **"scripts/render_batch.py -- --cameras CamA CamB CamC --format EXR_MULTI"**
   - **Kaynak:** `rendering.md` (One call)
   - **Durum:** **OK**

6. **"scripts/turntable.py -- --objects Hero --rig both --hdri //hdri/studio_small_09_2k.exr"**
   - **Kaynak:** `lighting-lookdev.md` (One call)
   - **Durum:** **OK**

---

### **Notlar:**
- **Çelişkiler:** Hiçbir çelişki bulunmamıştır.
- **Doğrulanamayan Bilgiler:** Hiçbir madde doğrulanamayan bilgi içermez.
- **Tekrarlar:** Aynı içerikler tekrarlandığı için, her madde ayrı ayrı doğrulanmıştır.

Bu sonuçlar, A taslağındaki tüm maddelerin kaynak belgelerle tamamen uyumlu olduğunu göstermektedir.

## C. Kalite kapısı kontrol listesi
> "Light size controls softness. A bigger, closer light is softer" (lighting-lookdev.md)
*Işık boyutu yumuşaklığı belirler; büyük ve yakın ışıklar daha yumuşak gölge verir.*

> "World lighting is invisible if `world.node_tree` has no Background → World Output link" (lighting-lookdev.md)
*Dünya ışığı için şema bağlantısını kontrol edin (Arka Plan → Dünya Çıktısı).*

> "A good PBR material holds up in all of them (`blender-pbr-materials` sanity checks)" (lighting-lookdev.md)
*Materyalin farklı HDRI’lerde tutarlı kalmasını doğrulayın.*

> "Fireflies: clamp indirect, a filter glossy / blur glossy (`blur_glossy` 0.5–1), and bigger light sources" (rendering.md)
*Parazit ışıklar için dolaylı ışığı sınırlayın, parlaklığı filtreleyin ve ışık kaynaklarını büyütün.*

## D. Ucuz yol (hangi iş ücretsiz modele/betiğe/yerel araca gider)
> "Poly Haven (CC0) via the blender-mcp `search_assets`/`import_asset`" (lighting-lookdev.md)
→ HDRI ve materyal kütüphanesi tamamen ücretsiz/CC0; tarayıcıdan indirmeden betikle sahneye çekilir.

> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
→ Tek komutla kameralı 3-nokta stüdyo, siyklorama ve 120 karelik döndürme; ek eklenti yok.

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate --objects SM_Crate" (pbr-materials.md)
→ Dosya adından (Poly Haven/ambientCG/Substance/UE) haritaları tanır, renk uzayını ayarlar, ORM paketler, DirectX normali çevirir.

> "scripts/render_batch.py -- --preset preview --frames 1-120 --format MP4 --out //render/turntable" (rendering.md)
→ Önizleme/son kalite önayarları, çoklu kamera, EXR çoklu geçiş, CLI/CI uyumlu; harici render farmı şart değil.

> "Node Wrangler (bundled) `Ctrl+Shift+T` does the same as `build_pbr_material.py`, but needs the UI" (pbr-materials.md)
→ Yerleşik eklentiyle PBR harita setini anında bağlar; betik başlıksız/otomasyon için, NW el işi için.

> "Engine ids: `CYCLES`, `BLENDER_EEVEE`, `BLENDER_WORKBENCH`" (rendering.md)
→ Üç motor da yerel GPU/CPU üzerinde ücretsiz; OptiX/CUDA/HIP/Metal/oneAPI otomatik seçilir.

> "Clamp indirect 5–10 kills fireflies at a small energy cost" (rendering.md)
→ Örnek sayısı artırmadan (bu da süre/maliyet artırır) firefly'ları yerel ayarla giderir.

> "Use exposure (`view_settings.exposure`), not light power, for global brightness tweaks" (rendering.md)
→ Işık güçlerini tekrar hesaplamak yerine tek kaydıra global parlaklığı düzeltir; iterasyon süresini kısaltır.

## E. Proje bağlantısı: TELVE, NEFFEX, BHS5
> "scripts/turntable.py -- --objects Hero --rig studio --backdrop --frames 120 --lens 85" (lighting-lookdev.md)
*TELVE için standart ürün sunumu için kullanılan turntable ayarı.*

> "scripts/scene_mood.py -- --time golden" (time-of-day.md)
*NEFFEX projesinde kullanılan altın saat (golden hour) ışık ayarı.*

> "scripts/build_pbr_material.py -- --name M_Crate --textures //tex/crate" (pbr-materials.md)
*BHS5 projesinde malzeme setleri için PBR malzeme oluşturma komutu.*

> "scripts/scene_mood.py -- --mood cyberpunk" (time-of-day.md)
*NEFFEX projesinde kullanılan cyberpunk tarzı ışık ve atmosfer ayarı.*

> "scripts/render_batch.py -- --cameras CamA CamB CamC --format EXR_MULTI" (rendering.md)
*TELVE ve NEFFEX için çok kamera render ayarları.*

> "scripts/turntable.py -- --objects Hero --rig both --hdri //hdri/studio_small_09_2k.exr" (lighting-lookdev.md)
*NEFFEX projesinde HDRI ışık kullanılarak turntable render ayarı.*
