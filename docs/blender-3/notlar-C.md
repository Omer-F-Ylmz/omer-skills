# BLENDER-3 notlar C — kamera · kompozisyon · ürün render · turntable

Kaynak: 4 transkript (.video-cache/<id>/segmentler.jsonl); klasörlerde kare yoktu, kare açılmadı.
Biçim: mekanizma (neden işe yarar) · ~zaman · bpy karşılığı (Blender 5.x) · sayısal öneri. "doğrula" = 5.x API adı canlıda sınanmalı.
Not: videolar 2.91–4.x dönemi. EEVEE bloom/AO paneli EEVEE Next'te (4.2+) kalktı; bloom yerine compositor Glare düğümü kullanılır.

## W07u4S8xJXs · CG Boost · sinematik render için 10 ipucu
- Kamera yüksekliği duyguyu taşır: yukarıdan bakış genel bakış/üstünlük verir, yere yakın alttan bakış konuyu ağır ve heybetli gösterir · ~05:57 · `cam.location.z` < konu merkezi, `rotation_euler.x` < 90° · kahraman kadrajı için kamera konu merkezinin biraz altında, 0 ile −10° arası yukarı bakış.
- Kompozisyon adaylarını ucuz motorla hızlı karşılaştırmak: her açı ayrı render yuvasına alınır · ~06:59 · `scene.render.engine = "BLENDER_WORKBENCH"`, `resolution_percentage = 25`, her aday ayrı dosyaya · aday başına ≤3 s render; 3–5 aday.
- Geniş en-boy oranı "sinematik" algı yaratır; anamorfik sıkıştırma dijitalde gereksiz · ~07:36–09:39 · `render.resolution_x = 2560`, `resolution_y = 1080` · sinematik kahraman için ≈21:9; ürün kataloğu için 1:1 ya da 4:5 (çıkarım).
- Üçler kuralı / altın oran / altın üçgen kılavuzları: önemli öğe kesişimlere yakın konur, dogmatik değil · ~09:40–10:40 · `cam.data.show_composition_thirds`, `show_composition_golden`, `show_composition_golden_tria_a` (yalnız görünüm; headless'ta `bpy_extras.object_utils.world_to_camera_view` ile nesne merkezinin 1/3 ya da 1/2 çizgisine uzaklığı ölçülür) · tek ürün için merkez ya da 1/3 dikey çizgi.
- Odak uzaklığı psikolojisi: 40–50 mm göz gibi nötr; 60–210 mm perspektifi sıkıştırır, detayı öne çıkarır, tek noktaya odaklar; ~30 mm hafif bükülme ile tedirginlik · ~11:37–13:39 · `cam.data.lens`, `cam.data.lens_unit = "MILLIMETERS"` · ürün için uzun lens bandı.
- Hollanda açısı (eksen etrafında küçük yatma) gerilim katar; abartılmamalı · ~13:39–14:41 · kameranın görüş ekseni (yerel Z) etrafında dönüş: `cam.rotation_euler` üzerinde roll (doğrula: yerel eksen için `rotation_mode` / matris çarpımı) · 2–4°; ürün kataloğunda 0°.
- Ayna testi: kompozisyon yatay çevrilince denge hatası göze çarpar · ~15:00 · kamera `scale.x = -1` ya da compositor Flip düğümü (5.x'te `scene.compositing_node_group`, doğrula) · yalnız denetim renderında.
- Işık rolleri: anahtar (önden açıyla), arka/rim (siluet ayırır), dolgu (karanlığı açar); rim için koni açısı daraltılmış spot ve sahne dışı motive edilmiş kaynak · ~17:27, ~22:49 · `light.type = "SPOT"`, `light.spot_size`, `light.spot_blend` · rim spot koni 15–30°, blend 0.5+ (çıkarım).
- Son işlem: hafif hacim sisi, bloom/glare, DOF yalnız yakın çekimde; vinyet (elips maske + bulanıklık %40 + çarpma), film greni (overlay), eğri: mavi gölgeleri kaldır, yeşil parlakları indir, kontrast ekle · ~25:08–29:04 · Principled Volume `Density`; compositor `CompositorNodeEllipseMask`, `CompositorNodeBlur` (relative), Mix multiply, `CompositorNodeCurveRGB` (5.x düğüm adları doğrula) · sis yoğunluğu ≤0.02; vinyet faktörü 0.2–0.4.

## xxKZ1EjyjjU · Vishnu Menon · Blender kamera ustalık sınıfı: odak uzaklığı
- Sınıflar: ≤35 mm geniş, 50 mm normal, ≥75 mm tele; ≤24 mm'de belirgin bozulma · ~01:14, ~04:03 · `cam.data.lens` · ürün kahramanı için tele bandı.
- Sıkıştırma: aynı kadrajı korumak için kamera geri çekilip lens uzatılınca nesnenin ön-arka farkı küçülür; 18 mm'de şişe uzun ve perspektifli, 55 mm'de basık ve "doğru" oranlı · ~04:15–06:16 · lens artarken mesafe orantılı artar: `d2 = d1 * lens2 / lens1` · ürün oranını bozmamak için 85–105 mm (portre fotoğrafçılığı gerekçesi) · ~06:16.
- Aynı odak noktasında uzun lens daha sığ alan derinliği (daha çok arka plan bulanıklığı) verir · ~07:07–08:07 · `cam.data.dof.use_dof = True`, `aperture_fstop` · tele + düşük f-stop = güçlü ayrışma; ürün tamamen keskin kalacaksa f-stop yükseltilir.
- Sensör: varsayılan 36 mm tam kare; gerçek kamera presetleri sensörü değiştirir, efektif odak = lens × crop faktörü · ~08:35–10:37, ~14:51 · `cam.data.sensor_width = 36`, `cam.data.sensor_fit = "AUTO"` · tarif 36 mm'de sabit kalsın ki mm değerleri fotoğrafçı sezgisiyle örtüşsün.
- Zoom burst: konu merkezde tutulur (kenarlar en çok bozulur), lens 10 karede 24→105 mm, doğrusal interpolasyon, hareket bulanıklığı açık · ~16:35–18:38 · `cam.data.keyframe_insert("lens")`, `render.use_motion_blur = True`, `render.motion_blur_shutter = 1.0` · tanıtım vurgusu için; turntable'da kullanılmaz.
- Dolly zoom: kamera bir empty'ye bağlanır, empty yaklaşırken lens düşürülür, konu boyutu sabit kalır · ~19:02–20:03 · `cam.parent = empty`; her karede `lens = lens0 * d / d0` · 120 kare.

## xOUQUDoflxU · Ryan King Art · ürün görselleştirme bölüm 1 (mikrofon modelleme)
- Gerçek ölçek: model gerçek boyutta kurulur, ölçek uygulanır; DOF ve ışık düşümü sahne birimine bağlı olduğu için şart · ~02:58 · `bpy.ops.object.transform_apply(scale=True)` (ya da veri düzeyinde `mesh.transform`) · ürün 8–20 cm ⇒ 0.08–0.20 birim.
- Küçük nesnede kırpılma: görünüm/kamera yakın düzlemi küçültülür · ~03:59 · `cam.data.clip_start = 0.01` (görünüm için `space.clip_start`) · 0.001–0.01 m.
- 80 mm odak "biraz yakınlaştırıp düzleştirir", ürüne daha iyi oturur · ~03:59 · `cam.data.lens = 80` · 80–100 mm.
- Sert kenarlarda ince bevel + ağırlıklı normal: ışık kenarda parlama çizgisi yakalar, düz yüzeyde gölgelendirme bozulmaz · ~06:02–07:02, ~11:26 · `mod = obj.modifiers.new("Bevel","BEVEL"); mod.segments = 4; mod.width` küçük; `obj.modifiers.new("WN","WEIGHTED_NORMAL")` · bevel genişliği ürün boyutunun ~%0.3–0.5'i, segments 3–4.
- Yansıma için stüdyo HDRI (Poly Haven fotoğraf stüdyosu, 1K yeterli) ve metal parçalara parmak izi/yüzey kusuru dokusu · ~02:01 · World `ShaderNodeTexEnvironment`; kusur haritası → Principled `Roughness` · HDRI 1K–2K; kusur haritası roughness'ta ±0.1 oynatır (çıkarım).
- Yıkıcı adımdan önce yedek koleksiyona kopya; isimlendirme ve koleksiyon düzeni · ~13:38, ~16:42 · `bpy.data.collections.new("backup")`, `hide_render = True` · tarif betiğinde gereksiz (betik zaten yeniden üretir).

## glz3-ZClzGc · J Derinor · 360 turntable ürün animasyonu
- Döner tabla + sabit zemin: yalnız dönecek parçalar bir empty'ye bağlanır (dönüşümü koruyarak), zemin/kumaş sabit kalır · ~15:14 · `child.parent = empty; child.matrix_parent_inverse = empty.matrix_world.inverted()` · kamera sabit, ürün döner.
- Döngü: Z dönüşü 0°→360° anahtarı, 30 fps × 10 s = 300 kare, iki anahtar doğrusal interpolasyon ⇒ sabit hız · ~15:14–16:15 · `empty.keyframe_insert("rotation_euler", index=2)`; doğrusal için ya `context.preferences.edit.keyframe_new_interpolation_type = "LINEAR"` ekleme öncesi ya da sürücü `drv = empty.driver_add("rotation_euler", 2); drv.driver.expression = "(frame-1)/N*2*pi"` (5.x katmanlı action API'si yerine; doğrula) · videoda 360° son karede ⇒ ilk ve son kare aynı, döngüde takılma; düzeltme: 360° anahtarını N+1. kareye koy, 1..N render et.
- Kamera: 50 mm varsayılan yerine 100 mm; DOF odak nesnesi ürün, f-stop ~1–1.5 · ~14:13 · `cam.data.lens = 100`, `dof.focus_object = urun`, `dof.aperture_fstop` · gerçek ölçekte küçük üründe f/1–1.5 ürünün arkasını da bulandırır; ürün keskin kalsın diye f/2.8–4.
- Kamera hafif aşağı bakar, zemin detayı kadraja girer; farklı açılar denenir · ~16:15 · `rotation_euler.x` · 10–25° yukarıdan bakış (çıkarım).
- Işık: üç alan ışığı (üst + iki yan), Cycles + gürültü giderme, AgX "very high contrast"; emisyon panelleri ambiyans için düşük tutulur, ışıklar tek tek kapatılıp etkisi okunur · ~05:13–06:14, ~17:17 · `light.type = "AREA"`; `scene.cycles.use_denoising = True`; `view_settings.look` (5.x'te ad doğrula) · emisyon dolgusu lamba katkısının altında kalsın.
- Zemin: zemin düzlemi alt bölünüp kumaş simülasyonuyla örtü, ürün çarpışma nesnesi · ~11:09 · `CLOTH` + `COLLISION` modifier, `quality = 12` · sim betikte pahalı; tarif varsayılanı düz/kavisli fon olsun (sonsuz fon videoda yok).
- Malzemede gürültü dokusu → color ramp → bump + roughness: düz siyah plastikte mikro varyasyon ışığı kırar · ~06:14–07:15 · `ShaderNodeTexNoise` → `ShaderNodeValToRGB` → `ShaderNodeBump` · bump strength 0.05–0.15 (çıkarım).

## tarif varsayılan adayları
1. Ölçek: ürün gerçek boyutta (0.08–0.20 m), ölçek uygulanmış; `cam.data.clip_start = 0.005` · kanıt xOUQUDoflxU ~02:58, ~03:59.
2. Odak: `lens = 90` (aralık 85–105), `sensor_width = 36`; kamera mesafesi kadrajdan hesaplanır: `d = (h_urun / doluluk) * lens / sensor_h` (sensor_h = 36 / en-boy oranı, sensor_fit AUTO'da yatay kadrajda) · kanıt xxKZ1EjyjjU ~06:16, glz3-ZClzGc ~14:13.
3. Kadraj doluluğu: ürünün yansıtılmış sınır kutusu kadraj yüksekliğinin %60–70'i; merkez ya da 1/3 dikey çizgi; `world_to_camera_view` ile ölç · kanıt W07u4S8xJXs ~09:40 (sayı çıkarım).
4. Yükseklik: stüdyo kadrajında kamera ürün merkezine 10–20° yukarıdan bakar; kahraman kadrajında merkezin altından 0 ile −10° · kanıt W07u4S8xJXs ~05:57, glz3-ZClzGc ~16:15 (derece çıkarım).
5. Roll 0°; Hollanda açısı yalnız istenirse 2–4° · kanıt W07u4S8xJXs ~14:41.
6. DOF: `use_dof = True`, `focus_object = urun`, `aperture_fstop = 4` (ürün tümüyle keskin) ; arka plan ayrışması istenirse 2.8; f/1–1.5 yalnız tek detay kadrajında · kanıt glz3-ZClzGc ~14:13, xxKZ1EjyjjU ~07:07.
7. Fon: kavisli sonsuz fon (düzlem + bevel, köşe yarıçapı ≈ ürün yüksekliği, segments ≥16) ya da `render.film_transparent = True`; dönen parçalar dışında zemin sabit · kanıt glz3-ZClzGc ~15:14 (fon eğrisi notlar-A 5UCc3Z_-ibs ~04:50).
8. Turntable: ürün (kamera değil) empty'ye bağlı döner; 30 fps, N = 120 (4 s web) ya da 300 (10 s); 0°@1 → 360°@N+1 doğrusal (ya da sürücü), render 1..N ⇒ dikişsiz döngü; hareket bulanıklığı kapalı · kanıt glz3-ZClzGc ~15:14–16:15, xxKZ1EjyjjU ~17:35 (linear).

## kontrol listesi
- Ölçek uygulanmış mı (`obj.scale == (1,1,1)`), ürün boyutu 0.08–0.20 m aralığında mı?
- `lens` 85–105, `sensor_width` 36, roll 0° mi?
- Ürün sınır kutusu kadrajda %60–70 yükseklik, hiçbir köşesi kadraj dışında değil mi (`world_to_camera_view` 0–1 içinde)?
- DOF odak nesnesi ürün mü; ürünün ön ve arka kenarı keskin mi (f-stop ≥2.8)?
- Turntable: kare 1 ile N+1 aynı açı, N renderlanmıyor; interpolasyon LINEAR (fcurve ya da sürücü) mi?
- Dönen hiyerarşide zemin/fon yok mu; kamera sabit mi?
- Işıklar tek tek kapatılıp her birinin amacı doğrulandı mı; emisyon/HDRI ana ışıkları bastırmıyor mu?
- Look/view transform AgX ve look adı 5.x enum'unda geçerli mi (`view_settings.bl_rna.properties["look"]` ile doğrula)?
