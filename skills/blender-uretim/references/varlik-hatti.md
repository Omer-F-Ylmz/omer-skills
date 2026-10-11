# Varlık hattı — topoloji, adlandırma, doku, dışa aktarım, doğrulama

Oyun/web/AR varlığı için kurallar. Kaynak: KAYNAK.md (B = blender-kiln). Ölçüler `olculer.md`, malzeme tarifi `malzemeler.md`,
GLB/pişirme/AgX `web-aktarim.md`; burada tekrarlanmaz. Sayılar kılavuzdur, tavan değil: aşan için raporla, bloklama.
Üretim yolu: spec JSON → `tarif.py` → özet JSON. Bu dosya spec'in neyi doğru kurması gerektiğini söyler.

## Topoloji
- Deforme olan (karakter, animasyonlu) quad; statik optimize prop üçgen olabilir. N-gon her yerde kaçınılır, gerekirse üçgenle.
- Kenar halkaları kas/eklem çizgisini izler (göz, ağız, omuz, dirsek, diz). 5 kenarlı kutup 3 kenarlıdan iyi; kutbu deformasyon bölgesinden uzak tut.
- Temizlik: kapalı mesh (kasıtlı hariç), üst üste/iç yüz yok, sıfır alanlı yüz yok, çift köşe yok (merge by distance), normaller dışa.
- Yapay zekâ/tarama meshi yoğun üçgendir (100-300K): retopo ya da decimate gerekir.
- Bütçe (üçgen): web prop 0.5-3K, hero/karakter 5-15K, arka plan 100-500; mobil prop 1-5K; konsol/PC prop 5-30K; VR/AR prop 1-5K. Katman: lightweight prop 0.3-1.5K · balanced 1.5-5K · detailed 5-15K (karakter 3-8K · 8-20K · 20-80K). En üstün 2 katına kadar iyi, geometriyi görünen yere harca.
- Decimate (`DECIMATE`, COLLAPSE genel; Un-Subdivide düzenli ızgara; Planar düz yüz): önce/sonra sayı + görüntü, orijinal yedek, tek agresif geçiş yerine düşük oranlı çok geçiş. İnce parçalar (tel, halka, askı; gövdeden ~10 kat ince) decimate edilmez: eğri + yuvarlak bevel ile yeniden kur. Sonra açık/kaynaşmış kenar sayısını öncekiyle karşılaştır.
- LOD: LOD0 %100 · LOD1 %50 · LOD2 %25 · LOD3 %10-12; ad `Ad_LOD0..3`; `gltfpack -i x.glb -o y.glb -si 0.5` (`-sa` agresif). Uzaklıklar tipik 10/25/50/100 m.

## Adlandırma
- Blender'da PascalCase + önek: `SM_` statik, `SK_` iskeletli, `A_` animasyon; parça `SM_Sandalye_Bacak_01`, varyant `_01`, LOD `_LOD0`. Boşluk, özel karakter, aksan yok. Nesne adı ile mesh verisi eşleşir: `SM_X` / `SM_X_Mesh`.
- Malzeme `M_Tür_Varyant` (`M_Wood_Oak`, `M_Metal_RustedSteel`). Doku `T_Ad_Ek`: `_D`/`_BaseColor`, `_N`, `_R`, `_M`, `_AO`, `_ORM`, `_E`, `_H`. Koleksiyon `Props_X`, `Characters_X`.
- Dışa aktarılan dosya: glTF/USDZ kebab-case (`ahsap-sandalye.glb`), FBX önekli PascalCase (`SM_AhsapSandalye.fbx`).
- Not: tarifteki `GEO- MAT- LGT-` önekleri (blender-oturum) bizim sahne içi adlardır; varlık teslimi için bu dosyanın önekleri geçerli, çakışırsa teslim adı kazanır.
- glTF adı dönüşür: boşluk → `_`, nokta silinir (`Sphere.003` → `Sphere003`). Çalışma zamanı kodu ada bakıyorsa adı dışa aktarılan GLB'den doğrula, Blender'dan değil.
- Dışa aktarma sonrası klasör: `<ad>/<ad>_original.glb`, `_final.glb`, `<ad>.blend`, `<ad>_log.md` (kaynak, lisans, işlem sayıları).

## UV ve malzeme
- Dikiş gizli yerde (alt, iç, arka), doğal kontur/malzeme geçişinde; sert yüzeyde dikiş keskin kenarla çakışır; görünür düz yüzün ortasında olmaz. Otomatik: `smart_project` (bpy-teknik.md).
- Texel yoğunluğu varlık boyunca tek tip: mobil/web 5-10 px/cm (1K-2K), konsol/PC 10-20 px/cm (2K-4K). Ada boşluğu 2K'da 4-8 px, 4K'da 8-16 px; doluluk hedefi >%85. Gerçek zamanlıda tek UV 0-1; UDIM glTF'te yok.
- Tek gölgelendirici Principled BSDF (glTF PBR ile 1:1), metal/pürüz iş akışı. Metallic çoğunlukla 0 ya da 1. AO/Roughness/Metallic `_ORM` paketi R=AO, G=Roughness, B=Metallic.
- Doku çözünürlüğü (base/normal/ORM): web 512-1024 / 512-1024 / 512; mobil 1024; PC/konsol 2048-4096; hero 4096. Web varsayılanı 1024 (yakın çekim ya da konsol 2048). 2'nin kuvveti.
- Web: base JPEG/WebP (kayıplı olur), normal PNG/WebP, KTX2/Basis en iyi sıkıştırma. Dönüştür: web-aktarim.md `glb_hat.py`.
- Hızlı değerler (taban renk sRGB, metal, pürüz): meşe (0.45,0.28,0.14) 0 0.6-0.8 · çelik (0.55,0.55,0.55) 1 0.3-0.5 · altın (1.0,0.77,0.34) 1 0.2-0.4. Mutfak/seramik tarifleri malzemeler.md'de.

## Doku stratejisi (beyaz/dokusuz mesh)
- Sıra: (1) gerçekçi → bölge analizi + Poly Haven PBR; (2) stilize/low-poly → yalnız değerli Principled (görüntü dokusu yok); (3) kullanıcı elle boyar → UV + bölgeye göre malzeme yuvası hazırla.
- Bölge analizi: yüz normali + sınırlayıcı kutudaki konumla kümele (yatay+üst yarı = oturak/yüzey, dikey+alt çeyrek = ayak, dikey+üst yarı = sırt). Her kümeye `material_index` ver; bölge etiketini kullanıcıdan teyit al.
- GLB'de kalan/kaybolan (denetle): taban renk, metallic, roughness, normal, emisyon, clearcoat, sheen, IOR, kısmi transmission KALIR. SSS, Shader-to-RGB (toon), prosedürel düğümler (Noise/Voronoi/Wave/Musgrave), roughness üstünde ColorRamp, Noise→Bump KAYBOLUR. Bağımsız AO ve displacement/height haritası sessizce düşer (AO yalnız ARM paketli doldurulur; displacement'ın yuvası yok → normal haritaya fırında ya da bilerek at). SSS için görünümü taban renge fırınla.
- Denetim düğüm tipinde değil harita düzeyinde: malzemenin sahip olduğu haritalarla dışa aktarılan glTF'nin doldurduğu yuvaları karşılaştır. Dışa aktarıcı konsolunda "More than one shader node tex image" uyarısı bilgi kaybıdır.
- Fırınlama (Cycles gerekir): hedef görüntü oluştur (roughness/normal `Non-Color`), her malzemeye `ShaderNodeTexImage` ekle ve aktif yap, UV yoksa aç, `bpy.ops.object.bake(type='DIFFUSE'|'ROUGHNESS'|'NORMAL'|'EMIT')`, PNG kaydet, geçici düğümü sil, fırınlanmış görüntüleri BSDF'e bağla, prosedürel düğümü kaldır, denetimi yinele. Tarifte `uv: lightmap` + `blender_pisir.py` pişirmesi ışık içindir (web-aktarim.md), bu malzeme fırınlaması ayrı iştir.
- Poly Haven dokusu: 1k indir (web), kopya yolu `tools/varlik_indir.py`. Her malzeme için `M_Tür_Varyant`.

## Dışa aktarım
- Eksen: Blender ileri -Y, yukarı +Z; glTF +Z/Y-up (dışa aktarıcı çevirir, `export_yup=True`); FBX (Unreal) ileri +X; USDZ Y-up. Kök kemik Unreal'de X-ileri.
- GLB: önce `transform_apply`, sonra dışa aktar. Draco'yu Blender'dan açma (`export_draco_mesh_compression_enable=False`); sıkıştırma sonraki adımdır. Bizim hat meshopt + webp (`glb_hat.py`); Draco istemcide kod çözücü ister, meshopt WASM kod çözücüsüz çalışır. Kabaca: Draco konum 14 bit/normal 10 bit nicemler; KTX2 doku boyutunu %60-80 kısar.
- `export_apply`: B `False` önerir (Array/Mirror şişirir: 1 MB → 56 MB). `tarif.py` `export_apply=True` kullanır (tarif Bevel/Subdiv/Decimate üretir, Array yok; modifier'lar yazılsın diye). Spec'e Array/Mirror eklenirse bu ayarı yeniden düşün. Geometry Nodes için `False` yanlıştır: önce `modifier_apply`.
- `gltf-transform optimize` KULLANMA (içindeki `simplify` geometriyi bozar). Tekil adımlar, sıra: `resize --width 1024 --height 1024` → `webp --quality 90` → `draco` (sonuncu, geri alınamaz; Draco'yu yeniden kodlama mesh bozar) → `inspect`. Yine bizim hatta `glb_hat.py`.
- FBX: `export_scene.fbx(use_selection=True, apply_scale_options='FBX_SCALE_ALL', apply_unit_scale=True, bake_space_transform=True, mesh_smooth_type='FACE', use_armature_deform_only=True, add_leaf_bones=False, path_mode='COPY', embed_textures=True)`. Unity: ölçek 1.0, malzemeler motorda yeniden kurulur, animasyon All Actions/NLA. Unreal: çarpışma `UCX_Ad`, LOD `Ad_LOD0`, Nanite'ta yüksek poli doğrudan.
- USDZ (Apple AR): Blender doğal verir: `bpy.ops.wm.usd_export(filepath="x.usdz", selected_objects_only=True, export_materials=True, export_textures_mode='NEW', relative_paths=True, convert_world_material=False)`. `convert_world_material` True ise arşive `.exr` DomeLight girer, USDZ yalnız PNG/JPEG kabul eder (iOS Quick Look bozulabilir) → False. Doku üst sınırı 4096 (Apple 2048 önerir); özel gölgelendirici yok; geçici doku adları arşivde yeniden adlandırılır. glTF'in düşürdüğü displacement'ı USDZ taşır.
- Çoklu hedef: önce GLB (birincil), aynı sahneden FBX, USDZ.
- Headless dışa aktarım: `--python-exit-code 1` şart (yoksa hatalı dışa aktarım exit 0); çıkış kodu + dosya var mı denetle. Yolu tırnakla (boşluk).

## Temizlik ve doğrulama kontrol listesi
Sıra (B "yürütme sırası"), her adım betikle; sayılar özet JSON'a:
1. `transform_apply` (konum+dönüş+ölçek) ve ARDINDAN merge by distance. Sıra önemli: ölçek 100'de önce birleştirmek 928 yüzden 108'ini sildi. Eşiği mesh'in kendi birimiyle ver (`1e-4`). Tek-yüz-normalli low-poly dışa aktarım her kenarı böler; düz merge normali atar ve mesh yeniden pürüzsüzleşir (>5° bükülen köşe %26.7 → %94.5). Merge'ten önce köşe normalini kaydet, sonra geri yaz; rig'lenecekse kaynak mesh birleşik (kaynaşık) olmalı, bölünmüş kopyalar eklemde açılır.
2. Normali tutarlı yap (`normals_make_consistent(inside=False)`; görsel kontrol: Face Orientation mavi = doğru).
3. Gevşek geometriyi sil (`select_loose` → delete), dejenere erit (`dissolve_degenerate`, 1e-4).
4. Kapalılık: kaynaşmış kenar (>2 yüz) 0 olmalı; açık kenarı yalnız raporla.
5. Köken tabanın ortası: sınırlayıcı kutunun min z'sini 0'a indir, `origin_set`, `transform_apply(location=True)`.
6. Ölçek: 1 birim = 1 m. Beklenen yükseklik: karakter ~1.75, sandalye ~0.85, masa ~0.75, kapı ~2.10; <0.01 m ya da >100 m uyarı.
7. Adlandırma, yetim temizliği (`orphans_purge`), malzeme: boş yuva yok, eksik doku (`node.type == 'TEX_IMAGE' and node.image is None`) yok.
8. Üçgen sayısı katman aralığında; aşıyorsa rapora yaz.
- Dışa aktarım sonrası: Khronos doğrulayıcı (`gltf-transform validate x.glb` exit 0; format denetler, mesh değil, kaynaşmış yüz geçer); dosya boyutu ham <30 MB, optimize web <5 MB; `inspect` ile mesh/doku/animasyon sayısı, beklenmeyen kopya yok; 3-5 malzemede roughness/metalness/renk Blender'la uyumlu; animasyon adları glTF eşlemesine göre. Bizde karşılığı `tools/blender_dogrula.py` + `glb_hat.py`.

## Kaynak bulma
- Önce var olanı ara, sonra üret. Poly Haven: tümü CC0, anahtarsız (HDRI, doku, model); Sketchfab: indirilebilir + ücretsiz, API jetonu ister.
- Lisans kuralı: CC0 serbest; CC-BY / CC-BY-SA kaynağı ve lisansı log'a yaz (uyar); CC-BY-NC ticari işte kullanma.
- Poly Haven canlı API'si: benzersiz User-Agent zorunlu (ToS 2.4), görünür atıf (2.5) → log'a `Source: Poly Haven (polyhaven.com), via public API`. `files/<id>` → format → çözünürlük; web için `1k` (aynı sandalye: 2K sıkıştırmasız 16.2 MB, 2K WebP 1.03 MB, 1K 0.48 MB). Araç: `tools/varlik_indir.py`.
- İçe aktarılan varlık kaynağın adıyla gelir: boyutu doğrula (Poly Haven aramada mm verir, içe aktarma m: 0.568 doğru, 568 dönüşüm olmadı demek) ve adı kuralına göre yeniden adlandır.
- 2-3 yinelemede uygun varlık çıkmazsa üretime geç. Karakter için T-poz isteği rig öncesi belirlenir.

## Animasyon ve karakter özü
- Karakter rig planlıysa T-poz: kolların omuzdan ele açısı ±15° içinde T, -15..-45° A, <-45° I-poz (dönüştür; ölçüm yatay dilimle değil omuz→el ile). T-poz'da kulaç ≈ boy.
- Rig seçimi köşe/kemik oranıyla: <700 köşe → elle 12-20 kemik; 700-3000 → `armature_basic_human_metarig_add` (35 deform); >3000 → `armature_human_metarig_add` (160); dört ayak >900 → basic quadruped (46). Rigify insan ~3200 köşe ister; 370 köşede 160 kemiğin 107'si hiçbir köşeyi etkilemedi, baş koptu. Bağlamadan sonra ölü kemik say (`vertex_groups` ağırlığı >0.01 olmayan); varsa bir kademe küçült.
- Animasyona hazır iskelet: eklemi uzvun büküldüğü yere koy, hareket verisi adlarıyla adlandır (`Hips→Spine→Spine1→Neck→Head`, `LeftUpLeg→LeftLeg→LeftFoot→LeftToeBase`, `LeftArm→LeftForeArm→LeftHand`, `Tail1..`). Tek kemikli bacak diz bükemez.
- Rigify üretilen uzuvlar IK'dadır; FK kontrolleri çevrilmeden sessizce hareket etmez. Blender 5.x kemik koleksiyonları kemik katmanlarının yerini aldı.
- Hareket yolu konuya göre: kendi klibi varsa koru; Mixamo kitaplığı (~2500 klip, Adobe hesabı, yeniden hedefle) standart humanoid için; eklemli nesne (lamba, kapak, kapı) rijit parçaları anahtarla: parça tek kemiğe %100 ağırlık, menteşe açma işaretini ölç, öngörü/aşma/sekme vuruşları. UniMate (metin→hareket) ağırlıkları CC BY-NC 4.0 (ticari değil), 3.2 GB; kullanılmaz (aşağıda).
- Betikli animasyon kuralları (bpy-teknik.md "Animasyon" ile birlikte): kemiği kendi dinlenme çerçevesinde sür; IK kutup açısını dinlenme pozundan çöz; bacak uzunluğunun ≤%95'inde bükülü tut; döngüyü tam kapat; hareketi sayıyla ve hareket halinde değerlendir.

## Referans sadakati (fidelity)
- Fikir: foto varsa gözle değil ölç, dikkati ölçümün çözemediğine harca. Bu bizde `tools/kontur_profil.py` + `blender_gorunum.py --referans` (silüet IoU ≥ 0.90-0.95).
- Adımlar: (1) ayrıntı envanteri (bacak sayısı, kulp biçimi, oran), brief ile foto çelişirse brief kazanır; gerçek boyut sorulur ya da varsayım olarak yazılır, kamera yüksekliği görünen kenardan okunur. (2) siluet pikselden ölçülür. (3) her parçanın bağlı olduğu kontrol edilir: birleşen parça diğerine girer, kesit değişmez. (4) malzeme anıdan değil görüntüden örneklenir, fiziksel malzeme başına bir malzeme, yama patina metal kalır. (5) iki tur karşılaştırma.
- Genel: ince parçanın (tel, tüp, kulp) kalınlığını da pikselden ölç, gövdeyi değil; en büyük siluet farkı buradan gelir. Yuvarlak parça yakında yuvarlak kalsın: tüp çevresi ≥16, dönel gövde ≥32 kenar, pürüzsüz; eğri cam ≥64 segment ve tek kabuk. İnce ayrıntı çizik/çukur/kenar çentiği ile, kabartma genliği artırarak değil (dökme metal gibi görünür). Ölçek ayrıntıya göre: arka plan prop → envanter+bağlılık; varsayılan → hepsi, iki tur; hero → ek görünümler.

## Tarife sığmayan iş
Tarif = tek headless koşu + özet JSON. Aşağıdakiler kaynaklarda var, bizde yok; gerekirse belirtilen yolla.
- Her fazdan önce `get_scene_info`, her fazdan sonra `get_viewport_screenshot` (B kural 1-2, 22): canlı MCP turu ve ekran görüntüsü döngüsü. Tarif özet JSON ve sayısal kapı verir; görüntü gerekirse `blender_gorunum.py` tek sayfa. Canlı inceleme blender-oturum canlı oturumu.
- Faz sonu çerçeve odaklama (`view3d.view_selected`) ve iki zıt açıdan görüntü: GUI viewport'a ihtiyaç duyar; tarifte yok, `blender_gorunum.py` kamerası kullanılır.
- `get_*_status` / MCP eklenti sürüm denetimi, `uvx blender-mcp install-addon`, port 9876 (B kural 23): MCP kurulumu, blender-oturum'un işi, tarifi ilgilendirmez.
- Batch modu (YAML manifest, sihirbaz, otonom çok varlık; B batch-mode): uzun gözetimsiz koşu ve çok MCP turu; tarifte tek varlık/koşu. Gerekirse varlık başına ayrı spec + dış döngü, onaylı ayrı iş.
- Yapay zekâ üretimi (Hunyuan3D, TRELLIS, Rodin, Tripo, HF Space, `gradio_client`): ücretli/yerel GPU/ağ çağrısı, lisans (Hunyuan AB dışı; ağırlıklar kısıtlı); tarif üretimi dışında. Ayrı onaylı iş, sayısal tavanlı ("en çok N çağrı").
- Konsept resim üretimi (FLUX.1-schnell HF Space, nano-banana/Gemini, Pollinations): ücretli/ağ çağrısı. `gorsel-uret` skill'i, onaylı ayrı iş. Üretilen görselde filigran/atıf kaldırılmaz.
- Fidelity_check render↔foto yineleme döngüsü (`template_profile.py`, iki düzeltme turu): çok render + yargı turu. Bizde tek `kontur_profil.py` + `blender_gorunum.py --referans` turu (1 iyileştirme); fazlası yalnız kullanıcı isterse.
- Etkileşimli onay kapıları (decimate/silme/her adımda "Keep? yes/no/adjust", guided mod): tarif tek koşu, sormaz. Yıkıcı işlem gerekiyorsa (silme, decimate) koşudan önce kullanıcıdan onay al, .blend'i yedekle.
- Sürekli ham kopya/yedek ve `_original/_clean/_textured/_optimized` ara GLB serisi (full depolama): tarifte tek `glb` çıktısı; ara dosya gerekirse spec'i birden çok `glb` yoluyla ayrı koş.
- UniMate / MoCapAnything / `tools/quadruped.py` hareket üretimi: GB'lık kurulum, ticari olmayan ağırlıklar, GPU, hareketi izleme turu; tarifin `anim` anahtarı yalnız konum/dönüş/ölçek anahtarı verir. Karakter animasyonu ayrı onaylı iş.
- Rig kurma/ağırlık boyama/Rigify (`parent_set ARMATURE_AUTO`, ölü kemik doğrulaması): Edit-mod override'lı, gözle doğrulama ister; tarif spec'inde rig anahtarı yok. blender-oturum canlı oturumunda ya da ayrı betikle.
- Geometri sihirbazlığı: Geometry Nodes ağacı kurma, Simulation Zone, Grease Pencil çizimi: sürüme duyarlı düğüm adları ve canlı sorgu ister; tarif ilkelleri (kup/silindir/kure/koni/duzlem/torus) dışında. blender-oturum canlı oturumu.
