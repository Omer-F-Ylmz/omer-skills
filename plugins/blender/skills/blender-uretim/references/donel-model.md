# Dönel model: silüetten Screw

Fincan, kupa, cezve gövdesi, moka gövdesi gibi dönel simetrik nesneler. Kaynak: 7-blender.md Q4 (kaynaklarda Screw yok → akış bizim tarifimiz) + `tools/kontur_profil.py`.

## Akış

| # | adım | araç / ayar | kaynak |
|---|---|---|---|
| 1 | Yandan profil silüeti: fotoğraf ya da `gorsel_uret` ("tam yandan ortografik, siyah silüet, beyaz zemin, perspektifsiz, gölgesiz") | gorsel-uret skill'i | Q4 |
| 2 | Kulp yönü: `--kulp sag\|sol\|yok`; eksen üst/alt %15 bant orta noktalarının medyanı (kulp bandı dışı) | kontur_profil | ARAC-2 |
| 3 | `uv run tools/kontur_profil.py <siluet.png> --yukseklik-mm N --kulp sag [--ic-profil] [--blend x.blend]` — N `olculer.md`'den | kontur_profil | ARAC-2 |
| 4 | Profil XZ'de x=0 eksenli zincir → Screw 360°, Z, viewport 32 / render 64 adım, Merge açık | araç kurar | Q4 |
| 5 | Subdivision 1-2 + dudakta crease; iç profil yoksa Solidify ~3 mm | elle | Q4 (Solidify öneri) |
| 6 | Gövde IoU: araç ≥ 0.95 değilse exit 1 → silüeti düzelt, eşiği düşürme | kontur_profil | ARAC-2 |
| 7 | Q1 ön görünüm silüet IoU: girdiyle aynı kamera (`blender_gorunum --referans`) | blender_gorunum | #1 |

## Ayrı parçalar (gövdeye sonra)

| parça | tarif | kaynak |
|---|---|---|
| kulp (fincan/kupa) | 3 noktalı Bezier eğri (üst bağlantı → dış kavis → alt bağlantı), `bevel_mode="ROUND"`, `bevel_depth` = kalınlık/2; mesh'e çevir → Boolean Union ile gövde | Q4 |
| cezve sapı | gövdeden yatay çıkan ayrı eğri, uçta hafif yukarı; bevel yuvarlak, uca doğru taper; boy `olculer.md` "sap" | Q4 |
| cezve ağzı (döküm burnu) | dudak halkasında bir yandaki 3-5 vertex seçilir → orantılı düzenleme (Sharp, yarıçap ≈ ağız çapının 1/3'ü) ile dışa + hafif yukarı 3-6 mm | Q4 (oranlar öneri) |
| tabak | ayrı profil → aynı Screw akışı | öneri |

Eğri tarifinin kodu (kulp):

```python
cu = bpy.data.curves.new("GEO-KulpEgri", "CURVE"); cu.dimensions = "3D"
sp = cu.splines.new("BEZIER"); sp.bezier_points.add(2)
for bp, co in zip(sp.bezier_points, [(r, 0, z_ust), (r + w, 0, z_orta), (r, 0, z_alt)]):
    bp.co = co; bp.handle_left_type = bp.handle_right_type = "AUTO"
cu.bevel_mode, cu.bevel_depth, cu.bevel_resolution = "ROUND", kalinlik / 2, 4
```
Yazmadan önce `cu.bl_rna.properties` canlı sorgusu; sürüm farkında `search_api_docs`.
