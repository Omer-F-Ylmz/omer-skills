# Eğitimlerden mekanizmalar (BLENDER-3)

18 eğitim videosu (Blender Guru, CG Boost, Grant Abbitt, Default Cube, Ryan King Art, Vishnu Menon, CGMatter, rileyb3d, Joey Carlino, J Derinor) ve Blender 5.2 manual'ı incelendi. Burada yalnız mekanizmalar var, metin kopyası yok. Kanıt satırları (video id · zaman) wt `docs/blender-3/notlar-{A..D}.md` içinde.

## tarif.py'nin kendiliğinden uyguladıkları (`BLENDER_KALITE=0` hepsini kapatır)
- Oto kamera 85 mm. Mesafe FOV'dan hesaplanır, kadraj doluluğu aynı kalır. `clip_start` 0.01. DOF f/4 ve odak ürün merkezindedir. Geniş açı yakın kenarı şişirir, f/4 ise ürünü keskin tutarken fonu yumuşatır.
- Kenar pahı: `bevel` verilmemiş küp, silindir ve koniye en büyük boyutun %0.6'sı kadar pah, 2 segment ve `harden_normals` uygulanır. Keskin kenar ışık yakalamaz, ince pah vurgu çizgisi verir. Düzleme (zemine) uygulanmaz.
- Anim anahtarları LINEAR'dır. Turntable sabit hızla döner, kullanıcı tercihi işlem sonunda geri yüklenir.
- EEVEE'de raytracing açılır (5.x varsayılanı kapalıdır). RT ve Fast GI tam çözünürlüktedir: FGI 4 ışın ve 16 adım, gölge 2 ışın ve 8 adım. 384 px'de yaklaşık +0.09 sn tutar.
- Cycles'ta sekme sınırı 6 (diffuse 2, glossy 3) ve `sample_clamp_indirect` 5'tir. Stüdyo ürününde süre yaklaşık %21 kısalır, ateşböceği gürültüsü kesilir.
- Alınmayan: AgX "Medium High Contrast" look. Sırlı beyaz seramikte ≥250 piksel oranı %2.04'e çıktı ve yanma kapısını (%2) aştı.

## Spec'te elle seçilecekler
- **Işık:** World gücü düşük kalır. Dolgu world'den değil hedefli lambadan gelir. Anahtar ışığın boyu ürünün 1.5–2 katı, uzaklığı 3–4 katıdır. Dolgu anahtarın 0.25–0.4'ü, kenar ışığı 0.5–1 katıdır. Her ışık tek başına bir amaca hizmet etmelidir. Sonsuz fon için `isik_kur.kivrimli_zemin` kullanılır; köşe yarıçapı yaklaşık ürün yüksekliği kadardır.
- **Malzeme:** Metallic yalnız 0 ya da 1 olur, IOR ve specular varsayılanda kalır. Pürüzlülük: sırlı seramik 0.05–0.15, mat seramik 0.4–0.6, pirinç/bakır metal 0.2–0.35. Pürüzlülükte ±0.05 procedural varyasyon (Noise → Map Range) "CG temizliği"ni kırar.
- **Modelleme:** Modifier'dan önce ölçek uygulanır. Eğri parçada düşük kafes + subsurf 2 kullanılır, düz parçada subsurf olmaz. Modifier sırası Boolean → Subsurf → Bevel → WeightedNormal'dir. Panel çizgisi için ayrı malzeme veya inset kullanılır. GLB için ürün başına en fazla 4 malzeme.
- **Kamera:** Stüdyoda 10–20° yukarıdan, kahraman kadrajında 0 ile −10° arasından çekilir. Roll 0°'dır. Dikey çizgiler için tilt değil `shift_y` kullanılır. Ürün kadraj yüksekliğinin %60–70'ini doldurur.
- **Turntable:** Dönen şey kamera değil üründür. 0° kare 1'e, 360° kare N+1'e konur, render 1..N alınır; böylece dikişsiz döngü olur ve ilk ile son kare aynı çıkmaz. Hareket bulanıklığı kapalıdır. Cycles'ta `use_persistent_data` açılır.
- **Render:** Cycles kahraman çekiminde 128–256 örnek, adaptive 0.01 ve OIDN (albedo+normal) kullanılır. Tüm açılar tek `blender -b` sürecinde render edilir, çünkü shader derlemesi her ayar değişiminde tekrar ödenir.
- **Geometry Nodes (headless):** `bpy.data.node_groups.new(type="GeometryNodeTree")` → `interface.new_socket` (Geometry giriş/çıkış) → `modifiers.new(type="NODES").node_group = ng`. Tekrar eden dağıtım işleri (taş, vida, perçin) için kullanılır. GLB'den önce örnekler realize edilir.
- **Rig:** Yalnız deform kemikleri dışa aktarılır. Ağırlık etkisi en fazla 4 kemikten gelir. Basit IK zinciri 2 kemiktir.
- **GLB:** Modifier'lar uygulanır, procedural malzeme bake edilir, yalnız Principled + Image Texture kalır. Doku WEBP olur. Draco kullanılıyorsa istemcide çözücü olmalıdır.

## Render öncesi kontrol listesi
1. Ölçek (1,1,1), ürün 0.08–0.20 m.
2. Kadraj: ürün köşeleri kadraj içinde, doluluk %60–70, roll 0.
3. Üründe kırpılmış beyaz yok, gövdenin bir yanı daha koyu, temas gölgesi var.
4. Fonda ufuk çizgisi yok, fon eşit aydınlanmış.
5. Metallic 0/1, veri dokuları Non-Color.
6. Ters normal 0, açık kenar 0 (decal/düzlem hariç).
7. Cycles'ta samples 4096'da bırakılmamış, denoise açık. EEVEE'de raytracing açık.
8. Turntable: kare 1 = kare N+1 açısı, LINEAR. GLB'de üçgen ve malzeme bütçesi tutuyor.
