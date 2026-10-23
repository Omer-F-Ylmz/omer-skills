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
