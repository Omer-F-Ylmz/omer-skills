# 7 — Blender hattı: daha güzel + daha hızlı (KAYNAK-TARAMA-BLENDER, 2026-10-01)

20 kaynak · okuma 3 sonnet subagent (README + SKILL/references + tek betik) · örneklem teyidi: 6 lisans/yıldız + cc-blender ürün oranı + TMHS lisansı tuttu. Kod kopyalanmadı; kurulum yok.
Ölçüt sütunu: bakım (★ · son push) · CC'de çift mi · izin kapsamı · context maliyeti.

| # | Kaynak | Mekanizma | Bizdeki karşılığı | Karar | Faz | Lisans | Ölçütler |
|---|---|---|---|---|---|---|---|
| 1 | RobLe3/cc-blender-skill | 30 zincir skill (ahujasid MCP üstünde): malzemeye göre ışık tablosu; multiview-fit-loop (ön/yan/arka/üst düz silüet render → IoU/bbox/centroid → ayarla → tekrar); contour-to-mesh (OpenCV kontur → Delaunay → sığ derinlik) | blender-oturum akışı var, tarif/döngü yok | UYARLA (ışık tablosu + silüet IoU döngüsü, tarif olarak) | 2 | MIT | ★80 · 2026-05-01 · çift (ayrı MCP'ye bağlı) · bpy+Bash+OpenCV · 30 SKILL, ağır |
| 2 | ra100/blender-claude-plugin | 8 yalnız-md skill, resmi Lab MCP için "MCP-First" bölümü; düğüm katalogları (~373 GN, ~95 shader) | search_api_docs / get_python_api_docs aynı bilgiyi canlı verir | ÖĞREN ("önce doküman aracı" kuralı) | 2 | MIT | ★17 · 2026-04-29 · çift · yalnız md · 8 SKILL+16 ref, büyük |
| 3 | ThanhNguyxnOrg/blendops | 48 plan/denetim skill'i, "kanıtsız render/GLB iddiası yok" kapısı | CLAUDE.md "kanıtsız bitti yok" kuralı | RED (Draft v0, eval koşmamış, iskelet) | — | MIT | ★3 · 2026-09-21 · çift · md · 48 skill, ağır |
| 4 | TMHSDigital/Blender-Developer-Tools | 60 headless örnek: `blender -b --python`, assert + başarısızlıkta sıfır-dışı çıkış; export ön ayarı (önce transform_apply, glTF +Y); bake-high-to-low | headless betik sözleşmesi yok | ÖĞREN (yalnız fikir) | 1 | CC-BY-NC-ND-4.0 (kod/türev yasak) | ★14 · 2026-10-01 · kısmen çift · yerel blender · 16 skill+9 kural |
| 5 | emalorenzo/three-agent-skills (three-best-practices + r3f) | 100+ kural/17 kategori performans-bellek: GLTF Draco/KTX2/meshopt, dispose, InstancedMesh/merge/LOD, koşullu render, pixelRatio | 24 threejs-* görsel/efekt odaklı; teslim/bellek boşluk | UYARLA (eksik kategoriler) | 2 | README MIT, LICENSE dosyası yok → teyit şart | ★54 · 2026-01-28 · az çift (gölge/kamera/post) · md · SKILL ~1720 kelime + büyük ek |
| 6 | ahujasid/mcp-for-blender | Poly Haven: ara → önizle → indir (1k-2k; HDRI yeni world, doku → Principled, lisans nesne özelliğine); güvenli mod env (dosya/süreç/ağ engeli); canlı API sorgusu bpy_api_lookup/describe_node_type (yalnız ikincil kaynak) | Lab MCP execute/screenshot var; Poly Haven yok | UYARLA (Poly Haven + canlı soket sorgusu mekanizması; sunucu kurulmaz) | 1 | MIT | ★29810 · 2026-09-30 · çift (ikinci Blender MCP) · keyfi bpy+ağ, telemetri varsayılan açık · 36 araç |
| 7 | Blender Lab MCP (resmi) | 26 araç; `*_for_cli` ikizleri .blend'i arka planda açar; paketli API/manual RST; weak_sandbox "gerçek sandbox değil" (kapsam doğrulanamadı); örnek istemler: manifold, malzemesiz nesne, mutlak yol, ters normal, uniform olmayan ölçek | ZATEN VAR — fark: yalnız canlı oturum araçlarını kullanıyoruz; `_for_cli` headless denetim ve örnek kontrol listesi kullanılmıyor | ZATEN VAR | 2 | GPL-3.0 | v1.0.3 · tek MCP · korumasız bpy · ertelenmiş araçlar |
| 8 | strayspark "Verification beats vision" | Ekran görüntüsü yalnız görünüşü kanıtlar; deterministik assert (11 koşul), measure (bbox/hacim + is_closed), verify_export (glTF geri oku, 0 mesh = FAIL), tolerans 0.001; headless | threejs-visual-validation web tarafında; Blender sayısal kapısı yok | UYARLA (mekanizma; ürün kapalı) | 1 | kapalı ürün, kod yok | blog 2026-09-14, satıcı yazısı |
| 9 | strayspark sunucu karşılaştırması | Resmi 26 araç/korumasız · mcp-for-blender 36/isteğe bağlı güvenli mod · Pro 120+ ücretli · StraySpark 556 (~9.5k şema token) | Lab MCP seçimimiz | ÖĞREN (seçimi teyit; araç sayısı = context) | — | blog | 2026-09-25, satıcı yazısı |
| 10 | verianim (PyPI) | Planlayıcı/kodlayıcı/iyileştirici + görsel/video doğrulayıcı; önce statik sahne, sonra animasyon; doğrulama render'ı Workbench, saydam/yansıtıcı gizli | yok | RED (lisans); Workbench fikri Q1'e | — | Demonstration (ticari değil, AGPL koşullu) | 2026-06-10 · — · bpy+soket 8888+LLM anahtarı · CLI |
| 11 | ellmos-ai/ellmos-blender-use-mcp | Her çağrı `blender --background --python` + zaman aşımı 120 s + JSON; verify_visual 4 görünüm (ön/yan/üst/perspektif) + sayısal: uygulanmamış döndürme, havada parça, pivot dışarıda, başıboş empty | `execute_blender_code_for_cli` aynı headless fikir | ÖĞREN (4 görünüm + kontrol listesi) | 1 | MIT | ★2 · 2026-09-30, olgunlaşmamış · çift · bpy, ağ yok |
| 12 | threedle/ll3m | Planlayıcı → retrieval (BlenderRAG, hata mesajıyla yeniden sorgu) → kodlayıcı; eleştirmen 5 görünüm (kamera bbox'tan) VLM sorun+çözüm; doğrulayıcı her çözümün uygulandığını teyit; kod düzenlenir, sıfırdan yazılmaz; tur tavanı/puan yok | search_api_docs var; döngü protokolü yok | ÖĞREN | 2 | Demonstration (ticari değil); sunucu kapalı | ★554 · 2026-03-07 · — · hesap+keyfi bpy |
| 13 | techinz/blender-batch-lightmap-baker | Panel betiği: nesne başına ayrı lightmap (atlas yok), UV yoksa otomatik, Combined/Diffuse/Glossy, 512-2048; iddia FPS 3-4× masaüstü, 5× mobil, GLB −%15 | yok | ÖĞREN | 1 | MIT | ★27 · 2025-05-11 (durgun) · — · bpy · ~7 KB |
| 14 | Ibrahim-3d/Blender-Quick-Lightmap-Baker | İkinci UV "Light Map" + Smart Unwrap tek atlas + Cycles bake → kopya koleksiyon, tek emission malzemesi; önce Apply Scale; three.js'te flipY=false | yok | UYARLA (atlas akışı headless yeniden yazım; GPL kod alınmaz) | 1 | GPL-3.0 | ★0 · 2026-09-30 · — · add-on · ~3 KB |
| 15 | pmndrs/postprocessing | ToneMappingEffect(AGX) zincir sonunda; renderer.toneMapping = NoToneMapping + HalfFloat buffer; LUT3D; CDL efekti repoda bulunamadı | ZATEN VAR — threejs-exposure-color-grading kendi ölçer+LUT'unu yazar; fark: küçük ürün sahnesinde hazır efekt yeter, ölçer gerekmez | ZATEN VAR | 3 | Zlib | ★2871 · 2026-10-01 · çift · npm |
| 16 | n8python/n8ao | Hazır SSAO geçişi; aoRadius sahne ölçeğinin 1-2 mertebe altı, distanceFalloff 1, intensity 2-5, halfRes 2-4× kazanç (~1 ms sabit), MSAA yok → SMAA | ZATEN VAR — threejs-screen-space-ambient-occlusion (GTAO) elle; fark: n8ao WebGL/pmndrs zincirine tek geçiş | ZATEN VAR | 3 | CC0-1.0 | ★497 · 2026-08-10 · çift · npm |
| 17 | mrdoob/three.js #27362 | Blender exposure 0 ≠ three.js exposure 1; fark ışık birimi/hat, eşleme formülü yok; ek LUT uzaklaştırır; pişmiş PNG [0,1] kırpar | exposure-color-grading genel kural | ÖĞREN (eşleme deneysel kalibrasyon) | 3 | MIT | issue · — · — |
| 18 | builder.io webgl-scroll-animation | GLTF + scroll 0..1 → rotation.y = π/2·p, lerp min(dt·6,1); kamera z 3.2 fov 35; ambient 0.4 + Environment "city"; storyboard görseli ajana | ZATEN VAR — web-sahne-desenleri; fark: sayısal başlangıç değerleri + storyboard girdisi | ZATEN VAR | 3 | blog | 2025-10-02 |
| 19 | NodeToPython (BrendanParmer) | Shader/GN/compositor ağacını (alt gruplar, varsayılanlar, yerleşim) okunur bpy betiğine ya da add-on zip'e çevirir; UI düğmesi, headless dışa aktarım doğrulanmadı | yok | UYARLA (malzeme tarif kütüphanesi) | 1 kurulum · 2 tarif | GPL-3.0 | ★363 · 2026-08-23 · v4.2.0, Blender 4.2–5.2 · dosya yazar · MCP aracı yok |
| 20 | cgwire/blender-scripting-geometry-nodes | 47 satırlık tek GN örneği | execute_blender_code ile aynısı | RED (lisanssız, yeni bilgi yok) | — | yok | ★3 · 2025-10-31 |

## 1 Görsel eleştiri döngüsü
- Sıra: sayısal kapı → biçim → görünüş. Görüntü ölçeği/pivotu/topolojiyi kanıtlamaz (#8: FINISHED dönüp hiçbir şey değiştirmeyen operatör, 0.01 ölçek, 14 non-manifold kenar görüntüde görünmez).
- Sayısal kapı (headless `*_for_cli`, görüntüsüz): bbox hedefe ±0.001 m (#8) · non-manifold 0 + is_closed · uygulanmamış ölçek/döndürme yok · havada/kopuk parça yok · pivot bbox içinde · başıboş empty yok (#11) · her nesnede malzeme · mutlak yol yok (#7) · glTF geri okunduğunda mesh > 0 (#8).
- Görünüm: 4 sabit (ön · yan · üst · 3/4 perspektif); #11 4, #12 5, #1 ön/yan/arka/üst kullanıyor. Kamera uzaklığı bbox'tan (#12). Dönel simetride arka = ön, 4 yeter.
- Motor: biçim turları Workbench, düz silüet, saydam/yansıtıcı gizli (#10, #1); Eevee yalnız son turda 1 kahraman görünüm; Cycles yalnız teslim.
- Puan: referans varsa görünüm başına silüet IoU (#1; eşik kaynakta yok → öneri ≥ 0.90 + bbox oranı ±%3). Referans yoksa VLM eleştirisi madde listesi, doğrulayıcı her maddeyi evet/hayır teyit eder (#12). Geçiş = kapı tam PASS ∧ IoU eşiği ∧ açık madde 0.
- Tur tavanı: hiçbir kaynak vermiyor (#12 onaya dek döner). Öneri 3 tur; iki tur üst üste IoU artışı < 0.02 ise dur + DUR raporu. Tur içinde betik düzenlenir, sıfırdan yazılmaz (#12).

## 2 Ürün ışığı hazır profilleri
- #1 tablosu (anahtar:dolgu:kenar güç oranı): ürün 5:1:1.5, nötr 5000K (teyitli) · cam 3:1:1.2 · ahşap 4:1:1.5, 3000K · kumaş 3:1:0.5. Işık uzaklığı = max(boyut×1.5, 1 m). Belirsizse 3 nokta + HDRI dolgu 0.3.
- EK (yalnız arama özeti, zayıf; 3dskillup, artivoxa): dolgu ≈ anahtarın %50'si, kenar ≈ %25; elektronik 1.5:1, yüksek kontrast 4:1+; anahtar geniş yumuşak area, kamera ekseninden 30-45°; HDRI gücü 0.1-0.3 yalnız yansıma için. 5:1 ile 2:1 arası fark tanım farkı (güç oranı vs fotoğrafçı oranı).
- Malzemeye göre: metal/cam → önce neyin yansıdığını kur: kameraya görünmez geniş softbox/gradyan emisyon düzlemleri (Visibility > Camera kapalı), kenar ışığı yansımayı şekillendirir; test mat gri + krom küre. Sırlı seramik (TELVE fincanı) kaynakta yok → öneri ürün profili + iki dikey şerit softbox (uzun vurgu çizgisi). Mat seramik/plastik kaynakta yok → ürün profili, kenar 1.
- HDRI: Poly Haven stüdyo HDRI'si 1k-2k (#6: kademe başı ~4× boyut, indirme ana iş parçacığını dondurur); yeni world olarak bağla, mevcut world ezilmez. Somut ad kaynakta yok; Faz 1 Poly Haven aramasıyla seçilir.

## 3 Web'e taşırken güzellik kaybını önleme
- Kural: görüşten bağımsız olan pişer (diffuse, AO → UV2 lightMap/aoMap), görüşe bağlı olan ortam haritasında kalır (yansıma, parlaklık → PMREM'li HDRI).
- Statik sahne (tezgâh, oda, sabit ürün): tam diffuse lightmap, tek atlas 1024/2048, önce Apply Scale (#14); kazanç iddiası 3-4× FPS masaüstü, 5× mobil, GLB −%15 (#13, kendi ölçümü).
- Scroll'da dönen ürün (#18, web-sahne-desenleri): yön bağımlı ışık pişirilmez (ışık nesneyle döner); yalnız AO pişir + HDRI ortamı. AO pişirilemeyen dinamik nesnede n8ao halfRes (#16).
- Pişmiş PNG [0,1]'e kırpar (#17) → lightmap yoğunluğu < 1 tutulur, lightMapIntensity ile ölçeklenir ya da HDR saklanır; ton eşleme pişirmeye karışmaz.
- AgX eşleşmesi: (1) Blender View Transform AgX, Look None, Exposure 0, Gamma 1. (2) three.js postprocessing varsa renderer.toneMapping = NoToneMapping, HalfFloat buffer, ToneMappingEffect(AGX) zincirin sonunda (#15); yoksa AgXToneMapping. (3) Exposure eşdeğeri yok (#17) → aynı kamera + %18 gri kart + krom küreyle toneMappingExposure taraması, ortalama luminans farkı en küçük değer (öneri; formül kaynakta yok). (4) Eşleşene dek ek LUT/grading yok (#17). (5) Look iki tarafta aynı.

## 4 Dönel simetrik nesneler: silüetten Screw
- Kaynaklarda karşılık yok: 20 kaynağın hiçbiri Screw/Spin/lathe anmıyor. En yakın #1 contour-to-mesh (düz rölyef, dönel değil) ve #4 süperelips kesit loft'u.
- Tarif (Faz 2'de search_manual_docs ile teyit): ön ortografik silüet (fotoğraf ya da gorsel-uret) → eksenin sağ yarısında dış + iç profil (dudak ve taban dahil, tek çizgi) → piksel→mm (bilinen yükseklik, ör. fincan 60 mm) → XZ düzleminde x=0 eksenli vertex zinciri → Screw modifier (360°, Z, viewport 32 / render 64 adım, Merge açık) → Subdivision 1-2 + dudakta crease. İç profil çizilmezse Solidify ~3 mm (öneri).
- Kulp/ağız ayrı: kulp eğri + bevel profili, gövdeye boolean union; cezve ağzı orantılı düzenleme, sap ayrı eğri.
- Doğrulama: Q1 ön görünüm silüet IoU, girdi görseliyle aynı kamera (#1 multiview-fit-loop'un doğal kullanımı).

## 5 Prosedürel malzeme kütüphanesi
- En ucuz yol: malzemeyi bir kez Blender UI'da kur → NodeToPython Script kipi → `.py` tarif (alt gruplar, varsayılanlar, yerleşim dahil) → kütüphaneye kaydet → execute_blender_code ile çağır. Yeni araç yazılmaz.
- Başlangıç kümesi (öneri, TELVE): sırlı seramik, mat seramik, bakır (cezve), pirinç, cam, koyu ahşap, kahve sıvısı/köpük.
- Tarif başlığına Blender sürümü; soket adları sürümle değişir (#12: "Specular" → "Specular IOR Level") → çağırmadan önce canlı `node.inputs` sorgusu (#6 describe_node_type mekanizması).
- Doku gerçekçiliği gerekirse Poly Haven CC0 doku → Principled (#6) prosedürelden ucuz.
- Sınır: NodeToPython UI'dan çalışır, headless dışa aktarım doğrulanmadı; GPL-3.0, üretilen-kod lisans uyarısı kurulum dalgasında okunacak. Düğüm adları için #2 (MIT); #4 procedural-materials NC-ND, yalnız fikir.

## Faz 1 alınacaklar (araç; kurulum ayrı dalga)
1. NodeToPython eklentisi (extensions.blender.org v4.2.0) — #19
2. Poly Haven çekme (api.polyhaven.com, HDRI/doku 1k-2k, CC0) blender_oturum alt komutu; ahujasid sunucusu kurulmaz — #6
3. Sayısal doğrulama betiği (headless `*_for_cli`): Q1 kapı listesinin tamamı — #7 #8 #11
4. Görünüm betiği: 4 Workbench + 1 Eevee, bbox'tan kamera, silüet IoU — #1 #10 #11 #12
5. Headless lightmap/AO pişirme: UV2 "LightMap" + tek atlas + Cycles + denoise, önce Apply Scale — #13 #14
6. Headless betik sözleşmesi: assert + sıfır-dışı çıkış + zaman aşımı + JSON — #4 #11
7. Kontur → profil noktaları yardımcısı (OpenCV) — Q4

## Faz 2 alınacaklar (skill)
1. blender-oturum references: ürün ışığı profilleri tablosu (Q2) — #1
2. Eleştiri döngüsü protokolü: kapı → Workbench 4 görünüm → Eevee; 3 tur; madde-madde doğrulayıcı; betik düzenlenir — #8 #12
3. Hata mesajıyla search_api_docs yeniden sorgu + düğüm yazmadan önce canlı soket sorgusu — #2 #6 #12
4. Lab MCP `_for_cli` + örnek kontrol listesi kullanımı (ZATEN VAR farkı) — #7
5. Silüetten dönel model tarifi (Screw) — Q4
6. Malzeme tarif kütüphanesi düzeni + sürüm başlığı — #19
7. Export kuralı: transform_apply → glTF +Y; glTF bütçe 500k üçgen tavanı (#8) — #4 #8
8. three-agent-skills eksik kategorileri (GLTF Draco/KTX2/meshopt, dispose, instancing, koşullu render), lisans teyidi şartlı — #5
9. web-sahne-desenleri: pişir/ortam haritası kuralı + AgX eşleme adımları + #18 sayıları; Faz 3'te TELVE'de ölçülür — #15-#18
