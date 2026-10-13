# BLENDER-3 notlar B — hard-surface · geometry nodes

Kaynak: `C:\Projeler\.video-cache\<id>\segmentler.jsonl` (kare yok, yalnız transkript). Ölçek varsayımı: 1 BU = 1 m; ürün 8–20 cm.
Biçim: mekanizma (neden) · ~zaman · bpy karşılığı · sayısal öneri. "doğrula" = 5.2.1'de soket/özellik adı sınanmadı.

## Ml2t8uxPAQU · CG Boost · 6 hard-surface hilesi
- Düşük poligon kafes + Subsurf: az köşeli kontrol ağı biçimi yönetilebilir tutar, pürüzsüzlüğü modifier üretir · ~0:22–1:23 · `primitive_cylinder_add(vertices=16)` + inset/bridge faces, `modifiers.new(type='SUBSURF')` · silindir 16 köşe, subsurf 2.
- Keskin kenarı açıya göre seç, crease ver: yüz açısı eşiği sert kenarları otomatik bulur; crease subsurf'ün o kenarı yumuşatmasını engeller · ~2:25 · `bpy.ops.mesh.edges_select_sharp(sharpness=radians(30))` → mesh `crease_edge` float EDGE özniteliği = 1.0; subsurf `use_creases=True` · crease 1.0 (yumuşak kalacak loop'larda 0).
- Crease'li kenarlara bevel weight + Bevel(limit=WEIGHT) + harden normals: subsurf'ün yuvarladığı köşeye ince, ışığı yakalayan pah ekler; harden normals düz yüzlerde gölge bulanıklığını keser · ~3:26 · `bevel_weight_edge` özniteliği = 1.0; `BEVEL: limit_method='WEIGHT', harden_normals=True` · ağırlık 1.0.
- Modifier sabitleme: Bevel/Subsurf'ü sona sabitleyince sonradan eklenen Mirror otomatik önce çalışır, simetri dikişinde çimdiklenme olmaz · ~3:58 · `mod.use_pin_to_last = True` (4.2+) · Mirror her zaman Subsurf/Bevel'den önce.
- Kablo = eğri + bevel derinliği, noktaları elle değil çizimle üret; yüzeye yapıştırma seçeneği · ~4:34 · `curve.data.bevel_depth`, `bevel_resolution`; headless'ta noktaları kodla ver · ürün kablosu derinlik 1.5–3 mm, çözünürlük 2–4.
- Dik açılı boru birleşimi: iki silindir ucunu loop köprüsüyle bağla, ara kesit + yumuşaklık dirsek oluşturur · ~5:38 · `bpy.ops.mesh.bridge_edge_loops(number_cuts=5, smoothness=1.0)` (edit modu; doğrula) · cuts 5.
- Ek parçayı gövdeye oturtma: origin'i taban loop'una al, yüzeye hizalı yapıştır, sonra vertex grubu ile sınırlı Shrinkwrap'ı yığının başına koy; Data Transfer ile gövdenin normallerini dikiş bölgesine aktar → birleşim izi kaybolur · ~6:07–8:44 · `SHRINKWRAP: target, vertex_group`; `DATA_TRANSFER: object, use_loop_data=True, data_types_loops={'CUSTOM_NORMAL'}, loop_mapping='POLYINTERP_NEAREST', vertex_group` · Shrinkwrap sıra 0, Data Transfer en sonda.

## nsTjnQ067sw · CG Boost · hard-surface temelleri (kupa robotu)
- Tamamen dörtgen küre tabanı: kutu-küre (quad sphere) subsurf'te kutup sıkışması yapmaz · ~0:40–1:45 · Extra Objects eklentisi headless'ta yoksa: küp + `SUBSURF levels=2` uygula + `CAST factor=1` (doğrula) · alt bölüm 4 eşdeğeri.
- Kabuk yığını: Subsurf(viewport=render=2) → Solidify(içe) → Bevel(küçük, +1 segment, harden normals) + otomatik pürüzsüz · ~2:49–3:52 · `SUBSURF levels=2, render_levels=2`; `SOLIDIFY thickness, offset=-1`; `BEVEL segments=2–3, harden_normals=True` · kalınlık 1.5–2.5 mm.
- Panel/ayırma çizgisi: loop kes, yüz halkasını ayrı mesh'e böl (Y) → gerçek boşluk, renk ayrımı ve malzeme yuvası doğal olur · ~4:55 · `bpy.ops.mesh.loopcut_slide` / `bpy.ops.mesh.split()` · ayrı parça ayrı malzeme.
- Modifier'dan önce ölçek+dönüş uygula: uygulanmamış ölçek bevel genişliğini eksenlere göre çarpıtır, Shrinkwrap projeksiyonu yanlış eksende çalışır · ~6:48, ~16:48, ~25:13 · `bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)` · her parça için zorunlu.
- Sap: köşe loop'larına önce mesh bevel, yan kenarlara crease; Subsurf'ten SONRA Bevel modifier; faceting kalırsa subsurf 3 · ~7:51–8:51 · `bpy.ops.mesh.bevel`, `crease_edge`, yığın sırası SUBSURF→BEVEL · subsurf 2 (gerekirse 3).
- Gövdeye bağlantı: uç yüzlere vertex grubu, Shrinkwrap `wrap_method='PROJECT'`, tek eksen (± yön), küçük offset ile kesişmeyi önle · ~9:54–10:56, ~14:17–15:22 · `use_project_x=True, use_negative_direction=True, offset` · offset 0.1–0.3 mm.
- İç parçayı korumak: küçük bevel'de `use_clamp_overlap=False`; iç lens kenarı da pahlanıyorsa açı sınırını yükselt · ~13:17–14:17 · `BEVEL limit_method='ANGLE', angle_limit=radians(60)` · açı >50°.
- Düz parça → subsurf yok, yalnız Bevel(2 segment)+harden normals; kesik detay = Boolean(brush/slice), Bevel Boolean'ın ALTINDA · ~18:52–20:55 · `BOOLEAN operation='DIFFERENCE'`, yığın BOOLEAN→BEVEL · küçük silindir 8 köşe (~16:48).
- Tekrar eden parça: bağlı kopya (aynı mesh) + modifier'ı seçililere kopyala; ayna = 3B imleç etrafında X'te ölçek −1 · ~20:55–22:59 · `obj.copy()` (data paylaşılır), `bpy.ops.object.modifier_copy_to_selected` · —
- Etiket/decal: 10 kesimli düzlemden harf yüzlerini bırak, Subsurf(SIMPLE) ile yoğunluk ver, Shrinkwrap project ile gövdeye yasla · ~23:09–25:13 · `SUBSURF subdivision_type='SIMPLE'` + `SHRINKWRAP` · offset ~0.1 mm.

## MC_MXaGZfqM · Grant Abbitt (Steven) · GN prosedürel taş yol
- Eğriyi zemine oturt: önce yukarı kaldır, sonra aşağı ışın at, isabet konumunu yeni konum yap · ~2:00–3:00 · `GeometryNodeObjectInfo` → `GeometryNodeRaycast` ("Target Geometry", çıkış "Hit Position") → `GeometryNodeSetPosition` ("Position") · ön kaldırma Z=+10 m, ışın yönü (0,0,−1).
- Yeniden örnekle: nokta sayısı hem zemine uyumu hem taş aralığını belirler · ~4:05 · `GeometryNodeResampleCurve` (Count; mod enum/menü soketi doğrula) · 15, profil için 4–5 (~7:30).
- Şerit üret: çizgi profiliyle loft; tek değer → Combine XYZ ile başlangıç −w, bitiş +w · ~5:12–6:14 · `GeometryNodeCurveToMesh` + `GeometryNodeCurvePrimitiveLine` ("Start","End") + `ShaderNodeMath(MULTIPLY, −1)` + `ShaderNodeCombineXYZ`; eğim için `GeometryNodeSetCurveTilt`; yüz yönünü kontrol et · genişlik 1–1.5.
- Düzensiz parke: rastgele seçili dörtgenleri üçgenle, sonra dual mesh → altıgen/çokgen karışımı; rastgele yüz sil · ~8:52–11:05 · `GeometryNodeTriangulate` (Beauty) + `FunctionNodeRandomValue` (BOOLEAN, Probability) + `GeometryNodeDualMesh` + `GeometryNodeDeleteGeometry` (domain FACE) · olasılık 0.6.
- Inset taklidi: sıfır ofsetli extrude + yalnız "Top" seçimine Scale Elements; Separate Geometry ile "Top"=taş, "Inverted"=derz · ~11:50–13:54 · `GeometryNodeExtrudeMesh` (Offset Scale=0, çıkış "Top") → `GeometryNodeScaleElements` → `GeometryNodeSeparateGeometry` (FACE) · ölçek rastgele 0.90–0.95. Ürün için: panel/ızgara deliği deseni.
- Kalınlık: extrude + önceki geometriyle birleştir (alt kapak), ters yüzleri çevir, mesafeyle birleştir · ~14:37–15:38 · `GeometryNodeJoinGeometry` → `GeometryNodeFlipFaces` → `GeometryNodeMergeByDistance` · kalınlık rastgele 0.15–0.25.
- Destek loop + subsurf: önce Subdivide Mesh (kenar loop'ları biçimi tutar), sonra Subdivision Surface · ~17:25 · `GeometryNodeSubdivideMesh` (Level 1) → `GeometryNodeSubdivisionSurface` (Level 2) · —
- Gürültüyle hafif bozma: noise → −0.5 merkezle → Vector Math SCALE ile genlik; üst yüz eğimi ve yüzey pürüzü ayrı · ~15:38–19:14 · `ShaderNodeTexNoise` (Scale 20) + `ShaderNodeVectorMath` (SUBTRACT 0.5, SCALE) → SetPosition "Offset" · genlik 0.05 (eğim 0.3); sonra `GeometryNodeSetShadeSmooth`, `GeometryNodeSetMaterial` (Join'den ÖNCE ~23:06).
- Dağıtım/örnekleme: derz yüzlerine nokta saç, koleksiyondan rastgele örnek; yakınlık ile yoğunluk maskesi; havada kalmayı küçük negatif Z ile göm · ~19:45–24:07 · `GeometryNodeDistributePointsOnFaces` (Density) + `GeometryNodeInstanceOnPoints` (Pick Instance) + `GeometryNodeCollectionInfo` (Separate/Reset Children) + `GeometryNodeProximity` · yoğunluk 50, ölçek 0.2–0.5.

## 9f-B8xk0peA · Grant Abbitt · yosunlu kaya (shader düğümü; GN değil)
- Yöne göre maske: normalin Z bileşeni + renk rampası → üstte malzeme A, altta B (yalnız yüksekliğe göre değil, şekli izler) · ~1:32–3:34 · `ShaderNodeTexCoord` ("Normal") → `ShaderNodeSeparateXYZ` ("Z") → `ShaderNodeValToRGB` → `ShaderNodeMixShader` "Fac" (~7:07) · rampa siyah ~0.4, beyaz ~0.7 (doğrula görsel).
- UV'siz doku: görüntü dokusunda kutu projeksiyonu + küçük harman, dikişsiz sonuç · ~5:23–6:23 · `ShaderNodeTexImage.projection='BOX', projection_blend=0.1`, vektör = Generated · harman 0.1.
- Maske yerel koordinatta: dönüş uygulanmazsa "üst" yanlış yöne düşer · ~8:07 · `transform_apply(rotation=True)` · —
- Rock Generator otomatik pürüzsüzü kapatıldı (istenmeyen gölgelenme) · ~1:00 · Extra Objects eklentisi; headless'ta güvenme · —

## GN kalıbı (headless bpy, 5.x)
```python
import bpy
obj = bpy.data.objects["Govde"]
ng = bpy.data.node_groups.new("PanelInset", 'GeometryNodeTree')
ng.interface.new_socket("Geometry", in_out='INPUT', socket_type='NodeSocketGeometry')
ng.interface.new_socket("Geometry", in_out='OUTPUT', socket_type='NodeSocketGeometry')
s = ng.interface.new_socket("Olcek", in_out='INPUT', socket_type='NodeSocketFloat'); s.default_value = 0.92
N, L = ng.nodes, ng.links
gi, go = N.new('NodeGroupInput'), N.new('NodeGroupOutput')
ex = N.new('GeometryNodeExtrudeMesh'); ex.inputs['Offset Scale'].default_value = 0.0
se = N.new('GeometryNodeScaleElements')
L.new(gi.outputs['Geometry'], ex.inputs['Mesh'])
L.new(ex.outputs['Mesh'], se.inputs['Geometry'])
L.new(ex.outputs['Top'], se.inputs['Selection'])
L.new(gi.outputs['Olcek'], se.inputs['Scale'])
L.new(se.outputs['Geometry'], go.inputs['Geometry'])
mod = obj.modifiers.new("GN", 'NODES'); mod.node_group = ng
mod[s.identifier] = 0.9  # modifier tarafı değer (identifier ör. "Socket_2"; doğrula)
with bpy.context.temp_override(object=obj): bpy.ops.object.modifier_apply(modifier="GN")
```
Not: örnekler (instance) GLB'ye gitmeden `GeometryNodeRealizeInstances` ile gerçekleştirilmeli ya da exporter'ın GPU instancing seçeneği kullanılmalı (doğrula).

## tarif varsayılan adayları (8–20 cm ürün)
1. Modifier'dan önce `transform_apply(rotation=True, scale=True)`; ölçek (1,1,1) değilse dur — kanıt nsTjnQ067sw ~6:48, ~25:13; 9f-B8xk0peA ~8:07. GLB: etkisiz, yalnız doğruluk.
2. Bevel genişliği = en büyük boyutun %0.6'sı, sınırlar 0.5–1.5 mm; `segments=2` (eğri yüzde 3); `limit_method='ANGLE', angle_limit=30°` (iç parça varsa 60°); `use_clamp_overlap=False` — kanıt nsTjnQ067sw ~3:52, ~13:17–14:17, ~18:52. GLB: her sert kenar ×2–3 şerit; düşük polide 1 segment + harden normals.
3. Her bevel'de `harden_normals=True` (5.x'te auto smooth bayrağı gerekmez; doğrula) — kanıt Ml2t8uxPAQU ~3:26, nsTjnQ067sw ~3:52. GLB: özel normaller `export_normals=True` ile taşınır, poli maliyeti yok — düşük polide en ucuz kalite kazancı.
4. Pürüzsüz gölgeleme açıya göre: `mesh.shade_smooth()` + `mesh.set_sharp_from_angle(angle=radians(30))` (4.1+ API; doğrula) — kanıt nsTjnQ067sw ~2:49, ~18:52. GLB: keskin kenarlar köşe bölünmesiyle dışa aktarılır, küçük köşe artışı.
5. Eğri yüzlü parça: düşük kafes (silindir 16, küçük 8 köşe) + `SUBSURF levels=2, render_levels=2` + sert kenarlarda `crease_edge=1.0`; düz parçada subsurf yok — kanıt Ml2t8uxPAQU ~0:22–2:25, nsTjnQ067sw ~2:49, ~16:48, ~18:52. GLB: seviye 2 = yüz ×16; web için levels=1 ve crease yerine destek loop'u (crease dışa aktarılmaz).
6. Yığın sırası sabit: Shrinkwrap(vgroup) → Mirror → Boolean → Subsurf → Bevel → Data Transfer/WeightedNormal; Bevel ve Subsurf `use_pin_to_last=True` — kanıt Ml2t8uxPAQU ~3:58, ~7:08; nsTjnQ067sw ~8:51, ~20:55. GLB: tümü `export_apply=True` ile uygulanır.
7. Ek parça bağlantısı: uç yüzler vertex grubunda, `SHRINKWRAP wrap_method='PROJECT'`, tek eksen, `offset=0.0002` (0.2 mm); dikişe `DATA_TRANSFER CUSTOM_NORMAL, POLYINTERP_NEAREST` aynı grupla — kanıt nsTjnQ067sw ~9:54–10:56; Ml2t8uxPAQU ~7:43. GLB: normal aktarımı sıfır poli maliyetle dikişi gizler.
8. Panel çizgisi/ayrı renk: loop'u ayrı mesh'e böl (split) veya GN inset (extrude 0 + ScaleElements 0.90–0.95) — kanıt nsTjnQ067sw ~4:55; MC_MXaGZfqM ~11:50. GLB: ayrı malzeme = ayrı primitive/draw call; ürün başına ≤4 malzeme.

## kontrol listesi
- Her nesnede `scale == (1,1,1)` ve `rotation_euler == 0` (uygulanmış) mı?
- Boyut doğrulama: `obj.dimensions` 0.08–0.20 m aralığında mı (BU = m, glTF metre)?
- Yüz yönü: `bmesh` ile `recalc_face_normals` sonrası ters yüz sayısı 0 mı (GN extrude+join sonrası Flip Faces gerekebilir; MC_MXaGZfqM ~14:37)?
- Manifold: `bpy.ops.mesh.select_non_manifold()` ile açık kenar sayısı 0 mı (solidify/decal düzlemleri hariç)?
- Çakışık köşe: `bmesh.ops.remove_doubles(dist=1e-5)` sonrası köşe sayısı değişmedi mi?
- Subsurf/kutup: subsurf'lü mesh'te üçgen/n-gon oranı düşük, dörtgen ağırlıklı mı (quad sphere ilkesi)?
- Kesişme: Shrinkwrap'lı parçalar gövdeye 0.1–0.3 mm offsetle mi duruyor, gömülme/havada kalma yok mu?
- GLB bütçesi: uygulanmış toplam üçgen sayısı hedefin altında mı (ör. ≤50k), örnekler realize edildi mi, malzeme sayısı ≤4 mü?
