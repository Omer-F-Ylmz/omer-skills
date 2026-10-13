# BLENDER-3 notlar — grup D (render ayarı · rig · web GLB)

Kaynak: 6 transkript (segmentler.jsonl) + Blender 5.2 LTS manual (EEVEE Raytracing, Cycles Sampling, Cycles Light Paths, glTF 2.0 add-on) + yerel bpy incelemesi (Blender 5.2.1, `-b --factory-startup`).
Biçim: `mekanizma (neden) · ~zaman · bpy · sayısal varsayılan`. "5.2 vars." = yerelde okunan fabrika değeri.

## Sürüm farkı (EEVEE Next, 4.2+)
- 4.2'de EEVEE yeniden yazıldı (EEVEE Next): eski `use_ssr`, `use_gtao`, `use_soft_shadows`, `shadow_cube_size` yok; yerine `use_raytracing`, `ray_tracing_options.*`, `shadow_ray_count/step_count`, `fast_gi_*`. Motor kimliği 4.2–4.x'te `BLENDER_EEVEE_NEXT`, 5.2'de yine `BLENDER_EEVEE` (enum'da yalnız bu var).
- 5.2 vars.: `taa_render_samples=64`, `taa_samples=16`, `use_raytracing=False`, `ray_tracing_method='SCREEN'`, `ray_tracing_options.resolution_scale='2'` (1:2), `trace_max_roughness=0.5`, `screen_trace_quality=0.25`, `screen_trace_thickness=0.1`, denoise spatial/temporal/bilateral açık, `use_shadows=True`, `shadow_ray_count=1`, `shadow_step_count=6`, `use_fast_gi=True` (GLOBAL_ILLUMINATION), `fast_gi_resolution='2'`, `fast_gi_ray_count=2`, `fast_gi_step_count=8`, `clamp_surface_indirect=10`.
- Cycles 5.2 vars.: `samples=4096`, adaptive açık `adaptive_threshold=0.01`, `adaptive_min_samples=0`, `denoiser='OPENIMAGEDENOISE'`, passes `RGB_ALBEDO_NORMAL`, prefilter `ACCURATE`, `denoising_quality='HIGH'`, bounces max/diff/glossy/trans/transp/vol = 12/4/4/12/8/0, `sample_clamp_direct=0`, `sample_clamp_indirect=10`, `light_sampling_threshold=0.01`, `use_light_tree=True`, caustics refl/refr açık, `blur_glossy=1.0`, `filter_width=1.5`, `device='CPU'`.

## kYOsR9Kb8Ek · CGMatter · Cycles'ı hızlandırma (Blender 4.1)
- GPU + OptiX: binlerce çekirdek örnekleri paralel işler; videoda örnek hızı ~10–20 kat · 0:28 · `prefs.addons['cycles'].preferences.compute_device_type='OPTIX'`, `scene.cycles.device='GPU'` · vars. CPU.
- Düşük örnek + denoise: 1→10→100 örnekte denoise sonrası fark azalıyor · 0:55 · `cycles.samples`, `use_denoising=True` · vars. 4096/açık.
- Persistent data: sahne verisi kareler arasında yeniden kurulmaz (animasyon/turntable) · 1:20 · `render.use_persistent_data=True` · vars. False.
- Simplify: alt bölme tavanı + doku tavanı bellek/zaman keser · 1:35 · `render.use_simplify=True`, `simplify_subdivision_render=1..3`, `cycles.texture_limit_render='2048'` · vars. 6 / OFF.
- Kamera/mesafe culling: kadraj dışı nesneler işlenmez · 1:50 · `cycles.use_camera_cull`, `use_distance_cull` + nesne başına bayrak (doğrula) · vars. False.
- Fast GI + animated seed: birkaç sekmeden sonra AO'ya geçer; gürültü deseni kare başına değişir · 2:00 · `cycles.use_fast_gi=True`, `use_animated_seed=True` · vars. False. Scrambling distance: manual'a göre Blue-Noise desenle çalışmaz (5.x varsayılan desen Automatic=Blue-Noise türevi → doğrula).
- Toplam sekme: 0'da cam siyah, 4'te saydam; 12→5 uzlaşma · 2:25 · `cycles.max_bounces=5` · vars. 12.
- Çıktı: PNG sıkıştırması yavaş; 0 ya da EXR half DWAA · 2:36 · `image_settings.compression=0` / `file_format='OPEN_EXR'`, `color_depth='16'`, `exr_codec='DWAA'` · vars. 15. Ayrıca decimate %45, partikül segmenti düşürme, %50 çözünürlük + harici büyütme, kare adımı 2 + optik akış ara kare (Claude için yalnız turntable taslakta anlamlı).

## dLZEmfqob7k · rileyb3d · iç mekân Cycles optimizasyonu
- Gürültü = az ışık ya da az örnek; çok ışık eklemek kontrastı öldürür, tek ana ışık · 1:37 · — · —.
- Portal: pencereye oturan dikdörtgen area light örnekleri açıklığa yönlendirir · 2:30 · `light.cycles.is_portal=True` (doğrula) · vars. False.
- Cam/perde gölge hilesi: Light Path "Is Shadow Ray" → Mix(cam, Transparent); gölge ışınında saydam, yansımada cam · 3:32 · node kurulumu (ShaderNodeLightPath, ShaderNodeMixShader) · —.
- Seçici denoise: Cryptomatte maskesiyle duvara güçlü, mobilyaya hafif denoise (Noisy Image ile karıştır) · 5:35 · `view_layer.use_pass_cryptomatte_material=True` + compositor · —.
- Noise threshold 0.01→0.02 hızlandırır · 8:30 · `cycles.adaptive_threshold=0.02` · vars. 0.01.
- Saydam katman çoksa transparent sekme 24 (zamana etkisi az) · 8:55 · `cycles.transparent_max_bounces=24` · vars. 8.
- Ateşböceği: direct clamp'e dokunma; indirect 10→5 ya da 3 · 9:12 · `sample_clamp_indirect=3..5` · vars. 10. Pixel filter 1.5→1.0 daha keskin · `cycles.filter_width=1.0`.
- Sonuç: 1920×1080, RTX 2080, <1 dk; yazar en fazla ~5 dk render.

## RsCNKHSRk_s · CG Boost · EEVEE kalite ayarları (4.2+ arayüz)
- Ray tracing tek tıkla yansıma/kırılma/dolaylı ışık getirir (kapalıyken ışık probu yolu) · 0:35 · `eevee.use_raytracing=True` · vars. False.
- Örnek sayısı genel gürültüyü belirler; 16/32/64/128 → ~1.6/3/6/12 s (1080p×%150): örnek ×2 = süre ×2 · 1:18, 7:16 · `taa_render_samples` · vars. 64.
- Gölge: rays (ışık başına ışın, maks 4) + steps (ışın başına örnek, maks 16); 1/2→4/16 süre ~10→25 s · 1:50, 8:56 · `shadow_ray_count`, `shadow_step_count` · vars. 1/6.
- RT çözünürlüğü 1:2→1:1 cam/metal yansımasını netleştirir; 1:16 bozuk · 2:16 · `ray_tracing_options.resolution_scale='1'` · vars. '2'.
- Screen trace thickness artınca yansıma/kırılma artefaktı azalır; bu sahnede 1 m, süreye etkisi yok · 2:40 · `ray_tracing_options.screen_trace_thickness=1.0` · vars. 0.1 (manual: yüksek değer yansımayı uzatıp titretebilir).
- Fast GI: çözünürlük 1:1 + rays (maks 16) / steps (maks 64); 2/8→4/16→8/32→16/64 = 30 s→45 s→1:27→3:13 · 3:00, 9:50 · `fast_gi_resolution='1'`, `fast_gi_ray_count`, `fast_gi_step_count` · vars. '2', 2/8. Yazar: durağanda maks, animasyonda aşırı.

## DDeB4tDVCGY · Joey Carlino · hızlı rig
- Armatür + kemik yerleşimi; head = pivot; yüzey yakalama ile gövdeye oturtma · 0:20 · `bpy.ops.object.armature_add`, `edit_bones.new` · —.
- Simetri: sol kemiklere `.L` son eki, sonra symmetrize; pose aynalama buna dayanır · 1:23 · `bpy.ops.armature.symmetrize()` · —.
- Otomatik ağırlık: Armature modifier + kemik adlı vertex group'lar · 1:56 · `bpy.ops.object.parent_set(type='ARMATURE_AUTO')` · —. "Bone heat weighting failed" = üst üste binen parçalar → remesh/ayır; az geometri = kötü bükülme → loop cut.
- Weight paint: auto normalize (bir kemiğe eklenen ağırlık diğerlerinden düşer), smooth · 4:17 · `tool_settings.use_auto_normalize=True`, `bpy.ops.object.vertex_group_smooth` · —.
- Rijit parça: kemiğe doğrudan ebeveyn ya da boş gruplar + ağırlık 1; hile: bireysel orijinle ölçek 0.1 → auto weights → ölçek 10 · 5:34, 6:35 · `parent_set(type='BONE')` / `'ARMATURE_NAME'`; `vertex_group_quantize(steps=1)` · —.
- IK: deform kapalı ayrı IK kemiği, ebeveyn temizle, IK constraint chain 2–3, pole hedef + pole angle · 8:12 · `pose_bone.constraints.new('IK')`, `chain_count=2`, `pole_target`, `bone.use_deform=False` · —.

## oQUPYvX97cU · ZJ Design Lab · web için glTF
- Görünmeyen geometriyi sil (alt yüzey), basit düzlemle kapat; yük önce boyuttan gelir · 1:30 · decimate / silme · —.
- Animasyonları NLA'ya stash/push down ve adlandır → glTF'te ayrı klip, kodda tek tek oynatılır · 2:30 · `export_animation_mode='NLA_TRACKS'` ya da `'ACTIONS'` · vars. ACTIONS.
- Modifier uygula, resim sıkıştırma "automatic" · 3:20 · `export_apply=True`, `export_image_format='AUTO'` · vars. False/AUTO.
- Yazar "glTF embedded" seçiyor; manual'a göre embedded en verimsiz (Base64) → web için GLB tercih · `export_format='GLB'`.
- Doğrulama: glTF viewer'da sürükle-bırak; pmndrs gltfjsx ile React bileşeni, gölgeleri kapalı üretip elle aç · 4:00 · harici araç · —.

## gsqrHDmgTfA · Conor Woodard · KTX2 doku sıkıştırma
- Orijinal: disk 1.6 MB, VRAM 11.2 MB, 1 draw call (gltf.report) · 0:50 · — · —.
- Çift sıkıştırmayı önle: dışa aktarımda resim formatı Automatic, ayrı (glTF Separate) çıktı → harici araç (ZenCompress) · 1:30 · `export_format='GLTF_SEPARATE'` · —.
- UASTC: az sıkıştırma/yüksek kalite (metin, gradyan); VRAM 11.2→7 MB (−%38), disk biraz arttı · 3:30 · harici (gltf-transform `uastc` — doğrula) · —.
- ETC1S: güçlü sıkıştırma, düz renkler; VRAM ~−%50, disk orijinalle aynı, keskin kenarda hayalet piksel · 4:30 · harici (`etc1s` — doğrula) · —.
- Normal map sıkıştırılmaz (bozulur); diffuse/roughness/metallic sıkıştırılabilir · 3:28 · — · —.

## Manual notları (5.2 LTS)
- EEVEE: Light Probe izleme ve Fast GI'da AO yöntemi en ucuz; maliyet precision, çözünürlük, rays/steps ile artar. `trace_max_roughness=1` her yüzeyi izler, Fast GI'ı kapatır.
- Cycles: noise threshold önerilen aralık 0.1–0.001; min light bounces yükseltmek süreyi sert artırır; light tree dokulu/karmaşık ışık shader'ında gürültü artırabilir; OIDN genelde en kaliteli, "None" passes detayı yayar (en az Albedo).
- Light paths: clamp ateşböceğini keser ama gerçek parlak vurguyu da kısar; caustics kapatmak gürültüyü azaltır; Filter Glossy için 1.0 başlangıç.
- glTF: modifier sonrası mesh; quad/ngon üçgenlenir; dikiş/flat shading köşe sayısını artırır; yalnız Principled BSDF + bağlı Image Texture (+Mapping → KHR_texture_transform) çıkar, prosedürel → bake; area/world ışığı düşer; animasyon yalnız transform/pose/shape key; 4 ya da 8 dışı influence izleyicide bozulabilir. 5.2 vars.: Draco kapalı, level 6, quant pos/norm/uv 14/10/12; meshopt kapalı; `export_def_bones=False`, `export_all_influences=False`, lights/cameras False, `export_yup=True`.

## Yerel ölçüm (Blender 5.2.1, 384×384, basit sahne: zemin + metal küre + cam küre + area light; sıcak, 3 render medyanı)
- EEVEE: taban (RT kapalı, s64) 0.19 s · RT açık 0.24 · +RT 1:1 0.26 · +FGI 1:1 0.25 · +gölge 2/8 0.27 · +FGI 4/16 0.28 · FGI 16/64 0.47 · s128 (4/16 ile) 0.43 · s32 0.17.
- Soğuk ilk render/ayar değişimi sonrası shader derleme: 0.4–14 s (gölge ayarı değişiminde 14 s gözlendi) → 384 px'te asıl maliyet derleme, ayar değil.
- Cycles CPU s128: varsayılan sekmeler 6.5 s → 6/2/2/4/4 5.1 s (−%21); threshold 0.02 bu sahnede anlamlı fark vermedi (6.2 s).

## tarif varsayılan adayları
1. EEVEE 384–512 px önizleme: `use_raytracing=True`, `ray_tracing_options.resolution_scale='1'`, `fast_gi_resolution='1'`, `fast_gi_ray_count=4`, `fast_gi_step_count=16`, `shadow_ray_count=2`, `shadow_step_count=8`, `taa_render_samples=64`. Kanıt: CG Boost kalite karşılaştırması + yerel 0.19→0.28 s (+%47, mutlak +0.09 s).
2. `ray_tracing_options.screen_trace_thickness=0.5` (sahne ölçeği ~1–3 m; CG Boost 1 m'de süre etkisiz). İnce nesnede kaçırma görülürse yükselt, uzayan yansımada düşür.
3. Kahraman EEVEE: `fast_gi_ray_count=16`, `fast_gi_step_count=64`, `shadow_ray_count=4`, `shadow_step_count=16`, `taa_render_samples=128`; önizlemede değil (yerel ×1.7, videoda 30 s→3:13).
4. Tek süreçte toplu render: bütün açıları aynı `blender -b` çağrısında çiz, ayarları ilk renderdan önce sabitle (derleme 0.4–14 s her ayar değişiminde tekrar ödenir).
5. Cycles kahraman: `device='GPU'` (varsa, OptiX), `samples=256` (512 tavan), `use_adaptive_sampling=True`, `adaptive_threshold=0.01` (taslakta 0.02), `use_denoising=True`, OIDN + `RGB_ALBEDO_NORMAL` + `ACCURATE`.
6. Cycles ışık yolu (ürün/stüdyo): `max_bounces=6`, `diffuse_bounces=2`, `glossy_bounces=3`, `transmission_bounces=6` (≥4, yoksa cam kararır), `transparent_max_bounces=8` (yığılı alfa → 24), `sample_clamp_indirect=5`, `caustics_reflective=caustics_refractive=False`. Kanıt: yerel −%21, rileyb3d, CGMatter, manual.
7. Turntable/animasyon: `render.use_persistent_data=True`, `cycles.use_animated_seed=True`; çıktı PNG `compression=0` ya da EXR half DWAA.
8. Web GLB: `export_format='GLB'`, `export_apply=True`, `export_image_format='AUTO'` (boyut kritikse `'WEBP'` + `export_image_webp_fallback=True`), `export_draco_mesh_compression_enable=True` (level 6, 14/10/12; istemcide Draco çözücü gerekir — doğrula), riglide `export_def_bones=True`, klip başına NLA/stash + `export_animation_mode='ACTIONS'`; KTX2 dışarıda (UASTC metin/gradyan, ETC1S düz renk, normal map hariç).

## kontrol listesi
- [ ] `scene.render.engine` 5.x'te `'BLENDER_EEVEE'` / `'CYCLES'` (4.2–4.x betiklerde `BLENDER_EEVEE_NEXT` kalmasın); eski `use_ssr/use_gtao` çağrısı yok.
- [ ] EEVEE'de `use_raytracing=True` ve RT/FGI çözünürlüğü `'1'`; cam/metal yüzeyde yansıma görünür.
- [ ] Cycles'ta `samples` 4096 varsayılanında bırakılmadı; adaptive + denoise açık.
- [ ] Camlı sahnede `transmission_bounces ≥ 4`, saydam katman çoksa `transparent_max_bounces` artırıldı.
- [ ] Ayarlar ilk renderdan önce sabit; açılar tek süreçte.
- [ ] GLB: modifier uygulandı, prosedürel malzeme bake edildi, yalnız Principled + Image Texture.
- [ ] GLB: Draco açıksa istemci çözücüsü hazır; rig'de yalnız deform kemikleri, influence 4.
- [ ] gltf.report / glTF viewer ile disk, VRAM, draw call ve animasyon klipleri doğrulandı.
