# Web aktarım: GLB, pişirme, AgX

Kaynak: 7-blender.md Q3 + Faz 2 madde 7, 9. Web sahnesi tarafı: web-sahne-desenleri skill'i.

## Export

| adım | kural | kaynak |
|---|---|---|
| 1 | `transform_apply` (döndürme + ölçek) → glTF +Y (`export_yup=True`), GLB | #4 |
| 2 | Bütçe: toplam ≤ 500k üçgen | #8 |
| 3 | `tools/blender_dogrula.py <blend> --glb x.glb` — geri okuma, 0 mesh = FAIL | #8 |
| 4 | `tools/glb_hat.py x.glb` — meshopt + webp, validate hatası exit 1 | ARAC-1 |

## Pişirme kararı

| sahne | ne pişer | ne kalır | kaynak |
|---|---|---|---|
| statik (tezgâh, oda, sabit ürün) | `blender_pisir.py --mod isik` tam diffuse, tek atlas 1024/2048, önce Apply Scale | yansıma → HDRI | #13 #14 |
| scroll'da dönen ürün | yalnız `--mod ao` (ışık nesneyle döner) | ışık + yansıma → HDRI; dinamikte n8ao | #16 #18 |
| yansıma, parlaklık | pişmez | PMREM'li HDRI | Q3 |

Yoğunluk: 8 bit PNG [0,1]'e kırpar (#17); araç p99.9'u 0.9'a ölçekler, `lightMapIntensity` geri çarpar. **lightMapIntensity > 2** ise 8 bitte bantlanır → `blender_pisir` SONUC'ta `uyari` verir; `--hdr` (EXR) ya da `--png16` (16 bit PNG) ile yeniden pişir (öneri eşik 2).

## AgX eşleme (sıra değişmez)

1. Blender: View Transform AgX, Look None, Exposure 0, Gamma 1. (#15 #17)
2. three.js: postprocessing varsa `renderer.toneMapping = NoToneMapping`, HalfFloat buffer, `ToneMappingEffect(AGX)` zincirin sonunda; yoksa `AgXToneMapping`. (#15)
3. Exposure eşdeğeri yok (#17) → aynı kamera + %18 gri kart + krom küre; `toneMappingExposure` taraması, ortalama luminans farkı en küçük değer. (öneri)
4. Eşleşene dek ek LUT/grading yok. (#17)
5. Look iki tarafta aynı. (#17)

## three.js tarafı

| konu | kural | kaynak |
|---|---|---|
| ortam | HDRI → `PMREMGenerator.fromEquirectangular` → `scene.environment` | Q3 |
| lightmap | `material.lightMap = tex; tex.channel = 1; tex.flipY = false; material.lightMapIntensity = <SONUC>` | #14 (flipY) · öneri (channel) |
| ton eşleme | hattın en sonunda, bir kez | #15 |
