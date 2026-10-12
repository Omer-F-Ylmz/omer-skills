# bpy teknik notlar — headless betik, geometri, malzeme, ışık, render, animasyon

Önce tarif: `tools/blender/lib/tarif.py` spec JSON'u çoğu işi karşılar, model bpy yazmaz. Bu dosya spec'e sığmayan işte
(`blender_cli.py` ile `exec`/betik) ya da `tarif.py`'yi genişletirken okunur. Kaynak: KAYNAK.md (A = rapcan).
Soket adı/ışık profili/malzeme tarifi zaten `malzemeler.md` ve `isik-profilleri.md`'de; burada tekrarlanmaz.

## Betik iskeleti ve tuzaklar
- Çalıştırma: `blender -b --factory-startup --python-exit-code 1 -P x.py -- args`; argüman `sys.argv[sys.argv.index("--")+1:]`. `--factory-startup` kullanıcı ayarı/eklenti etkisini keser; `--python-exit-code 1` olmadan betik hatası exit 0 verir (B).
- Önce sürüm: `bpy.app.version_string`; sürüme duyarlı çağrıyı `try/except` ya da `bpy.app.version` ile dallandır.
- Temiz sahne: varsayılan küp/kamera/ışığı sil, yetim veriyi at (`bpy.data.<koleksiyon>` döngüsü; `bpy.ops.outliner.orphans_purge(do_recursive=True)`). `tarif.py` bunu `--blend` yoksa yapar.
- Varsayılan: operatör yerine veri API'si + `bmesh`. `bpy.ops.*` bağlama (aktif nesne, mod) bağlı; headless'ta `context is incorrect` verir. Gerekirse `with bpy.context.temp_override(active_object=o, object=o, selected_objects=[o]): ...`.
- Nesne kurma: `me = bpy.data.meshes.new(ad)` → `bpy.data.objects.new(ad, me)` → `bpy.context.collection.objects.link(o)`. Koleksiyona bağlanmayan nesne render'da yok.
- Canlı keşif (tahmin yok): `[s.name for s in bsdf.inputs]`, `dir(bpy.ops.mesh)`, `bpy.data` koleksiyonları.
- Bayat referans: `StructRNA ... has been removed` = operatör/`to_mesh` sonrası tutulan referans; `bpy.data`'dan adla yeniden al.
- `scene.frame_current = n` değerlendirmeyi güncellemez → `scene.frame_set(n)`.
- Değerlendirilmiş (modifier'lı) geometri: `ob.evaluated_get(bpy.context.evaluated_depsgraph_get()).to_mesh()`, iş bitince `to_mesh_clear()`. Ham mesh modifier'ı yok sayar.
- Ölçek: ışık watt'ı ve fiziksel malzeme metre ölçeğini varsayar; 0.01 birimlik model siyah çıkar. 1 birim = 1 m (olculer.md).
- Kaydet: `bpy.ops.wm.save_as_mainfile(filepath=...)`; taşınabilirlik için önce `bpy.ops.file.pack_all()`.
- Sürüm kırıkları (A): Principled "Specular" → "Specular IOR Level", Emission → `Emission Color`+`Emission Strength` (4.0); `mesh.use_auto_smooth` kalktı → "Smooth by Angle" (`bpy.ops.object.shade_auto_smooth(angle=0.5236)`, 4.1+, `AttributeError`'da `use_smooth=True`); Eevee kimliği 4.2'de `BLENDER_EEVEE_NEXT`, 5.x'te yine `BLENDER_EEVEE` olabilir → ikisini dene; Grease Pencil v3 (4.3+) API'si farklı; varsayılan görünüm AgX (4.0+). `use_nodes` 6.0'da kalkacak, `node_tree` varlığını denetle (B).
- Belirsizlikte hata metniyle API belgesi sorgula (blender-uretim "API disiplini"); ikinci denemeyi tahminle yapma.

## Geometri
- `bmesh.ops`: `create_cube/uvsphere/icosphere/cone/grid`, `extrude_face_region`, `inset_region`, `bevel`, `subdivide_edges`, `spin` (döner profil → donel-model.md), `bridge_loops`, `solidify`. Elle kurulan meshe `from_pydata` sonrası `mesh.update(); mesh.validate()`.
- Birleştirme üç ayrı iştir (yanlış seçim "kırık görünür"ün 1 numaralı nedeni):
  - join: tek nesne, yüzeyler kaynaşmaz; değiyorsa ayrıca `remove_doubles`. Operatörle override gerekir (`selected_editable_objects` da verilir).
  - boolean: kaynaşık sağlam katı. Modifier kullan (`type="BOOLEAN"`, `operation`, `object`, `solver="EXACT"`), sonra `modifier_apply`, kesiciyi sil. Girdiler kapalı + normaller tutarlı olmalı; FLOAT çözücüde eş düzlemli yüzeyden kaçın.
  - parent: ayrı nesne, birlikte hareket (`child.parent = p; child.matrix_parent_inverse = p.matrix_world.inverted()`). Eklemli parça/parça başına malzeme için.
- Çift köşe: join, mirror, array sonrası `bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-4)` (metre ölçeği; ölçeğe göre ayarla). Dönüşümü uygulamadan birleştirme (B: ölçek 100'de birleştirme yüzey siler) → önce `transform_apply`, sonra birleştir, sonra normal.
- Normal: `bmesh.ops.recalc_face_normals`; kapalı ters mesh için `reverse_faces`. Düz/pürüzsüz yüzey başına `poly.use_smooth`, normal yönünden bağımsız. Sert yüzey: pürüzsüz + bevel ya da keskin kenar; organik: hepsi pürüzsüz.
- Kapalılık: kenar başına yüz sayısı. `len(e.link_faces) > 2` her zaman kusur (kaynaşmış iç yüz; glTF doğrulayıcı yakalamaz); `== 1` açık kenar, yalnız su geçirmez olması gereken işte (baskı, fizik) kusur. Çare: `remove_doubles`, `holes_fill`, gevşek geometriyi sil.
- Modifier sırası: Mirror → Array → Solidify → Bevel → Subdivision → Boolean → Triangulate (dışa aktarım). `levels` (viewport) ve `render_levels` ayrı.
- Çoğaltma: bağlantılı kopya aynı mesh verisini paylaşır (`bpy.data.objects.new(ad, base.data)`); binlercesi için koleksiyon örnekleme ya da Geometry Nodes (düğüm adları sürümle değişir, canlı doğrula). Rastgelelikte `random.seed`.
- Geometry Nodes çıktısı yalnız modifier sonucudur; dışa aktarmadan önce `modifier_apply` (aksi halde taban mesh yazılır, B ölçtü: 2 688 üçgen → 2). Sonda Realize Instances. Simulation Zone: Group Input değerleri bölgeye geçmez, state item kullan.

## Malzeme
- Kurulum: `mat.use_nodes = True`, `bsdf = nodes["Principled BSDF"]`, `bsdf.inputs[ad].default_value`, `obj.data.materials.append(mat)`. Renk girişi doğrusaldır; hex/sRGB için `c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4`.
- Giriş adları (4.x/5.x): Base Color, Metallic, Roughness, IOR, `Specular IOR Level`, `Transmission Weight`, `Subsurface Weight`/`Radius`/`Scale`, `Coat Weight`, `Sheen Weight`, `Emission Color`/`Emission Strength`, Alpha, Normal. Sürümde yoksa listele, tahmin etme.
- Doku renk uzayı: base color/emission = sRGB; roughness, metallic, normal, AO, displacement, maske = `img.colorspace_settings.name = "Non-Color"`. Yanlış uzay hatasız ama yanlış görünür.
- Normal haritası araya `ShaderNodeNormalMap` ister; kabartma için `ShaderNodeBump` (Height ← Noise `Factor`; 5.2'de `Fac` → `Factor`). Yüzey başına malzeme: `poly.material_index`.
- Prosedürel: Noise/Voronoi/Wave/Gradient + MapRange/ColorRamp. GLB'de kaybolur → varlik-hatti.md "Doku" (bake).
- UV: ilkel/`from_pydata` meshte yoktur. `bpy.ops.uv.smart_project(angle_limit=1.15, island_margin=0.02)` (radyan; B 66° yazar) Edit modda tüm yüz seçiliyken, override ile; kutu için `cube_project`. Döşeme için Mapping + Texture Coordinate.
- Harici görüntü eksik yol = pembe; `img.pack()` ya da `file.pack_all()`. Emisyon `Strength > 1` ışık verir (Cycles/Eevee).
- Saydam çizim düzlemi: Alpha ← doku `Alpha`; `mat.blend_method` sürüme göre değişti (4.2+ `surface_render_method`), canlı doğrula.

## Işık ve dünya
- Veri API'si: `bpy.data.lights.new(ad, type)` (POINT/SUN/SPOT/AREA), `energy`, `color`; hedefe `TRACK_TO` (`track_axis="TRACK_NEGATIVE_Z"`, `up_axis="UP_Y"`).
- Birim: POINT/SPOT/AREA = watt (küçük sahnede yüzler-binler; 10 W alan ışığı görünmez); SUN = W/m² ölçekten bağımsız, öğle ≈ 3-5, 1000 çerçeveyi yakar. AREA `size`/`size_y` büyüdükçe gölge yumuşar; SPOT `spot_size` (radyan) + `spot_blend`. 3 nokta profili ve yerleşim: isik-profilleri.md.
- HDRI: world `ShaderNodeTexEnvironment` → Background `Color`, `Strength`. Yoksa düz renk dünya yine ortam ışığı verir; ışıksız + dünyası siyah = siyah render. HDRI'yi kameradan gizleyip aydınlatmayı tutmak: `film_transparent = True`. Tarifte `hdri` anahtarı.
- Görünüm: `scene.view_settings.view_transform` = `AgX` (foto-gerçekçi) ya da `Standard` (düz grafik, tam renk); önce ışık gücünü, sonra `exposure`'u ayarla. Web için AgX eşleme: web-aktarim.md.

## Render
- Motor: Cycles gerçekçi/cam/yansıma, Eevee hız/önizleme (cam ve GI yaklaşık). Cycles GPU: `scene.cycles.device="GPU"` + `preferences.addons["cycles"].preferences` (`compute_device_type`, `get_devices()`, `d.use=True`); GPU kilidi blender-oturum'da.
- Örnek: Cycles 32-64 önizleme, 128-512 son; `use_denoising`, `use_adaptive_sampling`. Eevee `scene.eevee.taa_render_samples`. Çözünürlük `resolution_x/_y/_percentage`.
- Kamera: `bpy.data.cameras.new`, `lens` (35 geniş, 50 doğal, 85 portre), `scene.camera = cam` (atlanırsa render boş), DOF `dof.use_dof/focus_object/aperture_fstop`, ortho `type="ORTHO"` + `ortho_scale`.
- Çıktı: `image_settings.file_format` PNG/OPEN_EXR/JPEG, `color_depth`, `filepath`, `bpy.ops.render.render(write_still=True)`. Şeffaf arka plan `film_transparent` + `color_mode="RGBA"`. Parlama/renk derecelemesi için `scene.use_nodes` ile compositor (Glare).
- Dışa aktarım ve hedefler: varlik-hatti.md "Dışa aktarım"; `export_scene.gltf(filepath, export_format="GLB")`, `wm.usd_export`, STL için `wm.stl_export` (eski: `export_mesh.stl`), OBJ `wm.obj_export`.
- Siyah = ışık yok/çok düşük ya da dünya siyah; boş = nesne bağlı değil/kamera ters/nesne arkada; pembe = doku yolu; soluk = görünüm dönüşümü ya da fazla güç.

## Animasyon
- Önce aralık: `frame_start/_end`, `render.fps` (varsayılan 1-250 sessizce kırpar/doldurur). `obj.keyframe_insert(data_path="location", frame=n[, index=i])`; yol: `location`, `rotation_euler`, `scale`, `'["özellik"]'`, shape key `value`. Tarifte `anim`/`kare` bunu yapar.
- Aradeğerleme: kare noktalarında `interpolation` (BEZIER varsayılan, LINEAR mekanik, CONSTANT tutma, BACK/ELASTIC/BOUNCE taşma) ve `easing`. Döngü: `fc.modifiers.new("CYCLES")`. 5.x/4.4+ katmanlı action'da `action.fcurves` yoktur; kanal kümesi `action.layers[].strips[].channelbag(slot)` altındadır, canlı sorgula (A eski yolu, B yenisini yazar).
- Tam döngü: P karelik döngü 0..P-1 anahtarlanır; P'yi de yazmak dikişte takılır (B).
- Sürücü (driver): `obj.driver_add("rotation_euler", 0)`, `drv.type="SCRIPTED"`, `variables.new()` (`TRANSFORMS`, `targets[0].id/transform_type/transform_space`), `expression` (tekerlek: `-x / yarıçap`).
- Kısıt: `TRACK_TO`/`DAMPED_TRACK` (yüzünü dön), `FOLLOW_PATH` (`use_curve_follow`, eğri `use_path`, `path_duration`, `eval_time` anahtarla), `COPY_*`, `CHILD_OF` (animasyonlu etki), `LIMIT_*`.
- Armatür: `bpy.data.armatures.new` + `edit_bones` (Edit mod override'lı), bağlama `parent_set(type="ARMATURE_AUTO")`, kemik `pose.bones[ad].keyframe_insert("rotation_euler", frame=n)`; uzuv için IK kısıtı. Karakter/rig seçimi: varlik-hatti.md "Animasyon ve karakter".
- Shape key: `shape_key_add("Basis")`, ikinci anahtarın `data[i].co`'su, `value` 0→1 anahtarla.
- Animasyon render: PNG dizisi (yarıda kalırsa devam), `filepath="…/kare_"`, `render(animation=True)`; doğrudan video `FFMPEG` + `ffmpeg.format/codec`. Örnek sayısını düşük tut. Dönüş ekseni işaretini kullanmadan ölç (+0.2 rad çevirip probu izle); bağlı kemik sürüşünü kemiğin kendi eksen çerçevesinde yaz.

## 2B nesneler
- Eğri: `bpy.data.curves.new(ad, "CURVE")`, `dimensions="2D"` (kapalı spline dolu düz şekil, logo) ya da `"3D"`; `splines.new("BEZIER"|"NURBS"|"POLY")`, `bezier_points.add(n-1)`, `handle_*_type="AUTO"`, kapalı için `use_cyclic_u`. Kulp eğrisi kodu: donel-model.md.
- Derinlik mesh'e çevirmeden: `bevel_depth` (yuvarlak tüp), `bevel_resolution`, `extrude` (düz kalınlık), `fill_mode="BOTH"`, özel profil `bevel_object`. Mesh gerekirse `object.convert(target="MESH")` (override).
- Yazı: `bpy.data.curves.new(ad, "FONT")`, `body`, `align_x/_y="CENTER"`, `extrude`, `bevel_depth`, `font = bpy.data.fonts.load(ttf)`. Yazı eğridir; boolean/harf harf için mesh'e çevir.
- SVG: `bpy.ops.import_curve.svg` (eklenti; kapalıysa aç ya da yolu eğriye çevir); gelen eğri SVG birimiyle küçüktür, ölçekle sonra `extrude/bevel`.
- Düz resim/sprite: `create_grid` düzlemi + `ShaderNodeTexImage` (Color → Base Color, Alpha → Alpha); düz görünüm için emisyon + `Standard`.
- Grease Pencil v3 (4.3+) API'si sürümle farklı: koleksiyon adını `dir(bpy.data)`'dan bul; yalnız düz vektör gerekiyorsa dolu 2B eğri daha basit ve sürüm-kararlı.
