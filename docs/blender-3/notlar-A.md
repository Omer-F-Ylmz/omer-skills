# BLENDER-3 notlar A — ışık · gerçekçilik · malzeme · procedural

Kaynak: 5 transkript (.video-cache/<id>/segmentler.jsonl); hiçbir videoda kare yoktu (goz/kareler boş), o yüzden kare açılmadı.
Biçim: mekanizma (neden işe yarar) · ~zaman · bpy karşılığı (Blender 5.x) · sayısal öneri. "doğrula" = 5.x API adı canlıda sınanmalı.
Not: videolar 2.78–2.83 dönemi. Filmic'in 4.0+ halefi AgX; EEVEE contact shadow ayarları EEVEE Next'te (4.2+) kalktı, o kısımlar atlandı.

## 5UCc3Z_-ibs · Blender Guru · stüdyo ışığı (sandalye, sonsuz fon)
- Odak uzaklığı derinliği belirler: geniş açı derinliği abartır, uzun lens düzleştirir; eğik kamera yerine lens kaydırma kullanınca dikey çizgiler eğilmez · ~00:25, 01:26 · `cam.data.lens`, `cam.data.shift_y` (rotation_euler.x ≈ 90° kalır) · ürün için 85–105 mm; yükseklik shift_y 0.05–0.15 ile ayarlanır.
- Tüm ışık lambalardan gelsin diye world kapatılır; formu gösteren şey gölgedir, kameranın arkasındaki ışık formu düzleştirir · ~01:42 · `world.node_tree.nodes["Background"].inputs["Strength"].default_value` · world 0 (yansıma için en fazla 0.05); anahtar ışık kamera eksenine 30–60° yanda.
- Sonsuz fon: düzlemin bir kenarı yukarı extrude edilir, bevel ve smooth shading ile köşe çizgisi kaybolur · ~04:50 · `obj.modifiers.new("Bevel","BEVEL")` → `.width`, `.segments`; `mesh.shade_smooth()` (doğrula) · segments ≥16; bevel genişliği ≈ fon yüksekliğinin 0.3–0.5'i.
- Ters kare yasası: mesafe 2× olunca ışık 1/4 olur. Işık uzaklaşınca fon eşitlenir (güç artırılarak telafi edilir), yakınlaşınca düşüş sertleşir · ~05:51–06:53 · `light.energy` ile mesafe birlikte değişir · fonun eşit olması için ışık-nesne mesafesi ≥ nesne-fon mesafesinin 2–3 katı (çıkarım).
- False Color ısı haritası: gri = doğru pozlama (0 EV), camgöbeği = −1 stop, yeşil/sarı/kırmızı = aşırı pozlama. Konu üzerinde gri bölge kalmalı · ~08:29 · `scene.view_settings.view_transform = "False Color"`, kontrolden sonra `"AgX"`'e dönülür · deneme renderı düşük örnekle alınır.
- Varsayılan (Filmic) look soluk durur; daha yüksek kontrast gölgeyi koyulaştırır, parlak alanı açar. "very high" fazla gelir · ~09:31 · `scene.view_settings.look = "AgX - High Contrast"` (look adı 5.x'te doğrula) · High ya da Medium High.
- Her ışığın bir amacı olmalı ve tek başına yakılarak kontrol edilmeli. Yan dolgu ışığı fona taşmasın diye fonun arkasına yerleştirilir · ~10:32–11:33 · diğer ışıklarda `obj.hide_render = True` ile solo render · dolgu, anahtar ışığın %25–40'ı (oran: çıkarım).
- Işığın boyutu gölgenin yumuşaklığını belirler: büyük kaynak detayı saklar, küçük kaynak vurgular. Renk istenirse blackbody aralığında sıcak/soğuk kalınmalı · ~12:47–13:48 · point için `light.shadow_soft_size`, area için `light.size`; renk: `light.color` · dolgu hafif soğuk (≈0.9, 0.95, 1.0).
- AO pass, sekme kenarındaki ve temas noktasındaki gölgeyi geri kazandırır ve nesneyi zemine oturtur. World'deki AO kutusu açılmaz, yalnız pass kullanılır · ~17:53–19:55 · `world.light_settings.distance`, `view_layer.use_pass_ambient_occlusion=True`; compositor'da Mix MULTIPLY (5.x compositor API'si doğrula) · mesafe ≈ 0.2 × nesne boyu (fincan için 0.02–0.03 m), fac 0.3–0.4.
- Gürültü azaltma albedo ve normal geçişleriyle yapılır · ~15:50–16:52 · `scene.cycles.use_denoising=True`, `denoiser="OPENIMAGEDENOISE"`, `denoising_input_passes="RGB_ALBEDO_NORMAL"` · 128–256 örnek.
- Turntable: kamera bir empty'ye parent edilir, empty Z ekseninde döner, interpolasyon lineer olur · ~20:25 · `cam.parent = empty`; `preferences.edit.keyframe_new_interpolation_type="LINEAR"` (doğrula) · 100 kare / 360°.

## bum0F00TaKU · Blender Guru · ışığı iyileştirme (3 sahne üzerinden)
- Önce "bu görüntü ne anlatacak" sorusu sorulur; form göstermek ile gizem yaratmak farklı ışık ister. Her ışığın sahnede bir kaynak gerekçesi olmalı · ~02:00, 08:32 · — · ürün için hedef formu göstermektir: anahtar ışık yanda ve yukarıda durur.
- Anahtar ışık önden alınırsa hacim düzleşir; yana ve aşağı/yukarı kaydırıldığında yüzey kıvrımları gölgeyle okunur · ~03:00–04:02 · `light.location` · anahtar ışık yatayda 35–50°, dikeyde 20–40° yukarıda.
- Işık gücü False Color ile ayarlanır: yüzün/odak bölgesinin bir kısmı gri (0 EV) olmalı, sonra Filmic/AgX'e dönülür · ~03:00 · `view_settings.view_transform` "False Color" ↔ "AgX" · odakta gri, kırpılma yok.
- Arka ışık / rim nesneyi fondan ayırır. Büyük yarıçap ışığı yüzeyin etrafına sarar. Taşma olursa spot ışık kullanılır ki zemin aydınlanıp göz oraya kaymasın · ~04:35, 26:48–28:49 · `bpy.data.lights.new(type="SPOT")`, `.spot_size`, `.spot_blend` · rim gücü anahtarın 0.5–1 katı, konumu nesnenin arkasında 120–160°.
- Odak noktasına yakın konan küçük ışık hızlı düşüşle vurguyu orada toplar; uzak ışık her yeri battaniye gibi eşit kaplar · ~05:48–06:50 · ışık mesafesi · etiket/logo vurgusu için ışık yakın konur (≈ nesne boyunun 2–3 katı).
- Arka plandaki görüntü doygunluğu ve değeri kısılarak bastırılır, alan derinliği ayrımı artırır · ~09:33–10:34 · `cam.data.dof.use_dof=True`, `.aperture_fstop`, `.focus_object` · ürün için f/2.8–5.6.
- Güneş boyutu 0 iğne gibi sert gölge verir, çok büyük değer yumuşak lapa yapar; ara bir değer seçilir. Sahne dışı gölge (gobo) mekânı büyük gösterir · ~15:23, 17:25 · `sun.angle` · 1–3°.
- World'ü dolgu ışığı olarak kullanmak zemini de aydınlatır; bunun yerine hedefli küçük bir dolgu lambası konur · ~30:13 · area/spot dolgu + world düşük tutulur · world ≤ 0.05.
- Hafif hacim saçılması arka planı dolu gösterir ama daha fazla örnek ister · ~31:13 · world Volume'a `ShaderNodeVolumeScatter`, Density · 0.005–0.01; örnek sayısı 2× (ürün için genelde kapalı).

## 4H5W6C_Mbck · Blender Guru · Principled BSDF ile foto-gerçekçi malzeme
- Fresnel: her yüzey kenarda daha çok, merkezde ≈%2–5 yansıtır. Diffuse+glossy karışımında bu etki yoktur, Principled ise kendiliğinden hesaplar · ~03:57–06:59 · `ShaderNodeBsdfPrincipled` · elle fresnel kurulmaz.
- Pürüzlülük arttıkça fresnel parlaması da azalır; ikisi birbirine bağlıdır · ~07:38–09:39 · `inputs["Roughness"]` · cilalı seramik 0.05–0.15, mat seramik/kil 0.4–0.6, kauçuk 0.6–0.8.
- Malzemeler ya dielektrik ya metaldir. Metalde diffuse bileşen yoktur ve yansıma renklidir · ~10:11–14:14 · `inputs["Metallic"]` · yalnız 0 ya da 1 (kirli/oksitli yüzeyde maske ile karışım).
- Yansımayı yok etmek için specular kısılmaz, pürüzlülük artırılır. Varsayılan değer IOR 1.5'e karşılık gelir; tint sıfırda kalır · ~17:02–20:04 · `inputs["IOR"]=1.5`, `inputs["Specular IOR Level"]=0.5` (4.0+ adları) · bu değerlere dokunulmaz.
- Coat iki pürüzlülük katmanı verir: pürüzlü taban, üstünde keskin lake yansıması (araba boyası, lake ahşap, sırlı yüzey) · ~25:08–26:11 · `inputs["Coat Weight"]`, `inputs["Coat Roughness"]`, `inputs["Coat Normal"]` · coat 1.0, coat pürüzlülüğü 0.03–0.08, taban 0.25–0.4.
- Anizotropi gerektiğinde fırçalanmış metal ve tava dibi gibi dairesel yansıma için tangent yönü verilir; sheen yalnız kumaşta kullanılır · ~21:05, 23:06 · `inputs["Anisotropic"]`, `inputs["Tangent"]` (radial tangent node), `inputs["Sheen Weight"]` · varsayılan 0.
- Cam = Transmission 1 + metallic 0 + beyaz taban rengi · ~27:11–28:12 · `inputs["Transmission Weight"]=1`, `inputs["IOR"]` · cam 1.45–1.52, roughness 0–0.05.
- Veri haritaları (metalness/roughness/normal) Non-Color olmalı; normal haritası Normal Map düğümünden geçmeli. Çoğunlukla düz yüzeye normal, gerçek kabartmaya displacement verilir, ikisi birden kullanılmaz · ~31:33, 34:36 · `img.colorspace_settings.name="Non-Color"`, `ShaderNodeNormalMap`, `mat.displacement_method` · el ayarı slider yerine pürüzlülük varyasyonu daha gerçekçi durur.

## m9AT7H4GGrA · Blender Guru · gerçekçiliğin gizli malzemesi (dinamik aralık)
- sRGB/Standard dönüşümü ≈8 stop dar aralık verir: parlak alan patlar, odalar karanlık kalır ve sanatçı sahte dolgu lambası ekler. Geniş aralıklı dönüşüm (Filmic, bugün AgX) gerçek ışık değerlerine izin verir · ~02:45–05:38, 11:19 · `scene.view_settings.view_transform="AgX"` (asla "Standard" değil) · AgX varsayılan kalır.
- Çözüm sahte ışık eklemek değil, ana ışığı fiziksel güce çıkarıp sekmenin sahneyi doldurmasını sağlamaktır · ~08:00, 17:19–18:20 · `light.energy` · eklenen her dolgu ışığından önce anahtar ışığın gücü False Color'da sınanır.
- Ham log görüntü soluk görünür; look kontrastı geri getirir. Burada base contrast tercih ediliyor · ~16:02–17:19 · `view_settings.look` · Base ile High arası (5UC ile birlikte değerlendirilince Medium High).
- False Color: mavi düşük, yeşil düşük-orta, sarı orta, kırmızı yüksek, beyaz kırpılmış. Konu kırmızıya kadar çıkabilir, beyaz fon kırpılabilir · ~18:56–19:57 · view_transform "False Color" · üründe beyaz (kırpılma) olmamalı.
- Geniş aralıklı dönüşüm aşırı pozlamada renk tonunu korur ve beyaza doğru doyumu düşürür; Standard'da renk tonu kayar ve neon gibi görünür (emission'da da aynısı) · ~22:19–24:20 · AgX · parlak emission/logo yüzeyinde Standard kullanılmaz.
- Renk düzeltme compositor'da Color Balance düğümünün ASC-CDL moduyla yapılır; display-referred karışım modları (multiply/screen/overlay) sahne verisini bozabilir · ~26:31–29:27 · `CompositorNodeColorBalance.correction_method="OFFSET_POWER_SLOPE"` (5.x doğrula) · not: 5UC'deki AO multiply ile çelişiyor, bu yüzden AO fac düşük tutulur ya da adım atlanır.

## Q53LOCFVp70 · Default Cube · procedural düğümler #1
- Procedural doku matematikle üretilir: çözünürlük sınırı yoktur, disk yeri tutmaz ve parametreyle denetlenir (görüntü dokusu yakın plan çekimde kırılır) · ~03:30–04:33 · `ShaderNodeTexCoord` → `ShaderNodeVectorMath(operation="LENGTH")` → `ShaderNodeMath(operation="LESS_THAN")` · indirme yasağıyla uyumlu tek yol budur.
- Düğüm grubu iç ağı gizler ve tek bir slider dışarı verir; iki şekil çıkarılınca halka elde edilir · ~05:34 · `bpy.data.node_groups.new(type="ShaderNodeTree")`, `ng.interface.new_socket(...)`, `ShaderNodeMath(operation="SUBTRACT")` · kontrol başına bir giriş soketi.
- Tiler: koordinat ölçeklenir, FRACTION ile her hücre yinelenir, hücre başına rastgele seed verilir; sonuç desen ya da zemin dokusu olur · ~06:12–07:34 · `ShaderNodeMapping` → `VectorMath(operation="FRACTION")`; hücre rastgeleliği için `ShaderNodeTexWhiteNoise` (doğrula) · fincan dokusu ve desen için kullanılabilir.
- Pratik uzantı (çıkarım): Noise → Map Range → Roughness ile mikro pürüzlülük varyasyonu, 4H5'teki "harita slider'dan iyidir" kuralının indirmesiz karşılığıdır · 4H5 ~33:35 · `ShaderNodeTexNoise(Scale≈ 30/nesne_m)`, `ShaderNodeMapRange` · aralık taban ±0.05.

## tarif varsayılan adayları
Ürün: 8–20 cm fincan/cezve, Cycles stüdyo. Sayılardan "çıkarım" olanlar videoda sayıyla geçmez, mekanizmadan türetilmiştir.
1. Renk yönetimi: `view_transform="AgX"`, look Medium High Contrast; Standard yasak · m9AT7H4GGrA 11:19, 16:02; 5UCc3Z_-ibs 09:31.
2. World 0–0.05; dolgu world'den değil, hedefli lambadan gelir · 5UCc3Z_-ibs 01:42; bum0F00TaKU 30:13.
3. Üç ışık: anahtar area, boyutu 1.5–2× ürün boyu, uzaklığı 3–4× ürün boyu, yatayda 35–50° yanda ve 30° yukarıda; dolgu anahtarın 0.25–0.4'ü, hafif soğuk; rim 0.5–1×, arkada 120–160°. Oranlar çıkarımdır · 5UCc3Z_-ibs 02:42, 10:32, 12:47; bum0F00TaKU 26:48.
4. Sonsuz fon: L şekilli düzlem, bevel genişliği ≈ fon yüksekliğinin 0.3–0.5'i, segments ≥16, smooth; anahtar ışık fona ürünün 2–3 katı uzakta (ters kare yasasıyla fon eşitlenir) · 5UCc3Z_-ibs 04:50, 06:53.
5. Malzeme: metallic yalnız 0 ya da 1; IOR 1.5 ve Specular IOR Level 0.5'e dokunulmaz. Roughness: sırlı seramik 0.05–0.15 (ya da coat 1 + coat roughness 0.05 + taban 0.3), mat seramik 0.4–0.6, bakır/pirinç cezve metallic 1 + roughness 0.2–0.35 · 4H5W6C_Mbck 10:11, 17:02, 25:08.
6. Pürüzlülüğe procedural varyasyon (Noise → Map Range, ±0.05). Kenar pahı (çıkarım; videolarda yalnız fon pahı var): Bevel modifier genişliği ≈ ürün boyunun %0.5'i (0.5–1 mm), 3 segment, kenarda fresnel parlaması yakalanır · 4H5W6C_Mbck 33:35, 03:57; Q53LOCFVp70 03:30; 5UCc3Z_-ibs 04:50.
7. Kamera 85–105 mm, dikey çizgiler için tilt yerine shift_y; DOF f/4 civarı, odak ürün · 5UCc3Z_-ibs 00:25, 01:26; bum0F00TaKU 10:34.
8. Render: 128–256 örnek + OIDN (albedo+normal); AO pass mesafesi ≈ 0.2× ürün boyu, multiply fac ≤0.3 (ya da atlanır) · 5UCc3Z_-ibs 16:52, 17:53; m9AT7H4GGrA 29:27.

## kontrol listesi
1. False Color: üründe gri/orta bölge var, üründe beyaz (kırpılma) yok · 5UC 08:29, m9A 19:57.
2. view_transform AgX, look ayarlı, exposure ±1 içinde · m9A 11:19.
3. Gölge formu okutuyor: gövdenin bir yanı daha koyu, temas gölgesi var · 5UC 01:42.
4. Her ışık tek başına render edildiğinde amacı belli; zemin ve fon gereksiz yere aydınlanmıyor · 5UC 10:32, bum 28:49.
5. Fonda ufuk çizgisi ya da kenar görünmüyor, fon eşit aydınlanmış · 5UC 04:50.
6. Metallic 0 ya da 1; veri dokuları Non-Color; specular varsayılanda · 4H5 13:13, 31:33.
7. Kamerada dikeyler paralel (shift kullanıldı, tilt yok), lens 85 mm ve üstü · 5UC 01:26.
8. Denoise açık, düz fonda leke ya da gürültü kalmadı · 5UC 16:52, bum 21:27.
